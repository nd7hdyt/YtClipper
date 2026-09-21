/**
 * Simplified project card - new progress system
 */

import React, { useState, useEffect } from 'react'
import { Card, Typography, Space, Button, Tag, Tooltip, Modal, message } from 'antd'
import { 
  PlayCircleOutlined, 
  EyeOutlined, 
  DeleteOutlined, 
  ReloadOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { SimpleProgressBar } from './SimpleProgressBar'
import { 
  useSimpleProgressStore, 
  isCompleted, 
  isFailed,
  SimpleProgress 
} from '../stores/useSimpleProgressStore'

const { Title, Text } = Typography

interface Project {
  id: string
  title: string
  description?: string
  status: string
  created_at: string
  updated_at: string
  video_path?: string
  srt_path?: string
  category?: string
}

interface SimpleProjectCardProps {
  project: Project
  onStartProcessing?: (projectId: string) => void
  onViewDetails?: (projectId: string) => void
  onDelete?: (projectId: string) => void
  onRetry?: (projectId: string) => void
}

export const SimpleProjectCard: React.FC<SimpleProjectCardProps> = ({
  project,
  onStartProcessing,
  onViewDetails,
  onDelete,
  onRetry
}) => {
  const navigate = useNavigate()
  const { getProgress, startPolling, stopPolling } = useSimpleProgressStore()
  const [showProgress, setShowProgress] = useState(false)
  
  const progress = getProgress(project.id)

  // Show progress based on project status
  useEffect(() => {
    if (project.status === 'processing') {
      setShowProgress(true)
      // Poll this project's progress
      startPolling([project.id], 2000)
    } else {
      setShowProgress(false)
      stopPolling()
    }
  }, [project.status, project.id, startPolling, stopPolling])

  const handleStartProcessing = () => {
    if (onStartProcessing) {
      onStartProcessing(project.id)
    }
  }

  const handleViewDetails = () => {
    if (onViewDetails) {
      onViewDetails(project.id)
    } else {
      navigate(`/project/${project.id}`)
    }
  }

  const handleDelete = () => {
    Modal.confirm({
      title: 'Confirm delete',
      content: `Delete project "${project.title}"? This cannot be undone.`,
      okText: 'Delete',
      okType: 'danger',
      cancelText: 'Cancel',
      onOk: () => {
        if (onDelete) {
          onDelete(project.id)
        }
      }
    })
  }

  const handleRetry = () => {
    if (onRetry) {
      onRetry(project.id)
    }
  }

  // Status icon and color
  const getStatusConfig = (status: string, progress?: SimpleProgress) => {
    if (progress && isFailed(progress.message)) {
      return {
        icon: <ExclamationCircleOutlined />,
        color: '#ff4d4f',
        text: 'Failed'
      }
    }
    
    if (progress && isCompleted(progress.stage)) {
      return {
        icon: <CheckCircleOutlined />,
        color: '#52c41a',
        text: 'Completed'
      }
    }
    
    if (status === 'processing' || (progress && !isCompleted(progress.stage))) {
      return {
        icon: <ReloadOutlined spin />,
        color: '#1890ff',
        text: 'Processing'
      }
    }
    
    return {
      icon: <PlayCircleOutlined />,
      color: '#666666',
      text: 'Pending'
    }
  }

  const statusConfig = getStatusConfig(project.status, progress || undefined)
  const canStart = project.status === 'pending' || project.status === 'failed'
  const canRetry = project.status === 'failed' || (progress && isFailed(progress.message))

  return (
    <Card
      hoverable
      style={{ margin: '8px 0' }}
      actions={[
        canStart && (
          <Tooltip title="Start processing">
            <Button 
              type="primary" 
              icon={<PlayCircleOutlined />}
              onClick={handleStartProcessing}
            >
              Start processing
            </Button>
          </Tooltip>
        ),
        canRetry && (
          <Tooltip title="Retry">
            <Button 
              icon={<ReloadOutlined />}
              onClick={handleRetry}
            >
              Retry
            </Button>
          </Tooltip>
        ),
        <Tooltip title="View details">
          <Button 
            icon={<EyeOutlined />}
            onClick={handleViewDetails}
          >
            View details
          </Button>
        </Tooltip>,
        <Tooltip title="Delete project">
          <Button 
            danger 
            icon={<DeleteOutlined />}
            onClick={handleDelete}
          >
            Delete
          </Button>
        </Tooltip>
      ].filter(Boolean)}
    >
      <Space direction="vertical" style={{ width: '100%' }}>
        {/* Title and status */}
        <Space align="center" style={{ width: '100%', justifyContent: 'space-between' }}>
          <Title level={5} style={{ margin: 0, flex: 1 }}>
            {project.title}
          </Title>
          <Tag 
            color={statusConfig.color} 
            icon={statusConfig.icon}
            style={{ margin: 0 }}
          >
            {statusConfig.text}
          </Tag>
        </Space>

        {/* Project description */}
        {project.description && (
          <Text type="secondary" style={{ fontSize: '12px' }}>
            {project.description}
          </Text>
        )}

        {/* Category tag */}
        {project.category && (
          <Tag color="blue" style={{ fontSize: '11px' }}>
            {project.category}
          </Tag>
        )}

        {/* Progress bar */}
        {showProgress && (
          <SimpleProgressBar
            projectId={project.id}
            autoStart={false} // Already handled in useEffect
            showDetails={true}
            onProgressUpdate={(progress) => {
              // Hide once completed
              if (isCompleted(progress.stage)) {
                setShowProgress(false)
                message.success('Project completed!')
              } else if (isFailed(progress.message)) {
                message.error('Project failed!')
              }
            }}
          />
        )}

        {/* Timestamps */}
        <Space style={{ fontSize: '11px', color: '#999' }}>
          <Text type="secondary">
            Created: {new Date(project.created_at).toLocaleDateString()}
          </Text>
          <Text type="secondary">
            Updated: {new Date(project.updated_at).toLocaleDateString()}
          </Text>
        </Space>
      </Space>
    </Card>
  )
}
