<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">

      <!-- FORMULAIRE -->
      <ComponentCard title="Ajouter Type de Défaut">
        <form @submit.prevent="addDefaut" class="space-y-4">

          <!-- Nom -->
          <div>
            <label class="block mb-1">Nom défaut</label>
            <input
              v-model="defaut.nom"
              type="text"
              class="w-full border p-2 rounded"
              placeholder="Nom du défaut"
              required
            />
          </div>

          <!-- Description -->
          <div>
            <label class="block mb-1">Description</label>
            <textarea
              v-model="defaut.description"
              class="w-full border p-2 rounded"
              placeholder="Description"
            ></textarea>
          </div>

          <!-- Gravité -->
          <div>
            <label class="block mb-1">Gravité</label>
            <select v-model="defaut.gravite" class="w-full border p-2 rounded">
              <option value="">Choisir</option>
              <option value="faible">Faible</option>
              <option value="moyenne">Moyenne</option>
              <option value="critique">Critique</option>
            </select>
          </div>

          <!-- Upload Photo -->
          <div>
            <label class="block mb-2">Photo défaut</label>

            <!-- input caché -->
            <input
              type="file"
              ref="fileInput"
              class="hidden"
              @change="handleImage"
            />

            <!-- bouton joli -->
            <button
              type="button"
              @click="openFile"
              class="flex items-center gap-2 px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
            >
              📷 Ajouter Photo
            </button>
          </div>

          <!-- preview -->
          <div v-if="imagePreview">
            <img :src="imagePreview" class="w-32 mt-2 rounded shadow"/>
          </div>

          <button class="px-4 py-2 text-white bg-green-600 rounded hover:bg-green-700">
            Ajouter
          </button>

        </form>
      </ComponentCard>

      <!-- LISTE -->
      <ComponentCard title="Liste Types Défauts">

        <table class="w-full border">

          <thead>
          <tr class="bg-gray-100">
            <th class="p-2">Nom</th>
            <th>Description</th>
            <th>Gravité</th>
            <th>Photo</th>
            <th>Actions</th>
          </tr>
          </thead>

          <tbody>

          <tr v-for="d in defauts" :key="d.id" class="text-center border-t">

            <td>{{ d.nom }}</td>
            <td>{{ d.description }}</td>
            <td>{{ d.gravite }}</td>

            <td>
              <img
                v-if="d.photo"
                :src="d.photo"
                class="w-12 mx-auto"
              />
            </td>

            <td class="space-x-2">

              <button
                class="px-2 py-1 text-white bg-yellow-500 rounded"
                @click="editDefaut(d)"
              >
                Modifier
              </button>

              <button
                class="px-2 py-1 text-white bg-red-600 rounded"
                @click="deleteDefaut(d.id)"
              >
                Supprimer
              </button>

            </td>

          </tr>

          </tbody>

        </table>

      </ComponentCard>

    </div>

  </AdminLayout>
</template>

<script setup>

import { ref } from 'vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'

const currentPageTitle = ref("Type Défaut")

const defaut = ref({
  nom:'',
  description:'',
  gravite:''
})

const defauts = ref([])

const imageFile = ref(null)
const imagePreview = ref(null)
const fileInput = ref(null)

const openFile = ()=>{
  fileInput.value.click()
}

const handleImage = (event)=>{
  imageFile.value = event.target.files[0]
  imagePreview.value = URL.createObjectURL(imageFile.value)
}

const addDefaut = () => {

  const newDefaut = {
    id: Date.now(),
    nom: defaut.value.nom,
    description: defaut.value.description,
    gravite: defaut.value.gravite,
    photo: imagePreview.value
  }

  defauts.value.push(newDefaut)

  defaut.value = {
    nom:'',
    description:'',
    gravite:''
  }

  imagePreview.value = null
}

const deleteDefaut = (id)=>{
  defauts.value = defauts.value.filter(d => d.id !== id)
}

const editDefaut = (d) => {
  defaut.value = { ...d }
}

</script>
