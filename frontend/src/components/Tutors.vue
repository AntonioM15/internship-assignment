<!-- src/components/Tutors.vue -->
<template>
  <div class="container">
    <Header/>
    <NavBar/>
    <ActionBar
      :kind="'tutors'"
      :degrees="degrees"
      @course-changed="onCourseChanged"
      @nameText-changed="onNameTextChanged"
      @status-changed="onStatusChanged"
    />
    <div v-if="error" style="padding: 22px; color: red; font-size: 15px; font-weight: bold;">Error: {{ error }}</div>
    <div v-else class="tutors-layout">
      <section class="left-panel">
        <div class="card-list">
          <ScrollableCardList
            :items="tutors"
            :kind="'tutors'"
            v-model="selectedTutor"
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
import NavBar from './generic/NavBar.vue'
import ActionBar from './generic/ActionBar.vue'
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
      degrees: [],
      tutors: [],
      selectedTutor: null,
      // ActionBar filters
      course: '',
      nameText: '',
      selectedStatus: 'unknown'
    }
  },
  mounted () {
    this.fetchTutors()
  },
  methods: {
    fetchTutors () {
      this.loading = true
      this.error = null
      const path = `${apiUrl}/api/v1/tutors`
      const params = {
        ...(this.course && { degree_id: this.course }),
        ...(this.nameText && { full_name: this.nameText }),
        ...((this.selectedStatus && this.selectedStatus !== 'unknown') && { status: this.selectedStatus })
      }

      axios.get(path, { params })
        .then(response => {
          this.degrees = response.data.data.degrees
          this.tutors = response.data.data.tutors
          // Restore tutor selection if included
          if (this.selectedTutor) {
            const found = this.tutors.find(s => s.official_id === this.tutors.official_id)
            this.selectedTutor = found || null
          }
        })
        .catch(err => {
          this.error = err.response.data.message || err.message
        })
        .finally(() => {
          this.loading = false
        })
    },
    // Filter handlers
    onCourseChanged (val) {
      this.course = val._id
      this.fetchTutors()
    },
    onNameTextChanged (val) {
      this.nameText = val
      this.fetchTutors()
    },
    onStatusChanged (val) {
      this.selectedStatus = val
      this.fetchTutors()
    }
  }
}

</script>

<style scoped src="../css/Tutors.css"></style>
