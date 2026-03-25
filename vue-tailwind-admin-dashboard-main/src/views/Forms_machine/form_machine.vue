<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'

// ================= API (PROXY FIX) =================
const API_URL = '/api/Machine'

// ================= STATES =================
const currentPageTitle = ref("Gestion des Machines")

const machine = ref({
  codeMachine: '',
  nomMachine: '',
  actif: true
})

const editingId = ref(null)
const machines = ref([])
const errorMessage = ref('')
const successMessage = ref('')
const loading = ref(false)

// ================= GET =================
const fetchMachines = async () => {
  try {
    loading.value = true
    const res = await axios.get(API_URL)
    machines.value = res.data
  } catch (err) {
    console.log("ERROR:", err)
    errorMessage.value = "Impossible de charger les machines (backend/CORS)."
  } finally {
    loading.value = false
  }
}

// ================= SAVE =================
const saveMachine = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!machine.value.codeMachine || machine.value.codeMachine.length !== 8) {
    errorMessage.value = "Code machine doit contenir 8 caractères"
    return
  }

  if (!machine.value.nomMachine.trim()) {
    errorMessage.value = "Nom machine obligatoire"
    return
  }

  try {
    if (editingId.value) {
      await axios.put(`${API_URL}/${editingId.value}`, machine.value)
      successMessage.value = "Machine modifiée"
    } else {
      await axios.post(API_URL, machine.value)
      successMessage.value = "Machine ajoutée"
    }

    resetForm()
    fetchMachines()

  } catch (err) {
    console.log("ERROR SAVE:", err)
    errorMessage.value = "Erreur serveur / Network Error"
  }
}

// ================= EDIT =================
const editMachine = (m) => {
  machine.value = { ...m }
  editingId.value = m.id
}

// ================= DELETE =================
const deleteMachine = async (id) => {
  if (!confirm("Supprimer cette machine ?")) return

  try {
    await axios.delete(`${API_URL}/${id}`)
    fetchMachines()
  } catch (err) {
    errorMessage.value = "Erreur suppression"
  }
}

// ================= RESET =================
const resetForm = () => {
  machine.value = {
    codeMachine: '',
    nomMachine: '',
    actif: true
  }
  editingId.value = null
}

// ================= INIT =================
onMounted(fetchMachines)
</script>

<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <!-- Formulaire Ajout / Édition -->
    <ComponentCard :title="editingId ? 'Modifier la Machine' : 'Ajouter une Machine'">
      <div v-if="successMessage" class="mb-4 p-4 bg-green-100 text-green-800 rounded-lg">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="mb-4 p-4 bg-red-100 text-red-800 rounded-lg">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="saveMachine" class="space-y-6">
        <div>
          <label class="block mb-2 text-sm font-medium">
            Code Machine <span class="text-red-600">*</span>
          </label>
          <input
            v-model="machine.codeMachine"
            type="text"
            maxlength="8"
            placeholder="Ex: MAC00001"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400"
            :disabled="editingId">   <!-- on bloque souvent le code en édition -->
        </div>

        <div>
          <label class="block mb-2 text-sm font-medium">
            Nom Machine <span class="text-red-600">*</span>
          </label>
          <input
            v-model="machine.nomMachine"
            type="text"
            placeholder="Ex: Presse hydraulique 150T"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400"
          />
        </div>

        <div>
          <label class="block mb-2 text-sm font-medium">État</label>
          <select
            v-model="machine.actif"
            class="w-full px-4 py-2 border rounded-lg bg-white"
          >
            <option :value="true">Active</option>
            <option :value="false">Inactive</option>
          </select>
        </div>

        <div class="flex gap-4">
          <button
            type="submit"
            class="px-6 py-3 text-white bg-green-600 rounded-lg hover:bg-green-700 transition"



            :disabled="loading"
          >
            {{ loading ? 'En cours...' : (editingId ? 'Modifier Machine' : 'Ajouter Machine') }}
          </button>
          <button
            type="button"
            @click="resetForm"
            class="px-5 py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
            :disabled="loading"
          >
            Annuler
          </button>
          <button
            v-if="editingId"
            type="button"
            @click="machine = { codeMachine: '', nomMachine: '', actif: true }; editingId = null"
            class="px-6 py-3 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition"
          >
            Annuler
          </button>
        </div>
      </form>
    </ComponentCard>

    <!-- Liste des machines -->
    <ComponentCard title="Liste des Machines">
      <div v-if="loading" class="text-center py-8 text-gray-500">Chargement...</div>
      <div v-else-if="machines.length === 0" class="text-center py-8 text-gray-500">
        Aucune machine pour le moment
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nom</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">État</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="m in machines" :key="m.id || m.codeMachine" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ m.codeMachine }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ m.nomMachine }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
                    m.actif ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  ]"
                >
                  {{ m.actif ? 'Active' : 'Inactive' }}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <button
                @click="editMachine(m)"
                class="text-indigo-600 hover:text-indigo-900 mr-3"
                title="Modifier"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
              </button>

              <button
                @click="deleteMachine(m.id || m.codeMachine)"
                class="text-red-600 hover:text-red-900"
                title="Supprimer"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </ComponentCard>
  </AdminLayout>
</template>
