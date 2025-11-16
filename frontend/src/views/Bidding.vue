<template>
  <div class="bidding">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <h2>投标管理</h2>
      <el-button type="primary" @click="$router.push('/bidding/create')">
        <el-icon><Plus /></el-icon>
        创建投标
      </el-button>
    </div>

    <!-- 筛选和搜索 -->
    <el-card class="filter-card" shadow="never">
      <el-form :model="filters" :inline="true">
        <el-form-item label="状态">
          <el-select v-model="filters.status" placeholder="全部状态" clearable @change="handleFilterChange">
            <el-option label="草稿" value="draft" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已提交" value="submitted" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 投标列表 -->
    <el-card class="table-card" shadow="never">
      <el-table
        v-loading="biddingStore.isLoading"
        :data="biddingStore.bidResponses"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="title" label="投标项目" min-width="200">
          <template #default="{ row }">
            <div class="bid-title">
              <h4>{{ row.title }}</h4>
              <p v-if="row.tender_id" class="bid-tender-id">招标ID: {{ row.tender_id }}</p>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="created_at" label="创建时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column prop="updated_at" label="更新时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.updated_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              text
              @click="viewBid(row.id)"
            >
              查看
            </el-button>
            <el-button
              v-if="row.status === 'draft'"
              type="success"
              size="small"
              text
              @click="editBid(row.id)"
            >
              编辑
            </el-button>
            <el-dropdown trigger="click">
              <el-button type="info" size="small" text>
                更多
                <el-icon><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="duplicateBid(row.id)">
                    <el-icon><CopyDocument /></el-icon>
                    复制
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-if="row.status === 'completed'"
                    @click="downloadBid(row.id)"
                  >
                    <el-icon><Download /></el-icon>
                    下载
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-if="row.status === 'completed'"
                    @click="submitBid(row.id)"
                  >
                    <el-icon><Upload /></el-icon>
                    提交
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-if="row.status === 'draft'"
                    @click="deleteBid(row.id)"
                    divided
                  >
                    <el-icon><Delete /></el-icon>
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="biddingStore.pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useBiddingStore } from '@/stores/bidding'

const router = useRouter()
const biddingStore = useBiddingStore()

// 分页和筛选
const currentPage = ref(1)
const pageSize = ref(20)
const filters = reactive({
  status: ''
})

// 获取投标列表
const fetchBids = async () => {
  try {
    await biddingStore.fetchBidResponses({
      page: currentPage.value,
      page_size: pageSize.value,
      status: filters.status || undefined
    })
  } catch (error: any) {
    ElMessage.error(`获取投标列表失败: ${error.message}`)
  }
}

// 处理筛选变化
const handleFilterChange = () => {
  currentPage.value = 1
  fetchBids()
}

// 重置筛选
const handleReset = () => {
  filters.status = ''
  currentPage.value = 1
  fetchBids()
}

// 处理分页大小变化
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  fetchBids()
}

// 处理当前页变化
const handleCurrentChange = (page: number) => {
  currentPage.value = page
  fetchBids()
}

// 查看投标
const viewBid = (id: string) => {
  router.push(`/bidding/${id}`)
}

// 编辑投标
const editBid = (id: string) => {
  router.push(`/bidding/${id}/edit`)
}

// 复制投标
const duplicateBid = async (id: string) => {
  try {
    const bid = await biddingStore.getBidResponse(id)
    const newBid = {
      title: `${bid.data.title} (副本)`,
      content: bid.data.content,
      status: 'draft' as const
    }
    await biddingStore.createBidResponse(newBid)
    ElMessage.success('投标复制成功')
    fetchBids()
  } catch (error: any) {
    ElMessage.error(`复制投标失败: ${error.message}`)
  }
}

// 下载投标
const downloadBid = (id: string) => {
  // TODO: 实现下载功能
  ElMessage.info('下载功能待实现')
}

// 提交投标
const submitBid = async (id: string) => {
  try {
    await ElMessageBox.confirm('确认提交此投标？提交后无法修改。', '确认提交', {
      type: 'warning'
    })

    // TODO: 调用提交API
    ElMessage.success('投标提交成功')
    fetchBids()
  } catch (error) {
    // 用户取消操作
  }
}

// 删除投标
const deleteBid = async (id: string) => {
  try {
    await ElMessageBox.confirm('确认删除此投标？删除后无法恢复。', '确认删除', {
      type: 'warning'
    })

    // TODO: 调用删除API
    ElMessage.success('投标删除成功')
    fetchBids()
  } catch (error) {
    // 用户取消操作
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
  return new Date(dateString).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchBids()
})
</script>

<style scoped>
.bidding {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.filter-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.bid-title h4 {
  margin: 0 0 4px 0;
  color: #303133;
  font-size: 16px;
}

.bid-tender-id {
  margin: 0;
  color: #909399;
  font-size: 12px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>