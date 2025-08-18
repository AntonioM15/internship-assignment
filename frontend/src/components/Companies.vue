<!-- src/components/Companies.vue -->
<template>
  <div class="container">
    <Header/>
    <NavBar/>
    <ActionBar :kind="'companies'"/>
    <div v-if="error" style="color: red;">Error: {{ error }}</div>
    <div v-else-if="loading">Cargando...</div>
    <ul v-else>
      <li v-for="(item, index) in data" :key="index">{{ item }}</li>
    </ul>
  </div>

</template>

<script>
import apiUrl from '../config'
import Header from './generic/Header.vue'
import NavBar from './generic/NavBar.vue'
import ActionBar from './generic/ActionBar.vue'
import axios from 'axios'

export default {
  name: 'Companies',
  components: {
    Header,
    NavBar,
    ActionBar
  },
  data () {
    return {
      loading: true,
      error: null
    }
  },
  mounted () {
    const path = `${apiUrl}/api/v1/companies`
    axios.get(path)
      .then(response => {
        this.data = response.data.data
      })
      .catch(err => {
        this.error = err.response.data.message || err.message
      })
      .finally(() => {
        this.loading = false
      })
  },
  methods: {
  }
}

</script>

<style scoped src="../css/Companies.css"></style>
