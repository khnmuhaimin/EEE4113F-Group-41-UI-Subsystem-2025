import { API_BASE_URL } from "@/endpoints/utils";

/**
 * Logs in the admin using email and password.
 * Sends a POST request to the server with the email and password to authenticate the admin.
 * 
 * @param {string} email - The admin's email address.
 * @param {string} password - The admin's password.
 * @returns {Promise<Response>} The response object from the server.
 */
export const loginAsAdmin = async (email: string, password: string): Promise<Response> => {
    const response = await fetch(`${API_BASE_URL}/admins/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
    });

    return response;
}


/**
 * Logs out the admin by sending a POST request to the server's logout endpoint.
 * Includes cookies to ensure the session is properly terminated.
 * 
 * @returns {Promise<Response>} The response object from the server.
 */
export const logoutAsAdmin = async (): Promise<Response> => {
    const response = await fetch(`${API_BASE_URL}/admins/logout`, {
        method: "POST",
        credentials: "include"  // ensures cookies are sent
    });

    return response;
}