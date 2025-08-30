<!-- src/components/Companies.vue -->
<template>
  <div class="container">
    <Header/>
    <NavBar/>
    <ActionBar
      :kind="'companies'"
      :degrees="degrees"
      @course-changed="onFieldChanged"
      @nameText-changed="onNameTextChanged"
      @status-changed="onStatusChanged"
    />
    <div v-if="error" style="color: red;">Error: {{ error }}</div>
    <div v-else class="companies-layout">
      <section class="left-panel">
        <div class="card-list">
          <ScrollableCardList
            :items="companies"
            :kind="'companies'"
            v-model="selectedCompany"
            itemKey="id"
            :selected-internship.sync="selectedInternship"
            @internship-change="selectedInternship = $event"
          />
        </div>
      </section>
      <section class="right-panel">
        <CompanyBox
          v-if="selectedCompany && !selectedInternship"
          :item="selectedCompany"
          @hide="onHideCompany"
          @cancel="onCancelCompany"
          @save="onSaveCompany"
          @input="onEditedCompany"
        />
        <InternshipBox
          v-if="selectedInternship"
          :item="selectedInternship"
          @hide="onHideInternship"
          @cancel="onCancelInternship"
          @save="onSaveInternship"
          @input="onEditedInternship"
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
import axios from 'axios'
import CompanyBox from './generic/boxes/CompanyBox.vue'
import InternshipBox from './generic/boxes/InternshipBox.vue'

export default {
  name: 'Companies',
  components: {
    Header,
    NavBar,
    ActionBar,
    ScrollableCardList,
    CompanyBox,
    InternshipBox
  },
  data () {
    return {
      loading: true,
      error: null,
      degrees: [],
      companies: [],
      selectedCompany: null,
      selectedInternship: null,
      // ActionBar filters
      field: '',
      nameText: '',
      selectedStatus: 'unknown'
    }
  },
  mounted () {
    this.fetchCompanies()
  },
  methods: {
    fetchCompanies () {
      this.loading = true
      this.error = null
      const path = `${apiUrl}/api/v1/companies`
      const params = {
        ...(this.field && { field: this.field }),
        ...(this.nameText && { full_name: this.nameText }),
        ...((this.selectedStatus && this.selectedStatus !== 'unknown') && { status: this.selectedStatus })
      }

      axios.get(path, { params })
        .then(response => {
          this.degrees = response.data.data.degrees
          this.companies = response.data.data.companies
          if (this.selectedCompany) {
            // Restore company selection if included
            const found = this.companies.find(s => s.full_name === this.selectedCompany.full_name)
            this.selectedCompany = found || null
          } else if (this.selectedInternship) {
            // Restore internship selection if included
            let foundInternship = null
            for (const company of this.companies) {
              const internshipList = Array.isArray(company.internships) ? company.internships : []
              const match = internshipList.find(i =>
                i &&
                i.title === this.selectedInternship.title &&
                i.company.full_name === this.selectedInternship.company.full_name
              )
              if (match) {
                foundInternship = match
                break
              }
            }
            this.selectedInternship = foundInternship || null
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
    onFieldChanged (val) {
      // Fields only save the name and not a full object
      this.field = val.full_name
      this.fetchCompanies()
    },
    onNameTextChanged (val) {
      this.nameText = val
      this.fetchCompanies()
    },
    onStatusChanged (val) {
      this.selectedStatus = val
      this.fetchCompanies()
    },
    // COMPANY handlers
    onHideCompany () {
      // TODO: implement hide functionality
    },
    onCancelCompany () {
      this.selectedCompany = null
    },
    onEditedCompany (updated) {
      // Optionally keep a live mirror of edits in the selected object (in-memory only)
      this.selectedCompany = { ...this.selectedCompany, ...updated }
    },
    onSaveCompany (payload) {
      // TODO
      // Persist changes when API is available
      // axios.put(`${apiUrl}/api/v1/companies/${payload.id}`, payload)
      //   .then(() => { /* refresh or notify */ })
      //   .catch(e => { this.error = e.response?.data?.message || e.message })
      // For now, merge into local list
      const idx = this.companies.findIndex(s => s.id === payload.id)
      if (idx !== -1) this.$set(this.companies, idx, { ...this.companies[idx], ...payload })
      this.selectedCompany = { ...this.selectedCompany, ...payload }
    },
    // INTERNSHIP handlers
    onHideInternship () {
      // TODO: implement hide functionality
    },
    onCancelInternship () {
      this.selectedInternship = null
    },
    onEditedInternship (updated) {
      this.selectedInternship = { ...this.selectedInternship, ...updated }
    },
    onSaveInternship (payload) {
      const { companyId, ...patch } = payload
      const companyIdx = this.companies.findIndex(c => c && c.id === companyId)
      if (companyIdx !== -1) {
        const company = this.companies[companyIdx]
        const internships = Array.isArray(company.internships) ? company.internships : []
        const idx = internships.findIndex(i => i && i.id === payload.id)
        if (idx !== -1) {
          const updated = internships.slice()
          updated[idx] = { ...updated[idx], ...patch }
          this.$set(this.companies, companyIdx, { ...company, internships: updated })
        }
      }
      this.selectedInternship = { ...this.selectedInternship, ...patch, id: payload.id }
    }
  }
}

</script>

<style scoped src="../css/Companies.css"></style>
