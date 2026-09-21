import React, { useState, useEffect } from 'react'
import {
  Card,
  Table,
  Button,
  Space,
  Tag,
  Progress,
  Modal,
  Form,
  Select,
  DatePicker,
  Input,
  message,
  Popconfirm,
  Row,
  Col,
  Statistic,
  Divider
} from 'antd'
import {
  ReloadOutlined,
  EyeOutlined,
  StopOutlined,
  ExclamationCircleOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  CloseCircleOutlined
} from '@ant-design/icons'
import { uploadApi, BILIBILI_PARTITIONS, UploadRecord } from '../services/uploadApi'
import dayjs from 'dayjs'

const { RangePicker } = DatePicker
const { Option } = Select
interface UploadTask {
  id: string
  project_id: string
  account_id: string
  clip_id: string
  title: string
  description: string
  tags: string
  partition_id: number
  bvid?: string
  status: string
  error_message?: string
  created_at: string
  updated_at: string
  progress?: number
  current_step?: string
}

const mapRecordToTask = (record: UploadRecord): UploadTask => ({
  id: String(record.id),
  project_id: record.project_id ? String(record.project_id) : '',
  account_id: String(record.account_id),
  clip_id: record.clip_id || '',
  title: record.title || 'ENtask',
  description: record.description || '',
  tags: record.tags || '[]',
  partition_id: record.partition_id,
  bvid: record.bv_id,
  status: record.status,
  error_message: record.error_message,
  created_at: record.created_at,
  updated_at: record.updated_at,
  progress: record.progress,
})

interface UploadTaskManagerProps {
  projectId?: string
}

