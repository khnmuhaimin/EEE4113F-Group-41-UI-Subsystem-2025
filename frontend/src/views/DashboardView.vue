<script setup lang="ts">
import DashboardCard from "@/components/DashboardCard.vue";
import WeightScatterChart from "@/components/WeightScatterChart.vue";
import NavBar from "@/components/NavBar.vue";
import { UserType } from "@/enums/UserType";
import router from "@/router";
import { useLoginStore } from "@/stores/LoginStore";
import { useUserStore } from "@/stores/UserStore";
import { useWeightReadingsStore } from "@/stores/WeightReadingsStore";
import { onMounted } from "vue";
import { useWeighingNodesStore } from "@/stores/WeighingNodesStore";


const userStore = useUserStore()
const weightReadingsStore = useWeightReadingsStore();
const weighingNodesStore = useWeighingNodesStore();

const handleLogin = () => {
    router.push("/login")
}

const handleLogout = () => {
    const loginStore = useLoginStore()
    loginStore.logout()
    router.push("/login")
}

onMounted(async () => {
    await weightReadingsStore.fetch();
    await weighingNodesStore.fetch();
});

</script>

<template>
    <NavBar/>
    <div>Hello world</div>
    <div v-if="userStore.type === UserType.ADMIN">
        <p>You are an admin. Your name is {{ userStore.name }}. Your email address is {{ userStore.email }}.</p>
        <button @click="handleLogout">Logout</button>
    </div>
    <div v-if="userStore.type === UserType.GUEST">
        <p>You are a guest. We don't know your name or email address.</p>
        <button @click="handleLogin">Login</button>
    </div>
    <div>This is the dashboard.</div>
    <div>
        <DashboardCard>
            <h5>Total Readings</h5>
            <p>{{ weightReadingsStore.numReadings() }}</p>
        </DashboardCard>
        <DashboardCard>
            <h5>Weight Readings</h5>
            <WeightScatterChart :readings="weightReadingsStore.weightReadings" />
        </DashboardCard>
        <DashboardCard>
            <h5>Total Weighing Nodes</h5>
            <p>{{ weighingNodesStore.numNodes() }}</p>
        </DashboardCard>
    </div>
</template>