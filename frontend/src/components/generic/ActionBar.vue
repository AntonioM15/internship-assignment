<!-- src/components/ActionBar.vue -->
<template>
  <div class="action-bar">
    <div class="filters-section">
      <div class="filter-group" style="min-width: 400px;">
        <select class="filter-element"  style="width: 40%; min-width: 150px;" v-model="course" :class="{ 'is-placeholder': course === '' }">
          <option value="">Titulación</option> <!-- Used as a placeholder -->
          <option
            v-for="deg in degrees"
            :key="deg"
            :value="deg"
          >
            {{ deg.full_name }}
          </option>
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
      <button class="add-entity-btn" @click="addEntities">
        <img :src="iconAdd" :alt="buttonText" style="width:24px;height:24px; margin: 0 8px 0 6px;"/>
        {{ buttonText }}
      </button>
    </div>
    <!-- Popup mount -->
    <AddEntitiesPopUp
      v-if="showAddPopUp"
      :kind="kind"
      @cancel="showAddPopUp = false"
      @upload="onUploadCsv"
    />
  </div>
</template>

<script>

import IconAdd from '../../assets/IconAddLight.svg'
import IconStatusWhite from '../../assets/IconStatusWhite.svg'
import IconStatusBlue from '../../assets/IconStatusBlue.svg'
import IconStatusGreen from '../../assets/IconStatusGreen.svg'
import IconStatusRed from '../../assets/IconStatusRed.svg'
import IconStatusYellow from '../../assets/IconStatusYellow.svg'
import AddEntitiesPopUp from './popups/AddEntitiesPopUp.vue'

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
  components: {
    AddEntitiesPopUp
  },
  props: {
    kind: {
      type: String,
      default: 'students'
    },
    degrees: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      course: '',
      nameText: '',
      iconAdd: IconAdd,
      statusOptions: ['unknown', 'unassigned', 'provisional', 'assigned', 'ongoing'], // Deterministic order for the select
      statusIcons: {
        unknown: IconStatusWhite,
        unassigned: IconStatusRed,
        provisional: IconStatusYellow,
        assigned: IconStatusBlue,
        ongoing: IconStatusGreen
      },
      statusTexts: {
        unknown: 'Todos los estados',
        unassigned: 'Por asignar',
        provisional: 'Asignado - Por aprobar',
        assigned: 'Asignado - Aprobado',
        ongoing: 'Asignado - En curso'
      },
      selectedStatus: 'unknown', // When unknown include all the statuses - used as default value
      showAddPopUp: false
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
  watch: {
    course (val) {
      this.$emit('course-changed', val)
    },
    nameText (val) {
      this.$emit('nameText-changed', val)
    }
  },
  methods: {
    emitStatus () {
      this.$emit('status-changed', this.selectedStatus)
    },
    addEntities () {
      this.showAddPopUp = true
    },
    onUploadCsv (payload) {
      // Bubble the payload up so the page can handle parsing/uploading
      this.$emit('upload-csv', payload)
      this.showAddPopUp = false
    }
  }
}
</script>

<style scoped>
@import url('../../css/ActionBar.css');
</style>
