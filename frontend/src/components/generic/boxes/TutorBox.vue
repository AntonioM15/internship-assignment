<template>
  <div class="tutor-box">
    <div class="box-body">
      <div class="top-row">
        <div class="avatar">
          <img :src="defaultIcon" alt="Avatar" />
        </div>

        <div class="description">
          <textarea
            id="desc"
            v-model="form.description"
            rows="5"
            placeholder="Descripción tutor."
          />
        </div>
      </div>

      <div class="identity-row">
        <input
          type="text"
          v-model="form.fullName"
          placeholder="Nombre Apellido Apellido"
        />
        <input
          type="text"
          :value="degreesText"
          disabled
          aria-label="Titulación"
        />
      </div>

      <div class="location-row">
        <input type="text" v-model="form.city" placeholder="Ciudad" aria-label="Ciudad" />
        <input type="text" v-model="form.pc" placeholder="CP" aria-label="Código Postal" />
        <input type="text" v-model="form.address" placeholder="Dirección" aria-label="Dirección" />
      </div>

      <div class="secondary">
        <div class="section-title">Información secundaria</div>
        <div class="observations" style="height: 22vh">
          <textarea
            id="obs"
            v-model="form.notes"
            rows="4"
            placeholder="Observaciones"
          />
        </div>
      </div>
    </div>
    <div class="box-footer">
      <button class="btn ghost" @click="onHide">Ocultar</button>
      <div class="spacer"></div>
      <button class="btn secondary" @click="onCancel">Cancelar</button>
      <button class="btn primary" @click="onSave">Guardar</button>
    </div>
  </div>
</template>

<script>
import IconUserDefault from '../../../assets/IconUserDefault.svg'

export default {
  name: 'TutorBox',
  props: {
    item: {
      type: Object,
      required: true
    },
    degrees: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      form: this.mapItemToForm(this.item),
      defaultIcon: IconUserDefault
    }
  },
  computed: {
    degreesText () {
      const d = this.item && this.item.degrees
      const codes = Array.isArray(d) ? d.map(deg => deg && deg.code).filter(Boolean) : []
      return codes.join(', ')
    }
  },
  watch: {
    item: {
      deep: true,
      immediate: false,
      handler (val) {
        this.form = this.mapItemToForm(val)
      }
    }
  },
  methods: {
    mapItemToForm (i) {
      if (!i) {
        return {
          fullName: '',
          degree: '',
          city: '',
          pc: '',
          address: '',
          description: '',
          internshipType: '',
          notes: ''
        }
      }
      // Try to map common field names while keeping graceful fallbacks
      return {
        fullName: i.full_name || '',
        degree: i.degree || '',
        city: i.location ? i.location.city : '',
        pc: i.location ? i.location.postal_code : '',
        address: i.location ? i.location.address : '',
        description: i.description || '',
        internshipType: i.internship_type || '',
        notes: i.observations && i.observations.length > 0 ? i.observations[i.length - 1].text : ''
      }
    },
    onHide () {
      // TODO: implement hide functionality
      this.$emit('hide')
    },
    onCancel () {
      // Restore fields from the original item and notify parent
      this.form = this.mapItemToForm(this.item)
      this.$emit('cancel')
    },
    onSave () {
      // Emit an update with the edited data
      this.$emit('save', { ...this.form, id: this.item.id })
      // Also support v-model like flow
      this.$emit('input', { ...this.item, ...this.form })
    },
    capitalize (val) {
      return String(val).charAt(0).toUpperCase() + String(val).slice(1)
    }
  }
}
</script>

<style scoped>
@import url('../../../css/Boxes.css');
</style>
