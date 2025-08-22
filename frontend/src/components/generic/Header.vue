<template>
  <header class="header">
    <h1>{{ title }}</h1>
  </header>
</template>

<script>
export default {
  name: 'Header',
  props: {
    title: {
      type: String,
      default: 'Portal Prácticas de Ciclos'
    }
  }
}
</script>

<style scoped>
@import url('../../css/Header.css');
</style>
