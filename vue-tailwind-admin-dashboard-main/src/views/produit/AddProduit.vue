<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <ComponentCard title="Ajouter Produit">
      <form @submit.prevent="addProduit" class="space-y-4">

        <!-- Code Article -->
        <div>
          <label>Code Article</label>
          <input v-model="produit.codeArticle" type="text" class="w-full border p-2 rounded" required />
        </div>

        <!-- Numéro OF -->
        <div>
          <label>Numéro d'ordre de fabrication (OF)</label>
          <input v-model="produit.numOF" type="text" class="w-full border p-2 rounded" placeholder="Ex: OF12345678" required />
        </div>

        <!-- Nombre d'échantillons -->
        <div>
          <label>Nombre d'échantillons</label>
          <input v-model.number="produit.nbEchantillons" type="number" min="1" class="w-full border p-2 rounded" />
        </div>

        <!-- Type de défaut (liste) -->
        <div>
          <label>Type de Défaut</label>
          <select v-model="produit.defaut" @change="updatePhoto" class="w-full border p-2 rounded">
            <option value="">Choisir un défaut</option>
            <option v-for="d in defauts" :key="d.id" :value="d.nom">{{ d.nom }}</option>
          </select>
        </div>

        <!-- Affichage automatique de la photo du défaut -->
        <div v-if="produitPhoto" class="mt-2">
          <label>Photo du défaut :</label>
          <img :src="produitPhoto" class="w-32 rounded shadow"/>
        </div>

        <button class="px-4 py-2 text-white bg-green-600 rounded hover:bg-green-700">
          Ajouter Produit
        </button>
      </form>
    </ComponentCard>

    <!-- Liste Produits -->
    <ComponentCard title="Liste des Produits">
      <table class="w-full border">
        <thead>
        <tr class="bg-gray-100">
          <th>Code Article</th>
          <th>Num OF</th>
          <th>Défaut</th>
          <th>Photo</th>
          <th>Nb Échantillons</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="p in produits" :key="p.id" class="text-center border-t">
          <td>{{ p.codeArticle }}</td>
          <td>{{ p.numOF }}</td>
          <td>{{ p.defaut }}</td>
          <td><img v-if="p.photo" :src="p.photo" class="w-12 mx-auto"/></td>
          <td>{{ p.nbEchantillons }}</td>
        </tr>
        </tbody>
      </table>
    </ComponentCard>

  </AdminLayout>
</template>

<script setup>
import { ref } from 'vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'

const currentPageTitle = ref("Ajouter Produit")

// Types de défaut avec photo
const defauts = ref([
  { id:1, nom:'Rayure', photo:'/images/defauts/rayure.jpg' },
  { id:2, nom:'Cassure', photo:'/images/defauts/cassure.jpg' },
  { id:3, nom:'Fissure', photo:'/images/defauts/fissure.jpg' }
])

const produit = ref({
  codeArticle: '',
  numOF: '',
  nbEchantillons: 1,
  defaut: ''
})

const produits = ref([])

// photo automatique selon défaut
const produitPhoto = ref(null)

// mettre à jour la photo automatiquement
const updatePhoto = () => {
  const selected = defauts.value.find(d => d.nom === produit.value.defaut)
  produitPhoto.value = selected ? selected.photo : null
}

// ajouter produit
const addProduit = () => {
  const ofPattern = /^OF\d{8}$/
  if (!ofPattern.test(produit.value.numOF)) {
    alert("Numéro OF invalide : doit commencer par OF + 8 chiffres")
    return
  }

  produits.value.push({
    id: Date.now(),
    codeArticle: produit.value.codeArticle,
    numOF: produit.value.numOF,
    nbEchantillons: produit.value.nbEchantillons,
    defaut: produit.value.defaut,
    photo: produitPhoto.value
  })

  produit.value = { codeArticle:'', numOF:'', nbEchantillons:1, defaut:'' }
  produitPhoto.value = null
}
</script>
