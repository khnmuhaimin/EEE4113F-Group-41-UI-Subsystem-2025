<template>
  <canvas ref="chartCanvas"></canvas>
</template>

<script setup lang="ts">
    import { ref, onMounted, watch } from "vue";
    import Chart from "chart.js/auto";
    import "chartjs-adapter-date-fns";
    import type { WeightReading } from "@/types/WeightReading";
    import 'chartjs-plugin-trendline';

    const props = defineProps<{
        readings: WeightReading[];
    }>();

    const chartCanvas = ref<HTMLCanvasElement | null>(null);
    let chartInstance: any | null = null;

    const createChart = () => {
        if (!chartCanvas.value) return;

        const dataPoints = props.readings.map((r) => ({
            x: new Date(r.created_at * 1000), // assuming seconds timestamp
            y: r.weight,
        }));

        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(chartCanvas.value, {
            type: "scatter",
            data: {
                datasets: [
                    {
                        label: "Penguin Weight over Time",
                        data: dataPoints,
                        backgroundColor: "rgba(54, 162, 235, 0.7)"
                    }
                ],
            },
            options: {
                scales: {
                    x: {
                        type: "time",
                        time: {
                            tooltipFormat: "MMM dd yyyy, HH:mm",
                            unit: "day",
                        },
                        title: {
                            display: true,
                            text: "Time",
                        },
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Weight (g)",
                        },
                        beginAtZero: true,
                    },
                },
            },
        });
    };

    onMounted(() => {
        console.log("creating chart")
    // createChart();
    });

    watch(
        () => props.readings,
        () => {
            createChart();
        }
    );
</script>

<style scoped>
canvas {
  width: 100%;
  max-height: 300px;
}
</style>