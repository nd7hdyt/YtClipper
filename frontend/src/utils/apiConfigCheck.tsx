/**
 * API config check utility
 * Check whether API config is complete before creating a project
 */

import { settingsApi } from '../services/api'
import { isDesktopMode } from './desktopMode'
import { message, Modal } from 'antd'
import { useNavigate } from 'react-router-dom'

export interface ApiConfigStatus {
  hasValidConfig: boolean
  missingProviders: string[]
  currentProvider?: string
  currentApiKey?: string
}

/**
 * Check whether API config is complete
 */
export const checkApiConfig = async (): Promise<ApiConfigStatus> => {
  try {
    console.log('=== Starting API config check ===')
    
    // Check whether running in desktop mode
    const isDesktop = await isDesktopMode()
    console.log('Desktop mode check:', isDesktop)
    
    // Try to fetch settings regardless of desktop mode
    let settings
    try {
      settings = await settingsApi.getSettings()
      console.log('Fetch settings succeeded:', settings)
    } catch (error) {
      console.warn('Failed to fetch settings, maybe not in desktop mode:', error)
      // If fetching settings failed, check desktop mode
      if (!isDesktop) {
        console.log('Not desktop mode, returning no-config status')
        return {
          hasValidConfig: false,
          missingProviders: ['LLM API'],
          currentProvider: undefined,
          currentApiKey: undefined
        }
      }
      // Fetch failed in desktop mode, also return no-config
      console.log('Failed to fetch settings in desktop mode, returning no-config status')
      return {
        hasValidConfig: false,
        missingProviders: ['LLM API'],
        currentProvider: undefined,
        currentApiKey: undefined
      }
    }
    
    if (!settings || !settings.api || !settings.api.api_keys) {
      console.log('Incomplete settings data:', { settings, hasApi: !!settings?.api, hasApiKeys: !!settings?.api?.api_keys })
      return {
        hasValidConfig: false,
        missingProviders: ['LLM API'],
        currentProvider: undefined,
        currentApiKey: undefined
      }
    }

    const apiKeys = settings.api.api_keys
    // Fix: api_model is the model name, not the provider
    // Provider comes from api_provider or llm_provider
    const currentProvider = settings.api.api_provider || settings.api.llm_provider || 'dashscope'
    
    console.log('API config details:', {
      currentProvider,
      apiKeys: {
        dashscope: apiKeys.dashscope ? '***' + apiKeys.dashscope.slice(-4) : 'Not configured',
        openai: apiKeys.openai ? '***' + apiKeys.openai.slice(-4) : 'Not configured',
        gemini: apiKeys.gemini ? '***' + apiKeys.gemini.slice(-4) : 'Not configured',
        siliconflow: apiKeys.siliconflow ? '***' + apiKeys.siliconflow.slice(-4) : 'Not configured',
        jimeng_access: apiKeys.jimeng_access ? '***' + apiKeys.jimeng_access.slice(-4) : 'Not configured',
        jimeng_secret: apiKeys.jimeng_secret ? '***' + apiKeys.jimeng_secret.slice(-4) : 'Not configured'
      }
    })
    
    // Check current provider's API key
    let currentApiKey = ''
    let hasValidKey = false
    
    switch (currentProvider) {
      case 'dashscope':
        currentApiKey = apiKeys.dashscope || ''
        hasValidKey = !!currentApiKey.trim()
        console.log('DashScope API key check:', { hasKey: !!currentApiKey, keyLength: currentApiKey.length, isValid: hasValidKey })
        break
      case 'openai': {
        currentApiKey = apiKeys.openai || ''
        // Self-hosted OpenAI-compatible services (Ollama / vLLM etc.) may have no key; a base URL is enough
        const hasCustomBaseUrl = !!(settings.api.api_base_url || '').trim()
        hasValidKey = !!currentApiKey.trim() || hasCustomBaseUrl
        console.log('OpenAI API key check:', { hasKey: !!currentApiKey, keyLength: currentApiKey.length, hasCustomBaseUrl, isValid: hasValidKey })
        break
      }
      case 'gemini':
        currentApiKey = apiKeys.gemini || ''
        hasValidKey = !!currentApiKey.trim()
        console.log('Gemini API key check:', { hasKey: !!currentApiKey, keyLength: currentApiKey.length, isValid: hasValidKey })
        break
      case 'siliconflow':
        currentApiKey = apiKeys.siliconflow || ''
        hasValidKey = !!currentApiKey.trim()
        console.log('SiliconFlow API key check:', { hasKey: !!currentApiKey, keyLength: currentApiKey.length, isValid: hasValidKey })
        break
      case 'jimeng':
        currentApiKey = apiKeys.jimeng_access || ''
        hasValidKey = !!(apiKeys.jimeng_access?.trim() && apiKeys.jimeng_secret?.trim())
        console.log('Jimeng API key check:', { 
          hasAccess: !!apiKeys.jimeng_access, 
          hasSecret: !!apiKeys.jimeng_secret, 
          isValid: hasValidKey 
        })
        break
      default:
        hasValidKey = false
        console.log('Unknown provider:', currentProvider)
    }

    console.log('=== API config check final result ===', {
      hasValidConfig: hasValidKey,
      currentProvider,
      currentApiKey: currentApiKey ? '***' + currentApiKey.slice(-4) : undefined,
      isDesktop
    })

    return {
      hasValidConfig: hasValidKey,
      missingProviders: hasValidKey ? [] : ['LLM API'],
      currentProvider,
      currentApiKey: currentApiKey ? '***' + currentApiKey.slice(-4) : undefined
    }
  } catch (error) {
    console.error('API config check failed:', error)
    return {
      hasValidConfig: false,
      missingProviders: ['LLM API'],
      currentProvider: undefined,
      currentApiKey: undefined
    }
  }
}

