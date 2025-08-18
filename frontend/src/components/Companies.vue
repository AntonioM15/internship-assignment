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
          />
        </div>
      </section>
      <section class="right-panel">
        <CompanyBox
          v-if="selectedCompany"
          :item="selectedCompany"
          @hide="onHide"
          @cancel="onCancel"
          @save="onSaveCompany"
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
import axios from 'axios'
import CompanyBox from './generic/boxes/CompanyBox.vue'

export default {
  name: 'Companies',
  components: {
    Header,
    NavBar,
    ActionBar,
    ScrollableCardList,
    CompanyBox
  },
  data () {
    return {
      loading: true,
      error: null,
      companies: [],
      selectedCompany: null
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
    onHide () {
      // TODO: implement hide functionality
    },
    onCancel () {
      this.selectedCompany = null
    },
    onEditedLocal (updated) {
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
    }
  }
}

</script>

<style scoped src="../css/Companies.css"></style>
