<script setup lang="ts">
import { ref } from 'vue';
import { loginAsAdmin } from './../utils/api/loginApi'

const email = ref("")
const password = ref("")
const loginMessage = ref("");
const attemptedLogin = false;

const handleLogin = async () => {
  // const response = await loginAsAdmin(email.value, password.value);
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
    <button @click="handleLogin">Login as Admin</button>
    <button @click="handleLogin">Login as Guest</button>
  </div>
  <div>{{ `Email: ${email} Password: ${password}` }}</div>
  <div v-if="attemptedLogin">{{ loginMessage }}</div>
</template>