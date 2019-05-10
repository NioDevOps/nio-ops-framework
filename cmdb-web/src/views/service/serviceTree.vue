<template>
  <div class="app-container">
    <ServiceDlg
      ref="dlg"
      @callback="load"
    />
    <div class="tree">
      <el-row type="flex">
        <el-input
          v-model.lazy="searchword"
          span="6"
          placeholder="search..."
          @keyup.enter="search"
        />
        <!--        <el-button-->
        <!--          icon="el-icon-search"-->
        <!--          @click="search"-->
        <!--          circle>-->
        <!--        </el-button>-->
        <el-button
          type="primary"
          round
          @click="openCreateDlg(null)"
        >
          new root
        </el-button>
      </el-row>
      <v-tree ref="tree" :data="treeData" :multiple="true" :tpl="tpl" :halfcheck="true" />
    </div>
  </div>
</template>

<script>
import { getServiceTree } from '@/api/service'
import ServiceDlg from './serviceDLg'

export default {
  name: 'ServiceTree',
  components: { ServiceDlg },
  data() {
    return {
      treeData: [],
      searchword: ''
    }
  },
  created() {
    this.load()
  },
  methods: {
    tpl(...args) {
      // let {0: node, 2: parent, 3: index } = args
      const { 0: node } = args
      let titleClass = node.selected ? 'node-title node-selected' : 'node-title'
      if (node.searched) titleClass += ' node-searched'
      return <span>
        <svg-icon icon-class='peoples' />
        <span class={titleClass} domPropsInnerHTML={node.title} ></span>
        <el-button size='mini' onClick={ () => this.openCreateDlg(node.id)}> add </el-button>
      </span>
    },
    search() {
      this.$refs.tree.searchNodes(this.searchword)
    },
    openCreateDlg(n) {
      this.$refs.dlg.open_dlg(null, n)
    },
    load() {
      getServiceTree()
        .then(
          (r) => {
            this.treeData = r.data.tree
          }
        )
    }
  }
}
</script>

