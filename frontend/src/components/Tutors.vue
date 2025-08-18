<!-- src/components/Tutors.vue -->
<template>
  <div class="container">
    <Header/>
    <NavBar/>
    <ActionBar :kind="'tutors'"/>
    <div v-if="error" style="color: red;">Error: {{ error }}</div>
    <div v-else-if="loading">Cargando...</div>
    <div v-else class="tutors-layout">
      <section class="left-panel">
        <div class="card-list">
          <ScrollableCardList
            :items="tutors"
            :kind="'tutors'"
            itemKey="id"
          />
        </div>
      </section>
    </div>
  </div>

</template>

<script>
import apiUrl from '../config'
import Header from './generic/Header.vue'
import ActionBar from './generic/ActionBar.vue'
import NavBar from './generic/NavBar.vue'
import ScrollableCardList from './generic/ScrollableCardList.vue'
import axios from 'axios'

export default {
  name: 'Tutors',
  components: {
    Header,
    NavBar,
    ActionBar,
    ScrollableCardList
  },
  data () {
    return {
      loading: true,
      error: null,
      tutors: [],
      selectedTutor: null // TODO nothing yet
    }
  },
  mounted () {
    const path = `${apiUrl}/api/v1/tutors`
    axios.get(path)
      .then(response => {
        this.tutors = response.data.data.tutors
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

<style scoped src="../css/Tutors.css"></style>
