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

  // fetchENproject tasks
  const allTasks = tasks || []
  const projectTasks = allTasks.filter((task: TaskStatusType) => task.project_id === projectId)
  const activeTasks = projectTasks.filter((task: TaskStatusType) => 
    task.status === 'running' || task.status === 'pending'
  )
  const completedTasks = projectTasks.filter((task: TaskStatusType) => task.status === 'completed')
  const failedTasks = projectTasks.filter((task: TaskStatusType) => task.status === 'failed')

  // RefreshTask list
  const handleRefresh = () => {
    loadProjectTasks(projectId)
    message.success('Task listENRefresh')
  }

  // View tasksDetails
  const handleViewTask = (task: TaskStatusType) => {
    setSelectedTask(task)
    setTaskDetailVisible(true)
  }

  // Deletetask
  const handleDeleteTask = (taskId: string) => {
    confirm({
      title: 'ENDelete',
      icon: <ExclamationCircleOutlined />,
      content: 'DeleteENDeleteEN tasksEN？DeleteEN。',
      okText: 'Delete',
      okType: 'danger',
      cancelText: 'Cancel',
      onOk() {
        message.success(`taskENDelete: ${taskId}`)
      }
    })
  }

  // fetchStatusIcon
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

  // Table columns
  const columns = [
    {
      title: 'taskEN',
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
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'completed' ? 'success' : status === 'running' ? 'processing' : status === 'failed' ? 'error' : status === 'pending' ? 'warning' : 'default'}>
          {status === 'completed' ? 'Completed' :
           status === 'running' ? 'Running' :
           status === 'failed' ? 'Failed' :
           status === 'pending' ? 'Pending' : status}
        </Tag>
      )
    },
    {
      title: 'Progress',
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
      title: 'ENStep',
      dataIndex: 'current_step',
      key: 'current_step',
      render: (step: string) => step || '-'
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (timestamp: string) => (
        <Text type="secondary">
          {new Date(timestamp).toLocaleString('zh-CN')}
        </Text>
      )
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 120,
      render: (_: any, record: TaskStatusType) => (
        <Space size="small">
          <Button
            type="text"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => handleViewTask(record)}
            title="ViewDetails"
          />
          <Button
            type="text"
            size="small"
            icon={<ExclamationCircleOutlined />}
            onClick={() => handleDeleteTask(record.id)}
            title="Deletetask"
            danger
          />
        </Space>
      )
    }
  ]

  if (projectTasks.length === 0) {
    return (
      <Card title="Task management" size="small">
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <Text type="secondary">ENprojectENtaskEN</Text>
        </div>
      </Card>
    )
  }

  return (
    <Card 
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>Task management</span>
          <Button 
            type="primary" 
            size="small"
            icon={<ReloadOutlined />}
            onClick={handleRefresh}
            loading={loading}
          >
            Refresh
          </Button>
        </div>
      }
      size="small"
    >
      {/* Task stats */}
      <Row gutter={16} style={{ marginBottom: '16px' }}>
        <Col span={6}>
          <Statistic
            title="Total tasks"
            value={projectTasks.length}
            prefix={<ClockCircleOutlined />}
          />
        </Col>
        <Col span={6}>
          <Statistic
            title="Active tasks"
            value={activeTasks.length}
            valueStyle={{ color: '#1890ff' }}
            prefix={<ClockCircleOutlined />}
          />
        </Col>
        <Col span={6}>
          <Statistic
            title="Completed"
            value={completedTasks.length}
            valueStyle={{ color: '#52c41a' }}
            prefix={<CheckCircleOutlined />}
          />
        </Col>
        <Col span={6}>
          <Statistic
            title="Failedtask"
            value={failedTasks.length}
            valueStyle={{ color: '#ff4d4f' }}
            prefix={<CloseCircleOutlined />}
          />
        </Col>
      </Row>

      {/* Active tasks */}
      {activeTasks.length > 0 && (
        <Card 
          size="small" 
          style={{ marginBottom: '16px' }}
          title={`Active tasks (${activeTasks.length})`}
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

      {/* Task list */}
      <Table
        columns={columns}
        dataSource={projectTasks}
        rowKey="id"
        pagination={{
          pageSize: 5,
          showSizeChanger: false,
          showTotal: (total, range) => 
            `EN ${range[0]}-${range[1]} EN，Total ${total} EN`
        }}
        size="small"
        loading={loading}
      />

      {/* taskDetailsdialog */}
      <Modal
        title="taskDetails"
        open={taskDetailVisible}
        onCancel={() => setTaskDetailVisible(false)}
        footer={[
          <Button key="close" onClick={() => setTaskDetailVisible(false)}>
            Close
          </Button>
        ]}
        width={800}
      >
        {selectedTask && (
          <div>
            <Text>Task ID: {selectedTask.id}</Text>
            <br />
            <Text>Status: {selectedTask.status}</Text>
            <br />
            <Text>Progress: {selectedTask.progress}%</Text>
            <br />
            <Text>message: {selectedTask.message}</Text>
          </div>
        )}
      </Modal>
    </Card>
  )
}
