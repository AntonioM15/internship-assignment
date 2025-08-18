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
import ScrollableCardList from './generic/ScrollableCardList.vue'
import ActionBar from './generic/ActionBar.vue'
import StudentBox from './generic/boxes/StudentBox.vue'
import axios from 'axios'

export default {
  name: 'Students',
  components: {
    Header,
    NavBar,
    ScrollableCardList,
    ActionBar,
    StudentBox
  },
  data () {
    return {
      loading: true,
      error: null,
      students: [],
      selectedStudent: null
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
