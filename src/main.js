import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { Quasar } from "quasar";
import quasarUserOptions from "./quasar-user-options";

// element-plus
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

createApp(App)
  .use(Quasar, quasarUserOptions)
  .use(ElementPlus)
  .use(store)
  .use(router)
  .mount("#app");
