import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Tabs, 
  Form, 
  Input, 
  InputNumber, 
  Switch, 
  Button, 
  message, 
  Space,
  Typography,
  Divider,
  Row,
  Col,
  Statistic
} from 'antd';
import { 
  SettingOutlined, 
  ApiOutlined, 
  DatabaseOutlined, 
  ToolOutlined,
  SaveOutlined,
  ReloadOutlined
} from '@ant-design/icons';

const { Title } = Typography;
const { TabPane } = Tabs;

interface DesktopConfig {
  app_name: string;
  app_version: string;
  debug_mode: boolean;
  host: string;
  port: number;
  max_memory_usage: number;
  database_url: string;
  celery_broker_url: string;
  celery_result_backend: string;
  celery_worker_concurrency: number;
  dashscope_api_key: string;
  openai_api_key: string;
  gemini_api_key: string;
  siliconflow_api_key: string;
  default_model: string;
  max_tokens: number;
  timeout: number;
  chunk_size: number;
  min_score_threshold: number;
  max_clips_per_collection: number;
  max_retries: number;
  log_level: string;
  log_retention_days: number;
}

interface SystemInfo {
  platform: string;
  platform_version: string;
  architecture: string;
  processor: string;
  memory_total: number;
  memory_available: number;
  memory_usage_percent: number;
  disk_usage_percent: number;
  python_version: string;
  app_version: string;
}

interface ServiceStatus {
  is_running: boolean;
  port: number;
  uptime: string;
  memory_usage: number;
  cpu_usage: number;
  last_health_check: string;
}

