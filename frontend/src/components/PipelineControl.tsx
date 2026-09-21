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

  // fetchtranslatedstatus
  const fetchPipelineStatus = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`/api/v1/pipeline/status/${projectId}`);
      if (!response.ok) {
        throw new Error('fetchtranslatedstatusfailed');
      }
      
      const data = await response.json();
      setPipelineStatus(data);
      
      // translatedstatustranslated
      if (onStatusChange) {
        onStatusChange(data.project_status);
      }
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'translatederror');
    } finally {
      setLoading(false);
    }
  };

  // starttranslated
  const startPipeline = async () => {
    try {
      setActionLoading(true);
      
      const response = await fetch(`/api/v1/pipeline/start/${projectId}`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error('starttranslatedfailed');
      }
      
      const result = await response.json();
      message.success(result.message);
      
      // translatedstatus
      await fetchPipelineStatus();
      
    } catch (err) {
      message.error(err instanceof Error ? err.message : 'startfailed');
    } finally {
      setActionLoading(false);
    }
  };

  // translated
  const stopPipeline = async () => {
    try {
      setActionLoading(true);
      
      const response = await fetch(`/api/v1/pipeline/stop/${projectId}`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error('translatedfailed');
      }
      
      const result = await response.json();
      message.success(result.message);
      
      // translatedstatus
      await fetchPipelineStatus();
      
    } catch (err) {
      message.error(err instanceof Error ? err.message : 'translatedfailed');
    } finally {
      setActionLoading(false);
    }
  };

  // translated
  const restartPipeline = async () => {
    try {
      setActionLoading(true);
      
      const response = await fetch(`/api/v1/pipeline/restart/${projectId}`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error('translatedfailed');
      }
      
      const result = await response.json();
      message.success(result.message);
      
      // translatedstatus
      await fetchPipelineStatus();
      
    } catch (err) {
      message.error(err instanceof Error ? err.message : 'translatedfailed');
    } finally {
      setActionLoading(false);
    }
  };

  // translatedstatus
  useEffect(() => {
    if (projectId) {
      fetchPipelineStatus();
      
      // per10secondstranslatedonetranslated
      const interval = setInterval(fetchPipelineStatus, 10000);
      return () => clearInterval(interval);
    }
  }, [projectId]);

  // fetchstatusconfig
  const getStatusConfig = (status: string) => {
    switch (status) {
      case 'processing':
        return { color: 'processing', text: 'processing', icon: <PlayCircleOutlined /> };
      case 'completed':
        return { color: 'success', text: 'completed', icon: <CheckCircleOutlined /> };
      case 'failed':
        return { color: 'error', text: 'failed', icon: <CloseCircleOutlined /> };
      case 'pending':
        return { color: 'default', text: 'etc.translated', icon: <ClockCircleOutlined /> };
      case 'paused':
        return { color: 'warning', text: 'translated', icon: <PauseCircleOutlined /> };
      default:
        return { color: 'default', text: status, icon: <ClockCircleOutlined /> };
    }
  };

  // fetchtaskstatusconfig
  const getTaskStatusConfig = (status: string) => {
    switch (status) {
      case 'running':
        return { color: 'processing', text: 'translated' };
      case 'completed':
        return { color: 'success', text: 'completed' };
      case 'failed':
        return { color: 'error', text: 'failed' };
      case 'pending':
        return { color: 'default', text: 'etc.translated' };
      case 'cancelled':
        return { color: 'warning', text: 'translatedcancel' };
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
            <Text>translatedinfetchtranslatedstatus...</Text>
          </div>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card size="small" style={{ marginBottom: 16 }}>
        <Alert
          message="fetchtranslatedstatusfailed"
          description={error}
          type="error"
          showIcon
          action={
            <Button size="small" onClick={fetchPipelineStatus}>
              translated
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
              translated
            </Title>
            <Tag color={statusConfig.color}>
              {statusConfig.text}
            </Tag>
          </Space>
        </div>

        {/* translatedbytranslated */}
        <Space style={{ marginBottom: 16 }}>
          {canStart && (
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={startPipeline}
              loading={actionLoading}
            >
              starttranslated
            </Button>
          )}
          
          {canStop && (
            <Button
              danger
              icon={<PauseCircleOutlined />}
              onClick={stopPipeline}
              loading={actionLoading}
            >
              translated
            </Button>
          )}
          
          {canRestart && (
            <Button
              icon={<ReloadOutlined />}
              onClick={restartPipeline}
              loading={actionLoading}
            >
              translated
            </Button>
          )}
          
          <Button
            icon={<EyeOutlined />}
            onClick={() => setStatusModalVisible(true)}
          >
            translated
          </Button>
        </Space>

        {/* tasktranslated */}
        <div style={{ display: 'flex', justifyContent: 'space-around', marginBottom: 16 }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1890ff' }}>
              {pipelineStatus.total_tasks}
            </div>
            <div style={{ fontSize: '12px', color: '#666' }}>translatedtask</div>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#52c41a' }}>
              {pipelineStatus.running_tasks}
            </div>
            <div style={{ fontSize: '12px', color: '#666' }}>translated</div>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#faad14' }}>
              {pipelineStatus.completed_tasks}
            </div>
            <div style={{ fontSize: '12px', color: '#666' }}>completed</div>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ff4d4f' }}>
              {pipelineStatus.failed_tasks}
            </div>
            <div style={{ fontSize: '12px', color: '#666' }}>failed</div>
          </div>
        </div>

        {/* translatedtaskprogress */}
        {pipelineStatus.tasks.length > 0 && (
          <div>
            <Text strong>translatedtask:</Text>
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
                  step: {task.realtime_step || task.current_step}
                </div>
              </div>
            ))}
          </div>
        )}

        <div style={{ marginTop: 16, textAlign: 'center' }}>
          <Text type="secondary">statusper10secondstranslatedupdate</Text>
        </div>
      </Card>

      {/* statustranslated */}
      <Modal
        title="translatedstatustranslated"
        open={statusModalVisible}
        onCancel={() => setStatusModalVisible(false)}
        footer={null}
        width={800}
      >
        {pipelineStatus && (
          <div>
            <div style={{ marginBottom: 16 }}>
              <Text strong>projectstatus: </Text>
              <Tag color={statusConfig.color}>{statusConfig.text}</Tag>
            </div>
            
            <List
              header={<Text strong>tasklist</Text>}
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
                        <div>step: {task.realtime_step || task.current_step}</div>
                        {task.step_details && <div>translated: {task.step_details}</div>}
                        <div>createtranslated: {new Date(task.created_at).toLocaleString()}</div>
                        {task.started_at && (
                          <div>translated: {new Date(task.started_at).toLocaleString()}</div>
                        )}
                        {task.completed_at && (
                          <div>translated: {new Date(task.completed_at).toLocaleString()}</div>
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
