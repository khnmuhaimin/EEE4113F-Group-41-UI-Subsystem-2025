<script setup lang="ts">
import { UserType } from '@/enums/UserType';
import router from '@/router';
import { useLoginStore } from '@/stores/LoginStore';
import { useUserStore } from '@/stores/UserStore';

const loginStore = useLoginStore()
const userStore = useUserStore()

const login = () => {
    router.push("/login")
}

const logout = async () => {
    await loginStore.logout()
    router.push("/login")
}

const viewWeighingNodes = () => {
    router.push("/weighing-nodes")
    return;
}

const viewWeighingNodesActive = () => {
    console.log(router.currentRoute.value.path)
    return router.currentRoute.value.path === "/weighing-nodes"
}

const viewDashboard = () => {
    router.push("/dashboard")
    return
}

const dashboardActive = () => {
    return router.currentRoute.value.path === "/dashboard"
}
</script>

<template>
    <nav id="navbar" class="navbar navbar-expand-lg">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <img id="penguin-image" src="/penguin.png" alt="logo">
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#menu-container" aria-controls="menu-container" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="menu-container">
                <ul id="menu-options" class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li v-if="userStore.type === UserType.ADMIN" class="nav-item">
                        <button v-if="userStore.type === UserType.ADMIN" class="nav-link btn">Download Data</button>
                    </li>
                    <li class="nav-item">
                        <button class="nav-link btn" :onclick="viewDashboard" :disabled="dashboardActive()">Dashboard</button>
                    </li>
                    <li v-if="userStore.type === UserType.ADMIN" class="nav-item">
                        <button v-if="userStore.type === UserType.ADMIN" class="nav-link btn" :onclick="viewWeighingNodes" :disabled="viewWeighingNodesActive()">Weighing Nodes</button>
                    </li>
                    <li v-if="userStore.type === UserType.GUEST" class="nav-item">
                        <button class="nav-link btn" :onclick="login">Login</button>
                    </li>
                    <li v-if="userStore.type === UserType.ADMIN" class="nav-item">
                        <button class="nav-link btn" :onclick="logout">Logout</button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<style scoped lang="scss">

@import "./../scss/layout.scss";

#navbar {
    background-color: #c7d6e5;
    padding-left: 5%;
    padding-right: 5%;
    padding-top: 1%;
    padding-bottom: 1%;
}

#penguin-image {
    width: 50px;
    height: 50px;
    margin-bottom: 5px;
}

@media (min-width: 992px) {
    
}
</style>
