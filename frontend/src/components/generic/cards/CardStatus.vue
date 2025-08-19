<template>
  <div class="item-status">
    <slot name="status" :item="item" :status="normalizedStatus">
      <img :src="statusIcon" :alt="`Estado: ${normalizedStatus}`" />
    </slot>
  </div>
</template>

<script>
import IconStatusWhite from '../../../assets/IconStatusWhite.svg'
import IconStatusBlue from '../../../assets/IconStatusBlue.svg'
import IconStatusGreen from '../../../assets/IconStatusGreen.svg'
import IconStatusRed from '../../../assets/IconStatusRed.svg'
import IconStatusYellow from '../../../assets/IconStatusYellow.svg'

export default {
  name: 'CardStatus',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      availableStatuses: ['unassigned', 'provisional', 'assigned', 'ongoing'],
      statusIcons: {
        unknown: IconStatusWhite,
        unassigned: IconStatusRed,
        provisional: IconStatusYellow,
        assigned: IconStatusBlue,
        ongoing: IconStatusGreen
      }
    }
  },
  computed: {
    normalizedStatus () {
      const value = (this.item && this.item.status) ? String(this.item.status).toLowerCase() : ''
      return this.availableStatuses.includes(value) ? value : 'unknown'
    },
    statusIcon () {
      return this.statusIcons[this.normalizedStatus]
    }
  }
}
</script>

<style scoped>
@import url('../../../css/Cards.css');
</style>
