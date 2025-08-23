<template>
  <div class="modal-overlay" @click.self="emitCancel">
    <div class="modal-window">
      <div class="modal-columns">
        <section class="modal-col">
          <div class="icon-box">
            <slot name="icon">
              <img :src="defaultIcon" alt="Avatar"/>
            </slot>
          </div>
          <div class="title">{{ studentName }}</div>
          <div class="subtitle">{{ studentDegree }}</div>
        </section>

        <section class="modal-col divider">
          <div class="icon-box">
            <slot name="icon">
              <img :src="defaultIcon" alt="Avatar"/>
            </slot>
          </div>
          <div class="title">{{ tutorName }}</div>
          <div class="subtitle">{{ tutorDegrees }}</div>
        </section>

        <section class="modal-col">
          <div class="icon-box">
            <slot name="icon">
              <img :src="defaultCompanyIcon" alt="Avatar"/>
            </slot>
          </div>
          <div class="title">{{ companyName }}</div>
          <div class="subtitle">{{ internshipTitle }}</div>
        </section>
      </div>

      <div class="modal-actions">
        <div class="spacer"></div>
        <button class="btn" @click="emitCancel">Cancelar</button>
        <button class="btn" @click="$emit('save', assignment)">Guardar</button>
      </div>
    </div>
  </div>
</template>

<script>
import IconUserDefault from '../../../assets/IconUserDefault.svg'
import IconCompanyDark from '../../../assets/IconCompanyDark.svg'

export default {
  name: 'AssignmentPopUp',
  props: {
    assignment: { type: Object, required: true }
  },
  data () {
    return {
      defaultIcon: IconUserDefault,
      defaultCompanyIcon: IconCompanyDark
    }
  },
  computed: {
    studentName () {
      const a = this.assignment
      return (a.student && a.student.full_name) || 'Por asignar'
    },
    studentDegree () {
      const a = this.assignment
      return (a.student && a.student.degree) || ''
    },
    tutorName () {
      const a = this.assignment
      return (a.tutor && a.tutor.full_name) || 'Por asignar'
    },
    tutorDegrees () {
      const a = this.assignment
      const d = a.tutor && a.tutor.degrees
      return Array.isArray(d) ? d.join(', ') : ''
    },
    companyName () {
      const a = this.assignment
      return (a.company && a.company.full_name) || ''
    },
    internshipTitle () {
      const a = this.assignment
      return a.title || ''
    }
  },
  mounted () {
    window.addEventListener('keydown', this.onKeydown)
  },
  beforeDestroy () {
    window.removeEventListener('keydown', this.onKeydown)
  },
  methods: {
    onKeydown (e) {
      if (e.key === 'Escape') this.emitCancel()
    },
    emitCancel () {
      this.$emit('cancel')
    }
  }
}
</script>

<style scoped>
@import url('../../../css/PopUps.css');
</style>
