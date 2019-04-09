<template>
  <div class="app-container">
    <el-button
      @click="addNewStepDefine"
    >
      +
    </el-button>
    <diagram
      ref="diag"
      v-bind:model-data="diagramData"
      v-on:model-changed="modelChanged"
      v-on:changed-selection="changedSelection"
      style="border: solid 1px black; width:100%; height:400px">
    </diagram>
  </div>
</template>
<script>
  import diagram from './components/diagram'
  export default {
    name: "workflowDefine",
    components:{ diagram},
    data(){
      return {
        diagramData: {  // passed to <diagram> as its modelData
          class: "go.GraphLinksModel",
          copiesArrays: true,
          "copiesArrayObjects": true,
          nodeCategoryProperty: "type",
          linkFromPortIdProperty: "frompid",
          linkToPortIdProperty: "topid",
          nodeDataArray: [
            {"key":1, "type":"StepDefine", "name":"Product"},
            {"key":2, "type":"StepDefine", "name":"Product"},
            {"key":3, "type":"StepDefine", "name":"Product"},
          ],
          linkDataArray: [
            {"from":1, "frompid":"COMMIT", "to":2, "topid":"INPUT"},
            // { from: 1, to: 2 },
            // { from: 1, to: 3 },
            // { from: 3, to: 4 },
            // { from: 2, to: 4 },
            // { from: 4, to: 5 },
            // { from: 7, to: 5 },
            // { from: 8, to: 5 },

          ]
        }
      }
    },
    methods:{
      addNewStepDefine(){
        this.diagramData.nodeDataArray.push({"type": "StepDefine", "name": "New Step Define"})
      },
      modelChanged: function(e) {
        if (e.isTransactionFinished) {  // show the model data in the page's TextArea
          this.savedModelText = e.model.toJson();
        }
      },
      changedSelection: function(e) {
        var node = e.diagram.selection.first();
        if (node instanceof go.Node) {
          this.currentNode = node;
          this.currentNodeText = node.data.text;
        } else {
          this.currentNode = null;
          this.currentNodeText = "";
        }
      },
    }
  }
</script>
