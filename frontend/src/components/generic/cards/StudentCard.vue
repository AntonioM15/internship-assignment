<template>
  <div class="card-item">
    <div class="icon-box">
      <slot name="icon" :item="item">
        <img :src="defaultIcon" alt="Avatar" />
      </slot>
    </div>
    <div class="item-text">
      <div class="item-title">
        <slot name="title" :item="item">
          {{ item.full_name }}
        </slot>
      </div>
      <div class="item-text">
        <slot name="degree" :item="item">
          <!-- TODO - Update to json methods to show the actual degree name -->
          {{ item.degree }}
        </slot>
      </div>
    </div>
    <div class="item-status">
      <slot name="status" :item="item" :status="normalizedStatus">
        <img :src="statusIcon" :alt="`Estado: ${normalizedStatus}`" />
      </slot>
    </div>
  </div>
</template>

<script>
import IconUserDefault from '../../../assets/IconUserDefault.svg'
import IconStatusWhite from '../../../assets/IconStatusWhite.svg'
import IconStatusBlue from '../../../assets/IconStatusBlue.svg'
import IconStatusGreen from '../../../assets/IconStatusGreen.svg'
import IconStatusRed from '../../../assets/IconStatusRed.svg'
import IconStatusYellow from '../../../assets/IconStatusYellow.svg'

export default {
  name: 'StudentCard',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      defaultIcon: IconUserDefault,
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
