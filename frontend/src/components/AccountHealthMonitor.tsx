import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  Tag,
  Button,
  Space,
  Tooltip,
  Progress,
  Modal,
  message,
  Statistic,
  Row,
  Col,
  Alert,
  Spin,
  Badge
} from 'antd';
import {
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  CloseCircleOutlined,
  QuestionCircleOutlined,
  ReloadOutlined,
  SettingOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';
// translateddate-fnsdependencies，useBuilt-intranslated

// translated
interface AccountHealth {
  account_id: number;
  username: string;
  status: 'healthy' | 'warning' | 'critical' | 'unknown';
  message: string;
  details: {
    cookie?: {
      status: string;
      message: string;
      expires_in?: number;
    };
    login?: {
      status: string;
      message: string;
      user_info?: {
        uname: string;
        mid: number;
        level: number;
      };
    };
    upload?: {
      status: string;
      message: string;
    };
  };
  last_check: string;
  expires_in?: number;
}

interface HealthSummary {
  total_accounts: number;
  healthy_count: number;
  warning_count: number;
  critical_count: number;
  unknown_count: number;
  accounts: AccountHealth[];
  last_updated: string;
}

interface AccountHealthMonitorProps {
  onRefresh?: () => void;
}

const AccountHealthMonitor: React.FC<AccountHealthMonitorProps> = () => {
  const [healthData, setHealthData] = useState<HealthSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState<number[]>([]);
  const [detailsVisible, setDetailsVisible] = useState(false);
  const [selectedAccount, setSelectedAccount] = useState<AccountHealth | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [refreshInterval, setRefreshInterval] = useState<number | null>(null);

  // translatedformattranslated
  const getTimeAgo = (dateString: string) => {
    const now = new Date();
    const date = new Date(dateString);
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
    
    if (diffInSeconds < 60) {
      return 'translated';
    } else if (diffInSeconds < 3600) {
      const minutes = Math.floor(diffInSeconds / 60);
      return `${minutes}minutestranslated`;
    } else if (diffInSeconds < 86400) {
      const hours = Math.floor(diffInSeconds / 3600);
      return `${hours}translated`;
    } else {
      const days = Math.floor(diffInSeconds / 86400);
      return `${days}translated`;
    }
  };

  // fetchtranslatedstatustranslated
  const fetchHealthSummary = async (forceCheck = false) => {
    try {
      setLoading(true);
      const endpoint = forceCheck ? '/health/check' : '/health/summary';
      const method = forceCheck ? 'POST' : 'GET';
      const body = forceCheck ? JSON.stringify({ force_check: true }) : undefined;
      
      const response = await fetch(endpoint, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const data = await response.json();
      setHealthData(data);
      
      if (forceCheck) {
        message.success('Health Checktranslated');
      }
    } catch (error) {
      console.error('fetchtranslatedstatusfailed:', error);
      message.error('fetchtranslatedstatusfailed');
    } finally {
      setLoading(false);
    }
  };

  // checktranslated Account
  const checkSingleAccount = async (accountId: number, forceCheck = true) => {
    try {
      setRefreshing(prev => [...prev, accountId]);
      
      const response = await fetch(`/api/v1/health/check/${accountId}?force_check=${forceCheck}`, {
        method: 'GET',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const updatedAccount = await response.json();
      
      // updatetranslated
      setHealthData(prev => {
        if (!prev) return prev;
        
        const updatedAccounts = prev.accounts.map(account => 
          account.account_id === accountId ? updatedAccount : account
        );
        
        // translated
        const statusCounts = {
          healthy: 0,
          warning: 0,
          critical: 0,
          unknown: 0
        };
        
        updatedAccounts.forEach(account => {
          statusCounts[account.status as keyof typeof statusCounts]++;
        });
        
        return {
          ...prev,
          accounts: updatedAccounts,
          healthy_count: statusCounts.healthy,
          warning_count: statusCounts.warning,
          critical_count: statusCounts.critical,
          unknown_count: statusCounts.unknown,
          last_updated: new Date().toISOString()
        };
      });
      
      message.success(`Account ${updatedAccount.username} checktranslated`);
    } catch (error) {
      console.error('checkAccountfailed:', error);
      message.error('checkAccountfailed');
    } finally {
      setRefreshing(prev => prev.filter(id => id !== accountId));
    }
  };

  // translatedCookie
  const refreshCookie = async (accountId: number) => {
    try {
      const response = await fetch('/health/refresh-cookie', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          account_id: accountId,
          auto_refresh: true
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.success) {
        message.success(result.message);
      } else {
        message.warning(result.message);
      }
    } catch (error) {
      console.error('translatedCookiefailed:', error);
      message.error('translatedCookiefailed');
    }
  };

  // fetchstatustranslated
  const getStatusTag = (status: string) => {
    const statusConfig = {
      healthy: { color: 'success', icon: <CheckCircleOutlined />, text: 'translated' },
      warning: { color: 'warning', icon: <ExclamationCircleOutlined />, text: 'translated' },
      critical: { color: 'error', icon: <CloseCircleOutlined />, text: 'translated' },
      unknown: { color: 'default', icon: <QuestionCircleOutlined />, text: 'translated' }
    };
    
    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.unknown;
    
    return (
      <Tag color={config.color} icon={config.icon}>
        {config.text}
      </Tag>
    );
  };

  // fetchtranslatedprogresstranslated
  const getExpirationProgress = (expiresIn?: number) => {
    if (expiresIn === undefined || expiresIn === null) {
      return null;
    }
    
    const totalDays = 30; // translatedCookietranslated30translated
    const percentage = Math.max(0, Math.min(100, (expiresIn / totalDays) * 100));
    
    let status: 'success' | 'normal' | 'exception' = 'success';
    if (expiresIn <= 0) {
      status = 'exception';
    } else if (expiresIn <= 7) {
      status = 'normal';
    }
    
    return (
      <Tooltip title={`translated ${expiresIn} translated`}>
        <Progress
          percent={percentage}
          status={status}
          size="small"
          showInfo={false}
          strokeWidth={6}
        />
      </Tooltip>
    );
  };

  // translated
  const columns = [
    {
      title: 'Account',
      dataIndex: 'username',
      key: 'username',
      render: (username: string, record: AccountHealth) => (
        <Space>
          <span>{username}</span>
          {record.details.login?.user_info && (
            <Tooltip title={`etc.translated: ${record.details.login.user_info.level}`}>
              <Badge count={record.details.login.user_info.level} color="blue" />
            </Tooltip>
          )}
        </Space>
      ),
    },
    {
      title: 'translatedstatus',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => getStatusTag(status),
    },
    {
      title: 'Cookiestatus',
      key: 'cookie_status',
      render: (record: AccountHealth) => (
        <Space direction="vertical" size="small">
          {getStatusTag(record.details.cookie?.status || 'unknown')}
          {getExpirationProgress(record.expires_in)}
        </Space>
      ),
    },
    {
      title: 'translatedcheck',
      dataIndex: 'last_check',
      key: 'last_check',
      render: (lastCheck: string) => (
        <Tooltip title={new Date(lastCheck).toLocaleString()}>
          <Space>
            <ClockCircleOutlined />
            {getTimeAgo(lastCheck)}
          </Space>
        </Tooltip>
      ),
    },
    {
      title: 'translated',
      key: 'actions',
      render: (record: AccountHealth) => (
        <Space>
          <Button
            type="text"
            icon={<ReloadOutlined />}
            loading={refreshing.includes(record.account_id)}
            onClick={() => checkSingleAccount(record.account_id)}
          >
            check
          </Button>
          <Button
            type="text"
            icon={<SettingOutlined />}
            onClick={() => {
              setSelectedAccount(record);
              setDetailsVisible(true);
            }}
          >
            translated
          </Button>
          {record.status === 'critical' || record.status === 'warning' ? (
            <Button
              type="text"
              danger
              onClick={() => refreshCookie(record.account_id)}
            >
              translatedCookie
            </Button>
          ) : null}
        </Space>
      ),
    },
  ];

  // translatedfetchtranslated
  useEffect(() => {
    fetchHealthSummary();
  }, []);

  // translated
  useEffect(() => {
    if (autoRefresh) {
      const interval = window.setInterval(() => {
        fetchHealthSummary();
      }, 60000); // perminutestranslatedonetranslated
      setRefreshInterval(interval);
    } else {
      if (refreshInterval) {
        clearInterval(refreshInterval);
        setRefreshInterval(null);
      }
    }
    
    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, [autoRefresh]);

  return (
    <div>
      {/* translated */}
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="translatedAccounttranslated"
              value={healthData?.total_accounts || 0}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="translatedAccount"
              value={healthData?.healthy_count || 0}
              valueStyle={{ color: '#3f8600' }}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="translatedAccount"
              value={healthData?.warning_count || 0}
              valueStyle={{ color: '#cf1322' }}
              prefix={<ExclamationCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="translatedissue"
              value={healthData?.critical_count || 0}
              valueStyle={{ color: '#cf1322' }}
              prefix={<CloseCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* translated */}
      <Card style={{ marginBottom: 16 }}>
        <Space>
          <Button
            type="primary"
            icon={<ReloadOutlined />}
            loading={loading}
            onClick={() => fetchHealthSummary(true)}
          >
            translatedcheck
          </Button>
          <Button
            icon={<ReloadOutlined />}
            loading={loading}
            onClick={() => fetchHealthSummary()}
          >
            translatedstatus
          </Button>
          <Button
            type={autoRefresh ? 'primary' : 'default'}
            onClick={() => setAutoRefresh(!autoRefresh)}
          >
            {autoRefresh ? 'translated' : 'translated'}
          </Button>
        </Space>
        
        {healthData?.last_updated && (
          <div style={{ float: 'right', color: '#666' }}>
            translatedupdate: {getTimeAgo(healthData.last_updated)}
          </div>
        )}
      </Card>

      {/* translatedinfo */}
      {healthData && (healthData.critical_count > 0 || healthData.warning_count > 0) && (
        <Alert
          message="Accounttranslated"
          description={`translated ${healthData.critical_count}  translatedissueAnd ${healthData.warning_count}  translated，translatedprocess`}
          type="warning"
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}

      {/* Accountlist */}
      <Card title="Accounttranslatedstatus">
        <Spin spinning={loading}>
          <Table
            columns={columns}
            dataSource={healthData?.accounts || []}
            rowKey="account_id"
            pagination={{
              pageSize: 10,
              showSizeChanger: true,
              showQuickJumper: true,
              showTotal: (total) => `translated ${total}  Account`,
            }}
          />
        </Spin>
      </Card>

      {/* translated */}
      <Modal
        title={`Accounttranslated - ${selectedAccount?.username}`}
        open={detailsVisible}
        onCancel={() => setDetailsVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailsVisible(false)}>
            translated
          </Button>,
          <Button
            key="refresh"
            type="primary"
            icon={<ReloadOutlined />}
            onClick={() => {
              if (selectedAccount) {
                checkSingleAccount(selectedAccount.account_id);
              }
            }}
          >
            translatedcheck
          </Button>,
        ]}
        width={600}
      >
        {selectedAccount && (
          <div>
            <Row gutter={16}>
              <Col span={12}>
                <Card title="translatedinfo" size="small">
                  <p><strong>AccountID:</strong> {selectedAccount.account_id}</p>
                  <p><strong>usertranslated:</strong> {selectedAccount.username}</p>
                  <p><strong>translatedstatus:</strong> {getStatusTag(selectedAccount.status)}</p>
                  <p><strong>statustranslated:</strong> {selectedAccount.message}</p>
                </Card>
              </Col>
              <Col span={12}>
                <Card title="checktranslated" size="small">
                  <p><strong>translatedcheck:</strong> {new Date(selectedAccount.last_check).toLocaleString()}</p>
                  {selectedAccount.expires_in !== undefined && (
                    <p><strong>Cookietranslated:</strong> {selectedAccount.expires_in} translated</p>
                  )}
                </Card>
              </Col>
            </Row>
            
            <Card title="translatedstatus" size="small" style={{ marginTop: 16 }}>
              {selectedAccount.details.cookie && (
                <div style={{ marginBottom: 12 }}>
                  <strong>Cookiestatus:</strong> {getStatusTag(selectedAccount.details.cookie.status)}
                  <p>{selectedAccount.details.cookie.message}</p>
                </div>
              )}
              
              {selectedAccount.details.login && (
                <div style={{ marginBottom: 12 }}>
                  <strong>translatedstatus:</strong> {getStatusTag(selectedAccount.details.login.status)}
                  <p>{selectedAccount.details.login.message}</p>
                  {selectedAccount.details.login.user_info && (
                    <p>userinfo: {selectedAccount.details.login.user_info.uname} (etc.translated {selectedAccount.details.login.user_info.level})</p>
                  )}
                </div>
              )}
              
              {selectedAccount.details.upload && (
                <div>
                  <strong>Uploadtranslated:</strong> {getStatusTag(selectedAccount.details.upload.status)}
                  <p>{selectedAccount.details.upload.message}</p>
                </div>
              )}
            </Card>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default AccountHealthMonitor;