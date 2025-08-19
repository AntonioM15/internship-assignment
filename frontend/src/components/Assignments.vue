<!-- src/components/Assigments.vue -->
<template>
  <div class="container">
    <Header/>
    <NavBar/>
    <AssignmentsActionBar :kind="'assignments'"/>
    <div v-if="error" style="color: red;">Error: {{ error }}</div>
    <div v-else-if="loading">Cargando...</div>
    <div v-else class="assignments-layout">
      <div class="card-list">
          <ScrollableCardList
            :items="assignments"
            :kind="'assignments'"
            v-model="selectedAssignment"
            itemKey="id"
          />
        </div>
    </div>
  </div>

</template>

<script>
import apiUrl from '../config'
import Header from './generic/Header.vue'
import NavBar from './generic/NavBar.vue'
import AssignmentsActionBar from './generic/AssignmentsActionBar.vue'
import axios from 'axios'
import ScrollableCardList from './generic/ScrollableCardList.vue'

export default {
  name: 'Assignments',
  components: {
    Header,
    NavBar,
    AssignmentsActionBar,
    ScrollableCardList
  },
  data () {
    return {
      loading: true,
      error: null,
      assignments: [],
      selectedAssignment: null
    }
  },
  mounted () {
    const path = `${apiUrl}/api/v1/assignments`
    axios.get(path)
      .then(response => {
        this.assignments = response.data.data.internships
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

<style scoped src="../css/Assigments.css"></style>
