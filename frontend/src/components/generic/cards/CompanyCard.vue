<template>
  <div
    class="card-item"
    :class="{ selected }"
    @click="toggle"
    role="button"
    tabindex="0"
  >
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
    },
    selectedItem: {
      type: Object,
      default: null
    },
    itemKey: {
      type: String,
      default: 'id'
    }
  },
  data () {
    return {
      defaultCompanyIcon: IconCompanyDark
    }
  },
  computed: {
    selected () {
      const k = this.itemKey
      if (!this.selectedItem) return false
      if (k && this.item && this.selectedItem &&
          this.item[k] !== undefined && this.selectedItem[k] !== undefined) {
        return this.item[k] === this.selectedItem[k]
      }
      return this.selectedItem === this.item
    }
  },
  methods: {
    toggle () {
      if (this.selected) {
        this.$emit('input', null)
        this.$emit('unselect', this.item)
      } else {
        this.$emit('input', this.item)
        this.$emit('select', this.item)
      }
    }
  }
}
</script>

<style scoped>
@import url('../../../css/Cards.css');
</style>
