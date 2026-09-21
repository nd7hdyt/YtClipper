import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Layout, Card, Progress, Steps, Typography, Button, Alert, Space, Spin, message } from 'antd'
import { CheckCircleOutlined, LoadingOutlined, ExclamationCircleOutlined, ArrowLeftOutlined } from '@ant-design/icons'
import { projectApi } from '../services/api'
import { useProjectStore } from '../store/useProjectStore'

const { Content } = Layout
const { Title, Text } = Typography
const { Step } = Steps

interface ProcessingStatus {
  status: 'processing' | 'completed' | 'error'
  current_step: number
  total_steps: number
  step_name: string
  progress: number
  error_message?: string
}

const ProcessingPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { currentProject, setCurrentProject } = useProjectStore()
  const [status, setStatus] = useState<ProcessingStatus | null>(null)
  const [loading, setLoading] = useState(true)

  const steps = [
    { title: 'Outline extraction', description: 'Extract a structural outline from the video transcription' },
    { title: 'Timeline locating', description: 'Locate topic time ranges based on SRT subtitles' },
    { title: 'Content scoring', description: 'Score clip quality and viral potential on multiple dimensions' },
    { title: 'Title generation', description: 'Generate engaging titles for top-scoring clips' },
    { title: 'Topic clustering', description: 'Group related clips into collection recommendations' },
    { title: 'Video cutting', description: 'Generate clip and collection videos with FFmpeg' }
  ]

  useEffect(() => {
    if (!id) return
    
    loadProject()
    const interval = setInterval(checkStatus, 2000) // Check status every 2s
    
    return () => clearInterval(interval)
  }, [id])

  const loadProject = async () => {
    if (!id) return
    
    try {
      const project = await projectApi.getProject(id)
      setCurrentProject(project)
      
      // If the project is completed, jump straight to the detail page
      if (project.status === 'completed') {
        navigate(`/project/${id}`)
        return
      }
      
      // If the project is pending, start processing
      if (project.status === 'pending') {
        await startProcessing()
      }
    } catch (error) {
      message.error('Failed to load project')
      console.error('Load project error:', error)
    } finally {
      setLoading(false)
    }
  }

  const startProcessing = async () => {
    if (!id) return
    
    try {
      await projectApi.startProcessing(id)
      message.success('Started processing project')
    } catch (error) {
      message.error('Failed to start processing')
      console.error('Start processing error:', error)
    }
  }

  const checkStatus = async () => {
    if (!id) return
    
    try {
      const statusData = await projectApi.getProcessingStatus(id)
      setStatus(statusData)
      
      // If processing is completed, jump to the project detail page
      if (statusData.status === 'completed') {
        message.success('Video processing complete! Jumping to the results page...')
        setTimeout(() => {
          navigate(`/project/${id}`)
        }, 2000)
      }
      
      // If processing failed, show the detailed error
      if (statusData.status === 'error') {
        const errorMsg = statusData.error_message || 'Unknown error during processing'
        message.error(`Processing failed: ${errorMsg}`)
        
        // Offer a retry option
        message.info('You can go back home to re-upload the file or contact support', 5)
      }
      
    } catch (error: any) {
      console.error('Check status error:', error)
      
      // Suggest follow-ups based on error type
      if (error.response?.status === 404) {
        message.error('Project not found or already deleted')
        setTimeout(() => navigate('/'), 2000)
      } else if (error.code === 'ECONNABORTED') {
        message.warning('Network timeout, retrying...')
      } else {
        message.error('Failed to fetch processing status, please refresh and retry')
      }
    }
  }

  const getStepStatus = (stepIndex: number) => {
    if (!status) return 'wait'
    
    if (status.status === 'error') {
      return stepIndex < status.current_step ? 'finish' : 'error'
    }
    
    if (stepIndex < status.current_step) return 'finish'
    if (stepIndex === status.current_step) return 'process'
    return 'wait'
  }

  const getStepIcon = (stepIndex: number) => {
    const stepStatus = getStepStatus(stepIndex)
    
    if (stepStatus === 'finish') return <CheckCircleOutlined />
    if (stepStatus === 'process') return <LoadingOutlined />
    if (stepStatus === 'error') return <ExclamationCircleOutlined />
    return null
  }

  if (loading) {
    return (
      <Content style={{ padding: '24px', display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
        <Spin size="large" tip="Loading..." />
      </Content>
    )
  }

  return (
    <Content style={{ padding: '24px', maxWidth: '1000px', margin: '0 auto' }}>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Title level={2}>Video processing progress</Title>
          <Button 
            icon={<ArrowLeftOutlined />} 
            onClick={() => navigate('/')}
          >
            Back to Home
          </Button>
        </div>

        {currentProject && (
          <Card>
            <Title level={4}>{currentProject.name}</Title>
            <Text type="secondary">Project ID: {currentProject.id}</Text>
          </Card>
        )}

        {status?.status === 'error' && (
          <Alert
            message="Processing failed"
            description={
              <div>
                <p>{status.error_message || 'Unknown error during processing'}</p>
                <p style={{ marginTop: '8px', fontSize: '12px', color: '#666' }}>
                  Possible causes: unsupported file format, corrupted file, network issue, or server error
                </p>
              </div>
            }
            type="error"
            showIcon
            action={
              <Space>
                <Button size="small" onClick={() => window.location.reload()}>
                  Refresh
                </Button>
                <Button size="small" onClick={() => navigate('/')}>
                  Back to Home
                </Button>
              </Space>
            }
          />
        )}

        {status && status.status === 'processing' && (
          <Card title="Processing progress">
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <Text strong>Overall progress</Text>
                  <Text>{Math.round(status.progress)}%</Text>
                </div>
                <Progress 
                  percent={status.progress} 
                  status="active"
                  strokeColor={{
                    '0%': '#108ee9',
                    '100%': '#87d068',
                  }}
                />
              </div>

              <div>
                <Text strong>Current step: </Text>
                <Text>{status.step_name}</Text>
              </div>

              <Steps 
                direction="vertical" 
                current={status.current_step}
                status="process"
              >
                {steps.map((step, index) => (
                  <Step
                    key={index}
                    title={step.title}
                    description={step.description}
                    status={getStepStatus(index)}
                    icon={getStepIcon(index)}
                  />
                ))}
              </Steps>
            </Space>
          </Card>
        )}

        {status?.status === 'completed' && (
          <Alert
            message="Processing complete"
            description="Video processed successfully, jumping to the project detail page..."
            type="success"
            showIcon
          />
        )}
      </Space>
    </Content>
  )
}

export default ProcessingPage