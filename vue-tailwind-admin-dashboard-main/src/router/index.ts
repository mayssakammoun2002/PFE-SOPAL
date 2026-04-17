import { createRouter, createWebHistory } from 'vue-router'

/* ✅ GET USER (TOKEN + ROLE) */
function getUser() {
  try {
    const userStr = localStorage.getItem('user')
    const user = userStr ? JSON.parse(userStr) : null
    return user && user.token ? user : null
  } catch {
    return null
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { left: 0, top: 0 }
  },

  routes: [
    {
      path: '/',
      name: 'signin',
      component: () => import('../views/Auth/Signin.vue'),
      meta: { title: 'Signin' }
    },
    {
      path: '/signin',
      name: 'Signin',
      component: () => import('../views/Auth/Signin.vue'),
      meta: { title: 'Signin' }
    },
    {
      path: '/signup',
      name: 'Signup',
      component: () => import('../views/Auth/Signup.vue'),
      meta: { title: 'Signup' }
    },

    /* ================== PROTECTED ROUTES ================== */

    {
      path: '/calendar',
      name: 'Calendar',
      component: () => import('../views/Others/Calendar.vue'),
      meta: { title: 'Calendar', requiresAuth: true }
    },

    {
      path: '/profile',
      name: 'Profile',
      component: () => import('../views/Others/UserProfile.vue'),
      meta: { title: 'Profile', requiresAuth: true }
    },

    {
      path: '/form-elements',
      name: 'Form Elements',
      component: () => import('@/views/Forms_machine/FormElements.vue'),
      meta: { title: 'Form Elements', requiresAuth: true }
    },

    {
      path: '/basic-tables',
      name: 'Basic Tables',
      component: () => import('../views/Tables/BasicTables.vue'),
      meta: { title: 'Basic Tables', requiresAuth: true }
    },

    {
      path: '/form_crudUser',
      name: 'Form User',
      component: () => import('@/views/User/Gestion_user.vue'),
      meta: {
        title: 'Gestion Utilisateur',
        requiresAuth: true,
        requiresAdmin: true
      }
    },

    {
      path: '/form_crudmachine',
      name: 'Form Machine',
      component: () => import('@/views/Forms_machine/form_machine.vue'),
      meta: {
        title: 'Gestion Machine',
        requiresAuth: true
      }
    },

    {
      path: '/form_crudtypedefaut',
      name: 'Form Type Defaut',
      component: () => import('../views/defauts/ AddDefaut.vue'),
      meta: {
        title: 'Gestion Type De Défaut',
        requiresAuth: true
      }



    },

    {
      path: '/form_litedesproduits',
      name: 'Produits',
      component: () => import('../views/produit/AddProduit.vue'),
      meta: {
        title: 'Gestion des produits',
        requiresAuth: true
      }
    },

    {
      path: '/form_resultat_de_controle',
      name: 'Controle',
      component: () => import('../views/resultat_controle/controle.vue'),
      meta: {
        title: 'Résultat de contrôle',
        requiresAuth: true
      }
    },

    /* ================== UI ROUTES ================== */

    {
      path: '/alerts',
      name: 'Alerts',
      component: () => import('../views/UiElements/Alerts.vue'),
      meta: { title: 'Alerts', requiresAuth: true }
    },
    {
      path: '/avatars',
      name: 'Avatars',
      component: () => import('../views/UiElements/Avatars.vue'),
      meta: { title: 'Avatars', requiresAuth: true }
    },
    {
      path: '/badge',
      name: 'Badge',
      component: () => import('../views/UiElements/Badges.vue'),
      meta: { title: 'Badge', requiresAuth: true }
    },
    {
      path: '/buttons',
      name: 'Buttons',
      component: () => import('../views/UiElements/Buttons.vue'),
      meta: { title: 'Buttons', requiresAuth: true }
    },
    {
      path: '/images',
      name: 'Images',
      component: () => import('../views/UiElements/Images.vue'),
      meta: { title: 'Images', requiresAuth: true }
    },
    {
      path: '/videos',
      name: 'Videos',
      component: () => import('../views/UiElements/Videos.vue'),
      meta: { title: 'Videos', requiresAuth: true }
    },

    /* ================== OTHER ================== */

    {
      path: '/blank',
      name: 'Blank',
      component: () => import('../views/Pages/BlankPage.vue'),
      meta: { title: 'Blank', requiresAuth: true }
    },
    {
      path: '/error-404',
      name: '404 Error',
      component: () => import('../views/Errors/FourZeroFour.vue'),
      meta: { title: '404 Error' }
    }
  ]
})

/* ================== GLOBAL GUARD ================== */
router.beforeEach((to, from, next) => {
  const user = getUser()

  // 🔥 TITLE
  document.title = `Vue.js ${to.meta.title || ''} | Dashboard`

  // ❌ NOT LOGGED IN
  if (to.meta.requiresAuth && !user) {
    return next('/signin')
  }

  // ❌ NOT ADMIN
  if (to.meta.requiresAdmin && user?.role !== 'Admin') {
    return next('/form_resultat_de_controle')
  }

  next()
})

export default router
