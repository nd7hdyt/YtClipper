/**
 * Simplified progress management — fixed stages + polling
 */

import { create } from 'zustand'

export interface SimpleProgress {
  project_id: string
  stage: string
  percent: number
  message: string
  ts: number
}

interface SimpleProgressState {
  // Status data
  byId: Record<string, SimpleProgress>
  
  // Polling control
  pollingInterval: number | null
  isPolling: boolean
  
  // Actions
  upsert: (progress: SimpleProgress) => void
  startPolling: (projectIds: string[], intervalMs?: number) => void
  stopPolling: () => void
  clearProgress: (projectId: string) => void
  clearAllProgress: () => void
  
  // Getters
  getProgress: (projectId: string) => SimpleProgress | null
  getAllProgress: () => Record<string, SimpleProgress>
}

export const useSimpleProgressStore = create<SimpleProgressState>((set, get) => {
  let timer: number | null = null

  return {
    // Initial status
    byId: {},
    pollingInterval: null,
    isPolling: false,

    // Update or insert progress data
    upsert: (progress: SimpleProgress) => {
      set((state) => ({
        byId: {
          ...state.byId,
          [progress.project_id]: progress
        }
      }))
    },

    // Start polling
    startPolling: (projectIds: string[], intervalMs: number = 5000) => {
      const { stopPolling, isPolling } = get()
      
      // If already polling, stop first
      if (isPolling) {
        stopPolling()
      }

      if (projectIds.length === 0) {
        console.warn('No project ID, skipping polling')
        return
      }

      console.log(`Start pollingProgress: ${projectIds.join(', ')}`)

      // Fetch once immediately
      const fetchSnapshots = async () => {
        try {
          const queryString = projectIds.map(id => `project_ids=${id}`).join('&')
          const response = await fetch(`/api/v1/simple-progress/snapshot?${queryString}`)
          
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`)
          }
          
          const snapshots: SimpleProgress[] = await response.json()
          
          // Update status
          snapshots.forEach(snapshot => {
            console.log(`Update progress: ${snapshot.project_id} - ${snapshot.stage} (${snapshot.percent}%)`)
            get().upsert(snapshot)
          })
          
          console.log(`Polling update: ${snapshots.length} ENproject`)
          
          // If no progress or all projects reached terminal state, auto-stop polling
          try {
            const allTerminal = snapshots.length > 0 && snapshots.every(s => {
              return isCompleted(s.stage) || isFailed(s.message)
            })
            // Only stop when progress exists and all projects are completed
            // If snapshots.length === 0, project may still be pending; don't stop polling
            if (snapshots.length > 0 && allTerminal) {
              console.log('All projects completed, auto-stopping polling')
              get().stopPolling()
            } else if (snapshots.length === 0) {
              console.log('Project may still be pending, continue polling')
            }
          } catch (e) {
            // Guarded catch to avoid breaking subsequent polling
            console.warn('Error detecting terminal state, but continuing:', e)
          }
          
        } catch (error) {
          console.error('Polling progress failed:', error)
        }
      }

      // Execute once immediately
      fetchSnapshots()

      // Set timer
      timer = window.setInterval(fetchSnapshots, intervalMs)

      set({
        isPolling: true,
        pollingInterval: intervalMs
      })
    },

    // Stop polling
    stopPolling: () => {
      if (timer) {
        clearInterval(timer)
        timer = null
      }
      
      set({
        isPolling: false,
        pollingInterval: null
      })
      
      console.log('Stop pollingProgress')
    },

    // Clear single project progress
    clearProgress: (projectId: string) => {
      set((state) => {
        const newById = { ...state.byId }
        delete newById[projectId]
        return { byId: newById }
      })
    },

    // Clear all progress
    clearAllProgress: () => {
      set({ byId: {} })
    },

    // Get single project progress
    getProgress: (projectId: string) => {
      return get().byId[projectId] || null
    },

    // Get all progress
    getAllProgress: () => {
      return get().byId
    }
  }
})

// Stage display name map
export const STAGE_DISPLAY_NAMES: Record<string, string> = {
  'INGEST': 'Ingest',
  'SUBTITLE': 'Subtitles',
  'ANALYZE': 'Analysis', 
  'HIGHLIGHT': 'Highlights',
  'EXPORT': 'Export',
  'DONE': 'Done'
}

// Stage color map
export const STAGE_COLORS: Record<string, string> = {
  'INGEST': '#1890ff',      // blue
  'SUBTITLE': '#52c41a',    // green
  'ANALYZE': '#fa8c16',     // orange
  'HIGHLIGHT': '#722ed1',   // purple
  'EXPORT': '#eb2f96',      // pink
  'DONE': '#13c2c2'         // cyan
}

// Get stage display name
export const getStageDisplayName = (stage: string): string => {
  return STAGE_DISPLAY_NAMES[stage] || stage
}

// Get stage color
export const getStageColor = (stage: string): string => {
  return STAGE_COLORS[stage] || '#666666'
}

// Check if completed
export const isCompleted = (stage: string): boolean => {
  return stage === 'DONE'
}

// Check if failed
export const isFailed = (message: string): boolean => {
  return message.includes('Failed') || message.includes('Error') || message.includes('Failed')
}
