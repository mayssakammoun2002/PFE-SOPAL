<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <div class="space-y-6">

      <!-- ================= FORMULAIRE ================= -->
      <ComponentCard :title="editingId ? 'Modifier Type de Défaut' : 'Ajouter Type de Défaut'">

        <div v-if="errorMsg" class="p-4 mb-4 bg-red-50 border border-red-200 text-red-700 rounded">
          {{ errorMsg }}
        </div>

        <form @submit.prevent="submitDefaut" class="space-y-4">

          <div>
            <label class="block mb-2 text-sm font-medium">Nom défaut      <span class="text-red-600">*</span></label>
            <input v-model="form.nomDefaut" type="text" class="w-full border p-2 rounded" required />
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Description     <span class="text-red-600">*</span> </label>

            <textarea v-model="form.description" class="w-full border p-2 rounded" required></textarea>
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Solution      <span class="text-red-600">*</span></label>
            <textarea v-model="form.solution" class="w-full border p-2 rounded" required></textarea>
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Fréquence</label>
            <input v-model="form.frequence" type="number" class="w-full border p-2 rounded" />
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Code Article      <span class="text-red-600">*</span></label>
            <input v-model="form.codeArticle" type="text" class="w-full border p-2 rounded" required />
          </div>

          <!-- IMAGE -->
          <div>
            <input type="file" ref="fileInput" class="hidden" @change="handleImage" />

            <button type="button" @click="openFile"
                    class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              📷 Ajouter photo
            </button>

            <div class="flex flex-col gap-3 mt-3">
              <img v-if="imagePreview"
                   :src="imagePreview"
                   class="w-24 h-24 object-cover rounded border" />
            </div>
          </div>

          <!-- BUTTONS -->
          <div class="flex gap-4">
            <button type="submit"
                    class="px-6 py-2 text-white rounded"
                    :class="editingId ? 'bg-orange-600' : 'bg-green-600'">
              {{ editingId ? 'Modifier défaut' : 'Ajouter défaut' }}
            </button>

            <button
              type="button"
              @click="resetForm"
              class="px-5 py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
              :disabled="loading"
            >
              Annuler
            </button>
          </div>

        </form>
      </ComponentCard>

      <!-- ================= TABLEAU STYLE PRODUIT ================= -->
      <ComponentCard title="Liste Types Défauts">

        <div v-if="defauts.length === 0" class="text-center py-6 text-gray-500">
          Aucun défaut
        </div>

        <table v-else class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nom</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Solution</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fréquence</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Photo</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
          </thead>

          <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="d in defauts" :key="d.id" class="hover:bg-gray-50">

            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ d.nomDefaut }}
            </td>

            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ truncate(d.description) }}
            </td>

            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ truncate(d.solution) }}
            </td>

            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ d.frequence || '-' }}
            </td>

            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ d.codeArticle }}
            </td>

            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <img
                v-if="d.imagePath"
                :src="`http://localhost:5100/images/${d.imagePath}`"
                class="w-30 h-30 rounded object-cover"
              />
              <span v-else>-</span>
            </td>

            <!-- ✅ FIXED ACTIONS (NO nested td) -->
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <div class="flex items-center gap-4">

                <!-- EDIT -->
                <button
                  @click="editDefaut(d)"
                  title="Modifier"
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

                <!-- DELETE -->
                <button
                  @click="deleteDefaut(d.id)"
                  title="Supprimer"
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

const API = '/api/TypeDefaut'

const currentPageTitle = ref("Gestion Types de Défauts")
const errorMsg = ref('')

const form = ref({
  nomDefaut: '',
  description: '',
  solution: '',
  frequence: 0,
  codeArticle: ''
})

const defauts = ref([])
const imageFile = ref(null)
const imagePreview = ref(null)
const fileInput = ref(null)
const editingId = ref(null)

/* LOAD */
const loadDefauts = async () => {
  try {
    const res = await axios.get(API)
    defauts.value = res.data
  } catch {
    errorMsg.value = "Impossible de charger les données"
  }
}

onMounted(loadDefauts)

/* IMAGE */
const openFile = () => fileInput.value.click()

const handleImage = (e) => {
  const file = e.target.files[0]
  if (!file) return
  imageFile.value = file
  imagePreview.value = URL.createObjectURL(file)
}

/* SUBMIT */
const submitDefaut = async () => {
  try {
    const fd = new FormData()

    fd.append('NomDefaut', form.value.nomDefaut)
    fd.append('Description', form.value.description)
    fd.append('Solution', form.value.solution)
    fd.append('Frequence', form.value.frequence)
    fd.append('CodeArticle', form.value.codeArticle)

    if (imageFile.value) {
      fd.append('ImageFile', imageFile.value)
    }

    if (editingId.value) {
      await axios.put(`${API}/${editingId.value}`, fd)
    } else {
      await axios.post(API, fd)
    }

    resetForm()
    loadDefauts()

  } catch {
    errorMsg.value = "Erreur API"
  }
}

/* EDIT */
const editDefaut = (d) => {
  form.value = { ...d }
  editingId.value = d.id
}

/* DELETE */
const deleteDefaut = async (id) => {
  try {
    await axios.delete(`${API}/${id}`)
    loadDefauts()
  } catch {
    errorMsg.value = "Erreur suppression"
  }
}

/* RESET */
const resetForm = () => {
  form.value = {
    nomDefaut: '',
    description: '',
    solution: '',
    frequence: 0,
    codeArticle: ''
  }
  editingId.value = null
  imageFile.value = null
  imagePreview.value = null
  fileInput.value.value = null
}

/* UTILS */
const truncate = (text, n = 40) =>
  text?.length > n ? text.slice(0, n) + '...' : text
</script>

<style scoped>
.space-y-6 {
  padding: 20px;
  background: #f8fafc;
}

table {
  border-radius: 12px;
  overflow: hidden;
}

thead {
  background: #f9fafb;
}

td {
  color: #475569;
}
</style>
