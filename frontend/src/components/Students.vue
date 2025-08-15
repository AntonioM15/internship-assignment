<!-- src/components/Students.vue -->
<template>
  <div class="container">
    <Header/>
    <NavBar/>
    <ActionBar/>
    <div v-if="error" style="color: red;">Error: {{ error }}</div>
    <div v-else-if="loading">Cargando...</div>
    <div v-else class="students-layout">
      <section class="left-panel">
        <div class="card-list">
          <ScrollableCardList :items="students" :kind="'students'" />
        </div>
      </section>
      <section class="right-panel">
      </section>
    </div>
  </div>

</template>

<script>
import apiUrl from '../config'
import Header from './generic/Header.vue'
import NavBar from './generic/NavBar.vue'
import ScrollableCardList from './generic/ScrollableCardList.vue'
import ActionBar from './generic/ActionBar.vue'
import axios from 'axios'

export default {
  name: 'Students',
  components: {
    Header,
    NavBar,
    ScrollableCardList,
    ActionBar
  },
  data () {
    return {
      loading: true,
      error: null,
      students: []
    }
  },
  mounted () {
    const path = `${apiUrl}/api/v1/students`
    axios.get(path)
      .then(response => {
        this.students = response.data.data.students
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

<style scoped src="../css/Students.css"></style>
