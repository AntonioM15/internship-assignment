<template>
  <div class="card-item">
    <div class="icon-box">
      <slot name="icon" :item="item">
        <img :src="defaultIcon" alt="Avatar" />
      </slot>
    </div>
    <div class="item-text">
      <slot name="content" :item="item">
        {{ item.description }}
      </slot>
    </div>
  </div>
</template>

<script>
import IconUserDefault from '../../../assets/IconUserDefault.svg'

export default {
  name: 'NotificationCard',
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
