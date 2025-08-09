<template>
  <div class="scrollable-box">
    <div v-for="(item, index) in items" :key="index" class="card-item">
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
  </div>
</template>

<script>
import IconUserDefault from '../../assets/IconUserDefault.svg'
export default {
  name: 'ScrollableCardList',
  props: {
    items: {
      type: Array,
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
@import url('../../css/ScrollableCardList.css');
</style>
