<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import { UserType } from "@/enums/UserType";
import router from "@/router";
import { useLoginStore } from "@/stores/LoginStore";
import { useUserStore } from "@/stores/UserStore";

const handleLogin = () => {
    router.push("/login")
}

const handleLogout = () => {
    const loginStore = useLoginStore()
    loginStore.logout()
    router.push("/login")
}

const userStore = useUserStore()
</script>

<template>
    <NavBar/>
    <div>Hello world</div>
    <div v-if="userStore.type === UserType.ADMIN">
        <p>You are an admin. Your name is {{ userStore.name }}. Your email address is {{ userStore.email }}.</p>
        <button @click="handleLogout">Logout</button>
    </div>
    <div v-if="userStore.type === UserType.GUEST">
        <p>You are a guest. We don't know your name or email address.</p>
        <button @click="handleLogin">Login</button>
    </div>
    <div>This is the dashboard.</div>
</template>