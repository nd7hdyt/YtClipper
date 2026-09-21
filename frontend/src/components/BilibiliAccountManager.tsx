import React, { useState, useEffect } from 'react'
import { Card, Button, Modal, Form, Input, Table, Tag, Space, message, Popconfirm, Tabs, Alert, Typography, Divider, Tooltip, Statistic } from 'antd'
import { PlusOutlined, DeleteOutlined, UserOutlined, CheckCircleOutlined, CloseCircleOutlined, QrcodeOutlined, ExclamationCircleOutlined, QuestionCircleOutlined, HeartOutlined, TrophyOutlined, EyeOutlined, ReloadOutlined } from '@ant-design/icons'
import { uploadApi, BilibiliAccount } from '../services/uploadApi'
import CookieHelper from './CookieHelper'
import AccountHealthMonitor from './AccountHealthMonitor'

const { TextArea } = Input
const { Text, Paragraph } = Typography
const { TabPane } = Tabs

interface AccountHealth {
  score: number
  status: 'excellent' | 'good' | 'warning' | 'poor'
  lastActive: string
  uploadCount: number
  successRate: number
}

const BilibiliAccountManager: React.FC = () => {
  const [accounts, setAccounts] = useState<BilibiliAccount[]>([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [activeTab, setActiveTab] = useState('cookie')
  const [cookieHelperVisible, setCookieHelperVisible] = useState(false)
  const [accountsHealth, setAccountsHealth] = useState<Record<string, AccountHealth>>({})
  const [refreshing, setRefreshing] = useState(false)
  
  // Form state
  const [passwordForm] = Form.useForm()
  const [cookieForm] = Form.useForm()
  const [qrSessionId, setQrSessionId] = useState<string>('')
  const [qrLoginStatus, setQrLoginStatus] = useState<string>('')
  const [qrCodeUrl, setQrCodeUrl] = useState<string>('')
  const [statusCheckInterval, setStatusCheckInterval] = useState<number | null>(null)

  // Fetch accounts
  const fetchAccounts = async () => {
    try {
      setLoading(true)
      const data = await uploadApi.getAccounts()
      setAccounts(data)
      // Also fetch account health
      await fetchAccountsHealth(data)
    } catch (error: any) {
      message.error('Failed to load accounts: ' + (error.message || 'Unknown error'))
    } finally {
      setLoading(false)
    }
  }

  // Fetch account health
  const fetchAccountsHealth = async (accountList?: BilibiliAccount[]) => {
    try {
      const targetAccounts = accountList || accounts
      const healthData: Record<string, AccountHealth> = {}
      
      for (const account of targetAccounts) {
        // Mock health data; should come from the API
        const score = Math.floor(Math.random() * 40) + 60 // 60-100 pts
        const uploadCount = Math.floor(Math.random() * 50) + 10
        const successRate = Math.floor(Math.random() * 30) + 70
        
        let status: AccountHealth['status'] = 'good'
        if (score >= 90) status = 'excellent'
        else if (score >= 75) status = 'good'
        else if (score >= 60) status = 'warning'
        else status = 'poor'
        
        healthData[account.id] = {
          score,
          status,
          lastActive: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
          uploadCount,
          successRate
        }
      }
      
      setAccountsHealth(healthData)
    } catch (error: any) {
      console.error('Failed to fetch account health:', error)
    }
  }

  // Refresh account health
  const refreshAccountsHealth = async () => {
    try {
      setRefreshing(true)
      await fetchAccountsHealth()
      message.success('Health status refreshed')
    } catch (error: any) {
      message.error('Refresh failed: ' + (error.message || 'Unknown error'))
    } finally {
      setRefreshing(false)
    }
  }

  useEffect(() => {
    fetchAccounts()
    
    // Clean up timer
    return () => {
      if (statusCheckInterval) {
        clearInterval(statusCheckInterval)
      }
    }
  }, [])

  // Password login
  const handlePasswordLogin = async (values: any) => {
    try {
      setLoading(true)
      await uploadApi.passwordLogin(values.username, values.password, values.nickname)
      message.success('Password login succeeded!')
      setModalVisible(false)
      passwordForm.resetFields()
      fetchAccounts()
    } catch (error: any) {
      message.error('Password login failed: ' + (error.message || 'Unknown error'))
    } finally {
      setLoading(false)
    }
  }

  // Cookie import login
  const handleCookieLogin = async (values: any) => {
    try {
      setLoading(true)
      
      // Parse cookie string
      const cookieStr = values.cookies.trim()
      const cookies: Record<string, string> = {}
      
      cookieStr.split(';').forEach((cookie: string) => {
        const [key, value] = cookie.trim().split('=')
        if (key && value) {
          cookies[key] = value
        }
      })
      
      if (Object.keys(cookies).length === 0) {
        message.error('Invalid cookie format, please check your input')
        return
      }
      
      await uploadApi.cookieLogin(cookies, values.nickname)
      message.success('Cookie imported!')
      setModalVisible(false)
      cookieForm.resetFields()
      fetchAccounts()
    } catch (error: any) {
      message.error('Cookie import failed: ' + (error.message || 'Unknown error'))
    } finally {
      setLoading(false)
    }
  }

  // Start QR login
  const startQRLogin = async (nickname?: string) => {
    try {
      setLoading(true)
      
      // Clear previous polling
      if (statusCheckInterval) {
        clearInterval(statusCheckInterval)
        setStatusCheckInterval(null)
      }
      
      const response = await uploadApi.startQRLogin(nickname)
      setQrSessionId(response.session_id)
      setQrLoginStatus(response.status)
      
      // Start polling login status
      let pollCount = 0
      const maxPolls = 60
      
      const interval = window.setInterval(async () => {
        try {
          pollCount++
          if (pollCount > maxPolls) {
            message.error('QR login timed out, please retry')
            setQrSessionId('')
            setQrLoginStatus('')
            setQrCodeUrl('')
            clearInterval(interval)
            return
          }
          
          const statusResponse = await uploadApi.checkQRLoginStatus(response.session_id)
          setQrLoginStatus(statusResponse.status)
          
          if (statusResponse.qr_code) {
            setQrCodeUrl(statusResponse.qr_code)
          }
          
          if (statusResponse.status === 'success') {
            message.success('QR login succeeded!')
            clearInterval(interval)
            setModalVisible(false)
            fetchAccounts()
          } else if (statusResponse.status === 'failed') {
            message.error('QR login failed, please retry')
            clearInterval(interval)
          }
        } catch (error: any) {
          console.error('Failed to check login status:', error)
        }
      }, 1000)
      
      setStatusCheckInterval(interval)
      
    } catch (error: any) {
      message.error('Failed to start QR login: ' + (error.message || 'Unknown error'))
    } finally {
      setLoading(false)
    }
  }

  // Delete account
  const handleDeleteAccount = async (accountId: string) => {
    try {
      await uploadApi.deleteAccount(accountId)
      message.success('Account deleted')
      fetchAccounts()
    } catch (error: any) {
      message.error('Failed to delete account: ' + (error.message || 'Unknown error'))
    }
  }

  // Health tag & color
  const getHealthStatusTag = (health?: AccountHealth) => {
    if (!health) return <Tag>Unknown</Tag>
    
    const statusConfig = {
      excellent: { color: 'green', text: 'Excellent', icon: <TrophyOutlined /> },
      good: { color: 'blue', text: 'Good', icon: <CheckCircleOutlined /> },
      warning: { color: 'orange', text: 'Warning', icon: <ExclamationCircleOutlined /> },
      poor: { color: 'red', text: 'Poor', icon: <CloseCircleOutlined /> }
    }
    
    const config = statusConfig[health.status]
    return (
      <Tooltip title={`Health score: ${health.score}/100`}>
        <Tag color={config.color} icon={config.icon}>
          {config.text} ({health.score})
        </Tag>
      </Tooltip>
    )
  }

  // Format last-active time
  const formatLastActive = (dateStr: string) => {
    const date = new Date(dateStr)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return 'Yesterday'
    if (diffDays < 7) return `${diffDays} days ago`
    return date.toLocaleDateString()
  }

  const columns = [
    {
      title: 'Username',
      dataIndex: 'username',
      key: 'username',
      render: (username: string) => (
        <Space>
          <UserOutlined />
          <span>{username}</span>
        </Space>
      ),
    },
    {
      title: 'Nickname',
      dataIndex: 'nickname',
      key: 'nickname',
    },
    {
      title: 'Account status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'red'} icon={status === 'active' ? <CheckCircleOutlined /> : <CloseCircleOutlined />}>
          {status === 'active' ? 'OK' : 'Error'}
        </Tag>
      ),
    },
    {
      title: 'Health',
      key: 'health',
      render: (_: any, record: BilibiliAccount) => getHealthStatusTag(accountsHealth[record.id]),
    },
    {
      title: 'Activity',
      key: 'activity',
      render: (_: any, record: BilibiliAccount) => {
        const health = accountsHealth[record.id]
        if (!health) return '-'
        
        return (
          <Space direction="vertical" size="small" style={{ width: '100%' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <EyeOutlined style={{ color: '#1890ff' }} />
              <span style={{ fontSize: '12px' }}>Uploads: {health.uploadCount}</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <HeartOutlined style={{ color: '#52c41a' }} />
              <span style={{ fontSize: '12px' }}>Success rate: {health.successRate}%</span>
            </div>
            <div style={{ fontSize: '11px', color: '#999' }}>
              Last active: {formatLastActive(health.lastActive)}
            </div>
          </Space>
        )
      },
    },
    {
      title: 'Actions',
      key: 'action',
      render: (_: any, record: BilibiliAccount) => (
        <Space size="middle">
          <Tooltip title="View details">
            <Button type="text" icon={<EyeOutlined />} size="small">
              Details
            </Button>
          </Tooltip>
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
        </Space>
      ),
    },
  ]

  // Aggregate stats
  const getTotalStats = () => {
    const safeAccounts = Array.isArray(accounts) ? accounts : []
    const totalAccounts = safeAccounts.length
    const activeAccounts = safeAccounts.filter(acc => acc.status === 'active').length
    const healthScores = Object.values(accountsHealth).map(h => h.score)
    const avgHealth = healthScores.length > 0 ? Math.round(healthScores.reduce((a, b) => a + b, 0) / healthScores.length) : 0
    const excellentCount = Object.values(accountsHealth).filter(h => h.status === 'excellent').length
    
    return { totalAccounts, activeAccounts, avgHealth, excellentCount }
  }

  const stats = getTotalStats()

  return (
    <div>
      <Tabs
        defaultActiveKey="accounts"
        items={[
          {
            key: 'accounts',
            label: (
              <span>
                <UserOutlined />
                Accounts
              </span>
            ),
            children: (
              <div>
                {/* Stats cards */}
                <div style={{ marginBottom: '16px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
                  <Card size="small">
                    <Statistic
                      title="Total accounts"
                      value={stats.totalAccounts}
                      prefix={<UserOutlined />}
                      valueStyle={{ color: '#1890ff' }}
                    />
                  </Card>
                  <Card size="small">
                    <Statistic
                      title="Active accounts"
                      value={stats.activeAccounts}
                      suffix={`/ ${stats.totalAccounts}`}
                      prefix={<CheckCircleOutlined />}
                      valueStyle={{ color: '#52c41a' }}
                    />
                  </Card>
                  <Card size="small">
                    <Statistic
                      title="Avg health"
                      value={stats.avgHealth}
                      suffix=" pts"
                      prefix={<HeartOutlined />}
                      valueStyle={{ color: stats.avgHealth >= 80 ? '#52c41a' : stats.avgHealth >= 60 ? '#faad14' : '#ff4d4f' }}
                    />
                  </Card>
                  <Card size="small">
                    <Statistic
                      title="Excellent accounts"
                      value={stats.excellentCount}
                      prefix={<TrophyOutlined />}
                      valueStyle={{ color: '#722ed1' }}
                    />
                  </Card>
                </div>

                <Card 
                  title="BilibiliAccounts" 
                  extra={
                    <Space>
                      <Tooltip title="RefreshHealth">
                        <Button 
                          icon={<ReloadOutlined />} 
                          onClick={refreshAccountsHealth}
                          loading={refreshing}
                          size="small"
                        >
                          Refresh
                        </Button>
                      </Tooltip>
                      <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
                        Add account
                      </Button>
                    </Space>
                  }
                >
                  <Table
                    columns={columns}
                    dataSource={accounts}
                    rowKey="id"
                    loading={loading}
                    pagination={{
                      pageSize: 10,
                      showSizeChanger: true,
                      showQuickJumper: true,
                      showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} items`
                    }}
                    scroll={{ x: 800 }}
                  />
                </Card>
              </div>
            ),
          },
          {
            key: 'health',
            label: (
              <span>
                <HeartOutlined />
                Health monitor
              </span>
            ),
            children: <AccountHealthMonitor onRefresh={fetchAccounts} />,
          },
        ]}
      />

      <Modal
        title="Add Bilibili account"
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false)
          setQrSessionId('')
          setQrLoginStatus('')
          setQrCodeUrl('')
          if (statusCheckInterval) {
            clearInterval(statusCheckInterval)
            setStatusCheckInterval(null)
          }
        }}
        footer={null}
        width={600}
      >
        <Alert
          message="Sign-in methods"
          description="To avoid Bilibili risk controls, cookie import is recommended. QR login may trigger them."
          type="info"
          showIcon
          style={{ marginBottom: 16 }}
        />

        <Tabs activeKey={activeTab} onChange={setActiveTab}>
          <TabPane tab="Import via cookie" key="cookie">
            <Form form={cookieForm} onFinish={handleCookieLogin} layout="vertical">
              <Form.Item
                name="nickname"
                label="Nickname"
                rules={[{ required: true, message: 'Please enter a nickname' }]}
              >
                <Input placeholder="Please enter a nickname" />
              </Form.Item>
              
                             <Form.Item
                 name="cookies"
                 label={
                   <Space>
                     <span>Cookie</span>
                     <Button 
                       type="link" 
                       size="small" 
                       icon={<QuestionCircleOutlined />}
                       onClick={() => setCookieHelperVisible(true)}
                     >
                       Help
                     </Button>
                   </Space>
                 }
                 rules={[{ required: true, message: 'Please enter the cookie' }]}
               >
                 <TextArea
                   rows={6}
                   placeholder="Copy the cookie from browser devtools, e.g. SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx"
                 />
               </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading} block>
                  Import cookie
                </Button>
              </Form.Item>
            </Form>
            
                         <Divider />
             <Paragraph type="secondary" style={{ fontSize: '12px' }}>
               <Text strong>Quick cookie guide:</Text>
               <br />
               Click Help above for detailed steps.
             </Paragraph>
          </TabPane>

          <TabPane tab="Password" key="password">
            <Form form={passwordForm} onFinish={handlePasswordLogin} layout="vertical">
              <Form.Item
                name="username"
                label="Username"
                rules={[{ required: true, message: 'Please enter a username' }]}
              >
                <Input placeholder="Enter your Bilibili username or phone" />
              </Form.Item>
              
              <Form.Item
                name="password"
                label="Password"
                rules={[{ required: true, message: 'Please enter a password' }]}
              >
                <Input.Password placeholder="Please enter a password" />
              </Form.Item>
              
              <Form.Item
                name="nickname"
                label="Nickname"
                rules={[{ required: true, message: 'Please enter a nickname' }]}
              >
                <Input placeholder="Please enter a nickname" />
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading} block>
                  Sign in
                </Button>
              </Form.Item>
            </Form>
            
            <Alert
              message="Note"
              description="Password login may require captcha; use cookie import if you hit issues."
              type="warning"
              showIcon
            />
          </TabPane>

          <TabPane tab="QR login" key="qr">
            <div style={{ textAlign: 'center' }}>
              {!qrSessionId ? (
                <div>
                  <Form.Item label="Nickname">
                    <Input placeholder="Please enter a nickname (optional)" />
                  </Form.Item>
                  <Button 
                    type="primary" 
                    icon={<QrcodeOutlined />}
                    onClick={() => startQRLogin()}
                    loading={loading}
                    block
                  >
                    Start QR login
                  </Button>
                </div>
              ) : (
                <div>
                  {qrCodeUrl && (
                    <div style={{ marginBottom: '16px' }}>
                      <img src={qrCodeUrl} alt="QR code" style={{ maxWidth: '200px' }} />
                    </div>
                  )}
                  
                  {qrLoginStatus === 'pending' && (
                    <p>Generating QR code...</p>
                  )}
                  
                  {qrLoginStatus === 'processing' && (
                    <p>Scan the QR code with the Bilibili app</p>
                  )}
                  
                  {qrLoginStatus === 'success' && (
                    <p style={{ color: '#52c41a' }}>✅ Signed in!</p>
                  )}
                  
                  {qrLoginStatus === 'failed' && (
                    <p style={{ color: '#ff4d4f' }}>❌ Sign-in failed, please retry</p>
                  )}
                </div>
              )}
            </div>
            
            <Alert
              message="Risk note"
              description="QR login may trigger risk controls; cookie import is preferred."
              type="error"
              showIcon
            />
          </TabPane>
        </Tabs>
      </Modal>

      <CookieHelper 
        visible={cookieHelperVisible}
        onClose={() => setCookieHelperVisible(false)}
      />
    </div>
  )
 }

export default BilibiliAccountManager
