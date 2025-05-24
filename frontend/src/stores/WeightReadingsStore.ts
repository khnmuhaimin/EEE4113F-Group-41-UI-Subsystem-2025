import type { WeightReading } from "@/types/WeightReading"
import { defineStore } from "pinia";
import { fetchWeightReadings } from "@/endpoints/dashboardEndpoints";
import { ref } from "vue";

export const useWeightReadingsStore = defineStore("weightReadings", () => {
    const fetchStatus = ref<"NOT_FETCHED" | "FETCHED" | "FETCHING">("NOT_FETCHED")
    const weightReadings = ref<WeightReading[]>([])

    const fetch = async () => {
        fetchStatus.value = "FETCHING"
        const response = await fetchWeightReadings()
        if (response.status === 401) {
            fetchStatus.value = "NOT_FETCHED"
        } else if (response.status === 200) {
            fetchStatus.value = "FETCHED"
            weightReadings.value = await response.json() as WeightReading[]
        }
    }

    const numReadings = () => weightReadings.value.length

    return { fetchStatus, weightReadings, fetch, numReadings }
})
