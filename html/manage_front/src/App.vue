<script setup>
import HelloWorld from './components/HelloWorld.vue'

</script>

<template>
    <router-view></router-view>
</template>



<script>
export default {
    data() {
        return {
            title: document.title
        }
    }
}
</script>

<style>
</style>
