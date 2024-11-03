<template>
  <div>
    <p>{{ message }}</p>
  </div>
</template>

<script>
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
      const path = 'http://127.0.0.1:5000/api/v1/landing/message'
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
