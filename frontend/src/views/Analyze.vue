<template>
  <div class="analyze">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>招标文档分析</h2>
    </div>

    <el-row :gutter="20">
      <!-- 左侧：输入区域 -->
      <el-col :span="12">
        <el-card class="input-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>招标文档内容</span>
              <el-upload
                :auto-upload="false"
                :on-change="handleFileUpload"
                :show-file-list="false"
                accept=".txt,.doc,.docx"
              >
                <el-button type="primary" size="small">
                  <el-icon><Upload /></el-icon>
                  上传文档
                </el-button>
              </el-upload>
            </div>
          </template>

          <div class="input-content">
            <el-input
              v-model="tenderContent"
              type="textarea"
              :rows="20"
              placeholder="请输入招标文档内容，或点击上方按钮上传文档..."
              show-word-limit
              maxlength="50000"
            />

            <div class="input-actions">
              <el-button @click="clearContent">清空</el-button>
              <el-button
                type="primary"
                :loading="biddingStore.isLoading"
                :disabled="!tenderContent.trim()"
                @click="analyzeTender"
              >
                <el-icon><Search /></el-icon>
                开始分析
              </el-button>
            </div>
          </div>
        </el-card>

        <!-- 快速操作 -->
        <el-card class="quick-actions-card" shadow="never">
          <template #header>
            <span>快速操作</span>
          </template>

          <div class="quick-actions">
            <el-button
              v-if="biddingStore.currentAnalysis"
              type="success"
              @click="generateOutline"
              :loading="biddingStore.isLoading"
            >
              <el-icon><EditPen /></el-icon>
              生成投标大纲
            </el-button>

            <el-button
              v-if="biddingStore.currentAnalysis"
              type="primary"
              @click="goToGenerate"
            >
              <el-icon><Document /></el-icon>
              生成投标文档
            </el-button>

            <el-button
              v-if="biddingStore.currentAnalysis"
              @click="saveAnalysis"
            >
              <el-icon><Download /></el-icon>
              保存分析结果
            </el-button>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧：分析结果 -->
      <el-col :span="12">
        <el-card class="result-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>分析结果</span>
              <el-button
                v-if="biddingStore.currentAnalysis"
                type="text"
                @click="copyAnalysis"
              >
                <el-icon><CopyDocument /></el-icon>
                复制
              </el-button>
            </div>
          </template>

          <!-- 分析结果内容 -->
          <div v-if="biddingStore.currentAnalysis" class="analysis-result">
            <!-- 关键要点 -->
            <div class="analysis-section">
              <h4>
                <el-icon><Star /></el-icon>
                关键要点
              </h4>
              <div class="key-points">
                <el-tag
                  v-for="(point, index) in biddingStore.currentAnalysis.key_points"
                  :key="index"
                  type="info"
                  class="key-point-tag"
                >
                  {{ point }}
                </el-tag>
              </div>
            </div>

            <!-- 详细分析 -->
            <div class="analysis-section">
              <h4>
                <el-icon><Document /></el-icon>
                详细分析
              </h4>
              <div class="analysis-content">
                {{ biddingStore.currentAnalysis.analysis }}
              </div>
            </div>

            <!-- 统计信息 -->
            <div class="analysis-stats">
              <el-descriptions :column="2" border>
                <el-descriptions-item label="关键要点数量">
                  {{ biddingStore.currentAnalysis.key_points.length }}
                </el-descriptions-item>
                <el-descriptions-item label="分析字数">
                  {{ biddingStore.currentAnalysis.analysis.length }}
                </el-descriptions-item>
                <el-descriptions-item label="原始文档字数">
                  {{ tenderContent.length }}
                </el-descriptions-item>
                <el-descriptions-item label="分析时间">
                  {{ new Date().toLocaleString('zh-CN') }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </div>

          <!-- 空状态 -->
          <el-empty
            v-else-if="!biddingStore.isLoading"
            description="请输入招标文档内容并点击分析"
          >
            <template #image>
              <el-icon size="64" color="#c0c4cc"><DocumentCopy /></el-icon>
            </template>
          </el-empty>

          <!-- 加载状态 -->
          <div v-if="biddingStore.isLoading" class="loading-content">
            <el-skeleton :rows="8" animated />
            <p class="loading-text">AI正在分析招标文档，请稍候...</p>
          </div>
        </el-card>

        <!-- 分析历史 -->
        <el-card class="history-card" shadow="never" v-if="analysisHistory.length > 0">
          <template #header>
            <div class="card-header">
              <span>分析历史</span>
              <el-button type="text" @click="clearHistory">
                清空历史
              </el-button>
            </div>
          </template>

          <div class="history-list">
            <div
              v-for="(item, index) in analysisHistory"
              :key="index"
              class="history-item"
              @click="loadHistoryItem(item)"
            >
              <div class="history-content">
                <h5>{{ item.title }}</h5>
                <p>{{ formatDate(item.createdAt) }}</p>
                <div class="history-summary">
                  {{ item.summary }}
                </div>
              </div>
              <el-icon class="history-arrow"><ArrowRight /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useBiddingStore } from '@/stores/bidding'

const router = useRouter()
const biddingStore = useBiddingStore()

