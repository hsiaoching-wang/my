import { createRouter, createWebHistory } from "vue-router";
import TinyMce from "@/views/TinyMce.vue";

const routes = [
  {
    path: "/",
    name: "TinyMce",
    component: TinyMce,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
