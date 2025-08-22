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
        <slot name="degrees" :item="item">
          <!-- TODO - Update to json methods to show the actual degrees names -->
          {{ degreesText }}
        </slot>
      </div>
    </div>
    <!-- TODO - Update to json methods -->
    <CardStatus :item="item" />
  </div>
</template>

<script>
import IconUserDefault from '../../../assets/IconUserDefault.svg'
import CardStatus from './CardStatus.vue'

export default {
  name: 'TutorCard',
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
    },
    degreesText () {
      const d = this.item && this.item.degrees
      const codes = Array.isArray(d) ? d.map(deg => deg && deg.code).filter(Boolean) : []
      return codes.join(', ')
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
