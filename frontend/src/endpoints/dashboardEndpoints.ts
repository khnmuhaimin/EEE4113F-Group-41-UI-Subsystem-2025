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


/**
 * Downloads the CSV data file from the server.
 * Returns the raw Response for the caller to handle (e.g., save file).
 * 
 * @returns {Promise<Response>} Raw response object containing the CSV file.
 */
export const downloadWeightData = (): void => {
    window.location.href = `${API_BASE_URL}/dashboard/weight-readings/csv`;
};

