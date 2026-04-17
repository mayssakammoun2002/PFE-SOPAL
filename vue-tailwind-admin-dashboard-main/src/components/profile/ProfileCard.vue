<template>
  <div>
    <!-- PROFILE CARD -->
    <div class="p-5 mb-6 border rounded-2xl">
      <div class="flex justify-between items-center">

        <!-- USER INFO -->
        <div class="flex items-center gap-4">
          <img src="/images/user/owner.jpg" class="w-20 h-20 rounded-full" />

          <div>
            <h4 class="text-lg font-semibold">
              {{ user.firstName }} {{ user.lastName }}
            </h4>

            <p class="text-sm text-gray-500">
              {{ user.role }}
            </p>

            <p class="text-sm text-gray-500">
              {{ user.email }}
            </p>
          </div>
        </div>

        <!-- BUTTON -->
        <button @click="isModal = true" class="px-4 py-2 bg-blue-500 text-white rounded">
          Edit
        </button>

      </div>
    </div>

    <!-- MODAL -->
    <div v-if="isModal" class="fixed inset-0 flex items-center justify-center bg-black/50">
      <div class="bg-white p-6 rounded-lg w-[400px]">

        <h3 class="text-lg font-bold mb-4">Edit Profile</h3>

        <input v-model="user.firstName" placeholder="First Name" class="input" />
        <input v-model="user.lastName" placeholder="Last Name" class="input" />
        <input v-model="user.email" placeholder="Email" class="input" />

        <div class="flex justify-end gap-2 mt-4">
          <button @click="isModal = false" class="px-3 py-1 border rounded">
            Cancel
          </button>

          <button @click="saveProfile" class="px-3 py-1 bg-blue-500 text-white rounded">
            Save
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const isModal = ref(false)

const user = ref({
  id: null,
  firstName: '',
  lastName: '',
  email: '',
  role: ''
})

// 🔥 GET USER CONNECTÉ
onMounted(async () => {
  try {
    const token = localStorage.getItem('token')

    const res = await axios.get('https://localhost:5001/api/utilisateur/me', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    user.value = res.data

  } catch (error) {
    console.error(error)
  }
})

// 🔥 UPDATE USER
const saveProfile = async () => {
  try {
    const token = localStorage.getItem('token')

    await axios.put(
      `https://localhost:5001/api/utilisateur/${user.value.id}`,
      user.value,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    alert("Profile updated ✅")
    isModal.value = false

  } catch (error) {
    console.error(error)
  }
}
</script>

<style>
.input {
  width: 100%;
  border: 1px solid gray;
  padding: 8px;
  margin-top: 8px;
  border-radius: 6px;
}
</style>
