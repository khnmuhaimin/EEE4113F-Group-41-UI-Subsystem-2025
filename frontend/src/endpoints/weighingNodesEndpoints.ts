import { API_BASE_URL } from "@/endpoints/utils";

export const getWeighingNodes = async (): Promise<Response> => {

    const response = await fetch(`${API_BASE_URL}/weighing-nodes/all`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    });

    return response;
}


export const flashLEDs = async (node_id: string, flash: boolean): Promise<Response> => {
    const response = await fetch(`${API_BASE_URL}/weighing-nodes/flash-leds`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            weighing_node_id: node_id,
            flash_leds: flash
        })
    });

    return response;
};
