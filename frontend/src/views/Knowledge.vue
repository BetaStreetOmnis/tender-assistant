<template>
  <div class="knowledge">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>知识库管理</h2>
      <p>管理和维护智能知识库，提升AI生成质量</p>
    </div>

    <el-row :gutter="20">
      <!-- 左侧：知识库列表 -->
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>知识文档</span>
              <div class="header-actions">
                <el-input
                  v-model="searchQuery"
                  placeholder="搜索知识库..."
                  style="width: 200px; margin-right: 12px"
                  @keyup.enter="searchKnowledge"
                  clearable
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
                <el-button type="primary" @click="showUploadDialog = true">
                  <el-icon><Plus /></el-icon>
                  上传文档
                </el-button>
              </div>
            </div>
          </template>

          <!-- 知识文档列表 -->
          <el-table :data="knowledgeList" v-loading="loading" stripe>
            <el-table-column prop="title" label="标题" min-width="200" />
            <el-table-column prop="category" label="分类" width="120">
              <template #default="{ row }">
                <el-tag size="small" :type="getCategoryType(row.category)">
                  {{ row.category }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="size" label="大小" width="100">
              <template #default="{ row }">
                {{ formatSize(row.size) }}
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="text"
                  size="small"
                  @click="viewDocument(row)"
                >
                  查看
                </el-button>
                <el-button
                  type="text"
                  size="small"
                  @click="editDocument(row)"
                >
                  编辑
                </el-button>
                <el-button
                  type="text"
                  size="small"
                  @click="deleteDocument(row)"
                  style="color: #f56c6c"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-card>
      </el-col>

      <!-- 右侧：统计信息 -->
      <el-col :span="8">
        <el-card shadow="never" class="stats-card">
          <template #header>
            <span>知识库统计</span>
          </template>

          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-value">{{ stats.total }}</div>
              <div class="stat-label">总文档数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.categories }}</div>
              <div class="stat-label">分类数量</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ formatSize(stats.totalSize) }}</div>
              <div class="stat-label">总大小</div>
            </div>
          </div>
        </el-card>

        <!-- 分类分布 -->
        <el-card shadow="never" class="category-card" style="margin-top: 20px">
          <template #header>
            <span>分类分布</span>
          </template>

          <div v-for="(count, category) in categoryStats" :key="category" class="category-item">
            <span class="category-name">{{ category }}</span>
            <el-tag size="small">{{ count }}</el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 上传对话框 -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传知识文档"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="uploadForm" :rules="uploadRules" ref="uploadFormRef" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="uploadForm.title" placeholder="请输入文档标题" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="uploadForm.category" placeholder="请选择分类" style="width: 100%">
            <el-option label="通用" value="通用" />
            <el-option label="建筑工程" value="建筑工程" />
            <el-option label="软件开发" value="软件开发" />
            <el-option label="医疗健康" value="医疗健康" />
            <el-option label="教育科研" value="教育科研" />
            <el-option label="金融服务" value="金融服务" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="uploadForm.content"
            type="textarea"
            :rows="10"
            placeholder="请输入文档内容，支持文字、段落等格式"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showUploadDialog = false">取消</el-button>
          <el-button type="primary" @click="uploadDocument" :loading="uploading">
            {{ uploading ? '上传中...' : '上传' }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 查看对话框 -->
    <el-dialog
      v-model="showViewDialog"
      :title="viewingDocument?.title"
      width="800px"
    >
      <div v-if="viewingDocument" class="document-content">
        <div class="document-meta">
          <el-tag :type="getCategoryType(viewingDocument.category)">
            {{ viewingDocument.category }}
          </el-tag>
          <span class="document-time">
            创建时间：{{ formatDate(viewingDocument.created_at) }}
          </span>
        </div>
        <div class="document-text">
          {{ viewingDocument.content }}
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { knowledgeApi, type KnowledgeDocument, type KnowledgeUploadRequest } from '@/api/knowledge'

// 状态
const loading = ref(false)
const uploading = ref(false)
const knowledgeList = ref<KnowledgeDocument[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchQuery = ref('')

// 对话框状态
const showUploadDialog = ref(false)
const showViewDialog = ref(false)
const viewingDocument = ref<KnowledgeDocument | null>(null)

// 表单数据
const uploadForm = ref<KnowledgeUploadRequest>({
  title: '',
  content: '',
  category: '通用'
})

const uploadFormRef = ref()

// 表单验证规则
const uploadRules = {
  title: [
    { required: true, message: '请输入文档标题', trigger: 'blur' },
    { min: 1, max: 100, message: '标题长度在 1 到 100 个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入文档内容', trigger: 'blur' },
    { min: 10, message: '内容至少 10 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ]
}

// 统计数据
const stats = computed(() => {
  const categories = new Set(knowledgeList.value.map(doc => doc.category)).size
  const totalSize = knowledgeList.value.reduce((sum, doc) => sum + doc.size, 0)

  return {
    total: total.value,
    categories,
    totalSize
  }
})

// 分类统计
const categoryStats = computed(() => {
  const stats: Record<string, number> = {}
  knowledgeList.value.forEach(doc => {
    stats[doc.category] = (stats[doc.category] || 0) + 1
  })
  return stats
})

// 获取知识库列表
const fetchKnowledgeList = async () => {
  try {
    loading.value = true
    const response = await knowledgeApi.list(currentPage.value, pageSize.value)

    if (response.data.code === 200) {
      knowledgeList.value = response.data.data.items
      total.value = response.data.data.total
    }
  } catch (error: any) {
    ElMessage.error(`获取知识库列表失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}

// 搜索知识库
const searchKnowledge = async () => {
  if (!searchQuery.value.trim()) {
    await fetchKnowledgeList()
    return
  }

  try {
    loading.value = true
    const response = await knowledgeApi.search(searchQuery.value, 100)

    if (response.data.code === 200) {
      knowledgeList.value = response.data.data
      total.value = response.data.data.length
    }
  } catch (error: any) {
    ElMessage.error(`搜索失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}

// 上传文档
const uploadDocument = async () => {
  try {
    await uploadFormRef.value.validate()

    uploading.value = true
    const response = await knowledgeApi.upload(uploadForm.value)

    if (response.data.code === 200) {
      ElMessage.success('文档上传成功')
      showUploadDialog.value = false
      uploadForm.value = { title: '', content: '', category: '通用' }
      await fetchKnowledgeList()
    }
  } catch (error: any) {
    ElMessage.error(`上传失败: ${error.message}`)
  } finally {
    uploading.value = false
  }
}

// 查看文档
const viewDocument = (doc: KnowledgeDocument) => {
  viewingDocument.value = doc
  showViewDialog.value = true
}

// 编辑文档
const editDocument = (doc: KnowledgeDocument) => {
  uploadForm.value = {
    title: doc.title,
    content: doc.content,
    category: doc.category
  }
  showUploadDialog.value = true
}

// 删除文档
const deleteDocument = async (doc: KnowledgeDocument) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文档 "${doc.title}" 吗？此操作不可撤销。`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await knowledgeApi.delete(doc.id)

    if (response.data.code === 200) {
      ElMessage.success('文档删除成功')
      await fetchKnowledgeList()
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(`删除失败: ${error.message}`)
    }
  }
}

// 分页处理
const handleSizeChange = (size: number) => {
  pageSize.value = size
  fetchKnowledgeList()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  fetchKnowledgeList()
}

// 辅助函数
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const formatSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getCategoryType = (category: string) => {
  const typeMap: Record<string, string> = {
    '通用': 'info',
    '建筑工程': 'success',
    '软件开发': 'primary',
    '医疗健康': 'warning',
    '教育科研': 'success',
    '金融服务': 'danger',
    '其他': ''
  }
  return typeMap[category] || 'info'
}

// 初始化
onMounted(() => {
  fetchKnowledgeList()
})
</script>

<style scoped>
.knowledge {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.stats-card .stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.category-card .category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.category-item:last-child {
  border-bottom: none;
}

.category-name {
  color: #303133;
}

.document-content {
  max-height: 60vh;
  overflow-y: auto;
}

.document-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.document-time {
  color: #909399;
  font-size: 14px;
}

.document-text {
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .knowledge .el-col:first-child {
    span: 24;
  }

  .knowledge .el-col:last-child {
    span: 24;
    margin-top: 20px;
  }

  .stats-card .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .header-actions {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .header-actions .el-input {
    margin-right: 0 !important;
  }

  .stats-card .stats-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
</style>