<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <div class="space-y-6">

      <!-- ================= FORMULAIRE ================= -->
      <ComponentCard :title="editingId ? 'Modifier Défaut' : 'Ajouter Défaut'">

        <div v-if="errorMsg" class="p-4 mb-4 bg-red-50 border border-red-200 text-red-700 rounded">
          {{ errorMsg }}
        </div>

        <form @submit.prevent="submitDefaut" class="space-y-4">

          <div>
            <label class="block mb-2 text-sm font-medium">Nom défaut <span class="text-red-600">*</span></label>
            <input v-model="form.nomDefaut" type="text" class="w-full border p-2 rounded" required />
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Description <span class="text-red-600">*</span></label>
            <textarea v-model="form.description" class="w-full border p-2 rounded h-24" required></textarea>
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Cause probable <span class="text-red-600">*</span></label>
            <textarea v-model="form.causeProbable" class="w-full border p-2 rounded h-24" required></textarea>
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Solution <span class="text-red-600">*</span></label>
            <textarea v-model="form.solution" class="w-full border p-2 rounded h-24" required></textarea>
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Fréquence</label>
            <input v-model="form.frequence" type="number" class="w-full border p-2 rounded" min="0" />
          </div>

          <!-- IMAGE -->
          <div>
            <input type="file" ref="fileInput" class="hidden" @change="handleImage" accept="image/*" />

            <button type="button" @click="openFile"
                    class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              📷 Ajouter photo
            </button>

            <div class="mt-3">
              <img v-if="imagePreview"
                   :src="imagePreview"
                   class="w-28 h-28 object-cover rounded border" />
            </div>
          </div>

          <div class="flex gap-4">
            <button type="submit"
                    class="px-6 py-2 text-white rounded font-medium"
                    :class="editingId ? 'bg-orange-600 hover:bg-orange-700' : 'bg-green-600 hover:bg-green-700'">
              {{ editingId ? 'Modifier défaut' : 'Ajouter défaut' }}
            </button>

            <button type="button"
                    @click="resetForm"
                    class="px-5 py-2 border border-gray-300 rounded hover:bg-gray-50">
              Annuler
            </button>
          </div>

        </form>
      </ComponentCard>

      <!-- ================= TABLE ================= -->
      <ComponentCard title="Liste des Défauts">

        <div v-if="defauts.length === 0" class="text-center py-8 text-gray-500">
          Aucun défaut enregistré
        </div>

        <table v-else class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left">Nom défaut</th>
            <th class="px-6 py-3 text-left">Description</th>
            <th class="px-6 py-3 text-left">Cause probable</th>
            <th class="px-6 py-3 text-left">Solution</th>
            <th class="px-6 py-3 text-left">Fréquence</th>
            <th class="px-6 py-3 text-left">Photo</th>
            <th class="px-6 py-3 text-left w-28">Actions</th>
          </tr>
          </thead>

          <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="d in defauts"
            :key="d.id"
            class="hover:bg-blue-50 transition-colors duration-150 cursor-pointer"
            @click="openDefautModal(d)"
          >
            <td class="px-6 py-4 font-medium">{{ d.nomDefaut }}</td>
            <td class="px-6 py-4 text-gray-600">{{ truncate(d.description) }}</td>
            <td class="px-6 py-4 text-gray-600">{{ truncate(d.causeProbable) }}</td>
            <td class="px-6 py-4 text-gray-600">{{ truncate(d.solution) }}</td>
            <td class="px-6 py-4">{{ d.frequence || '-' }}</td>

            <td class="px-6 py-4">
              <img v-if="d.imagePath"
                   :src="`http://localhost:5100/images/${d.imagePath}`"
                   class="w-16 h-16 object-cover rounded border"
                   alt="Photo du défaut" />
              <span v-else class="text-gray-400">-</span>
            </td>

            <td class="px-6 py-4" @click.stop>
              <div class="flex items-center gap-4">
                <button @click="editDefaut(d)" title="Modifier" class="text-indigo-600 hover:text-indigo-900">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                </button>
                <button @click="deleteDefaut(d.id)" title="Supprimer" class="text-red-600 hover:text-red-800">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M19 7L5 7M10 11V17M14 11V17M6 7L7 19C7 20.1046 7.89543 21 9 21H15C16.1046 21 17 20.1046 17 19L18 7M9 7V5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V7" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </ComponentCard>
    </div>

    <!-- ================= POP-UP (MODAL) PLUS PETIT & UNIFORME ================= -->
    <div v-if="showModal"
         class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/90 backdrop-blur-sm">

      <div class="bg-white w-full max-w-md mx-4 rounded-2xl shadow-2xl overflow-hidden max-h-[82vh] flex flex-col">

        <!-- Header -->
        <div class="px-5 py-4 border-b bg-gray-50 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-800">{{ modalTitle }}</h2>
          <button
            @click="showModal = false"
            class="text-2xl text-gray-400 hover:text-gray-600 leading-none">
            ×
          </button>
        </div>

        <!-- Contenu avec Scroll -->
        <div class="p-5 overflow-y-auto flex-1 text-gray-700 text-sm leading-relaxed">
          <div v-if="selectedDefaut" class="space-y-5">

            <div>
              <p class="text-xs uppercase tracking-widest text-gray-500 mb-1">Nom du défaut</p>
              <p class="font-medium">{{ selectedDefaut.nomDefaut }}</p>
            </div>

            <div>
              <p class="text-xs uppercase tracking-widest text-gray-500 mb-1">Description</p>
              <p class="whitespace-pre-wrap">{{ selectedDefaut.description || 'Non renseignée' }}</p>
            </div>

            <div>
              <p class="text-xs uppercase tracking-widest text-gray-500 mb-1">Cause probable</p>
              <p class="whitespace-pre-wrap">{{ selectedDefaut.causeProbable || 'Non renseignée' }}</p>
            </div>

            <div>
              <p class="text-xs uppercase tracking-widest text-gray-500 mb-1">Solution</p>
              <p class="whitespace-pre-wrap">{{ selectedDefaut.solution || 'Non renseignée' }}</p>
            </div>

            <div class="pt-4 border-t grid grid-cols-2 gap-6">
              <div>
                <p class="text-xs uppercase tracking-widest text-gray-500 mb-1">Fréquence</p>
                <p class="text-xl font-semibold text-blue-600">{{ selectedDefaut.frequence || 0 }}</p>
              </div>

              <div v-if="selectedDefaut.imagePath">
                <p class="text-xs uppercase tracking-widest text-gray-500 mb-2">Photo</p>
                <img
                  :src="`http://localhost:5100/images/${selectedDefaut.imagePath}`"
                  class="w-full rounded-lg border max-h-56 object-contain bg-gray-50"
                  alt="Photo du défaut"
                />
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import api from '@/services/api'

