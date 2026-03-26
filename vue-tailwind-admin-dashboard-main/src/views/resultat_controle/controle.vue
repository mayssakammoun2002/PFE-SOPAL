<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div class="space-y-8">
      <ComponentCard title="Contrôle Qualité">
        <form @submit.prevent="handleSubmit" class="space-y-6 max-w-2xl">

          <!-- CONTRÔLEUR -->
          <div>
            <label class="block text-sm font-medium mb-1">Contrôleur</label>
            <select v-model="form.utilisateurId" class="w-full border p-2 rounded">
              <option disabled value="">-- choisir --</option>
              <option v-for="u in utilisateurs" :key="u.id" :value="u.id">
                {{ u.nom }}
              </option>
            </select>
          </div>

          <!-- MACHINE -->
          <div>
            <label class="block text-sm font-medium mb-1">Machine</label>
            <select v-model="form.codeMachine" class="w-full border p-2 rounded">
              <option disabled value="">-- choisir --</option>
              <option v-for="m in machines" :key="m.codeMachine" :value="m.codeMachine">
                {{ m.nomMachine }}
              </option>
            </select>
          </div>

          <!-- PRODUIT -->
          <div>
            <label class="block text-sm font-medium mb-1">Produit</label>
            <select v-model="form.codeArticle" @change="onProduitChange" class="w-full border p-2 rounded">
              <option disabled value="">-- choisir --</option>
              <option v-for="p in produits" :key="p.codeArticle" :value="p.codeArticle">
                {{ p.nomProduit || p.designation || p.codeArticle }}
              </option>
            </select>
          </div>

          <!-- INFOS PRODUIT -->
          <div class="grid grid-cols-2 gap-2">
            <input
              disabled
              v-model="designation"
              class="border p-2 rounded"
              placeholder="Désignation"
            />
            <input
              disabled
              v-model="cadence"
              class="border p-2 rounded"
              placeholder="Cadence"
            />
            <input
              disabled
              :value="tailleEchantillons"
              class="border p-2 rounded col-span-2"
              placeholder="Nombre d'échantillons"
            />
          </div>

          <!-- TESTS -->
          <div v-for="(test, index) in tests" :key="index" class="border p-4 rounded">
            <label class="font-semibold block mb-2">Test {{ index + 1 }}</label>
            <input
              type="number"
              v-model.number="test.nbDefauts"
              @input="handleDefaut(index)"
              class="w-full border p-2 rounded"
              placeholder="Nombre de défauts"
              min="0"
            />

            <div v-if="test.showDefaut" class="mt-3 space-y-2">
              <select v-model="test.selectedDefaut" class="w-full border p-2 rounded">
                <option disabled value="">-- choisir un défaut --</option>
                <option v-for="d in defautsParProduit" :key="d.id" :value="d.nomDefaut">
                  {{ d.nomDefaut }}
                </option>
              </select>
              <input
                v-if="!test.selectedDefaut"
                v-model="test.newDefaut"
                class="w-full border p-2 rounded"
                placeholder="Nouveau défaut"
              />
            </div>
          </div>

          <!-- MESSAGES -->
          <div v-if="errorMsg" class="p-3 bg-red-100 text-red-700 rounded">
            {{ errorMsg }}
          </div>
          <div v-if="message" class="p-3 bg-green-100 text-green-700 rounded">
            {{ message }}
          </div>

          <!-- BOUTON -->
          <button
            type="submit"
            :disabled="loading"
            class="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-6 py-3 rounded font-medium w-full"
          >
            {{ loading ? "Enregistrement en cours..." : "Valider le contrôle" }}
          </button>
        </form>
      </ComponentCard>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "axios"
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'

// ==================== STATE ====================
const currentPageTitle = ref("Résultat de contrôle")
const loading = ref(false)
const message = ref("")
const errorMsg = ref("")

const utilisateurs = ref([
  { id: 1, nom: "Alice" },
  { id: 2, nom: "Bob" },
  { id: 3, nom: "Charlie" }
])

const produits = ref([])
const machines = ref([])
const defauts = ref([])

const designation = ref("")
const cadence = ref(0)
const tailleEchantillons = ref(0)     // ← Correction ici (était "taille")

const form = ref({
  codeMachine: "",
  codeArticle: "",
  utilisateurId: ""
})

const tests = ref([
  { nbDefauts: 0, showDefaut: false, selectedDefaut: "", newDefaut: "" },
  { nbDefauts: 0, showDefaut: false, selectedDefaut: "", newDefaut: "" }
])

const api = axios.create({ baseURL: "/api" })

// ==================== COMPUTED ====================
const defautsParProduit = computed(() => {
  if (!form.value.codeArticle) return []
  return defauts.value.filter(d => d.codeArticle === form.value.codeArticle)
})

// ==================== METHODS ====================
const onProduitChange = () => {
  const p = produits.value.find(x => x.codeArticle === form.value.codeArticle)
  if (p) {
    designation.value = p.designation || p.nomProduit || ""
    cadence.value = p.cadence || p.tailleEchantillonnage || 0
    tailleEchantillons.value = cadence.value < 75 ? 3 : 5
  } else {
    designation.value = ""
    cadence.value = 0
    tailleEchantillons.value = 0
  }
}

const handleDefaut = (index) => {
  tests.value[index].showDefaut = tests.value[index].nbDefauts > 0
}

const handleSubmit = async () => {
  // Validation frontend
  if (!form.value.codeMachine || !form.value.codeArticle || !form.value.utilisateurId) {
    errorMsg.value = "Veuillez sélectionner le Contrôleur, la Machine et le Produit"
    return
  }

  loading.value = true
  message.value = ""
  errorMsg.value = ""

  try {
    const payload = {
      CodeMachine: form.value.codeMachine,
      CodeArticle: form.value.codeArticle,
      UtilisateurId: Number(form.value.utilisateurId),
      NbDefautsTest1: Number(tests.value[0].nbDefauts || 0),
      NbDefautsTest2: Number(tests.value[1].nbDefauts || 0),
      Defaut1: tests.value[0].selectedDefaut || tests.value[0].newDefaut || "",
      Defaut2: tests.value[1].selectedDefaut || tests.value[1].newDefaut || ""
    }

    const res = await api.post("/ResultatControle", payload)

    const statut = res.data.statutLot || res.data.StatutLot || "Non Conforme"

    message.value = statut === "Conforme"
      ? "✅ Lot déclaré Conforme"
      : "❌ Lot déclaré Non Conforme"

    // Reset du formulaire
    resetForm()

  } catch (err) {
    console.error("Erreur Axios:", err)
    errorMsg.value = err.response?.data?.message ||
      err.response?.data?.details ||
      "Erreur lors de l'enregistrement. Vérifiez les données."
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  form.value = { codeMachine: "", codeArticle: "", utilisateurId: "" }
  designation.value = ""
  cadence.value = 0
  tailleEchantillons.value = 0

  tests.value.forEach(t => {
    t.nbDefauts = 0
    t.showDefaut = false
    t.selectedDefaut = ""
    t.newDefaut = ""
  })
}

// ==================== LOAD DATA ====================
const loadProduits = async () => {
  try { produits.value = (await api.get("/Produit")).data }
  catch (e) { console.error(e) }
}

const loadMachines = async () => {
  try { machines.value = (await api.get("/Machine")).data }
  catch (e) { console.error(e) }
}

const loadDefauts = async () => {
  try { defauts.value = (await api.get("/TypeDefaut")).data }
  catch (e) { console.error(e) }
}

onMounted(async () => {
  await Promise.all([loadProduits(), loadMachines(), loadDefauts()])
})
</script>
