import { fileURLToPath, URL } from 'node:url' // 导入 node:url 模块中的 fileURLToPath 和 URL 方法

import { defineConfig } from 'vite' // 导入 vite 库中的 defineConfig 方法
import vue from '@vitejs/plugin-vue' // 导入 vite 插件库中的 vue 插件

// https://vitejs.dev/config/
export default defineConfig({
  define: {
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'true' // 定义 Vue 生产环境下 SSR 不一致性检查的特性标志为 true
  },
  plugins: [vue()], // 使用 Vue 插件
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)) // 设置别名 '@'，指向项目的 src 目录
    }
  },
  server: {
    host: '0.0.0.0', // 设置服务器主机为本地所有可用的 IPv4 地址
    port: 80 // 设置服务器端口为 80
  }
})
