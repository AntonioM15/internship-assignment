<template>
  <div class="card-item">
    <div class="icon-box">
      <slot name="icon" :item="item">
        <img :src="defaultCompanyIcon" alt="Avatar" />
      </slot>
    </div>
    <div class="item-text">
      <div class="item-title">
        <slot name="title" :item="item">
          {{ item.full_name }}
        </slot>
      </div>
      <div class="item-text">
        <slot name="field" :item="item">
          {{ item.field }}
        </slot>
      </div>
    </div>
    <CardInternships :item="item"/>
  </div>
</template>

<script>
import IconCompanyDark from '../../../assets/IconCompanyDark.svg'
import CardInternships from './CardInternships.vue'

export default {
  name: 'CompanyCard',
  components: {
    CardInternships
  },
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      defaultCompanyIcon: IconCompanyDark
    }
  }
}
</script>

<style scoped>
@import url('../../../css/Cards.css');
</style>
