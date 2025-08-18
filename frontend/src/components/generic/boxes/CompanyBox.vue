<template>
  <div class="company-box">
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
            placeholder="Descripción empresa"
          />
        </div>
      </div>

      <div class="identity-row">
        <input
          type="text"
          v-model="form.fullName"
          placeholder="Nombre Empresa"
        />
        <select v-model="form.field" :class="{ 'is-placeholder': form.field === '' }" aria-label="Campo">
          <option value="">Campo</option> <!-- Used as a placeholder -->
          <option v-for="field in fields" :key="field" :value="field">{{ field }}</option>
        </select>
      </div>

      <div class="location-row">
        <input type="text" v-model="form.city" placeholder="Ciudad" aria-label="Ciudad" />
        <input type="text" v-model="form.cp" placeholder="CP" aria-label="Código Postal" />
        <input type="text" v-model="form.address" placeholder="Dirección" aria-label="Dirección" />
      </div>

      <div class="secondary">
        <div class="section-title">Información secundaria</div>
        <div class="observations" style="height: 25vh">
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
  name: 'StudentBox',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      form: this.mapItemToForm(this.item),
      // TODO - Fetch from backend
      fields: ['Programación', 'Electrónica', 'Mecánica'],
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
          fullName: '',
          field: '',
          city: '',
          cp: '',
          address: '',
          description: '',
          notes: ''
        }
      }
      // Try to map common field names while keeping graceful fallbacks
      return {
        fullName:  i.full_name || '',
        field: i.field || '',
        // TODO location needs to be improved in to json methods
        city: '',
        cp: '',
        address: '',
        // TODO descriptions
        description: '',
        // TODO notes (observations) needs to be improved in to json methods
        notes: ''
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
    }
  }
}
</script>

<style scoped>
@import url('../../../css/Boxes.css');
</style>
