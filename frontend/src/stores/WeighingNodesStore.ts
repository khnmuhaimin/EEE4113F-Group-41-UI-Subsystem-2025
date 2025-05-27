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
                weighingNodes.value.sort((a, b) => {
                    // Prioritize registration_in_progress
                    if (a.registration_in_progress !== b.registration_in_progress) {
                        if (a.registration_in_progress && !b.registration_in_progress) {
                            return -1;
                        } else {
                            return 1;
                        }
                    }

                    // If both are false, sort by location
                    if (!a.registration_in_progress && !b.registration_in_progress) {
                        if (a.location && b.location) {
                            return a.location.localeCompare(b.location);
                        }
                        if (a.location) return -1;
                        if (b.location) return 1;
                        return 0;
                    }

                    return 0;
                });
            }
        }
    }

    const numNodes = () => weighingNodes.value.length

    const numAliveNodes = () =>
    weighingNodes.value.filter(
        node => (Date.now() - Date.parse(node.last_pinged_at)) < 300_000
    ).length;


    const reset = () => {
        weighingNodes.value = []
        fetchStatus.value = "NOT_FETCHED"
    }

    return { fetchStatus, weighingNodes, fetch, numNodes, numAliveNodes, reset}
})