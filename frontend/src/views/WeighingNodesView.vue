<script setup lang="ts">
import BigMessage from "@/components/BigMessage.vue";
import NavBar from "@/components/NavBar.vue";
import { UserType } from "@/enums/UserType";
import router from "@/router";
import { useLoginStore } from "@/stores/LoginStore";
import { useUserStore } from "@/stores/UserStore";
import { useWeighingNodesStore } from "@/stores/WeighingNodesStore";
import { computed, onMounted, ref } from "vue";

const userStore = useUserStore()
const weighingNodesStore = useWeighingNodesStore()
const loginStore = useLoginStore()
const bigMessage = ref("")


const now = ref(Date.now());
setInterval(() => now.value = Date.now(), 1000);

const getLastPingText = (timestamp: string, _now = now.value) => {
  const diff = (_now - new Date(timestamp).getTime()) / 1000;
  if (diff < 60) return `${Math.floor(diff)} seconds ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`;
  return new Date(timestamp).toLocaleDateString();
}

onMounted( async () => {
    // if (userStore.type === UserType.GUEST) {
    //     router.push("/login")
    // }
    bigMessage.value = "Loading..."
    loginStore.email = "admin@org.com"
    loginStore.password = "admin"
    await loginStore.login()
    weighingNodesStore.fetch()
    if (userStore.type === UserType.GUEST) {
        bigMessage.value = "You need to be logged in to view this resource."
    } else if (weighingNodesStore.numNodes() === 0) {
        bigMessage.value = "You don't have any weighing nodes pending registration of deployed."
    } else {
        bigMessage.value = ""
    }
    console.log("Big message: " + bigMessage.value)
})
</script>

<template>
    <div class="minsize-fullscreen vertical-stack">
        <NavBar/>
        <BigMessage v-if="weighingNodesStore.numNodes() === 0" :message="bigMessage" style="flex: 1"/>
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
                Last Ping: {{ getLastPingText(node.last_pinged_at) }}
            </p>
            <p class="card-text">
            Created at: {{ new Date(node.created_at).toLocaleDateString() }}
            </p>
            <button v-if="node.registration_in_progress" class="btn btn-primary mt-2">
                Approve Registration
            </button>
            <p v-if="node.registration_in_progress">Flash the LEDs to see which node is waiting to be registered. When you click the button, wait a few seconds. The node might take a few seconds to starts flashing its LEDs.</p>
            <button v-if="node.registration_in_progress" class="btn btn-primary mt-2">
                Flash LEDs
            </button>
        </div>
        </div>
    </div>
</template>


<style lang="scss">

@import "./../scss/layout.scss";

</style>