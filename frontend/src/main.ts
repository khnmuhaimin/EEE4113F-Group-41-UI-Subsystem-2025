import App from "./App.vue"
import { createApp } from "vue"
import { createPinia } from "pinia"
import router from "./router"
import { useUserStore } from "./stores/UserStore"

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount("#app")

const userStore = useUserStore()
