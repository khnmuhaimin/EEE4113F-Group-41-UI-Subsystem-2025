import { createRouter, createWebHistory } from 'vue-router'

import DashboardView from '@/views/DashboardView.vue'
import LoginView from '@/views/LoginView.vue'
import WeighingNodesView from '@/views/WeighingNodesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/weighing-nodes',
      name: 'weighing-nodes',
      component: WeighingNodesView
    }
  ],
})

export default router
