import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Home'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'main',
      component: Main
    }
  ],
  mode: 'history'
})
