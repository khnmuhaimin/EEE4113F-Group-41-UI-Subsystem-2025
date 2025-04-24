import { UserType } from "@/enums/UserType";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useUserStore = defineStore("userStore", () => {
    const type = ref(UserType.GUEST)
    const name = ref<null | string>(null)
    const email = ref<null | string>(null)

    const setAdminDetails = (name: string, email: string) => {
        const userStore = useUserStore()
        userStore.type = UserType.ADMIN
        userStore.name = name
        userStore.email = email
    }

    const $reset = () => {
        type.value = UserType.GUEST
        name.value = null
        email.value = null
    }
    
    return { type, name, email, setAdminDetails, $reset}
})