import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'

const currentPageTitle = ref("Gestion des Défauts")
const errorMsg = ref('')

const form = ref({
  nomDefaut: '',
  description: '',
  causeProbable: '',
  solution: '',
  frequence: 0
})

const defauts = ref([])
const imageFile = ref(null)
const imagePreview = ref(null)
const fileInput = ref(null)
const editingId = ref(null)

// Modal
const showModal = ref(false)
const modalTitle = ref('')
const selectedDefaut = ref(null)

/* Load */
const loadDefauts = async () => {
  const res = await api.get('/TypeDefaut')
  defauts.value = res.data
}

onMounted(loadDefauts)

/* Image */
const openFile = () => fileInput.value?.click()

const handleImage = (e) => {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    imagePreview.value = URL.createObjectURL(file)
  }
}

/* Ouvrir le modal */
const openDefautModal = (defaut) => {
  selectedDefaut.value = {...defaut}
  modalTitle.value = `Détail : ${defaut.nomDefaut}`
  showModal.value = true
}

/* Submit */
const submitDefaut = async () => {
  const fd = new FormData()
  fd.append('NomDefaut', form.value.nomDefaut)
  fd.append('Description', form.value.description)
  fd.append('CauseProbable', form.value.causeProbable)
  fd.append('Solution', form.value.solution)
  fd.append('Frequence', form.value.frequence)

  if (imageFile.value) fd.append('ImageFile', imageFile.value)

  try {
    if (editingId.value) {
      await api.put(`/TypeDefaut/${editingId.value}`, fd)
    } else {
      await api.post('/TypeDefaut', fd)
    }
    resetForm()
    loadDefauts()
  } catch (err) {
    errorMsg.value = "Une erreur est survenue"
  }
}

/* Edit */
const editDefaut = (d) => {
  form.value = {
    nomDefaut: d.nomDefaut,
    description: d.description,
    causeProbable: d.causeProbable || '',
    solution: d.solution,
    frequence: d.frequence || 0
  }
  editingId.value = d.id
}

/* Delete */
const deleteDefaut = async (id) => {
  if (confirm('Voulez-vous vraiment supprimer ce défaut ?')) {
    await api.delete(`/TypeDefaut/${id}`)
    loadDefauts()
  }
}

/* Reset */
const resetForm = () => {
  form.value = {
    nomDefaut: '',
    description: '',
    causeProbable: '',
    solution: '',
    frequence: 0
  }
  editingId.value = null
  imageFile.value = null
  imagePreview.value = null
  if (fileInput.value) fileInput.value.value = ''
}

/* Truncate */
const truncate = (text, n = 45) => {
  if (!text) return ''
  return text.length > n ? text.slice(0, n) + '...' : text
}
</script>
