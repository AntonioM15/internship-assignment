<!-- src/components/Assigments.vue -->
<template>
  <div class="container">
    <Header/>
    <NavBar/>
    <AssignmentsActionBar
      :kind="'assignments'"
      @nameText-changed="onNameTextChanged"
      @status-changed="onStatusChanged"
    />
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
    <AssignmentPopUp
      v-if="selectedAssignment"
      :assignment="selectedAssignment"
      @cancel="onCancel"
      @save="onSave"
    />

  </div>

</template>

<script>
import apiUrl from '../config'
import Header from './generic/Header.vue'
import NavBar from './generic/NavBar.vue'
import AssignmentsActionBar from './generic/AssignmentsActionBar.vue'
import axios from 'axios'
import ScrollableCardList from './generic/ScrollableCardList.vue'
import AssignmentPopUp from './generic/popups/AssignmentPopUp.vue'

export default {
  name: 'Assignments',
  components: {
    Header,
    NavBar,
    AssignmentsActionBar,
    ScrollableCardList,
    AssignmentPopUp
  },
  data () {
    return {
      loading: true,
      error: null,
      assignments: [],
      selectedAssignment: null,
      // AssignmentsActionBar filters
      nameText: '',
      selectedStatus: 'unknown'
    }
  },
  mounted () {
    this.fetchAssignments()
  },
  methods: {
    fetchAssignments () {
      this.loading = true
      this.error = null
      const path = `${apiUrl}/api/v1/assignments`
      const params = {
        ...(this.nameText && { full_name: this.nameText }),
        ...((this.selectedStatus && this.selectedStatus !== 'unknown') && { status: this.selectedStatus })
      }

      axios.get(path, { params })
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
    // Filter handlers
    onNameTextChanged (val) {
      this.nameText = val
      this.fetchAssignments()
    },
    onStatusChanged (val) {
      this.selectedStatus = val
      this.fetchAssignments()
    },
    // Preview handlers
    onCancel () {
      // Close the pop-up and unselect the assignment
      this.selectedAssignment = null
    },
    onSave () {
      // TODO Placeholder for future action
    }
  }
}

</script>

<style scoped src="../css/Assigments.css"></style>
