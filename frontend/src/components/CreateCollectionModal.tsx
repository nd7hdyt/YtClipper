import React, { useState } from 'react'
import { Modal, Input, Checkbox, Typography, Button, Divider } from 'antd'
import { PlusOutlined, TagOutlined, FileTextOutlined, VideoCameraOutlined } from '@ant-design/icons'
import './CreateCollectionModal.css'

const { Text, Title } = Typography
const { TextArea } = Input

interface Clip {
  id: string
  title?: string
  generated_title?: string
  start_time: string
  end_time: string
  final_score: number
}

interface CreateCollectionModalProps {
  visible: boolean
  clips: Clip[]
  onCancel: () => void
  onCreate: (title: string, summary: string, clipIds: string[]) => void
  loading?: boolean
}

const CreateCollectionModal: React.FC<CreateCollectionModalProps> = ({
  visible,
  clips,
  onCancel,
  onCreate,
  loading = false
}) => {
  const [title, setTitle] = useState('')
  const [summary, setSummary] = useState('')
  const [selectedClips, setSelectedClips] = useState<string[]>([])

  const handleCreate = () => {
    if (!title.trim()) {
      return
    }
    onCreate(title.trim(), summary.trim(), selectedClips)
  }

  const handleCancel = () => {
    setTitle('')
    setSummary('')
    setSelectedClips([])
    onCancel()
  }

  const handleClipToggle = (clipId: string) => {
    setSelectedClips(prev => 
      prev.includes(clipId) 
        ? prev.filter(id => id !== clipId)
        : [...prev, clipId]
    )
  }

  const selectAllClips = () => {
    setSelectedClips(clips.map(clip => clip.id))
  }

  const clearAllClips = () => {
    setSelectedClips([])
  }

  return (
    <Modal
      title={null}
      open={visible}
      onCancel={handleCancel}
      footer={null}
      width={900}
      className="create-collection-modal"
      destroyOnClose
    >
      <div className="modal-content">
        {/* EN */}
        <div className="modal-header">
          <div className="header-icon">
            <PlusOutlined />
          </div>
          <div className="header-text">
            <Title level={3} className="modal-title">ENCollection</Title>
            <Text className="modal-subtitle">ENCollection</Text>
          </div>
        </div>

        <Divider className="header-divider" />

        {/* EN */}
        <div className="form-section">
          {/* CollectionTitle */}
          <div className="form-item">
            <div className="form-label">
              <TagOutlined className="label-icon" />
              <Text strong>CollectionTitle</Text>
              <span className="required-mark">*</span>
            </div>
            <Input
              placeholder="Please enterCollectionTitle"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="form-input"
              maxLength={50}
              showCount
            />
          </div>

          {/* CollectionDescription */}
          <div className="form-item">
            <div className="form-label">
              <FileTextOutlined className="label-icon" />
              <Text strong>CollectionDescription</Text>
            </div>
            <TextArea
              placeholder="Please enterCollectionDescription（EN）"
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              className="form-textarea"
              rows={3}
              maxLength={200}
              showCount
            />
          </div>

          {/* Select clip */}
          <div className="form-item">
            <div className="form-label">
              <VideoCameraOutlined className="label-icon" />
              <Text strong>Select clip</Text>
              <span className="required-mark">*</span>
            </div>
            
            <div className="clips-selection">
              <div className="selection-header">
                <Text className="selection-info">
                  EN {selectedClips.length} EN
                </Text>
                <div className="selection-actions">
                  <Button 
                    type="link" 
                    size="small" 
                    onClick={selectAllClips}
                    className="action-btn"
                  >
                    Select all
                  </Button>
                  <Button 
                    type="link" 
                    size="small" 
                    onClick={clearAllClips}
                    className="action-btn"
                  >
                    Clear
                  </Button>
                </div>
              </div>
              
              <div className="clips-grid">
                {clips.map((clip) => (
                  <div 
                    key={clip.id} 
                    className={`clip-item ${selectedClips.includes(clip.id) ? 'selected' : ''}`}
                    onClick={() => handleClipToggle(clip.id)}
                  >
                    <Checkbox 
                      checked={selectedClips.includes(clip.id)}
                      onChange={() => handleClipToggle(clip.id)}
                      className="clip-checkbox"
                    />
                    <div className="clip-content">
                      <div className="clip-title">
                        {clip.generated_title || clip.title || 'Unnamed clip'}
                      </div>
                      <div className="clip-meta">
                        <Text type="secondary" style={{ fontSize: '12px' }}>
                          {clip.start_time} - {clip.end_time} • Score: {(clip.final_score * 100).toFixed(0)}
                        </Text>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* ENActions */}
        <div className="modal-footer">
          <Button onClick={handleCancel} className="cancel-btn">
            Cancel
          </Button>
          <Button 
            type="primary" 
            onClick={handleCreate}
            disabled={!title.trim() || selectedClips.length === 0}
            loading={loading}
            className="create-btn"
          >
            ENCollection
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export default CreateCollectionModal