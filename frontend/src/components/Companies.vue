<!-- src/components/Companies.vue -->
<template>
  <div class="container">
    <Header/>
    <NavBar/>
    <ActionBar :kind="'companies'"/>
    <div v-if="error" style="color: red;">Error: {{ error }}</div>
    <div v-else-if="loading">Cargando...</div>
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
      companies: [],
      selectedCompany: null,
      selectedInternship: null
    }
  },
  mounted () {
    const path = `${apiUrl}/api/v1/companies`
    axios.get(path)
      .then(response => {
        this.companies = response.data.data.companies
      })
      .catch(err => {
        this.error = err.response.data.message || err.message
      })
      .finally(() => {
        this.loading = false
      })
  },
  methods: {
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
