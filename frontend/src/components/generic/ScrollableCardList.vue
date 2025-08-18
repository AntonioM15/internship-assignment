<template>
  <div class="scrollable-box">
    <div
      v-for="(item, index) in items"
      :key="index"
      class="card-items"
      :class="{ selected: isSelected(item) }"
      @click="onSelect(item, index)"
      role="button"
      tabindex="0"
    >
      <component :is="resolvedElement" :item="item" />
    </div>
  </div>
</template>

<script>
import DefaultCard from './cards/DefaultCard.vue'
import NotificationCard from './cards/NotificationCard.vue'
import StudentCard from './cards/StudentCard.vue'

// Local registry
const ELEMENTS = {
  notifications: NotificationCard,
  students: StudentCard
}

export default {
  name: 'ScrollableCardList',
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
    onSelect (item) {
      // Toggle selection: click again to unselect
      if (this.isSelected(item)) {
        this.$emit('input', null)
        this.$emit('unselect', item)
      } else {
        // v-model
        this.$emit('input', item)
        // Also emit explicit event if the parent prefers listening
        this.$emit('select', item)
      }
    },
    isSelected (item) {
      if (!this.value) return false
      const k = this.itemKey
      if (k && item && this.value && item[k] !== undefined && this.value[k] !== undefined) {
        return item[k] === this.value[k]
      }
      return this.value === item
    }
  }
}
</script>

<style scoped>
@import url('../../css/ScrollableCardList.css');
</style>
