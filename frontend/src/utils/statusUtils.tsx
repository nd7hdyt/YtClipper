/**
 * translatedone'sstatusprocesstool
 * translatedfrontendprojecttranslatedstatusprocesstranslatedonetranslated'sissue
 */

import { 
  ClockCircleOutlined, 
  LoadingOutlined, 
  CheckCircleOutlined, 
  ExclamationCircleOutlined,
  CloseCircleOutlined,
  PlayCircleOutlined
} from '@ant-design/icons'

// translatedone'sstatustranslated
export type ProjectStatus = 'pending' | 'processing' | 'completed' | 'failed'
export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
export type UploadStatus = 'pending' | 'processing' | 'success' | 'failed'

// projectstatusconfig
export interface ProjectStatusConfig {
  color: string
  icon: any
  text: string
  badgeStatus: 'default' | 'processing' | 'success' | 'error'
  backgroundColor: string
  borderColor: string
}

// taskstatusconfig
export interface TaskStatusConfig {
  color: string
  icon: any
  text: string
  badgeStatus: 'default' | 'processing' | 'success' | 'error'
}

// Uploadstatusconfig
export interface UploadStatusConfig {
  color: string
  icon: any
  text: string
  badgeStatus: 'default' | 'processing' | 'success' | 'error'
}

/**
 * fetchprojectstatusconfig
 */
export const getProjectStatusConfig = (status: ProjectStatus): ProjectStatusConfig => {
  switch (status) {
    case 'pending':
      return {
        color: '#1890ff',
        icon: ClockCircleOutlined,
        text: 'etc.translated',
        badgeStatus: 'processing',
        backgroundColor: 'rgba(217, 217, 217, 0.15)',
        borderColor: 'rgba(217, 217, 217, 0.3)'
      }
    case 'processing':
      return {
        color: '#1890ff',
        icon: LoadingOutlined,
        text: 'processing',
        badgeStatus: 'processing',
        backgroundColor: 'rgba(24, 144, 255, 0.15)',
        borderColor: 'rgba(24, 144, 255, 0.3)'
      }
    case 'completed':
      return {
        color: '#52c41a',
        icon: CheckCircleOutlined,
        text: 'completed',
        badgeStatus: 'success',
        backgroundColor: 'rgba(82, 196, 26, 0.15)',
        borderColor: 'rgba(82, 196, 26, 0.3)'
      }
    case 'failed':
      return {
        color: '#ff4d4f',
        icon: ExclamationCircleOutlined,
        text: 'failed',
        badgeStatus: 'error',
        backgroundColor: 'rgba(255, 77, 79, 0.15)',
        borderColor: 'rgba(255, 77, 79, 0.3)'
      }
    default:
      return {
        color: '#d9d9d9',
        icon: ClockCircleOutlined,
        text: 'translatedstatus',
        badgeStatus: 'default',
        backgroundColor: 'rgba(217, 217, 217, 0.15)',
        borderColor: 'rgba(217, 217, 217, 0.3)'
      }
  }
}

/**
 * fetchtaskstatusconfig
 */
export const getTaskStatusConfig = (status: TaskStatus): TaskStatusConfig => {
  switch (status) {
    case 'pending':
      return {
        color: '#1890ff',
        icon: ClockCircleOutlined,
        text: 'etc.translated',
        badgeStatus: 'processing'
      }
    case 'running':
      return {
        color: '#1890ff',
        icon: PlayCircleOutlined,
        text: 'translated',
        badgeStatus: 'processing'
      }
    case 'completed':
      return {
        color: '#52c41a',
        icon: CheckCircleOutlined,
        text: 'completed',
        badgeStatus: 'success'
      }
    case 'failed':
      return {
        color: '#ff4d4f',
        icon: CloseCircleOutlined,
        text: 'failed',
        badgeStatus: 'error'
      }
    case 'cancelled':
      return {
        color: '#d9d9d9',
        icon: CloseCircleOutlined,
        text: 'translatedcancel',
        badgeStatus: 'default'
      }
    default:
      return {
        color: '#d9d9d9',
        icon: ClockCircleOutlined,
        text: 'translatedstatus',
        badgeStatus: 'default'
      }
  }
}

/**
 * fetchUploadstatusconfig
 */
export const getUploadStatusConfig = (status: UploadStatus): UploadStatusConfig => {
  switch (status) {
    case 'pending':
      return {
        color: '#1890ff',
        icon: ClockCircleOutlined,
        text: 'translatedprocess',
        badgeStatus: 'processing'
      }
    case 'processing':
      return {
        color: '#1890ff',
        icon: LoadingOutlined,
        text: 'processing',
        badgeStatus: 'processing'
      }
    case 'success':
      return {
        color: '#52c41a',
        icon: CheckCircleOutlined,
        text: 'succeeded',
        badgeStatus: 'success'
      }
    case 'failed':
      return {
        color: '#ff4d4f',
        icon: CloseCircleOutlined,
        text: 'failed',
        badgeStatus: 'error'
      }
    default:
      return {
        color: '#d9d9d9',
        icon: ClockCircleOutlined,
        text: 'translatedstatus',
        badgeStatus: 'default'
      }
  }
}

/**
 * fetchprogresstranslatedstatus
 */
export const getProgressStatus = (status: ProjectStatus | TaskStatus | UploadStatus): 'normal' | 'active' | 'success' | 'exception' => {
  switch (status) {
    case 'processing':
    case 'running':
      return 'active'
    case 'completed':
    case 'success':
      return 'success'
    case 'failed':
      return 'exception'
    default:
      return 'normal'
  }
}

/**
 * translatedprojectprogresstranslated
 */
export const calculateProjectProgress = (
  status: ProjectStatus, 
  currentStep?: number, 
  totalSteps?: number
): number => {
  if (status === 'completed') return 100
  if (status === 'failed') return 0
  if (currentStep && totalSteps && totalSteps > 0) {
    return Math.round((currentStep / totalSteps) * 100)
  }
  return 0
}

/**
 * statustranslated
 * translated'sstatustranslated'stranslatedonestatustranslated
 */
export const normalizeProjectStatus = (status: string): ProjectStatus => {
  switch (status) {
    case 'error':
      return 'failed'
    case 'pending':
    case 'processing':
    case 'completed':
    case 'failed':
      return status as ProjectStatus
    default:
      return 'pending'
  }
}

export const normalizeTaskStatus = (status: string): TaskStatus => {
  switch (status) {
    case 'pending':
    case 'running':
    case 'completed':
    case 'failed':
    case 'cancelled':
      return status as TaskStatus
    default:
      return 'pending'
  }
}