/**
 * Show a dialog for missing API config
 */
export const showApiConfigModal = (missingProviders: string[], onNavigateToSettings?: () => void) => {
  const providerNames = {
    'LLM API': 'AI model API',
    'Speech API': 'Speech recognition API'
  }

  const missingNames = missingProviders.map(p => providerNames[p as keyof typeof providerNames] || p).join(', ')

  Modal.confirm({
    title: <span style={{ color: '#fff' }}>API config required</span>,
    content: (
      <div style={{ color: '#fff' }}>
        <p style={{ color: '#fff', marginBottom: '12px', fontSize: '14px' }}>Creating a project requires these APIs:</p>
        <p style={{ fontWeight: 'bold', color: '#40a9ff', marginBottom: '12px', fontSize: '16px' }}>{missingNames}</p>
        <p style={{ color: '#f0f0f0', fontSize: '14px' }}>Please configure them in Settings.</p>
      </div>
    ),
    okText: 'Go to Settings',
    cancelText: 'Cancel',
    onOk: () => {
      if (onNavigateToSettings) {
        onNavigateToSettings()
      } else {
        // Go to Settings
        window.location.href = '#/settings'
        // Hard reload to ensure navigation
        window.location.reload()
      }
    },
    icon: null,
    centered: true,
    style: { backgroundColor: '#1f1f1f' }
  })
}

/**
 * Check API config before creating a project
 * If incomplete, show a prompt and block creation
 */
export const validateApiConfigBeforeProjectCreation = async (): Promise<boolean> => {
  console.log('Validating API config...')
  const configStatus = await checkApiConfig()
  
  console.log('API config validation result:', configStatus)
  
  if (!configStatus.hasValidConfig) {
    console.log('API config invalid, showing dialog')
    showApiConfigModal(configStatus.missingProviders)
    return false
  }
  
  console.log('API config valid, allowing project creation')
  return true
}

/**
 * Friendly description for API config status
 */
export const getApiConfigDescription = (status: ApiConfigStatus): string => {
  if (status.hasValidConfig) {
    return `Configured ${status.currentProvider} API`
  } else {
    return 'API not configured, cannot create project'
  }
}
