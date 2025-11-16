<template>
  <div class="generate">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>智能文档生成</h2>
    </div>

    <el-row :gutter="20">
      <!-- 左侧：输入区域 -->
      <el-col :span="12">
        <el-card class="input-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>生成配置</span>
              <el-steps :active="currentStep" finish-status="success" simple>
                <el-step title="选择模板" />
                <el-step title="填写变量" />
                <el-step title="生成文档" />
              </el-steps>
            </div>
          </template>

          <!-- 步骤1：选择模板 -->
          <div v-show="currentStep === 0" class="step-content">
            <h3>选择模板</h3>
            <el-select
              v-model="selectedTemplate"
              placeholder="请选择模板"
              style="width: 100%"
              @change="handleTemplateChange"
            >
              <el-option
                v-for="template in templateStore.templates"
                :key="template.name"
                :label="template.name"
                :value="template.name"
              >
                <div class="template-option">
                  <span>{{ template.name }}</span>
                  <span class="template-variables-count">
                    {{ template.variables?.length || 0 }} 个变量
                  </span>
                </div>
              </el-option>
            </el-select>

            <div class="step-actions">
              <el-button
                type="primary"
                :disabled="!selectedTemplate"
                @click="nextStep"
              >
                下一步
              </el-button>
            </div>
          </div>

          <!-- 步骤2：填写变量 -->
          <div v-show="currentStep === 1" class="step-content">
            <div class="step-header">
              <h3>填写模板变量</h3>
              <div class="ai-actions">
                <el-checkbox v-model="useKnowledgeForAutoFill" style="margin-right: 10px">
                  使用知识库增强
                </el-checkbox>
                <el-button
                  type="success"
                  :icon="MagicStick"
                  :loading="autoFilling"
                  @click="autoFillVariables"
                  :disabled="templateStore.currentVariables.length === 0"
                >
                  {{ autoFilling ? '智能填充中...' : 'AI自动填充' }}
                </el-button>
              </div>
            </div>

            <el-alert
              v-if="autoFillResult"
              :title="autoFillResult.message"
              :type="autoFillResult.type"
              show-icon
              style="margin-bottom: 20px"
            />

            <div v-if="selectedTemplate && templateStore.currentVariables.length > 0">
              <el-form :model="variableValues" label-width="120px">
                <el-form-item
                  v-for="variable in templateStore.currentVariables"
                  :key="variable.name"
                  :label="variable.name"
                  :required="variable.required"
                >
                  <el-input
                    v-if="variable.type === 'text'"
                    v-model="variableValues[variable.name]"
                    :placeholder="variable.description || `请输入${variable.name}`"
                  />
                  <el-input-number
                    v-else-if="variable.type === 'number'"
                    v-model="variableValues[variable.name]"
                    style="width: 100%"
                  />
                  <el-date-picker
                    v-else-if="variable.type === 'date'"
                    v-model="variableValues[variable.name]"
                    type="date"
                    style="width: 100%"
                  />
                  <el-select
                    v-else-if="variable.type === 'select'"
                    v-model="variableValues[variable.name]"
                    :placeholder="`请选择${variable.name}`"
                    style="width: 100%"
                  >
                    <el-option
                      v-for="option in variable.options"
                      :key="option"
                      :label="option"
                      :value="option"
                    />
                  </el-select>
                </el-form-item>
              </el-form>

              <div class="step-actions">
                <el-button @click="prevStep">上一步</el-button>
                <el-button
                  type="primary"
                  :disabled="!isFormValid"
                  @click="nextStep"
                >
                  下一步
                </el-button>
              </div>
            </div>

            <el-empty v-else description="该模板无需填写变量" />
          </div>

          <!-- 步骤3：生成文档 -->
          <div v-show="currentStep === 2" class="step-content">
            <h3>生成文档</h3>
            <div class="generation-summary">
              <h4>生成概要</h4>
              <p><strong>模板：</strong>{{ selectedTemplate }}</p>
              <p><strong>变量数量：</strong>{{ Object.keys(variableValues).length }}</p>
            </div>

            <div class="generation-options">
              <el-checkbox v-model="useRag">使用知识库增强</el-checkbox>
            </div>

            <div class="step-actions">
              <el-button @click="prevStep">上一步</el-button>
              <el-button
                type="primary"
                :loading="templateStore.isLoading"
                @click="generateDocument"
              >
                生成文档
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧：预览和结果区域 -->
      <el-col :span="12">
        <el-card class="preview-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>预览区域</span>
              <el-button
                v-if="generatedDocument"
                type="primary"
                size="small"
                @click="downloadDocument"
              >
                <el-icon><Download /></el-icon>
                下载文档
              </el-button>
            </div>
          </template>

          <!-- 变量预览 -->
          <div v-if="currentStep === 2 && Object.keys(variableValues).length > 0" class="variables-preview">
            <h4>变量值预览</h4>
            <el-descriptions :column="1" border>
              <el-descriptions-item
                v-for="(value, key) in variableValues"
                :key="key"
                :label="key"
              >
                {{ formatVariableValue(value) }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <!-- 生成结果 -->
          <div v-if="generatedDocument" class="generation-result">
            <el-result
              icon="success"
              title="文档生成成功"
              :sub-title="`文件名：${generatedDocument.filename}`"
            >
              <template #extra>
                <el-button type="primary" @click="downloadDocument">
                  <el-icon><Download /></el-icon>
                  下载文档
                </el-button>
                <el-button @click="resetGeneration">重新生成</el-button>
              </template>
            </el-result>
          </div>

          <!-- 空状态 -->
          <el-empty
            v-if="!generatedDocument && currentStep !== 2"
            description="请在左侧配置生成参数"
          />
        </el-card>

        <!-- 生成状态 -->
        <el-card v-if="templateStore.isGenerating" class="status-card" shadow="never">
          <div class="generation-status">
            <el-progress
              :percentage="templateStore.generationStatus?.progress || 0"
              :status="templateStore.generationStatus?.status === 'failed' ? 'exception' : undefined"
            />
            <p class="status-text">
              {{ templateStore.generationStatus?.current_section || '正在生成文档...' }}
            </p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { MagicStick, Download } from '@element-plus/icons-vue'
import { useTemplateStore } from '@/stores/template'
import { biddingApi } from '@/api/bidding'

const route = useRoute()
const router = useRouter()
const templateStore = useTemplateStore()

// 状态
const currentStep = ref(0)
const selectedTemplate = ref('')
const variableValues = ref<Record<string, any>>({})
const useRag = ref(false)
const generatedDocument = ref<any>(null)

// 自动填充相关状态
const autoFilling = ref(false)
const useKnowledgeForAutoFill = ref(true)
const autoFillResult = ref<any>(null)
const tenderContent = ref('') // 从分析页面传递的招标文档内容

// 计算属性
const isFormValid = computed(() => {
  if (!templateStore.currentVariables.length) return true

  return templateStore.currentVariables.every(variable => {
    if (variable.required) {
      return variableValues.value[variable.name] !== undefined && variableValues.value[variable.name] !== ''
    }
    return true
  })
})

// 初始化
onMounted(async () => {
  await templateStore.fetchTemplates()

  // 如果URL中有template参数，自动选择
  const templateName = route.query.template as string
  if (templateName) {
    selectedTemplate.value = templateName
    await handleTemplateChange()
  }
})

// 处理模板选择变化
const handleTemplateChange = async () => {
  if (!selectedTemplate.value) return

  try {
    await templateStore.fetchTemplateVariables(selectedTemplate.value)

    // 重置变量值
    variableValues.value = {}
    templateStore.currentVariables.forEach(variable => {
      if (variable.type === 'number') {
        variableValues.value[variable.name] = 0
      } else if (variable.type === 'date') {
        variableValues.value[variable.name] = new Date()
      } else {
        variableValues.value[variable.name] = ''
      }
    })
  } catch (error: any) {
    ElMessage.error(`获取模板变量失败: ${error.message}`)
  }
}

// 下一步
const nextStep = () => {
  if (currentStep.value < 2) {
    currentStep.value++
  }
}

// 上一步
const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 生成文档
const generateDocument = async () => {
  if (!selectedTemplate.value) {
    ElMessage.error('请先选择模板')
    return
  }

  try {
    const result = await templateStore.generateFromTemplate({
      template_name: selectedTemplate.value,
      data: variableValues.value,
      use_rag: useRag.value
    })

    generatedDocument.value = result
    ElMessage.success('文档生成成功')
  } catch (error: any) {
    ElMessage.error(`生成文档失败: ${error.message}`)
  }
}

// 下载文档
const downloadDocument = async () => {
  if (!generatedDocument.value) return

  try {
    await templateStore.downloadFile(generatedDocument.value.filename)
  } catch (error: any) {
    ElMessage.error(`下载失败: ${error.message}`)
  }
}

// 重置生成
const resetGeneration = () => {
  generatedDocument.value = null
  currentStep.value = 0
  selectedTemplate.value = ''
  variableValues.value = {}
  useRag.value = false
}

// AI自动填充模板变量
const autoFillVariables = async () => {
  if (!selectedTemplate.value) {
    ElMessage.error('请先选择模板')
    return
  }

  if (templateStore.currentVariables.length === 0) {
    ElMessage.warning('该模板没有需要填充的变量')
    return
  }

  autoFilling.value = true
  autoFillResult.value = null

  try {
    // 从URL或本地存储获取招标文档内容
    if (!tenderContent.value) {
      // 尝试从本地存储获取
      const storedContent = localStorage.getItem('tender_content')
      if (storedContent) {
        tenderContent.value = storedContent
      }
    }

    // 调用后端自动填充API
    const response = await fetch('/api/v1/template/auto-fill', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        template_id: templateStore.templates.findIndex(t => t.name === selectedTemplate.value) + 1,
        tender_content: tenderContent.value || null,
        use_knowledge: useKnowledgeForAutoFill.value
      })
    })

    const result = await response.json()

    if (result.code === 200) {
      // 填充返回的变量值
      const filledValues = result.data.filled_values

      // 更新表单中的变量值
      Object.keys(filledValues).forEach(varName => {
        if (variableValues.value.hasOwnProperty(varName)) {
          variableValues.value[varName] = filledValues[varName]
        }
      })

      // 显示成功消息
      const message = `成功填充 ${Object.keys(filledValues).length} 个变量`
      autoFillResult.value = {
        type: 'success',
        message
      }

      ElMessage.success({
        message,
        duration: 3000
      })

    } else {
      autoFillResult.value = {
        type: 'error',
        message: result.message || '自动填充失败'
      }
      ElMessage.error(result.message || '自动填充失败')
    }

  } catch (error: any) {
    console.error('自动填充失败:', error)
    autoFillResult.value = {
      type: 'error',
      message: `网络错误: ${error.message}`
    }
    ElMessage.error(`自动填充失败: ${error.message}`)
  } finally {
    autoFilling.value = false
  }
}

