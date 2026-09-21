import axios from 'axios'
import { Project, Clip, Collection } from '../store/useProjectStore'
import { errorHandler } from '../utils/errorHandler'
import { apiConfigManager } from '../utils/apiConfig'
import {
  trackVideoImported,
  trackClipsExported,
  trackProcessingFailed,
} from '../analytics/events'

// Extend Axios config types
declare module 'axios' {
  interface InternalAxiosRequestConfig {
    metadata?: {
      startTime: number
      retryCount?: number
    }
  }
}

// Time formatter (unused, kept for later)

const api = axios.create({
  baseURL: apiConfigManager.getBaseUrl(),
  timeout: 300000, // Extend to 5-minute timeout
  headers: {
    'Content-Type': 'application/json',
  },
})

const RETRYABLE_METHODS = new Set(['get', 'head', 'options'])
const RETRYABLE_STATUS_CODES = new Set([408, 429, 500, 502, 503, 504])
const MAX_RETRIES = 2

const shouldRetry = (error: any): boolean => {
  const method = error?.config?.method?.toLowerCase()
  if (!method || !RETRYABLE_METHODS.has(method)) return false

  const status = error?.response?.status
  if (status && RETRYABLE_STATUS_CODES.has(status)) return true

  const code = error?.code
  return code === 'ECONNABORTED' || !error?.response
}

const getRetryDelay = (retryCount: number): number => 300 * Math.pow(2, retryCount)

apiConfigManager.addListener((config) => {
  api.defaults.baseURL = config.baseUrl
})

const isTauriRuntime = () => (
  typeof window !== 'undefined' &&
  ((window as any).__TAURI__ || (window as any).__TAURI_INTERNALS__)
)

// Request interceptor
api.interceptors.request.use(
  async (config) => {
    if (isTauriRuntime() && !apiConfigManager.isReady()) {
      await apiConfigManager.waitForReady()
    }

    config.baseURL = apiConfigManager.getBaseUrl()
    // Add request ID for tracing
    config.metadata = { startTime: Date.now() }
    return config
  },
  (error) => {
    errorHandler.handleError(error, 'RequestInterceptor')
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Log request duration
    if (response.config.metadata?.startTime) {
      const duration = Date.now() - response.config.metadata.startTime
      if (duration > 5000) { // Requests over 5s
        console.warn(`Slow API request: ${response.config.url} took ${duration}ms`)
      }
    }
    
    return response.data
  },
  async (error) => {
    if (shouldRetry(error)) {
      const currentRetryCount = error.config?.metadata?.retryCount || 0
      if (currentRetryCount < MAX_RETRIES) {
        error.config.metadata = {
          ...(error.config.metadata || { startTime: Date.now() }),
          retryCount: currentRetryCount + 1,
        }
        await new Promise((resolve) => setTimeout(resolve, getRetryDelay(currentRetryCount)))
        return api.request(error.config)
      }
    }

    // Use the unified error handler
    errorHandler.handleError(error, 'API')
    
    // Keep original error shape for backward compat
    if (error.response?.status === 429) {
      const message = error.response?.data?.detail || 'System is handling other projects, please try again later'
      error.userMessage = message
    }
    else if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
      error.userMessage = 'Request timed out; the project may still be processing in the background - check its status shortly'
    }
    else if (error.code === 'NETWORK_ERROR' || !error.response) {
      error.userMessage = 'Network connection failed, please check your network'
    }
    else if (error.response?.status >= 500) {
      error.userMessage = 'Internal server error, please try again later'
    }
    
    return Promise.reject(error)
  }
)

export interface UploadFilesRequest {
  video_file: File
  srt_file?: File
  project_name: string
  video_category?: string
}

export interface VideoCategory {
  value: string
  name: string
  description: string
  icon: string
  color: string
}

export interface VideoCategoriesResponse {
  categories: VideoCategory[]
  default_category: string
}

export interface ProcessingStatus {
  status: 'processing' | 'completed' | 'error'
  current_step: number
  total_steps: number
  step_name: string
  progress: number
  error_message?: string
}

// Bilibili API types
export interface BilibiliVideoInfo {
  title: string
  description: string
  duration: number
  uploader: string
  upload_date: string
  view_count: number
  like_count: number
  thumbnail: string
  url: string
}

