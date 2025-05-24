import { loginAsAdmin, logoutAsAdmin } from "@/endpoints/loginEndpoints"

import { LoginStatus } from "@/enums/LoginStatus"
import { defineStore } from "pinia"
import { deleteCookie } from "@/utils/utils"
import { ref } from "vue"
import router from "@/router"
import { useUserStore } from "@/stores/UserStore"

export const useLoginStore = defineStore("login", () => {
    const status = ref(LoginStatus.LOGGED_OUT)
    const email = ref("")
    const password = ref("")
    const emailHelp = ref("")
    const passwordHelp = ref("")
    const loginMessage = ref("")
    const errorMessage = ref<string | null>(null)  // null means no error
    const emailError = ref<"" | "MISSING" | "INVALID" | "INCORRECT" | null>(null)
    const passwordError = ref<"" | "MISSING" | "INCORRECT" | null>(null)

    const validateEmail = () => {
        if (email.value === "") {
            emailError.value = "MISSING"
        } else if (!email.value.includes("@")) {
            emailError.value = "INVALID"
        } else {
            emailError.value = null
        }
        return emailError.value === null;
    }

    const validatePassword = () => {
        if (password.value === "") {
            passwordError.value = "MISSING"
        } else {
            passwordError.value = null
        }
        return passwordError.value === null;
    }

    /**
     * Attempts to log in a user as an admin.
     *
     * - Prevents login if a login or logout is already in progress.
     * - Sets login status to LOGGING_IN and resets any existing error message.
     * - Sends a POST request to the login endpoint with the provided credentials.
     * - On success (204), sets status to LOGGED_IN and updates the user store with admin details
     * - On known failure, restores the previous status and displays the server-provided message.
     * - On unknown failure, restores the previous status and sets a generic error message.
     *
     * @param email - The admin's email address.
     * @param password - The admin's password.
     */
    const login = async () => {
        if (status.value == LoginStatus.LOGGING_IN || status.value == LoginStatus.LOGGING_OUT) {
            return  // do nothing to not complicate the logic
        }

        validateEmail()
        validatePassword()
        if (emailError.value !== null || passwordError.value !== null) {
            return
        }
        // reset the login status
        const previousStatus = status.value
        status.value = LoginStatus.LOGGING_IN
        errorMessage.value = null
        try {
            const response = await loginAsAdmin(email.value, password.value)
            const response_body = await response.json()
            console.log(response_body)
            if (response.status == 200) {
                // if login was successful
                console.log("Logged in successfully.")
                status.value = LoginStatus.LOGGED_IN
                const userStore = useUserStore()
                userStore.setAdminDetails(response_body["name"], email.value)
            } else if (response.status == 401){
                // if login failed due to a known reason
                status.value = previousStatus
                errorMessage.value = response_body["message"]
                emailError.value = "INCORRECT"
                passwordError.value = "INCORRECT"
            } else {
                status.value = previousStatus
                errorMessage.value = response_body["message"]
            }
        } catch (error) {
            // if login failed due to an unknown reason
            console.log(error)
            status.value = previousStatus
            errorMessage.value = "Something went wrong"
        }
    }

    /**
    * Logs the user out, performing the necessary steps for both frontend and backend.
    *
    * This function follows these steps:
    * 1. **Prevents multiple simultaneous logout actions**: If the current status is either `LOGGING_IN` or `LOGGING_OUT`, the function exits early to avoid overlapping actions.
    * 2. **Logs the user out from the backend**: If the user is currently logged in (`LOGGED_IN`), it calls the `logoutAsAdmin()` function to log the user out on the server side.
    * 3. **Resets the user store**: Clears all user-related state by calling `userStore.$reset()`, ensuring no leftover data from the logged-in session.
    * 4. **Deletes the session cookie**: Removes the `session_id` cookie from the client's browser using `deleteCookie("session_id")`, effectively ending the session on the client side.
    * 
    * @returns {Promise<void>} A promise that resolves when the logout process is completed.
    */
    const logout = async (): Promise<void> => {
        if (status.value === LoginStatus.LOGGING_IN || status.value === LoginStatus.LOGGING_OUT) {
            return; // dont complicate logic
        }
        const previousStatus = status.value
        status.value = LoginStatus.LOGGING_OUT
        if (previousStatus === LoginStatus.LOGGED_IN) {
            await logoutAsAdmin()
        }
        // reset just in case
        const userStore = useUserStore()
        userStore.$reset()
        deleteCookie("session_id")
        status.value = LoginStatus.LOGGED_OUT
    }

    /**
     * Checks if no error message is currently set.
     * @returns `true` if no error has occurred, `false` otherwise.
     */
    const errorOccured = (): boolean => {
        return errorMessage.value !== null
    }

    /**
     * Checks if a login or logout operation is currently in progress.
     * @returns `true` if in progress, `false` otherwise.
     */
    const inProgress = (): boolean => {
        return status.value === LoginStatus.LOGGING_IN || status.value === LoginStatus.LOGGING_OUT
    }

    const $reset = () => {
        email.value = ""
        password.value = ""
        emailHelp.value = ""
        passwordHelp.value = ""
        loginMessage.value = ""
        errorMessage.value = null
        emailError.value = null
        passwordError .value = null
    }

    return { status, email, password, emailHelp, passwordHelp, loginMessage, errorMessage, emailError, passwordError, login, logout, errorOccured, inProgress, $reset }
})