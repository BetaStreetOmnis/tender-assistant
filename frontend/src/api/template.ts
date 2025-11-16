import api from './index'
import {
  ApiResponse,
  Template,
  TemplateVariable,
  OutlineGeneration,
  DocumentGenerationResult,
  GenerationStatus
} from '@/types'

export const templateApi = {
  // 获取模板列表
  async getTemplates(): Promise<ApiResponse<{ templates: Template[] }>> {
    return api.get('/template/list').then(res => res.data)
  },

  // 上传模板
  async uploadTemplate(file: File, templateName: string, description?: string): Promise<ApiResponse<any>> {
    const formData = new FormData()
    formData.append('template_file', file)
    formData.append('template_name', templateName)
    if (description) {
      formData.append('description', description)
    }
    return api.upload('/template/upload', formData).then(res => res.data)
  },

  // 获取模板变量
  async getTemplateVariables(templateName: string): Promise<ApiResponse<{ template_name: string; variables: TemplateVariable[] }>> {
    return api.get('/template/variables', { template_name: templateName }).then(res => res.data)
  },

  // 基于模板生成文档
  async generateFromTemplate(params: {
    template_name: string
    data: Record<string, any>
    use_rag?: boolean
  }): Promise<ApiResponse<{ filename: string; download_url: string }>> {
    const formData = new FormData()
    formData.append('template_name', params.template_name)
    formData.append('data', JSON.stringify(params.data))
    formData.append('use_rag', params.use_rag?.toString() || 'false')
    return api.upload('/template/generate-from-template', formData).then(res => res.data)
  },

  // 生成大纲
  async generateOutline(params: {
    topic: string
    key_points?: string
    use_rag?: boolean
  }): Promise<ApiResponse<OutlineGeneration>> {
    const formData = new FormData()
    formData.append('topic', params.topic)
    if (params.key_points) {
      formData.append('key_points', params.key_points)
    }
    formData.append('use_rag', params.use_rag?.toString() || 'false')
    return api.upload('/template/generate-outline', formData).then(res => res.data)
  },

  // 生成完整文档
  async generateFullText(params: {
    outline: string
    key_points?: string
    use_rag?: boolean
  }): Promise<ApiResponse<{ task_id: string }>> {
    const formData = new FormData()
    formData.append('outline', params.outline)
    if (params.key_points) {
      formData.append('key_points', params.key_points)
    }
    formData.append('use_rag', params.use_rag?.toString() || 'false')
    return api.upload('/template/generate-fulltext', formData).then(res => res.data)
  },

  // 获取生成状态
  async getGenerationStatus(taskId: string): Promise<ApiResponse<GenerationStatus>> {
    return api.get(`/template/generation-status/${taskId}`).then(res => res.data)
  },

  // 处理下一个章节
  async processNextSection(taskId: string): Promise<ApiResponse<any>> {
    return api.post(`/template/process-next-section/${taskId}`).then(res => res.data)
  },

  // 导出Word文档
  async exportWord(content: string, contentType: 'outline' | 'fulltext' = 'outline'): Promise<ApiResponse<{ filename: string; download_url: string }>> {
    const formData = new FormData()
    formData.append('content', content)
    formData.append('content_type', contentType)
    return api.upload('/template/export-word', formData).then(res => res.data)
  },

  // 下载文件
  downloadFile(filename: string): Promise<void> {
    return api.download(`/template/download/${filename}`, filename)
  },

  // 删除模板
  async deleteTemplate(templateName: string): Promise<ApiResponse<{ message: string }>> {
    return api.delete(`/template/delete/${templateName}`).then(res => res.data)
  }
}