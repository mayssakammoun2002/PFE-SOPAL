<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <div class="space-y-8">
      <!-- Formulaire d'ajout -->
      <ComponentCard title="Ajouter un Produit">
        <form @submit.prevent="handleSubmit" class="space-y-6 max-w-2xl">
          <!-- Code Article -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Code Article <span class="text-red-500">*</span>
            </label>
            <input
              v-model.trim="form.codeArticle"
              type="text"
              maxlength="20"
              required
              placeholder="Ex: 03AT203-1"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
            />
          </div>

          <!-- Nom Produit -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Nom du Produit <span class="text-red-500">*</span>
            </label>
            <input
              v-model.trim="form.nomProduit"
              type="text"
              maxlength="50"
              required
              placeholder="Ex: Vis inox M8"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
            />
          </div>

          <!-- Désignation -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Désignation <span class="text-red-500">*</span>
            </label>
            <textarea
              v-model.trim="form.designation"
              rows="3"
              required
              minlength="3"
              maxlength="100"
              placeholder="Description détaillée du produit..."
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
            ></textarea>
          </div>

          <!-- Taille Échantillonnage -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              La cadence            </label>
            <input
              v-model.number="form.tailleEchantillonnage"
              type="number"
              min="1"
              max="100000000000000000"
              required
              placeholder="Ex: 74"

              class="w-full sm:w-48 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
            />
            <p class="mt-1 text-sm text-gray-500"> </p>
          </div>


<!--          &lt;!&ndash; Liste déroulante &ndash;&gt;-->
<!--          <div class="relative">-->
<!--            <label class="block text-sm font-medium text-gray-700 mb-1">-->
<!--              Types de défauts-->
<!--            </label>-->

<!--            &lt;!&ndash; Bouton &ndash;&gt;-->
<!--            <div-->
<!--              @click="showDropdown = !showDropdown"-->
<!--              class="border border-gray-300 rounded-lg p-2 cursor-pointer bg-white"-->
<!--            >-->
<!--              Sélectionner défauts-->
<!--            </div>-->

<!--            &lt;!&ndash; Dropdown &ndash;&gt;-->
<!--            <div-->
<!--              v-if="showDropdown"-->
<!--              class="absolute z-10 mt-2 w-full bg-white border border-gray-300 rounded-lg shadow max-h-60 overflow-y-auto"-->
<!--            >-->
<!--              <div-->
<!--                v-for="d in defauts"-->
<!--                :key="d.id"-->
<!--                class="flex flex-col gap-2 p-3 border-b hover:bg-gray-50"-->
<!--              >-->
<!--                &lt;!&ndash; Checkbox + nom &ndash;&gt;-->
<!--                <div class="flex items-center gap-2">-->
<!--                  <input-->
<!--                    type="checkbox"-->
<!--                    :value="d.id"-->
<!--                    v-model="form.typeDefautIds"-->
<!--                  />-->
<!--                  <span>{{ d.nomDefaut }}</span>-->
<!--                </div>-->

<!--                &lt;!&ndash; Image en dessous &ndash;&gt;-->
<!--                <img-->
<!--                  v-if="d.imagePath"-->
<!--                  :src="`http://localhost:5100/images/${d.imagePath}`"-->
<!--                  class="w-20 h-20 rounded object-cover ml-6"-->
<!--                />-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->

          <!-- Messages -->
          <div v-if="errorMessage" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
            {{ successMessage }}
          </div>
          <!-- Buttons -->
          <div class="flex justify-end gap-4 pt-4">
            <button
              type="button"
              @click="resetForm"
              class="px-5 py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
              :disabled="loading"
            >
              Annuler
            </button>

            <!-- Bouton AJOUTER -->
            <button
              v-if="!isEdit"
              type="submit"
              class="px-6 py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-green-400 disabled:cursor-not-allowed transition flex items-center gap-2"
              :disabled="loading"
            >
              <span v-if="loading">Enregistrement...</span>
              <span v-else>Ajouter le produit</span>
            </button>

            <!-- Bouton MODIFIER -->
            <button
              v-if="isEdit"
              type="submit"
              class="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed transition flex items-center gap-2"
              :disabled="loading"
            >
              <span v-if="loading">Enregistrement...</span>
              <span v-else>Modifier le produit</span>
            </button>
          </div>
        </form>
      </ComponentCard>

      <!-- Liste des produits -->
      <ComponentCard title="Produits existants">
        <div v-if="loading" class="text-center py-12 text-gray-500">
          Chargement...
        </div>
        <div v-else-if="produits.length === 0" class="text-center py-12 text-gray-500">
          Aucun produit pour le moment
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nom</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">La cadence</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="p in produits" :key="p.codeArticle" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ p.codeArticle }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ p.nomProduit }}
              </td>

              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ p.tailleEchantillonnage || '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex items-center gap-4">
                  <!-- Modifier -->
                  <button
                    @click="openEditModal(p)"
                    title="Modifier ce produit"
                    class="text-indigo-600 hover:text-indigo-900 transition-colors duration-150"
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

                  <!-- Supprimer -->
                  <button
                    @click="confirmDelete(p.codeArticle)"
                    title="Supprimer ce produit"
                    class="text-red-600 hover:text-red-800 transition-colors duration-150"
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
            </tbody>
          </table>
        </div>
      </ComponentCard>
    </div>
  </AdminLayout>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'