const DesktopSettings: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [config, setConfig] = useState<DesktopConfig | null>(null);
  const [systemInfo, setSystemInfo] = useState<SystemInfo | null>(null);
  const [serviceStatus, setServiceStatus] = useState<ServiceStatus | null>(null);

  // Load config
  const loadConfig = async () => {
    try {
      const response = await fetch('/api/v1/desktop/config');
      if (response.ok) {
        const data = await response.json();
        setConfig(data.config);
        form.setFieldsValue(data.config);
      } else {
        message.error('Load configFailed');
      }
    } catch (error) {
      console.error('Load configError:', error);
      message.error('Load configFailed');
    }
  };

  // Load system info
  const loadSystemInfo = async () => {
    try {
      const response = await fetch('/api/v1/desktop/system/info');
      if (response.ok) {
        const data = await response.json();
        setSystemInfo(data);
      }
    } catch (error) {
      console.error('Load system infoFailed:', error);
    }
  };

  // Load servicesStatus
  const loadServiceStatus = async () => {
    try {
      const response = await fetch('/api/v1/desktop/service/status');
      if (response.ok) {
        const data = await response.json();
        setServiceStatus(data);
      }
    } catch (error) {
      console.error('Load servicesStatusFailed:', error);
    }
  };

  // Saveconfig
  const saveConfig = async (values: DesktopConfig) => {
    setLoading(true);
    try {
      // ENDesktopConfigEN
      const configData = {
        app_name: values.app_name || "AutoClip Desktop",
        app_version: values.app_version || "1.0.0",
        debug_mode: values.debug_mode || false,
        host: values.host || "127.0.0.1",
        port: values.port || 8000,
        max_memory_usage: values.max_memory_usage || 2048,
        database_url: values.database_url || "sqlite:///data/autoclip.db",
        celery_broker_url: values.celery_broker_url || "db+sqlite:///data/celery_broker.db",
        celery_result_backend: values.celery_result_backend || "db+sqlite:///data/celery_results.db",
        celery_worker_concurrency: values.celery_worker_concurrency || 1,
        dashscope_api_key: values.dashscope_api_key || "",
        openai_api_key: values.openai_api_key || "",
        gemini_api_key: values.gemini_api_key || "",
        siliconflow_api_key: values.siliconflow_api_key || "",
        default_model: values.default_model || "qwen-plus",
        max_tokens: values.max_tokens || 4000,
        timeout: values.timeout || 30,
        chunk_size: values.chunk_size || 5000,
        min_score_threshold: values.min_score_threshold || 0.7,
        max_clips_per_collection: values.max_clips_per_collection || 5,
        max_retries: values.max_retries || 3,
        log_level: values.log_level || "INFO",
        log_retention_days: values.log_retention_days || 7
      };

      const response = await fetch('/api/v1/desktop/config', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(configData),
      });

      if (response.ok) {
        message.success('configSaveSucceeded');
        setConfig(configData);
      } else {
        const errorData = await response.json();
        message.error(`configSave failed: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('configSaveError:', error);
      message.error('configSave failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadConfig();
    loadSystemInfo();
    loadServiceStatus();
  }, []);

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>
        <SettingOutlined /> ENsettings
      </Title>
      
      <Tabs defaultActiveKey="basic">
        {/* Basic settings */}
        <TabPane tab={<span><SettingOutlined />Basic settings</span>} key="basic">
          <Card>
            <Form
              form={form}
              layout="vertical"
              onFinish={saveConfig}
              initialValues={config ?? undefined}
            >
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    name="app_name"
                    label="App name"
                    rules={[{ required: true, message: 'Please enterApp name' }]}
                  >
                    <Input />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="app_version"
                    label="App version"
                    rules={[{ required: true, message: 'Please enterApp version' }]}
                  >
                    <Input />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item
                name="debug_mode"
                label="EN"
                valuePropName="checked"
              >
                <Switch />
              </Form.Item>

              <Divider />

              <Title level={4}>serviceconfig</Title>
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    name="host"
                    label="Host"
                    rules={[{ required: true, message: 'Please enterHost' }]}
                  >
                    <Input />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="port"
                    label="port"
                    rules={[{ required: true, message: 'Please enterport' }]}
                  >
                    <InputNumber min={1} max={65535} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item
                name="max_memory_usage"
                label="Max memory usage (MB)"
                rules={[{ required: true, message: 'Please enterMax memory usage' }]}
              >
                <InputNumber min={512} max={8192} style={{ width: '100%' }} />
              </Form.Item>

              <Form.Item>
                <Space>
                  <Button 
                    type="primary" 
                    htmlType="submit" 
                    loading={loading}
                    icon={<SaveOutlined />}
                  >
                    Saveconfig
                  </Button>
                  <Button 
                    icon={<ReloadOutlined />}
                    onClick={loadConfig}
                  >
                    EN
                  </Button>
                </Space>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>

        {/* APIsettings */}
        <TabPane tab={<span><ApiOutlined />APIsettings</span>} key="api">
          <Card>
            <Form
              form={form}
              layout="vertical"
              onFinish={saveConfig}
              initialValues={config ?? undefined}
            >
              <Title level={4}>APIEN</Title>
              <Form.Item
                name="dashscope_api_key"
                label="DashScope API Key"
              >
                <Input.Password placeholder="Please enterDashScope API Key" />
              </Form.Item>

              <Form.Item
                name="openai_api_key"
                label="OpenAI API Key"
              >
                <Input.Password placeholder="Please enterOpenAI API Key" />
              </Form.Item>

              <Form.Item
                name="gemini_api_key"
                label="Gemini API Key"
              >
                <Input.Password placeholder="Please enterGemini API Key" />
              </Form.Item>

              <Form.Item
                name="siliconflow_api_key"
                label="SiliconFlow API Key"
              >
                <Input.Password placeholder="Please enterSiliconFlow API Key" />
              </Form.Item>

              <Divider />

              <Title level={4}>Modelconfig</Title>
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    name="default_model"
                    label="Default model"
                    rules={[{ required: true, message: 'Please enterDefault model' }]}
                  >
                    <Input />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="max_tokens"
                    label="maxTokenEN"
                    rules={[{ required: true, message: 'Please entermaxTokenEN' }]}
                  >
                    <InputNumber min={100} max={8000} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item
                name="timeout"
                label="Timeout (EN)"
                rules={[{ required: true, message: 'Please enterTimeout' }]}
              >
                <InputNumber min={10} max={300} style={{ width: '100%' }} />
              </Form.Item>

              <Form.Item>
                <Button 
                  type="primary" 
                  htmlType="submit" 
                  loading={loading}
                  icon={<SaveOutlined />}
                >
                  Saveconfig
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>

        {/* Processing settings */}
        <TabPane tab={<span><ToolOutlined />Processing settings</span>} key="processing">
          <Card>
            <Form
              form={form}
              layout="vertical"
              onFinish={saveConfig}
              initialValues={config ?? undefined}
            >
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    name="chunk_size"
                    label="Chunk size"
                    rules={[{ required: true, message: 'Please enterChunk size' }]}
                  >
                    <InputNumber min={1000} max={10000} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="min_score_threshold"
                    label="Min score threshold"
                    rules={[{ required: true, message: 'Please enterMin score threshold' }]}
                  >
                    <InputNumber min={0.1} max={1.0} step={0.1} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    name="max_clips_per_collection"
                    label="ENCollectionMax clips"
                    rules={[{ required: true, message: 'Please enterMax clips' }]}
                  >
                    <InputNumber min={1} max={20} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="max_retries"
                    label="maxRetryEN"
                    rules={[{ required: true, message: 'Please entermaxRetryEN' }]}
                  >
                    <InputNumber min={1} max={10} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item>
                <Button 
                  type="primary" 
                  htmlType="submit" 
                  loading={loading}
                  icon={<SaveOutlined />}
                >
                  Saveconfig
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>

        {/* System info */}
        <TabPane tab={<span><DatabaseOutlined />System info</span>} key="system">
          <Card>
            {systemInfo && (
              <Row gutter={16}>
                <Col span={8}>
                  <Statistic
                    title="Actionssystem"
                    value={systemInfo.platform}
                    suffix={systemInfo.platform_version}
                  />
                </Col>
                <Col span={8}>
                  <Statistic
                    title="arch"
                    value={systemInfo.architecture}
                  />
                </Col>
                <Col span={8}>
                  <Statistic
                    title="Pythonversion"
                    value={systemInfo.python_version}
                  />
                </Col>
              </Row>
            )}

            {systemInfo && (
              <>
                <Divider />
                <Row gutter={16}>
                  <Col span={12}>
                    <Statistic
                      title="EN"
                      value={formatBytes(systemInfo.memory_total)}
                    />
                  </Col>
                  <Col span={12}>
                    <Statistic
                      title="EN"
                      value={formatBytes(systemInfo.memory_available)}
                    />
                  </Col>
                </Row>
                <Row gutter={16}>
                  <Col span={12}>
                    <Statistic
                      title="EN"
                      value={systemInfo.memory_usage_percent}
                      suffix="%"
                    />
                  </Col>
                  <Col span={12}>
                    <Statistic
                      title="EN"
                      value={systemInfo.disk_usage_percent}
                      suffix="%"
                    />
                  </Col>
                </Row>
              </>
            )}

            {serviceStatus && (
              <>
                <Divider />
                <Title level={4}>serviceStatus</Title>
                <Row gutter={16}>
                  <Col span={8}>
                    <Statistic
                      title="serviceStatus"
                      value={serviceStatus.is_running ? "running" : "EN"}
                      valueStyle={{ color: serviceStatus.is_running ? '#3f8600' : '#cf1322' }}
                    />
                  </Col>
                  <Col span={8}>
                    <Statistic
                      title="port"
                      value={serviceStatus.port}
                    />
                  </Col>
                  <Col span={8}>
                    <Statistic
                      title="EN"
                      value={serviceStatus.uptime}
                    />
                  </Col>
                </Row>
              </>
            )}

            <Divider />
            <Button 
              icon={<ReloadOutlined />}
              onClick={() => {
                loadSystemInfo();
                loadServiceStatus();
              }}
            >
              Refreshinfo
            </Button>
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default DesktopSettings;
