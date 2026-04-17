```vue
<template>
  <div>
    <!-- PROFILE -->
    <div class="p-5 mb-6 border rounded-2xl">
      <h4 class="text-lg font-semibold mb-4">Utilisateur connecté</h4>

      <div v-if="user">
        <p><b>First Name:</b> {{ user.firstName }}</p>
        <p><b>Last Name:</b> {{ user.lastName }}</p>
        <p><b>Email:</b> {{ user.email }}</p>
        <p><b>Role:</b> {{ user.role }}</p>
      </div>

      <div v-else>
        Chargement...
      </div>

      <button @click="isModalOpen = true" class="mt-4">
        Edit
      </button>
    </div>

    <!-- MODAL -->
    <div v-if="isModalOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-xl w-[400px]">
        <h3 class="text-lg font-semibold mb-4">Edit Profile</h3>

        <input v-model="user.firstName" placeholder="First Name" class="border p-2 w-full mb-2"/>
        <input v-model="user.lastName" placeholder="Last Name" class="border p-2 w-full mb-2"/>
        <input v-model="user.email" placeholder="Email" class="border p-2 w-full mb-2"/>

        <div class="flex justify-end gap-2 mt-4">
          <button @click="isModalOpen = false">Cancel</button>
          <button @click="saveProfile">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

// 🔥 STATE
const user = ref(null)
const isModalOpen = ref(false)

// 🔥 TOKEN
const token = localStorage.getItem("token")

// 🔥 GET USER CONNECTÉ AUTOMATIQUEMENT
const getUser = async () => {
  if (!token) {
    console.log("Pas de token")
    return
  }

  try {
    const res = await axios.get("http://localhost:5100/api/Utilisateur/me", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    user.value = res.data
  } catch (err) {
    console.error("Erreur récupération user:", err)
  }
}

// 🔥 UPDATE USER
const saveProfile = async () => {
  try {
    await axios.put(
      `http://localhost:5100/api/Utilisateur/${user.value.id}`,
      {
        firstName: user.value.firstName,
        lastName: user.value.lastName,
        email: user.value.email,
        role: 1 // ⚠️ adapte selon ton enum
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    alert("Profil mis à jour ✅")
    isModalOpen.value = false
  } catch (err) {
    console.error("Erreur update:", err)
  }
}

// 🔥 AUTO LOAD
onMounted(() => {
  getUser()
})
</script>
```
