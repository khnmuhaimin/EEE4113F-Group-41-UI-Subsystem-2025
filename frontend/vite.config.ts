import { URL, fileURLToPath } from "node:url"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import vueDevTools from "vite-plugin-vue-devtools"
import vueJsx from "@vitejs/plugin-vue-jsx"

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url))
    },
  },
  server: {
    allowedHosts: [
      'eee4113f-group-41.online', // Add the allowed host here
    ],
  }
})
