<script>
import {ref, reactive, onMounted, toRefs, watch, defineComponent, defineProps, defineEmits, computed } from "vue";
import EditorChild from "@/components/EditorChild"

import { ElCascader } from 'element-plus';
import {generateData, getData} from "@/api/editor";
export default defineComponent ({
  name: "TinyMce",
  components: {EditorChild, ElCascader},
  setup() {
    const editorValue = ref('<h1>test</h1>');
    let selectedOptions = reactive({selectedOptionData: []});
    let {selectedOptionData} = toRefs(selectedOptions)
    const optionsData = ref([
      {
        "value": "edit or Review",
        "label": "Edit or review",
        "children": [
              {"value": "improve writing", "label": "improve writing"},
              { "value": "make shorter", "label": "make shorter" },
              { "value": "simplify language", "label": "simplify language" }
            
        ]
      },
      {
        "value": "generate form selection",
        "label": "Generate form selection",
        "children": [
              {"value": "summarize", "label": "summarize"},
              { "value": "continue", "label": "continue" }
        ]
      },
      {
        "value": "change tone",
        "label": "Change tone",
        "children": [
              {"value": "profesional", "label": "profesional"},
              { "value": "casual", "label": "casual" },
              { "value": "direct", "label": "direct" },
              {"value": "confident", "label": "confident"},
              {"value": "friendly", "label": "friendly"}
            
        ]
      },
      {
        "value": "change style",
        "label": "Change style",
        "children": [
              {"value": "busuness", "label": "busuness"},
              { "value": "legal", "label": "legal" },
              { "value": "journalism", "label": "journalism" }
            
        ]
      },
      {
        "value": "translate",
        "label": "Translate",
        "children": [
            
              { "value": "translate to English", "label": "translate to English" },
              {"value": "translate to Tradionnal Chinese", "label": "translate to Tradionnal Chinese"},
              { "value": "translate to Simplified Chinese", "label": "translate to Simplified Chinese" },
              { "value": "translate to Japanese", "label": "translate to Japanese" }
            
            
        ]
      },
      // {
      //   "value": "change layout",
      //   "label": "Change layout",
      //   "children": [
      //         {"value": "papers", "label": "papers"},
      //         { "value": "press release", "label": "press release" },
      //         { "value": "blog", "label": "blog" }
            
      //   ]
      // }
    ])

    // watch
    watch(editorValue, (newValue) => {
      // console.log('watch2 parent ::',newValue);
    });
    
    // methods
    const handleChange = async (value) => {
      const arrData = [value[0], value[1]]
      const data = {
        work: arrData,
        content: editorValue.value
      }
      console.log(data, 'data::');
      try {
        const res = await generateData(data);
        console.log(res, 'res::');
        // const responseData = response.data;
        // console.log('API response:', responseData);

      } catch (error) {
        console.error('API error:', error);
      }
    };
 

    return {
      editorValue, selectedOptionData, handleChange, optionsData
    }
  }
});

</script>

<template>
  <div class="q-pt-lg q-px-lg">
    <div class="q-mb-xl">
      <!-- {{ selectedOptionData }} -->
      <!-- <ElCascader
        v-model="selectedOptionData"
        :options="optionsData"
        @change="handleChange"
        placeholder="Please select"
      ></ElCascader> -->
    </div>
    <EditorChild v-model="editorValue" :editorId="'gpt_editor'" />
  </div>
</template>