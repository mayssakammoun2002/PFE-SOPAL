<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">

      <!-- FORMULAIRE AJOUT / MODIF -->
      <ComponentCard :title="editMode ? 'Modifier Machine' : 'Ajouter Machine'">
        <form @submit.prevent="submitMachine" class="space-y-5">

          <div>
            <label class="block mb-2 text-sm font-medium">Code Machine</label>
            <input v-model="machine.codeMachine"
                   type="text"
                   placeholder="Code unique (8 caractères)"
                   maxlength="8"
                   class="w-full px-4 py-2 border rounded-lg"
                   :readonly="editMode"
                   required />
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Nom Machine</label>
            <input v-model="machine.nomMachine"
                   type="text"
                   placeholder="Nom machine"
                   class="w-full px-4 py-2 border rounded-lg"
                   required />
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Etat</label>
            <select v-model="machine.actif" class="w-full px-4 py-2 border rounded-lg">
              <option :value="true">Active</option>
              <option :value="false">Inactive</option>
            </select>
          </div>

          <div>
            <label class="block mb-2 text-sm font-medium">Photo Machine</label>
            <input type="file" @change="handleImage" />
          </div>

          <div v-if="imagePreview">
            <img :src="imagePreview" class="w-32 mt-2 rounded shadow" />
          </div>

          <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            {{ editMode ? 'Modifier' : 'Ajouter' }}
          </button>

          <button v-if="editMode" type="button" @click="resetForm" class="px-6 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
            Annuler
          </button>

        </form>
      </ComponentCard>

      <!-- LISTE DES MACHINES -->
      <ComponentCard title="Liste Machines">
        <table class="w-full border">
          <thead>
          <tr class="bg-gray-100">
            <th>Code</th>
            <th>Nom</th>
            <th>Etat</th>
            <th>Photo</th>
            <th>Actions</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="m in machines" :key="m.codeMachine" class="text-center border-t">
            <td>{{ m.codeMachine }}</td>
            <td>{{ m.nomMachine }}</td>
            <td>{{ m.actif ? 'Active' : 'Inactive' }}</td>
            <td>
              <img v-if="m.photo" :src="m.photo" class="w-12 mx-auto rounded" />
            </td>
            <td class="space-x-2">
              <button @click="editMachine(m)" class="px-2 py-1 bg-yellow-500 text-white rounded">Modifier</button>
              <button @click="deleteMachine(m.codeMachine)" class="px-2 py-1 bg-red-600 text-white rounded">Supprimer</button>
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
import MachineService from '@/services/MachineService.js'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'

const currentPageTitle = ref("CRUD Machines")
const machines = ref([])

const machine = ref({
  codeMachine: '',
  nomMachine: '',
  actif: true,
  photo: null
})

const imageFile = ref(null)
const imagePreview = ref(null)
const editMode = ref(false)

const getMachines = () => {
  MachineService.getAll().then(res => {
    machines.value = res.data
  })
}

const handleImage = (event) => {
  imageFile.value = event.target.files[0]
  imagePreview.value = URL.createObjectURL(imageFile.value)
  machine.value.photo = imagePreview.value
}

const submitMachine = () => {
  if(editMode.value) {
    MachineService.update(machine.value.codeMachine, machine.value)
      .then(() => {
        getMachines()
        resetForm()
      })
  } else {
    MachineService.create(machine.value)
      .then(() => {
        getMachines()
        resetForm()
      })
  }
}

const editMachine = (m) => {
  machine.value = {...m}
  imagePreview.value = m.photo
  editMode.value = true
}

const deleteMachine = (code) => {
  if(confirm("Supprimer cette machine ?")) {
    MachineService.delete(code).then(() => getMachines())
  }
}

const resetForm = () => {
  machine.value = { codeMachine:'', nomMachine:'', actif:true, photo:null }
  imageFile.value = null
  imagePreview.value = null
  editMode.value = false
}

onMounted(getMachines)
</script>
