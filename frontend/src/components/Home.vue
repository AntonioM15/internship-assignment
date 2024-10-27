<!-- src/components/Home.vue -->
<template>
  <div class="container">
    <div class="header">
      <h1>Portal Prácticas de Ciclos</h1>
    </div>

    <div class="main">
      <div class="left-section">
        <div class="icons">
          <img class="icon" src="../assets/IconCompany.svg" alt="Empresas" />
          <img class="icon" src="../assets/IconProfessor.svg" alt="Profesores" />
          <img class="icon" src="../assets/IconStudent.svg" alt="Estudiantes" />
        </div>

        <div class="description">
          <p class="title">Una web para gobernarlos a todos</p>
          <p class="subtitle">Empresas, tutores y estudiantes en la misma plataforma</p>
        </div>
      </div>

      <div class="right-section">
        <div class="top-right-section">
          <h2>Iniciar sesión</h2>
          <form @submit.prevent="login">
            <input type="text" v-model="username" placeholder="usuario" required>
            <input type="password" v-model="password" placeholder="contraseña" required>
            <div class="custom-button">
              <button type="submit">Log in</button>
            </div>
          </form>
        </div>

        <div class="bottom-right-section">
          <h2>Recuperar contraseña</h2>
          <form @submit.prevent="recoverPassword">
            <input type="text" v-model="recoverUsername" placeholder="usuario" required>
            <div class="custom-button">
              <button type="submit">Solicitar</button>
            </div>
          </form>
          <p class="help-text">¿Tienes algún problema? <a href="#">Contáctanos</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: '',
      recoverUsername: ''
    }
  },
  methods: {
    login () {
      console.log('Iniciando sesión con', this.username, this.password)
    },
    recoverPassword () {
      console.log('Recuperar contraseña para', this.recoverUsername)
    }
  }
}

</script>

<style scoped src="../css/Home.css"></style>
