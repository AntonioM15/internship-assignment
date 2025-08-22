<template>
  <div
    class="card-item"
    :class="{ selected }"
    @click="toggle"
    role="button"
    tabindex="0"
  >
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
