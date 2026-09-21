import React, { useState, useRef, useEffect } from 'react'
import { Input, Button, Space, message, Tooltip, Modal } from 'antd'
import { EditOutlined, CheckOutlined } from '@ant-design/icons'
import { projectApi } from '../services/api'
import MagicWandIcon from './icons/MagicWandIcon'

interface EditableTitleProps {
  title: string
  clipId: string
  onTitleUpdate?: (newTitle: string) => void
  maxLength?: number
  style?: React.CSSProperties
  className?: string
}

const EditableTitle: React.FC<EditableTitleProps> = ({
  title,
  clipId,
  onTitleUpdate,
  maxLength = 200,
  style,
  className
}) => {
  const [isEditing, setIsEditing] = useState(false)
  const [editValue, setEditValue] = useState(title)
  const [loading, setLoading] = useState(false)
  const [generating, setGenerating] = useState(false)
  const inputRef = useRef<any>(null)

  // translatedtitletranslated，translatedstatus
  useEffect(() => {
    setEditValue(title)
  }, [title])

  // translatedtitletranslated，iftranslatedintranslated，ensuretranslated
  useEffect(() => {
    if (!isEditing) {
      setEditValue(title)
    }
  }, [title, isEditing])

  // translated
  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus()
      // TextAreatranslatedselecttranslated，usesetSelectionRangetranslated
      if (inputRef.current.setSelectionRange) {
        inputRef.current.setSelectionRange(0, inputRef.current.value.length)
      }
    }
  }, [isEditing])

  const handleStartEdit = () => {
    setEditValue(title)
    setIsEditing(true)
  }

  const handleCancel = () => {
    setEditValue(title)
    setIsEditing(false)
  }

  const handleSave = async () => {
    const trimmedValue = editValue.trim()
    
    if (!trimmedValue) {
      message.error('translated')
      return
    }
    
    if (trimmedValue.length > maxLength) {
      message.error(`translated${maxLength} translated`)
      return
    }
    
    if (trimmedValue === title) {
      setIsEditing(false)
      return
    }

    setLoading(true)
    try {
      await projectApi.updateClipTitle(clipId, trimmedValue)
      message.success('translatedupdatesucceeded')
      setIsEditing(false)
      // translatedupdatelocalstatus，translatedcalltranslated
      onTitleUpdate?.(trimmedValue)
    } catch (error: any) {
      console.error('updatetranslatedfailed:', error)
      message.error(error.userMessage || error.message || 'updatetranslatedfailed')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateTitle = async () => {
    console.log('translated，clipId:', clipId)
    setGenerating(true)
    try {
      const result = await projectApi.generateClipTitle(clipId)
      console.log('translated:', result)
      if (result.success && result.generated_title) {
        setEditValue(result.generated_title)
        message.success('translatedsucceeded，translatedcantranslatedorclicktranslated')
      } else {
        message.error('translatedfailed')
      }
    } catch (error: any) {
      console.error('translatedfailed:', error)
      message.error(error.userMessage || error.message || 'translatedfailed')
    } finally {
      setGenerating(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSave()
    } else if (e.key === 'Escape') {
      handleCancel()
    }
  }

  if (isEditing) {
    return (
      <Modal
        title="translated"
        open={isEditing}
        onCancel={handleCancel}
        footer={null}
        width={600}
        destroyOnClose
        maskClosable={false}
      >
        <div style={{ marginBottom: '16px' }}>
          <Input.TextArea
            ref={inputRef}
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            onKeyDown={handleKeyPress}
            maxLength={maxLength}
            placeholder="translated"
            autoSize={{ minRows: 3, maxRows: 8 }}
            style={{ 
              resize: 'none',
              fontSize: '14px',
              lineHeight: '1.5'
            }}
          />
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ fontSize: '12px', color: '#666' }}>
            translated: {editValue.length}/{maxLength}
          </div>
          <Space>
            <Tooltip title="AItranslated">
              <Button
                icon={<MagicWandIcon />}
                loading={generating}
                onClick={() => {
                  console.log('AItranslatedbytranslatedclick');
                  handleGenerateTitle();
                }}
                disabled={loading}
              >
                AItranslated
              </Button>
            </Tooltip>
            <Button onClick={handleCancel} disabled={loading || generating}>
              cancel
            </Button>
            <Button
              type="primary"
              icon={<CheckOutlined />}
              loading={loading}
              onClick={handleSave}
              disabled={generating}
            >
              translated
            </Button>
          </Space>
        </div>
      </Modal>
    )
  }

  return (
    <div
      style={{
        cursor: 'text',
        ...style
      }}
      className={`ac-editable ${className || ''}`}
      onClick={handleStartEdit}
      title="clicktranslated"
    >
      <span style={{ wordBreak: 'break-word', display: 'inline' }}>
        {title}
        <EditOutlined
          className="ac-editable-pen"
          style={{
            color: 'var(--ac-muted)',
            fontSize: '11px',
            opacity: 0,
            transition: 'opacity 0.15s',
            marginLeft: '6px',
            display: 'inline'
          }}
        />
      </span>
    </div>
  )
}

export default EditableTitle
