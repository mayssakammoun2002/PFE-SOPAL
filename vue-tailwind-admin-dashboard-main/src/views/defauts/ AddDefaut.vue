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
            <textarea v-model="form.description" class="w-full border p-2 rounded" required></textarea>
          </div>

          <!-- ✅ NEW -->
          <div>
            <label class="block mb-2 text-sm font-medium">Cause probable <span class="text-red-600">*</span></label>
            <textarea v-model="form.causeProbable" class="w-full border p-2 rounded" required></textarea>
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Solution <span class="text-red-600">*</span></label>
            <textarea v-model="form.solution" class="w-full border p-2 rounded" required></textarea>
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Fréquence</label>
            <input v-model="form.frequence" type="number" class="w-full border p-2 rounded" />
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
              class="px-5 py-2 border border-gray-300 rounded hover:bg-gray-50"
            >
              Annuler
            </button>
          </div>

        </form>
      </ComponentCard>

      <!-- ================= TABLE ================= -->
      <ComponentCard title="Liste des Défauts">

        <div v-if="defauts.length === 0" class="text-center py-6 text-gray-500">
          Aucun défaut
        </div>

        <table v-else class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3">Nom</th>
            <th class="px-6 py-3">Description</th>
            <th class="px-6 py-3">Cause</th> <!-- ✅ -->
            <th class="px-6 py-3">Solution</th>
            <th class="px-6 py-3">Fréquence</th>
            <th class="px-6 py-3">Photo</th>
            <th class="px-6 py-3">Actions</th>
          </tr>
          </thead>

          <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="d in defauts" :key="d.id">

            <td class="px-6 py-4">{{ d.nomDefaut }}</td>

            <td class="px-6 py-4">{{ truncate(d.description) }}</td>

            <!-- ✅ -->
            <td class="px-6 py-4">{{ truncate(d.causeProbable) }}</td>

            <td class="px-6 py-4">{{ truncate(d.solution) }}</td>

            <td class="px-6 py-4">{{ d.frequence || '-' }}</td>

            <td class="px-6 py-4">
              <img v-if="d.imagePath"
                   :src="`http://localhost:5100/images/${d.imagePath}`"
                   class="w-20 h-20 object-cover rounded" />
              <span v-else>-</span>
            </td>

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
                      d="M19 7L5 7M10 11V17M14 11V17M6 7L7 19C7 20.1046 7.89543 21 9 21H15C16.1046 21 17 20.1046 17 19L18 7M9 7V5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V7"
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
import api from '@/services/api'

import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'

const currentPageTitle = ref("Gestion des Défauts")
const errorMsg = ref('')

const form = ref({
  nomDefaut: '',
  description: '',
  causeProbable: '', // ✅
  solution: '',
  frequence: 0
})

const defauts = ref([])
const imageFile = ref(null)
const imagePreview = ref(null)
const fileInput = ref(null)
const editingId = ref(null)

/* LOAD */
const loadDefauts = async () => {
  const res = await api.get('/TypeDefaut')
  defauts.value = res.data
}

onMounted(loadDefauts)

/* IMAGE */
const openFile = () => fileInput.value.click()

const handleImage = (e) => {
  const file = e.target.files[0]
  imageFile.value = file
  imagePreview.value = URL.createObjectURL(file)
}

/* SUBMIT */
const submitDefaut = async () => {
  const fd = new FormData()

  fd.append('NomDefaut', form.value.nomDefaut)
  fd.append('Description', form.value.description)
  fd.append('CauseProbable', form.value.causeProbable) // ✅
  fd.append('Solution', form.value.solution)
  fd.append('Frequence', form.value.frequence)

  if (imageFile.value) {
    fd.append('ImageFile', imageFile.value)
  }

  if (editingId.value) {
    await api.put(`/TypeDefaut/${editingId.value}`, fd)
  } else {
    await api.post('/TypeDefaut', fd)
  }

  resetForm()
  loadDefauts()
}

/* EDIT */
const editDefaut = (d) => {
  form.value = {
    nomDefaut: d.nomDefaut,
    description: d.description,
    causeProbable: d.causeProbable,
    solution: d.solution,
    frequence: d.frequence
  }
  editingId.value = d.id
}

/* DELETE */
const deleteDefaut = async (id) => {
  await api.delete(`/TypeDefaut/${id}`)
  loadDefauts()
}

/* RESET */
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
}

/* UTILS */
const truncate = (text, n = 40) =>
  text?.length > n ? text.slice(0, n) + '...' : text
</script>