const currentPageTitle = ref('Ajouter un Produit')
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const showDropdown = ref(false)

const produits = ref([])
const defauts = ref([])

const isEdit = ref(false)

const form = ref({
  codeArticle: '',
  nomProduit: '',
  designation: '',
  tailleEchantillonnage: null,
  typeDefautIds: []
})

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// ======================
// FETCH DATA
// ======================

const fetchDefauts = async () => {
  try {
    const res = await api.get('/TypeDefaut')
    defauts.value = res.data
  } catch (err) {
    console.error(err)
  }
}

const fetchProduits = async () => {
  loading.value = true
  try {
    const res = await api.get('/Produit')
    produits.value = res.data
  } catch (err) {
    errorMessage.value = 'Erreur chargement produits'
  } finally {
    loading.value = false
  }
}

// ======================
// RESET FORM
// ======================

const resetForm = () => {
  form.value = {
    codeArticle: '',
    nomProduit: '',
    designation: '',
    tailleEchantillonnage: null,
    typeDefautIds: []
  }

  isEdit.value = false
  errorMessage.value = ''
  successMessage.value = ''
}

// ======================
// EDIT
// ======================

const openEditModal = (p) => {
  isEdit.value = true
  form.value.codeArticle = p.codeArticle
  form.value.nomProduit = p.nomProduit
  form.value.designation = p.designation
  form.value.tailleEchantillonnage = p.tailleEchantillonnage

  // ✅ convertir en number
  form.value.typeDefautIds = p.typeDefauts
    ? p.typeDefauts.map(d => Number(d.id))
    : []
}

// ======================
// SUBMIT (FIXED)
// ======================

const handleSubmit = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!form.value.codeArticle || !form.value.nomProduit) {
    errorMessage.value = "Code article et nom du produit sont obligatoires"
    return
  }

  loading.value = true

  try {
    const payload = {
      codeArticle: form.value.codeArticle.trim().toUpperCase(),
      nomProduit: form.value.nomProduit.trim(),
      designation: form.value.designation.trim(),
      tailleEchantillonnage: form.value.tailleEchantillonnage || 0,
      typeDefautIds: form.value.typeDefautIds.map(id => Number(id))
    }

    if (isEdit.value) {
      await api.put(`/Produit/${form.value.codeArticle}`, payload)
      successMessage.value = 'Produit modifié avec succès !'
    } else {
      await api.post('/Produit', payload)
      successMessage.value = 'Produit ajouté avec succès !'
    }

    resetForm()
    await fetchProduits()
  } catch (err) {
    console.error(err.response?.data)
    errorMessage.value = err.response?.data?.message ||
      err.response?.data?.detail ||
      "Erreur lors de l'enregistrement"
  } finally {
    loading.value = false
  }
}
// ======================
// DELETE
// ======================

const confirmDelete = async (codeArticle) => {
  if (!confirm(`Supprimer le produit ${codeArticle} ?`)) return

  loading.value = true
  try {
    await api.delete(`/Produit/${codeArticle}`)
    successMessage.value = 'Produit supprimé'
    await fetchProduits()
  } catch (err) {
    console.error("Erreur complète :", err.response?.data);

    errorMessage.value =
      err.response?.data?.detail ||
      err.response?.data?.message ||
      "Erreur serveur inconnue";
  }
}

// ======================

onMounted(() => {
  fetchProduits()
  fetchDefauts()
})
</script>
