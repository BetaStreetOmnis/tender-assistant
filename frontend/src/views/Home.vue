<template>
  <div class="home">
    <!-- 欢迎区域 -->
    <el-card class="welcome-card" shadow="hover">
      <div class="welcome-content">
        <div class="welcome-text">
          <h1>🎯 欢迎使用 AI 标书助理系统</h1>
          <p class="subtitle">
            基于DocuGen的智能投标文档生成平台，助力您高效完成投标工作
          </p>
          <div class="feature-tags">
            <el-tag type="success" effect="light">
              <el-icon><Check /></el-icon>
              招标文档智能分析
            </el-tag>
            <el-tag type="primary" effect="light">
              <el-icon><Document /></el-icon>
              投标大纲自动生成
            </el-tag>
            <el-tag type="warning" effect="light">
              <el-icon><Magic /></el-icon>
              完整文档AI生成
            </el-tag>
          </div>
        </div>
        <div class="welcome-actions">
          <el-button type="primary" size="large" @click="$router.push('/bidding/create')">
            <el-icon><Plus /></el-icon>
            创建投标
          </el-button>
          <el-button size="large" @click="$router.push('/templates')">
            <el-icon><FolderOpened /></el-icon>
            管理模板
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 快速操作卡片 -->
    <el-row :gutter="20" class="quick-actions">
      <el-col :span="6">
        <el-card class="action-card" shadow="hover" @click="$router.push('/analyze')">
          <div class="action-content">
            <el-icon class="action-icon" color="#409EFF"><Search /></el-icon>
            <h3>招标分析</h3>
            <p>智能分析招标文档，提取关键要点</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="action-card" shadow="hover" @click="$router.push('/generate')">
          <div class="action-content">
            <el-icon class="action-icon" color="#67C23A"><Magic /></el-icon>
            <h3>智能生成</h3>
            <p>基于大纲生成完整投标文档</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="action-card" shadow="hover" @click="$router.push('/templates')">
          <div class="action-content">
            <el-icon class="action-icon" color="#E6A23C"><FolderOpened /></el-icon>
            <h3>模板管理</h3>
            <p>上传和管理投标模板</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="action-card" shadow="hover" @click="$router.push('/dashboard')">
          <div class="action-content">
            <el-icon class="action-icon" color="#F56C6C"><DataAnalysis /></el-icon>
            <h3>数据统计</h3>
            <p>查看投标项目统计数据</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 系统状态 -->
    <el-card class="status-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>系统状态</span>
          <el-button type="text" @click="refreshStatus">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>

      <el-row :gutter="20" v-if="systemInfo">
        <el-col :span="8">
          <div class="status-item">
            <div class="status-label">系统版本</div>
            <div class="status-value">{{ systemInfo.version }}</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="status-item">
            <div class="status-label">运行状态</div>
            <div class="status-value">
              <el-tag :type="systemInfo.status === 'running' ? 'success' : 'danger'">
                {{ systemInfo.status === 'running' ? '正常运行' : '异常' }}
              </el-tag>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="status-item">
            <div class="status-label">可用功能</div>
            <div class="status-value">{{ systemInfo.features?.length || 0 }} 项</div>
          </div>
        </el-col>
      </el-row>

      <el-skeleton v-else :rows="3" animated />
    </el-card>

    <!-- 最新动态 -->
    <el-card class="recent-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>最新动态</span>
          <el-button type="text" @click="$router.push('/bidding')">
            查看全部
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
      </template>

      <div v-if="recentBids.length > 0">
        <div
          v-for="bid in recentBids"
          :key="bid.id"
          class="recent-item"
          @click="$router.push(`/bidding/${bid.id}`)"
        >
          <div class="recent-content">
            <h4>{{ bid.title }}</h4>
            <div class="recent-meta">
              <el-tag :type="getStatusType(bid.status)" size="small">
                {{ getStatusText(bid.status) }}
              </el-tag>
              <span class="recent-time">
                {{ formatDate(bid.created_at) }}
              </span>
            </div>
          </div>
          <el-icon class="recent-arrow"><ArrowRight /></el-icon>
        </div>
      </div>

      <el-empty v-else description="暂无投标项目" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { systemApi } from '@/api/system'
import { biddingApi } from '@/api/bidding'
import type { SystemInfo, BidResponse } from '@/types'

const systemInfo = ref<SystemInfo | null>(null)
const recentBids = ref<BidResponse[]>([])

// 获取系统信息
const getSystemInfo = async () => {
  try {
    const result = await systemApi.getSystemInfo()
    systemInfo.value = result.data
  } catch (error: any) {
    console.error('获取系统信息失败:', error)
  }
}

// 获取最新投标
const getRecentBids = async () => {
  try {
    const result = await biddingApi.getBidResponses({ page: 1, page_size: 5 })
    recentBids.value = result.data.items
  } catch (error: any) {
    console.error('获取最新投标失败:', error)
  }
}

// 刷新状态
const refreshStatus = async () => {
  try {
    const result = await systemApi.healthCheck()
    ElMessage.success(`系统状态: ${result.data.status}`)
    await getSystemInfo()
  } catch (error: any) {
    ElMessage.error(`系统检查失败: ${error.message}`)
  }
}

// 获取状态类型
const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    draft: 'info',
    in_progress: 'warning',
    completed: 'success',
    submitted: 'primary'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    draft: '草稿',
    in_progress: '进行中',
    completed: '已完成',
    submitted: '已提交'
  }
  return textMap[status] || status
}

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  getSystemInfo()
  getRecentBids()
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  margin-bottom: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-text h1 {
  margin: 0 0 12px 0;
  font-size: 28px;
  font-weight: bold;
}

.subtitle {
  margin: 0 0 20px 0;
  font-size: 16px;
  opacity: 0.9;
}

.feature-tags {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.feature-tags .el-tag {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
}

.welcome-actions {
  display: flex;
  gap: 16px;
}

.quick-actions {
  margin-bottom: 24px;
}

.action-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 180px;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.action-content {
  text-align: center;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.action-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.action-content h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: #303133;
}

.action-content p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.status-card,
.recent-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-item {
  text-align: center;
}

.status-label {
  color: #909399;
  font-size: 14px;
  margin-bottom: 8px;
}

.status-value {
  color: #303133;
  font-size: 16px;
  font-weight: 500;
}

.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.recent-item:hover {
  background-color: #f8f9fa;
}

.recent-item:last-child {
  border-bottom: none;
}

.recent-content h4 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 16px;
}

.recent-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.recent-time {
  color: #909399;
  font-size: 14px;
}

.recent-arrow {
  color: #c0c4cc;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    text-align: center;
    gap: 24px;
  }

  .quick-actions .el-col {
    margin-bottom: 16px;
  }

  .feature-tags {
    justify-content: center;
  }
}
</style>