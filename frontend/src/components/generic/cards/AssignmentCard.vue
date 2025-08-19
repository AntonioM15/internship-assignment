<template>
  <div class="card-row">
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
            <!-- TODO - Update to json methods -->
            {{ item.student.full_name }}
          </slot>
        </div>
        <div class="item-text">
          <slot name="degree" :item="item">
            <!-- TODO - Update to json methods to show the actual degree name -->
            {{ item.student.degree }}
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
            {{ item.tutor.full_name }}
          </slot>
        </div>
        <div class="item-text">
          <slot name="degrees" :item="item">
            <!-- TODO - Update to json methods to show the actual degrees names -->
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
            {{ item.company.full_name }}
          </slot>
        </div>
        <div class="item-text">
          <slot name="field" :item="item">
            {{ item.company.field }}
          </slot>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import IconUserDefault from '../../../assets/IconUserDefault.svg'
import IconCompanyDark from '../../../assets/IconCompanyDark.svg'

export default {
  name: 'AssignmentCard',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      defaultIcon: IconUserDefault,
      defaultCompanyIcon: IconCompanyDark
    }
  },
  computed: {
    tutorDegreesText () {
      const d = this.item && this.item.degrees
      return Array.isArray(d) ? d.join(', ') : ''
    }
  }
}
</script>

<style scoped>
@import url('../../../css/Cards.css');
</style>
