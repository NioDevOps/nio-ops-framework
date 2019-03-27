<template>
  <div class="app-container">
    <div class="tree">
      <input class="tree-search-input" type="text" v-model.lazy="searchword" placeholder="search..."/>
      <button class=" tree-search-btn" type="button" @click="search">GO</button>
      <v-tree ref='tree' :data='treeData' :multiple="true" :tpl='tpl' :halfcheck='true'/>
    </div>
  </div>
</template>

<script>
import {getServiceTree} from '@/api/service'

export default {
  name: 'serviceTree',
  data() {
    return {
      treeData: [],
      searchword: '',
    }
  },
  created() {
    getServiceTree()
      .then(
        (r) => {
          this.treeData = r.data.tree
        }
      )
  },
  methods: {
    tpl(...args) {
      // let {0: node, 2: parent, 3: index } = args
      let { 0: node } = args
      let titleClass = node.selected ? 'node-title node-selected' : 'node-title'
      if (node.searched) titleClass += ' node-searched'
      return <span>
        <svg-icon icon-class="peoples" />
        <span class={titleClass} domPropsInnerHTML={node.title} ></span>
      </span>
    },
    search() {
      this.$refs.tree.searchNodes(this.searchword)
    }
  }
}
</script>

