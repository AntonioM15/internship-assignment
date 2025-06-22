import Vue from 'vue'
import Router from 'vue-router'
import Assignments from '@/components/Assignments'
import Companies from '@/components/Companies'
import Dashboard from '@/components/Dashboard'
import Home from '@/components/Home'
import Main from '@/components/Main'
import Students from '@/components/Students'
import Tutors from '@/components/Tutors'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/landing', name: 'home', component: Home },
    // TODO remove Main -> Main should redirect to landing or dashboard depending if the user has logged in
    { path: '/', name: 'main', component: Main },
    { path: '/dashboard', name: 'main', component: Dashboard },
    { path: '/students', name: 'main', component: Students },
    { path: '/tutors', name: 'main', component: Tutors },
    { path: '/companies', name: 'main', component: Companies },
    { path: '/assignments', name: 'main', component: Assignments }
  ],
  mode: 'history'
})
