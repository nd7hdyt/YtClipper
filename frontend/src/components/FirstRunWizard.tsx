import React, { useState, useEffect } from 'react'
import { Card, Button, Typography, Space, Alert, message, Form, Input, Select } from 'antd'
import { 
  SoundOutlined, 
  ApiOutlined, 
  CheckCircleOutlined,
  LoadingOutlined,
  LinkOutlined,
  InfoCircleOutlined
} from '@ant-design/icons'
import { ExternalLink } from '../utils/externalLinks'
import { settingsApi } from '../services/api'
import { isDesktopMode } from '../utils/desktopMode'

const { Title, Text } = Typography
const { Option } = Select

interface FirstRunWizardProps {
  onComplete: () => void
}

interface ConfigForm {
  // Speech recognition config
  speechMethod: string
  whisperModel: string
  openaiApiKey: string
  
  // LLM config
  llmProvider: string
  llmApiKey: string
  azureApiKey?: string
  azureRegion?: string
  googleApiKey?: string
  aliyunApiKey?: string
  customApiKey?: string
  customEndpoint?: string
}

const FirstRunWizard: React.FC<FirstRunWizardProps> = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0)
  const [loading, setLoading] = useState(false)
  const [form] = Form.useForm<ConfigForm>()
  
  const [config, setConfig] = useState<ConfigForm>({
    speechMethod: 'whisper_local',
    whisperModel: 'base',
    openaiApiKey: '',
    llmProvider: 'dashscope',
    llmApiKey: ''
  })

  // Ensure the form is initialized correctly on mount
  useEffect(() => {
    form.setFieldsValue(config)
    console.log('Form initialized with:', config)
  }, [form])

  const handleNext = () => {
    if (currentStep === 0) {
      // Validate the step 1 config
      const values = form.getFieldsValue()
      console.log('Next clicked - form values:', values)
      console.log('llmProvider:', values.llmProvider)
      console.log('llmApiKey:', values.llmApiKey)
      
      if (!values.llmProvider || !values.llmApiKey || values.llmApiKey.trim() === '') {
        message.error('Please select an LLM provider and enter an API key')
        return
      }
      setConfig({ ...config, ...values })
      setCurrentStep(1)
    } else {
      handleComplete()
    }
  }

  const handleComplete = async () => {
    setLoading(true)
    try {
      const values = form.getFieldsValue()
      const finalConfig = { ...config, ...values }
      
      // Validate the speech recognition config
      if (!finalConfig.speechMethod) {
        message.error('Please select a speech recognition method')
        setLoading(false)
        return
      }
      
      // Only save the LLM config when the user entered an API key
      if (finalConfig.llmApiKey && finalConfig.llmApiKey.trim()) {
        try {
          await saveLLMConfig(finalConfig)
          console.log('LLM config saved')
        } catch (error) {
          console.error('Failed to save LLM config:', error)
          message.error('Failed to save LLM config, please retry')
          setLoading(false)
          return
        }
      }
      
      // Save the speech recognition config with error handling
      try {
        await saveSpeechConfig(finalConfig)
      } catch (error) {
        console.warn('Speech config save failed, using defaults:', error)
        // Don't throw; let the user finish the wizard
      }
      
      // Download the model for local Whisper
      if (finalConfig.speechMethod === 'whisper_local') {
        await downloadWhisperModel(finalConfig.whisperModel)
      }
      
      // Done - go straight to the home page
      message.success('Setup complete! Welcome to AutoClip')
      onComplete()
    } catch (error) {
      console.error('Failed to save config:', error)
      const errorMessage = error instanceof Error ? error.message : 'Failed to save config, please retry'
      message.error(`Failed to save config: ${errorMessage}`)
    } finally {
      setLoading(false)
    }
  }

  // Skip the current step and set it up later
  const handleSkip = async () => {
    if (currentStep === 0) {
      // Skip AI model setup, go to speech recognition setup
      setCurrentStep(1)
      message.info('Skipped AI model setup. You can configure it later in Settings.', 3)
    } else {
      // Skip speech recognition setup and finish the wizard
      // Make sure no empty API config is saved
      try {
        // Only save the speech config, not the LLM config
        const values = form.getFieldsValue()
        const finalConfig = { ...config, ...values }
        try {
          await saveSpeechConfig(finalConfig)
        } catch (error) {
          console.warn('Speech config save failed, using defaults:', error)
        }
        
        message.info('Skipped speech setup. You can configure it later in Settings.', 3)
        onComplete()
      } catch (error) {
        message.error('Failed to save config, please retry')
        console.error('Failed to save config:', error)
      }
    }
  }

  const saveLLMConfig = async (config: ConfigForm) => {
    try {
      // Allow saving config in web mode too, for testing and dev
      const isDesktop = await isDesktopMode()
      console.log('Desktop mode check:', isDesktop)

      console.log('Saving LLM config:', {
        provider: config.llmProvider,
        apiKeyLength: config.llmApiKey?.length || 0
      })

      // Fetch existing settings to avoid wiping stored API keys
      let existingSettings = null
      try {
        existingSettings = await settingsApi.getSettings()
      } catch (error) {
        console.warn('Failed to load existing settings, using defaults:', error)
      }

      // Get existing API keys; only update the current provider's key
      const existingApiKeys = existingSettings?.api?.api_keys || {}
      
      const settings = {
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
            // Only update the current provider's key, keep the others
            dashscope: config.llmProvider === 'dashscope' ? config.llmApiKey : (existingApiKeys.dashscope || ''),
            openai: config.llmProvider === 'openai' ? config.llmApiKey : (existingApiKeys.openai || ''),
            gemini: config.llmProvider === 'gemini' ? config.llmApiKey : (existingApiKeys.gemini || ''),
            siliconflow: config.llmProvider === 'siliconflow' ? config.llmApiKey : (existingApiKeys.siliconflow || ''),
            jimeng_access: existingApiKeys.jimeng_access || '',
            jimeng_secret: existingApiKeys.jimeng_secret || ''
          },
          api_model: config.llmProvider === 'dashscope' ? 'qwen-plus' : 
                     config.llmProvider === 'openai' ? 'gpt-3.5-turbo' :
                     config.llmProvider === 'gemini' ? 'gemini-pro' : 'qwen-plus',
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
          log_file_path: "",
          log_file_max_size: 10,
          log_file_backup_count: 5
        }
      }
      
      console.log('Sending settings to backend:', settings)
      const result = await settingsApi.updateSettings(settings)
      console.log('LLM config saved, backend response:', result)
    } catch (error) {
      console.error('Failed to save LLM config:', error)
      const detail = error instanceof Error ? error.message : 'Unknown error'
      throw new Error(`Failed to save LLM config: ${detail}`)
    }
  }

  const saveSpeechConfig = async (config: ConfigForm) => {
    try {
      // Check desktop mode
      const isDesktop = await isDesktopMode()
      if (!isDesktop) {
        console.warn('Not desktop mode, skipping speech config save')
        return
      }

      const values = form.getFieldsValue()
      const speechConfig = {
        method: config.speechMethod,
        whisper_config: {
          model_name: config.whisperModel || 'base',
          language: 'auto',
          enable_timestamps: true,
          enable_punctuation: true
        },
        openai_config: {
          api_key: values.openaiApiKey || '',
          language: 'auto',
          enable_timestamps: true
        },
        azure_config: {
          api_key: values.azureApiKey || '',
          region: values.azureRegion || '',
          language: 'auto',
          enable_timestamps: true,
          enable_punctuation: true
        },
        google_config: {
          api_key: values.googleApiKey || '',
          language: 'auto',
          enable_timestamps: true,
          enable_punctuation: true
        },
        aliyun_config: {
          api_key: values.aliyunApiKey || '',
          language: 'auto',
          enable_timestamps: true,
          enable_punctuation: true
        },
        custom_api_config: {
          api_key: values.customApiKey || '',
          endpoint: values.customEndpoint || '',
          language: 'auto',
          enable_timestamps: true,
          enable_punctuation: true
        },
        enable_fallback: true,
        fallback_method: 'whisper_local',
        output_format: 'srt'
      }
      
      const response = await fetch('/api/v1/speech-recognition/config', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(speechConfig)
      })
      
      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`Failed to save speech recognition config: ${response.status} ${errorText}`)
      }
      
      console.log('Speech recognition config saved')
    } catch (error) {
      console.error('Failed to save speech recognition config:', error)
      if (error instanceof Error) {
        throw new Error(`Failed to save speech recognition config: ${error.message}`)
      } else {
        throw new Error('Failed to save speech recognition config')
      }
    }
  }

  const downloadWhisperModel = async (modelName: string) => {
    try {
      const response = await fetch('/api/v1/speech-recognition/whisper-models/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: modelName })
      })
      
      if (!response.ok) {
        throw new Error('Model download failed')
      }
    } catch (error) {
      console.error('Whisper model download failed:', error)
      // Don't block wizard completion
    }
  }


  const testApiConnection = async (provider: string, apiKey: string) => {
    // Get the latest API key from the form
    const formValues = form.getFieldsValue()
    const currentApiKey = formValues.llmApiKey || apiKey
    
    console.log('testApiConnection args:', { provider, apiKey })
    console.log('testApiConnection form values:', formValues)
    console.log('testApiConnection current API key:', currentApiKey)
    
    if (!currentApiKey || currentApiKey.trim() === '') {
      message.warning('Please enter an API key first')
      return
    }
    
    try {
      const response = await fetch('/api/v1/settings/test-api', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider, api_key: currentApiKey })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      const result = await response.json()
      if (result.success) {
        message.success('API connection test passed!')
      } else {
        message.error(`API connection test failed: ${result.error || 'Unknown error'}`)
      }
    } catch (error) {
      console.error('API test error:', error)
      const detail = error instanceof Error ? error.message : 'Network error'
      message.error(`API connection test failed: ${detail}`)
    }
  }

  // Smart hint for how to obtain an API key
  const getApiKeyHelp = (provider: string) => {
    const helpMap: Record<string, { name: string; url: string; description: string }> = {
      dashscope: {
        name: 'Alibaba Qwen',
        url: 'https://dashscope.aliyun.com',
        description: 'Sign up for Alibaba Cloud, enable DashScope, then create an API key'
      },
      openai: {
        name: 'OpenAI',
        url: 'https://platform.openai.com',
        description: 'Sign up for OpenAI and create a key on the API Keys page'
      },
      gemini: {
        name: 'Google Gemini',
        url: 'https://makersuite.google.com',
        description: 'Sign in with Google and create a key on the API Keys page'
      },
      siliconflow: {
        name: 'SiliconFlow',
        url: 'https://cloud.siliconflow.cn',
        description: 'Sign up for SiliconFlow and create an API key in the console'
      }
    }
    return helpMap[provider] || helpMap.dashscope
  }

  return (
    <div style={{ 
      maxWidth: '600px', 
      margin: '0 auto', 
      padding: '24px 16px',
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center'
    }}>
      {/* Header — compact */}
      <div style={{ textAlign: 'center', marginBottom: '24px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <img src="/favicon.png" alt="AutoClip" style={{ width: 40, height: 40, marginBottom: '8px', display: 'block' }} />
        <Title level={2} style={{ color: '#1890ff', marginBottom: '8px' }}>
          Welcome to AutoClip
        </Title>
        <Text type="secondary" style={{ fontSize: '14px' }}>
          Let's quickly set up your AI video clipping tool
        </Text>
      </div>

      {/* Main config card — compact spacing */}
      <Card style={{ marginBottom: '16px' }}>
        {/* Step title — compact */}
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            gap: '8px',
            marginBottom: '4px'
          }}>
            {currentStep === 0 ? <ApiOutlined style={{ color: '#1890ff' }} /> : <SoundOutlined style={{ color: '#1890ff' }} />}
            <Title level={4} style={{ margin: 0 }}>
              {currentStep === 0 ? 'Configure AI model' : 'Configure speech recognition'}
            </Title>
          </div>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            {currentStep === 0 
              ? 'Pick an LLM provider and enter an API key' 
              : 'Pick a speech recognition option'
            }
          </Text>
        </div>

        <Form 
          form={form} 
          layout="vertical" 
          initialValues={config}
          onValuesChange={(changedValues, allValues) => {
            console.log('Form values changed:', { changedValues, allValues })
          }}
        >
          {currentStep === 0 ? (
            // LLM step — compact layout
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              <Form.Item
                name="llmProvider"
                label="AI model provider"
                rules={[{ required: true, message: 'Please select an AI model provider' }]}
                style={{ marginBottom: '12px' }}
              >
                <Select size="middle" placeholder="Select a provider">
                  <Option value="dashscope">
                    <Space>
                      <Text strong>Alibaba Qwen</Text>
                      <Text type="secondary">(Recommended in China)</Text>
                    </Space>
                  </Option>
                  <Option value="openai">
                    <Space>
                      <Text strong>OpenAI GPT</Text>
                      <Text type="secondary">(Needs international access)</Text>
                    </Space>
                  </Option>
                  <Option value="gemini">
                    <Space>
                      <Text strong>Google Gemini</Text>
                      <Text type="secondary">(Needs international access)</Text>
                    </Space>
                  </Option>
                  <Option value="siliconflow">
                    <Space>
                      <Text strong>SiliconFlow</Text>
                      <Text type="secondary">(China-friendly alternative)</Text>
                    </Space>
                  </Option>
                </Select>
              </Form.Item>

              {/* API key input + test button — horizontal layout */}
              <Form.Item
                name="llmApiKey"
                label="API Key"
                rules={[{ required: true, message: 'Please enter an API key' }]}
                style={{ marginBottom: '12px' }}
              >
                <div style={{ display: 'flex', gap: '8px' }}>
                  <Input.Password 
                    size="middle" 
                    placeholder="Enter your API key"
                    style={{ 
                      flex: 1,
                      backgroundColor: '#fafafa',
                      borderColor: '#d9d9d9'
                    }}
                  />
                  <Button 
                    type="default"
                    size="middle"
                    onClick={() => {
                      const values = form.getFieldsValue()
                      console.log('Test button clicked — form values:', values)
                      testApiConnection(values.llmProvider || 'dashscope', values.llmApiKey || '')
                    }}
                    style={{ width: '80px' }}
                    icon={<LinkOutlined />}
                  >
                    Test
                  </Button>
                </div>
              </Form.Item>

              {/* Smart API key help */}
              <Form.Item shouldUpdate={(prevValues, currentValues) => prevValues.llmProvider !== currentValues.llmProvider}>
                {({ getFieldValue }) => {
                  const provider = getFieldValue('llmProvider') || 'dashscope'
                  const help = getApiKeyHelp(provider)
                  return (
                    <Alert
                      message={
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <InfoCircleOutlined />
                          <span>How to get a {help.name} API key</span>
                        </div>
                      }
                      description={
                        <div>
                          <p style={{ margin: '4px 0', fontSize: '12px' }}>{help.description}</p>
                          <p style={{ margin: '4px 0', fontSize: '12px' }}>
                            Visit: <ExternalLink url={help.url} text={help.url} />
                          </p>
                        </div>
                      }
                      type="info"
                      showIcon={false}
                      style={{ fontSize: '12px' }}
                    />
                  )
                }}
              </Form.Item>
            </Space>
          ) : (
            // Speech recognition step — compact layout
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              <Form.Item
                name="speechMethod"
                label="Speech recognition option"
                rules={[{ required: true, message: 'Please select a speech recognition option' }]}
                style={{ marginBottom: '12px' }}
              >
                <Select size="middle" placeholder="Select an option">
                  <Option value="whisper_local">
                    <Space>
                      <span>🆓</span>
                      <Text strong>Local Whisper model</Text>
                      <Text type="secondary">(Free offline, beginner-friendly)</Text>
                    </Space>
                  </Option>
                  <Option value="openai_api">
                    <Space>
                      <span>🤖</span>
                      <Text strong>OpenAI Whisper API</Text>
                      <Text type="secondary">(Cloud, higher accuracy)</Text>
                    </Space>
                  </Option>
                  <Option value="azure_speech">
                    <Space>
                      <span>☁️</span>
                      <Text strong>Azure Speech Services</Text>
                      <Text type="secondary">(Enterprise-grade)</Text>
                    </Space>
                  </Option>
                  <Option value="google_speech">
                    <Space>
                      <span>🌐</span>
                      <Text strong>Google Speech-to-Text</Text>
                      <Text type="secondary">(Multi-language)</Text>
                    </Space>
                  </Option>
                  <Option value="aliyun_speech">
                    <Space>
                      <span>☁️</span>
                      <Text strong>Alibaba speech recognition</Text>
                      <Text type="secondary">(Optimized for Chinese)</Text>
                    </Space>
                  </Option>
                  <Option value="custom_api">
                    <Space>
                      <span>⚙️</span>
                      <Text strong>Custom API</Text>
                      <Text type="secondary">(Custom server endpoint)</Text>
                    </Space>
                  </Option>
                </Select>
              </Form.Item>

              <Form.Item shouldUpdate={(prevValues, currentValues) => prevValues.speechMethod !== currentValues.speechMethod} noStyle>
                {({ getFieldValue }) => {
                  const speechMethod = getFieldValue('speechMethod')
                  
                  if (speechMethod === 'whisper_local') {
                    return (
                      <Form.Item
                        name="whisperModel"
                        label="Model size"
                        style={{ marginBottom: '12px' }}
                      >
                        <Select size="middle" placeholder="Select a model">
                          <Option value="tiny">Tiny (39MB) - Fastest</Option>
                          <Option value="base">Base (74MB) - Balanced (Recommended)</Option>
                          <Option value="small">Small (244MB) - Better accuracy</Option>
                          <Option value="medium">Medium (769MB) - High accuracy</Option>
                          <Option value="large">Large (1550MB) - Best accuracy</Option>
                        </Select>
                      </Form.Item>
                    )
                  }
                  
                  if (speechMethod === 'openai_api') {
                    return (
                      <Form.Item
                        name="openaiApiKey"
                        label="OpenAI API Key"
                        rules={[{ required: true, message: 'Please enter an OpenAI API key' }]}
                        style={{ marginBottom: '12px' }}
                      >
                        <Input.Password 
                          size="middle" 
                          placeholder="Enter your OpenAI API key"
                        />
                      </Form.Item>
                    )
                  }
                  
                  if (speechMethod === 'azure_speech') {
                    return (
                      <Space direction="vertical" size="small" style={{ width: '100%' }}>
                        <Form.Item
                          name="azureApiKey"
                          label="Azure API Key"
                          rules={[{ required: true, message: 'Please enter an Azure API key' }]}
                          style={{ marginBottom: '8px' }}
                        >
                          <Input.Password 
                            size="middle" 
                            placeholder="Enter your Azure Speech API key"
                          />
                        </Form.Item>
                        <Form.Item
                          name="azureRegion"
                          label="Azure region"
                          style={{ marginBottom: '12px' }}
                        >
                          <Input 
                            size="middle" 
                            placeholder="e.g. eastus, westus2"
                          />
                        </Form.Item>
                      </Space>
                    )
                  }
                  
                  if (speechMethod === 'google_speech') {
                    return (
                      <Form.Item
                        name="googleApiKey"
                        label="Google API Key"
                        rules={[{ required: true, message: 'Please enter a Google API key' }]}
                        style={{ marginBottom: '12px' }}
                      >
                        <Input.Password 
                          size="middle" 
                          placeholder="Enter your Google Speech-to-Text API key"
                        />
                      </Form.Item>
                    )
                  }
                  
                  if (speechMethod === 'aliyun_speech') {
                    return (
                      <Form.Item
                        name="aliyunApiKey"
                        label="Alibaba Cloud API key"
                        rules={[{ required: true, message: 'Please enter an Alibaba Cloud API key' }]}
                        style={{ marginBottom: '12px' }}
                      >
                        <Input.Password 
                          size="middle" 
                          placeholder="Enter your Alibaba speech recognition API key"
                        />
                      </Form.Item>
                    )
                  }
                  
                  if (speechMethod === 'custom_api') {
                    return (
                      <Space direction="vertical" size="small" style={{ width: '100%' }}>
                        <Form.Item
                          name="customApiKey"
                          label="Custom API key"
                          rules={[{ required: true, message: 'Please enter a custom API key' }]}
                          style={{ marginBottom: '8px' }}
                        >
                          <Input.Password 
                            size="middle" 
                            placeholder="Enter your custom API key"
                          />
                        </Form.Item>
                        <Form.Item
                          name="customEndpoint"
                          label="API endpoint"
                          rules={[{ required: true, message: 'Please enter an API endpoint' }]}
                          style={{ marginBottom: '12px' }}
                        >
                          <Input 
                            size="middle" 
                            placeholder="e.g. https://api.example.com/speech"
                          />
                        </Form.Item>
                      </Space>
                    )
                  }
                  
                  return null
                }}
              </Form.Item>

              {/* Smart setup notes — shown per selected option */}
              <Form.Item shouldUpdate={(prevValues, currentValues) => prevValues.speechMethod !== currentValues.speechMethod} style={{ marginBottom: '8px' }}>
                {({ getFieldValue }) => {
                  const speechMethod = getFieldValue('speechMethod')
                  
                  const getMethodDescription = (method: string) => {
                    const descriptions: Record<string, { icon: string; name: string; description: string }> = {
                      whisper_local: {
                        icon: '🆓',
                        name: 'Local Whisper model',
                        description: 'Free offline use; the model downloads on first use, no network needed afterwards. Recommended for beginners.'
                      },
                      openai_api: {
                        icon: '🤖',
                        name: 'OpenAI Whisper API',
                        description: 'Cloud processing with higher accuracy, billed by usage. Needs a stable connection.'
                      },
                      azure_speech: {
                        icon: '☁️',
                        name: 'Azure Speech Services',
                        description: 'Enterprise-grade speech recognition with many languages and dialects, fit for business use.'
                      },
                      google_speech: {
                        icon: '🌐',
                        name: 'Google Speech-to-Text',
                        description: 'Multi-language support, high accuracy, real-time recognition.'
                      },
                      aliyun_speech: {
                        icon: '☁️',
                        name: 'Alibaba speech recognition',
                        description: 'Optimized for Chinese, fast access in China, supports many Chinese dialects.'
                      },
                      custom_api: {
                        icon: '⚙️',
                        name: 'Custom API',
                        description: 'Supports a custom server endpoint; plug in your own speech service.'
                      }
                    }
                    return descriptions[method] || descriptions.whisper_local
                  }
                  
                  const methodInfo = getMethodDescription(speechMethod)
                  
                  return (
                    <Alert
                      message={
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <span>{methodInfo.icon}</span>
                          <span>{methodInfo.name} setup notes</span>
                        </div>
                      }
                      description={
                        <div style={{ fontSize: '12px' }}>
                          <p style={{ margin: '4px 0' }}>{methodInfo.description}</p>
                        </div>
                      }
                      type="info"
                      showIcon={false}
                      style={{ fontSize: '12px', marginTop: '8px' }}
                    />
                  )
                }}
              </Form.Item>
            </Space>
          )}
        </Form>
      </Card>

      {/* Bottom buttons — no step indicator, unified button style */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '12px'
      }}>
        <div>
          {currentStep > 0 && (
            <Button 
              size="middle"
              onClick={() => setCurrentStep(0)}
              disabled={loading}
            >
              Back
            </Button>
          )}
        </div>
        
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button 
            type="default"
            size="middle"
            onClick={handleSkip}
            disabled={loading}
          >
            Set up later
          </Button>
          <Button 
            type="primary" 
            size="middle"
            onClick={handleNext}
            loading={loading}
            icon={loading ? <LoadingOutlined /> : <CheckCircleOutlined />}
          >
            {currentStep === 0 ? 'Next' : 'Get started'}
          </Button>
        </div>
      </div>

      {loading && (
        <div style={{ 
          textAlign: 'center', 
          marginTop: '20px',
          padding: '20px',
          background: '#f5f5f5',
          borderRadius: '8px'
        }}>
          <LoadingOutlined style={{ fontSize: '24px', marginRight: '8px' }} />
          <Text>Saving config and creating a sample project…</Text>
        </div>
      )}
    </div>
  )
}

export default FirstRunWizard