// 状态
const tenderContent = ref('')
const analysisHistory = ref<any[]>([])

// 分析招标文档
const analyzeTender = async () => {
  if (!tenderContent.value.trim()) {
    ElMessage.warning('请输入招标文档内容')
    return
  }

  try {
    await biddingStore.analyzeTender(tenderContent.value)

    // 保存到历史记录
    const historyItem = {
      title: `分析_${new Date().toLocaleDateString('zh-CN')}`,
      content: tenderContent.value,
      analysis: biddingStore.currentAnalysis,
      summary: biddingStore.currentAnalysis?.key_points.slice(0, 3).join('，') || '',
      createdAt: new Date().toISOString()
    }
    analysisHistory.value.unshift(historyItem)

    ElMessage.success('分析完成')
  } catch (error: any) {
    ElMessage.error(`分析失败: ${error.message}`)
  }
}

// 生成投标大纲
const generateOutline = async () => {
  if (!biddingStore.currentAnalysis) {
    ElMessage.warning('请先分析招标文档')
    return
  }

  try {
    const result = await biddingStore.generateOutline({
      tender_requirements: tenderContent.value,
      key_points: biddingStore.currentAnalysis.key_points.join('\n'),
      rag_content: biddingStore.currentAnalysis.analysis
    })

    ElMessage.success('大纲生成成功')

    // 跳转到生成页面
    router.push({
      path: '/generate',
      query: {
        outline: result.outline
      }
    })
  } catch (error: any) {
    ElMessage.error(`生成大纲失败: ${error.message}`)
  }
}

// 跳转到文档生成
const goToGenerate = () => {
  router.push('/generate')
}

// 保存分析结果
const saveAnalysis = () => {
  if (!biddingStore.currentAnalysis) return

  const data = {
    tenderContent: tenderContent.value,
    analysis: biddingStore.currentAnalysis,
    exportTime: new Date().toISOString()
  }

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `招标分析_${new Date().toLocaleDateString('zh-CN')}.json`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)

  ElMessage.success('分析结果已保存')
}

// 复制分析结果
const copyAnalysis = async () => {
  if (!biddingStore.currentAnalysis) return

  const text = `关键要点：\n${biddingStore.currentAnalysis.key_points.join('\n')}\n\n详细分析：\n${biddingStore.currentAnalysis.analysis}`

  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('分析结果已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

// 清空内容
const clearContent = () => {
  tenderContent.value = ''
  biddingStore.currentAnalysis = null
}

// 文件上传处理
const handleFileUpload = (file: any) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    tenderContent.value = e.target?.result as string
    ElMessage.success('文档上传成功')
  }
  reader.onerror = () => {
    ElMessage.error('文档读取失败')
  }
  reader.readAsText(file)
}

// 加载历史记录
const loadHistoryItem = (item: any) => {
  tenderContent.value = item.content
  biddingStore.currentAnalysis = item.analysis
  ElMessage.success('已加载历史分析')
}

// 清空历史记录
const clearHistory = () => {
  analysisHistory.value = []
  localStorage.removeItem('tender_analysis_history')
  ElMessage.success('历史记录已清空')
}

// 格��化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

// 初始化
onMounted(() => {
  // 从localStorage加载历史记录
  const saved = localStorage.getItem('tender_analysis_history')
  if (saved) {
    try {
      analysisHistory.value = JSON.parse(saved)
    } catch (error) {
      console.error('加载历史记录失败:', error)
    }
  }
})

// 监听历史记录变化，保存到localStorage
import { watch } from 'vue'
watch(analysisHistory, (newHistory) => {
  localStorage.setItem('tender_analysis_history', JSON.stringify(newHistory))
}, { deep: true })
</script>

<style scoped>
.analyze {
  max-width: 1400px;
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

.input-content {
  margin-bottom: 16px;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
}

.quick-actions-card {
  margin-top: 20px;
}

.quick-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.analysis-result {
  max-height: 600px;
  overflow-y: auto;
}

.analysis-section {
  margin-bottom: 24px;
}

.analysis-section h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 12px 0;
  color: #303133;
  font-size: 16px;
}

.key-points {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
}

.key-point-tag {
  margin-bottom: 8px;
}

.analysis-content {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 6px;
  line-height: 1.6;
  color: #606266;
  white-space: pre-wrap;
  margin-bottom: 20px;
}

.analysis-stats {
  margin-top: 20px;
}

.loading-content {
  text-align: center;
}

.loading-text {
  margin-top: 16px;
  color: #909399;
}

.history-card {
  margin-top: 20px;
}

.history-list {
  max-height: 300px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.history-item:hover {
  background-color: #f8f9fa;
}

.history-item:last-child {
  border-bottom: none;
}

.history-content {
  flex: 1;
}

.history-content h5 {
  margin: 0 0 4px 0;
  color: #303133;
  font-size: 14px;
}

.history-content p {
  margin: 0 0 4px 0;
  color: #909399;
  font-size: 12px;
}

.history-summary {
  color: #606266;
  font-size: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-arrow {
  color: #c0c4cc;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .analyze .el-col {
    margin-bottom: 20px;
  }

  .quick-actions {
    flex-direction: column;
  }

  .input-actions {
    flex-direction: column;
    gap: 12px;
  }
}
</style>