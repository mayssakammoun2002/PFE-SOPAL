#!/usr/bin/env python3
# ============================================================
#  backend_sopal_optimised.py  —  VERSION CORRIGÉE v3.0
#  FastAPI + RAG Local + Ollama (Phi-3 / OpenHermes)
#
#  ✅ CORRECTION PRINCIPALE : STREAMING ajouté
#  ✅ Timeout frontend 30s → résolu avec SSE streaming
#  ✅ Prompt raccourci pour Phi-3
#  ✅ Pas de clé API — tout tourne en local
# ============================================================

import json
import os
import logging
import asyncio
from pathlib import Path
from typing import Optional, List
from datetime import datetime
import hashlib

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from functools import lru_cache

# LangChain imports
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# ─── Logging Setup ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-8s] %(name)s → %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("sopal_rag")

# ─── FastAPI App ────────────────────────────────────────────
app = FastAPI(
    title="SOPAL RAG Chatbot API",
    description="RAG Local optimisé avec Phi-3/OpenHermes — Défauthèque FA0214",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Configuration ──────────────────────────────────────────
OLLAMA_URL   = os.getenv("OLLAMA_URL",   "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")
KB_PATH      = os.getenv("KB_PATH",      "02_KNOWLEDGE_BASE.json")
EMBED_MODEL  = os.getenv("EMBED_MODEL",  "all-MiniLM-L6-v2")

CACHE_SIZE     = 1000
RAG_TOP_K      = 3
LLM_TEMPERATURE = 0.3
LLM_MAX_TOKENS  = 150   # ← réduit (était 200) pour aller plus vite
LLM_TIMEOUT     = 60    # ← timeout Ollama côté serveur

# Globales
vectorstore:     Optional[FAISS]               = None
embeddings_model: Optional[HuggingFaceEmbeddings] = None
response_cache:  dict = {}


# ════════════════════════════════════════════════════════════
#  1. KNOWLEDGE BASE
# ════════════════════════════════════════════════════════════

def load_knowledge_base(path: str) -> List[Document]:
    kb_file = Path(path)
    if not kb_file.exists():
        log.warning(f"KB non trouvée: {path} — utilisation fallback")
        return get_fallback_documents()

    with open(kb_file, encoding="utf-8") as f:
        data = json.load(f)

    defects = data.get("defauthèque", {}).get("defects", [])
    docs = []

    for d in defects:
        defaut_id   = d.get("id")
        defaut_name = d.get("fr_name", "Unknown")

        # 1️⃣ Description
        docs.append(Document(
            page_content=(
                f"Défaut: {defaut_name}\n"
                f"Type: {d.get('category', 'N/A')}\n"
                f"Description: {d.get('description', '')}\n"
            ),
            metadata={"defaut_id": defaut_id, "defaut_name": defaut_name, "section": "description"}
        ))

        # 2️⃣ Causes
        causes = d.get("probable_causes", [])
        if causes:
            docs.append(Document(
                page_content=(
                        f"Causes du défaut '{defaut_name}':\n" +
                        "\n".join(f"  • {c}" for c in causes)
                ),
                metadata={"defaut_id": defaut_id, "defaut_name": defaut_name, "section": "causes"}
            ))

        # 3️⃣ Remèdes
        remedies = d.get("remedies", [])
        if remedies:
            txt = f"Remèdes pour '{defaut_name}':\n"
            for r in remedies:
                txt += (
                    f"\nÉtape {r.get('step')}: {r.get('action')}\n"
                    f"  Paramètre: {r.get('parameter', 'N/A')}\n"
                    f"  Unité: {r.get('unit', 'N/A')}"
                )
            docs.append(Document(
                page_content=txt,
                metadata={"defaut_id": defaut_id, "defaut_name": defaut_name, "section": "remedies"}
            ))

        # 4️⃣ Critères d'acceptation
        acceptance = d.get("acceptance_criteria", {})
        if acceptance:
            acc_doc = (
                f"Critères d'acceptation pour '{defaut_name}':\n"
                f"  Pièce référence: {acceptance.get('reference_part', 'N/A')}\n"
                f"  Limit: {acceptance.get('limit', 'N/A')}\n"
                f"  Zones: {', '.join(acceptance.get('zones', []))}"
            )
            if "special_case" in acceptance:
                acc_doc += f"\n  Cas spécial: {acceptance['special_case']}"
            docs.append(Document(
                page_content=acc_doc,
                metadata={"defaut_id": defaut_id, "defaut_name": defaut_name, "section": "acceptance"}
            ))

        # 5️⃣ Tips opérateur
        tips = d.get("operator_tips", [])
        if tips:
            docs.append(Document(
                page_content=(
                        f"Conseils pour '{defaut_name}':\n" +
                        "\n".join(f"  💡 {t}" for t in tips)
                ),
                metadata={"defaut_id": defaut_id, "defaut_name": defaut_name, "section": "tips"}
            ))

    log.info(f"✅ KB chargée: {len(defects)} défauts → {len(docs)} documents")
    return docs


def get_fallback_documents() -> List[Document]:
    return [
        Document(
            page_content=(
                "Défaut: Criques ou fissures\n"
                "Causes: Température métal fondu, température moule, composition Zn/Mg.\n"
                "Remèdes: 1) Vérifier température coulée (°C) "
                "2) Vérifier température moule (°C) "
                "3) Vérifier proportion Zn/Mg"
            ),
            metadata={"defaut_name": "Criques", "section": "general"}
        ),
    ]


# ════════════════════════════════════════════════════════════
#  2. SYSTEM PROMPT  (raccourci pour Phi-3 → plus rapide)
# ════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """Expert fonderie SOPAL. Réponds en français, max 100 mots.
Utilise UNIQUEMENT le contexte fourni. Numérote les étapes des remèdes.
Si l'info n'existe pas, dis-le. N'invente rien."""


def build_prompt(context: str, defaut_context: Optional[str], question: str) -> str:
    defaut_line = f"\nDéfaut en cours: {defaut_context}" if defaut_context else ""
    return (
        f"{SYSTEM_PROMPT}\n"
        f"\n{'='*40}\n"
        f"CONTEXTE:\n{context}\n"
        f"{'='*40}"
        f"{defaut_line}\n"
        f"\nQuestion: {question}\n"
        f"\nRéponse:"
    )


# ════════════════════════════════════════════════════════════
#  3. CACHE HELPERS
# ════════════════════════════════════════════════════════════

@lru_cache(maxsize=CACHE_SIZE)
def _hash_prompt(prompt: str) -> str:
    return hashlib.md5(prompt.encode()).hexdigest()


def get_rag_context(message: str, defaut_context: Optional[str]):
    """Récupère les documents RAG et construit le contexte."""
    search_query = f"{defaut_context} {message}" if defaut_context else message
    results = vectorstore.similarity_search(search_query, k=RAG_TOP_K)

    context_parts = []
    source_names = set()
    for r in results:
        context_parts.append(r.page_content)
        if name := r.metadata.get("defaut_name"):
            source_names.add(name)

    context = "\n\n---\n\n".join(context_parts) or "Pas de contexte pertinent trouvé"
    return context, list(source_names)


# ════════════════════════════════════════════════════════════
#  4. STARTUP
# ════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    global vectorstore, embeddings_model

    log.info("🚀 Démarrage SOPAL RAG Backend v3.0...")
    start = datetime.now()

    log.info(f"📦 Chargement embeddings: {EMBED_MODEL}")
    embeddings_model = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    docs = load_knowledge_base(KB_PATH)

    log.info("🔍 Construction index FAISS...")
    vectorstore = FAISS.from_documents(docs, embeddings_model)
    log.info(f"   ✅ FAISS prêt: {vectorstore.index.ntotal} vecteurs")

    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        models = [m["name"] for m in r.json().get("models", [])]
        if any(OLLAMA_MODEL.split(":")[0] in m for m in models):
            log.info(f"✅ Ollama OK — {OLLAMA_MODEL} disponible")
        else:
            log.warning(f"⚠️ Modèle {OLLAMA_MODEL} non trouvé. Lancez: ollama pull {OLLAMA_MODEL}")
    except Exception as e:
        log.warning(f"⚠️ Ollama inaccessible: {e}")

    elapsed = (datetime.now() - start).total_seconds()
    log.info(f"✅ Backend SOPAL prêt en {elapsed:.1f}s — http://localhost:8000")


# ════════════════════════════════════════════════════════════
#  5. MODÈLES PYDANTIC
# ════════════════════════════════════════════════════════════

class ChatRequest(BaseModel):
    message: str
    defaut_context: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []
    latency_ms: float = 0
    model: str = OLLAMA_MODEL
    cache_hit: bool = False


# ════════════════════════════════════════════════════════════
#  6. ENDPOINTS
# ════════════════════════════════════════════════════════════

# ─── Health ─────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    ollama_ok = False
    model_ok  = False
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        ollama_ok = r.ok
        models = [m["name"] for m in r.json().get("models", [])]
        model_ok = any(OLLAMA_MODEL.split(":")[0] in m for m in models)
    except:
        pass

    return {
        "status": "OK" if (vectorstore and ollama_ok) else "DEGRADED",
        "vectorstore": vectorstore is not None,
        "vectors_indexed": vectorstore.index.ntotal if vectorstore else 0,
        "ollama_running": ollama_ok,
        "model": OLLAMA_MODEL,
        "model_available": model_ok,
        "cache_size": len(response_cache),
        "timestamp": datetime.now().isoformat()
    }


# ─── Chat classique (sans streaming) ────────────────────────
@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Endpoint RAG sans streaming — garde pour compatibilité."""
    import time
    start_time = time.time()

    if not vectorstore:
        raise HTTPException(status_code=503, detail="Vectorstore non prêt")

    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message vide")

    log.info(f"❓ '{message[:60]}' | Défaut: '{req.defaut_context}'")

    context, source_names = get_rag_context(message, req.defaut_context)
    prompt = build_prompt(context, req.defaut_context, message)

    # Vérifier cache
    cache_key = _hash_prompt(prompt)
    if cache_key in response_cache:
        log.info(f"💾 Cache hit")
        return ChatResponse(
            response=response_cache[cache_key],
            sources=source_names,
            latency_ms=0,
            cache_hit=True
        )

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": LLM_TEMPERATURE,
                    "top_p": 0.9,
                    "num_predict": LLM_MAX_TOKENS,
                    "repeat_penalty": 1.1,
                    "stop": ["Question:", "Défaut:"],
                    "num_thread": 8,
                }
            },
            timeout=LLM_TIMEOUT
        )
        response.raise_for_status()
        text = response.json().get("response", "").strip()

        # Cacher la réponse
        response_cache[cache_key] = text
        if len(response_cache) > CACHE_SIZE:
            response_cache.pop(next(iter(response_cache)))

        elapsed_ms = (time.time() - start_time) * 1000
        log.info(f"✅ Réponse ({len(text)} chars) en {elapsed_ms:.0f}ms")

        return ChatResponse(
            response=text,
            sources=source_names,
            latency_ms=elapsed_ms,
            model=OLLAMA_MODEL
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Ollama non disponible. Lancez: ollama serve")
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Timeout Ollama. Essayez /api/chat/stream")
    except Exception as e:
        log.error(f"❌ Erreur Ollama: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─── ✅ NOUVEAU : Chat avec STREAMING (Server-Sent Events) ───
@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    """
    ✅ CORRECTION PRINCIPALE
    Endpoint streaming SSE — résout le timeout 30s du frontend.
    Les tokens arrivent au fur et à mesure → l'utilisateur voit
    la réponse s'écrire en temps réel sans attendre la fin.
    """
    if not vectorstore:
        raise HTTPException(status_code=503, detail="Vectorstore non prêt")

    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message vide")

    log.info(f"🌊 STREAM ❓ '{message[:60]}' | Défaut: '{req.defaut_context}'")

    context, source_names = get_rag_context(message, req.defaut_context)
    prompt = build_prompt(context, req.defaut_context, message)

    # Vérifier cache — si réponse en cache, streamer quand même token par token
    cache_key = _hash_prompt(prompt)
    if cache_key in response_cache:
        log.info(f"💾 Cache hit — streaming simulé")
        cached = response_cache[cache_key]

        def stream_cached():
            # Simuler un streaming depuis le cache
            words = cached.split(" ")
            for i, word in enumerate(words):
                token = word + (" " if i < len(words) - 1 else "")
                yield f"data: {json.dumps({'token': token, 'sources': source_names})}\n\n"
            yield f"data: [DONE]\n\n"

        return StreamingResponse(stream_cached(), media_type="text/event-stream")

    def generate():
        """
        Générateur SSE — envoie chaque token Ollama au frontend.
        Format: "data: {json}\n\n"  (standard Server-Sent Events)
        """
        full_response = ""
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": True,          # ← STREAMING ACTIVÉ dans Ollama
                    "options": {
                        "temperature": LLM_TEMPERATURE,
                        "top_p": 0.9,
                        "num_predict": LLM_MAX_TOKENS,
                        "repeat_penalty": 1.1,
                        "stop": ["Question:", "Défaut:"],
                        "num_thread": 8,
                    }
                },
                stream=True,                 # ← requests lit ligne par ligne
                timeout=LLM_TIMEOUT
            )

            # Envoyer d'abord les sources
            yield f"data: {json.dumps({'sources': source_names})}\n\n"

            # Lire chaque token Ollama et le transmettre
            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    chunk = json.loads(line)
                    token = chunk.get("response", "")
                    if token:
                        full_response += token
                        yield f"data: {json.dumps({'token': token})}\n\n"
                    if chunk.get("done"):
                        break
                except json.JSONDecodeError:
                    continue

            # Cacher la réponse complète
            if full_response:
                response_cache[cache_key] = full_response
                if len(response_cache) > CACHE_SIZE:
                    response_cache.pop(next(iter(response_cache)))

            log.info(f"✅ Stream terminé ({len(full_response)} chars)")
            yield f"data: [DONE]\n\n"

        except requests.exceptions.ConnectionError:
            yield f"data: {json.dumps({'error': 'Ollama non disponible. Lancez: ollama serve'})}\n\n"
        except requests.exceptions.Timeout:
            yield f"data: {json.dumps({'error': 'Timeout Ollama — modèle trop lent'})}\n\n"
            if full_response:
                yield f"data: [DONE]\n\n"
        except Exception as e:
            log.error(f"❌ Erreur stream: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # Important pour nginx
        }
    )


# ─── Défauts ────────────────────────────────────────────────
@app.get("/api/defauts")
async def list_defauts():
    docs = load_knowledge_base(KB_PATH)
    seen = {}
    for doc in docs:
        if (name := doc.metadata.get("defaut_name")) and name not in seen:
            seen[name] = doc.metadata.get("defaut_id")
    defauts = [{"id": v, "name": k} for k, v in seen.items()]
    return {"defauts": sorted(defauts, key=lambda x: x["id"]), "total": len(defauts)}


# ─── Stats ──────────────────────────────────────────────────
@app.get("/api/stats")
async def stats():
    return {
        "timestamp": datetime.now().isoformat(),
        "vectorstore_vectors": vectorstore.index.ntotal if vectorstore else 0,
        "response_cache_size": len(response_cache),
        "max_cache_size": CACHE_SIZE,
        "config": {
            "model": OLLAMA_MODEL,
            "rag_top_k": RAG_TOP_K,
            "temperature": LLM_TEMPERATURE,
            "max_tokens": LLM_MAX_TOKENS,
            "timeout_sec": LLM_TIMEOUT,
            "streaming": True,
        }
    }


# ════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    log.info("🚀 Lancement FastAPI v3.0 avec streaming...")
    uvicorn.run(
        "backend_sopal:app",
        host="0.0.0.0",

        port=8000,
        reload=False,
        log_level="info",
        workers=1   # ← 1 worker avec streaming (pas multi-process)
    )
