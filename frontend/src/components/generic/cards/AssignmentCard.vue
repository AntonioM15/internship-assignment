<template>
  <div
    class="card-row"
    :class="{ selected }"
    @click="toggle"
    role="button"
    tabindex="0"
  >
    <!-- STUDENT -->
    <div class="card-item">
      <div class="icon-box" style="width: 70px; height: 70px;">
        <slot name="icon" :item="item">
          <img :src="defaultIcon" alt="Avatar" style="width: 50px; height: 50px;"/>
        </slot>
      </div>
      <div class="item-text">
        <div class="item-title">
          <slot name="title" :item="item">
            {{ item && item.student ? item.student.full_name : null }}
          </slot>
        </div>
        <div class="item-text">
          <slot name="degree" :item="item">
            {{ item && item.student ? item.student.degree : null }}
          </slot>
        </div>
      </div>
    </div>
    <!-- TUTOR -->
    <div class="card-item">
      <div class="icon-box" style="width: 70px; height: 70px;">
        <slot name="icon" :item="item">
          <img :src="defaultIcon" alt="Avatar" style="width: 50px; height: 50px;"/>
        </slot>
      </div>
      <div class="item-text">
        <div class="item-title">
          <slot name="title" :item="item">
            {{ item && item.tutor ? item.tutor.full_name : null }}
          </slot>
        </div>
        <div class="item-text">
          <slot name="degrees" :item="item">
            <!-- {{ item.tutor.degrees.join(', ') }} -->
            {{ tutorDegreesText }}
          </slot>
        </div>
      </div>
    </div>
    <!-- COMPANY -->
    <div class="card-item">
      <div class="icon-box" style="width: 70px; height: 70px;">
        <slot name="icon" :item="item" >
          <img :src="defaultCompanyIcon" alt="Avatar" style="width: 50px; height: 50px;"/>
        </slot>
      </div>
      <div class="item-text">
        <div class="item-title">
          <slot name="title" :item="item">
            {{ item && item.company ? item.company.full_name : null }}
          </slot>
        </div>
        <div class="item-text">
          <slot name="field" :item="item">
            {{ item && item.company ? item.company.field : null }}
          </slot>
        </div>
      </div>
      <CardStatus :item="item" />
    </div>
  </div>

</template>

<script>
import IconUserDefault from '../../../assets/IconUserDefault.svg'
import IconCompanyDark from '../../../assets/IconCompanyDark.svg'
import CardStatus from './CardStatus.vue'

export default {
  name: 'AssignmentCard',
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
      defaultIcon: IconUserDefault,
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
    },
    tutorDegreesText () {
      const d = this.item && this.item.degrees
      return Array.isArray(d) ? d.join(', ') : ''
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