export interface BilibiliDownloadRequest {
  url: string
  project_name: string
  video_category?: string
  browser?: string
}

export interface BilibiliDownloadTask {
  id: string
  url: string
  project_name: string
  video_category?: string
  browser?: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  progress: number
  error_message?: string
  video_info?: BilibiliVideoInfo
  project_id?: string
  created_at: string
  updated_at: string
}

// Settings API
export const settingsApi = {
  // Get system settings
  getSettings: (): Promise<any> => {
    return api.get('/settings')
  },

  // Update system settings
  updateSettings: (settings: any): Promise<any> => {
    return api.put('/settings/', settings)
  },

  // Test API key
  testApiKey: (
    provider: string,
    apiKey: string,
    options: { baseUrl?: string; model?: string } = {}
  ): Promise<{ success: boolean; error?: string }> => {
    return api.post('/settings/test-api', { 
      provider, 
      api_key: apiKey,
      base_url: options.baseUrl,
      model: options.model,
    })
  },

  // Get all available models
  getAvailableModels: (): Promise<any> => {
    return api.get('/settings/available-models')
  },

  // Get current provider info
  getCurrentProvider: (): Promise<any> => {
    return api.get('/settings/current-provider')
  },

  // Models actually served by local OpenAI-compatible service (Ollama / LM Studio / vLLM)
  listCompatibleModels: (
    params: { provider?: string; baseUrl?: string; apiKey?: string }
  ): Promise<{ reachable: boolean; base_url: string; models: string[]; error?: string }> => {
    return api.get('/settings/compatible-models', {
      params: { provider: params.provider, base_url: params.baseUrl, api_key: params.apiKey },
    })
  },

  // Check desktop mode
  checkDesktopMode: (): Promise<{ is_desktop_mode: boolean; environment: any }> => {
    return api.get('/settings/desktop-mode')
  }
}

