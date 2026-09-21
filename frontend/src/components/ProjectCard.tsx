import React, { useState, useEffect } from 'react'
import { Card, Button, Space, Typography, Popconfirm, message, Tooltip } from 'antd'
import { PlayCircleOutlined, DeleteOutlined, DownloadOutlined, ReloadOutlined, LoadingOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { Project } from '../store/useProjectStore'
import { projectApi } from '../services/api'
import { UnifiedStatusBar } from './UnifiedStatusBar'
import FeedbackDialog from './FeedbackDialog'
import { useSimpleProgressStore } from '../stores/useSimpleProgressStore'
import { Btn } from '../ui'
// import { 
//   getProjectStatusConfig, 
//   calculateProjectProgress, 
//   normalizeProjectStatus,
//   getProgressStatus 
// } from '../utils/statusUtils'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import timezone from 'dayjs/plugin/timezone'
import utc from 'dayjs/plugin/utc'
import 'dayjs/locale/en'

dayjs.extend(relativeTime)
dayjs.extend(timezone)
dayjs.extend(utc)
dayjs.locale('en')

// Pulse animation
const pulseAnimation = `
  @keyframes pulse {
    0% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.5;
      transform: scale(1.1);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }
`

// Inject styles into the page
if (typeof document !== 'undefined') {
  const style = document.createElement('style')
  style.textContent = pulseAnimation
  document.head.appendChild(style)
}

const { Text } = Typography

// Tracks which project ids have already had a best-effort auto-start, surviving
// component remounts (the list briefly unmounts while HomePage shows its
// loading spinner). A useRef would reset on every remount and let auto-start
// fire again, which created an infinite onRetry→loadProjects→remount loop.
// Project ids are unique per import, so once-per-session is exactly right.
const autoStartedProjectIds = new Set<string>()

interface ProjectCardProps {
  project: Project
  onDelete: (id: string) => void
  onRetry?: (id: string) => void
  onClick?: () => void
}

const ProjectCard: React.FC<ProjectCardProps> = ({ project, onDelete, onRetry, onClick }) => {
  const navigate = useNavigate()
  const [videoThumbnail, setVideoThumbnail] = useState<string | null>(null)
  const [thumbnailLoading, setThumbnailLoading] = useState(false)
  const [isRetrying, setIsRetrying] = useState(false)

  // Category info
  const getCategoryInfo = (category?: string) => {
    const categoryMap: Record<string, { name: string; icon: string; color: string }> = {
      'default': { name: 'Default', icon: '🎬', color: '#4facfe' },
      'knowledge': { name: 'Knowledge', icon: '📚', color: '#52c41a' },
      'business': { name: 'Business', icon: '💼', color: '#faad14' },
      'opinion': { name: 'Opinion', icon: '💭', color: '#722ed1' },
      'experience': { name: 'Experience', icon: '🌟', color: '#13c2c2' },
      'speech': { name: 'Talk & Speech', icon: '🎤', color: '#eb2f96' },
      'content_review': { name: 'Commentary', icon: '🎭', color: '#f5222d' },
      'entertainment': { name: 'Entertainment', icon: '🎪', color: '#fa8c16' }
    }
    return categoryMap[category || 'default'] || categoryMap['default']
  }

  // Thumbnail cache
  const thumbnailCacheKey = `thumbnail_${project.id}`
  
  // Generate the project video thumbnail (cached)
  useEffect(() => {
    const generateThumbnail = async () => {
      // Prefer the backend-provided thumbnail
      if (project.thumbnail) {
        setVideoThumbnail(project.thumbnail)
        console.log(`Using backend thumbnail: ${project.id}`)
        return
      }
      
      if (!project.video_path) {
        console.log('No video path for project:', project.id)
        return
      }
      
      // Check the cache
      const cachedThumbnail = localStorage.getItem(thumbnailCacheKey)
      if (cachedThumbnail) {
        setVideoThumbnail(cachedThumbnail)
        return
      }
      
      setThumbnailLoading(true)
      
      try {
        const video = document.createElement('video')
        video.crossOrigin = 'anonymous'
        video.muted = true
        video.preload = 'metadata'
        
        // Try multiple possible video file paths
        const possiblePaths = [
          'input/input.mp4',
          'input.mp4',
          project.video_path,
          `${project.video_path}/input.mp4`
        ].filter(Boolean)
        
        let videoLoaded = false
        
        for (const path of possiblePaths) {
          if (videoLoaded) break
          
          try {
            const videoUrl = projectApi.getProjectFileUrl(project.id, path)
            console.log('Trying video:', videoUrl)
            
            await new Promise((resolve, reject) => {
              const timeoutId = setTimeout(() => {
                reject(new Error('Video load timed out'))
              }, 10000) // 10s timeout
              
              video.onloadedmetadata = () => {
                clearTimeout(timeoutId)
                console.log('Video metadata loaded:', videoUrl)
                video.currentTime = Math.min(5, video.duration / 4) // Frame at 1/4 or 5s
              }
              
              video.onseeked = () => {
                clearTimeout(timeoutId)
                try {
                  const canvas = document.createElement('canvas')
                  const ctx = canvas.getContext('2d')
                  if (!ctx) {
                    reject(new Error('Canvas context unavailable'))
                    return
                  }
                  
                  // Thumbnail size
                  const maxWidth = 320
                  const maxHeight = 180
                  const aspectRatio = video.videoWidth / video.videoHeight
                  
                  let width = maxWidth
                  let height = maxHeight
                  
                  if (aspectRatio > maxWidth / maxHeight) {
                    height = maxWidth / aspectRatio
                  } else {
                    width = maxHeight * aspectRatio
                  }
                  
                  canvas.width = width
                  canvas.height = height
                  ctx.drawImage(video, 0, 0, width, height)
                  
                  const thumbnail = canvas.toDataURL('image/jpeg', 0.7)
                  setVideoThumbnail(thumbnail)
                  
                  // Cache the thumbnail
                  try {
                    localStorage.setItem(thumbnailCacheKey, thumbnail)
                  } catch (e) {
                    // Evict old cache when localStorage is full
                    const keys = Object.keys(localStorage).filter(key => key.startsWith('thumbnail_'))
                    if (keys.length > 50) { // Keep at most 50 thumbnails
                      keys.slice(0, 10).forEach(key => localStorage.removeItem(key))
                      localStorage.setItem(thumbnailCacheKey, thumbnail)
                    }
                  }
                  
                  videoLoaded = true
                  resolve(thumbnail)
                } catch (error) {
                  reject(error)
                }
              }
              
              video.onerror = (error) => {
                clearTimeout(timeoutId)
                console.error('Video load failed:', videoUrl, error)
                reject(error)
              }
              
              video.src = videoUrl
            })
            
            break // Break on success
          } catch (error) {
            console.warn(`Path ${path} failed:`, error)
            continue // Try the next path
          }
        }
        
        if (!videoLoaded) {
          console.error('All video paths failed')
        }
      } catch (error) {
        console.error('Thumbnail generation error:', error)
      } finally {
        setThumbnailLoading(false)
      }
    }
    
    generateThumbnail()
  }, [project.id, project.video_path, thumbnailCacheKey])

  // Download state from the download progress
  const downloadProgress = project.processing_config?.download_progress || 0
  const isDownloading = project.status === 'pending' && downloadProgress > 0 && downloadProgress < 100
  const isImporting = project.status === 'pending' && !isDownloading
  
  // Normalized status
  const normalizedStatus = project.status === 'error' ? 'failed' : 
                          isDownloading ? 'downloading' :
                          isImporting ? 'importing' : project.status
  
  // Debug info
  console.log('ProjectCard Debug:', {
    projectId: project.id,
    projectStatus: project.status,
    downloadProgress,
    isDownloading,
    isImporting,
    normalizedStatus,
    processingConfig: project.processing_config
  })

  // Auto-start pending projects (excluding downloads).
  // Key: each project auto-attempts at most once, and failures stay silent.
  // Previously isRetrying was a dep while handleRetry flipped it,
  // re-triggering the effect -> spamming POST /process for a Bilibili
  // project whose download wasn't done (400 "Video file not found") ->
  // endless "retry failed" toasts. The backend auto-starts the
  // pipeline once the download finishes, so one best-effort start is enough.
  useEffect(() => {
    if (
      project.status === 'pending' &&
      !isDownloading &&
      !autoStartedProjectIds.has(project.id)
    ) {
      autoStartedProjectIds.add(project.id)
      // Bilibili imports whose download isn't done yet return 400 here —
      // that's fine, the backend auto-starts the pipeline when the download
      // completes. Silent + no onRetry so this never drives the parent's
      // toast/reload path.
      handleRetry({ silent: true })
    }
  }, [project.status, project.id, isDownloading])
  
  // Progress percent
  const progressPercent = project.status === 'completed' ? 100 : 
                         project.status === 'failed' ? 0 :
                         isDownloading ? downloadProgress : // Show real download progress while downloading
                         isImporting ? 5 : // Pending shows 5% as waiting
                         project.current_step && project.total_steps ? 
                         Math.round((project.current_step / project.total_steps) * 100) : 
                         project.status === 'processing' ? 10 : 0

  const [feedbackOpen, setFeedbackOpen] = useState(false)
  const failedProgress = useSimpleProgressStore((st) => st.getProgress(project.id))
  const failureContext = {
    source: 'failure' as const,
    project_id: project.id,
    stage: failedProgress?.stage,
    error_message: project.error_message || failedProgress?.message || undefined,
  }

  const handleRetry = async (opts?: { silent?: boolean }) => {
    if (isRetrying) return

    setIsRetrying(true)
    try {
      // PENDING uses startProcessing; other states use retryProcessing
      if (project.status === 'pending') {
        await projectApi.startProcessing(project.id)
      } else {
        await projectApi.retryProcessing(project.id)
      }
      // Let the parent handle toast / refresh. But silent auto-start must never
      // notify the parent, otherwise we'd loop:
      // handleRetryProject -> loadProjects -> list remount -> auto-start again.
      // Only manual retries notify the parent.
      if (onRetry && !opts?.silent) {
        onRetry(project.id)
      }
    } catch (error) {
      console.error('Retry failed:', error)
      // Silent auto-start failures stay quiet; only manual retries toast.
      if (!opts?.silent) {
        message.error('Retry failed, please try again later')
      }
    } finally {
      setIsRetrying(false)
    }
  }

  return (
    <>
    <Card
      hoverable
      className="project-card"
      style={{
        width: '100%',
        borderRadius: '16px',
        overflow: 'hidden',
        background: 'var(--ac-card)',
        border: '1px solid var(--ac-line)',
        boxShadow: 'none',
        transition: 'all 0.2s ease',
        cursor: 'pointer',
        marginBottom: '0px'
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-2px)'
        e.currentTarget.style.boxShadow = 'var(--ac-shadow)'
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)'
        e.currentTarget.style.boxShadow = 'none'
      }}
      bodyStyle={{
        padding: '18px 20px 20px',
        background: 'transparent',
        display: 'flex',
        flexDirection: 'column'
      }}
      cover={
        <div
          style={{
            height: 160,
            position: 'relative',
            background: videoThumbnail
              ? `url(${videoThumbnail}) center/cover`
              : 'var(--ac-thumb)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            overflow: 'hidden'
          }}
          onClick={() => {
            // Importing projects can't be opened
            if (project.status === 'pending') {
              message.warning('Project is importing, please check back later')
              return
            }
            
            // Processing projects can't be opened
            if (project.status === 'processing') {
              message.warning('Project is processing, please wait until it finishes')
              return
            }
            
            if (onClick) {
              onClick()
            } else {
              navigate(`/project/${project.id}`)
            }
          }}
        >
          {/* Thumbnail loading state */}
          {thumbnailLoading && (
            <div style={{ textAlign: 'center', color: 'var(--ac-muted)' }}>
              <LoadingOutlined style={{ fontSize: '22px', marginBottom: '4px' }} />
              <div style={{ fontSize: '12px' }}>Generating cover…</div>
            </div>
          )}

          {/* Default when there is no thumbnail */}
          {!videoThumbnail && !thumbnailLoading && (
            <PlayCircleOutlined style={{ fontSize: '32px', color: 'var(--ac-muted)' }} />
          )}
          
          {/* Category tag - top left */}
          {project.video_category && project.video_category !== 'default' && (
            <div style={{
              position: 'absolute',
              top: '8px',
              left: '8px'
            }}>
              <span className="ac-tag ac-tag--sans" style={{ position: 'static', fontSize: 11 }}>
                {getCategoryInfo(project.video_category).name}
              </span>
            </div>
          )}
          
          {/* Removed top-right status dot - noisy and redundant */}
          
          {/* Timestamp and actions - moved to cover bottom */}
          <div style={{
            position: 'absolute',
            bottom: '0',
            left: '0',
            right: '0',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'flex-end',
            background: 'linear-gradient(to top, rgba(0,0,0,0.42), rgba(0,0,0,0))',
            borderRadius: '0',
            padding: '10px 12px',
            height: '52px'
          }}>
            <Text style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.92)' }}>
              {dayjs(project.created_at).tz('Asia/Shanghai').fromNow()}
            </Text>
            
            {/* Actions */}
            <div 
              className="card-action-buttons"
              style={{
                display: 'flex',
                gap: '4px',
                opacity: 0,
                transition: 'opacity 0.3s ease'
              }}
            >
              {/* Failed: only retry + delete */}
              {normalizedStatus === 'failed' ? (
                <>
                  <Button
                    type="text"
                    icon={<ReloadOutlined />}
                    loading={isRetrying}
                    onClick={(e) => {
                      e.stopPropagation()
                      handleRetry()
                    }}
                    style={{
                      height: '22px',
                      width: '22px',
                      borderRadius: '999px',
                      color: 'rgba(255,255,255,0.9)',
                      border: '1px solid rgba(255,255,255,0.25)',
                      background: 'rgba(20,20,19,0.45)',
                      padding: 0,
                      minWidth: '22px',
                      fontSize: '10px'
                    }}
                  />
                  
                  <Popconfirm
                    title="Delete this project?"
                    description="This cannot be undone"
                    onConfirm={(e) => {
                      e?.stopPropagation()
                      onDelete(project.id)
                    }}
                    onCancel={(e) => {
                      e?.stopPropagation()
                    }}
                    okText="Delete"
                    cancelText="Cancel"
                  >
                    <Button
                      type="text"
                      icon={<DeleteOutlined />}
                      onClick={(e) => {
                        e.stopPropagation()
                      }}
                      style={{
                      height: '22px',
                      width: '22px',
                      borderRadius: '999px',
                      color: 'rgba(255,255,255,0.9)',
                      border: '1px solid rgba(255,255,255,0.25)',
                      background: 'rgba(20,20,19,0.45)',
                      padding: 0,
                      minWidth: '22px',
                      fontSize: '10px'
                    }}
                    />
                  </Popconfirm>
                </>
              ) : (
                /* Other states: download + retry + delete */
                <>
                  <Space size={4}>
                    {/* Retry button - shown while processing/waiting so users can resubmit */}
                    {(normalizedStatus === 'processing' || normalizedStatus === 'importing' || project.status === 'pending') && (
                      <Tooltip title={project.status === 'pending' ? "Start processing" : "Resubmit task"}>
                        <Button
                          type="text"
                          icon={<ReloadOutlined />}
                          loading={isRetrying}
                          onClick={(e) => {
                            e.stopPropagation()
                            handleRetry()
                          }}
                          style={{
                      height: '22px',
                      width: '22px',
                      borderRadius: '999px',
                      color: 'rgba(255,255,255,0.9)',
                      border: '1px solid rgba(255,255,255,0.25)',
                      background: 'rgba(20,20,19,0.45)',
                      padding: 0,
                      minWidth: '22px',
                      fontSize: '10px'
                    }}
                        />
                      </Tooltip>
                    )}
                    
                    {/* Download button - completed only */}
                    {normalizedStatus === 'completed' && (
                      <Button
                        type="text"
                        icon={<DownloadOutlined />}
                        onClick={(e) => {
                          e.stopPropagation()
                          // Download action
                          message.info('Download is coming soon...')
                        }}
                        style={{
                      height: '22px',
                      width: '22px',
                      borderRadius: '999px',
                      color: 'rgba(255,255,255,0.9)',
                      border: '1px solid rgba(255,255,255,0.25)',
                      background: 'rgba(20,20,19,0.45)',
                      padding: 0,
                      minWidth: '22px',
                      fontSize: '10px'
                    }}
                      />
                    )}
                    
                    {/* Delete button */}
                    <Popconfirm
                      title="Delete this project?"
                      description="This cannot be undone"
                      onConfirm={(e) => {
                        e?.stopPropagation()
                        onDelete(project.id)
                      }}
                      onCancel={(e) => {
                        e?.stopPropagation()
                      }}
                      okText="Delete"
                      cancelText="Cancel"
                    >
                      <Button
                        type="text"
                        icon={<DeleteOutlined />}
                        onClick={(e) => {
                          e.stopPropagation()
                        }}
                        style={{
                      height: '22px',
                      width: '22px',
                      borderRadius: '999px',
                      color: 'rgba(255,255,255,0.9)',
                      border: '1px solid rgba(255,255,255,0.25)',
                      background: 'rgba(20,20,19,0.45)',
                      padding: 0,
                      minWidth: '22px',
                      fontSize: '10px'
                    }}
                      />
                    </Popconfirm>
                  </Space>
                 </>
               )}
            </div>
          </div>
        </div>
      }
    >
      <div style={{ padding: '0', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <div>
          {/* Project name - always on top */}
          <div style={{ marginBottom: '12px', position: 'relative' }}>
            <Tooltip title={project.name} placement="top">
              <Text 
                strong 
                style={{ 
                  fontSize: '13px', 
                  color: '#ffffff',
                  fontWeight: 600,
                  lineHeight: '16px',
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  cursor: 'help',
                  height: '32px'
                }}
              >
                {project.name}
              </Text>
            </Tooltip>
          </div>
          
          {/* Status and stats - Calm Premium, see DESIGN.md */}
          {(normalizedStatus === 'importing' || normalizedStatus === 'downloading' || normalizedStatus === 'processing' || normalizedStatus === 'failed') ? (
            // In progress / failed: thin line or terminal dot, full width
            <div style={{ marginBottom: '2px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
              <UnifiedStatusBar
                projectId={project.id}
                status={normalizedStatus}
                downloadProgress={progressPercent}
                onStatusChange={(newStatus) => {
                  console.log(`Project ${project.id} status: ${normalizedStatus} -> ${newStatus}`)
                }}
                onDownloadProgressUpdate={(progress) => {
                  console.log(`Project ${project.id} download progress: ${progress}%`)
                }}
              />
              {normalizedStatus === 'failed' && (
                // Failed: retry + feedback (feedback auto-attaches stage / error / version / model)
                <div style={{ display: 'flex', gap: 2, flex: '0 0 auto' }} onClick={(e) => e.stopPropagation()}>
                  <Btn variant="text" size="sm" style={{ height: 26, padding: '0 8px', fontSize: 12.5 }} loading={isRetrying} onClick={() => handleRetry()}>Retry</Btn>
                  <Btn variant="text" size="sm" style={{ height: 26, padding: '0 8px', fontSize: 12.5 }} onClick={() => setFeedbackOpen(true)}>Feedback</Btn>
                </div>
              )}
            </div>
          ) : (
            // Completed: dot + gray mono meta (N clips, M collections)
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2px' }}>
              <UnifiedStatusBar
                projectId={project.id}
                status={normalizedStatus}
                downloadProgress={progressPercent}
                onStatusChange={() => {}}
              />
              <div style={{ color: 'var(--ac-muted)', fontSize: '12.5px', whiteSpace: 'nowrap' }}>
                <span className="ac-mono">{project.total_clips || 0}</span> clips
                <span style={{ margin: '0 6px' }}>·</span>
                <span className="ac-mono">{project.total_collections || 0}</span> collections
              </div>
            </div>
          )}

          {/* Detailed progress hidden - percent only in the status block */}

        </div>
      </div>
    </Card>
    <FeedbackDialog open={feedbackOpen} onClose={() => setFeedbackOpen(false)} context={failureContext} />
    </>
  )
}

export default ProjectCard