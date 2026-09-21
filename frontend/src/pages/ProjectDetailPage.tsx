import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { message } from 'antd'
import dayjs from 'dayjs'
import { useProjectStore, Clip, Collection } from '../store/useProjectStore'
import { projectApi } from '../services/api'
import ClipCard from '../components/ClipCard'
import CollectionCard from '../components/CollectionCard'
import CollectionPreviewModal from '../components/CollectionPreviewModal'
import CreateCollectionModal from '../components/CreateCollectionModal'
import { useCollectionVideoDownload } from '../hooks/useCollectionVideoDownload'
import { ProjectTaskManager } from '../components/ProjectTaskManager'
import FeedbackDialog from '../components/FeedbackDialog'
import { Btn, Icon, Section, Segmented, parseTimecode, fmtDuration } from '../ui'

const ProjectDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const {
    currentProject,
    loading,
    error,
    setCurrentProject,
    upsertProject,
    updateCollection,
    addCollection,
    deleteCollection,
    removeClipFromCollection,
    reorderCollectionClips,
    addClipToCollection
  } = useProjectStore()

  const [statusLoading, setStatusLoading] = useState(false)
  const [showCreateCollection, setShowCreateCollection] = useState(false)
  const [feedbackOpen, setFeedbackOpen] = useState(false)
  const [sortBy, setSortBy] = useState<'time' | 'score'>('score')
  const [showCollectionDetail, setShowCollectionDetail] = useState(false)
  const [selectedCollection, setSelectedCollection] = useState<Collection | null>(null)
  const { generateAndDownloadCollectionVideo } = useCollectionVideoDownload()

  useEffect(() => {
    if (!id) return
    loadProject()
    loadProcessingStatus()
  }, [id])

  const loadProject = async () => {
    if (!id) return
    try {
      const project = await projectApi.getProject(id)
      if (project.status === 'completed') {
        try {
          const [clips, collections] = await Promise.all([
            projectApi.getClips(id),
            projectApi.getCollections(id)
          ])
          const projectWithData = { ...project, clips: clips || [], collections: collections || [] }
          setCurrentProject(projectWithData)
          // Keep the project list in sync to avoid drift between the page and the list
          upsertProject(projectWithData)
        } catch (err) {
          console.error('Failed to load clips/collections:', err)
          setCurrentProject(project)
        }
      } else {
        setCurrentProject(project)
      }
    } catch (err) {
      console.error('Failed to load project:', err)
      message.error('Failed to load project')
    }
  }

  const loadProcessingStatus = async () => {
    if (!id) return
    setStatusLoading(true)
    try {
      await projectApi.getProcessingStatus(id)
    } catch (err) {
      console.error('Failed to load processing status:', err)
    } finally {
      setStatusLoading(false)
    }
  }

  const handleStartProcessing = async () => {
    if (!id) return
    try {
      await projectApi.startProcessing(id)
      message.success('Processing started')
      loadProcessingStatus()
    } catch (err) {
      console.error('Failed to start processing:', err)
      message.error('Failed to start processing')
    }
  }

  const handleRetryProcessing = async () => {
    if (!id) return
    setStatusLoading(true)
    try {
      await projectApi.retryProcessing(id)
      message.success('Processing restarted')
      loadProcessingStatus()
      await loadProject()
    } catch (err) {
      console.error('Failed to retry processing:', err)
      message.error('Retry failed, please try again later')
    } finally {
      setStatusLoading(false)
    }
  }

  const handleCreateCollection = async (title: string, summary: string, clipIds: string[]) => {
    if (!id) return
    try {
      await addCollection(id, {
        id: `collection_${Date.now()}`,
        collection_title: title,
        collection_summary: summary,
        clip_ids: clipIds,
        collection_type: 'manual',
        created_at: new Date().toISOString()
      })
      setShowCreateCollection(false)
      message.success('Collection created successfully')
    } catch (err) {
      console.error('Failed to create collection:', err)
      message.error('Failed to create collection')
    }
  }

  const handleViewCollection = (collection: Collection) => {
    setSelectedCollection(collection)
    setShowCollectionDetail(true)
  }

  const handleRemoveClipFromCollection = async (collectionId: string, clipId: string): Promise<void> => {
    if (!id) return
    try {
      await removeClipFromCollection(id, collectionId, clipId)
      message.success('Clip removed from collection')
    } catch (err) {
      console.error('Failed to remove clip from collection:', err)
      message.error('Failed to remove clip')
    }
  }

  const handleDeleteCollection = async (collectionId: string) => {
    if (!id) return
    try {
      await deleteCollection(id, collectionId)
      setShowCollectionDetail(false)
      setSelectedCollection(null)
      message.success('Collection deleted')
    } catch (err) {
      console.error('Failed to delete collection:', err)
      message.error('Failed to delete collection')
    }
  }

  const handleReorderCollectionClips = async (collectionId: string, newClipIds: string[]): Promise<void> => {
    if (!id) return
    try {
      await reorderCollectionClips(id, collectionId, newClipIds)
      message.success('Collection order updated')
    } catch (err) {
      console.error('Failed to reorder collection clips:', err)
      message.error('Failed to update collection order')
    }
  }

  const handleAddClipToCollection = async (collectionId: string, clipIds: string[]): Promise<void> => {
    if (!id) return
    try {
      await addClipToCollection(id, collectionId, clipIds)
      message.success('Clips added to collection')
    } catch (err) {
      console.error('Failed to add clip to collection:', err)
      message.error('Failed to add clips')
    }
  }

  const getSortedClips = () => {
    if (!currentProject?.clips) return []
    const clips = [...currentProject.clips]
    if (sortBy === 'score') return clips.sort((a, b) => b.final_score - a.final_score)
    return clips.sort((a, b) => parseTimecode(a.start_time) - parseTimecode(b.start_time))
  }

  if (loading) {
    return (
      <div className="ac-page" style={{ display: 'flex', justifyContent: 'center', paddingTop: 120 }}>
        <span className="ac-btn ac-btn--text" style={{ color: 'var(--ac-muted)' }}><span className="spin" /> Loading</span>
      </div>
    )
  }

  if (error || !currentProject) {
    return (
      <div className="ac-page">
        <div className="ac-empty">
          <b>Load failed</b>
          {error || 'Project not found'}
          <div style={{ marginTop: 16 }}>
            <Btn size="sm" onClick={() => navigate('/')}>Back to Home</Btn>
          </div>
        </div>
      </div>
    )
  }

  const clips = currentProject.clips || []
  const collections = currentProject.collections || []
  const totalClipSec = clips.reduce((s, c) => s + Math.max(0, parseTimecode(c.end_time) - parseTimecode(c.start_time)), 0)
  const sortedCollections = [...collections].sort((a, b) => {
    const ta = a.created_at ? new Date(a.created_at).getTime() : 0
    const tb = b.created_at ? new Date(b.created_at).getTime() : 0
    return tb - ta
  })
  const isCompleted = currentProject.status === 'completed'
  const isFailed = currentProject.status === 'failed' || (currentProject.status as string) === 'error'
  const failureContext = {
    source: 'failure' as const,
    project_id: currentProject.id,
    error_message: currentProject.error_message || undefined,
  }

  return (
    <div className="ac-page">
      {/* Page header: back · title · mono meta */}
      <header>
        <button className="ac-back" onClick={() => navigate('/')}>
          <Icon.Back /> Projects
        </button>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 24 }}>
          <div style={{ minWidth: 0 }}>
            <h1 className="ac-title">{currentProject.name}</h1>
            <div className="ac-meta">
              {isCompleted ? (
                <>
                  <span><span className="ac-mono">{clips.length}</span> clips</span>
                  <span className="dot" />
                  <span><span className="ac-mono">{collections.length}</span> collections</span>
                  {totalClipSec > 0 && (
                    <>
                      <span className="dot" />
                      <span>Total <span className="ac-mono">{fmtDuration(totalClipSec)}</span></span>
                    </>
                  )}
                </>
              ) : (
                <span>{currentProject.status === 'pending' ? 'Pending' : isFailed ? 'Failed' : 'Processing'}</span>
              )}
              {currentProject.created_at && (
                <>
                  <span className="dot" />
                  <span>{dayjs(currentProject.created_at).fromNow()}</span>
                </>
              )}
            </div>
          </div>
          {currentProject.status === 'pending' && (
            <Btn variant="cta" onClick={handleStartProcessing} loading={statusLoading}>Start processing</Btn>
          )}
          {isFailed && (
            <div style={{ display: 'flex', gap: 8, flex: '0 0 auto' }}>
              <Btn onClick={() => setFeedbackOpen(true)}>Report issue</Btn>
              <Btn variant="cta" onClick={handleRetryProcessing} loading={statusLoading}>Retry</Btn>
            </div>
          )}
        </div>
      </header>

      {isCompleted ? (
        <>
          {/* Collections */}
          <Section
            title="Collections"
            count={collections.length}
            description={collections.length > 0 ? 'AI stitches related clips into a finished video by topic; order and title are editable.' : 'Combine several clips into one themed video.'}
            right={
              <Btn size="sm" onClick={() => setShowCreateCollection(true)}>
                <Icon.Plus size={13} /> New collection
              </Btn>
            }
          >
            {collections.length > 0 ? (
              <div className="ac-hscroll">
                {sortedCollections.map((collection) => (
                  <CollectionCard
                    key={collection.id}
                    collection={collection}
                    clips={clips}
                    onView={handleViewCollection}
                    onUpdate={(collectionId, updates) => updateCollection(currentProject.id, collectionId, updates)}
                    onGenerateVideo={async (collectionId) => {
                      const c = collections.find((x) => x.id === collectionId)
                      if (c) await generateAndDownloadCollectionVideo(currentProject.id, collectionId, c.collection_title)
                    }}
                    onDelete={handleDeleteCollection}
                  />
                ))}
              </div>
            ) : (
              <div className="ac-empty">
                <b>No collections yet</b>
                Pick a few clips below and click "New collection".
              </div>
            )}
          </Section>

          {/* Clips */}
          <Section
            title="Clips"
            count={clips.length}
            right={
              <Segmented
                size="sm"
                ariaLabel="Sort"
                value={sortBy}
                onChange={setSortBy}
                options={[{ value: 'score', label: 'By score' }, { value: 'time', label: 'By time' }]}
              />
            }
          >
            {clips.length > 0 ? (
              <div className="ac-grid-3">
                {getSortedClips().map((clip) => (
                  <ClipCard
                    key={clip.id}
                    clip={clip}
                    projectId={currentProject.id}
                    videoUrl={projectApi.getClipVideoUrl(currentProject.id, clip.id, clip.title || clip.generated_title)}
                    onDownload={(clipId) => projectApi.downloadVideo(currentProject.id, clipId)}
                    onClipUpdate={(clipId: string, updates: Partial<Clip>) => {
                      const updatedProject = {
                        ...currentProject,
                        clips: clips.map((c: Clip) => (c.id === clipId ? { ...c, ...updates } : c))
                      }
                      setCurrentProject(updatedProject)
                    }}
                  />
                ))}
              </div>
            ) : (
              <div className="ac-empty">
                <b>No clips produced</b>
                You can lower the "Minimum score threshold" in settings and retry.
                <div style={{ marginTop: 12 }}>
                  <Btn variant="text" size="sm" onClick={() => setFeedbackOpen(true)}>Looks wrong? Let us know</Btn>
                </div>
              </div>
            )}
          </Section>
        </>
      ) : isFailed ? (
        <div className="ac-empty" style={{ marginTop: 32 }}>
          <b>Processing did not succeed</b>
          {currentProject.error_message ? (
            <span className="ac-mono" style={{ display: 'block', marginTop: 6, color: 'var(--ac-muted)', wordBreak: 'break-all' }}>
              {currentProject.error_message}
            </span>
          ) : (
            'You can retry directly; if it keeps failing, click "Report issue" and the environment and error will be attached automatically.'
          )}
        </div>
      ) : (
        <div style={{ marginTop: 32 }}>
          <ProjectTaskManager projectId={currentProject.id} projectName={currentProject.name} />
          <div className="ac-empty" style={{ marginTop: 24 }}>
            <b>Still processing</b>
            Clips and collections will appear here when done.
          </div>
        </div>
      )}

      <FeedbackDialog open={feedbackOpen} onClose={() => setFeedbackOpen(false)} context={failureContext} />

      <CreateCollectionModal
        visible={showCreateCollection}
        clips={clips}
        onCancel={() => setShowCreateCollection(false)}
        onCreate={handleCreateCollection}
      />

      <CollectionPreviewModal
        visible={showCollectionDetail}
        collection={selectedCollection}
        clips={clips}
        projectId={currentProject.id}
        onClose={() => {
          setShowCollectionDetail(false)
          setSelectedCollection(null)
        }}
        onUpdateCollection={(collectionId, updates) => updateCollection(currentProject.id, collectionId, updates)}
        onRemoveClip={handleRemoveClipFromCollection}
        onReorderClips={handleReorderCollectionClips}
        onDelete={handleDeleteCollection}
        onAddClip={handleAddClipToCollection}
      />
    </div>
  )
}

export default ProjectDetailPage
