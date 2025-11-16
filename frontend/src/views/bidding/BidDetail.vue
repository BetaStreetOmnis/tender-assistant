<template>
  <div class="bid-detail">
    <el-card v-if="bidData" shadow="never">
      <template #header>
        <div class="card-header">
          <span>投标详情</span>
          <div class="header-actions">
            <el-button v-if="bidData.status === 'draft'" type="primary" @click="editBid">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button @click="$router.go(-1)">返回</el-button>
          </div>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="项目标题">
          {{ bidData.title }}
        </el-descriptions-item>
        <el-descriptions-item label="招标ID">
          {{ bidData.tender_id || '无' }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(bidData.status)">
            {{ getStatusText(bidData.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ formatDate(bidData.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="更新时间" :span="2">
          {{ formatDate(bidData.updated_at) }}
        </el-descriptions-item>
      </el-descriptions>

      <div class="content-section">
        <h3>项目内容</h3>
        <div class="content-display">
          {{ bidData.content || '暂无内容' }}
        </div>
      </div>
    </el-card>

    <el-skeleton v-else :rows="10" animated />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useBiddingStore } from '@/stores/bidding'

const route = useRoute()
const router = useRouter()
const biddingStore = useBiddingStore()

const bidData = ref<any>(null)

const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    draft: 'info',
    in_progress: 'warning',
    completed: 'success',
    submitted: 'primary'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    draft: '草稿',
    in_progress: '进行中',
    completed: '已完成',
    submitted: '已提交'
  }
  return textMap[status] || status
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const editBid = () => {
  router.push(`/bidding/${route.params.id}/edit`)
}

const loadBidDetail = async () => {
  try {
    const result = await biddingStore.getBidResponse(route.params.id as string)
    bidData.value = result
  } catch (error: any) {
    ElMessage.error(`加载投标详情失败: ${error.message}`)
  }
}

onMounted(() => {
  loadBidDetail()
})
</script>

<style scoped>
.bid-detail {
  max-width: 1000px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.content-section {
  margin-top: 24px;
}

.content-section h3 {
  margin: 0 0 16px 0;
  color: #303133;
}

.content-display {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 6px;
  line-height: 1.6;
  white-space: pre-wrap;
  min-height: 200px;
}
</style>