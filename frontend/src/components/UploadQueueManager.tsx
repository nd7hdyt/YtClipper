import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  Button,
  Progress,
  Tag,
  Space,
  Modal,
  Form,
  Input,
  Select,
  message,
  Tooltip,
  Statistic,
  Row,
  Col,
  Badge
} from 'antd';
import {
  ReloadOutlined,
  PlusOutlined,
  UploadOutlined,
  EyeOutlined,
  StopOutlined
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';

const { TextArea } = Input;
const { Option } = Select;

interface UploadTask {
  task_id: string;
  video_path: string;
  title: string;
  description: string;
  tags: string;
  account_id?: number;
  priority: number;
  status: string;
  created_at: string;
  updated_at: string;
  progress: number;
  error_message?: string;
  retry_count: number;
  max_retries: number;
  celery_task_id?: string;
  bv_id?: string;
}

interface QueueStatus {
  queued_tasks: number;
  processing_tasks: number;
  max_concurrent: number;
  queue_details: Array<{
    task_id: string;
    title: string;
    priority: number;
    created_at: string;
  }>;
  processing_details: Array<{
    task_id: string;
    title: string;
    progress: number;
    account_id: number;
  }>;
}

interface BilibiliAccount {
  id: number;
  username: string;
  nickname?: string;
  status: string;
  is_vip: boolean;
  level: number;
  can_upload: boolean;
}

const UploadQueueManager: React.FC = () => {
  const [tasks, setTasks] = useState<UploadTask[]>([]);
  const [queueStatus, setQueueStatus] = useState<QueueStatus | null>(null);
  const [accounts, setAccounts] = useState<BilibiliAccount[]>([]);
  const [loading, setLoading] = useState(false);
  const [addTaskModalVisible, setAddTaskModalVisible] = useState(false);
  const [batchUploadModalVisible, setBatchUploadModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [batchForm] = Form.useForm();

  // Fetch queue status
  const fetchQueueStatus = async () => {
    try {
      const response = await fetch('/api/upload-queue/status');
      if (response.ok) {
        const data = await response.json();
        setQueueStatus(data);
      }
    } catch (error) {
      console.error('Fetch queue statusFailed:', error);
    }
  };

  // Fetch upload history
  const fetchUploadHistory = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/upload-queue/history?limit=50');
      if (response.ok) {
        const data = await response.json();
        setTasks(data.records || []);
      }
    } catch (error) {
      console.error('Fetch upload historyFailed:', error);
      message.error('Fetch upload historyFailed');
    } finally {
      setLoading(false);
    }
  };

  // Fetch Bilibili account list
  const fetchAccounts = async () => {
    try {
      const response = await fetch('/bilibili/accounts');
      if (response.ok) {
        const data = await response.json();
        setAccounts(data.accounts || []);
      }
    } catch (error) {
      console.error('Failed to fetch account list:', error);
    }
  };

  // Add single task
  const handleAddTask = async (values: any) => {
    try {
      const response = await fetch('/api/upload-queue/add-task', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
      });

      if (response.ok) {
        const data = await response.json();
        message.success(`Task added: ${data.task_id}`);
        setAddTaskModalVisible(false);
        form.resetFields();
        fetchQueueStatus();
        fetchUploadHistory();
      } else {
        const error = await response.json();
        message.error(`Failed to add task: ${error.detail}`);
      }
    } catch (error) {
      console.error('Failed to add task:', error);
      message.error('Failed to add task');
    }
  };

  // Batch add tasks
  const handleBatchUpload = async (values: any) => {
    try {
      const tasks = values.tasks.split('\n').filter((line: string) => line.trim()).map((line: string) => {
        const [video_path, title, description = '', tags = ''] = line.split('|').map((s: string) => s.trim());
        return {
          video_path,
          title,
          description,
          tags,
          priority: values.priority || 'normal'
        };
      });

      const response = await fetch('/api/upload-queue/add-batch-tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tasks }),
      });

      if (response.ok) {
        const data = await response.json();
        message.success(`Batch added ${data.count}  tasks`);
        setBatchUploadModalVisible(false);
        batchForm.resetFields();
        fetchQueueStatus();
        fetchUploadHistory();
      } else {
        const error = await response.json();
        message.error(`Batch add failed: ${error.detail}`);
      }
    } catch (error) {
      console.error('Batch add failed:', error);
      message.error('Batch add failed');
    }
  };

  // Cancel task
  const handleCancelTask = async (taskId: string) => {
    try {
      const response = await fetch(`/api/upload-queue/task/${taskId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        message.success('Task cancelled');
        fetchQueueStatus();
        fetchUploadHistory();
      } else {
        const error = await response.json();
        message.error(`Cancel taskFailed: ${error.detail}`);
      }
    } catch (error) {
      console.error('Cancel taskFailed:', error);
      message.error('Cancel taskFailed');
    }
  };

  // Retry task
  const handleRetryTask = async (taskId: string) => {
    try {
      const response = await fetch(`/api/upload-queue/retry/${taskId}`, {
        method: 'POST',
      });

      if (response.ok) {
        const data = await response.json();
        message.success(`Task re-added: ${data.new_task_id}`);
        fetchQueueStatus();
        fetchUploadHistory();
      } else {
        const error = await response.json();
        message.error(`Retry taskFailed: ${error.detail}`);
      }
    } catch (error) {
      console.error('Retry taskFailed:', error);
      message.error('Retry taskFailed');
    }
  };

  // Get status tags
  const getStatusTag = (status: string) => {
    const statusConfig: Record<string, { color: string; text: string }> = {
      pending: { color: 'default', text: 'Pending' },
      queued: { color: 'blue', text: 'Queued' },
      processing: { color: 'orange', text: 'Processing' },
      completed: { color: 'green', text: 'Completed' },
      failed: { color: 'red', text: 'Failed' },
      cancelled: { color: 'gray', text: 'Cancelled' }
    };
    
    const config = statusConfig[status] || { color: 'default', text: status };
    return <Tag color={config.color}>{config.text}</Tag>;
  };

  // Get priority tags
  const getPriorityTag = (priority: number) => {
    const priorityConfig: Record<number, { color: string; text: string }> = {
      1: { color: 'default', text: 'Low' },
      2: { color: 'blue', text: 'Normal' },
      3: { color: 'orange', text: 'High' },
      4: { color: 'red', text: 'Urgent' }
    };
    
    const config = priorityConfig[priority] || { color: 'default', text: 'Normal' };
    return <Tag color={config.color}>{config.text}</Tag>;
  };

  // Table columns
  const columns: ColumnsType<UploadTask> = [
    {
      title: 'Task ID',
      dataIndex: 'task_id',
      key: 'task_id',
      width: 120,
      render: (text: string) => (
        <Tooltip title={text}>
          <span>{text.substring(0, 8)}...</span>
        </Tooltip>
      ),
    },
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      ellipsis: true,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => getStatusTag(status),
    },
    {
      title: 'Priority',
      dataIndex: 'priority',
      key: 'priority',
      width: 80,
      render: (priority: number) => getPriorityTag(priority),
    },
    {
      title: 'Progress',
      dataIndex: 'progress',
      key: 'progress',
      width: 120,
      render: (progress: number, record: UploadTask) => (
        <Progress 
          percent={progress} 
          size="small" 
          status={record.status === 'failed' ? 'exception' : 'active'}
        />
      ),
    },
    {
      title: 'Account ID',
      dataIndex: 'account_id',
      key: 'account_id',
      width: 80,
    },
    {
      title: 'BV ID',
      dataIndex: 'bv_id',
      key: 'bv_id',
      width: 120,
      render: (bvId: string) => bvId ? (
        <a href={`https://www.bilibili.com/video/${bvId}`} target="_blank" rel="noopener noreferrer">
          {bvId}
        </a>
      ) : '-',
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 150,
      render: (text: string) => new Date(text).toLocaleString(),
    },
    {
      title: 'Actions',
      key: 'action',
      width: 150,
      render: (_, record: UploadTask) => (
        <Space size="small">
          {record.status === 'failed' && (
            <Button
              type="link"
              size="small"
              icon={<ReloadOutlined />}
              onClick={() => handleRetryTask(record.task_id)}
            >
              Retry
            </Button>
          )}
          {(record.status === 'queued' || record.status === 'processing') && (
            <Button
              type="link"
              size="small"
              danger
              icon={<StopOutlined />}
              onClick={() => handleCancelTask(record.task_id)}
            >
              Cancel
            </Button>
          )}
          {record.error_message && (
            <Tooltip title={record.error_message}>
              <Button type="link" size="small" icon={<EyeOutlined />}>
                Error
              </Button>
            </Tooltip>
          )}
        </Space>
      ),
    },
  ];

  useEffect(() => {
    fetchQueueStatus();
    fetchUploadHistory();
    fetchAccounts();

    // Periodically refresh status
    const interval = setInterval(() => {
      fetchQueueStatus();
      fetchUploadHistory();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="upload-queue-manager">
      {/* Queue stats */}
      {queueStatus && (
        <Row gutter={16} style={{ marginBottom: 16 }}>
          <Col span={6}>
            <Card>
              <Statistic
                title="Queuedtask"
                value={queueStatus.queued_tasks}
                prefix={<Badge status="processing" />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Processing tasks"
                value={queueStatus.processing_tasks}
                prefix={<Badge status="success" />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Max concurrency"
                value={queueStatus.max_concurrent}
                prefix={<Badge status="default" />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Available accounts"
                value={(accounts || []).filter(acc => acc.status === 'active' && acc.can_upload).length}
                prefix={<Badge status="success" />}
              />
            </Card>
          </Col>
        </Row>
      )}

      {/* Actions */}
      <Card style={{ marginBottom: 16 }}>
        <Space>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setAddTaskModalVisible(true)}
          >
            Add task
          </Button>
          <Button
            icon={<UploadOutlined />}
            onClick={() => setBatchUploadModalVisible(true)}
          >
            Batch upload
          </Button>
          <Button
            icon={<ReloadOutlined />}
            onClick={() => {
              fetchQueueStatus();
              fetchUploadHistory();
            }}
          >
            Refresh
          </Button>
        </Space>
      </Card>

      {/* Task list */}
      <Card title="Upload tasks">
        <Table
          columns={columns}
          dataSource={tasks}
          rowKey="task_id"
          loading={loading}
          pagination={{
            pageSize: 20,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `Total ${total}  records`,
          }}
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* Add taskmodal */}
      <Modal
        title="addUpload tasks"
        open={addTaskModalVisible}
        onCancel={() => setAddTaskModalVisible(false)}
        onOk={() => form.submit()}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleAddTask}
        >
          <Form.Item
            name="video_path"
            label="Video file path"
            rules={[{ required: true, message: 'Please enterVideo file path' }]}
          >
            <Input placeholder="/path/to/video.mp4" />
          </Form.Item>
          
          <Form.Item
            name="title"
            label="Video title"
            rules={[{ required: true, message: 'Please enterVideo title' }]}
          >
            <Input placeholder="Video title" maxLength={80} />
          </Form.Item>
          
          <Form.Item
            name="description"
            label="Video description"
          >
            <TextArea rows={4} placeholder="Video description" maxLength={2000} />
          </Form.Item>
          
          <Form.Item
            name="tags"
            label="Tags"
          >
            <Input placeholder="Tags1,Tags2,Tags3" />
          </Form.Item>
          
          <Form.Item
            name="account_id"
            label="Specify account"
          >
            <Select placeholder="Auto-select best account" allowClear>
              {(accounts || []).filter(acc => acc.status === 'active' && acc.can_upload).map(account => (
                <Option key={account.id} value={account.id}>
                  {account.nickname || account.username} 
                  {account.is_vip && <Tag color="gold">VIP</Tag>}
                  <Tag color="blue">Lv.{account.level}</Tag>
                </Option>
              ))}
            </Select>
          </Form.Item>
          
          <Form.Item
            name="priority"
            label="Priority"
            initialValue="normal"
          >
            <Select>
              <Option value="low">Low</Option>
              <Option value="normal">Normal</Option>
              <Option value="high">High</Option>
              <Option value="urgent">Urgent</Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>

      {/* Batch uploadmodal */}
      <Modal
        title="Batch uploadtask"
        open={batchUploadModalVisible}
        onCancel={() => setBatchUploadModalVisible(false)}
        onOk={() => batchForm.submit()}
        width={800}
      >
        <Form
          form={batchForm}
          layout="vertical"
          onFinish={handleBatchUpload}
        >
          <Form.Item
            name="tasks"
            label="Task list"
            rules={[{ required: true, message: 'Please enterTask list' }]}
            extra="EN tasks，EN：videoEN|Title|Description|Tags"
          >
            <TextArea
              rows={10}
              placeholder={`/path/to/video1.mp4|Video title1|Video description1|Tags1,Tags2
/path/to/video2.mp4|Video title2|Video description2|Tags3,Tags4`}
            />
          </Form.Item>
          
          <Form.Item
            name="priority"
            label="ENPriority"
            initialValue="normal"
          >
            <Select>
              <Option value="low">Low</Option>
              <Option value="normal">Normal</Option>
              <Option value="high">High</Option>
              <Option value="urgent">Urgent</Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default UploadQueueManager;