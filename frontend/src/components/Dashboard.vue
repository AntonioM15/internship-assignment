<!-- src/components/Dashboard.vue -->
<template>
  <div class="container">
    <Header/>
    <NavBar/>
    <div v-if="error" style="padding: 22px; color: red; font-size: 15px; font-weight: bold;">Error: {{ error }}</div>
    <div v-else class="dashboard-layout">
      <section class="left-panel">
        <h2>Empresas</h2>
        <div class="card-list">
          <ScrollableCardList :items="notifications.worker" :kind="'notifications'" />
        </div>
      </section>
      <section class="right-panel">
        <div class="half-panel">
          <h2>Estudiantes</h2>
          <div class="card-list">
            <ScrollableCardList :items="notifications.student" :kind="'notifications'" />
          </div>
        </div>
        <div class="half-panel">
          <h2>Profesores</h2>
          <div class="card-list">
            <ScrollableCardList :items="notifications.tutor" :kind="'notifications'" />
          </div>
        </div>
      </section>
    </div>
  </div>

</template>

<script>
import apiUrl from '../config'
import Header from './generic/Header.vue'
import NavBar from './generic/NavBar.vue'
import ScrollableCardList from './generic/ScrollableCardList.vue'
import axios from 'axios'

export default {
  name: 'Dashboard',
  components: {
    Header,
    NavBar,
    ScrollableCardList
  },
  data () {
    return {
      loading: true,
      error: null,
      notifications: {}
    }
  },
  mounted () {
    const path = `${apiUrl}/api/v1/dashboard/notifications`
    axios.get(path)
      .then(response => {
        this.notifications = response.data.data
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

<style scoped src="../css/Dashboard.css"></style>
