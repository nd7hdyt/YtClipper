import React, { useState, useEffect } from 'react'
import { 
  Layout, 
  Card, 
  Button, 
  Typography, 
  Space, 
  Alert, 
  Row, 
  Col, 
  Form, 
  Input, 
  message,
  Tag,
  Descriptions,
  Collapse
} from 'antd'
import { 
  BugOutlined, 
  ApiOutlined, 
  SettingOutlined, 
  CheckCircleOutlined,
  CloseCircleOutlined,
  ReloadOutlined
} from '@ant-design/icons'
import { settingsApi } from '../services/api'
import { isDesktopMode } from '../utils/desktopMode'

const { Content } = Layout
const { Title, Text, Paragraph } = Typography
const { Panel } = Collapse

interface DebugInfo {
  desktopMode: {
    isDesktop: boolean
    source: string
    environment?: any
  }
  apiStatus: {
    settings: boolean
    desktopMode: boolean
    testApi: boolean
  }
  currentSettings: any
  errors: string[]
}

const DebugPage: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [debugInfo, setDebugInfo] = useState<DebugInfo>({
    desktopMode: { isDesktop: false, source: 'unknown' },
    apiStatus: { settings: false, desktopMode: false, testApi: false },
    currentSettings: null,
    errors: []
  })
  const [form] = Form.useForm()

  // Test desktop mode detection
  const testDesktopMode = async () => {
    try {
      setLoading(true)
      const isDesktop = await isDesktopMode()
      const info = {
        isDesktop,
        source: 'frontend_check',
        environment: {
          userAgent: navigator.userAgent,
          hasTauri: Boolean((window as any).__TAURI__ || (window as any).__TAURI_INTERNALS__),
          location: window.location.href,
        }
      }
      setDebugInfo(prev => ({
        ...prev,
        desktopMode: info
      }))
      message.success('Desktop mode detection complete')
    } catch (error: any) {
      const errorMsg = `Desktop mode detection failed: ${error.message}`
      setDebugInfo(prev => ({
        ...prev,
        errors: [...prev.errors, errorMsg]
      }))
      message.error(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  // Test API connections
  const testApiConnections = async () => {
    const errors: string[] = []
    const apiStatus = { settings: false, desktopMode: false, testApi: false }

    try {
      setLoading(true)
      
      // Test settings API
      try {
        const settings = await settingsApi.getSettings()
        apiStatus.settings = true
        setDebugInfo(prev => ({
          ...prev,
          currentSettings: settings
        }))
      } catch (error: any) {
        errors.push(`Settings API failed: ${error.message}`)
      }

      // Test desktop mode API
      try {
        const desktopMode = await settingsApi.checkDesktopMode()
        apiStatus.desktopMode = true
        console.log('Desktop mode API response:', desktopMode)
      } catch (error: any) {
        errors.push(`Desktop mode API failed: ${error.message}`)
      }

      // Test API key test endpoint
      try {
        const testResult = await settingsApi.testApiKey('dashscope', 'test-key')
        apiStatus.testApi = true
        console.log('API test response:', testResult)
      } catch (error: any) {
        errors.push(`API test endpoint failed: ${error.message}`)
      }

      setDebugInfo(prev => ({
        ...prev,
        apiStatus,
        errors: [...prev.errors, ...errors]
      }))

      if (errors.length === 0) {
        message.success('All API connection tests passed')
      } else {
        message.warning(`Some API tests failed: ${errors.length} error(s)`)
      }
    } catch (error: any) {
      const errorMsg = `API connection test failed: ${error.message}`
      setDebugInfo(prev => ({
        ...prev,
        errors: [...prev.errors, errorMsg]
      }))
      message.error(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  // Test API key saving
  const testApiKeySave = async () => {
    try {
      setLoading(true)
      const values = form.getFieldsValue()
      
      if (!values.apiKey || !values.provider) {
        message.error('Please enter an API key and a provider')
        return
      }

      const testSettings = {
        basic: {
          app_name: "AutoClip Desktop",
          app_version: "1.0.0",
          debug_mode: false,
          auto_start: true
        },
        service: {
          host: "127.0.0.1",
          port: 8000,
          max_memory_usage: 2048
        },
        api: {
          api_keys: {
            dashscope: values.provider === 'dashscope' ? values.apiKey : '',
            openai: values.provider === 'openai' ? values.apiKey : '',
            gemini: values.provider === 'gemini' ? values.apiKey : '',
            siliconflow: values.provider === 'siliconflow' ? values.apiKey : '',
            jimeng_access: '',
            jimeng_secret: ''
          },
          api_model: values.provider === 'dashscope' ? 'qwen-plus' : 
                     values.provider === 'openai' ? 'gpt-3.5-turbo' :
                     values.provider === 'gemini' ? 'gemini-pro' : 'qwen-plus',
          api_max_tokens: 4000,
          api_timeout: 30
        },
        processing: {
          processing_chunk_size: 5000,
          processing_min_score: 0.7,
          processing_max_clips: 5,
          processing_max_retries: 3
        },
        logs: {
          log_level: "INFO",
          log_retention_days: 7
        }
      }

      await settingsApi.updateSettings(testSettings)
      message.success('API key save test succeeded!')
    } catch (error: any) {
      const errorMsg = `API key save failed: ${error.message}`
      setDebugInfo(prev => ({
        ...prev,
        errors: [...prev.errors, errorMsg]
      }))
      message.error(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  // Clear cache and re-detect
  const refreshAll = async () => {
    await testDesktopMode()
    await testApiConnections()
  }

  // Auto-detect on page load
  useEffect(() => {
    testDesktopMode()
    testApiConnections()
  }, [])

  return (
    <Layout style={{ minHeight: '100vh', background: '#f5f5f5' }}>
      <Content style={{ padding: '24px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <Title level={2}>
            <BugOutlined /> AutoClip Debug Page
          </Title>
          
          <Paragraph>
            This page is for debugging desktop mode detection and API key saving. Please test each feature in order.
          </Paragraph>

          <Row gutter={[16, 16]}>
            {/* Desktop mode detection */}
            <Col span={24}>
              <Card title="Desktop mode detection" extra={
                <Space>
                  <Button 
                    icon={<ReloadOutlined />} 
                    onClick={testDesktopMode}
                    loading={loading}
                  >
                    Re-detect
                  </Button>
                  <Button 
                    icon={<ReloadOutlined />} 
                    onClick={refreshAll}
                    loading={loading}
                  >
                    Refresh all
                  </Button>
                </Space>
              }>
                <Descriptions bordered column={2}>
                  <Descriptions.Item label="Desktop mode status">
                    <Tag color={debugInfo.desktopMode.isDesktop ? 'green' : 'red'}>
                      {debugInfo.desktopMode.isDesktop ? 'Yes' : 'No'}
                    </Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="Detection source">
                    <Tag color="blue">{debugInfo.desktopMode.source}</Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="Environment info" span={2}>
                    <pre style={{ margin: 0, fontSize: '12px' }}>
                      {JSON.stringify(debugInfo.desktopMode.environment, null, 2)}
                    </pre>
                  </Descriptions.Item>
                </Descriptions>
              </Card>
            </Col>

            {/* API connection test */}
            <Col span={24}>
              <Card title="API connection test" extra={
                <Button 
                  icon={<ApiOutlined />} 
                  onClick={testApiConnections}
                  loading={loading}
                >
                  Test connection
                </Button>
              }>
                <Row gutter={16}>
                  <Col span={8}>
                    <Card size="small">
                      <Space>
                        {debugInfo.apiStatus.settings ? 
                          <CheckCircleOutlined style={{ color: 'green' }} /> : 
                          <CloseCircleOutlined style={{ color: 'red' }} />
                        }
                        <Text>Settings API</Text>
                      </Space>
                    </Card>
                  </Col>
                  <Col span={8}>
                    <Card size="small">
                      <Space>
                        {debugInfo.apiStatus.desktopMode ? 
                          <CheckCircleOutlined style={{ color: 'green' }} /> : 
                          <CloseCircleOutlined style={{ color: 'red' }} />
                        }
                        <Text>Desktop mode API</Text>
                      </Space>
                    </Card>
                  </Col>
                  <Col span={8}>
                    <Card size="small">
                      <Space>
                        {debugInfo.apiStatus.testApi ? 
                          <CheckCircleOutlined style={{ color: 'green' }} /> : 
                          <CloseCircleOutlined style={{ color: 'red' }} />
                        }
                        <Text>API test endpoint</Text>
                      </Space>
                    </Card>
                  </Col>
                </Row>
              </Card>
            </Col>

            {/* API key save test */}
            <Col span={24}>
              <Card title="API key save test" extra={
                <Button 
                  type="primary"
                  icon={<SettingOutlined />} 
                  onClick={testApiKeySave}
                  loading={loading}
                >
                  Test save
                </Button>
              }>
                <Form form={form} layout="vertical">
                  <Row gutter={16}>
                    <Col span={12}>
                      <Form.Item
                        name="provider"
                        label="API provider"
                        rules={[{ required: true, message: 'Please select a provider' }]}
                      >
                        <Input placeholder="dashscope, openai, gemini, siliconflow" />
                      </Form.Item>
                    </Col>
                    <Col span={12}>
                      <Form.Item
                        name="apiKey"
                        label="API Key"
                        rules={[{ required: true, message: 'Please enter an API key' }]}
                      >
                        <Input.Password placeholder="Please enter an API key" />
                      </Form.Item>
                    </Col>
                  </Row>
                </Form>
              </Card>
            </Col>

            {/* Current settings info */}
            {debugInfo.currentSettings && (
              <Col span={24}>
                <Card title="Current settings">
                  <Collapse>
                    <Panel header="View full settings" key="1">
                      <pre style={{ 
                        background: '#f5f5f5', 
                        padding: '16px', 
                        borderRadius: '4px',
                        fontSize: '12px',
                        maxHeight: '400px',
                        overflow: 'auto'
                      }}>
                        {JSON.stringify(debugInfo.currentSettings, null, 2)}
                      </pre>
                    </Panel>
                  </Collapse>
                </Card>
              </Col>
            )}

            {/* Error info */}
            {debugInfo.errors.length > 0 && (
              <Col span={24}>
                <Card title="Errors" style={{ borderColor: '#ff4d4f' }}>
                  {debugInfo.errors.map((error, index) => (
                    <Alert
                      key={index}
                      message={error}
                      type="error"
                      showIcon
                      style={{ marginBottom: '8px' }}
                    />
                  ))}
                </Card>
              </Col>
            )}

            {/* Usage instructions */}
            <Col span={24}>
              <Card title="Instructions">
                <Alert
                  message="Debug steps"
                  description={
                    <div>
                      <p>1. First check that "Desktop mode detection" shows "Yes"</p>
                      <p>2. Then run the "API connection test" and make sure every connection is green</p>
                      <p>3. Finally, enter a real API key in the "API key save test"</p>
                      <p>4. If errors appear, see the "Errors" section</p>
                    </div>
                  }
                  type="info"
                  showIcon
                />
              </Card>
            </Col>
          </Row>
        </div>
      </Content>
    </Layout>
  )
}

export default DebugPage