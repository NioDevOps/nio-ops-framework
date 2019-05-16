<template>
  <el-dialog title="Service" :visible.sync="open">
    <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="Name" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="resourcetype" prop="resourcetype">
        <el-select v-model="form.resourcetype">
          <el-option value="NormalService">NormalService</el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Info" prop="info">
        <el-input v-model="form.info" type="textarea" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submit">立即创建</el-button>
        <el-button @click="close_dlg">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<script>
import { postService } from '@/api/service'

export default {
  name: 'ServiceDlg',
  props: {
    mode: { type: String, default: 'create' },
    callback: { type: Function, default: () => {} }
  },
  data() {
    return {
      service_type: 'NormalService',
      create_mode: 'create',
      open: false,
      form: {},
      rules: {
        name: [
          { required: true, trigger: 'blur' }
        ],
        info: [
          { required: true, trigger: 'blur' }
        ]
      }
    }
  },
  created() {
  },
  methods: {
    submit() {
      this.$refs.form.validate(
        (valid) => {
          if (valid) {
            if (this.mode === 'create') {
              this.create()
            }
          } else {
            return false
          }
        }
      )
    },
    create() {
      postService(this.form)
        .then(
          (resp) => {
            this.$message.success('success')
            this.$emit('callback', resp)
            this.close_dlg(resp)
          }
        )
        .catch(
          (e) => {
            console.log(e)
            this.$message.error(e)
          }
        )
    },
    close_dlg() {
      this.open = false
      this.form = {}
    },
    open_dlg(service, parent) {
      if (service != null) {
        this.form = service
      } else if (this.mode === this.create_mode) {
        this.form.parent = parent
      }
      this.open = true
    }
  }
}
</script>
