<!-- src/components/NavBar.vue -->
<template>
  <nav class="navbar">
    <ul class="nav-list">
      <li class="nav-item" v-for="link in links" :key="link.name">
        <router-link :to="link.path">{{ link.name }}</router-link>
      </li>
    </ul>
  </nav>

</template>

<script>
export default {
  name: 'NavBar',
  data () {
    return {
      links: [
        { name: 'Inicio', path: '/dashboard' },
        { name: 'Estudiantes', path: '/students' },
        { name: 'Tutores', path: '/tutors' },
        { name: 'Empresas', path: '/companies' },
        { name: 'Asignaciones', path: '/assignments' }
      ]
    }
  }
}

</script>

<style scoped>
@import url('../../css/NavBar.css');
</style>
