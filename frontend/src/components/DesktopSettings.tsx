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

  // translatedconfig
  const loadConfig = async () => {
    try {
      const response = await fetch('/api/v1/desktop/config');
      if (response.ok) {
        const data = await response.json();
        setConfig(data.config);
        form.setFieldsValue(data.config);
      } else {
        message.error('translatedconfigfailed');
      }
    } catch (error) {
      console.error('translatedconfigerror:', error);
      message.error('translatedconfigfailed');
    }
  };

  // translatedSysteminfo
  const loadSystemInfo = async () => {
    try {
      const response = await fetch('/api/v1/desktop/system/info');
      if (response.ok) {
        const data = await response.json();
        setSystemInfo(data);
      }
    } catch (error) {
      console.error('translatedSysteminfofailed:', error);
    }
  };

  // translatedservicestatus
  const loadServiceStatus = async () => {
    try {
      const response = await fetch('/api/v1/desktop/service/status');
      if (response.ok) {
        const data = await response.json();
        setServiceStatus(data);
      }
    } catch (error) {
      console.error('translatedservicestatusfailed:', error);
    }
  };

  // translatedconfig
  const saveConfig = async (values: DesktopConfig) => {
    setLoading(true);
    try {
      // translatedbackendtranslated'sDesktopConfigtranslated
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
        message.success('configtranslatedsucceeded');
        setConfig(configData);
      } else {
        const errorData = await response.json();
        message.error(`configtranslatedfailed: ${errorData.detail || 'translatederror'}`);
      }
    } catch (error) {
      console.error('configtranslatederror:', error);
      message.error('configtranslatedfailed');
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
        <SettingOutlined /> translatedsettings
      </Title>
      
      <Tabs defaultActiveKey="basic">
        {/* translatedsettings */}
        <TabPane tab={<span><SettingOutlined />translatedsettings</span>} key="basic">
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
                    label="translatedusetranslated"
                    rules={[{ required: true, message: 'translatedusetranslated' }]}
                  >
                    <Input />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="app_version"
                    label="translateduseversion"
                    rules={[{ required: true, message: 'translateduseversion' }]}
                  >
                    <Input />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item
                name="debug_mode"
                label="translated"
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
                    label="translated"
                    rules={[{ required: true, message: 'translated' }]}
                  >
                    <Input />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="port"
                    label="translated"
                    rules={[{ required: true, message: 'translated' }]}
                  >
                    <InputNumber min={1} max={65535} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item
                name="max_memory_usage"
                label="translateduse (MB)"
                rules={[{ required: true, message: 'translateduse' }]}
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
                    translatedconfig
                  </Button>
                  <Button 
                    icon={<ReloadOutlined />}
                    onClick={loadConfig}
                  >
                    translated
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
              <Title level={4}>APIkey</Title>
              <Form.Item
                name="dashscope_api_key"
                label="DashScope API Key"
              >
                <Input.Password placeholder="translatedDashScope API Key" />
              </Form.Item>

              <Form.Item
                name="openai_api_key"
                label="OpenAI API Key"
              >
                <Input.Password placeholder="translatedOpenAI API Key" />
              </Form.Item>

              <Form.Item
                name="gemini_api_key"
                label="Gemini API Key"
              >
                <Input.Password placeholder="translatedGemini API Key" />
              </Form.Item>

              <Form.Item
                name="siliconflow_api_key"
                label="SiliconFlow API Key"
              >
                <Input.Password placeholder="translatedSiliconFlow API Key" />
              </Form.Item>

              <Divider />

              <Title level={4}>modelconfig</Title>
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    name="default_model"
                    label="defaultmodel"
                    rules={[{ required: true, message: 'translateddefaultmodel' }]}
                  >
                    <Input />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="max_tokens"
                    label="translatedTokentranslated"
                    rules={[{ required: true, message: 'translatedTokentranslated' }]}
                  >
                    <InputNumber min={100} max={8000} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item
                name="timeout"
                label="translated (seconds)"
                rules={[{ required: true, message: 'translated' }]}
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
                  translatedconfig
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>

        {/* processsettings */}
        <TabPane tab={<span><ToolOutlined />processsettings</span>} key="processing">
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
                    label="translated"
                    rules={[{ required: true, message: 'translated' }]}
                  >
                    <InputNumber min={1000} max={10000} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="min_score_threshold"
                    label="translated"
                    rules={[{ required: true, message: 'translated' }]}
                  >
                    <InputNumber min={0.1} max={1.0} step={0.1} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    name="max_clips_per_collection"
                    label="per collectiontranslated"
                    rules={[{ required: true, message: 'translated' }]}
                  >
                    <InputNumber min={1} max={20} style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="max_retries"
                    label="translated"
                    rules={[{ required: true, message: 'translated' }]}
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
                  translatedconfig
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>

        {/* Systeminfo */}
        <TabPane tab={<span><DatabaseOutlined />Systeminfo</span>} key="system">
          <Card>
            {systemInfo && (
              <Row gutter={16}>
                <Col span={8}>
                  <Statistic
                    title="translatedSystem"
                    value={systemInfo.platform}
                    suffix={systemInfo.platform_version}
                  />
                </Col>
                <Col span={8}>
                  <Statistic
                    title="translated"
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
                      title="translated"
                      value={formatBytes(systemInfo.memory_total)}
                    />
                  </Col>
                  <Col span={12}>
                    <Statistic
                      title="canusetranslated"
                      value={formatBytes(systemInfo.memory_available)}
                    />
                  </Col>
                </Row>
                <Row gutter={16}>
                  <Col span={12}>
                    <Statistic
                      title="translatedusetranslated"
                      value={systemInfo.memory_usage_percent}
                      suffix="%"
                    />
                  </Col>
                  <Col span={12}>
                    <Statistic
                      title="translatedusetranslated"
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
                <Title level={4}>servicestatus</Title>
                <Row gutter={16}>
                  <Col span={8}>
                    <Statistic
                      title="servicestatus"
                      value={serviceStatus.is_running ? "translated" : "translated"}
                      valueStyle={{ color: serviceStatus.is_running ? '#3f8600' : '#cf1322' }}
                    />
                  </Col>
                  <Col span={8}>
                    <Statistic
                      title="translated"
                      value={serviceStatus.port}
                    />
                  </Col>
                  <Col span={8}>
                    <Statistic
                      title="Runtimetranslated"
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
              translatedinfo
            </Button>
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default DesktopSettings;