// 格式化变量值显示
const formatVariableValue = (value: any) => {
  if (value instanceof Date) {
    return value.toLocaleDateString('zh-CN')
  }
  return String(value) || '未设置'
}

// 监听步骤变化
watch(currentStep, (newStep) => {
  if (newStep === 2) {
    // 进入最后一步时，更新URL
    router.replace({
      query: {
        ...route.query,
        template: selectedTemplate.value
      }
    })
  }
})

// 初始化时检查是否有传递的招标文档内容
onMounted(async () => {
  await templateStore.fetchTemplates()

  // 如果URL中有template参数，自动选择
  const templateName = route.query.template as string
  if (templateName) {
    selectedTemplate.value = templateName
    await handleTemplateChange()
  }

  // 从URL参数获取招标文档内容
  const tenderContentParam = route.query.tenderContent as string
  if (tenderContentParam) {
    tenderContent.value = decodeURIComponent(tenderContentParam)
  } else {
    // 从本地存储获取
    const storedContent = localStorage.getItem('tender_content')
    if (storedContent) {
      tenderContent.value = storedContent
    }
  }
})
</script>

<style scoped>
.generate {
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

.step-content {
  min-height: 300px;
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.step-header h3 {
  margin: 0;
  color: #303133;
}

.ai-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.step-content h3 {
  margin: 0 0 20px 0;
  color: #303133;
}

.step-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.template-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.template-variables-count {
  font-size: 12px;
  color: #909399;
}

.generation-summary {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.generation-summary h4 {
  margin: 0 0 12px 0;
  color: #303133;
}

.generation-summary p {
  margin: 4px 0;
  color: #606266;
}

.generation-options {
  margin-bottom: 20px;
}

.variables-preview {
  margin-bottom: 20px;
}

.variables-preview h4 {
  margin: 0 0 16px 0;
  color: #303133;
}

.generation-result {
  text-align: center;
}

.status-card {
  margin-top: 20px;
}

.generation-status {
  text-align: center;
}

.status-text {
  margin-top: 12px;
  color: #606266;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .generate .el-col {
    margin-bottom: 20px;
  }
}
</style>