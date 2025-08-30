<!-- src/components/ActionBar.vue -->
<template>
  <div class="action-bar">
    <div class="filters-section">
      <div class="filter-group">
        <input
          type="text"
          class="filter-element"
          style="width: 60%; min-width: 300px; padding-left: 5px;"
          placeholder="Título Práctica"
          v-model="nameText"
        />
      </div>
      <div class="filter-group" style="margin-left: 4px;">
        <img :src="statusIcons[selectedStatus]" :alt="statusTexts[selectedStatus]" style="width:24px;height:24px; margin: 0 8px 0 6px;"/>
        <select
          class="filter-element"
          style="width: 100%; min-width: 225px;"
          v-model="selectedStatus" :class="{ 'is-placeholder': selectedStatus === 'white' }"
          @change="emitStatus"
        >
          <option v-for="statusOption in statusOptions" :key="statusOption" :value="statusOption">
            {{ statusTexts[statusOption] }}
          </option>
        </select>
      </div>
    </div>
    <div class="action-section">
      <div class="action-group" style="min-width: 225px;">
        <select class="action-element"  style="width: 100%;" v-model="assignmentKind">
          <option v-for="assignmentOptions in assignmentOptions" :key="assignmentOptions" :value="assignmentOptions">
            {{ assignmentsTexts[assignmentOptions] }}
          </option>
        </select>
      </div>
      <button class="assign-btn" @click="assignEntities">
        Asignar
      </button>
    </div>
  </div>
</template>

<script>

import IconStatusWhite from '../../assets/IconStatusWhite.svg'
import IconStatusBlue from '../../assets/IconStatusBlue.svg'
import IconStatusGreen from '../../assets/IconStatusGreen.svg'
import IconStatusRed from '../../assets/IconStatusRed.svg'
import IconStatusYellow from '../../assets/IconStatusYellow.svg'

export default {
  name: 'AssignmentsActionBar',
  props: {
    // Not used, kept for consistency with other components
    kind: {
      type: String,
      default: 'assignments'
    }
  },
  data () {
    return {
      nameText: '',
      statusOptions: ['white', 'red', 'yellow', 'blue', 'green'], // Deterministic order for the select
      statusIcons: {
        white: IconStatusWhite,
        red: IconStatusRed,
        yellow: IconStatusYellow,
        blue: IconStatusBlue,
        green: IconStatusGreen
      },
      statusTexts: {
        white: 'Todos los estados',
        red: 'Por asignar',
        yellow: 'Asignado - Por aprobar',
        blue: 'Asignado - Aprobado',
        green: 'Asignado - En curso'
      },
      selectedStatus: 'white',
      assignmentKind: 'distanceStudents', // Distance for students used as default value
      assignmentOptions: ['distanceStudents', 'distanceTutors', 'preferenceStudents', 'preferenceCompanies'],
      assignmentsTexts: {
        distanceStudents: 'Distancia estudiantes',
        distanceTutors: 'Distancia profesores',
        preferenceStudents: 'Preferencia estudiantes',
        preferenceCompanies: 'Preferencia empresas'
      }
    }
  },
  methods: {
    emitStatus () {
      this.$emit('status-changed', this.selectedStatus)
    },
    assignEntities () {
      // TODO: Implement popup
      console.log('Adding a new entity')
    }
  }
}
</script>

<style scoped>
@import url('../../css/AssignmentsActionBar.css');
</style>
