import React, { useState, useRef, useEffect } from 'react'
import { Modal, Row, Col, Button, Space, Typography, Tag, message, Popconfirm } from 'antd'
import { PlayCircleOutlined, DeleteOutlined, MenuOutlined, CloseOutlined, LeftOutlined, RightOutlined, PlusOutlined, UploadOutlined } from '@ant-design/icons'
import ReactPlayer from 'react-player'
import { DragDropContext, Droppable, Draggable, DropResult } from 'react-beautiful-dnd'
import { Collection, Clip, useProjectStore } from '../store/useProjectStore'
import { projectApi } from '../services/api'
import AddClipToCollectionModal from './AddClipToCollectionModal'
import { useCollectionVideoDownload } from '../hooks/useCollectionVideoDownload'
import UploadModal from './UploadModal'
import EditableTitle from './EditableTitle'
import './CollectionPreviewModal.css'

const { Title, Text } = Typography

interface CollectionPreviewModalProps {
  visible: boolean
  collection: Collection | null
  clips: Clip[]
  projectId: string
  onClose: () => void
  onUpdateCollection: (collectionId: string, updates: Partial<Collection>) => void
  onRemoveClip: (collectionId: string, clipId: string) => Promise<void>
  onReorderClips: (collectionId: string, newClipIds: string[]) => void
  onAddClip?: (collectionId: string, clipIds: string[]) => void
  onDelete?: (collectionId: string) => void
}

