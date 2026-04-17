<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <div class="space-y-8">

      <!-- FORM -->
      <ComponentCard title="Ajouter un utilisateur">
        <form @submit.prevent="handleSubmit" class="space-y-6 max-w-2xl">

          <input v-model="form.firstName" placeholder="Prénom" class="input" required />
          <input v-model="form.lastName" placeholder="Nom" class="input" required />
          <input v-model="form.email" type="email" placeholder="Email" class="input" required />
          <input v-model="form.password" type="password" placeholder="Mot de passe" class="input" required />

          <select v-model="form.role" class="input">
            <option :value="0">User</option>
            <option :value="1">Admin</option>
          </select>

          <div v-if="errorMessage" class="msg-error">
            {{ errorMessage }}
          </div>

          <div v-if="successMessage" class="msg-success">
            {{ successMessage }}
          </div>

          <div class="flex justify-end gap-4 pt-4">
            <button type="button" @click="resetForm" class="btn-cancel">
              Annuler
            </button>

            <button type="submit" class="btn-primary">
              <span v-if="isEdit">Modifier</span>
              <span v-else>Ajouter</span>
            </button>
          </div>

        </form>
      </ComponentCard>

      <!-- TABLE -->
      <ComponentCard title="Liste des utilisateurs">

        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">

            <thead class="bg-gray-50">
            <tr>
              <th class="th">Nom</th>
              <th class="th">Email</th>
              <th class="th">Rôle</th>
              <th class="th">Actions</th>
            </tr>
            </thead>

            <tbody class="bg-white divide-y divide-gray-200">

            <tr v-for="u in users" :key="u.id">

              <td class="td">
                {{ u.firstName }} {{ u.lastName }}
              </td>

              <td class="td">
                {{ u.email }}
              </td>

              <td class="td">
                  <span v-if="u.role === 1 || u.role === 'Admin'" class="role-admin">
                    Admin
                  </span>
                <span v-else class="role-user">
                    User
                  </span>
              </td>

              <td class="td">
                <div class="flex gap-3">

                  <button
                    @click="editUser(u)"
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
                  <button
                    @click="deleteUser(u.id)"
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
        </div>

      </ComponentCard>

    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'
const users = ref([])
const errorMessage = ref('')
const successMessage = ref('')
const isEdit = ref(false)

const form = ref({
  id: null,
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  role: 0
})

/* 🔐 CHECK ADMIN */
const checkAdmin = () => {
  const userStr = localStorage.getItem('user')

  if (!userStr) {
    window.location.href = '/login'
    return
  }

  const user = JSON.parse(userStr)

  if (user?.role !== "Admin" && user?.Role !== "Admin") {
    window.location.href = '/form_resultat_de_controle'
  }
}

/* 📥 GET USERS */
const fetchUsers = async () => {
  try {
    const res = await api.get('/Utilisateur')
    users.value = res.data
  } catch (err) {
    errorMessage.value = "Accès refusé (401 - token manquant)"
  }
}

/* RESET */
const resetForm = () => {
  form.value = {
    id: null,
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    role: 0
  }
  isEdit.value = false
}

/* ➕ / ✏️ SUBMIT */
const handleSubmit = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  try {
    if (isEdit.value) {
      await api.put(`/Utilisateur/${form.value.id}`, form.value)
      successMessage.value = "Utilisateur modifié"
    } else {
      await api.post('/Utilisateur/signup', form.value)
      successMessage.value = "Utilisateur ajouté"
    }

    resetForm()
    fetchUsers()

  } catch (err) {
    errorMessage.value = "Erreur serveur ou 401 Unauthorized"
  }
}

/* ✏️ EDIT */
const editUser = (u) => {
  isEdit.value = true

  form.value = {
    id: u.id,
    firstName: u.firstName,
    lastName: u.lastName,
    email: u.email,
    password: '',
    role: u.role === 1 || u.role === "Admin" ? 1 : 0
  }
}

/* 🗑 DELETE */
const deleteUser = async (id) => {
  if (!confirm("Supprimer cet utilisateur ?")) return

  try {
    await api.delete(`/Utilisateur/${id}`)
    fetchUsers()
  } catch (err) {
    errorMessage.value = "Suppression refusée (401)"
  }
}

/* INIT */
onMounted(() => {
  checkAdmin()
  fetchUsers()
})
</script>

<style>
.input {
  width: 100%;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
}

.btn-primary {
  background: #16a34a;
  color: white;
  padding: 10px 20px;
  border-radius: 10px;
}

.btn-cancel {
  border: 1px solid #ccc;
  padding: 10px 20px;
  border-radius: 10px;
}

.th {
  padding: 12px;
  text-align: left;
  font-size: 12px;
  color: gray;
}

.td {
  padding: 12px;
}

.role-admin {
  color: red;
  font-weight: bold;
}

.role-user {
  color: blue;
  font-weight: bold;
}

.msg-error {
  background: #fee2e2;
  padding: 10px;
  border-radius: 8px;
  color: red;
}

.msg-success {
  background: #dcfce7;
  padding: 10px;
  border-radius: 8px;
  color: green;
}
</style>
