<!-- src/components/Home.vue -->
<template>
  <div class="container">
    <Header/>

    <div class="main">
      <div class="left-section">
        <div class="icons">
          <img class="icon" src="../assets/IconCompanyDark.svg" alt="Empresas" />
          <img class="icon" src="../assets/IconProfessorDark.svg" alt="Profesores" />
          <img class="icon" src="../assets/IconStudentDark.svg" alt="Estudiantes" />
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
            <input type="text" v-model="email" placeholder="email" required>
            <input type="password" v-model="password" placeholder="contraseña" required>
            <div class="button-with-message">
              <p class="custom-message" @change="loginMessage" style="color: red"> {{loginMessage}} </p>
              <div class="custom-button">
                <button type="submit">Log in</button>
              </div>
            </div>
          </form>
        </div>

        <div class="bottom-right-section">
          <h2>Recuperar contraseña</h2>
          <form @submit.prevent="recoverPassword">
            <input type="text" v-model="recoverEmail" placeholder="email" required>
            <div class="button-with-message">
              <p class="custom-message" @change="passwordMessage" :style="{ color: passwordMessageColor}">
                {{passwordMessage}}
              </p>
              <div class="custom-button">
                <button type="submit">Solicitar</button>
              </div>
            </div>
          </form>
          <p class="help-text">¿Tienes algún problema? <a href="#">Contáctanos</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiUrl from '../config'
import Header from './generic/Header.vue'
import axios from 'axios'

export default {
  name: 'Login',
  components: {
    Header
  },
  data () {
    return {
      email: '',
      password: '',
      recoverEmail: '',
      loginMessage: '',
      passwordMessage: '',
      passwordMessageColor: 'red'
    }
  },
  methods: {
    async login () {
      // TODO manage urls more professionally
      const path = `${apiUrl}/api/v1/landing/login`
      const params = {
        'email': this.email,
        'password': this.password
      }
      try {
        await axios.post(path, params)
        this.loginMessage = ''
        await this.$router.push('/dashboard')
      } catch (error) {
        // update loginMessage with the error
        const errorContent = error.response
        this.loginMessage = errorContent.data.message
      }
    },
    async recoverPassword () {
      const path = `${apiUrl}/api/v1/landing/password-recovery`
      const params = {
        'email': this.recoverEmail
      }
      try {
        const response = await axios.post(path, params)
        // update passwordMessage
        this.passwordMessage = response.data.message
        this.passwordMessageColor = 'green'
      } catch (error) {
        // update passwordMessage
        const errorContent = error.response
        this.passwordMessage = errorContent.data.message
        this.passwordMessageColor = 'red'
      }
    }
  }
}

</script>

<style scoped src="../css/Home.css"></style>
