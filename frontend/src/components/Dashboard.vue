<!-- src/components/Dashboard.vue -->
<template>
  <div class="container">
    <Header/>
    <NavBar/>
  </div>

</template>

<script>
import Header from './generic/Header.vue'
import NavBar from './generic/NavBar.vue'

export default {
  name: 'Dashboard',
  components: {
    Header,
    NavBar
  },
  data () {
    return {
    }
  },
  methods: {
  }
}

</script>

<style scoped src="../css/Dashboard.css"></style>