const UploadTaskManager: React.FC<UploadTaskManagerProps> = ({ projectId }) => {
  const [tasks, setTasks] = useState<UploadTask[]>([])
  const [loading, setLoading] = useState(false)
  const [filteredTasks, setFilteredTasks] = useState<UploadTask[]>([])
  const [selectedTask, setSelectedTask] = useState<UploadTask | null>(null)
  const [detailModalVisible, setDetailModalVisible] = useState(false)
  const [filters, setFilters] = useState({
    status: '',
    accountId: '',
    dateRange: null as any,
    keyword: ''
  })

  // fetchsubmissionTask list
  const fetchTasks = async () => {
    try {
      setLoading(true)
      const records = await uploadApi.getUploadRecords(projectId)
      const safeRecords = Array.isArray(records) ? records.map(mapRecordToTask) : []
      setTasks(safeRecords)
      setFilteredTasks(safeRecords)
    } catch (error: any) {
      message.error('fetchsubmissiontaskFailed: ' + (error.message || 'Unknown error'))
      setTasks([])
      setFilteredTasks([])
    } finally {
      setLoading(false)
    }
  }

  // Retry failed tasks
  const retryTask = async (_taskId: string) => {
    message.info('Bsite upload is in progressIn development — coming soon！', 3);
    return;
    
    // Legacy code disabled
    try {
      // ENRetryAPI
      message.success('taskRetryEN')
      fetchTasks() // Refreshlist
    } catch (error: any) {
      message.error('Retry taskFailed: ' + (error.message || 'Unknown error'))
    }
  }

  // CancelIn progress tasks
  const cancelTask = async (_taskId: string) => {
    message.info('Bsite upload is in progressIn development — coming soon！', 3);
    return;
    
    // Legacy code disabled
    try {
      // ENCancelAPI
      message.success('Task cancelled')
      fetchTasks() // Refreshlist
    } catch (error: any) {
      message.error('Cancel taskFailed: ' + (error.message || 'Unknown error'))
    }
  }

  // View tasksDetails
  const showTaskDetail = (task: UploadTask) => {
    setSelectedTask(task)
    setDetailModalVisible(true)
  }

  // EN
  const applyFilters = () => {
    const safeTasks = Array.isArray(tasks) ? tasks : []
    let filtered = safeTasks

    if (filters.status) {
      filtered = filtered.filter(task => task.status === filters.status)
    }

    if (filters.accountId) {
      filtered = filtered.filter(task => task.account_id === filters.accountId)
    }

    if (filters.keyword) {
      filtered = filtered.filter(task => 
        task.title.toLowerCase().includes(filters.keyword.toLowerCase()) ||
        task.description.toLowerCase().includes(filters.keyword.toLowerCase())
      )
    }

    if (filters.dateRange && filters.dateRange.length === 2) {
      const startDate = filters.dateRange[0].startOf('day')
      const endDate = filters.dateRange[1].endOf('day')
      filtered = filtered.filter(task => {
        const taskDate = dayjs(task.created_at)
        return taskDate.isAfter(startDate) && taskDate.isBefore(endDate)
      })
    }

    setFilteredTasks(filtered)
  }

  // EN
  const resetFilters = () => {
    setFilters({
      status: '',
      accountId: '',
      dateRange: null,
      keyword: ''
    })
    setFilteredTasks(Array.isArray(tasks) ? tasks : [])
  }

  // Get status tagsEN
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'orange'
      case 'processing':
        return 'blue'
      case 'success':
        return 'green'
      case 'failed':
        return 'red'
      default:
        return 'default'
    }
  }

  // fetchStatusIcon
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <ClockCircleOutlined />
      case 'processing':
        return <ExclamationCircleOutlined />
      case 'success':
        return <CheckCircleOutlined />
      case 'failed':
        return <CloseCircleOutlined />
      default:
        return null
    }
  }

  // fetchStatusText
  const getStatusText = (status: string) => {
    switch (status) {
      case 'pending':
        return 'pending'
      case 'processing':
        return 'Processing'
      case 'success':
        return 'Succeeded'
      case 'failed':
        return 'Failed'
      default:
        return status
    }
  }

  // EN
  const getStatistics = () => {
    const safeTasks = Array.isArray(tasks) ? tasks : []
    const total = safeTasks.length
    const pending = safeTasks.filter(t => t.status === 'pending').length
    const processing = safeTasks.filter(t => t.status === 'processing').length
    const success = safeTasks.filter(t => t.status === 'success').length
    const failed = safeTasks.filter(t => t.status === 'failed').length

    return { total, pending, processing, success, failed }
  }

  useEffect(() => {
    fetchTasks()
  }, [projectId])

  useEffect(() => {
    applyFilters()
  }, [filters, tasks])

  const columns = [
    {
      title: 'taskinfo',
      key: 'task_info',
      render: (record: UploadTask) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>{record.title}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            projectID: {record.project_id.slice(0, 8)}...
          </div>
        </div>
      )
    },
    {
      title: 'ClipEN',
      key: 'clip_count',
      render: (record: UploadTask) => {
        const clipCount = record.clip_id.split(',').filter(id => id.trim()).length
        return <Tag>{clipCount} ENClip</Tag>
      }
    },
    {
      title: 'Partition',
      key: 'partition',
      render: (record: UploadTask) => {
        const partition = BILIBILI_PARTITIONS.find(p => p.id === record.partition_id)
        return partition ? partition.name : `Partition${record.partition_id}`
      }
    },
    {
      title: 'Status',
      key: 'status',
      render: (record: UploadTask) => (
        <Tag color={getStatusColor(record.status)} icon={getStatusIcon(record.status)}>
          {getStatusText(record.status)}
        </Tag>
      )
    },
    {
      title: 'Progress',
      key: 'progress',
      render: (record: UploadTask) => {
        if (record.status === 'processing' && record.progress !== undefined) {
          return <Progress percent={record.progress} size="small" />
        } else if (record.status === 'success') {
          return <Progress percent={100} size="small" status="success" />
        } else if (record.status === 'failed') {
          return <Progress percent={0} size="small" status="exception" />
        }
        return <Progress percent={0} size="small" />
      }
    },
    {
      title: 'Created',
      key: 'created_at',
      render: (record: UploadTask) => dayjs(record.created_at).format('YYYY-MM-DD HH:mm')
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (record: UploadTask) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => showTaskDetail(record)}
          >
            Details
          </Button>
          
          {record.status === 'failed' && (
            <Button
              type="link"
              size="small"
              icon={<ReloadOutlined />}
              onClick={() => retryTask(record.id)}
            >
              Retry
            </Button>
          )}
          
          {record.status === 'processing' && (
            <Popconfirm
              title="DeleteENCancelEN tasksEN？"
              onConfirm={() => cancelTask(record.id)}
              okText="Delete"
              cancelText="Cancel"
            >
              <Button
                type="link"
                size="small"
                danger
                icon={<StopOutlined />}
              >
                Cancel
              </Button>
            </Popconfirm>
          )}
        </Space>
      )
    }
  ]

  const stats = getStatistics()

  return (
    <div style={{ padding: '24px' }}>
      {/* Stats card */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={4}>
          <Card>
            <Statistic title="Total tasks" value={stats.total} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="pending" value={stats.pending} valueStyle={{ color: '#faad14' }} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="Processing" value={stats.processing} valueStyle={{ color: '#1890ff' }} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="Succeeded" value={stats.success} valueStyle={{ color: '#52c41a' }} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="Failed" value={stats.failed} valueStyle={{ color: '#ff4d4f' }} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic 
              title="SucceededEN" 
              value={stats.total > 0 ? Math.round((stats.success / stats.total) * 100) : 0}
              suffix="%" 
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      {/* EN */}
      <Card style={{ marginBottom: '16px' }}>
        <Row gutter={16} align="middle">
          <Col span={6}>
            <Form.Item label="Status" style={{ marginBottom: 0 }}>
              <Select
                placeholder="ENStatus"
                value={filters.status}
                onChange={(value) => setFilters({ ...filters, status: value })}
                allowClear
              >
                <Option value="pending">pending</Option>
                <Option value="processing">Processing</Option>
                <Option value="success">Succeeded</Option>
                <Option value="failed">Failed</Option>
              </Select>
            </Form.Item>
          </Col>
          <Col span={6}>
            <Form.Item label="EN" style={{ marginBottom: 0 }}>
              <RangePicker
                value={filters.dateRange}
                onChange={(dates) => setFilters({ ...filters, dateRange: dates })}
                placeholder={['EN', 'EN']}
              />
            </Form.Item>
          </Col>
          <Col span={6}>
            <Form.Item label="EN" style={{ marginBottom: 0 }}>
              <Input
                placeholder="SearchTitleENDescription"
                value={filters.keyword}
                onChange={(e) => setFilters({ ...filters, keyword: e.target.value })}
              />
            </Form.Item>
          </Col>
          <Col span={6}>
            <Space>
              <Button type="primary" onClick={applyFilters}>
                EN
              </Button>
              <Button onClick={resetFilters}>
                EN
              </Button>
              <Button icon={<ReloadOutlined />} onClick={fetchTasks}>
                Refresh
              </Button>
            </Space>
          </Col>
        </Row>
      </Card>

      {/* Task list */}
      <Card title={`submissionTask list (${filteredTasks.length})`}>
        <Table
          columns={columns}
          dataSource={filteredTasks}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `EN ${range[0]}-${range[1]} EN，Total ${total} EN`
          }}
        />
      </Card>

      {/* taskDetailsdialog */}
      <Modal
        title="taskDetails"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            Close
          </Button>
        ]}
        width={800}
      >
        {selectedTask && (
          <div>
            <Row gutter={16}>
              <Col span={12}>
                <div><strong>Task ID:</strong> {selectedTask.id}</div>
                <div><strong>projectID:</strong> {selectedTask.project_id}</div>
                <div><strong>Title:</strong> {selectedTask.title}</div>
                <div><strong>Description:</strong> {selectedTask.description}</div>
              </Col>
              <Col span={12}>
                <div><strong>Status:</strong> 
                  <Tag color={getStatusColor(selectedTask.status)} style={{ marginLeft: 8 }}>
                    {getStatusText(selectedTask.status)}
                  </Tag>
                </div>
                <div><strong>Partition:</strong> 
                  {(() => {
                    const partition = BILIBILI_PARTITIONS.find(p => p.id === selectedTask.partition_id)
                    return partition ? partition.name : `Partition${selectedTask.partition_id}`
                  })()}
                </div>
                <div><strong>Created:</strong> {dayjs(selectedTask.created_at).format('YYYY-MM-DD HH:mm:ss')}</div>
                <div><strong>Updated:</strong> {dayjs(selectedTask.updated_at).format('YYYY-MM-DD HH:mm:ss')}</div>
              </Col>
            </Row>
            
            <Divider />
            
            <div>
              <strong>Clipinfo:</strong>
              <div style={{ marginTop: 8 }}>
                {selectedTask.clip_id.split(',').filter(id => id.trim()).map((clipId, index) => (
                  <Tag key={index} style={{ marginBottom: 4 }}>{clipId.trim()}</Tag>
                ))}
              </div>
            </div>
            
            {selectedTask.tags && (
              <>
                <Divider />
                <div>
                  <strong>Tags:</strong>
                  <div style={{ marginTop: 8 }}>
                    {JSON.parse(selectedTask.tags).map((tag: string, index: number) => (
                      <Tag key={index} color="blue">{tag}</Tag>
                    ))}
                  </div>
                </div>
              </>
            )}
            
            {selectedTask.bvid && (
              <>
                <Divider />
                <div>
                  <strong>BV ID:</strong> {selectedTask.bvid}
                </div>
              </>
            )}
            
            {selectedTask.error_message && (
              <>
                <Divider />
                <div>
                  <strong>Errorinfo:</strong>
                  <div style={{ marginTop: 8, color: '#ff4d4f', backgroundColor: '#fff2f0', padding: 8, borderRadius: 4 }}>
                    {selectedTask.error_message}
                  </div>
                </div>
              </>
            )}
          </div>
        )}
      </Modal>
    </div>
  )
}

export default UploadTaskManager



