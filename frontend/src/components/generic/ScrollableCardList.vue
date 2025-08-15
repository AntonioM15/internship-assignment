<template>
  <div class="scrollable-box">
    <div v-for="(item, index) in items" :key="index" class="card-items">
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
    }
  },
  computed: {
    resolvedElement () {
      return ELEMENTS[this.kind] || DefaultCard
    }
  }

}
</script>

<style scoped>
@import url('../../css/ScrollableCardList.css');
</style>
