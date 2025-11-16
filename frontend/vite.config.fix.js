import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    target: 'es2015',
    minify: false, // 禁用压缩以避免模块问题
    sourcemap: false,
    rollupOptions: {
      output: {
        // 手动分割，避免循环依赖
        manualChunks: {
          'element-plus': ['element-plus'],
          'vue-core': ['vue', 'vue-router'],
          'pinia': ['pinia'],
          'axios': ['axios']
        },
        // 确保格式兼容
        format: 'es',
        // 避免动态导入
        dynamicImportFunction: 'import'
      }
    }
  }
})
