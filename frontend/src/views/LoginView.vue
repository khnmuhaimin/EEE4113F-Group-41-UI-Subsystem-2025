<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useLoginStore } from "@/stores/LoginStore"
import { LoginStatus } from "@/enums/LoginStatus"
import router from "@/router"

const loginStore = useLoginStore()

const handleAdminLogin = async () => {

  await loginStore.login()
  if (loginStore.status === LoginStatus.LOGGED_IN) {
    router.push("/dashboard")
  }

  if (loginStore.emailError === "MISSING") {
    loginStore.emailHelp = "Enter the email address."
  } else if (loginStore.emailError === "INVALID") {
    loginStore.emailHelp = "The email address is not valid."
  } else if (loginStore.emailError === "INCORRECT" || loginStore.emailError === null) {
    loginStore.emailHelp = ""
  }

  if (loginStore.passwordError === "MISSING") {
    loginStore.passwordHelp = "Enter the password."
  } else if (loginStore.passwordError === "INCORRECT" || loginStore.passwordError === null) {
    loginStore.passwordHelp = ""
  }

  if (loginStore.emailError === "INCORRECT" || loginStore.passwordError === "INCORRECT") {
    loginStore.loginMessage = "Are you sure your login details are correct?"
  }
}

const handleGuestLogin = async() => {
  await loginStore.logout()
  router.push("/dashboard")
}

onMounted(() => {
  loginStore.$reset()
})
</script>

<template>
  <div class="fullscreen stackable-container">
    <div id="image-container" class="center-children">
      <!-- <a href="https://www.flaticon.com/free-icons/penguin" title="penguin icons">Penguin icons created by Freepik - Flaticon</a> -->
      <img id="penguin-image" src="/penguin.png" alt="logo" class="img-fluid my-5">
    </div>
    <div id="form-container" class="vertical-stack center-children my-3">
      <div id="email-container" class="vertical-stack center-children horizontal-fill my-3">
        <label id="email-label" for="email" class="form-label">Email:</label>
        <input id="email" v-model="loginStore.email" type="text" class="form-control" :class="{ 'is-invalid': loginStore.emailError !== null }"/>
        <div id="email-help" class="form-text">{{ loginStore.emailHelp }}</div>
      </div>
      <div id="password-container" class="vertical-stack center-children horizontal-fill my-3">
        <label id="password-label" for="password" class="form-label">Password:</label>
        <input id="password" v-model="loginStore.password" type="password" class="form-control" :class="{ 'is-invalid': loginStore.passwordError !== null }"/>
        <div id="password-help" class="form-text">{{ loginStore.passwordHelp }}</div>
      </div>
      <div class="vertical-stack horizontal-fill center-children my-3">
        <button id="admin-login-button" class="btn my-2" @click="handleAdminLogin" :disabled="loginStore.inProgress()">Login as Admin</button>
        <button id="guest-login-button" class="btn my-2" @click="handleGuestLogin" :disabled="loginStore.inProgress()">Continue As Guest</button>
      </div>
      <div id="login-message">{{ loginStore.loginMessage }}</div>
    </div>
  </div>
</template>


<style scoped lang="scss">

@import "./../scss/layout.scss";

.stackable-container {
  display: flex;
  flex-direction: column; /* Stack vertically by default */
}

@media (min-width: 992px) {
  .stackable-container {
    flex-direction: row; /* Stack horizontally on large screens */
    justify-content: space-evenly;
  }
}

#form-container {
  width: 100%;
}

#image-container {
  width: 100%;
  background-color: #c7d6e5;
}

@media (min-width: 992px) {
  #image-container {
    width: 40%;
  }
  #form-container {
    width: 60%;
  }
}

#email-label, #email, #email-help, #password-label, #password, #password-help, #admin-login-button, #guest-login-button {
  width: 75%;
}

@media (min-width: 992px) {
  #email-label, #email, #email-help, #password-label, #password, #password-help, #admin-login-button, #guest-login-button {
    width: 50%;
  }
}

#email-help, #password-help, #login-message {
  min-height: 1.5rem;
}


#penguin-image {
  width: 25%
}

@media (min-width: 992px) {
  #penguin-image {
    width: 50%
  }
}

#admin-login-button {
  background-color: #5d5d84;
  color: white;
}

#guest-login-button {
  background-color: white;
  border-color: #5d5d84;
}

</style>
