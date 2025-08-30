<!-- src/components/Students.vue -->
<template>
  <div class="container">
    <Header/>
    <NavBar/>
    <ActionBar
      :kind="'students'"
      :degrees="degrees"
      @course-changed="onCourseChanged"
      @nameText-changed="onNameTextChanged"
      @status-changed="onStatusChanged"
    />
    <div v-if="error" style="color: red;">Error: {{ error }}</div>
    <div v-else-if="loading">Cargando...</div>
    <div v-else class="students-layout">
      <section class="left-panel">
        <div class="card-list">
          <ScrollableCardList
            :items="students"
            :kind="'students'"
            v-model="selectedStudent"
            itemKey="id"
          />
        </div>
      </section>
      <section class="right-panel">
        <StudentBox
          v-if="selectedStudent"
          :item="selectedStudent"
          @hide="onHide"
          @cancel="onCancel"
          @save="onSaveStudent"
          @input="onEditedLocal"
        />
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
import StudentBox from './generic/boxes/StudentBox.vue'
import axios from 'axios'

export default {
  name: 'Students',
  components: {
    Header,
    NavBar,
    ActionBar,
    ScrollableCardList,
    StudentBox
  },
  data () {
    return {
      loading: true,
      error: null,
      degrees: [],
      students: [],
      selectedStudent: null,
      // ActionBar filters
      course: '',
      nameText: '',
      selectedStatus: 'unknown'
    }
  },
  mounted () {
    this.fetchStudents()
  },
  methods: {
    fetchStudents () {
      this.loading = true
      this.error = null
      const path = `${apiUrl}/api/v1/students`
      const params = {
        ...(this.course && { degree_id: this.course }),
        ...(this.nameText && { full_name: this.nameText }),
        ...((this.selectedStatus && this.selectedStatus !== 'unknown') && { status: this.selectedStatus })
      }

      axios.get(path, { params })
        .then(response => {
          this.degrees = response.data.data.degrees
          this.students = response.data.data.students
          // Restore student selection if included
          if (this.selectedStudent) {
            const found = this.students.find(s => s.official_id === this.selectedStudent.official_id)
            this.selectedStudent = found || null
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
      this.fetchStudents()
    },
    onNameTextChanged (val) {
      this.nameText = val
      this.fetchStudents()
    },
    onStatusChanged (val) {
      this.selectedStatus = val
      this.fetchStudents()
    },
    // Preview handlers
    onHide () {
      // TODO: implement hide functionality
    },
    onCancel () {
      this.selectedStudent = null
    },
    onEditedLocal (updated) {
      // Optionally keep a live mirror of edits in the selected object (in-memory only)
      this.selectedStudent = { ...this.selectedStudent, ...updated }
    },
    onSaveStudent (payload) {
      // TODO
      // Persist changes when API is available
      // axios.put(`${apiUrl}/api/v1/students/${payload.id}`, payload)
      //   .then(() => { /* refresh or notify */ })
      //   .catch(e => { this.error = e.response?.data?.message || e.message })
      // For now, merge into local list
      const idx = this.students.findIndex(s => s.id === payload.id)
      if (idx !== -1) this.$set(this.students, idx, { ...this.students[idx], ...payload })
      this.selectedStudent = { ...this.selectedStudent, ...payload }
    }
  }
}

</script>

<style scoped src="../css/Students.css"></style>
