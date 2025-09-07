<script>
import apiUrl from '../config'
import axios from 'axios'

export default {
  name: 'Main',
  methods: {
    async redirectBasedOnAuth () {
      const path = `${apiUrl}/api/v1/landing/is-user-logged-in`
      try {
        const response = await axios.get(path, {withCredentials: true})
        const isLoggedIn = response.data.data.logged_in

        if (isLoggedIn) {
          await this.$router.replace({path: '/dashboard'})
        } else {
          await this.$router.replace({ path: '/landing' })
        }
      } catch (e) {
        // On error, default to landing
        await this.$router.replace({ path: '/landing' })
      }
    }
  },
  created () {
    this.redirectBasedOnAuth()
  }
}
</script>
