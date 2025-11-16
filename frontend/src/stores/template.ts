import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { templateApi } from '@/api/template'
import type {
  Template,
  TemplateVariable,
  OutlineGeneration,
  GenerationStatus
} from '@/types'

export const useTemplateStore = defineStore('template', () => {
  // 状态
  const templates = ref<Template[]>([])
  const currentTemplate = ref<Template | null>(null)
  const currentVariables = ref<TemplateVariable[]>([])
  const currentOutline = ref<OutlineGeneration | null>(null)
  const generationStatus = ref<GenerationStatus | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const isLoading = computed(() => loading.value)
  const hasError = computed(() => error.value !== null)
  const errorMessage = computed(() => error.value)
  const isGenerating = computed(() =>
    generationStatus.value?.status === 'in_progress'
  )

  // 获取模板列表
  const fetchTemplates = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await templateApi.getTemplates()
      templates.value = response.data.templates
      return response.data.templates
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 上传模板
  const uploadTemplate = async (file: File, templateName: string, description?: string) => {
    loading.value = true
    error.value = null
    try {
      const response = await templateApi.uploadTemplate(file, templateName, description)
      await fetchTemplates() // 重新获取模板列表
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取模板变量
  const fetchTemplateVariables = async (templateName: string) => {
    loading.value = true
    error.value = null
    try {
      const response = await templateApi.getTemplateVariables(templateName)
      currentVariables.value = response.data.variables
      currentTemplate.value = {
        name: response.data.template_name,
        filename: `${response.data.template_name}.docx`,
        variables: response.data.variables
      }
      return response.data.variables
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 基于模板生成文档
  const generateFromTemplate = async (params: {
    template_name: string
    data: Record<string, any>
    use_rag?: boolean
  }) => {
    loading.value = true
    error.value = null
    try {
      const response = await templateApi.generateFromTemplate(params)
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 生成大纲
  const generateOutline = async (params: {
    topic: string
    key_points?: string
    use_rag?: boolean
  }) => {
    loading.value = true
    error.value = null
    try {
      const response = await templateApi.generateOutline(params)
      currentOutline.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 生成完整文档
  const generateFullText = async (params: {
    outline: string
    key_points?: string
    use_rag?: boolean
  }) => {
    loading.value = true
    error.value = null
    try {
      const response = await templateApi.generateFullText(params)
      generationStatus.value = {
        task_id: response.data.task_id,
        status: 'pending',
        progress: 0
      }
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取生成状态
  const fetchGenerationStatus = async (taskId: string) => {
    try {
      const response = await templateApi.getGenerationStatus(taskId)
      generationStatus.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  // 处理下一个章节
  const processNextSection = async (taskId: string) => {
    loading.value = true
    error.value = null
    try {
      const response = await templateApi.processNextSection(taskId)
      generationStatus.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 导出Word文档
  const exportWord = async (content: string, contentType: 'outline' | 'fulltext' = 'outline') => {
    loading.value = true
    error.value = null
    try {
      const response = await templateApi.exportWord(content, contentType)
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 下载文件
  const downloadFile = async (filename: string) => {
    try {
      await templateApi.downloadFile(filename)
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  // 删除模板
  const deleteTemplate = async (templateName: string) => {
    loading.value = true
    error.value = null
    try {
      const response = await templateApi.deleteTemplate(templateName)
      await fetchTemplates() // 重新获取模板列表
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 清除错误
  const clearError = () => {
    error.value = null
  }

  // 重置状态
  const reset = () => {
    templates.value = []
    currentTemplate.value = null
    currentVariables.value = []
    currentOutline.value = null
    generationStatus.value = null
    loading.value = false
    error.value = null
  }

  return {
    // 状态
    templates,
    currentTemplate,
    currentVariables,
    currentOutline,
    generationStatus,
    isLoading,
    hasError,
    errorMessage,
    isGenerating,

    // 方法
    fetchTemplates,
    uploadTemplate,
    fetchTemplateVariables,
    generateFromTemplate,
    generateOutline,
    generateFullText,
    fetchGenerationStatus,
    processNextSection,
    exportWord,
    downloadFile,
    deleteTemplate,
    clearError,
    reset
  }
})