<template>
  <div class="internships-wrapper" v-if="company">
    <div v-if="internships.length !== 0" class="internships-list">
      <div
        v-for="(internship, idx) in internships"
        :key="idx"
        class="internship-card"
        :class="{ selected: isSelected(internship) }"
        @click="toggle(internship)"
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
        <CardStatus :item="internship" />
      </div>
    </div>
  </div>
</template>

<script>
import CardStatus from './CardStatus.vue'

export default {
  name: 'InternshipCard',
  components: {
    CardStatus
  },
  props: {
    company: {
      type: Object,
      required: true
    },
    value: {
      type: Object,
      default: null
    },
    itemKey: {
      type: String,
      default: 'id'
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
    },
    isSelected (i) {
      const k = this.itemKey
      if (!this.value) return false
      if (k && i && this.value && i[k] !== undefined && this.value[k] !== undefined) {
        return i[k] === this.value[k]
      }
      return this.value === i
    },
    toggle (i) {
      const next = this.isSelected(i) ? null : i
      // Emit v-model update
      this.$emit('input', next)
      // Also emit a semantic event if parents want to react
      this.$emit('select-internship', next)
    }
  }
}
</script>

<style scoped>
@import url('../../../css/Cards.css');
</style>
