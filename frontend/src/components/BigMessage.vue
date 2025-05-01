<script setup lang="ts">
import { onMounted, ref } from 'vue';

const props = defineProps(['message'])
const message = ref("")

onMounted(() => {
    message.value = props.message
})
</script>

<template>
    <div id="message-container">
        <div id="message">
            {{ message }}
        </div>
    </div>
</template>

<style scoped lang="scss">

@import "./../scss/layout.scss";

#message-container {
    text-align: center;
    justify-content: center;
    align-items: center;
    display: flex;
}

#message {
    justify-content: space-around;
}

</style>