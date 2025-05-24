import { API_BASE_URL } from "@/endpoints/utils";

export const getWeighingNodes = async (): Promise<Response> => {

    const response = await fetch(`${API_BASE_URL}/weighing-nodes`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    });

    return response;
}