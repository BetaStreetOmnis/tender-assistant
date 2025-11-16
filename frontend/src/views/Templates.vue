<template>
  <div class="templates">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <h2>模板管理</h2>
      <el-button type="primary" @click="$router.push('/templates/create')">
        <el-icon><Plus /></el-icon>
        上传模板
      </el-button>
    </div>

    <!-- 模板统计 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon size="32" color="#409EFF"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ templateStore.templates.length }}</div>
              <div class="stat-label">总模板数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon size="32" color="#67C23A"><FolderOpened /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ activeTemplatesCount }}</div>
              <div class="stat-label">活跃模板</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon size="32" color="#E6A23C"><Setting /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalVariablesCount }}</div>
              <div class="stat-label">变量总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon size="32" color="#F56C6C"><Download /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ downloadsCount }}</div>
              <div class="stat-label">下载次数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 模板列表 -->
    <el-card class="templates-card" shadow="never">
      <div class="templates-header">
        <h3>模板列表</h3>
        <el-button @click="refreshTemplates">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>

      <el-empty v-if="templateStore.templates.length === 0" description="暂无模板">
        <el-button type="primary" @click="$router.push('/templates/create')">
          上传第一个模板
        </el-button>
      </el-empty>

      <el-row v-else :gutter="20">
        <el-col
          v-for="template in templateStore.templates"
          :key="template.name"
          :span="8"
          class="template-col"
        >
          <el-card class="template-card" shadow="hover">
            <div class="template-header">
              <div class="template-icon">
                <el-icon size="24" color="#409EFF"><Document /></el-icon>
              </div>
              <div class="template-actions">
                <el-dropdown trigger="click">
                  <el-button type="text" size="small">
                    <el-icon><MoreFilled /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="editTemplate(template)">
                        <el-icon><Edit /></el-icon>
                        编辑
                      </el-dropdown-item>
                      <el-dropdown-item @click="downloadTemplate(template)">
                        <el-icon><Download /></el-icon>
                        下载
                      </el-dropdown-item>
                      <el-dropdown-item @click="duplicateTemplate(template)">
                        <el-icon><CopyDocument /></el-icon>
                        复制
                      </el-dropdown-item>
                      <el-dropdown-item
                        @click="deleteTemplate(template)"
                        divided
                      >
                        <el-icon><Delete /></el-icon>
                        删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>

            <div class="template-content">
              <h4 class="template-name">{{ template.name }}</h4>
              <p class="template-description">
                {{ template.description || '暂无描述' }}
              </p>

              <div class="template-meta">
                <div class="template-variables">
                  <el-icon><Setting /></el-icon>
                  <span>{{ template.variables?.length || 0 }} 个变量</span>
                </div>
                <div class="template-filename">
                  <el-icon><Document /></el-icon>
                  <span>{{ template.filename }}</span>
                </div>
              </div>

              <div class="template-variables-list" v-if="template.variables?.length > 0">
                <el-tag
                  v-for="variable in template.variables.slice(0, 3)"
                  :key="variable.name"
                  size="small"
                  type="info"
                  class="variable-tag"
                >
                  {{ variable.name }}
                </el-tag>
                <el-tag
                  v-if="template.variables.length > 3"
                  size="small"
                  type="info"
                  class="variable-tag"
                >
                  +{{ template.variables.length - 3 }}
                </el-tag>
              </div>
            </div>

            <div class="template-footer">
              <el-button
                type="primary"
                size="small"
                @click="useTemplate(template)"
              >
                使用模板
              </el-button>
              <el-button
                size="small"
                @click="previewTemplate(template)"
              >
                预览
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useTemplateStore } from '@/stores/template'
import { biddingApi } from '@/api/bidding'
import type { Template } from '@/types'

const router = useRouter()
const templateStore = useTemplateStore()
const downloadsCount = ref(0)

// 计算属性
const activeTemplatesCount = computed(() => {
  return templateStore.templates.length
})

const totalVariablesCount = computed(() => {
  return templateStore.templates.reduce((total, template) => {
    return total + (template.variables?.length || 0)
  }, 0)
})

// 获取模板列表
const refreshTemplates = async () => {
  try {
    await templateStore.fetchTemplates()
  } catch (error: any) {
    ElMessage.error(`获取模板列表失败: ${error.message}`)
  }
}

// 使用模板
const useTemplate = (template: Template) => {
  router.push({
    path: '/generate',
    query: {
      template: template.name
    }
  })
}

// 编辑模板
const editTemplate = (template: Template) => {
  router.push(`/templates/${template.name}/edit`)
}

// 下载模板
const downloadTemplate = (template: Template) => {
  templateStore.downloadFile(template.filename)
    .then(() => {
      downloadsCount.value++
      ElMessage.success('模板下载成功')
    })
    .catch((error: any) => {
      ElMessage.error(`下载失败: ${error.message}`)
    })
}

// 复制模板
const duplicateTemplate = async (template: Template) => {
  // TODO: 实现模板复制功能
  ElMessage.info('模板复制功能待实现')
}

// 删除模板
const deleteTemplate = async (template: Template) => {
  try {
    await ElMessageBox.confirm(
      `确认删除模板 "${template.name}"？删除后无法恢复。`,
      '确认删除',
      {
        type: 'warning',
        confirmButtonText: '确认删除',
        cancelButtonText: '取消'
      }
    )

    await templateStore.deleteTemplate(template.name)
    ElMessage.success('模板删除成功')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(`删除失败: ${error.message}`)
    }
  }
}

// 预览模板
const previewTemplate = async (template: Template) => {
  try {
    await templateStore.fetchTemplateVariables(template.name)
    // TODO: 打开预览对话框
    ElMessage.info('预览功能待实现')
  } catch (error: any) {
    ElMessage.error(`预览失败: ${error.message}`)
  }
}

onMounted(() => {
  refreshTemplates()
})
</script>

<style scoped>
.templates {
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

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  height: 100px;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  margin-right: 16px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.templates-card {
  min-height: 400px;
}

.templates-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.templates-header h3 {
  margin: 0;
  color: #303133;
}

.template-col {
  margin-bottom: 20px;
}

.template-card {
  height: 100%;
  transition: all 0.3s ease;
}

.template-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.template-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.template-actions {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.template-card:hover .template-actions {
  opacity: 1;
}

.template-content {
  margin-bottom: 16px;
}

.template-name {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 18px;
  font-weight: 500;
}

.template-description {
  margin: 0 0 12px 0;
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.template-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.template-variables,
.template-filename {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #909399;
}

.template-variables-list {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.variable-tag {
  font-size: 11px;
}

.template-footer {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  border-top: 1px solid #f0f0f0;
  padding-top: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .template-col {
    margin-bottom: 16px;
  }

  .stats-row .el-col {
    margin-bottom: 12px;
  }
}
</style>