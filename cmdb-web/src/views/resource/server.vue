<template>
  <div class="app-container">
    <ResourceTable
      :resourcetype="'Server'"
    ></ResourceTable>
  </div>
</template>

<script>
import ResourceTable from '@/views/table/resourceTable'

export default {
  name: 'Server',
  components:{ResourceTable},
  data() {
    return {}
  },
  created() {
  },
  methods: {
  }
}
</script>
