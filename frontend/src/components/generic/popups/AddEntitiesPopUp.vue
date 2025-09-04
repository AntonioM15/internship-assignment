<template>
  <div class="modal-overlay" @click.self="emitCancel">
    <div class="modal-window" style="width: max(1000px, 35vw); height: max(550px, 50vh);">
      <div class="modal-columns" style="grid-template-columns: 1fr; height: max(400px, 35vh);">
        <!-- Example -->
        <section style="text-align:center;">
          <div class="title">Ejemplo de CSV válido - {{ kindLabel }}</div>
          <pre class="example-text">{{ sampleCsv }}</pre>
        </section>

        <!-- File input -->
        <section style="text-align:center; padding-top: 40px;">
          <div class="title">Selecciona el archivo</div>
          <input
            ref="fileInput"
            type="file"
            accept=".csv,text/csv"
            @change="onFileChange"
            style="display:none"
          />
          <div class="icon-box"
            @click="triggerBrowse"
            style="cursor:pointer; user-select:none; margin-top:10px;"
          >
            <img
              :alt="selectedFile ? 'Archivo seleccionado' : 'Subir CSV'"
              :src="selectedFile ? fileAddedIcon : placeholderIcon"
            />
          </div>
          <div v-if="!selectedFile" class="subtitle">
            {{ 'Haz clic para elegir un archivo .csv' }}
          </div>
          <div v-if="selectedFile" class="subtitle" style="color: var(--text-primary-color);">
            {{ selectedFile.name }}
          </div>

          <div v-if="fileError" class="error-text">
            {{ fileError }}
          </div>
        </section>
      </div>

      <div class="modal-actions">
        <div class="spacer"></div>
        <button class="btn" @click="emitCancel">Cancelar</button>
        <button class="btn" :disabled="!selectedFile" @click="emitUpload">Subir</button>
      </div>
    </div>
  </div>
</template>

<script>
import IconAddEntities from '../../../assets/IconAddEntities.svg'
import IconFileAdded from '../../../assets/IconFileAdded.svg'

export default {
  name: 'AddEntitiesPopUp',
  props: {
    kind: {
      type: String,
      default: 'students'
    }
  },
  data () {
    return {
      selectedFile: null,
      fileError: '',
      placeholderIcon: IconAddEntities,
      fileAddedIcon: IconFileAdded,
      examples: {
        students: {
          headers: ['official_id', 'full_name', 'email', 'degree', 'internship_type', 'description'],
          rows: [
            ['12345678A', 'Ana Pérez', 'ana.perez@example.com', 'PRG', 'regular', 'Experiencia en Python'],
            ['12345679B', 'Luis Gómez', 'luis.gomez@example.com', 'RED', 'regular', 'Interés por las plataformas de la nube']
          ]
        },
        tutors: {
          headers: ['official_id', 'full_name', 'email', 'degrees', 'description'],
          rows: [
            ['12345678A', 'María López', 'maria.lopez@example.com', 'PRG; ALG', 'Preferencia por prácticas de programación'],
            ['12345679B', 'Jorge Ruiz', 'jorge.ruiz@example.com', 'RED; SEC', 'No dispone de coche']
          ]
        },
        companies: {
          headers: ['full_name', 'email', 'field', 'description'],
          rows: [
            ['Tech Corp', 'contact@techcorp.example', 'PRG', 'Prácticas anteriores satisfactorias'],
            ['DataSoft', 'hr@datasoft.example', 'RED', 'Posibilidad de oferta tras práctica']
          ]
        }
      }
    }
  },
  computed: {
    example () {
      return this.examples[this.kind] || this.examples.students
    },
    sampleCsv () {
      const h = this.example.headers.join(',')
      const r = this.example.rows.map(row => row.map(this.escapeCsv).join(',')).join('\n')
      return `${h}\n${r}`
    },
    kindLabel () {
      switch (this.kind) {
        case 'students': return 'Estudiantes'
        case 'tutors': return 'Tutores'
        case 'companies': return 'Empresas'
        default: return this.kind
      }
    }
  },
  mounted () {
    window.addEventListener('keydown', this.onKeydown)
  },
  beforeDestroy () {
    window.removeEventListener('keydown', this.onKeydown)
  },
  methods: {
    onKeydown (e) {
      if (e.key === 'Escape') this.emitCancel()
    },
    emitCancel () {
      this.$emit('cancel')
    },
    triggerBrowse () {
      this.$refs.fileInput && this.$refs.fileInput.click()
    },
    onFileChange (e) {
      this.fileError = ''
      const file = e.target.files && e.target.files[0]
      if (!file) {
        this.selectedFile = null
        return
      }
      // Basic validation
      const isCsv = /\.csv$/i.test(file.name) || file.type === 'text/csv'
      if (!isCsv) {
        this.fileError = 'El archivo debe ser .csv'
        this.selectedFile = null
        return
      }
      this.selectedFile = file
    },
    emitUpload () {
      if (!this.selectedFile) {
        this.fileError = 'Selecciona un archivo antes de continuar'
        return
      }
      // Emit file and kind so parent can handle parsing/uploading
      this.$emit('upload', { file: this.selectedFile, kind: this.kind })
    },
    escapeCsv (value) {
      const s = String(value == null ? '' : value)
      if (/[",\n]/.test(s)) {
        return `"${s.replace(/"/g, '""')}"`
      }
      return s
    }
  }
}
</script>

<style scoped>
@import url('../../../css/PopUps.css');

</style>
