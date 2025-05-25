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
  <NavBar />
  <div class="dashboard-container">
    <div class="summary-cards">
      <DashboardCard>
        <h5>Weights Collected</h5>
        <p>Number of weight recordings collected.</p>
        <p>{{ weightReadingsStore.numReadings() }}</p>
      </DashboardCard>
      <DashboardCard>
        <h5>Total Weighing Nodes</h5>
        <p>Weighing nodes registered</p>
        <p>{{ weighingNodesStore.numNodes() }}</p>
      </DashboardCard>
      <DashboardCard>
        <h5>Weighing Nodes Online</h5>
        <p>Weighing nodes registered and alive.</p>
        <p>{{ weighingNodesStore.numNodes() }}</p>
      </DashboardCard>
    </div>

    <div class="chart-card">
      <DashboardCard>
        <h5>Weight Readings</h5>
        <WeightScatterChart :readings="weightReadingsStore.weightReadings" />
      </DashboardCard>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  margin: 0 auto;
  width: 90%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.summary-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem; /* adds space above the summary cards */
}

.chart-card {
  margin-top: 0.5rem;
}

.download-button {
  align-self: flex-start;
  margin-top: 0.5rem;
  margin-bottom: 2rem; /* adds space below the button */
}

@media (min-width: 768px) {
  .dashboard-container {
    width: 75%;
  }

  .summary-cards {
    flex-direction: row;
  }
}
</style>
