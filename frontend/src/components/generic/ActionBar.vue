<!-- src/components/ActionBar.vue -->
<template>
  <div class="action-bar">
    <div class="filters-section">
      <div class="filter-group" style="min-width: 400px;">
        <select class="filter-element"  style="width: 40%; min-width: 150px;" v-model="course" :class="{ 'is-placeholder': course === '' }">
          <!-- TODO - values are mocked -->
          <option value="">Titulación</option> <!-- Used as a placeholder -->
          <option value="informatica">Informática</option>
          <option value="electronica">Electrónica</option>
          <option value="mecanica">Mecánica</option>
        </select>
        <input
          type="text"
          class="filter-element"
          style="width: 60%; min-width: 225px; padding-left: 5px;"
          :placeholder="filterPlaceholder"
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
      <button class="add-student-btn" @click="addEntities">
        <img src="../../assets/IconAddLight.svg" :alt="buttonText" style="width:24px;height:24px; margin: 0 8px 0 6px;"/>
        {{ buttonText }}
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

const TEXTS = {
  students: {
    singular: 'estudiante',
    plural: 'estudiantes'
  },
  tutors: {
    singular: 'tutor',
    plural: 'tutores'
  },
  companies: {
    singular: 'empresa',
    plural: 'empresas'
  }
}

export default {
  name: 'ActionBar',
  props: {
    kind: {
      type: String,
      default: 'students'
    }
  },
  data () {
    return {
      tab: '',
      course: '',
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
      selectedStatus: 'white'
    }
  },
  computed: {
    filterPlaceholder () {
      return `Nombre ${TEXTS[this.kind].singular}`
    },
    buttonText () {
      return `Añadir ${TEXTS[this.kind].plural}`
    }
  },
  methods: {
    emitStatus () {
      this.$emit('status-changed', this.selectedStatus)
    },
    addEntities () {
      // TODO: Implement popup
      console.log('Adding a new entity')
    }
  }
}
</script>

<style scoped>
@import url('../../css/ActionBar.css');
</style>
