<template>
  <div id="app">
    <!-- 布局组件 -->
    <el-container class="layout-container">
      <!-- 侧边栏 -->
      <el-aside width="240px" class="sidebar">
        <div class="logo">
          <h2>🎯 AI标书助理</h2>
        </div>

        <el-menu
          :default-active="$route.path"
          :router="true"
          class="sidebar-menu"
          text-color="#333"
          active-text-color="#409EFF"
          background-color="#f8f9fa"
        >
          <el-menu-item index="/">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>

          <el-menu-item index="/dashboard">
            <el-icon><DataAnalysis /></el-icon>
            <span>仪表板</span>
          </el-menu-item>

          <el-sub-menu index="/bidding">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>投标管理</span>
            </template>
            <el-menu-item index="/bidding">投标列表</el-menu-item>
            <el-menu-item index="/bidding/create">创建投标</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/templates">
            <template #title>
              <el-icon><FolderOpened /></el-icon>
              <span>模板管理</span>
            </template>
            <el-menu-item index="/templates">模板列表</el-menu-item>
            <el-menu-item index="/templates/create">上传模板</el-menu-item>
          </el-sub-menu>

          <el-menu-item index="/generate">
            <el-icon><Magic /></el-icon>
            <span>智能生成</span>
          </el-menu-item>

          <el-menu-item index="/analyze">
            <el-icon><Search /></el-icon>
            <span>招标分析</span>
          </el-menu-item>

          <el-menu-item index="/settings">
            <el-icon><Setting /></el-icon>
            <span>系统设置</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-container class="main-container">
        <!-- 顶部导航 -->
        <el-header class="header">
          <div class="header-left">
            <h3>{{ $route.meta.title || 'AI标书助理系统' }}</h3>
          </div>
          <div class="header-right">
            <el-button type="text" @click="checkSystemStatus">
              <el-icon><Refresh /></el-icon>
              系统状态
            </el-button>
          </div>
        </el-header>

        <!-- 主要内容 -->
        <el-main class="main-content">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>

    <!-- 全局加载状态 -->
    <el-loading
      v-if="globalLoading"
      :lock="true"
      text="加载中..."
      background="rgba(0, 0, 0, 0.7)"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { systemApi } from '@/api/system'

const globalLoading = ref(false)

// 检查系统状态
const checkSystemStatus = async () => {
  try {
    globalLoading.value = true
    const result = await systemApi.healthCheck()
    ElMessage.success(`系统状态: ${result.data.status}`)
  } catch (error: any) {
    ElMessage.error(`系统检查失败: ${error.message}`)
  } finally {
    globalLoading.value = false
  }
}

onMounted(() => {
  // 初始化时检查系统状态
  checkSystemStatus()
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: #f8f9fa;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #e4e7ed;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.logo h2 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.sidebar-menu {
  flex: 1;
  border-right: none;
}

.main-container {
  display: flex;
  flex-direction: column;
}

.header {
  background-color: white;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left h3 {
  margin: 0;
  color: #303133;
  font-weight: 500;
}

.main-content {
  flex: 1;
  padding: 24px;
  background-color: #f5f7fa;
  overflow-y: auto;
}

/* 路由过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    width: 200px !important;
  }

  .header {
    padding: 0 16px;
  }

  .main-content {
    padding: 16px;
  }
}
</style>