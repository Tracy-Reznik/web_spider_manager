//导入createRouter和createWebHashHistory
import {createRouter,createWebHashHistory} from 'vue-router'
import Home from "../components/Home.vue";
const router = createRouter({
    history: createWebHashHistory(),
    //路由列表，由对象数组组成，每个对象由若干选项组成
    routes: [
        {
            path: '/',
            component: Home
        },
    ]
})
export default router