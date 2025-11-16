import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { biddingApi } from '@/api/bidding'
import type {
  BidResponse,
  BidResponseCreate,
  TenderAnalysis,
  OutlineGeneration,
  DocumentGenerationResult,
  PaginatedResponse,
  PaginationParams,
  Template
} from '@/types'

export const useBiddingStore = defineStore('bidding', () => {
  // 状态
  const bidResponses = ref<BidResponse[]>([])
  const templates = ref<Template[]>([])
  const currentAnalysis = ref<TenderAnalysis | null>(null)
  const currentOutline = ref<OutlineGeneration | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref({
    total: 0,
    page: 1,
    page_size: 20
  })

  // 计算属性
  const isLoading = computed(() => loading.value)
  const hasError = computed(() => error.value !== null)
  const errorMessage = computed(() => error.value)

  // 投标响应管理
  const fetchBidResponses = async (params?: PaginationParams & { status?: string }) => {
    loading.value = true
    error.value = null
    try {
      const response = await biddingApi.getBidResponses(params)
      bidResponses.value = response.data.items
      pagination.value = {
        total: response.data.total,
        page: response.data.page,
        page_size: response.data.page_size
      }
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const createBidResponse = async (data: BidResponseCreate) => {
    loading.value = true
    error.value = null
    try {
      const response = await biddingApi.createBidResponse(data)
      bidResponses.value.unshift(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const getBidResponse = async (id: string) => {
    loading.value = true
    error.value = null
    try {
      const response = await biddingApi.getBidResponse(id)
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 模板管理
  const fetchTemplates = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await biddingApi.getTemplates()
      templates.value = response.data.templates
      return response.data.templates
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 招标分析
  const analyzeTender = async (tenderContent: string) => {
    loading.value = true
    error.value = null
    try {
      const response = await biddingApi.analyzeTender(tenderContent)
      currentAnalysis.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 大纲生成
  const generateOutline = async (params: {
    tender_requirements: string
    key_points?: string
    rag_content?: string
  }) => {
    loading.value = true
    error.value = null
    try {
      const response = await biddingApi.generateOutline(params)
      currentOutline.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 文档生成
  const generateDocument = async (params: {
    outline: string
    tender_requirements: string
    rag_content?: string
  }) => {
    loading.value = true
    error.value = null
    try {
      const response = await biddingApi.generateDocument(params)
      return response.data
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 基于模板生成
  const generateFromTemplate = async (params: {
    template_name: string
    data: Record<string, any>
  }) => {
    loading.value = true
    error.value = null
    try {
      const response = await biddingApi.generateFromTemplate(params)
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
    bidResponses.value = []
    templates.value = []
    currentAnalysis.value = null
    currentOutline.value = null
    loading.value = false
    error.value = null
    pagination.value = {
      total: 0,
      page: 1,
      page_size: 20
    }
  }

  return {
    // 状态
    bidResponses,
    templates,
    currentAnalysis,
    currentOutline,
    pagination,
    isLoading,
    hasError,
    errorMessage,

    // 方法
    fetchBidResponses,
    createBidResponse,
    getBidResponse,
    fetchTemplates,
    analyzeTender,
    generateOutline,
    generateDocument,
    generateFromTemplate,
    clearError,
    reset
  }
})