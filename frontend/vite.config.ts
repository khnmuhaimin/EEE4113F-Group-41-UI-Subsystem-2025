import { URL, fileURLToPath } from 'node:url'

import { defineConfig } from 'vite'
import path from 'node:path'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vite.dev/config/

let allowedHosts: [string]
if (typeof process.env.DOMAIN === 'string') {
  allowedHosts = [process.env.DOMAIN]
} else {
  allowedHosts = [] as unknown as [string]
}

export default defineConfig({
  server: {
    allowedHosts
  },
  plugins: [
    vue(),
    vueJsx(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '~bootstrap': path.resolve(__dirname, 'node_modules/bootstrap'),
    },
  },
})
