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
      <div v-if="isCompanyOpen(item)" class="internships-panel">
        <InternshipCard
          :company="item"
          v-model="selectedInternship"
          :item-key="itemKey"
          @input="onInternshipInput"
        />
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
    },
    selectedInternship: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      lastSelectedCompany: null
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
    },
    // The internships panel remains open if either:
    // - the company is selected (normal behavior), or
    // - an internship belonging to that company is currently selected.
    isCompanyOpen (item) {
      if (this.kind !== 'companies') return false
      if (this.isCompanySelected(item)) return true
      if (!this.selectedInternship) return false
      const k = this.itemKey
      const hasInternships = item && Array.isArray(item.internships)
      if (!hasInternships) return false
      return item.internships.some(i => {
        if (k && i && this.selectedInternship &&
          i[k] !== undefined && this.selectedInternship[k] !== undefined) {
          return i[k] === this.selectedInternship[k]
        }
        return i === this.selectedInternship
      })
    },
    // Selecting an internship unselects the company; unselecting the internship restores the previous company
    onInternshipInput (nextInternship) {
      if (nextInternship) {
        // If selecting an internship, remember the current company and clear it
        this.lastSelectedCompany = this.value || this.lastSelectedCompany
        this.selectedInternship = nextInternship
        this.$emit('input', null)
      } else {
        // Unselecting an internship restores the previous company selection
        const toRestore = this.kind === 'companies' ? this.lastSelectedCompany : null
        this.selectedInternship = null
        if (toRestore) {
          this.$emit('input', toRestore)
        }
      }
      // notify parent that internship is cleared
      this.$emit('update:selected-internship', this.selectedInternship)
    }

  },
  watch: {
    selectedInternship (val) {
      this.selectedInternship = val
      this.$emit('update:selected-internship', this.selectedInternship)
    }
  }
}
</script>

<style scoped>
@import url('../../css/ScrollableCardList.css');
</style>
