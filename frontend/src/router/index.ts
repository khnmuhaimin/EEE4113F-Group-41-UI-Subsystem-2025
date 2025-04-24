import { createRouter, createWebHistory } from "vue-router"

import DashboardView from "@/views/DashboardView.vue"
import LoginView from "@/views/LoginView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", redirect: "/dashboard" },
    { path: "/login", component: LoginView },
    { path: "/dashboard", component: DashboardView }
  ],
})

export default router
