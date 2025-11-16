import api from './index'
import { ApiResponse, SystemInfo } from '@/types'

export const systemApi = {
  // 获取系统信息
  getSystemInfo(): Promise<ApiResponse<SystemInfo>> {
    return api.get('/').then(res => res.data)
  },

  // 健康检查
  healthCheck(): Promise<ApiResponse<{ status: string; service: string }>> {
    return api.get('/health').then(res => res.data)
  }
}