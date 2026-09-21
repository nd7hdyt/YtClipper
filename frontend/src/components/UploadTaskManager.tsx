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
  title: record.title || 'translatedtask',
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

  // fetchtranslatedtasklist
  const fetchTasks = async () => {
    try {
      setLoading(true)
      const records = await uploadApi.getUploadRecords(projectId)
      const safeRecords = Array.isArray(records) ? records.map(mapRecordToTask) : []
      setTasks(safeRecords)
      setFilteredTasks(safeRecords)
    } catch (error: any) {
      message.error('fetchtranslatedtaskfailed: ' + (error.message || 'translatederror'))
      setTasks([])
      setFilteredTasks([])
    } finally {
      setLoading(false)
    }
  }

  // translatedfailed'stask
  const retryTask = async (_taskId: string) => {
    message.info('BsiteUploadfeaturetranslatedinIn Development，translated！', 3);
    return;
    
    // translateduse
    try {
      // thistranslatedcalltranslatedAPI
      message.success('tasktranslatedstart')
      fetchTasks() // translatedlist
    } catch (error: any) {
      message.error('translatedtaskfailed: ' + (error.message || 'translatederror'))
    }
  }

  // canceltranslated'stask
  const cancelTask = async (_taskId: string) => {
    message.info('BsiteUploadfeaturetranslatedinIn Development，translated！', 3);
    return;
    
    // translateduse
    try {
      // thistranslatedcallcancelAPI
      message.success('tasktranslatedcancel')
      fetchTasks() // translatedlist
    } catch (error: any) {
      message.error('canceltaskfailed: ' + (error.message || 'translatederror'))
    }
  }

  // translatedtasktranslated
  const showTaskDetail = (task: UploadTask) => {
    setSelectedTask(task)
    setDetailModalVisible(true)
  }

  // translatedusetranslatedSelecttranslated
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

  // translatedSelecttranslated
  const resetFilters = () => {
    setFilters({
      status: '',
      accountId: '',
      dateRange: null,
      keyword: ''
    })
    setFilteredTasks(Array.isArray(tasks) ? tasks : [])
  }

  // fetchstatustranslated
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

  // fetchstatustranslated
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

  // fetchstatustranslated
  const getStatusText = (status: string) => {
    switch (status) {
      case 'pending':
        return 'translatedprocess'
      case 'processing':
        return 'processing'
      case 'success':
        return 'succeeded'
      case 'failed':
        return 'failed'
      default:
        return status
    }
  }

  // translated
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
      title: 'cliptranslated',
      key: 'clip_count',
      render: (record: UploadTask) => {
        const clipCount = record.clip_id.split(',').filter(id => id.trim()).length
        return <Tag>{clipCount}  clip</Tag>
      }
    },
    {
      title: 'translated',
      key: 'partition',
      render: (record: UploadTask) => {
        const partition = BILIBILI_PARTITIONS.find(p => p.id === record.partition_id)
        return partition ? partition.name : `translated${record.partition_id}`
      }
    },
    {
      title: 'status',
      key: 'status',
      render: (record: UploadTask) => (
        <Tag color={getStatusColor(record.status)} icon={getStatusIcon(record.status)}>
          {getStatusText(record.status)}
        </Tag>
      )
    },
    {
      title: 'progress',
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
      title: 'createtranslated',
      key: 'created_at',
      render: (record: UploadTask) => dayjs(record.created_at).format('YYYY-MM-DD HH:mm')
    },
    {
      title: 'translated',
      key: 'actions',
      render: (record: UploadTask) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => showTaskDetail(record)}
          >
            translated
          </Button>
          
          {record.status === 'failed' && (
            <Button
              type="link"
              size="small"
              icon={<ReloadOutlined />}
              onClick={() => retryTask(record.id)}
            >
              translated
            </Button>
          )}
          
          {record.status === 'processing' && (
            <Popconfirm
              title="translatedcancelthis tasktranslated？"
              onConfirm={() => cancelTask(record.id)}
              okText="translated"
              cancelText="cancel"
            >
              <Button
                type="link"
                size="small"
                danger
                icon={<StopOutlined />}
              >
                cancel
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
      {/* translated */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={4}>
          <Card>
            <Statistic title="translatedtasktranslated" value={stats.total} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="translatedprocess" value={stats.pending} valueStyle={{ color: '#faad14' }} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="processing" value={stats.processing} valueStyle={{ color: '#1890ff' }} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="succeeded" value={stats.success} valueStyle={{ color: '#52c41a' }} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="failed" value={stats.failed} valueStyle={{ color: '#ff4d4f' }} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic 
              title="succeededtranslated" 
              value={stats.total > 0 ? Math.round((stats.success / stats.total) * 100) : 0}
              suffix="%" 
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      {/* translatedSelecttranslated */}
      <Card style={{ marginBottom: '16px' }}>
        <Row gutter={16} align="middle">
          <Col span={6}>
            <Form.Item label="status" style={{ marginBottom: 0 }}>
              <Select
                placeholder="Selectselectstatus"
                value={filters.status}
                onChange={(value) => setFilters({ ...filters, status: value })}
                allowClear
              >
                <Option value="pending">translatedprocess</Option>
                <Option value="processing">processing</Option>
                <Option value="success">succeeded</Option>
                <Option value="failed">failed</Option>
              </Select>
            </Form.Item>
          </Col>
          <Col span={6}>
            <Form.Item label="translated" style={{ marginBottom: 0 }}>
              <RangePicker
                value={filters.dateRange}
                onChange={(dates) => setFilters({ ...filters, dateRange: dates })}
                placeholder={['translated', 'translated']}
              />
            </Form.Item>
          </Col>
          <Col span={6}>
            <Form.Item label="translated" style={{ marginBottom: 0 }}>
              <Input
                placeholder="translatedortranslated"
                value={filters.keyword}
                onChange={(e) => setFilters({ ...filters, keyword: e.target.value })}
              />
            </Form.Item>
          </Col>
          <Col span={6}>
            <Space>
              <Button type="primary" onClick={applyFilters}>
                translatedSelect
              </Button>
              <Button onClick={resetFilters}>
                translated
              </Button>
              <Button icon={<ReloadOutlined />} onClick={fetchTasks}>
                translated
              </Button>
            </Space>
          </Col>
        </Row>
      </Card>

      {/* tasklist */}
      <Card title={`translatedtasklist (${filteredTasks.length})`}>
        <Table
          columns={columns}
          dataSource={filteredTasks}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `No. ${range[0]}-${range[1]} translated，translated ${total} translated`
          }}
        />
      </Card>

      {/* tasktranslated */}
      <Modal
        title="tasktranslated"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            translated
          </Button>
        ]}
        width={800}
      >
        {selectedTask && (
          <div>
            <Row gutter={16}>
              <Col span={12}>
                <div><strong>taskID:</strong> {selectedTask.id}</div>
                <div><strong>projectID:</strong> {selectedTask.project_id}</div>
                <div><strong>translated:</strong> {selectedTask.title}</div>
                <div><strong>translated:</strong> {selectedTask.description}</div>
              </Col>
              <Col span={12}>
                <div><strong>status:</strong> 
                  <Tag color={getStatusColor(selectedTask.status)} style={{ marginLeft: 8 }}>
                    {getStatusText(selectedTask.status)}
                  </Tag>
                </div>
                <div><strong>translated:</strong> 
                  {(() => {
                    const partition = BILIBILI_PARTITIONS.find(p => p.id === selectedTask.partition_id)
                    return partition ? partition.name : `translated${selectedTask.partition_id}`
                  })()}
                </div>
                <div><strong>createtranslated:</strong> {dayjs(selectedTask.created_at).format('YYYY-MM-DD HH:mm:ss')}</div>
                <div><strong>updatetranslated:</strong> {dayjs(selectedTask.updated_at).format('YYYY-MM-DD HH:mm:ss')}</div>
              </Col>
            </Row>
            
            <Divider />
            
            <div>
              <strong>clipinfo:</strong>
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
                  <strong>translated:</strong>
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
                  <strong>BVtranslated:</strong> {selectedTask.bvid}
                </div>
              </>
            )}
            
            {selectedTask.error_message && (
              <>
                <Divider />
                <div>
                  <strong>errorinfo:</strong>
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



