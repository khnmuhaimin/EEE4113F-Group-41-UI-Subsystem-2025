import { API_BASE_URL } from "@/endpoints/utils";

/**
 * Fetches raw weight reading response from the server.
 * JSON parsing is deferred to the caller.
 * 
 * @returns {Promise<Response>} Raw response object from the server.
 */
export const fetchWeightReadings = async (): Promise<Response> => {
    const response = await fetch(`${API_BASE_URL}/dashboard/weight-readings`);
    if (!response.ok) {
        throw new Error("Failed to fetch weight readings.");
    }
    return response;
};
