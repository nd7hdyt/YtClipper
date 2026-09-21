import React, { useState, useEffect } from 'react';
import { Progress, Card, Tag, Space, Typography, Spin } from 'antd';
import { PlayCircleOutlined, CheckCircleOutlined, CloseCircleOutlined, ClockCircleOutlined } from '@ant-design/icons';

const { Text, Title } = Typography;

interface TaskProgressProps {
  projectId: string;
  taskId?: string;
  status: string;
  onProgressUpdate?: (progress: number, step: string) => void;
}

interface TaskProgressData {
  id: string;
  name: string;
  status: string;
  progress: number;
  current_step: string;
  realtime_progress?: number;
  realtime_step?: string;
  step_details?: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
}

const TaskProgress: React.FC<TaskProgressProps> = ({ 
  projectId, 
  taskId, 
  status, 
  onProgressUpdate 
}) => {
  const [progressData, setProgressData] = useState<TaskProgressData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch task progress
  const fetchTaskProgress = async () => {
    if (!projectId) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`/api/v1/progress/project/${projectId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch progress');
      }
      
      const data = await response.json();
      if (data.tasks && data.tasks.length > 0) {
        // Find the current task or the first running one
        const currentTask = taskId 
          ? data.tasks.find((t: TaskProgressData) => t.id === taskId)
          : data.tasks.find((t: TaskProgressData) => t.status === 'running') || data.tasks[0];
        
        setProgressData(currentTask);
        
        // Notify parent of progress updates
        if (onProgressUpdate) {
          const progress = currentTask.realtime_progress || currentTask.progress;
          const step = currentTask.realtime_step || currentTask.current_step;
          onProgressUpdate(progress, step);
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  // Poll for progress updates
  useEffect(() => {
    if (status === 'processing') {
      // Fetch once immediately
      fetchTaskProgress();
      
      // Update every 5s
      const interval = setInterval(fetchTaskProgress, 5000);
      return () => clearInterval(interval);
    }
  }, [projectId, taskId, status]);

  // Status icon and color
  const getStatusConfig = (status: string) => {
    switch (status) {
      case 'running':
        return { icon: <PlayCircleOutlined />, color: 'processing', text: 'Processing' };
      case 'completed':
        return { icon: <CheckCircleOutlined />, color: 'success', text: 'Completed' };
      case 'failed':
        return { icon: <CloseCircleOutlined />, color: 'error', text: 'Failed' };
      case 'pending':
        return { icon: <ClockCircleOutlined />, color: 'default', text: 'Pending' };
      default:
        return { icon: <ClockCircleOutlined />, color: 'default', text: status };
    }
  };

  // Progress bar status
  const getProgressStatus = (status: string) => {
    switch (status) {
      case 'running':
        return 'active';
      case 'completed':
        return 'success';
      case 'failed':
        return 'exception';
      default:
        return 'normal';
    }
  };

  if (loading) {
    return (
      <Card size="small" style={{ marginBottom: 16 }}>
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <Spin size="large" />
          <div style={{ marginTop: 16 }}>
            <Text>Loading task progress...</Text>
          </div>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card size="small" style={{ marginBottom: 16 }}>
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <CloseCircleOutlined style={{ fontSize: 24, color: '#ff4d4f' }} />
          <div style={{ marginTop: 16 }}>
            <Text type="danger">{error}</Text>
          </div>
        </div>
      </Card>
    );
  }

  if (!progressData) {
    return null;
  }

  const statusConfig = getStatusConfig(progressData.status);
  const progressStatus = getProgressStatus(progressData.status);
  const currentProgress = progressData.realtime_progress || progressData.progress;
  const currentStep = progressData.realtime_step || progressData.current_step;

  return (
    <Card size="small" style={{ marginBottom: 16 }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
        <Space>
          {statusConfig.icon}
          <Title level={5} style={{ margin: 0 }}>
            {progressData.name || 'Video processing task'}
          </Title>
          <Tag color={statusConfig.color}>
            {statusConfig.text}
          </Tag>
        </Space>
      </div>

      <div style={{ marginBottom: 16 }}>
        <Progress
          percent={currentProgress}
          status={progressStatus}
          strokeColor={{
            '0%': '#108ee9',
            '100%': '#87d068',
          }}
        />
      </div>

      <div style={{ marginBottom: 8 }}>
        <Text strong>Current step: </Text>
        <Text>{currentStep || 'Unknown'}</Text>
      </div>

      {progressData.step_details && (
        <div style={{ marginBottom: 8 }}>
          <Text strong>Details: </Text>
          <Text type="secondary">{progressData.step_details}</Text>
        </div>
      )}

      <div style={{ fontSize: '12px', color: '#999' }}>
        <Space split={<Text type="secondary">|</Text>}>
          {progressData.created_at && (
            <Text type="secondary">
              Created: {new Date(progressData.created_at).toLocaleString()}
            </Text>
          )}
          {progressData.started_at && (
            <Text type="secondary">
              Started: {new Date(progressData.started_at).toLocaleString()}
            </Text>
          )}
          {progressData.completed_at && (
            <Text type="secondary">
              Completed: {new Date(progressData.completed_at).toLocaleString()}
            </Text>
          )}
        </Space>
      </div>

      {status === 'processing' && (
        <div style={{ marginTop: 16, textAlign: 'center' }}>
          <Text type="secondary">Progress auto-refreshes every 5s</Text>
        </div>
      )}
    </Card>
  );
};

export default TaskProgress; 