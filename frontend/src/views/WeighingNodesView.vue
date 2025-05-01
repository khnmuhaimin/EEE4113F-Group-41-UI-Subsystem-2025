<script setup lang="ts">
import BigMessage from "@/components/BigMessage.vue";
import NavBar from "@/components/NavBar.vue";
import { UserType } from "@/enums/UserType";
import router from "@/router";
import { useUserStore } from "@/stores/UserStore";
import { useWeighingNodesStore } from "@/stores/WeighingNodesStore";
import { onMounted } from "vue";

const userStore = useUserStore()
const weighingNodesStore = useWeighingNodesStore()

// onMounted(() => {
//   if (userStore.type === UserType.GUEST) {
//     router.push("/login")
//   }
// })
</script>

<template>
    <div class="minsize-fullscreen vertical-stack">
        <NavBar/>
        <BigMessage v-if="weighingNodesStore.size() === 0" message="You have no weighing nodes yet." style="flex: 1"/>
        <div class="card mb-3" v-for="node in weighingNodesStore.weighingNodes" :key="node.id">
        <div class="card-body">
            <h5 class="card-title">Location: {{ node.location || 'Unknown' }}</h5>
            <p class="card-text">
            Registration in progress:
            <span :class="{'text-success': node.registration_in_progress, 'text-danger': !node.registration_in_progress}">
                {{ node.registration_in_progress ? '✅' : '❌' }}
            </span>
            </p>
            <p class="card-text">
            LEDs flashing:
            <span :class="{'text-success': node.leds_flashing, 'text-danger': !node.leds_flashing}">
                {{ node.leds_flashing ? '✅' : '❌' }}
            </span>
            </p>
            <p class="card-text">
            Created at: {{ new Date(node.created_at).toLocaleDateString() }}
            </p>
        </div>
        </div>
    </div>
</template>


<style lang="scss">

@import "./../scss/layout.scss";

</style>