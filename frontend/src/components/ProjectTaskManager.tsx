import React, { useState } from 'react'
import { Card, Table, Tag, Progress, Space, Typography, Button, Modal, message, Row, Col, Statistic } from 'antd'
import { ReloadOutlined, EyeOutlined, ExclamationCircleOutlined, CheckCircleOutlined, ClockCircleOutlined, CloseCircleOutlined } from '@ant-design/icons'
import { useTaskStatus } from '../hooks/useTaskStatus'
import { TaskStatus as TaskStatusType } from '../hooks/useTaskStatus'

const { Text } = Typography
const { confirm } = Modal

interface ProjectTaskManagerProps {
  projectId: string
  projectName?: string
}

export const ProjectTaskManager: React.FC<ProjectTaskManagerProps> = ({ 
  projectId
}) => {
  const { tasks, loading, loadProjectTasks } = useTaskStatus()
  const [selectedTask, setSelectedTask] = useState<TaskStatusType | null>(null)
  const [taskDetailVisible, setTaskDetailVisible] = useState(false)

  // fetchtranslatedproject'stask
  const allTasks = tasks || []
  const projectTasks = allTasks.filter((task: TaskStatusType) => task.project_id === projectId)
  const activeTasks = projectTasks.filter((task: TaskStatusType) => 
    task.status === 'running' || task.status === 'pending'
  )
  const completedTasks = projectTasks.filter((task: TaskStatusType) => task.status === 'completed')
  const failedTasks = projectTasks.filter((task: TaskStatusType) => task.status === 'failed')

  // translatedtasklist
  const handleRefresh = () => {
    loadProjectTasks(projectId)
    message.success('tasklisttranslated')
  }

  // translatedtasktranslated
  const handleViewTask = (task: TaskStatusType) => {
    setSelectedTask(task)
    setTaskDetailVisible(true)
  }

  // deletetask
  const handleDeleteTask = (taskId: string) => {
    confirm({
      title: 'Confirmdelete',
      icon: <ExclamationCircleOutlined />,
      content: 'translateddeletethis tasktranslated？deletetranslated。',
      okText: 'delete',
      okType: 'danger',
      cancelText: 'cancel',
      onOk() {
        message.success(`tasktranslateddelete: ${taskId}`)
      }
    })
  }

  // fetchstatustranslated
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />
      case 'running':
        return <ClockCircleOutlined style={{ color: '#1890ff' }} />
      case 'failed':
        return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />
      case 'pending':
        return <ClockCircleOutlined style={{ color: '#faad14' }} />
      default:
        return <ClockCircleOutlined style={{ color: '#d9d9d9' }} />
    }
  }

  // translated
  const columns = [
    {
      title: 'tasktranslated',
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: TaskStatusType) => (
        <Space>
          {getStatusIcon(record.status)}
          <Text strong>{text}</Text>
        </Space>
      )
    },
    {
      title: 'status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'completed' ? 'success' : status === 'running' ? 'processing' : status === 'failed' ? 'error' : status === 'pending' ? 'warning' : 'default'}>
          {status === 'completed' ? 'completed' :
           status === 'running' ? 'translated' :
           status === 'failed' ? 'failed' :
           status === 'pending' ? 'etc.translated' : status}
        </Tag>
      )
    },
    {
      title: 'progress',
      dataIndex: 'progress',
      key: 'progress',
      render: (progress: number, record: TaskStatusType) => (
        <Progress 
          percent={Math.round(progress)} 
          size="small"
          status={record.status === 'failed' ? 'exception' : 'normal'}
        />
      )
    },
    {
      title: 'translatedstep',
      dataIndex: 'current_step',
      key: 'current_step',
      render: (step: string) => step || '-'
    },
    {
      title: 'createtranslated',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (timestamp: string) => (
        <Text type="secondary">
          {new Date(timestamp).toLocaleString('zh-CN')}
        </Text>
      )
    },
    {
      title: 'translated',
      key: 'actions',
      width: 120,
      render: (_: any, record: TaskStatusType) => (
        <Space size="small">
          <Button
            type="text"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => handleViewTask(record)}
            title="translated"
          />
          <Button
            type="text"
            size="small"
            icon={<ExclamationCircleOutlined />}
            onClick={() => handleDeleteTask(record.id)}
            title="deletetask"
            danger
          />
        </Space>
      )
    }
  ]

  if (projectTasks.length === 0) {
    return (
      <Card title="tasktranslated" size="small">
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <Text type="secondary">translatedprojectNot yettasktranslated</Text>
        </div>
      </Card>
    )
  }

  return (
    <Card 
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>tasktranslated</span>
          <Button 
            type="primary" 
            size="small"
            icon={<ReloadOutlined />}
            onClick={handleRefresh}
            loading={loading}
          >
            translated
          </Button>
        </div>
      }
      size="small"
    >
      {/* tasktranslated */}
      <Row gutter={16} style={{ marginBottom: '16px' }}>
        <Col span={6}>
          <Statistic
            title="translatedtasktranslated"
            value={projectTasks.length}
            prefix={<ClockCircleOutlined />}
          />
        </Col>
        <Col span={6}>
          <Statistic
            title="translatedtask"
            value={activeTasks.length}
            valueStyle={{ color: '#1890ff' }}
            prefix={<ClockCircleOutlined />}
          />
        </Col>
        <Col span={6}>
          <Statistic
            title="completed"
            value={completedTasks.length}
            valueStyle={{ color: '#52c41a' }}
            prefix={<CheckCircleOutlined />}
          />
        </Col>
        <Col span={6}>
          <Statistic
            title="failedtask"
            value={failedTasks.length}
            valueStyle={{ color: '#ff4d4f' }}
            prefix={<CloseCircleOutlined />}
          />
        </Col>
      </Row>

      {/* translatedtask */}
      {activeTasks.length > 0 && (
        <Card 
          size="small" 
          style={{ marginBottom: '16px' }}
          title={`translatedtask (${activeTasks.length})`}
        >
          <Space wrap>
            {activeTasks.map((task: TaskStatusType) => (
              <div key={task.id} style={{ marginBottom: '8px' }}>
                <Text>{task.message || task.id}</Text>
                <Progress percent={task.progress} size="small" />
              </div>
            ))}
          </Space>
        </Card>
      )}

      {/* tasklist */}
      <Table
        columns={columns}
        dataSource={projectTasks}
        rowKey="id"
        pagination={{
          pageSize: 5,
          showSizeChanger: false,
          showTotal: (total, range) => 
            `No. ${range[0]}-${range[1]} translated，translated ${total} translated`
        }}
        size="small"
        loading={loading}
      />

      {/* tasktranslated */}
      <Modal
        title="tasktranslated"
        open={taskDetailVisible}
        onCancel={() => setTaskDetailVisible(false)}
        footer={[
          <Button key="close" onClick={() => setTaskDetailVisible(false)}>
            translated
          </Button>
        ]}
        width={800}
      >
        {selectedTask && (
          <div>
            <Text>taskID: {selectedTask.id}</Text>
            <br />
            <Text>status: {selectedTask.status}</Text>
            <br />
            <Text>progress: {selectedTask.progress}%</Text>
            <br />
            <Text>translated: {selectedTask.message}</Text>
          </div>
        )}
      </Modal>
    </Card>
  )
}
