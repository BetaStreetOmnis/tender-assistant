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
    minify: 'esbuild', // 使用esbuild而不是terser，减少变量名冲突
    sourcemap: false,
    rollupOptions: {
      output: {
        // 手动分割chunk，避免循环依赖
        manualChunks(id) {
          // 将大型库单独打包
          if (id.includes('node_modules')) {
            if (id.includes('element-plus')) {
              return 'element-plus'
            }
            if (id.includes('vue')) {
              return 'vue-vendor'
            }
            if (id.includes('axios')) {
              return 'axios'
            }
            if (id.includes('pinia')) {
              return 'pinia'
            }
            if (id.includes('vue-router')) {
              return 'vue-router'
            }
            return 'vendor'
          }
          // 应用代码
          if (id.includes('src')) {
            if (id.includes('views/Dashboard')) {
              return 'dashboard'
            }
            if (id.includes('views/Bidding')) {
              return 'bidding'
            }
            if (id.includes('views/Templates')) {
              return 'templates'
            }
            if (id.includes('views/Analyze')) {
              return 'analyze'
            }
            if (id.includes('views/Generate')) {
              return 'generate'
            }
            if (id.includes('views/Settings')) {
              return 'settings'
            }
          }
        },
        // 确保输出格式
        format: 'es',
        // 优化chunk大小警告
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    },
    // 优化构建选项
    chunkSizeWarningLimit: 1000,
    // 确保外部依赖不被打包
    external: [],
    // 启用代码分割
    dynamicImportVarsOptions: {
      exclude: []
    }
  },
  // 确保全局变量可用
  define: {
    'process.env.NODE_ENV': JSON.stringify('production')
  }
})