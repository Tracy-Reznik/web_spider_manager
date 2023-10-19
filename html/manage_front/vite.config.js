import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import ElementPlus from "element-plus";


// https://vitejs.dev/config/
export default defineConfig({
build: {
    rollupOptions: {
      output: {
      	// 在这里修改静态资源路径
        chunkFileNames: 'static/assets/js/[name]-[hash].js',
        entryFileNames: 'static/assets/js/[name]-[hash].js',
        assetFileNames: 'static/assets/[ext]/[name]-[hash].[ext]',
      }
    }
  },
  plugins: [
      vue(),
      AutoImport({
          resolvers: [ElementPlusResolver()],
      }),
      Components({
          resolvers: [ElementPlusResolver()],
      }),
  ],
})
