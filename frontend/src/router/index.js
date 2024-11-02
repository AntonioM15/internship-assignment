import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Main from '@/components/Main'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/landing',
      name: 'home',
      component: Home
    },
    {
      path: '/',
      name: 'main',
      component: Main
    }
  ],
  mode: 'history'
})
