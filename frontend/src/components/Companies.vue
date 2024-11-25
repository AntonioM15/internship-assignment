<!-- src/components/Companies.vue -->
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
  name: 'Companies',
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

<style scoped src="../css/Companies.css"></style>
