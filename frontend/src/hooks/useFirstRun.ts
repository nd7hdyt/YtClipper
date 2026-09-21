import { useState, useEffect } from 'react'

interface FirstRunState {
  isFirstRun: boolean
  isLoading: boolean
  hasCompleted: boolean
}

export const useFirstRun = () => {
  const [state, setState] = useState<FirstRunState>({
    isFirstRun: false,
    isLoading: true,
    hasCompleted: false
  })

  useEffect(() => {
    checkFirstRun()
  }, [])

  const checkFirstRun = async () => {
    try {
      console.log('🔍 translatedchecktranslatedstatus...')
      
      // createtranslated'sfetchtranslated
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000) // 5secondstranslated
      
      try {
        // checkIstranslatedconfig
        const response = await fetch('/api/v1/settings/', {
          signal: controller.signal
        })
        clearTimeout(timeoutId)
        
        if (response.ok) {
          const settings = await response.json()
          console.log('📋 fetchtranslatedsettings:', settings)
          
          // checkIstranslatedAPI Keyconfig
          const hasApiKey = settings.api?.api_keys?.dashscope || 
                           settings.api?.api_keys?.openai ||
                           settings.api?.api_keys?.gemini ||
                           settings.api?.api_keys?.siliconflow ||
                           // local / translated OpenAI translatedservicecantranslated key，translated
                           (settings.api?.api_provider === 'openai' && settings.api?.api_base_url)
          
          console.log('🔑 API Keystatus:', hasApiKey)
          
          // translatedcheckAPI Keyconfig，No needtranslatedproject
          setState({
            isFirstRun: !hasApiKey,
            isLoading: false,
            hasCompleted: hasApiKey
          })
        } else {
          console.log('❌ settingsAPItranslatedfailed:', response.status)
          // iftranslatedfetchsettings，translatedIstranslated
          setState({
            isFirstRun: true,
            isLoading: false,
            hasCompleted: false
          })
        }
      } catch (fetchError) {
        clearTimeout(timeoutId)
        if (fetchError instanceof Error && fetchError.name === 'AbortError') {
          console.log('⏰ APItranslated，translated')
        } else {
          console.log('❌ APItranslatedfailed:', fetchError)
        }
        setState({
          isFirstRun: true,
          isLoading: false,
          hasCompleted: false
        })
      }
    } catch (error) {
      console.error('❌ checktranslatedstatusfailed:', error)
      setState({
        isFirstRun: true,
        isLoading: false,
        hasCompleted: false
      })
    }
  }

  const markCompleted = () => {
    setState(prev => ({
      ...prev,
      isFirstRun: false,
      hasCompleted: true
    }))
  }

  return {
    ...state,
    markCompleted,
    refresh: checkFirstRun
  }
}
