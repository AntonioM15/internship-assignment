<!-- src/components/Students.vue -->
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
  name: 'Students',
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

<style scoped src="../css/Students.css"></style>
