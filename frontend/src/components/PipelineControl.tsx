import React, { useState, useEffect } from 'react';
import { Card, Button, Space, Typography, Alert, Spin, Progress, Tag, List, Modal, message } from 'antd';
import { 
  PlayCircleOutlined, 
  PauseCircleOutlined, 
  ReloadOutlined, 
  EyeOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

interface PipelineControlProps {
  projectId: string;
  onStatusChange?: (status: string) => void;
}

interface TaskInfo {
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

interface PipelineStatus {
  project_id: string;
  project_status: string;
  tasks: TaskInfo[];
  total_tasks: number;
  running_tasks: number;
  completed_tasks: number;
  failed_tasks: number;
}

const PipelineControl: React.FC<PipelineControlProps> = ({ 
  projectId, 
  onStatusChange 
}) => {
  const [pipelineStatus, setPipelineStatus] = useState<PipelineStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [statusModalVisible, setStatusModalVisible] = useState(false);

  // Fetch pipelineStatus
  const fetchPipelineStatus = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`/api/v1/pipeline/status/${projectId}`);
      if (!response.ok) {
        throw new Error('Fetch pipelineStatusFailed');
      }
      
      const data = await response.json();
      setPipelineStatus(data);
      
      // ENStatusChange
      if (onStatusChange) {
        onStatusChange(data.project_status);
      }
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  // Start pipeline
  const startPipeline = async () => {
    try {
      setActionLoading(true);
      
      const response = await fetch(`/api/v1/pipeline/start/${projectId}`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error('Start pipelineFailed');
      }
      
      const result = await response.json();
      message.success(result.message);
      
      // RefreshStatus
      await fetchPipelineStatus();
      
    } catch (err) {
      message.error(err instanceof Error ? err.message : 'ENFailed');
    } finally {
      setActionLoading(false);
    }
  };

  // Stop pipeline
  const stopPipeline = async () => {
    try {
      setActionLoading(true);
      
      const response = await fetch(`/api/v1/pipeline/stop/${projectId}`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error('Stop pipelineFailed');
      }
      
      const result = await response.json();
      message.success(result.message);
      
      // RefreshStatus
      await fetchPipelineStatus();
      
    } catch (err) {
      message.error(err instanceof Error ? err.message : 'ENFailed');
    } finally {
      setActionLoading(false);
    }
  };

  // Restart pipeline
  const restartPipeline = async () => {
    try {
      setActionLoading(true);
      
      const response = await fetch(`/api/v1/pipeline/restart/${projectId}`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error('Restart pipelineFailed');
      }
      
      const result = await response.json();
      message.success(result.message);
      
      // RefreshStatus
      await fetchPipelineStatus();
      
    } catch (err) {
      message.error(err instanceof Error ? err.message : 'ENFailed');
    } finally {
      setActionLoading(false);
    }
  };

  // ENRefreshStatus
  useEffect(() => {
    if (projectId) {
      fetchPipelineStatus();
      
      // EN10ENRefreshonce
      const interval = setInterval(fetchPipelineStatus, 10000);
      return () => clearInterval(interval);
    }
  }, [projectId]);

  // fetchStatusconfig
  const getStatusConfig = (status: string) => {
    switch (status) {
      case 'processing':
        return { color: 'processing', text: 'Processing', icon: <PlayCircleOutlined /> };
      case 'completed':
        return { color: 'success', text: 'Completed', icon: <CheckCircleOutlined /> };
      case 'failed':
        return { color: 'error', text: 'Failed', icon: <CloseCircleOutlined /> };
      case 'pending':
        return { color: 'default', text: 'Pending', icon: <ClockCircleOutlined /> };
      case 'paused':
        return { color: 'warning', text: 'EN', icon: <PauseCircleOutlined /> };
      default:
        return { color: 'default', text: status, icon: <ClockCircleOutlined /> };
    }
  };

  // Fetch tasksStatusconfig
  const getTaskStatusConfig = (status: string) => {
    switch (status) {
      case 'running':
        return { color: 'processing', text: 'running' };
      case 'completed':
        return { color: 'success', text: 'Completed' };
      case 'failed':
        return { color: 'error', text: 'Failed' };
      case 'pending':
        return { color: 'default', text: 'Pending' };
      case 'cancelled':
        return { color: 'warning', text: 'Cancelled' };
      default:
        return { color: 'default', text: status };
    }
  };

  if (loading) {
    return (
      <Card size="small" style={{ marginBottom: 16 }}>
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <Spin size="large" />
          <div style={{ marginTop: 16 }}>
            <Text>ENFetch pipelineStatus...</Text>
          </div>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card size="small" style={{ marginBottom: 16 }}>
        <Alert
          message="Fetch pipelineStatusFailed"
          description={error}
          type="error"
          showIcon
          action={
            <Button size="small" onClick={fetchPipelineStatus}>
              Retry
            </Button>
          }
        />
      </Card>
    );
  }

  if (!pipelineStatus) {
    return null;
  }

  const statusConfig = getStatusConfig(pipelineStatus.project_status);
  const canStart = pipelineStatus.project_status === 'pending' || pipelineStatus.project_status === 'failed';
  const canStop = pipelineStatus.project_status === 'processing';
  const canRestart = pipelineStatus.project_status === 'processing' || pipelineStatus.project_status === 'failed';

  return (
    <>
      <Card size="small" style={{ marginBottom: 16 }}>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
          <Space>
            {statusConfig.icon}
            <Title level={5} style={{ margin: 0 }}>
              EN
            </Title>
            <Tag color={statusConfig.color}>
              {statusConfig.text}
            </Tag>
          </Space>
        </div>

        {/* EN */}
        <Space style={{ marginBottom: 16 }}>
          {canStart && (
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={startPipeline}
              loading={actionLoading}
            >
              Start pipeline
            </Button>
          )}
          
          {canStop && (
            <Button
              danger
              icon={<PauseCircleOutlined />}
              onClick={stopPipeline}
              loading={actionLoading}
            >
              Stop pipeline
            </Button>
          )}
          
          {canRestart && (
            <Button
              icon={<ReloadOutlined />}
              onClick={restartPipeline}
              loading={actionLoading}
            >
              Restart pipeline
            </Button>
          )}
          
          <Button
            icon={<EyeOutlined />}
            onClick={() => setStatusModalVisible(true)}
          >
            ViewDetails
          </Button>
        </Space>

        {/* Task stats */}
        <div style={{ display: 'flex', justifyContent: 'space-around', marginBottom: 16 }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1890ff' }}>
              {pipelineStatus.total_tasks}
            </div>
            <div style={{ fontSize: '12px', color: '#666' }}>ENtask</div>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#52c41a' }}>
              {pipelineStatus.running_tasks}
            </div>
            <div style={{ fontSize: '12px', color: '#666' }}>running</div>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#faad14' }}>
              {pipelineStatus.completed_tasks}
            </div>
            <div style={{ fontSize: '12px', color: '#666' }}>Completed</div>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ff4d4f' }}>
              {pipelineStatus.failed_tasks}
            </div>
            <div style={{ fontSize: '12px', color: '#666' }}>Failed</div>
          </div>
        </div>

        {/* Current taskProgress */}
        {pipelineStatus.tasks.length > 0 && (
          <div>
            <Text strong>Current task:</Text>
            {pipelineStatus.tasks.map((task) => (
              <div key={task.id} style={{ marginTop: 8 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                  <Text>{task.name}</Text>
                  <Tag color={getTaskStatusConfig(task.status).color}>
                    {getTaskStatusConfig(task.status).text}
                  </Tag>
                </div>
                
                <Progress
                  percent={task.realtime_progress || task.progress}
                  size="small"
                  status={task.status === 'failed' ? 'exception' : 'normal'}
                />
                
                <div style={{ fontSize: '12px', color: '#666', marginTop: 4 }}>
                  Step: {task.realtime_step || task.current_step}
                </div>
              </div>
            ))}
          </div>
        )}

        <div style={{ marginTop: 16, textAlign: 'center' }}>
          <Text type="secondary">StatusEN10ENupdate</Text>
        </div>
      </Card>

      {/* StatusDetailsmodal */}
      <Modal
        title="ENStatusDetails"
        open={statusModalVisible}
        onCancel={() => setStatusModalVisible(false)}
        footer={null}
        width={800}
      >
        {pipelineStatus && (
          <div>
            <div style={{ marginBottom: 16 }}>
              <Text strong>projectStatus: </Text>
              <Tag color={statusConfig.color}>{statusConfig.text}</Tag>
            </div>
            
            <List
              header={<Text strong>Task list</Text>}
              dataSource={pipelineStatus.tasks}
              renderItem={(task) => (
                <List.Item>
                  <List.Item.Meta
                    title={
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Text>{task.name}</Text>
                        <Tag color={getTaskStatusConfig(task.status).color}>
                          {getTaskStatusConfig(task.status).text}
                        </Tag>
                      </div>
                    }
                    description={
                      <div>
                        <div>Step: {task.realtime_step || task.current_step}</div>
                        {task.step_details && <div>Details: {task.step_details}</div>}
                        <div>Created: {new Date(task.created_at).toLocaleString()}</div>
                        {task.started_at && (
                          <div>Start time: {new Date(task.started_at).toLocaleString()}</div>
                        )}
                        {task.completed_at && (
                          <div>CompletedEN: {new Date(task.completed_at).toLocaleString()}</div>
                        )}
                      </div>
                    }
                  />
                  
                  <div style={{ width: 200 }}>
                    <Progress
                      percent={task.realtime_progress || task.progress}
                      status={task.status === 'failed' ? 'exception' : 'normal'}
                    />
                  </div>
                </List.Item>
              )}
            />
          </div>
        )}
      </Modal>
    </>
  );
};

export default PipelineControl;
