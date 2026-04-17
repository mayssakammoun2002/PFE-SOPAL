import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5100/api'
})

// 🔥 TRÈS IMPORTANT
api.interceptors.request.use(config => {
  const user = JSON.parse(localStorage.getItem('user'))

  console.log("USER =>", user) // 👈 DEBUG

  if (user && user.token) {
    config.headers.Authorization = `Bearer ${user.token}`
  }

  return config
})

export default api
