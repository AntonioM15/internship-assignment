<template>
  <div>
    <p>{{ message }}</p>
  </div>
</template>

<script>
import apiUrl from '../config'
import axios from 'axios'

export default {
  name: 'Main',
  data () {
    return {
      message: 'Sin mensaje!'
    }
  },
  methods: {
    getMessage () {
      const path = `${apiUrl}/api/v1/landing/message`
      axios.get(path).then((response) => {
        this.message = response.data
      })
        .catch((error) => {
          console.log(error)
        })
    }
  },
  created () {
    this.getMessage()
  }
}
</script>
