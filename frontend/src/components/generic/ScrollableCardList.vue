<template>
  <div class="scrollable-box">
    <div
      v-for="(item, index) in items"
      :key="index"
      class="card-items"
    >
      <component
        :is="resolvedElement"
        :item="item"
        :selected-item="value"
        :item-key="itemKey"
        v-on="$listeners"
      />
      <div v-if="isCompanySelected(item)" class="internships-panel">
        <InternshipCard :company="item"/>
      </div>
    </div>
  </div>
</template>

<script>
import DefaultCard from './cards/DefaultCard.vue'
import NotificationCard from './cards/NotificationCard.vue'
import StudentCard from './cards/StudentCard.vue'
import TutorCard from './cards/TutorCard.vue'
import CompanyCard from './cards/CompanyCard.vue'
import AssignmentCard from './cards/AssignmentCard.vue'
import InternshipCard from './cards/InternshipCard.vue'

// Local registry
const ELEMENTS = {
  notifications: NotificationCard,
  students: StudentCard,
  tutors: TutorCard,
  companies: CompanyCard,
  assignments: AssignmentCard
}

export default {
  name: 'ScrollableCardList',
  components: {
    InternshipCard
  },
  props: {
    items: {
      type: Array,
      required: true
    },
    kind: {
      type: String,
      default: 'notifications'
    },
    // Supports v-model for selected element
    value: {
      type: Object,
      default: null
    },
    // Optional key to compare objects (falls back to strict equality)
    itemKey: {
      type: String,
      default: 'id'
    }
  },
  computed: {
    resolvedElement () {
      return ELEMENTS[this.kind] || DefaultCard
    }
  },
  methods: {
    isCompanySelected (item) {
      // relies on v-model being updated by the child component
      const k = this.itemKey
      if (!this.value) return false
      if (k && item && this.value && item[k] !== undefined && this.value[k] !== undefined) {
        return this.kind === 'companies' && item[k] === this.value[k]
      }
      return this.kind === 'companies' && this.value === item
    }
  }
}
</script>

<style scoped>
@import url('../../css/ScrollableCardList.css');
</style>
