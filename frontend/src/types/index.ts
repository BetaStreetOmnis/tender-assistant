// 通用响应接口
export interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
}

// 投标相关接口
export interface BidResponse {
  id: string
  tender_id?: string
  title: string
  status: 'draft' | 'in_progress' | 'completed' | 'submitted'
  content?: string
  created_at: string
  updated_at: string
}

export interface BidResponseCreate {
  tender_id?: string
  title: string
  content?: string
  status?: 'draft' | 'in_progress' | 'completed' | 'submitted'
}

// 模板相关接口
export interface Template {
  name: string
  filename: string
  description?: string
  variables: TemplateVariable[]
}

export interface TemplateVariable {
  name: string
  type: 'text' | 'number' | 'date' | 'select'
  description?: string
  required: boolean
  options?: string[] // 用于select类型
}

// 招标分析接口
export interface TenderAnalysis {
  analysis: string
  key_points: string[]
}

export interface OutlineGeneration {
  outline: string
  sections: OutlineSection[]
}

export interface OutlineSection {
  title: string
  level: number
  content?: string
  subsections?: OutlineSection[]
}

// 文档生成相关
export interface DocumentGenerationRequest {
  outline: string
  tender_requirements: string
  rag_content?: string
}

export interface DocumentGenerationResult {
  file_path: string
  download_url: string
  task_id?: string
}

export interface GenerationStatus {
  task_id: string
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  progress: number
  current_section?: string
  result?: DocumentGenerationResult
}

// 分页接口
export interface PaginationParams {
  page: number
  page_size: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

// 模板生成请求
export interface TemplateGenerationRequest {
  template_name: string
  data: Record<string, any>
  use_rag?: boolean
}

// 系统信息接口
export interface SystemInfo {
  message: string
  description: string
  version: string
  status: string
  features: string[]
  endpoints: {
    demo: string
    templates: string
    analyze: string
    docs: string
  }
}