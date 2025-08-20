<template>
  <div class="item-internships">
    <slot name="internships" :item="item">
      <div class="internships-icon">
        <img :src="iconInternships" :alt="`${internshipsCount} Internships`" />
        <span class="internships-count">{{ internshipsCount }}</span>
      </div>

    </slot>
  </div>
</template>

<script>
import IconInternships from '../../../assets/IconInternships.svg'

export default {
  name: 'CardInternships',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      iconInternships: IconInternships
    }
  },
  computed: {
    internshipsCount () {
      if (!this.item) return 0

      const list = this.item.internships || null
      return (Array.isArray(list)) ? list.length : 0
    }

  }
}
</script>

<style scoped>
@import url('../../../css/Cards.css');
</style>
