<template>
  <div class="internships-wrapper" v-if="company">
    <div v-if="internships.length !== 0" class="internships-list">
      <div
        v-for="(internship, idx) in internships"
        :key="idx"
        class="internship-card"
      >
        <div class="spacer"></div>
        <div class="content">
          <div class="title">
            {{ readTitle(internship) }}
          </div>
          <div class="subtitle">
            {{ readSubtitle(internship) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InternshipCard',
  props: {
    company: {
      type: Object,
      required: true
    }
  },
  computed: {
    internships () {
      const c = this.company
      return c && Array.isArray(c.internships) ? c.internships : []
    }
  },
  methods: {
    readTitle (i) {
      return i.title || ''
    },
    readSubtitle (i) {
      return i.description || ''
    }
  }
}
</script>

<style scoped>
@import url('../../../css/Cards.css');
</style>
