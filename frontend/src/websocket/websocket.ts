import { useWeighingNodesStore } from "@/stores/WeighingNodesStore";
import { useWeightReadingsStore } from "@/stores/WeightReadingsStore";

export const subscribeToNotifications = () => {
    const WEBSOCKET_BASE_URL = `wss://${import.meta.env.VITE_DOMAIN}/ws`;
    const ws = new WebSocket(WEBSOCKET_BASE_URL);

    ws.onerror = (err) => {
        console.error("WebSocket error:", err);
    };

    ws.onopen = () => {
        console.log("Connected to websocket server");
    };

    ws.onmessage = (event) => {
        console.log("received:", event.data);
        if (event.data === "FETCH_WEIGHING_NODES") {
            useWeighingNodesStore().fetch()
        } else if (event.data === "FETCH_WEIGHT_READINGS") {
            useWeightReadingsStore().fetch()
        }
    };
};
