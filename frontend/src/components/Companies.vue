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
  name: 'Companies',
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
  }
}

</script>

<style scoped src="../css/Companies.css"></style>
