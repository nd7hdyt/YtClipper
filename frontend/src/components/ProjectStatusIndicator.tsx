import React from 'react'
import { Badge, Tooltip } from 'antd'
import { Project } from '../store/useProjectStore'
// import { 
//   getProjectStatusConfig, 
//   normalizeProjectStatus 
// } from '../utils/statusUtils'

interface ProjectStatusIndicatorProps {
  project: Project
  showProgress?: boolean
  size?: 'small' | 'default' | 'large'
}

const ProjectStatusIndicator: React.FC<ProjectStatusIndicatorProps> = ({
  project,
  size = 'default'
}) => {
  // Simple status handling for now
  const normalizedStatus = project.status === 'error' ? 'failed' : project.status

  const getStepName = () => {
    if (normalizedStatus === 'processing' && project.current_step) {
      const stepNames = {
        1: 'Outline analysis',
        2: 'Timeline generation',
        3: 'Clip scoring',
        4: 'Title generation',
        5: 'Topic clustering',
        6: 'Video rendering'
      }
      return stepNames[project.current_step as keyof typeof stepNames] || 'Processing'
    }
    return 'Processing'
  }

  const getStatusConfig = () => {
    switch (normalizedStatus) {
      case 'processing':
        return { text: 'Processing', badgeStatus: 'processing' as const, color: '#1890ff' }
      case 'completed':
        return { text: 'Completed', badgeStatus: 'success' as const, color: '#52c41a' }
      case 'failed':
        return { text: 'Failed', badgeStatus: 'error' as const, color: '#ff4d4f' }
      default:
        return { text: 'Unknown', badgeStatus: 'default' as const, color: '#d9d9d9' }
    }
  }

  const config = getStatusConfig()

  if (size === 'small') {
    return (
      <Tooltip title={getStepName()}>
        <Badge status={config.badgeStatus} text={config.text} />
      </Tooltip>
    )
  }

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '100%',
      padding: '4px 8px',
      borderRadius: '4px',
      backgroundColor: `${config.color}15`,
      border: `1px solid ${config.color}30`,
      color: config.color,
      fontSize: '12px',
      fontWeight: 500,
      minHeight: '24px'
    }}>
      <span style={{ marginRight: '4px', display: 'flex', alignItems: 'center' }}>
        {config.text}
      </span>
      <span>{config.text}</span>
    </div>
  )
}

export default ProjectStatusIndicator