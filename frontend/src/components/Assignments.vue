<!-- src/components/Assigments.vue -->
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
  name: 'Assignments',
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

<style scoped src="../css/Assigments.css"></style>
