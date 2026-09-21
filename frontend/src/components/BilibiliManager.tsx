import React, { useState, useEffect } from 'react'
import { Button, Modal, Form, Input, Table, Tag, Space, message, Popconfirm, Tabs, Alert, Typography, Select, Row, Col, Tooltip, Progress, Descriptions, Statistic, Card } from 'antd'
import { PlusOutlined, DeleteOutlined, UserOutlined, CheckCircleOutlined, CloseCircleOutlined, UploadOutlined, QuestionCircleOutlined, ReloadOutlined, EyeOutlined, RedoOutlined, StopOutlined, ExclamationCircleOutlined, ClockCircleOutlined, PlayCircleOutlined } from '@ant-design/icons'
import { uploadApi, BilibiliAccount, BILIBILI_PARTITIONS, UploadRecord } from '../services/uploadApi'
import './BilibiliManager.css'

const { TextArea } = Input
const { Text } = Typography
const { Option } = Select
const { TabPane } = Tabs

interface BilibiliManagerProps {
  visible: boolean
  onClose: () => void
  projectId?: string
  clipIds?: string[]
  clipTitles?: string[]
  onUploadSuccess?: () => void
}

const BilibiliManager: React.FC<BilibiliManagerProps> = ({
  visible,
  onClose,
  projectId,
  clipIds = [],
  clipTitles = [],
  onUploadSuccess
}) => {
  const [activeTab, setActiveTab] = useState('upload')
  const [accounts, setAccounts] = useState<BilibiliAccount[]>([])
  const [loading, setLoading] = useState(false)
  const [showAddAccount, setShowAddAccount] = useState(false)
  const [cookieForm] = Form.useForm()
  const [uploadForm] = Form.useForm()
  
  // Upload-status state
  const [uploadRecords, setUploadRecords] = useState<UploadRecord[]>([])
  const [recordsLoading, setRecordsLoading] = useState(false)
  const [selectedRecord, setSelectedRecord] = useState<UploadRecord | null>(null)
  const [detailModalVisible, setDetailModalVisible] = useState(false)

  // Fetch account list
  const fetchAccounts = async () => {
    try {
      setLoading(true)
      const data = await uploadApi.getAccounts()
      setAccounts(data)
    } catch (error: any) {
      message.error('Failed to load accounts: ' + (error.message || 'Unknown error'))
    } finally {
      setLoading(false)
    }
  }

  // Fetch upload records
  const fetchUploadRecords = async () => {
    try {
      setRecordsLoading(true)
      const data = await uploadApi.getUploadRecords()
      setUploadRecords(data)
    } catch (error: any) {
      message.error('Failed to load upload records: ' + (error.message || 'Unknown error'))
    } finally {
      setRecordsLoading(false)
    }
  }

  // Retry an upload
  const handleRetry = async (recordId: string | number) => {
    try {
      await uploadApi.retryUpload(recordId)
      message.success('Retry submitted')
      fetchUploadRecords()
    } catch (error: any) {
      message.error('Retry failed: ' + (error.message || 'Unknown error'))
    }
  }

  // Cancel an upload
  const handleCancel = async (recordId: string | number) => {
    try {
      await uploadApi.cancelUpload(recordId)
      message.success('Task cancelled')
      fetchUploadRecords()
    } catch (error: any) {
      message.error('Cancel failed: ' + (error.message || 'Unknown error'))
    }
  }

  // Delete an upload
  const handleDelete = async (recordId: string | number) => {
    try {
      await uploadApi.deleteUpload(recordId)
      message.success('Task deleted')
      fetchUploadRecords()
    } catch (error: any) {
      message.error('Delete failed: ' + (error.message || 'Unknown error'))
    }
  }

  // View details
  const handleViewDetail = (record: UploadRecord) => {
    setSelectedRecord(record)
    setDetailModalVisible(true)
  }

  useEffect(() => {
    if (visible) {
      fetchAccounts()
      fetchUploadRecords()
      // Default to the upload tab when clips are selected
      if (clipIds.length > 0) {
        setActiveTab('upload')
      } else {
        setActiveTab('accounts')
      }
    }
  }, [visible, clipIds])

  // Cookie-import login
  const handleCookieLogin = async (values: any) => {
    try {
      setLoading(true)
      
      // Parse the cookie string
      const cookieStr = values.cookies.trim()
      const cookies: Record<string, string> = {}
      
      cookieStr.split(';').forEach((cookie: string) => {
        const trimmedCookie = cookie.trim()
        const equalIndex = trimmedCookie.indexOf('=')
        if (equalIndex > 0) {
          const key = trimmedCookie.substring(0, equalIndex).trim()
          const value = trimmedCookie.substring(equalIndex + 1).trim()
          if (key && value) {
            cookies[key] = value
          }
        }
      })
      
      if (Object.keys(cookies).length === 0) {
        message.error('Invalid cookie format, please check your input')
        return
      }
      
      await uploadApi.cookieLogin(cookies, values.nickname)
      message.success('Account added!')
      setShowAddAccount(false)
      cookieForm.resetFields()
      fetchAccounts()
    } catch (error: any) {
      message.error('Failed to add account: ' + (error.message || 'Unknown error'))
    } finally {
      setLoading(false)
    }
  }

  // Delete an account
  const handleDeleteAccount = async (accountId: string) => {
    try {
      await uploadApi.deleteAccount(accountId)
      message.success('Account deleted')
      fetchAccounts()
    } catch (error: any) {
      message.error('Failed to delete account: ' + (error.message || 'Unknown error'))
    }
  }

  // Submit an upload
  const handleUpload = async (values: any) => {
    // In-development notice
    message.info('Bilibili upload is in development — coming soon!', 3)
    return
    
    // Legacy code disabled
    if (!projectId || clipIds.length === 0) {
      message.error('No clips selected for upload')
      return
    }

    try {
      setLoading(true)
      
      const uploadData = {
        account_id: values.account_id,
        clip_ids: clipIds,
        title: values.title,
        description: values.description || '',
        tags: values.tags ? values.tags.split(',').map((tag: string) => tag.trim()) : [],
        partition_id: values.partition_id
      }

      // Call the upload API
      const response = await fetch(`/api/v1/upload/projects/${projectId}/upload`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(uploadData)
      })

      if (response.ok) {
        message.success('Upload task created, processing in the background…')
        onUploadSuccess?.()
        onClose()
      } else {
        const error = await response.json()
        message.error('Upload failed: ' + (error.detail || 'Unknown error'))
      }
    } catch (error: any) {
      message.error('Upload failed: ' + (error.message || 'Unknown error'))
    } finally {
      setLoading(false)
    }
  }

  // Status tag
  const getStatusTag = (status: string) => {
    const statusConfig = {
      pending: { color: 'default', icon: <ClockCircleOutlined />, text: 'Pending' },
      processing: { color: 'processing', icon: <PlayCircleOutlined />, text: 'Processing' },
      success: { color: 'success', icon: <CheckCircleOutlined />, text: 'Succeeded' },
      completed: { color: 'success', icon: <CheckCircleOutlined />, text: 'Completed' },
      failed: { color: 'error', icon: <ExclamationCircleOutlined />, text: 'Failed' },
      cancelled: { color: 'default', icon: <StopOutlined />, text: 'Cancelled' }
    }
    
    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.pending
    return (
      <Tag color={config.color} icon={config.icon}>
        {config.text}
      </Tag>
    )
  }

  // Partition name
  const getPartitionName = (partitionId: number) => {
    const partition = BILIBILI_PARTITIONS.find(p => p.id === partitionId)
    return partition ? partition.name : `Partition ${partitionId}`
  }

  // Format file size
  const formatFileSize = (bytes?: number) => {
    if (!bytes) return '-'
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
  }

  // Format duration
  const formatDuration = (seconds?: number) => {
    if (!seconds) return '-'
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60
    
    if (hours > 0) {
      return `${hours}h ${minutes}m`
    } else if (minutes > 0) {
      return `${minutes}m ${secs}s`
    } else {
      return `${secs}s`
    }
  }

  // Stats
  const getStatistics = () => {
    const safeRecords = Array.isArray(uploadRecords) ? uploadRecords : []
    const total = safeRecords.length
    const success = safeRecords.filter(r => r.status === 'success' || r.status === 'completed').length
    const failed = safeRecords.filter(r => r.status === 'failed').length
    const processing = safeRecords.filter(r => r.status === 'processing').length
    const pending = safeRecords.filter(r => r.status === 'pending').length
    
    return { total, success, failed, processing, pending }
  }

  // Cookie guide content
  const cookieGuideContent = (
    <div style={{ maxWidth: 300 }}>
      <div style={{ marginBottom: 8, fontWeight: 'bold' }}>How to get your cookie:</div>
      <ol style={{ margin: 0, paddingLeft: 16 }}>
        <li>Open the Bilibili site and sign in</li>
        <li>Press F12 to open devtools</li>
        <li>Click the Network tab</li>
        <li>Refresh the page</li>
        <li>Pick any request and inspect it</li>
        <li>Find the Cookie field in Request Headers</li>
        <li>Copy the cookie value (without the "Cookie: " prefix)</li>
      </ol>
    </div>
  )

  // Account table columns
  const accountColumns = [
    {
      title: 'Nickname',
      dataIndex: 'nickname',
      key: 'nickname',
      render: (nickname: string, record: BilibiliAccount) => (
        <Space>
          <UserOutlined />
          <span>{nickname || record.username}</span>
        </Space>
      ),
    },
    {
      title: 'Username',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'red'} icon={status === 'active' ? <CheckCircleOutlined /> : <CloseCircleOutlined />}>
          {status === 'active' ? 'OK' : 'Error'}
        </Tag>
      ),
    },
    {
      title: 'Actions',
      key: 'action',
      render: (_: any, record: BilibiliAccount) => (
        <Popconfirm
          title="Delete this account?"
          description="This cannot be undone."
          onConfirm={() => handleDeleteAccount(record.id)}
          okText="Delete"
          cancelText="Cancel"
        >
          <Button type="text" danger icon={<DeleteOutlined />} size="small">
            Delete
          </Button>
        </Popconfirm>
      ),
    },
  ]

  // Upload-status table columns
  const uploadStatusColumns = [
    {
      title: 'Task ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
      render: (id: string | number) => <Text code>{id}</Text>
    },
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      ellipsis: true,
      render: (title: string) => (
        <Tooltip title={title}>
          <Text>{title}</Text>
        </Tooltip>
      )
    },
    {
      title: 'Upload account',
      dataIndex: 'account_nickname',
      key: 'account_nickname',
      width: 120,
      render: (nickname: string, record: UploadRecord) => (
        <div>
          <div>{nickname || record.account_username}</div>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            {record.account_username}
          </Text>
        </div>
      )
    },
    {
      title: 'Partition',
      dataIndex: 'partition_id',
      key: 'partition_id',
      width: 100,
      render: (partitionId: number) => (
        <Tag>{getPartitionName(partitionId)}</Tag>
      )
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => getStatusTag(status)
    },
    {
      title: 'Progress',
      dataIndex: 'progress',
      key: 'progress',
      width: 120,
      render: (progress: number, record: UploadRecord) => {
        if (record.status === 'success' || record.status === 'completed') {
          return <Progress percent={100} size="small" status="success" />
        } else if (record.status === 'failed') {
          return <Progress percent={progress} size="small" status="exception" />
        } else if (record.status === 'processing') {
          return <Progress percent={progress} size="small" status="active" />
        } else {
          return <Progress percent={progress} size="small" />
        }
      }
    },
    {
      title: 'File size',
      dataIndex: 'file_size',
      key: 'file_size',
      width: 100,
      render: (fileSize: number) => <span>{formatFileSize(fileSize)}</span>
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 150,
      render: (date: string) => <span>{new Date(date).toLocaleString()}</span>
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 200,
      render: (_: any, record: UploadRecord) => (
        <Space size="small">
          <Button 
            type="link" 
            icon={<EyeOutlined />} 
            onClick={() => handleViewDetail(record)}
            size="small"
          >
            Details
          </Button>
          {record.status === 'failed' && (
            <Popconfirm
              title="Retry this upload task?"
              onConfirm={() => handleRetry(record.id)}
              okText="Retry"
              cancelText="Cancel"
            >
              <Button 
                type="link" 
                icon={<RedoOutlined />} 
                size="small"
              >
                Retry
              </Button>
            </Popconfirm>
          )}
          {(record.status === 'pending' || record.status === 'processing') && (
            <Popconfirm
              title="Cancel this upload task?"
              onConfirm={() => handleCancel(record.id)}
              okText="Confirm"
              cancelText="Cancel"
            >
              <Button 
                type="link" 
                icon={<StopOutlined />} 
                danger
                size="small"
              >
                Cancel
              </Button>
            </Popconfirm>
          )}
          {(record.status === 'success' || record.status === 'completed' || record.status === 'failed' || record.status === 'cancelled') && (
            <Popconfirm
              title="Delete this upload task? This cannot be undone."
              onConfirm={() => handleDelete(record.id)}
              okText="Delete"
              cancelText="Cancel"
            >
              <Button 
                type="link" 
                icon={<DeleteOutlined />} 
                danger
                size="small"
              >
                Delete
              </Button>
            </Popconfirm>
          )}
        </Space>
      )
    }
  ]

  return (
    <Modal
      open={visible}
      onCancel={onClose}
      footer={null}
      width={800}
      destroyOnClose
      className="bilibili-manager-modal"
    >
      {/* Custom header */}
      <div className="bilibili-manager-header">
        <div className="bilibili-manager-header-icon">
          <UploadOutlined />
        </div>
        <div className="bilibili-manager-header-content">
          <h2 className="bilibili-manager-header-title">Bilibili</h2>
          <p className="bilibili-manager-header-subtitle">
            {clipIds.length > 0 
              ? `Ready to upload ${clipIds.length} clips to Bilibili` 
              : 'Manage your Bilibili accounts and upload settings'
            }
          </p>
        </div>
      </div>

      <div className="bilibili-manager-tabs">
        <Tabs activeKey={activeTab} onChange={setActiveTab}>
        {/* Upload tab */}
        {clipIds.length > 0 && (
          <TabPane 
            tab={
              <span>
                <UploadOutlined />
                Upload
              </span>
            } 
            key="upload"
          >
            <div className="bilibili-manager-content">
              <Alert
                message="Upload info"
                description={`Ready to upload ${clipIds.length} clips to Bilibili`}
                type="info"
                showIcon
                style={{ marginBottom: 16 }}
              />

              <Form
              form={uploadForm}
              onFinish={handleUpload}
              layout="vertical"
              initialValues={{
                title: clipTitles.length === 1 ? clipTitles[0] : `${clipTitles[0]} + ${clipIds.length - 1} more`,
                partition_id: 4 // Default: gaming partition
              }}
            >
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    label="Account"
                    name="account_id"
                    rules={[{ required: true, message: 'Please select a Bilibili account' }]}
                  >
                    <Select 
                      placeholder="Select a Bilibili account"
                      notFoundContent={
                        <div style={{ textAlign: 'center', padding: '20px' }}>
                          <p>No accounts available</p>
                          <Button 
                            type="link" 
                            icon={<PlusOutlined />}
                            onClick={() => setShowAddAccount(true)}
                          >
                            Add account
                          </Button>
                        </div>
                      }
                    >
                      {(accounts || []).filter(acc => acc.status === 'active').map(account => (
                        <Option key={account.id} value={account.id}>
                          {account.nickname || account.username}
                        </Option>
                      ))}
                    </Select>
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    label="Partition"
                    name="partition_id"
                    rules={[{ required: true, message: 'Please select a partition' }]}
                  >
                    <Select placeholder="Select a partition" showSearch>
                      {BILIBILI_PARTITIONS.map(partition => (
                        <Option key={partition.id} value={partition.id}>
                          {partition.name}
                        </Option>
                      ))}
                    </Select>
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item
                label="Title"
                name="title"
                rules={[{ required: true, message: 'Please enter a video title' }]}
              >
                <Input placeholder="Enter a video title" maxLength={80} showCount />
              </Form.Item>

              <Form.Item
                label="Description"
                name="description"
              >
                <TextArea
                  placeholder="Enter a description (optional)"
                  rows={3}
                  maxLength={2000}
                  showCount
                />
              </Form.Item>

              <Form.Item
                label="Tags"
                name="tags"
              >
                <Input placeholder="Tags, comma-separated (optional)" />
              </Form.Item>

              <Form.Item>
                <Space>
                  <Button 
                    type="primary" 
                    onClick={() => message.info('In development — coming soon', 3)}
                    icon={<UploadOutlined />}
                  >
                    Start upload
                  </Button>
                  <Button onClick={onClose}>
                    Cancel
                  </Button>
                </Space>
              </Form.Item>
              </Form>
            </div>
          </TabPane>
        )}

        {/* Accounts tab */}
        <TabPane 
          tab={
            <span>
              <UserOutlined />
              Accounts
            </span>
          } 
          key="accounts"
        >
          <div className="bilibili-manager-content">
            <div style={{ marginBottom: 16 }}>
              <Button 
                type="primary" 
                icon={<PlusOutlined />} 
                onClick={() => setShowAddAccount(true)}
              >
                Add account
              </Button>
            </div>

            <Table
              columns={accountColumns}
              dataSource={accounts}
              rowKey="id"
              loading={loading}
              pagination={false}
              size="small"
            />
          </div>
        </TabPane>

        {/* Upload-status tab */}
        <TabPane 
          tab={
            <span>
              <ReloadOutlined />
              Uploads
            </span>
          } 
          key="status"
        >
          <div className="bilibili-manager-content">
            <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ margin: 0, color: '#ffffff' }}>Upload tasks</h3>
              <Button 
                type="primary" 
                icon={<ReloadOutlined />} 
                onClick={fetchUploadRecords}
                loading={recordsLoading}
              >
                Refresh
              </Button>
            </div>

            {/* Stats */}
            {(() => {
              const stats = getStatistics()
              return (
                <Row gutter={16} style={{ marginBottom: 24 }}>
                  <Col span={6}>
                    <Card style={{ background: '#262626', border: '1px solid #404040' }}>
                      <Statistic 
                        title={<span style={{ color: '#ffffff' }}>Total tasks</span>} 
                        value={stats.total} 
                        valueStyle={{ color: '#ffffff' }} 
                      />
                    </Card>
                  </Col>
                  <Col span={6}>
                    <Card style={{ background: '#262626', border: '1px solid #404040' }}>
                      <Statistic 
                        title={<span style={{ color: '#ffffff' }}>Succeeded</span>} 
                        value={stats.success} 
                        valueStyle={{ color: '#52c41a' }}
                        prefix={<CheckCircleOutlined />}
                      />
                    </Card>
                  </Col>
                  <Col span={6}>
                    <Card style={{ background: '#262626', border: '1px solid #404040' }}>
                      <Statistic 
                        title={<span style={{ color: '#ffffff' }}>Failed</span>} 
                        value={stats.failed} 
                        valueStyle={{ color: '#ff4d4f' }}
                        prefix={<ExclamationCircleOutlined />}
                      />
                    </Card>
                  </Col>
                  <Col span={6}>
                    <Card style={{ background: '#262626', border: '1px solid #404040' }}>
                      <Statistic 
                        title={<span style={{ color: '#ffffff' }}>In progress</span>} 
                        value={stats.processing + stats.pending} 
                        valueStyle={{ color: '#1890ff' }}
                        prefix={<PlayCircleOutlined />}
                      />
                    </Card>
                  </Col>
                </Row>
              )
            })()}

            {/* Task list */}
            <Table
              columns={uploadStatusColumns}
              dataSource={uploadRecords}
              rowKey="id"
              loading={recordsLoading}
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} items`
              }}
              scroll={{ x: 1200 }}
              size="small"
            />
          </div>
        </TabPane>
      </Tabs>
      </div>

      {/* Add-account dialog */}
      <Modal
        title="Add Bilibili account"
        open={showAddAccount}
        onCancel={() => {
          setShowAddAccount(false)
          cookieForm.resetFields()
        }}
        footer={null}
        width={600}
      >
        <Alert
          message="Cookie import recommended"
          description="Cookie import is the safest, most stable sign-in and won't trigger Bilibili risk controls."
          type="info"
          showIcon
          style={{ marginBottom: 16 }}
        />

        <Form form={cookieForm} onFinish={handleCookieLogin} layout="vertical">
          <Form.Item
            name="nickname"
            label="Nickname"
            rules={[{ required: true, message: 'Please enter a nickname' }]}
          >
            <Input placeholder="Nickname for identification" />
          </Form.Item>
          
          <Form.Item
            name="cookies"
            label={
              <Space>
                <span>Cookie</span>
                <Tooltip title={cookieGuideContent} placement="topLeft">
                  <Button 
                    type="link" 
                    size="small" 
                    icon={<QuestionCircleOutlined />}
                  >
                    How to get it
                  </Button>
                </Tooltip>
              </Space>
            }
            rules={[
              { required: true, message: 'Please enter the cookie' },
              { min: 10, message: 'Cookie must be at least 10 characters' }
            ]}
          >
            <TextArea
              rows={4}
              placeholder="Copy the cookie from browser devtools, e.g. SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx"
            />
          </Form.Item>
          
          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={loading}>
                Add account
              </Button>
              <Button onClick={() => setShowAddAccount(false)}>
                Cancel
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      {/* Upload-task detail modal */}
      <Modal
        title="Upload task details"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={null}
        width={800}
        className="bilibili-manager-modal"
      >
        {selectedRecord && (
          <div>
            <Descriptions 
              column={2} 
              bordered
              labelStyle={{ 
                background: '#1f1f1f', 
                color: '#ffffff',
                fontWeight: 'bold',
                borderRight: '1px solid #303030'
              }}
              contentStyle={{ 
                background: '#262626', 
                color: '#ffffff',
                borderLeft: '1px solid #303030'
              }}
              style={{ 
                background: '#262626',
                border: '1px solid #303030'
              }}
            >
              <Descriptions.Item label="Task ID" span={1}>
                <Text code>{selectedRecord.id}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="Status" span={1}>
                {getStatusTag(selectedRecord.status)}
              </Descriptions.Item>
              <Descriptions.Item label="Title" span={2}>
                <Text>{selectedRecord.title}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="Upload account" span={1}>
                <Text>{selectedRecord.account_nickname || selectedRecord.account_username}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="Partition" span={1}>
                <Tag>{getPartitionName(selectedRecord.partition_id)}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Project" span={1}>
                <Text>{selectedRecord.project_name || '-'}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="Clip ID" span={1}>
                <Text code>{selectedRecord.clip_id}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="Progress" span={2}>
                <Progress 
                  percent={selectedRecord.progress} 
                  status={
                    selectedRecord.status === 'failed' ? 'exception' :
                    selectedRecord.status === 'success' || selectedRecord.status === 'completed' ? 'success' :
                    selectedRecord.status === 'processing' ? 'active' : 'normal'
                  }
                />
              </Descriptions.Item>
              <Descriptions.Item label="File size" span={1}>
                <Text>{formatFileSize(selectedRecord.file_size)}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="Upload duration" span={1}>
                <Text>{formatDuration(selectedRecord.upload_duration)}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="BV ID" span={1}>
                {selectedRecord.bv_id ? <Text code>{selectedRecord.bv_id}</Text> : <Text>-</Text>}
              </Descriptions.Item>
              <Descriptions.Item label="AV ID" span={1}>
                {selectedRecord.av_id ? <Text code>{selectedRecord.av_id}</Text> : <Text>-</Text>}
              </Descriptions.Item>
              <Descriptions.Item label="Created" span={1}>
                <Text>{new Date(selectedRecord.created_at).toLocaleString()}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="Updated" span={1}>
                <Text>{new Date(selectedRecord.updated_at).toLocaleString()}</Text>
              </Descriptions.Item>
            </Descriptions>

            {selectedRecord.description && (
              <div style={{ marginTop: '16px' }}>
                <h4 style={{ color: '#ffffff' }}>Description</h4>
                <Text>{selectedRecord.description}</Text>
              </div>
            )}

            {selectedRecord.tags && (
              <div style={{ marginTop: '16px' }}>
                <h4 style={{ color: '#ffffff' }}>Tags</h4>
                <Text>{selectedRecord.tags}</Text>
              </div>
            )}

            {selectedRecord.error_message && (
              <div style={{ marginTop: '16px' }}>
                <h4 style={{ color: '#ffffff' }}>Error</h4>
                <Alert
                  message="Upload failed"
                  description={selectedRecord.error_message}
                  type="error"
                  showIcon
                />
              </div>
            )}

            <div style={{ marginTop: '24px', textAlign: 'right' }}>
              <Space>
                {selectedRecord.status === 'failed' && (
                  <Popconfirm
                    title="Retry this upload task?"
                    onConfirm={() => {
                      handleRetry(selectedRecord.id)
                      setDetailModalVisible(false)
                    }}
                    okText="Retry"
                    cancelText="Cancel"
                  >
                    <Button type="primary" icon={<RedoOutlined />}>
                      Retry
                    </Button>
                  </Popconfirm>
                )}
                <Button onClick={() => setDetailModalVisible(false)}>
                  Close
                </Button>
              </Space>
            </div>
          </div>
        )}
      </Modal>
    </Modal>
  )
}

export default BilibiliManager
