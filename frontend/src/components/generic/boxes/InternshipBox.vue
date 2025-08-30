<template>
  <div class="company-box">
    <div class="box-body">
      <div class="identity-row">
        <input
          type="text"
          v-model="form.title"
          placeholder="Título práctica"
        />
        <select v-model="form.field" :class="{ 'is-placeholder': form.field === '' }" aria-label="Campo">
          <option value="">Campo</option> <!-- Used as a placeholder -->
          <option v-for="field in fields" :key="field.full_name" :value="field.full_name">{{ field.full_name }}</option>
        </select>
      </div>

      <div class="location-row">
        <input type="text" v-model="form.city" placeholder="Ciudad" aria-label="Ciudad" />
        <input type="text" v-model="form.pc" placeholder="CP" aria-label="Código Postal" />
        <input type="text" v-model="form.address" placeholder="Dirección" aria-label="Dirección" />
      </div>

      <div class="secondary">
        <div class="section-title">Información secundaria</div>
        <div class="internship-row">
          <select v-model="form.internshipType" :class="{ 'is-placeholder': form.internshipType === '' }" aria-label="Tipo de práctica">
            <option value="">Tipo de práctica</option> <!-- Used as a placeholder -->
            <option v-for="opt in internshipTypes" :key="opt" :value="opt">{{ capitalize(opt) }}</option>
          </select>
        </div>
        <div class="observations" style="height: 30vh">
          <textarea
            id="obs"
            v-model="form.description"
            rows="4"
            placeholder="Descripción"
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
  name: 'InternshipBox',
  props: {
    item: {
      type: Object,
      required: true
    },
    fields: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      form: this.mapItemToForm(this.item),
      internshipTypes: ['regular', 'dual', 'extraordinaria'],
      defaultIcon: IconUserDefault
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
          title: '',
          field: '',
          city: '',
          pc: '',
          address: '',
          internshipType: '',
          description: ''
        }
      }
      // Try to map common field names while keeping graceful fallbacks
      return {
        title: i.title || '',
        field: i.company ? i.company.field : '',
        city: i.location ? i.location.city : '',
        pc: i.location ? i.location.postal_code : '',
        address: i.location ? i.location.address : '',
        internshipType: i.kind || '',
        description: i.description || ''
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
