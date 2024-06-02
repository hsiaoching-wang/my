<script>
import axios from 'axios';
import {ref, reactive, onMounted, onBeforeUnmount, toRefs, watch, defineComponent } from "vue";

import {generateData, enter2Data, getData} from "@/api/editor";
import { ElCascader, ElDialog } from 'element-plus';
// ==== tinymce ====

import Editor from "@tinymce/tinymce-vue";
import tinymce from 'tinymce/tinymce.js'

import 'tinymce/skins/ui/oxide/skin.css'
import 'tinymce/themes/silver'

// Icon
import 'tinymce/icons/default'

// 用到的外掛
import 'tinymce/plugins/emoticons';
import 'tinymce/plugins/emoticons/js/emojis.js';
import 'tinymce/plugins/table';
import 'tinymce/plugins/quickbars';
import 'tinymce/plugins/image'; // 新增 image 插件
import 'tinymce/plugins/imagetools';
import 'tinymce/plugins/paste';

import imgAssistant from "@/assets/icon/assistant.svg";
import {editIcon, RobotIcon2} from "@/shared/svg";

export default defineComponent ({
  name: "EditorChild",
  props: {
    editorId: {
      type: String,
      required: true,
    },
    modelValue: {
      type: String,
      required: true,
    },
    plugins: {
      type: [String, Array],
      default: 'quickbars emoticons image imagetools table paste',
    },
    toolbar: {
    type: [String, Array],
    default:
      ' editButton | robotButton | bold italic underline strikethrough | fontsizeselect | forecolor backcolor | alignleft aligncenter alignright alignjustify|bullist numlist |outdent indent blockquote | undo redo | axupimgs | removeformat | table | insertfile  | image |emoticons',
  },
  },
  emits: ['update:modelValue'],
  components: {Editor, ElCascader, ElDialog },
  setup(props, { emit }) {

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


    const { modelValue, editorId } = toRefs(props);
    const content = ref(modelValue.value);
    const tinymceId = ref(editorId.value);

    const gptDialog = ref(false)
    const gptAskDialog = ref(false)
    const autoLayoutDialog = ref(false)
    const cascaderDialog = ref(false)

    const imgAssistantRef = ref(imgAssistant)
    const resInputText = ref('')
    const askInputText = ref('')
    let fileModel = reactive({fileData: []})
    let {fileData} = toRefs(fileModel)
    const toggleVal = ref(false)

    let testData = reactive({data: null})
    let {data} = toRefs(testData)

    const init = reactive({
      // language: 'zh_TW',
      height: 500,
      menubar: true,
      content_css: false, //若true 會出現引入路徑錯誤
      skin: false, //若true 會出現引入路徑錯誤
      plugins: props.plugins,
      toolbar: props.toolbar,
      quickbars_insert_toolbar: false,
      branding: false,

      paste_data_images: true, // 启用粘贴图片功能
      automatic_uploads: true, // 自动上传
      // images_upload_handler: async (blobInfo, success, failure) => {
      //   try {
      //     const formData = new FormData();
      //     formData.append('file', blobInfo.blob(), blobInfo.filename());

      //     const response = await fetch('http://localhost:3000/upload', {
      //       method: 'POST',
      //       body: formData,
      //     });

      //     if (!response.ok) {
      //       throw new Error(`HTTP error! status: ${response.status}`);
      //     }

      //     const json = await response.json();

      //     if (!json || typeof json.location !== 'string') {
      //       throw new Error(`Invalid JSON: ${JSON.stringify(json)}`);
      //     }

      //     success(json.location);
      //   } catch (error) {
      //     failure(`Image upload failed: ${error.message}`);
      //   }
      // },
      setup: (editor) => {
        editor.on('keydown', (event) => {
          if (toggleVal.value == true && event.key === 'Enter') {
            getNewDataFromGPT(content.value);
            // emit('onEnterPress', content.value);
          }
        });

        // 处理粘贴和拖放
        editor.on('drop', (e) => {
          const items = (e.dataTransfer && e.dataTransfer.files) || [];
          if (items.length) {
            e.preventDefault();
            const file = items[0];
            const reader = new FileReader();
            reader.onload = (event) => {
              const base64 = event.target.result;
              // 将图片插入到编辑器
              editor.insertContent(`<img src="${base64}" />`);
            };
            reader.readAsDataURL(file);
          }
        });


        // editor.on('paste', (e) => {
        //   const clipboardData = e.clipboardData || window.clipboardData;
        //   const items = clipboardData.items || [];
        //   for (const item of items) {
        //     if (item.type.indexOf('image') !== -1) {
        //       const file = item.getAsFile();
        //       const reader = new FileReader();
        //       reader.onload = (event) => {
        //         const base64 = event.target.result;
        //         // 将图片插入到编辑器
        //         editor.insertContent(`<img src="${base64}" />`);
        //       };
        //       reader.readAsDataURL(file);
        //       e.preventDefault();
        //     }
        //   }
        // });

        editor.ui.registry.addButton('editButton', {
          icon: 'edit-icon',
          onAction: () => {
            console.log('onAction');
          }
        });
        editor.ui.registry.addButton('robotButton', {
          icon: 'robot-icon',
          onAction: () => {
            console.log('onAction');
          }
        });

        editor.ui.registry.addIcon('edit-icon', editIcon);
        editor.ui.registry.addIcon('robot-icon', RobotIcon2);
      }
    });
    // https://vue-lessons-api.vercel.app/courses/list
    const getNewDataFromGPT = async (content) => {
      const url = `https://vue-lessons-api.vercel.app/courses/list`
      // const res = await axios.get(url)
      // console.log(res, 'res::');
      // testData.data = res.data

      try {
        const data = {
          format: 'blog',
          sentence: content
        }
        console.log(data, 'data::');
        const res = await enter2Data(data);
        console.log(res, 'res::');
        // const responseData = response.data;
        // console.log('API response:', responseData);

      } catch (error) {
        console.error('API error:', error);
      }
    };

    const openDialog = () => {
      gptDialog.value = true
    }

    const handleChange = async (value) => {
      const arrData = [value[0], value[1]]
      const data = {
        work: arrData,
        content: content.value
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



    watch(content, (newValue) => {
      // console.log('watch1:', newValue)
      emit('update:modelValue', newValue);
    });
    
    watch(modelValue, (newValue) => {
      // console.log('watch3:', newValue)
      content.value = newValue;
    });

    onMounted(() => {
      tinymce.init({})
    })

    return {
      content, init, tinymceId, data, gptDialog, gptAskDialog, autoLayoutDialog, cascaderDialog, openDialog, imgAssistant: imgAssistantRef, resInputText, askInputText, fileData, toggleVal, selectedOptionData, optionsData, handleChange
    }
  }
});
</script>
<template>
<div>

  <!-- {{ content }} -->

    <!-- {{ data }} -->
  <div class="flex">
    <q-toggle v-model="toggleVal" label="Activate AI" />
  </div>
  <Editor
      :id="tinymceId"
      v-model="content"
      :init="init"
      ref="editor"
    ></Editor>

    <!-- 跳窗 -Cascader -->
    <el-dialog v-model="cascaderDialog" style="width: 70vw; height: 60vh">
    <p>这是一个基本的弹窗。</p>
      <ElCascader
          v-model="selectedOptionData"
          :options="optionsData"
          @change="handleChange"
          placeholder="Please select"
        ></ElCascader>
    </el-dialog>

    <!-- 跳窗 -AI Auto Layout -->
    <q-dialog v-model="autoLayoutDialog">
      <q-card class="q-pa-md" style="width: 80vw;">
        <div class="flex items-center">
          <img class="q-mr-md" :src="imgAssistant" />
          <div class="fz-larger text-weight-bold q-my-md">Auto Layout</div>
        </div>
        <p>
          Can keep writing without changing any style
        </p>
        <div class="flex q-mb-md">
          <q-file outlined v-model="fileData" dense class="q-mr-md" style="flex: 1 0 auto">
            <template v-slot:prepend>
              <q-icon name="attach_file" />
            </template>
          </q-file>
          <q-btn label="send" color="primary" />
        </div>
        </q-card>
    </q-dialog>

    <!-- 跳窗 -AI 詢問 -->
    <q-dialog v-model="gptAskDialog">
      <q-card class="q-pa-md" style="width: 80vw;">
        <div class="flex items-center">
          <img class="q-mr-md" :src="imgAssistant" />
          <div class="fz-larger text-weight-bold q-my-md">AI Assistant</div>
        </div>
        <div class="flex">
          <q-input
              style="flex: 1 0 auto"
              class="q-mr-md"
              outlined
              v-model="askInputText"
              type="test"
            />
            <q-btn label="send" color="primary" />
        </div>
        </q-card>
    </q-dialog>

    <!-- 跳窗 -AI 回傳 + 詢問 -->
    <q-dialog v-model="gptDialog">
      <q-card class="q-pa-md" style="max-width: 60vw;">

        <div class="flex items-center">
          <img class="q-mr-md" :src="imgAssistant" />
          <div class="fz-larger text-weight-bold q-my-md">AI Assistant</div>
        </div>
        <div>
          <q-input
            outlined
            :input-style="{ width: '100vw', height: '50VH' }"
            v-model="resInputText"
            type="textarea"
            maxlength="999"
          />
        </div>
        <div class="flex q-py-md">
          <q-btn class="q-mr-md" label="replace" color="primary" />
          <q-btn class="q-mr-md" flat label="insert below" color="dark" />
          <q-btn class="q-mr-md" flat label="try again" color="dark" />
          <q-btn class="q-mr-md" flat label="stop" color="grey" />
        </div>
        <div class="flex">
          <q-input
              style="flex: 1 0 auto"
              class="q-mr-md"
              outlined
              v-model="askInputText"
              type="test"
            />
            <q-btn label="send" color="primary" />
        </div>
      </q-card>
    </q-dialog>
</div>
</template>
<style lang="scss" scoped>

</style>