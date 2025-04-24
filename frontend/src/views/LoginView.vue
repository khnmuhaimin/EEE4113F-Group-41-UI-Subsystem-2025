<script setup lang="ts">
import { ref } from "vue"
import { useLoginStore } from "@/stores/LoginStore"
import { LoginStatus } from "@/enums/LoginStatus"
import router from "@/router"

const email = ref("")
const password = ref("")
const loginStore = useLoginStore()

const handleAdminLogin = async () => {
  await loginStore.login(email.value, password.value)
  if (loginStore.status === LoginStatus.LOGGED_IN) {
    router.push("/dashboard")
  }
}

const handleGuestLogin = async() => {
  await loginStore.logout()
  router.push("/dashboard")
}
</script>

<template>
  <div>
    <label for="email">Email:</label>
    <input id="email" v-model="email" type="text"/>
  </div>
  <div>
    <label for="password">Password:</label>
    <input id="password" v-model="password" type="password"/>
  </div>
  <div>
    <button @click="handleAdminLogin" :disabled="loginStore.inProgress()">Login as Admin</button>
    <button @click="handleGuestLogin" :disabled="loginStore.inProgress()">Continue As Guest</button>
  </div>
  <div v-if="loginStore.inProgress()">Loading</div>
  <div v-if="loginStore.errorOccured()">{{ loginStore.errorMessage }}</div>
</template>