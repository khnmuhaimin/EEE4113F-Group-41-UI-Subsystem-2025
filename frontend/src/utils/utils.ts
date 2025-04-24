/**
 * Retrieves the value of a specified cookie by name.
 * 
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string | null} The value of the cookie if found, or null if the cookie does not exist.
 */
export const getCookie = (name: string): string | null => {
    const cookies = document.cookie.split(";")
    for (const cookie of cookies) {
        const [key, value] = cookie.trim().split("=")
        if (key === name) {
            return decodeURIComponent(value)
        }
    }
    return null
}


/**
 * Deletes a specified cookie by setting its expiration date to a past date.
 * 
 * @param {string} cookieName - The name of the cookie to delete.
 */
export const deleteCookie = (cookieName: string) => {
    document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}