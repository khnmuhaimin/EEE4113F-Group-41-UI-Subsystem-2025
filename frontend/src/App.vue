<script setup lang="ts">
import { RouterView } from 'vue-router'
import { subscribeToNotifications } from './websocket/websocket'

subscribeToNotifications()
</script>

<template>
  <RouterView />
</template>
