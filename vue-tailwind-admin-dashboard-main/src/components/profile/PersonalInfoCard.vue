<template>
  <div>
    <div class="p-5 mb-6 border rounded-2xl">
      <h4 class="text-lg font-semibold mb-4">Utilisateur connecté</h4>

      <div v-if="user">
        <p><b>First Name:</b> {{ user.firstName }}</p>
        <p><b>Last Name:</b> {{ user.lastName }}</p>
        <p><b>Email:</b> {{ user.email }}</p>
        <p><b>Role:</b> {{ user.role }}</p>
      </div>
      <div v-else>Chargement...</div>

      <button @click="isModalOpen = true" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">
        Edit
      </button>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-xl w-[400px]">
        <h3 class="text-lg font-semibold mb-4">Edit Profile</h3>

        <input v-model="user.firstName" placeholder="First Name" class="border p-2 w-full mb-2 rounded"/>
        <input v-model="user.lastName"  placeholder="Last Name"  class="border p-2 w-full mb-2 rounded"/>
        <input v-model="user.email"     placeholder="Email"       class="border p-2 w-full mb-2 rounded"/>

        <div class="flex justify-end gap-2 mt-4">
          <button @click="isModalOpen = false" class="px-4 py-2 border rounded">Cancel</button>
          <button @click="saveProfile" class="px-4 py-2 bg-blue-500 text-white rounded">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from "vue"
import axios from "axios"

const user = ref(null)
const isModalOpen = ref(false)

// ✅ Lire depuis 'user' (pas 'token')
const getTokenAndId = () => {
  const stored = localStorage.getItem('user')
  if (!stored) return {token: null, id: null}
  const parsed = JSON.parse(stored)
  return {token: parsed.token, id: parsed.id}
}

const getUser = async () => {
  const {token, id} = getTokenAndId()

  if (!token) {
    console.warn("Pas de token trouvé")
    return
  }

  try {
    const res = await axios.get(`http://localhost:5100/api/Utilisateur/${id}`, {
      headers: {Authorization: `Bearer ${token}`}
    })
    user.value = res.data
  } catch (err) {
    console.error("Erreur récupération user:", err)
  }
}

const saveProfile = async () => {
  const {token} = getTokenAndId()

  try {
    await axios.put(
      `http://localhost:5100/api/Utilisateur/${user.value.id}`,
      {
        firstName: user.value.firstName,
        lastName: user.value.lastName,
        email: user.value.email,
        role: user.value.role
      },
      {headers: {Authorization: `Bearer ${token}`}}
    )

    // ✅ Mettre à jour le localStorage aussi
    const stored = JSON.parse(localStorage.getItem('user'))
    localStorage.setItem('user', JSON.stringify({...stored, ...user.value}))

    alert("Profil mis à jour ✅")
    isModalOpen.value = false
  } catch (err) {
    console.error("Erreur update:", err)
  }
}

onMounted(() => getUser())
</script>
