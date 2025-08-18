<template>
  <div class="card-item">
    <div class="item-text">
      <slot name="content" :item="item">
        {{ item.description }}
      </slot>
    </div>
  </div>
</template>

<script>

export default {
  name: 'DefaultCard',
  props: {
    item: {
      type: Object,
      required: true
    }
  }
}

</script>

<style scoped>
@import url('../../../css/Cards.css');
</style>
