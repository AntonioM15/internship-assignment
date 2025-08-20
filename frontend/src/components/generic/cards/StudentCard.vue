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
          {{ item.degree.code }}
        </slot>
      </div>
    </div>
    <CardStatus :item="item" />
  </div>
</template>

<script>
import IconUserDefault from '../../../assets/IconUserDefault.svg'
import CardStatus from './CardStatus.vue'

export default {
  name: 'StudentCard',
  components: {
    CardStatus
  },
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      defaultIcon: IconUserDefault
    }
  }
}
</script>

<style scoped>
@import url('../../../css/Cards.css');
</style>
