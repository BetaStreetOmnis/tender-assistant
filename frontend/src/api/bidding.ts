import api from './index'
import {
  ApiResponse,
  BidResponse,
  BidResponseCreate,
  TenderAnalysis,
  OutlineGeneration,
  DocumentGenerationRequest,
  DocumentGenerationResult,
  PaginatedResponse,
  PaginationParams,
  TemplateGenerationRequest,
  Template,
  TemplateVariable
} from '@/types'

export const biddingApi = {
  // 获取演示信息
  getDemo(): Promise<ApiResponse<any>> {
    return api.get('/bidding/demo').then(res => res.data)
  },

  // 投标响应管理
  async createBidResponse(data: BidResponseCreate): Promise<ApiResponse<BidResponse>> {
    return api.post('/bidding/responses', data).then(res => res.data)
  },

  async getBidResponses(params?: PaginationParams & { status?: string }): Promise<ApiResponse<PaginatedResponse<BidResponse>>> {
    return api.get('/bidding/responses', params).then(res => res.data)
  },

  async getBidResponse(id: string): Promise<ApiResponse<BidResponse>> {
    return api.get(`/bidding/responses/${id}`).then(res => res.data)
  },

  // 招标文档分析
  async analyzeTender(tenderContent: string): Promise<ApiResponse<TenderAnalysis>> {
    const formData = new FormData()
    formData.append('tender_content', tenderContent)
    return api.upload('/bidding/analyze-tender', formData).then(res => res.data)
  },

  // 生成投标大纲
  async generateOutline(params: {
    tender_requirements: string
    key_points?: string
    rag_content?: string
  }): Promise<ApiResponse<OutlineGeneration>> {
    const formData = new FormData()
    formData.append('tender_requirements', params.tender_requirements)
    if (params.key_points) {
      formData.append('key_points', params.key_points)
    }
    if (params.rag_content) {
      formData.append('rag_content', params.rag_content)
    }
    return api.upload('/bidding/generate-outline', formData).then(res => res.data)
  },

  // 生成投标文档
  async generateDocument(params: DocumentGenerationRequest): Promise<ApiResponse<DocumentGenerationResult>> {
    const formData = new FormData()
    formData.append('outline', params.outline)
    formData.append('tender_requirements', params.tender_requirements)
    if (params.rag_content) {
      formData.append('rag_content', params.rag_content)
    }
    return api.upload('/bidding/generate-document', formData).then(res => res.data)
  },

  // 基于模板生成文档
  async generateFromTemplate(params: TemplateGenerationRequest): Promise<ApiResponse<DocumentGenerationResult>> {
    const formData = new FormData()
    formData.append('template_name', params.template_name)
    formData.append('data', JSON.stringify(params.data))
    return api.upload('/bidding/generate-from-template', formData).then(res => res.data)
  },

  // 模板管理
  async getTemplates(): Promise<ApiResponse<{ templates: Template[]; count: number }>> {
    return api.get('/bidding/templates').then(res => res.data)
  },

  async uploadTemplate(file: File, name: string): Promise<ApiResponse<any>> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('name', name)
    return api.upload('/bidding/upload-template', formData).then(res => res.data)
  },

  async getTemplateVariables(templateName: string): Promise<ApiResponse<{ template_name: string; variables: TemplateVariable[]; count: number }>> {
    return api.get(`/bidding/templates/${templateName}/variables`).then(res => res.data)
  },

  async aiFillTemplateVariables(templateName: string, context: string): Promise<ApiResponse<any>> {
    const formData = new FormData()
    formData.append('context', context)
    return api.upload(`/bidding/templates/${templateName}/ai-fill`, formData).then(res => res.data)
  },

  async generateFromSpecificTemplate(templateName: string, variables: Record<string, any>): Promise<ApiResponse<DocumentGenerationResult>> {
    const formData = new FormData()
    formData.append('variables', JSON.stringify(variables))
    return api.upload(`/bidding/templates/${templateName}/generate`, formData).then(res => res.data)
  }
}