import type { WeighingNode } from "@/types/WeighingNode"
import { defineStore } from "pinia";
import { getWeighingNodes } from "@/endpoints/weighingNodesEndpoints";
import { ref } from "vue";

export const useWeighingNodesStore = defineStore("weighingNodes", () => {
    const fetchStatus = ref<"NOT_FETCHED" | "FETCHED" | "FIRST_FETCH" | "NON_FIRST_FETCH">("NOT_FETCHED")
    const weighingNodes = ref<WeighingNode[]>([])

    const fetch = async () => {
        if (fetchStatus.value === "NOT_FETCHED") {
            fetchStatus.value = "FIRST_FETCH"
            const response = await getWeighingNodes()
            if (response.status === 401) {
                fetchStatus.value = "NOT_FETCHED"
            } else if (response.status === 200) {
                fetchStatus.value = "FETCHED"
                weighingNodes.value = await response.json() as WeighingNode[]
            }
        }   
    }

    const numNodes = () => weighingNodes.value.length

    return { fetchStatus, weighingNodes, fetch, numNodes }
})