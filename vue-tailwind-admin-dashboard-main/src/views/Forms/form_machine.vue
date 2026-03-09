<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <ComponentCard title="Ajouter une Machine">
      <form @submit.prevent="addMachine" class="space-y-5">

        <!-- Nom Machine -->
        <div>
          <label class="block mb-2 text-sm font-medium">Nom Machine</label>
          <input
            v-model="machine.name"
            type="text"
            placeholder="Entrer le nom de la machine"
            class="w-full px-4 py-2 border rounded-lg focus:ring focus:ring-blue-200"
          />
        </div>



        <!-- Etat -->
        <div>
          <label class="block mb-2 text-sm font-medium">Etat</label>
          <select
            v-model="machine.status"
            class="w-full px-4 py-2 border rounded-lg"
          >
            <option value="">Choisir état</option>
            <option value="active">Active</option>
            <option value="maintenance">Maintenance</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>

        <!-- Description -->
        <div>
          <label class="block mb-2 text-sm font-medium">Description</label>
          <textarea
            v-model="machine.description"
            rows="4"
            class="w-full px-4 py-2 border rounded-lg"
            placeholder="Description de la machine"
          ></textarea>
        </div>

        <!-- bouton -->
        <button
          type="submit"
          class="px-6 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
        >
          Ajouter Machine
        </button>

      </form>
    </ComponentCard>

  </AdminLayout>
</template>

<script setup>
import { ref } from 'vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'

const currentPageTitle = ref("Ajouter Machine")

const machine = ref({
  name: '',
  type: '',
  status: '',
  description: ''
})

const addMachine = () => {
  console.log(machine.value)
}
</script>
