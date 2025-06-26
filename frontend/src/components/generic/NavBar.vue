<!-- src/components/NavBar.vue -->
<template>
  <nav class="navbar">
    <ul class="nav-list">
      <li class="nav-item" v-for="link in links" :key="link.name">
        <router-link :to="link.path" class="nav-set">
          <img
            class="icon"
            :src=currentIcon(link)
            :alt=link.name
            @mouseover="hoverIcon = link.hoverIcon"
            @mouseleave="hoverIcon = null"
          />
          {{ link.name }}
        </router-link>
      </li>
      <li class="spacer"></li> <!-- Spacer to push logout to the right -->
      <li class="nav-option" v-for="option in options" :key="option.name">
        <router-link :to="option.path" class="nav-set">
          <img
            class="option"
            :src="currentIcon(option)"
            :alt="option.name"
            @mouseover="hoverIcon = option.hoverIcon"
            @mouseleave="hoverIcon = null"
          />
          {{ option.name }}
        </router-link>
      </li>
    </ul>
  </nav>

</template>

<script>
import IconDashboardLight from '../../assets/IconDashboardLight.svg'
import IconDashboardDark from '../../assets/IconDashboardDark.svg'
import IconStudentLight from '../../assets/IconStudentLight.svg'
import IconStudentDark from '../../assets/IconStudentDark.svg'
import IconProfessorLight from '../../assets/IconProfessorLight.svg'
import IconProfessorDark from '../../assets/IconProfessorDark.svg'
import IconCompanyLight from '../../assets/IconCompanyLight.svg'
import IconCompanyDark from '../../assets/IconCompanyDark.svg'
import IconAssignmentsLight from '../../assets/IconAssignmentsLight.svg'
import IconAssignmentsDark from '../../assets/IconAssignmentsDark.svg'
import IconLogOutLight from '../../assets/IconLogOutLight.svg'
import IconLogOutDark from '../../assets/IconLogOutDark.svg'

export default {
  name: 'NavBar',
  data () {
    return {
      hoverIcon: null, // Save the icon or option that it's being hovered
      links: [
        { name: 'Inicio', path: '/dashboard', icon: IconDashboardLight, hoverIcon: IconDashboardDark },
        { name: 'Estudiantes', path: '/students', icon: IconStudentLight, hoverIcon: IconStudentDark },
        { name: 'Tutores', path: '/tutors', icon: IconProfessorLight, hoverIcon: IconProfessorDark },
        { name: 'Empresas', path: '/companies', icon: IconCompanyLight, hoverIcon: IconCompanyDark },
        { name: 'Asignaciones', path: '/assignments', icon: IconAssignmentsLight, hoverIcon: IconAssignmentsDark }
      ],
      options: [
        { name: '', path: '/logout', icon: IconLogOutLight, hoverIcon: IconLogOutDark }
      ]
    }
  },
  methods: {
    currentIcon (link) {
      // Return hover icon/option if active, otherwise return default icon/option
      return this.hoverIcon === link.hoverIcon ? link.hoverIcon : link.icon
    }
  }
}

</script>

<style scoped>
@import url('../../css/NavBar.css');
</style>
