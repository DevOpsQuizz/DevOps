import { createRouter, createWebHistory } from 'vue-router'
<<<<<<< HEAD
import HomeView from '@/views/HomeView.vue'
import AdminLoginView from '@/views/AdminLoginView.vue'
import UserLoginView from '@/views/UserLoginView.vue'
import UserRegisterView from '@/views/UserRegisterView.vue'
=======
import HomePage from '../views/HomePage.vue'
>>>>>>> laura

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
<<<<<<< HEAD
    {
      path: '/admin/login',
      name: 'admin-login',
      component: AdminLoginView,
    },
    {
      path: '/user/login',
      name: 'user-login',
      component: UserLoginView,
    },
    {
      path: '/user/register',
      name: 'user-register',
      component: UserRegisterView,
    },
=======
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue'),
    // },
>>>>>>> laura
  ],
})

export default router
