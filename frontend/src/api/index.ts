import axios, { AxiosInstance, AxiosResponse } from 'axios'
import { ApiResponse } from '@/types'

class ApiClient {
  private instance: AxiosInstance

  constructor() {
    this.instance = axios.create({
      baseURL: '/api/v1',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // 请求拦截器
    this.instance.interceptors.request.use(
      (config) => {
        // 可以在这里添加token等认证信息
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // 响应拦截器
    this.instance.interceptors.response.use(
      (response: AxiosResponse<ApiResponse>) => {
        const { data } = response
        if (data.code === 200) {
          return response
        } else {
          throw new Error(data.message || '请求失败')
        }
      },
      (error) => {
        const message = error.response?.data?.detail || error.message || '网络错误'
        throw new Error(message)
      }
    )
  }

  get<T = any>(url: string, params?: any): Promise<AxiosResponse<ApiResponse<T>>> {
    return this.instance.get(url, { params })
  }

  post<T = any>(url: string, data?: any, config?: any): Promise<AxiosResponse<ApiResponse<T>>> {
    return this.instance.post(url, data, config)
  }

  put<T = any>(url: string, data?: any): Promise<AxiosResponse<ApiResponse<T>>> {
    return this.instance.put(url, data)
  }

  delete<T = any>(url: string): Promise<AxiosResponse<ApiResponse<T>>> {
    return this.instance.delete(url)
  }

  // 文件上传
  upload<T = any>(url: string, formData: FormData): Promise<AxiosResponse<ApiResponse<T>>> {
    return this.instance.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }

  // 文件下载
  download(url: string, filename?: string): Promise<void> {
    return this.instance.get(url, {
      responseType: 'blob'
    }).then((response) => {
      const blob = new Blob([response.data])
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename || 'document'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
    })
  }
}

export default new ApiClient()