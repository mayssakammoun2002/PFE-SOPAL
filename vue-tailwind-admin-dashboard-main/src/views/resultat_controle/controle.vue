<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <div class="space-y-8">

      <!-- Formulaire Principal -->
      <ComponentCard :title="editingId ? 'Modifier le Contrôle' : 'Nouveau Contrôle Qualité'">
        <form @submit.prevent="handleSubmit" class="space-y-6 max-w-4xl">

          <!-- Informations Générales -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium mb-1">Contrôleur <span class="text-red-500">*</span></label>
              <select v-model="form.utilisateurId" class="w-full border p-3 rounded-lg" required>
                <option disabled value="">-- Choisir un contrôleur --</option>
                <option v-for="u in utilisateurs" :key="u.id" :value="u.id">
                  {{ u.firstName }} {{ u.lastName }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium mb-1">Machine <span class="text-red-500">*</span></label>
              <select v-model="form.codeMachine" class="w-full border p-3 rounded-lg" required>
                <option disabled value="">-- Choisir une machine --</option>
                <option v-for="m in machines" :key="m.codeMachine" :value="m.codeMachine">
                  {{ m.nomMachine }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium mb-1">Num OF <span class="text-red-500">*</span></label>
              <input v-model="form.numOF" class="w-full border p-3 rounded-lg" placeholder="Ex: OF-20260331-045" required />
            </div>

            <div>
              <label class="block text-sm font-medium mb-1">Code Article <span class="text-red-500">*</span></label>
              <input
                v-model="form.codeArticle"
                class="w-full border p-3 rounded-lg uppercase tracking-widest"
                placeholder="ABC123"
                @change="onCodeArticleChange"
                required
              />
            </div>

            <div class="lg:col-span-2">
              <label class="block text-sm font-medium mb-1">Quantité Produite <span class="text-red-500">*</span></label>
              <input type="number" v-model.number="form.quantite" class="w-full border p-3 rounded-lg" min="1" required />
            </div>

            <div class="lg:col-span-2">
              <label class="block text-sm font-medium mb-1">Cadence (pièces/heure) <span class="text-red-500">*</span></label>
              <input
                type="number"
                v-model.number="form.cadence"
                @change="calculerEchantillons"
                class="w-full border p-3 rounded-lg"
                min="1"
                required
              />
            </div>
          </div>

          <!-- Infos Produit -->
          <div v-if="form.codeArticle" class="grid grid-cols-3 gap-4 bg-gray-50 p-5 rounded-xl">
            <div>
              <label class="text-xs text-gray-500">Désignation</label>
              <input
                v-model="designation"
                :disabled="!isProduitInconnu"
                class="w-full border p-2 rounded-lg bg-white"
                :class="{ 'bg-amber-50 border-amber-300': isProduitInconnu }"
                placeholder="Saisir la désignation manuellement..."
              />
            </div>
            <div>
              <label class="text-xs text-gray-500">Cadence (base)</label>
              <input disabled v-model="cadenceBase" class="w-full border p-2 rounded-lg bg-white" />
            </div>
            <div>
              <label class="text-xs text-gray-500">Échantillons</label>
              <input disabled :value="tailleEchantillons" class="w-full border p-2 rounded-lg font-semibold text-green-700 bg-white" />
            </div>

            <div v-if="isProduitInconnu" class="col-span-3 p-4 bg-amber-50 border border-amber-200 rounded-xl text-amber-700 text-sm">
              ⚠️ Le produit <span class="font-mono font-semibold">{{ form.codeArticle.toUpperCase() }}</span> n'existe pas dans la base.<br>
              <strong>Vous pouvez saisir la désignation manuellement.</strong>
            </div>
          </div>

          <!-- TESTS ÉCHANTILLONS -->
          <div v-if="!editingId && form.codeArticle && form.quantite && form.cadence"
               class="border-2 border-dashed border-green-300 p-6 rounded-2xl bg-white">

            <div class="flex justify-between items-center mb-6">
              <h3 class="font-semibold text-2xl">Test {{ currentStep }} / 2</h3>
              <span class="px-5 py-2 bg-green-100 text-green-700 rounded-full font-medium">
                {{ tailleEchantillons }} échantillons
              </span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              <div v-for="(ech, index) in echantillons" :key="index" class="border rounded-2xl p-5 bg-gray-50 hover:bg-white transition">
                <p class="text-center font-medium mb-4">Échantillon {{ index + 1 }}</p>
                <div class="flex justify-center gap-4 mb-4">
                  <button type="button" @click="ech.valeur = 0"
                          :class="ech.valeur === 0 ? 'bg-green-600 text-white ring-2 ring-green-400' : 'bg-gray-200 hover:bg-gray-300'"
                          class="w-16 h-16 rounded-2xl text-3xl font-bold transition">0</button>
                  <button type="button" @click="ech.valeur = 1"
                          :class="ech.valeur === 1 ? 'bg-red-600 text-white ring-2 ring-red-400' : 'bg-gray-200 hover:bg-gray-300'"
                          class="w-16 h-16 rounded-2xl text-3xl font-bold transition">1</button>
                </div>

                <div v-if="ech.valeur === 1" class="space-y-3">
                  <select v-model="ech.defaut" class="w-full border p-3 rounded-lg">
                    <option value="">-- Choisir un défaut --</option>
                    <option v-if="defautsParProduit.length === 0" disabled class="text-amber-600 font-medium">
                      ⚠️ Tous les défauts sont affichés (produit inconnu)
                    </option>
                    <option v-for="d in defautsParProduit" :key="d.id" :value="d.nomDefaut">
                      {{ d.nomDefaut }}
                    </option>
                    <option value="Nouveau Défaut">➕ Nouveau Défaut</option>
                  </select>

                  <input v-if="ech.defaut === 'Nouveau Défaut'" v-model="ech.nouveauDefaut" placeholder="Nom du nouveau défaut" class="w-full border p-3 rounded-lg" />
                  <input v-model="ech.solution" placeholder="Solution corrective" class="w-full border p-3 rounded-lg" />
                </div>
              </div>
            </div>

            <button @click.prevent="validerTestEnCours" class="mt-8 w-full bg-green-600 hover:bg-green-700 text-white py-4 rounded-2xl font-semibold text-lg transition">
              Valider Test {{ currentStep }}
            </button>
          </div>

          <!-- Résultat Final -->
          <div v-if="isFinished" class="p-8 rounded-3xl text-center border-4"
               :class="finalStatut === 'Conforme' ? 'bg-green-100 border-green-400' : 'bg-red-100 border-red-400'">
            <div class="text-6xl mb-4">{{ finalStatut === 'Conforme' ? '✅' : '❌' }}</div>
            <h3 class="text-3xl font-bold">
              {{ finalStatut === 'Conforme' ? 'Lot Validé ✅' : 'Lot Non Validé - À Éliminer ❌' }}
            </h3>
            <div v-if="finalStatut === 'Non Conforme'" class="mt-6">
              <label class="block text-sm font-medium mb-2 text-red-700">Solution Globale Corrective *</label>
              <textarea v-model="solutionGlobale" rows="3" class="w-full border p-4 rounded-2xl"></textarea>
            </div>
          </div>

          <button v-if="isFinished || editingId" type="submit" :disabled="loading"
                  class="mt-6 w-full py-5 rounded-2xl font-semibold text-xl transition"
                  :class="editingId ? 'bg-orange-600 hover:bg-orange-700' : 'bg-green-600 hover:bg-green-700'">
            {{ loading ? "Enregistrement en cours..." : editingId ? "Modifier le Contrôle" : "Enregistrer le Contrôle" }}
          </button>

          <div v-if="errorMsg" class="p-4 bg-red-100 text-red-700 rounded-xl">{{ errorMsg }}</div>
          <div v-if="message" class="p-4 bg-green-100 text-green-700 rounded-xl">{{ message }}</div>
        </form>
      </ComponentCard>

      <!-- Historique -->
      <ComponentCard title="Historique des Résultats de Contrôle">
        <div class="overflow-x-auto">
          <table class="w-full text-sm border-collapse">
            <thead class="bg-gray-100">
            <tr>
              <th class="border p-3 text-left">Date</th>
              <th class="border p-3 text-left">Code Article</th>
              <th class="border p-3 text-left">Num OF</th>
              <th class="border p-3 text-left">Machine</th>
              <th class="border p-3 text-center">Quantité</th>
              <th class="border p-3 text-center">Cadence</th>
              <th class="border p-3 text-center">Éch.</th>
              <th class="border p-3 text-center">Défauts T1</th>
              <th class="border p-3 text-center">Défauts T2</th>
              <th class="border p-3 text-center">Statut</th>
              <th class="border p-3 text-center">Actions</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="res in resultats" :key="res.id" class="hover:bg-gray-50">
              <td class="border p-3">{{ new Date(res.dateControle || res.createdAt).toLocaleDateString('fr-FR') }}</td>
              <td class="border p-3 font-medium">{{ res.codeArticle }}</td>
              <td class="border p-3">{{ res.numOF }}</td>
              <td class="border p-3">{{ res.codeMachine }}</td>
              <td class="border p-3 text-center">{{ res.quantite }}</td>
              <td class="border p-3 text-center">{{ res.cadence }}</td>
              <td class="border p-3 text-center">{{ res.nbEchantillons }}</td>
              <td class="border p-3 text-center">{{ res.nbDefautsTest1 }}</td>
              <td class="border p-3 text-center">{{ res.nbDefautsTest2 }}</td>
              <td class="border p-3 text-center">
                  <span :class="res.statutLot === 'Conforme' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" class="px-4 py-1 rounded-full text-xs font-semibold">
                    {{ res.statutLot }}
                  </span>
              </td><td class="border p-3 text-center">
              <div class="flex gap-4 justify-center">

                <!-- ✏️ Modifier -->
                <button
                  @click="editControle(res)"
                  title="Modifier"
                  class="text-indigo-600 hover:text-indigo-900 transition duration-150 hover:scale-110"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                    />
                  </svg>
                </button>

                <!-- 🗑 Supprimer -->
                <button
                  @click="confirmDelete(res.id)"
                  title="Supprimer"
                  class="text-red-600 hover:text-red-800 transition duration-150 hover:scale-110"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>

              </div>
            </td>
            </tr>
            <tr v-if="resultats.length === 0">
              <td colspan="11" class="text-center p-8 text-gray-500">Aucun contrôle enregistré</td>
            </tr>
            </tbody>
          </table>
        </div>
      </ComponentCard>
    </div>
  </AdminLayout>
</template>
<script setup>
import { ref, onMounted, computed } from "vue"
import api from '@/services/api'  // ✅ SEULEMENT ÇA, plus d'axios direct

import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'

// ====================== STATE ======================
const currentPageTitle = ref("Résultat de Contrôle")
const loading = ref(false)
const message = ref("")
const errorMsg = ref("")
const editingId = ref(null)

const utilisateurs = ref([])
const machines = ref([])
const defauts = ref([])
const resultats = ref([])

const designation = ref("")
const cadenceBase = ref(0)
const tailleEchantillons = ref(3)
const isProduitInconnu = ref(false)

const form = ref({
  utilisateurId: null,
  codeMachine: "",
  codeArticle: "",
  numOF: "",
  quantite: null,
  cadence: null
})

const currentStep = ref(1)
const testResults = ref([])
const echantillons = ref([])
const isFinished = ref(false)
const finalStatut = ref("")
const solutionGlobale = ref("")

// ====================== COMPUTED ======================
const defautsParProduit = computed(() => {
  const code = form.value.codeArticle?.trim().toUpperCase()
  if (code && isProduitInconnu.value) return defauts.value
  return defauts.value.filter(d => d.codeArticle === code)
})

// ====================== PRODUIT ======================
const onCodeArticleChange = async () => {
  const code = (form.value.codeArticle || "").trim().toUpperCase()
  form.value.codeArticle = code
  if (!code) return resetProduitInfo()

  try {
    const response = await api.get(`/Produit/${code}`, {
      validateStatus: (status) => status === 200 || status === 404
    })

    if (response.status === 200) {
      designation.value = response.data?.designation || ""
      cadenceBase.value = response.data?.cadence || 0
      isProduitInconnu.value = false
      if (response.data?.cadence) form.value.cadence = response.data.cadence
    } else {
      designation.value = ""
      cadenceBase.value = 0
      isProduitInconnu.value = true
    }
  } catch (e) {
    console.warn("Erreur produit :", e)
    isProduitInconnu.value = true
  }
  calculerEchantillons()
}

const resetProduitInfo = () => {
  designation.value = ""
  cadenceBase.value = 0
  isProduitInconnu.value = false
  calculerEchantillons()
}

// ====================== CALCUL & TEST ======================
const calculerEchantillons = () => {
  const cad = Number(form.value.cadence) || 0
  tailleEchantillons.value = cad > 75 ? 5 : 3
  initEchantillons()
}

const initEchantillons = () => {
  echantillons.value = Array.from({ length: tailleEchantillons.value }, () => ({
    valeur: null,
    defaut: "",
    nouveauDefaut: "",
    solution: ""
  }))
}

const validerTestEnCours = () => {
  const nbDefauts = echantillons.value.filter(e => e.valeur === 1).length

  testResults.value.push({
    nbDefauts,
    echantillons: echantillons.value.map(e => ({ ...e }))
  })

  if (currentStep.value === 1) {
    if (nbDefauts === 0) {
      finalStatut.value = "Conforme"
      isFinished.value = true
    } else if (nbDefauts >= 2) {
      finalStatut.value = "Non Conforme"
      isFinished.value = true
    } else {
      currentStep.value = 2
      initEchantillons()
    }
  } else {
    finalStatut.value = nbDefauts === 0 ? "Conforme" : "Non Conforme"
    isFinished.value = true
  }
}

const extraireDefauts = () => {
  const echTest1 = testResults.value[0]?.echantillons || []
  const echTest2 = testResults.value[1]?.echantillons || []

  const defautsTest1 = echTest1.filter(e => e.valeur === 1)
  const defautsTest2 = echTest2.filter(e => e.valeur === 1)

  const resoudreDefaut = (ech) => {
    if (!ech) return null
    if (ech.defaut === 'Nouveau Défaut') return ech.nouveauDefaut?.trim() || null
    return ech.defaut?.trim() || null
  }

  return {
    defaut1: resoudreDefaut(defautsTest1[0]),
    defaut2: resoudreDefaut(defautsTest2[0])
  }
}

// ====================== SUBMIT ======================
const handleSubmit = async () => {
  errorMsg.value = ""
  message.value = ""

  if (!form.value.utilisateurId) return errorMsg.value = "❌ Sélectionnez un Contrôleur"
  if (!form.value.codeMachine) return errorMsg.value = "❌ Sélectionnez une Machine"
  if (!form.value.numOF?.trim()) return errorMsg.value = "❌ Num OF obligatoire"
  if (!form.value.codeArticle?.trim()) return errorMsg.value = "❌ Code Article obligatoire"
  if (!form.value.quantite || form.value.quantite < 1) return errorMsg.value = "❌ Quantité > 0"
  if (!form.value.cadence || form.value.cadence < 1) return errorMsg.value = "❌ Cadence > 0"

  loading.value = true

  const { defaut1, defaut2 } = extraireDefauts()

  const payload = {
    codeMachine: form.value.codeMachine.trim(),
    codeArticle: form.value.codeArticle.trim().toUpperCase(),
    numOF: form.value.numOF.trim(),
    utilisateurId: Number(form.value.utilisateurId),
    quantite: Number(form.value.quantite),
    cadence: Number(form.value.cadence),
    nbEchantillons: tailleEchantillons.value,
    nbDefautsTest1: testResults.value[0]?.nbDefauts ?? 0,
    nbDefautsTest2: testResults.value[1]?.nbDefauts ?? 0,
    solutionGlobale: solutionGlobale.value?.trim() || null,
    defaut1,
    defaut2
  }

  try {
    if (editingId.value) {
      const res = await api.put(`/ResultatControle/${editingId.value}`, payload)
      if (res.data?.success === false) {
        errorMsg.value = res.data?.message || "Erreur modification"
        return
      }
      message.value = "✅ Modifié avec succès"
    } else {
      const res = await api.post("/ResultatControle", payload)
      if (res.data?.success === false) {
        errorMsg.value = res.data?.message || "Erreur enregistrement"
        return
      }
      message.value = "✅ Contrôle enregistré avec succès"
    }

    await loadResultats()
    resetForm()
  } catch (err) {
    console.error("❌ ERREUR :", err.response?.data)
    errorMsg.value = err.response?.data?.message || "Erreur lors de l'enregistrement"
  } finally {
    loading.value = false
  }
}

// ====================== AUTRES ======================
const confirmDelete = (id) => {
  if (confirm("Supprimer ce contrôle ?")) {
    api.delete(`/ResultatControle/${id}`)
      .then(() => {
        message.value = "✅ Supprimé avec succès"
        loadResultats()
      })
      .catch(() => errorMsg.value = "Erreur suppression")
  }
}

const editControle = (res) => {
  editingId.value = res.id
  form.value = {
    utilisateurId: res.utilisateurId,
    codeMachine: res.codeMachine,
    codeArticle: res.codeArticle,
    numOF: res.numOF,
    quantite: res.quantite,
    cadence: res.cadence
  }
  finalStatut.value = res.statutLot || ""
  solutionGlobale.value = res.solutionGlobale || ""
  testResults.value = [
    { nbDefauts: res.nbDefautsTest1 || 0, echantillons: [] },
    { nbDefauts: res.nbDefautsTest2 || 0, echantillons: [] }
  ]
  isFinished.value = true
  onCodeArticleChange()
}

const resetForm = () => {
  editingId.value = null
  form.value = {
    utilisateurId: null,
    codeMachine: "",
    codeArticle: "",
    numOF: "",
    quantite: null,
    cadence: null
  }
  designation.value = ""
  cadenceBase.value = 0
  isProduitInconnu.value = false
  testResults.value = []
  isFinished.value = false
  finalStatut.value = ""
  solutionGlobale.value = ""
  currentStep.value = 1
  echantillons.value = []
}

// ====================== CHARGEMENT ======================
const loadUtilisateurs = async () => {
  utilisateurs.value = (await api.get("/Utilisateur")).data || []
}
const loadMachines = async () => {
  machines.value = (await api.get("/Machine")).data || []
}
const loadDefauts = async () => {
  defauts.value = (await api.get("/TypeDefaut")).data || []
}
const loadResultats = async () => {
  resultats.value = (await api.get("/ResultatControle")).data || []
}

onMounted(async () => {
  await Promise.all([loadUtilisateurs(), loadMachines(), loadDefauts(), loadResultats()])
})
</script>
