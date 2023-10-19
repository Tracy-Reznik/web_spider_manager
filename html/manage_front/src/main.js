import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import * as Elicons from '@element-plus/icons-vue';
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from "./router/index.js"




const app=createApp(App)
app.use(router)
app.use(ElementPlus)
Object.keys(Elicons).forEach((key) => {
    app.component(key, Elicons[key]);
});
app.mount('#app')

