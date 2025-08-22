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
      defaultIcon: IconUserDefault
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
