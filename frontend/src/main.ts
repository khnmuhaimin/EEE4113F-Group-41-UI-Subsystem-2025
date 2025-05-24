import './scss/styles.scss'

import App from './App.vue'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'

// import * as bootstrap from 'bootstrap'


const app = createApp(App)

app.use(createPinia())
app.use(router)
console.log("mounting")

app.mount('#app')