import request from './index'

export interface KnowledgeDocument {
  id: string
  title: string
  content: string
  category: string
  created_at: string
  size: number
}

export interface KnowledgeUploadRequest {
  title: string
  content: string
  category?: string
}

export interface KnowledgeListResponse {
  items: KnowledgeDocument[]
  total: number
  page: number
  page_size: number
}

export interface SearchResult {
  id: string
  title: string
  category: string
  content: string
  score: number
}

// 知识库API
export const knowledgeApi = {
  // 上传知识文档
  upload: (data: KnowledgeUploadRequest) => {
    return request.post('/api/v1/knowledge/upload', data)
  },

  // 获取知识库列表
  list: (page = 1, pageSize = 20) => {
    return request.get<KnowledgeListResponse>('/api/v1/knowledge/list', {
      params: {
        page,
        page_size: pageSize
      }
    })
  },

  // 搜索知识库
  search: (query: string, topK = 3) => {
    return request.get<SearchResult[]>('/api/v1/knowledge/search', {
      params: {
        query,
        top_k: topK
      }
    })
  },

  // 删除知识文档
  delete: (docId: string) => {
    return request.delete(`/api/v1/knowledge/${docId}`)
  },

  // 获取知识文档详情
  get: (docId: string) => {
    return request.get<KnowledgeDocument>(`/api/v1/knowledge/${docId}`)
  },

  // 更新知识文档
  update: (docId: string, data: Partial<KnowledgeUploadRequest>) => {
    return request.put(`/api/v1/knowledge/${docId}`, data)
  }
}