const CollectionPreviewModal: React.FC<CollectionPreviewModalProps> = ({
  visible,
  collection,
  clips,
  projectId,
  onClose,
  onRemoveClip,
  onReorderClips,
  onAddClip,
  onDelete
}) => {
  const [currentClipIndex, setCurrentClipIndex] = useState(0)
  const [playing, setPlaying] = useState(false)
  const autoPlay = true

  const [showAddClipModal, setShowAddClipModal] = useState(false)
  const [isUpdating, setIsUpdating] = useState(false)
  const [showUploadModal, setShowUploadModal] = useState(false)
  const playerRef = useRef<ReactPlayer>(null)
  const { setDragging } = useProjectStore()
  const { isGenerating, generateAndDownloadCollectionVideo } = useCollectionVideoDownload()

  // fromstoretranslatedfetchtranslated'scollectionstatus
  const { projects, currentProject, lastEditTimestamp } = useProjectStore()
  const latestCollection = collection ? 
    (currentProject?.collections?.find(c => c.id === collection.id) || 
     projects.find(p => p.collections?.some(c => c.id === collection.id))?.collections?.find(c => c.id === collection.id) ||
     collection) : null

  // bytranslatedlatestCollection.clip_ids'stranslatedclips
  const collectionClips = latestCollection ? 
    (Array.isArray(latestCollection.clip_ids) ? latestCollection.clip_ids : [])
      .map(clipId => (Array.isArray(clips) ? clips : []).find(clip => clip.id === clipId))
      .filter(Boolean) as Clip[] : []
  const currentClip = collectionClips[currentClipIndex]

  useEffect(() => {
    if (visible && collectionClips.length > 0) {
      setCurrentClipIndex(0)
      setPlaying(false)
    }
  }, [visible, latestCollection, collectionClips.length, lastEditTimestamp])

  const handleClipSelect = (index: number) => {
    setCurrentClipIndex(index)
    setPlaying(true)
  }

  const handlePlayNext = () => {
    if (currentClipIndex < collectionClips.length - 1) {
      setCurrentClipIndex(currentClipIndex + 1)
      if (autoPlay) {
        setPlaying(true)
      }
    } else {
      setPlaying(false)
    }
  }

  const handlePlayPrevious = () => {
    if (currentClipIndex > 0) {
      setCurrentClipIndex(currentClipIndex - 1)
      if (autoPlay) {
        setPlaying(true)
      }
    }
  }

  const handleVideoEnd = () => {
    if (autoPlay && currentClipIndex < collectionClips.length - 1) {
      handlePlayNext()
    } else {
      setPlaying(false)
    }
  }

  const handleDragStart = () => {
    console.log('translated')
    setDragging(true)
  }

  const handleDragEnd = async (result: DropResult) => {
    console.log('translated:', result)
    
    // translatediftranslatedstatus
    setDragging(false)
    
    if (!result.destination || !latestCollection) {
      console.log('translatedcancelortranslated')
      return
    }

    // checkIstranslated'stranslated
    if (result.source.index === result.destination.index) {
      console.log('translated，skipupdate')
      return
    }

    const newClipIds = Array.from(latestCollection.clip_ids)
    const [reorderedItem] = newClipIds.splice(result.source.index, 1)
    newClipIds.splice(result.destination.index, 0, reorderedItem)

    console.log('translated:', latestCollection.clip_ids)
    console.log('translated:', newClipIds)
    
    // translatedstatus
    const hideLoading = message.loading('translatedinupdatecliptranslated...', 0)
    setIsUpdating(true)
    
    try {
      await onReorderClips(latestCollection.id, newClipIds)
      
      // updatetranslated
      const currentClipId = collectionClips[currentClipIndex]?.id
      if (currentClipId) {
        const newIndex = newClipIds.indexOf(currentClipId)
        setCurrentClipIndex(newIndex)
      }
      
      hideLoading()
    } catch (error) {
      console.error('Failed to reorder clips:', error)
      hideLoading()
      message.error('cliptranslatedfailed')
    } finally {
      setIsUpdating(false)
    }
  }

  const handleRemoveClip = async (clipId: string) => {
    if (!latestCollection) return
    
    const hideLoading = message.loading('translatedintranslatedclip...', 0)
    setIsUpdating(true)
    
    try {
      await onRemoveClip(latestCollection.id, clipId)
      
      // translated
      const removedIndex = latestCollection.clip_ids.indexOf(clipId)
      if (removedIndex <= currentClipIndex && currentClipIndex > 0) {
        setCurrentClipIndex(currentClipIndex - 1)
      } else if (removedIndex === currentClipIndex && currentClipIndex >= collectionClips.length - 1) {
        setCurrentClipIndex(Math.max(0, collectionClips.length - 2))
      }
      
      hideLoading()
    } catch (error) {
      console.error('Failed to remove clip:', error)
      hideLoading()
      message.error('translatedclipfailed')
    } finally {
      setIsUpdating(false)
    }
  }

  const handleGenerateVideo = async () => {
    if (!latestCollection) return
    
    await generateAndDownloadCollectionVideo(
      projectId, 
      latestCollection.id, 
      latestCollection.collection_title
    )
  }

  const handleAddClips = async (selectedClipIds: string[]) => {
    if (!latestCollection || !onAddClip) return
    
    const hideLoading = message.loading('translatedinaddclip...', 0)
    setIsUpdating(true)
    
    try {
      await onAddClip(latestCollection.id, selectedClipIds)
      setShowAddClipModal(false)
      hideLoading()
    } catch (error) {
      console.error('Failed to add clips:', error)
      hideLoading()
      message.error('addclipfailed')
    } finally {
      setIsUpdating(false)
    }
  }

  const formatDuration = (clip: Clip) => {
    const start = clip.start_time.split(':')
    const end = clip.end_time.split(':')
    const startSeconds = parseInt(start[0]) * 3600 + parseInt(start[1]) * 60 + parseFloat(start[2].replace(',', '.'))
    const endSeconds = parseInt(end[0]) * 3600 + parseInt(end[1]) * 60 + parseFloat(end[2].replace(',', '.'))
    const duration = endSeconds - startSeconds
    const mins = Math.floor(duration / 60)
    const secs = Math.floor(duration % 60)
    return `${mins}:${String(secs).padStart(2, '0')}`
  }

  if (!latestCollection) return null

  return (
    <Modal
      title={null}
      open={visible}
      onCancel={onClose}
      footer={null}
      width="90vw"
      style={{ top: 20 }}
      styles={{ body: { padding: 0, height: 'min(90dvh, calc(100dvh - 40px))' } }}
      className="collection-preview-modal"
      closable={false}
      maskClosable={false}
      destroyOnClose={false}
      getContainer={false}
    >
      <div className="collection-preview-container">
        {/* translated */}
        <div className="preview-header">
          <div className="header-left">
            <Title level={4} style={{ margin: 0, color: 'var(--ac-ink)', display: 'inline-block', marginRight: '12px' }}>
              {latestCollection.collection_title}
            </Title>
            <Text style={{ color: 'var(--ac-sub)', fontSize: '13px' }}>
              ({collectionClips.length}  clip)
            </Text>
          </div>
          <div className="header-right">
            <Space>
              <Button 
                type="primary" 
                loading={isGenerating}
                onClick={handleGenerateVideo}
              >
                exporttranslatedvideo
              </Button>
              <Button 
                type="default" 
                icon={<UploadOutlined />}
                onClick={() => message.info('In Development，translated', 3)}
              >
                translatedBsite
              </Button>
              {onDelete && (
                <Popconfirm
                  title="deletecollection"
                  description="translateddeletethis collectiontranslated？translatedcantranslated。"
                  onConfirm={() => onDelete(latestCollection.id)}
                  okText="translated"
                  cancelText="cancel"
                >
                  <Button 
                    type="text" 
                    icon={<DeleteOutlined />}
                    style={{ color: 'var(--ac-error)' }}
                  >
                    delete
                  </Button>
                </Popconfirm>
              )}
              <Button 
                type="text" 
                icon={<CloseOutlined />} 
                onClick={onClose}
                aria-label="translatedcollectiontranslated"
                title="translated"
                style={{
                  color: 'var(--ac-ink)',
                  border: '1px solid var(--ac-line)',
                  background: 'var(--ac-card)',
                }}
              />
            </Space>
          </div>
        </div>

        {/* translated */}
        <div className="preview-content">
          <Row style={{ height: '100%' }}>
            {/* translatedvideotranslated */}
            <Col span={16} className="video-section">
              <div className="video-player-wrapper">
                <div className="video-container">
                  {currentClip ? (
                    <ReactPlayer
                      ref={playerRef}
                      url={projectApi.getClipVideoUrl(projectId, currentClip.id, currentClip.title || currentClip.generated_title)}
                      width="100%"
                      height="100%"
                      playing={playing}
                      controls
                      onEnded={handleVideoEnd}
                      onPlay={() => setPlaying(true)}
                      onPause={() => setPlaying(false)}
                    />
                  ) : (
                    <div className="empty-video">
                      <PlayCircleOutlined style={{ fontSize: '64px', color: '#d9d9d9' }} />
                      <Text style={{ color: '#999', marginTop: 16 }}>Not yetvideotranslated</Text>
                    </div>
                  )}
                </div>
                
                {/* videoinfotranslated - translatedvideotranslated */}
                {currentClip && (
                  <div className="video-info-bar">
                    <div className="video-info-content">
                      <div className="video-title-section">
                        <div className="video-title">
                          <EditableTitle
                            title={currentClip.title || currentClip.generated_title || 'translated'}
                            clipId={currentClip.id}
                            onTitleUpdate={(newTitle) => {
                              // thistranslatedcantranslated'supdatetranslated
                              console.log('translatedupdate:', newTitle)
                            }}
                            style={{ color: 'var(--ac-ink)', fontSize: '16px', fontWeight: '500' }}
                          />
                        </div>
                        <div className="video-meta">
                          <Tag style={{ background: 'var(--ac-line-2)', color: 'var(--ac-sub)', border: '1px solid var(--ac-line)', borderRadius: '6px' }}>
                            <span className="ac-mono">{formatDuration(currentClip)}</span>
                          </Tag>
                          <Tag
                            style={{
                              background: 'var(--ac-line-2)',
                              color: 'var(--ac-ink)',
                              border: '1px solid var(--ac-line)',
                              borderRadius: '6px'
                            }}
                          >
                            <span className="ac-mono">{(currentClip.final_score * 100).toFixed(0)}</span> translated
                          </Tag>
                          <Text style={{ color: 'var(--ac-muted)', marginLeft: 8 }}>
                            {currentClipIndex + 1} / {collectionClips.length}
                          </Text>
                        </div>
                      </div>
                      
                      <div className="video-controls">
                        <Button 
                          type="text" 
                          icon={<LeftOutlined />}
                          disabled={currentClipIndex === 0}
                          onClick={handlePlayPrevious}
                          title="translatedone clip"
                          className="control-btn"
                        />
                        <Button 
                          type="text" 
                          icon={<RightOutlined />}
                          disabled={currentClipIndex === collectionClips.length - 1}
                          onClick={handlePlayNext}
                          title="translatedone clip"
                          className="control-btn"
                        />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </Col>

            {/* translatedcliplist */}
            <Col span={8} className="playlist-section">
              <div className="playlist-container">
                <div className="playlist-header">
                  <div>
                    <Title level={5} style={{ margin: 0 }}>translatedlist</Title>
                    <Text type="secondary">translated</Text>
                  </div>
                  {onAddClip && (
                    <Button 
                      type="primary" 
                      size="middle"
                      icon={<PlusOutlined />}
                      onClick={() => setShowAddClipModal(true)}
                      disabled={isUpdating}
                      style={{
                        borderRadius: '999px',
                        background: 'var(--ac-cta-bg)',
                        border: 'none',
                        fontWeight: 500,
                        height: '36px',
                        padding: '0 16px',
                        fontSize: '14px'
                      }}
                    >
                      addclip
                    </Button>
                  )}
                </div>
                
                <DragDropContext onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
                  <Droppable droppableId="clips">
                    {(provided) => (
                      <div
                        {...provided.droppableProps}
                        ref={provided.innerRef}
                        className="clips-list"
                      >
                        {collectionClips.map((clip, index) => (
                          <Draggable key={clip.id} draggableId={clip.id} index={index}>
                            {(provided, snapshot) => (
                              <div
                                ref={provided.innerRef}
                                {...provided.draggableProps}
                                {...provided.dragHandleProps}
                                className={`clip-item ${
                                  index === currentClipIndex ? 'active' : ''
                                } ${snapshot.isDragging ? 'dragging' : ''}`}
                                onClick={() => {
                                  if (!snapshot.isDragging && !isUpdating) {
                                    handleClipSelect(index)
                                  }
                                }}
                              >
                                <div className="clip-drag-handle">
                                  <MenuOutlined />
                                </div>
                                
                                <div className="clip-content">
                                  <div className="clip-title">
                                    {clip.title || clip.generated_title}
                                  </div>
                                  <div className="clip-meta">
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px' }}>
                                      <Text type="secondary">
                                        {formatDuration(clip)}
                                      </Text>
                                      <span className="ac-mono" style={{
                                        background: 'var(--ac-line-2)',
                                        color: 'var(--ac-ink)',
                                        border: '1px solid var(--ac-line)',
                                        padding: '2px 6px',
                                        borderRadius: '6px',
                                        fontSize: '11px'
                                      }}>
                                        {(clip.final_score * 100).toFixed(0)} translated
                                      </span>
                                    </div>
                                  </div>
                                  {clip.recommend_reason && (
                                    <div className="clip-reason">
                                      <Text type="secondary" style={{ fontSize: '11px' }}>
                                        {clip.recommend_reason}
                                      </Text>
                                    </div>
                                  )}
                                </div>

                                <div className="clip-actions">
                                  <Popconfirm
                                    title="translatedfromcollectiontranslatedthis cliptranslated？"
                                    onConfirm={(e) => {
                                      e?.stopPropagation()
                                      handleRemoveClip(clip.id)
                                    }}
                                    okText="translated"
                                    cancelText="cancel"
                                    disabled={isUpdating}
                                  >
                                    <Button
                                      type="text"
                                      size="small"
                                      icon={<DeleteOutlined />}
                                      danger
                                      disabled={isUpdating}
                                      onClick={(e) => e.stopPropagation()}
                                      style={{ 
                                        display: 'flex', 
                                        alignItems: 'center', 
                                        justifyContent: 'center',
                                        width: '24px',
                                        height: '24px'
                                      }}
                                    />
                                  </Popconfirm>
                                </div>
                              </div>
                            )}
                          </Draggable>
                        ))}
                        {provided.placeholder}
                      </div>
                    )}
                  </Droppable>
                </DragDropContext>
              </div>
            </Col>
          </Row>
        </div>
      </div>
      
      {/* addcliptranslated */}
      <AddClipToCollectionModal
        visible={showAddClipModal}
        clips={clips}
        existingClipIds={latestCollection?.clip_ids || []}
        onCancel={() => setShowAddClipModal(false)}
        onConfirm={handleAddClips}
      />

      {/* translated */}
      <UploadModal
        visible={showUploadModal}
        onCancel={() => setShowUploadModal(false)}
        projectId={projectId}
        clipIds={collectionClips.map(clip => clip.id)}
        clipTitles={collectionClips.map(clip => clip.generated_title || clip.title || 'videotranslated')}
        onSuccess={() => {
          // translatedsucceededtranslatedcantranslatedortranslated
          console.log('collectiontranslatedsucceeded')
        }}
      />
    </Modal>
  )
}

export default CollectionPreviewModal
