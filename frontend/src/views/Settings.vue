<template>
  <div class="settings">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>系统设置</h2>
    </div>

    <el-row :gutter="20">
      <!-- 系统信息 -->
      <el-col :span="12">
        <el-card class="settings-card" shadow="never">
          <template #header>
            <span>系统信息</span>
          </template>

          <div v-if="systemInfo" class="system-info">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="系统名称">
                {{ systemInfo.message }}
              </el-descriptions-item>
              <el-descriptions-item label="系统描述">
                {{ systemInfo.description }}
              </el-descriptions-item>
              <el-descriptions-item label="版本号">
                {{ systemInfo.version }}
              </el-descriptions-item>
              <el-descriptions-item label="运行状态">
                <el-tag :type="systemInfo.status === 'running' ? 'success' : 'danger'">
                  {{ systemInfo.status === 'running' ? '正常运行' : '异常' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="功能数量">
                {{ systemInfo.features?.length || 0 }} 项
              </el-descriptions-item>
            </el-descriptions>

            <div class="system-features">
              <h4>系统功能</h4>
              <div class="features-list">
                <el-tag
                  v-for="feature in systemInfo.features"
                  :key="feature"
                  type="info"
                  class="feature-tag"
                >
                  {{ feature }}
                </el-tag>
              </div>
            </div>
          </div>

          <el-skeleton v-else :rows="6" animated />
        </el-card>
      </el-col>

      <!-- 系统状态 -->
      <el-col :span="12">
        <el-card class="settings-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>系统状态</span>
              <el-button @click="checkHealth">
                <el-icon><Refresh /></el-icon>
                检查状态
              </el-button>
            </div>
          </template>

          <div v-if="healthStatus" class="health-status">
            <div class="status-item">
              <div class="status-icon">
                <el-icon size="32" color="#67C23A"><CircleCheck /></el-icon>
              </div>
              <div class="status-info">
                <div class="status-title">服务状态</div>
                <div class="status-value">{{ healthStatus.status }}</div>
              </div>
            </div>

            <div class="status-item">
              <div class="status-icon">
                <el-icon size="32" color="#409EFF"><Server /></el-icon>
              </div>
              <div class="status-info">
                <div class="status-title">服务名称</div>
                <div class="status-value">{{ healthStatus.service }}</div>
              </div>
            </div>

            <div class="status-item">
              <div class="status-icon">
                <el-icon size="32" color="#E6A23C"><Timer /></el-icon>
              </div>
              <div class="status-info">
                <div class="status-title">检查时间</div>
                <div class="status-value">{{ lastCheckTime }}</div>
              </div>
            </div>
          </div>

          <el-empty v-else description="尚未进行健康检查" />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <!-- API端点 -->
      <el-col :span="12">
        <el-card class="settings-card" shadow="never">
          <template #header>
            <span>API端点</span>
          </template>

          <div v-if="systemInfo" class="api-endpoints">
            <div class="endpoint-item">
              <div class="endpoint-label">演示接口</div>
              <el-input
                :value="getFullUrl(systemInfo.endpoints.demo)"
                readonly
                class="endpoint-input"
              >
                <template #append>
                  <el-button @click="copyUrl(getFullUrl(systemInfo.endpoints.demo))">
                    <el-icon><CopyDocument /></el-icon>
                  </el-button>
                </template>
              </el-input>
            </div>

            <div class="endpoint-item">
              <div class="endpoint-label">模板接口</div>
              <el-input
                :value="getFullUrl(systemInfo.endpoints.templates)"
                readonly
                class="endpoint-input"
              >
                <template #append>
                  <el-button @click="copyUrl(getFullUrl(systemInfo.endpoints.templates))">
                    <el-icon><CopyDocument /></el-icon>
                  </el-button>
                </template>
              </el-input>
            </div>

            <div class="endpoint-item">
              <div class="endpoint-label">分析接口</div>
              <el-input
                :value="getFullUrl(systemInfo.endpoints.analyze)"
                readonly
                class="endpoint-input"
              >
                <template #append>
                  <el-button @click="copyUrl(getFullUrl(systemInfo.endpoints.analyze))">
                    <el-icon><CopyDocument /></el-icon>
                  </el-button>
                </template>
              </el-input>
            </div>

            <div class="endpoint-item">
              <div class="endpoint-label">API文档</div>
              <el-input
                :value="getFullUrl(systemInfo.endpoints.docs)"
                readonly
                class="endpoint-input"
              >
                <template #append>
                  <el-button @click="copyUrl(getFullUrl(systemInfo.endpoints.docs))">
                    <el-icon><CopyDocument /></el-icon>
                  </el-button>
                </template>
              </el-input>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 快捷操作 -->
      <el-col :span="12">
        <el-card class="settings-card" shadow="never">
          <template #header>
            <span>快捷操作</span>
          </template>

          <div class="quick-operations">
            <div class="operation-item" @click="openApiDocs">
              <el-icon size="24" color="#409EFF"><Document /></el-icon>
              <div class="operation-info">
                <div class="operation-title">API文档</div>
                <div class="operation-desc">查看完整的API文档</div>
              </div>
            </div>

            <div class="operation-item" @click="exportSystemInfo">
              <el-icon size="24" color="#67C23A"><Download /></el-icon>
              <div class="operation-info">
                <div class="operation-title">导出系统信息</div>
                <div class="operation-desc">下载系统配置信息</div>
              </div>
            </div>

            <div class="operation-item" @click="clearCache">
              <el-icon size="24" color="#E6A23C"><Delete /></el-icon>
              <div class="operation-info">
                <div class="operation-title">清除缓存</div>
                <div class="operation-desc">清理浏览器缓存数据</div>
              </div>
            </div>

            <div class="operation-item" @click="refreshAllData">
              <el-icon size="24" color="#F56C6C"><Refresh /></el-icon>
              <div class="operation-info">
                <div class="operation-title">刷新数据</div>
                <div class="operation-desc">重新加载所有数据</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { systemApi } from '@/api/system'
import { useBiddingStore } from '@/stores/bidding'
import { useTemplateStore } from '@/stores/template'

const biddingStore = useBiddingStore()
const templateStore = useTemplateStore()

const systemInfo = ref<any>(null)
const healthStatus = ref<any>(null)
const lastCheckTime = ref('')

// 获取系统信息
const getSystemInfo = async () => {
  try {
    const result = await systemApi.getSystemInfo()
    systemInfo.value = result.data
  } catch (error: any) {
    ElMessage.error(`获取系统信息失败: ${error.message}`)
  }
}

// 检查健康状态
const checkHealth = async () => {
  try {
    const result = await systemApi.healthCheck()
    healthStatus.value = result.data
    lastCheckTime.value = new Date().toLocaleString('zh-CN')
    ElMessage.success('健康检查完成')
  } catch (error: any) {
    ElMessage.error(`健康检查失败: ${error.message}`)
  }
}

// 获取完整URL
const getFullUrl = (endpoint: string) => {
  const baseUrl = window.location.origin
  return `${baseUrl}/api/v1${endpoint}`
}

// 复制URL
const copyUrl = async (url: string) => {
  try {
    await navigator.clipboard.writeText(url)
    ElMessage.success('URL已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

// 打开API文档
const openApiDocs = () => {
  window.open('/docs', '_blank')
}

// 导出系统信息
const exportSystemInfo = () => {
  const data = {
    systemInfo: systemInfo.value,
    healthStatus: healthStatus.value,
    exportTime: new Date().toISOString()
  }

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `系��信息_${new Date().toLocaleDateString('zh-CN')}.json`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)

  ElMessage.success('系统信息已导出')
}

// 清除缓存
const clearCache = () => {
  localStorage.clear()
  sessionStorage.clear()

  // 清除Pinia状态
  biddingStore.reset()
  templateStore.reset()

  ElMessage.success('缓存已清除，请刷新页面')
}

// 刷新所有数据
const refreshAllData = async () => {
  try {
    ElMessage.info('正在刷新数据...')

    await Promise.all([
      getSystemInfo(),
      checkHealth(),
      biddingStore.fetchBidResponses(),
      templateStore.fetchTemplates()
    ])

    ElMessage.success('数据刷新完成')
  } catch (error: any) {
    ElMessage.error(`刷新数据失败: ${error.message}`)
  }
}

onMounted(() => {
  getSystemInfo()
  checkHealth()
})
</script>

<style scoped>
.settings {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.system-info {
  margin-bottom: 20px;
}

.system-features {
  margin-top: 20px;
}

.system-features h4 {
  margin: 0 0 12px 0;
  color: #303133;
}

.features-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.feature-tag {
  margin-bottom: 8px;
}

.health-status {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.status-info {
  flex: 1;
}

.status-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 4px;
}

.status-value {
  font-size: 16px;
  color: #303133;
  font-weight: 500;
}

.api-endpoints {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.endpoint-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.endpoint-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.endpoint-input {
  font-family: 'Courier New', monospace;
}

.quick-operations {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.operation-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.operation-item:hover {
  background-color: #e9ecef;
  transform: translateX(4px);
}

.operation-info {
  flex: 1;
}

.operation-title {
  font-size: 16px;
  color: #303133;
  font-weight: 500;
  margin-bottom: 4px;
}

.operation-desc {
  font-size: 14px;
  color: #909399;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .settings .el-col {
    margin-bottom: 20px;
  }
}
</style>