// Project API
export const projectApi = {
  // Get video category config
  getVideoCategories: async (): Promise<VideoCategoriesResponse> => {
    return api.get('/video-categories')
  },

  // Get all projects
  getProjects: async (): Promise<Project[]> => {
    const response = await api.get('/projects/')
    // Handle paginated response, return items array
    return (response as any).items || response || []
  },

  // Get a single project
  getProject: async (id: string): Promise<Project> => {
    return api.get(`/projects/${id}`)
  },

  // Upload files and create a project
  uploadFiles: async (data: UploadFilesRequest): Promise<Project> => {
    const formData = new FormData()
    formData.append('video_file', data.video_file)
    if (data.srt_file) {
      formData.append('srt_file', data.srt_file)
    }
    formData.append('project_name', data.project_name)
    if (data.video_category) {
      formData.append('video_category', data.video_category)
    }
    
    try {
      const project = await api.post<unknown, Project>('/projects/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      trackVideoImported({
        source: 'upload',
        fileType: data.video_file?.type || undefined,
        sizeBytes: data.video_file?.size,
      })
      return project
    } catch (error: any) {
      trackProcessingFailed({
        stage: 'import',
        message: error?.message,
        code: error?.response?.status,
      })
      throw error
    }
  },

  // Delete a project
  deleteProject: async (id: string): Promise<void> => {
    await api.delete(`/projects/${id}`)
  },

  // Start processing a project
  startProcessing: async (id: string): Promise<void> => {
    await api.post(`/projects/${id}/process`)
  },

  // Retry processing a project
  retryProcessing: async (id: string): Promise<void> => {
    await api.post(`/projects/${id}/retry`)
  },

  // Get processing status
  getProcessingStatus: async (id: string): Promise<ProcessingStatus> => {
    return api.get(`/projects/${id}/status`)
  },

  // Get project logs
  getProjectLogs: async (id: string, lines: number = 50): Promise<{logs: Array<{timestamp: string, module: string, level: string, message: string}>}> => {
    return api.get(`/projects/${id}/logs?lines=${lines}`)
  },

  // Get project clips
  getClips: async (projectId: string): Promise<any[]> => {
    try {
      // Fetch only from DB, no longer falling back to filesystem
      console.log('🔍 Calling clips API for project:', projectId)
      const response = await api.get(`/clips/?project_id=${projectId}`)
      console.log('📦 Raw API response:', response)
      const clips = (response as any).items || response || []
      console.log('📋 Extracted clips:', clips.length, 'clips found')
      
      // Convert backend format to the frontend-expected shape
      const convertedClips = clips.map((clip: any) => {
        // Convert seconds to a time string
        const formatSecondsToTime = (seconds: number) => {
          const hours = Math.floor(seconds / 3600)
          const minutes = Math.floor((seconds % 3600) / 60)
          const secs = Math.floor(seconds % 60)
          return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
        }
        
        // Get content from metadata
        const metadata = clip.clip_metadata || {}
        
        return {
          id: clip.id,
          title: clip.title,
          generated_title: clip.title,
          start_time: formatSecondsToTime(clip.start_time),
          end_time: formatSecondsToTime(clip.end_time),
          duration: clip.duration || 0,
          final_score: clip.score || 0,
          recommend_reason: metadata.recommend_reason || '',
          outline: metadata.outline || '',
          // Use only metadata.content; avoid description (may be transcript)
          content: metadata.content || [],
          chunk_index: metadata.chunk_index || 0
        }
      })
      
      console.log('✅ Converted clips:', convertedClips.length, 'clips')
      console.log('📄 First clip sample:', convertedClips[0])
      return convertedClips
    } catch (error) {
      console.error('❌ Failed to get clips:', error)
      return []
    }
  },

  // Get project collections
  getCollections: async (projectId: string): Promise<any[]> => {
    try {
      // Fetch only from DB, no longer falling back to filesystem
      const response = await api.get(`/collections/?project_id=${projectId}`)
      const collections = (response as any).items || response || []
      
      // Convert backend format to the frontend-expected shape
      return collections.map((collection: any) => ({
        id: collection.id,
        collection_title: collection.name || collection.collection_title || '',
        collection_summary: collection.description || collection.collection_summary || '',
        clip_ids: collection.clip_ids || collection.metadata?.clip_ids || [],
        collection_type: collection.collection_type || 'ai_recommended',
        created_at: collection.created_at,
        project_id: collection.project_id,
        thumbnail_path: collection.thumbnail_path
      }))
    } catch (error) {
      console.error('Failed to get collections:', error)
      return []
    }
  },

  // Restart a specific step
  restartStep: async (id: string, step: number): Promise<void> => {
    await api.post(`/projects/${id}/restart-step`, { step })
  },

  // Update clip info
  updateClip: (projectId: string, clipId: string, updates: Partial<Clip>): Promise<Clip> => {
    return api.patch(`/projects/${projectId}/clips/${clipId}`, updates)
  },

  // Update clip title
  updateClipTitle: async (clipId: string, title: string): Promise<any> => {
    return api.patch(`/clips/${clipId}/title`, { title })
  },

  // Generate clip title
  generateClipTitle: async (clipId: string): Promise<{clip_id: string, generated_title: string, success: boolean}> => {
    return api.post(`/clips/${clipId}/generate-title`)
  },

  // Create a collection
  createCollection: (projectId: string, collectionData: { collection_title: string, collection_summary: string, clip_ids: string[] }): Promise<Collection> => {
    return api.post(`/collections/`, {
      project_id: projectId,
      name: collectionData.collection_title,
      description: collectionData.collection_summary,
      clip_ids: collectionData.clip_ids,
      collection_type: 'manual'
    })
  },

  // Update collection info
  updateCollection: (_projectId: string, collectionId: string, updates: Partial<Collection>): Promise<Collection> => {
    return api.put(`/collections/${collectionId}`, updates)
  },

  // Reorder collection clips
  reorderCollectionClips: (projectId: string, collectionId: string, clipIds: string[]): Promise<Collection> => {
    return api.patch(`/projects/${projectId}/collections/${collectionId}/reorder`, clipIds)
  },

  // Delete a collection
  deleteCollection: (_projectId: string, collectionId: string): Promise<{message: string, deleted_collection: string}> => {
    return api.delete(`/collections/${collectionId}`)
  },

  // Generate collection title
  generateCollectionTitle: (collectionId: string): Promise<{collection_id: string, generated_title: string, success: boolean}> => {
    return api.post(`/collections/${collectionId}/generate-title`)
  },

  // Update collection title
  updateCollectionTitle: (collectionId: string, title: string): Promise<{collection_id: string, title: string, success: boolean}> => {
    return api.put(`/collections/${collectionId}/title`, { title })
  },

  // Download clip video
  downloadClip: (_projectId: string, clipId: string): Promise<Blob> => {
    return api.get(`/files/projects/${_projectId}/clips/${clipId}`, {
      responseType: 'blob'
    })
  },

  // Download collection video
  downloadCollection: (projectId: string, collectionId: string): Promise<Blob> => {
    return api.get(`/files/projects/${projectId}/collections/${collectionId}`, {
      responseType: 'blob'
    })
  },

  // Export metadata
  exportMetadata: (projectId: string): Promise<Blob> => {
    return api.get(`/projects/${projectId}/export`, {
      responseType: 'blob'
    })
  },

  // Generate collection video
  generateCollectionVideo: (projectId: string, collectionId: string) => {
    return api.post(`/projects/${projectId}/collections/${collectionId}/generate`)
  },

  downloadVideo: async (projectId: string, clipId?: string, collectionId?: string) => {
    let url = `/projects/${projectId}/download`
    if (clipId) {
      url += `?clip_id=${clipId}`
    } else if (collectionId) {
      url += `?collection_id=${collectionId}`
    }
    
    try {
      // For blob responses, use axios directly instead of the interceptor
      const response = await axios.get(`/api/v1${url}`, { 
        responseType: 'blob',
        headers: {
          'Accept': 'application/octet-stream'
        }
      })
      
      // Get filename from response header; fallback to default
      const contentDisposition = response.headers['content-disposition']
      let filename = clipId ? `clip_${clipId}.mp4` : 
                     collectionId ? `collection_${collectionId}.mp4` : 
                     `project_${projectId}.mp4`
      
      if (contentDisposition) {
        // Try RFC 6266 filename* first
        const filenameStarMatch = contentDisposition.match(/filename\*=UTF-8''([^;]+)/)
        if (filenameStarMatch) {
          filename = decodeURIComponent(filenameStarMatch[1])
        } else {
          // Fallback to legacy filename param
          const filenameMatch = contentDisposition.match(/filename="([^"]+)"/)
          if (filenameMatch) {
            filename = filenameMatch[1]
          }
        }
      }
      
      // Create download link
      const blob = new Blob([response.data], { type: 'video/mp4' })
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename
      
      // Trigger download
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)

      trackClipsExported({
        clipCount: 1,
        // Distinguish export scope: clip / collection / project
        exportType: clipId ? 'clip' : collectionId ? 'collection' : 'project',
      })
      return response.data
    } catch (error: any) {
      console.error('Download failed:', error)
      trackProcessingFailed({
        stage: 'export',
        message: error?.message,
        code: error?.response?.status,
      })
      throw error
    }
  },

  // Get project file URL
  getProjectFileUrl: (projectId: string, filename: string): string => {
    return `${api.defaults.baseURL}/projects/${projectId}/files/${filename}`
  },

  // Get project video URL
  getProjectVideoUrl: (projectId: string): string => {
    return `${api.defaults.baseURL}/projects/${projectId}/video`
  },

  // Get clip video URL
  getClipVideoUrl: (projectId: string, clipId: string, _clipTitle?: string): string => {
    // Fetch clip video via the projects route
    return `/api/v1/projects/${projectId}/clips/${clipId}`
  },

  // Get collection video URL
  getCollectionVideoUrl: (projectId: string, collectionId: string): string => {
    // Fetch collection video via the files route
    return `/api/v1/files/projects/${projectId}/collections/${collectionId}`
  },

  // Generate project thumbnail
  generateThumbnail: async (projectId: string): Promise<{success: boolean, thumbnail: string, message: string}> => {
    return api.post(`/projects/${projectId}/generate-thumbnail`)
  },

  startClipExport: async (
    projectId: string,
    clipId: string,
    body: { preset: string; subtitles?: boolean; title_card?: boolean }
  ): Promise<{ ok: boolean; job_id: string; status: string }> => {
    return api.post(`/projects/${projectId}/clips/${clipId}/export`, body)
  },

  getExportJob: async (projectId: string, jobId: string): Promise<{
    job_id: string
    status: 'queued' | 'running' | 'completed' | 'failed'
    percent?: number
    error?: string
    result?: { path: string; title?: string; width?: number; height?: number; warnings?: string[] }
  }> => {
    return api.get(`/projects/${projectId}/exports/${jobId}`)
  },

  downloadExport: async (projectId: string, jobId: string) => {
    const response = await axios.get(`/api/v1/projects/${projectId}/exports/${jobId}/download`, {
      responseType: 'blob',
      headers: { Accept: 'application/octet-stream' },
    })
    const cd = response.headers['content-disposition'] || ''
    let filename = `export_${jobId.slice(0, 8)}.mp4`
    const star = cd.match(/filename\*=UTF-8''([^;]+)/)
    const plain = cd.match(/filename="([^"]+)"/)
    if (star) filename = decodeURIComponent(star[1])
    else if (plain) filename = plain[1]
    const url = window.URL.createObjectURL(new Blob([response.data], { type: 'video/mp4' }))
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  },
}

