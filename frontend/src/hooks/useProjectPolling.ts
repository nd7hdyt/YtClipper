import { useEffect, useRef, useState } from 'react'
import { projectApi } from '../services/api'
import { Project, useProjectStore } from '../store/useProjectStore'

interface UseProjectPollingOptions {
  interval?: number // EN，EN10EN
  onProjectsUpdate?: (projects: Project[]) => void
  enabled?: boolean // EN
}

export const useProjectPolling = ({
  interval = 30000, // EN30EN，ENrequest
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
        // ENfetchisDraggingStatus
        const currentIsDragging = useProjectStore.getState().isDragging
        
        // ENDrag，EN
        if (currentIsDragging) {
          console.log('Skipping poll: dragging in progress')
          return
        }
        
        console.log('Polling projects...')
        const projects = await projectApi.getProjects()
        console.log('Polled projects:', projects)
        
        // ensureprojectsEN
        const safeProjects = Array.isArray(projects) ? projects : []
        const hasProcessingProjects = safeProjects.some(p => p.status === 'processing')
        
        if (onProjectsUpdate) {
          console.log('Calling onProjectsUpdate with:', safeProjects)
          onProjectsUpdate(safeProjects)
        }
        
        setLastUpdateTime(Date.now())
        
        // EN：ENProcessingENproject，EN
        if (!hasProcessingProjects) {
          // ENproject，EN
          console.log('ENproject，EN')
        }
      } catch (error) {
        console.error('Polling error:', error)
      }
    }

    // Execute once immediately
    poll()
    
    // Set timer
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
      // ensureprojectsEN
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