<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <div class="space-y-8">

      <!-- FORMULAIRE -->
      <ComponentCard title="Contrôle Qualité">

        <form @submit.prevent="handleSubmit" class="space-y-6 max-w-2xl">

          <!-- CONTROLEUR -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Contrôleur</label>
            <select v-model="form.utilisateurId" class="w-full px-4 py-2 border rounded-lg">
              <option disabled value="">-- choisir --</option>
              <option v-for="u in utilisateurs" :key="u.id" :value="u.id">
                {{ u.nom }}
              </option>
            </select>
          </div>

          <!-- MACHINE -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Machine</label>
            <select v-model="form.codeMachine" class="w-full px-4 py-2 border rounded-lg">
              <option disabled value="">-- choisir --</option>
              <option v-for="m in machines" :key="m.codeMachine" :value="m.codeMachine">
                {{ m.nom }}
              </option>
            </select>
          </div>

          <!-- PRODUIT -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Produit</label>
            <select v-model="form.codeArticle" @change="onProduitChange"
                    class="w-full px-4 py-2 border rounded-lg">
              <option disabled value="">-- choisir --</option>
              <option v-for="p in produits" :key="p.codeArticle" :value="p.codeArticle">
                {{ p.nomProduit }}
              </option>
            </select>
          </div>

          <!-- AUTO INFOS -->
          <div class="grid grid-cols-2 gap-4">
            <input disabled v-model="designation" class="border p-2 rounded" placeholder="Désignation"/>
            <input disabled v-model="cadence" class="border p-2 rounded" placeholder="Cadence"/>
            <input disabled v-model="taille" class="border p-2 rounded" placeholder="Échantillons"/>
          </div>

          <!-- TEST 1 -->
          <div>
            <label class="font-semibold">Test 1</label>

            <input type="number"
                   v-model="test1.nbDefauts"
                   @input="handleDefaut(1)"
                   class="w-full border p-2 rounded mt-2"
                   placeholder="Nombre défauts"/>

            <div v-if="test1.showDefaut" class="mt-2 space-y-2">

              <select v-model="test1.selectedDefaut"
                      class="w-full border p-2 rounded">
                <option disabled value="">-- défaut --</option>
                <option v-for="d in defauts" :key="d.id" :value="d.nomDefaut">
                  {{ d.nomDefaut }}
                </option>
              </select>

              <!-- Nouveau défaut -->
              <input v-if="test1.selectedDefaut === ''"
                     v-model="test1.newDefaut"
                     placeholder="Nouveau défaut"
                     class="w-full border p-2 rounded"/>

              <input v-if="test1.selectedDefaut === ''"
                     v-model="test1.solution"
                     placeholder="Solution"
                     class="w-full border p-2 rounded"/>
            </div>
          </div>

          <!-- TEST 2 -->
          <div>
            <label class="font-semibold">Test 2</label>

            <input type="number"
                   v-model="test2.nbDefauts"
                   @input="handleDefaut(2)"
                   class="w-full border p-2 rounded mt-2"
                   placeholder="Nombre défauts"/>

            <div v-if="test2.showDefaut" class="mt-2 space-y-2">

              <select v-model="test2.selectedDefaut"
                      class="w-full border p-2 rounded">
                <option disabled value="">-- défaut --</option>
                <option v-for="d in defauts" :key="d.id" :value="d.nomDefaut">
                  {{ d.nomDefaut }}
                </option>
              </select>

              <input v-if="test2.selectedDefaut === ''"
                     v-model="test2.newDefaut"
                     placeholder="Nouveau défaut"
                     class="w-full border p-2 rounded"/>

              <input v-if="test2.selectedDefaut === ''"
                     v-model="test2.solution"
                     placeholder="Solution"
                     class="w-full border p-2 rounded"/>
            </div>
          </div>

          <!-- MESSAGE -->
          <div v-if="message"
               class="p-3 rounded text-white"
               :class="isError ? 'bg-red-500' : 'bg-green-500'">
            {{ message }}
          </div>

          <!-- BOUTON -->
          <button type="submit"
                  class="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700">
            Valider contrôle
          </button>

        </form>
      </ComponentCard>

    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'

const currentPageTitle = ref("Résultat de contrôle")

const produits = ref([])
const machines = ref([])
const utilisateurs = ref([])
const defauts = ref([])

const designation = ref("")
const cadence = ref(0)
const taille = ref(0)

const message = ref("")
const isError = ref(false)

const form = ref({
  codeMachine: "",
  codeArticle: "",
  utilisateurId: ""
})

const test1 = ref({
  nbDefauts: 0,
  showDefaut: false,
  selectedDefaut: "",
  newDefaut: "",
  solution: ""
})

const test2 = ref({
  nbDefauts: 0,
  showDefaut: false,
  selectedDefaut: "",
  newDefaut: "",
  solution: ""
})

const api = axios.create({
  baseURL: "/api"
})

/* RESET */
const resetForm = () => {
  form.value = { codeMachine: "", codeArticle: "", utilisateurId: "" }

  designation.value = ""
  cadence.value = 0
  taille.value = 0

  test1.value = { nbDefauts: 0, showDefaut: false, selectedDefaut: "", newDefaut: "", solution: "" }
  test2.value = { nbDefauts: 0, showDefaut: false, selectedDefaut: "", newDefaut: "", solution: "" }
}

/* PRODUIT */
const onProduitChange = () => {
  const p = produits.value.find(x => x.codeArticle === form.value.codeArticle)

  if (p) {
    designation.value = p.designation
    cadence.value = p.tailleEchantillonnage
    taille.value = cadence.value < 75 ? 3 : 5
    defauts.value = p.typeDefauts || []
  }
}

/* DEFAUT */
const handleDefaut = (t) => {
  if (t === 1)
    test1.value.showDefaut = test1.value.nbDefauts > 0
  else
    test2.value.showDefaut = test2.value.nbDefauts > 0
}

/* SUBMIT */
const handleSubmit = async () => {

  message.value = ""
  isError.value = false

  if (!form.value.codeMachine || !form.value.codeArticle || !form.value.utilisateurId) {
    isError.value = true
    message.value = "⚠️ Remplir tous les champs"
    return
  }

  const data = {
    codeMachine: form.value.codeMachine,
    codeArticle: form.value.codeArticle,
    utilisateurId: form.value.utilisateurId,

    nbDefautsTest1: test1.value.nbDefauts || 0,
    nbDefautsTest2: test2.value.nbDefauts || 0,

    defaut1: test1.value.selectedDefaut || test1.value.newDefaut || "",
    defaut2: test2.value.selectedDefaut || test2.value.newDefaut || "",

    solution1: test1.value.solution || "",
    solution2: test2.value.solution || ""
  }

  try {
    const res = await api.post("/ResultatControle", data)

    if (res.data.statutLot === "Conforme") {
      message.value = "✅ Lot Conforme"
    } else {
      isError.value = true
      message.value = "❌ Lot Non Conforme (Maintenance)"
    }

    resetForm()

  } catch (err) {
    console.error(err)
    isError.value = true
    message.value = "❌ Erreur API"
  }
}

/* LOAD */
onMounted(async () => {
  try {
    produits.value = (await api.get("/Produit")).data
    machines.value = (await api.get("/Machine")).data
    utilisateurs.value = (await api.get("/Utilisateur")).data
  } catch (err) {
    console.error(err)
  }
})
</script>
