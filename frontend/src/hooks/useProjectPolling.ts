import { useEffect, useRef, useState } from 'react'
import { projectApi } from '../services/api'
import { Project, useProjectStore } from '../store/useProjectStore'

interface UseProjectPollingOptions {
  interval?: number // translated，default10seconds
  onProjectsUpdate?: (projects: Project[]) => void
  enabled?: boolean // Istranslatedusetranslated
}

export const useProjectPolling = ({
  interval = 30000, // default30seconds，translated
  onProjectsUpdate,
  enabled = true
}: UseProjectPollingOptions = {}) => {
  const [isPolling, setIsPolling] = useState(false)
  const intervalRef = useRef<number | null>(null)
  const [lastUpdateTime, setLastUpdateTime] = useState<number>(Date.now())

    const startPolling = () => {
    if (!enabled || intervalRef.current) return

    setIsPolling(true)
    
    const poll = async () => {
      try {
        // translatedfetchisDraggingstatus
        const currentIsDragging = useProjectStore.getState().isDragging
        
        // iftranslatedintranslated，skipthistranslated
        if (currentIsDragging) {
          console.log('Skipping poll: dragging in progress')
          return
        }
        
        console.log('Polling projects...')
        const projects = await projectApi.getProjects()
        console.log('Polled projects:', projects)
        
        // ensureprojectsIstranslated
        const safeProjects = Array.isArray(projects) ? projects : []
        const hasProcessingProjects = safeProjects.some(p => p.status === 'processing')
        
        if (onProjectsUpdate) {
          console.log('Calling onProjectsUpdate with:', safeProjects)
          onProjectsUpdate(safeProjects)
        }
        
        setLastUpdateTime(Date.now())
        
        // translated：iftranslatedinprocess'sproject，translated
        if (!hasProcessingProjects) {
          // iftranslatedproject，cantranslatedonetranslated
          console.log('translatedproject，translated')
        }
      } catch (error) {
        console.error('Polling error:', error)
      }
    }

    // translatedonetranslated
    poll()
    
    // settingstranslated
    intervalRef.current = window.setInterval(poll, interval)
  }

  const stopPolling = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
    setIsPolling(false)
  }

  const refreshNow = async () => {
    try {
      const projects = await projectApi.getProjects()
      // ensureprojectsIstranslated
      const safeProjects = Array.isArray(projects) ? projects : []
      if (onProjectsUpdate) {
        onProjectsUpdate(safeProjects)
      }
      setLastUpdateTime(Date.now())
      return safeProjects
    } catch (error) {
      console.error('Manual refresh error:', error)
      throw error
    }
  }

  useEffect(() => {
    if (enabled) {
      startPolling()
    } else {
      stopPolling()
    }

    return () => {
      stopPolling()
    }
  }, [enabled, interval])

  return {
    isPolling,
    lastUpdateTime,
    startPolling,
    stopPolling,
    refreshNow
  }
}

export default useProjectPolling