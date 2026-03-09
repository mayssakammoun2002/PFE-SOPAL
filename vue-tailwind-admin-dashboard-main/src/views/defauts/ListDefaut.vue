<template>
  <ComponentCard title="Liste Type Défaut">

    <table class="w-full border">

      <tr>
        <th>Nom</th>
        <th>Description</th>
        <th>Gravité</th>
        <th>Actions</th>
      </tr>

      <tr v-for="d in defauts" :key="d.id">
        <td>{{d.nom}}</td>
        <td>{{d.description}}</td>
        <td>{{d.gravite}}</td>

        <td>
          <button @click="editDefaut(d)">Modifier</button>
          <button @click="deleteDefaut(d.id)">Supprimer</button>
        </td>

      </tr>

    </table>

  </ComponentCard>
</template>

<script setup>
import { ref } from 'vue'

const defauts = ref([
  { id:1, nom:"Rayure", description:"surface rayée", gravite:"faible"},
  { id:2, nom:"Cassure", description:"produit cassé", gravite:"critique"}
])

const deleteDefaut = (id)=>{
  defauts.value = defauts.value.filter(d=>d.id!==id)
}

const editDefaut = (d)=>{
  console.log("edit",d)
}
</script>