// Video download API
export const bilibiliApi = {
  // Parse Bilibili video info
  parseVideoInfo: async (url: string, browser?: string): Promise<{success: boolean, video_info: BilibiliVideoInfo}> => {
    const formData = new FormData()
    formData.append('url', url)
    if (browser) {
      formData.append('browser', browser)
    }
    return api.post('/bilibili/parse', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // Parse YouTube video info
  parseYouTubeVideoInfo: async (url: string, browser?: string): Promise<{success: boolean, video_info: BilibiliVideoInfo}> => {
    const formData = new FormData()
    formData.append('url', url)
    if (browser) {
      formData.append('browser', browser)
    }
    return api.post('/youtube/parse', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // Create a Bilibili download task
  createDownloadTask: async (data: BilibiliDownloadRequest): Promise<BilibiliDownloadTask> => {
    const task = await api.post<unknown, BilibiliDownloadTask>('/bilibili/download', data)
    trackVideoImported({ source: 'url', fileType: 'bilibili' })
    return task
  },

  // Create a YouTube download task
  createYouTubeDownloadTask: async (data: BilibiliDownloadRequest): Promise<BilibiliDownloadTask> => {
    const task = await api.post<unknown, BilibiliDownloadTask>('/youtube/download', data)
    trackVideoImported({ source: 'url', fileType: 'youtube' })
    return task
  },

  // Get download task status
  getTaskStatus: async (taskId: string): Promise<BilibiliDownloadTask> => {
    return api.get(`/bilibili/tasks/${taskId}`)
  },

  // Get YouTube download task status
  getYouTubeTaskStatus: async (taskId: string): Promise<BilibiliDownloadTask> => {
    return api.get(`/youtube/tasks/${taskId}`)
  },

  // Get all download tasks
  getAllTasks: async (): Promise<BilibiliDownloadTask[]> => {
    return api.get('/bilibili/tasks')
  },

  // Get all YouTube download tasks
  getAllYouTubeTasks: async (): Promise<BilibiliDownloadTask[]> => {
    return api.get('/youtube/tasks')
  }
}

// System status API
export const systemApi = {
  // Get system status
  getSystemStatus: (): Promise<{
    current_processing_count: number
    max_concurrent_processing: number
    total_projects: number
    processing_projects: string[]
  }> => {
    return api.get('/system/status')
  }
}

export interface WhisperRuntimeStatus {
  status: 'unknown' | 'not_installed' | 'installing' | 'installed' | 'error'
  progress: number
  message: string
  log_tail?: string
  platform_supported: boolean
  packages: string[]
}

export interface WhisperModel {
  name: string
  size: string
  sizeBytes: number
  description: string
  accuracy: string
  speed: string
  status: 'available' | 'downloading' | 'downloaded' | 'error' | 'not_found'
  downloadProgress?: number | null
  localPath?: string | null
  errorMessage?: string | null
}

// Speech recognition / Whisper runtime & model management
export const speechApi = {
  getRuntimeStatus: (): Promise<WhisperRuntimeStatus> => api.get('/whisper/runtime-status'),
  installRuntime: (): Promise<{ started: boolean; message: string }> => api.post('/whisper/install'),
  uninstallRuntime: (): Promise<{ success: boolean; message: string }> => api.post('/whisper/uninstall'),
  getModels: (): Promise<WhisperModel[]> => api.get('/whisper-models'),
  downloadModel: (model: string): Promise<unknown> => api.post('/whisper-models/download', { model }),
  deleteModel: (model: string): Promise<unknown> => api.delete(`/whisper-models/${model}`),
}

export default api
