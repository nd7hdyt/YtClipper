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
// removedate-fnsEN，EN

// EN
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

  // EN
  const getTimeAgo = (dateString: string) => {
    const now = new Date();
    const date = new Date(dateString);
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
    
    if (diffInSeconds < 60) {
      return 'Just now';
    } else if (diffInSeconds < 3600) {
      const minutes = Math.floor(diffInSeconds / 60);
      return `${minutes} minutes ago`;
    } else if (diffInSeconds < 86400) {
      const hours = Math.floor(diffInSeconds / 3600);
      return `${hours} hours ago`;
    } else {
      const days = Math.floor(diffInSeconds / 86400);
      return `${days}EN`;
    }
  };

  // Fetch healthStatusEN
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
        message.success('Health checkCompleted');
      }
    } catch (error) {
      console.error('Fetch healthStatusFailed:', error);
      message.error('Fetch healthStatusFailed');
    } finally {
      setLoading(false);
    }
  };

  // checkENaccount
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
      
      // updatehealthEN
      setHealthData(prev => {
        if (!prev) return prev;
        
        const updatedAccounts = prev.accounts.map(account => 
          account.account_id === accountId ? updatedAccount : account
        );
        
        // EN
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
      
      message.success(`account ${updatedAccount.username} checkCompleted`);
    } catch (error) {
      console.error('Check accountFailed:', error);
      message.error('Check accountFailed');
    } finally {
      setRefreshing(prev => prev.filter(id => id !== accountId));
    }
  };

  // RefreshCookie
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
      console.error('RefreshCookieFailed:', error);
      message.error('RefreshCookieFailed');
    }
  };

  // Get status tags
  const getStatusTag = (status: string) => {
    const statusConfig = {
      healthy: { color: 'success', icon: <CheckCircleOutlined />, text: 'health' },
      warning: { color: 'warning', icon: <ExclamationCircleOutlined />, text: 'Warning' },
      critical: { color: 'error', icon: <CloseCircleOutlined />, text: 'EN' },
      unknown: { color: 'default', icon: <QuestionCircleOutlined />, text: 'unknown' }
    };
    
    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.unknown;
    
    return (
      <Tag color={config.color} icon={config.icon}>
        {config.text}
      </Tag>
    );
  };

  // fetchENProgressEN
  const getExpirationProgress = (expiresIn?: number) => {
    if (expiresIn === undefined || expiresIn === null) {
      return null;
    }
    
    const totalDays = 30; // ENCookieEN30EN
    const percentage = Math.max(0, Math.min(100, (expiresIn / totalDays) * 100));
    
    let status: 'success' | 'normal' | 'exception' = 'success';
    if (expiresIn <= 0) {
      status = 'exception';
    } else if (expiresIn <= 7) {
      status = 'normal';
    }
    
    return (
      <Tooltip title={`EN ${expiresIn} EN`}>
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

  // Table columns
  const columns = [
    {
      title: 'account',
      dataIndex: 'username',
      key: 'username',
      render: (username: string, record: AccountHealth) => (
        <Space>
          <span>{username}</span>
          {record.details.login?.user_info && (
            <Tooltip title={`Level: ${record.details.login.user_info.level}`}>
              <Badge count={record.details.login.user_info.level} color="blue" />
            </Tooltip>
          )}
        </Space>
      ),
    },
    {
      title: 'healthStatus',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => getStatusTag(status),
    },
    {
      title: 'CookieStatus',
      key: 'cookie_status',
      render: (record: AccountHealth) => (
        <Space direction="vertical" size="small">
          {getStatusTag(record.details.cookie?.status || 'unknown')}
          {getExpirationProgress(record.expires_in)}
        </Space>
      ),
    },
    {
      title: 'Last check',
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
      title: 'Actions',
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
            Details
          </Button>
          {record.status === 'critical' || record.status === 'warning' ? (
            <Button
              type="text"
              danger
              onClick={() => refreshCookie(record.account_id)}
            >
              RefreshCookie
            </Button>
          ) : null}
        </Space>
      ),
    },
  ];

  // ENfetchEN
  useEffect(() => {
    fetchHealthSummary();
  }, []);

  // ENRefresh
  useEffect(() => {
    if (autoRefresh) {
      const interval = window.setInterval(() => {
        fetchHealthSummary();
      }, 60000); // ENRefreshonce
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
      {/* Stats card */}
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="ENaccountEN"
              value={healthData?.total_accounts || 0}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="healthaccount"
              value={healthData?.healthy_count || 0}
              valueStyle={{ color: '#3f8600' }}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Warningaccount"
              value={healthData?.warning_count || 0}
              valueStyle={{ color: '#cf1322' }}
              prefix={<ExclamationCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="EN"
              value={healthData?.critical_count || 0}
              valueStyle={{ color: '#cf1322' }}
              prefix={<CloseCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* ActionsEN */}
      <Card style={{ marginBottom: 16 }}>
        <Space>
          <Button
            type="primary"
            icon={<ReloadOutlined />}
            loading={loading}
            onClick={() => fetchHealthSummary(true)}
          >
            ENcheck
          </Button>
          <Button
            icon={<ReloadOutlined />}
            loading={loading}
            onClick={() => fetchHealthSummary()}
          >
            RefreshStatus
          </Button>
          <Button
            type={autoRefresh ? 'primary' : 'default'}
            onClick={() => setAutoRefresh(!autoRefresh)}
          >
            {autoRefresh ? 'ENRefresh' : 'ENRefresh'}
          </Button>
        </Space>
        
        {healthData?.last_updated && (
          <div style={{ float: 'right', color: '#666' }}>
            ENupdate: {getTimeAgo(healthData.last_updated)}
          </div>
        )}
      </Card>

      {/* Warninginfo */}
      {healthData && (healthData.critical_count > 0 || healthData.warning_count > 0) && (
        <Alert
          message="Account healthWarning"
          description={`EN ${healthData.critical_count} EN ${healthData.warning_count} ENWarning，EN`}
          type="warning"
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}

      {/* accountlist */}
      <Card title="Account healthStatus">
        <Spin spinning={loading}>
          <Table
            columns={columns}
            dataSource={healthData?.accounts || []}
            rowKey="account_id"
            pagination={{
              pageSize: 10,
              showSizeChanger: true,
              showQuickJumper: true,
              showTotal: (total) => `Total ${total} ENaccount`,
            }}
          />
        </Spin>
      </Card>

      {/* Detailsdialog */}
      <Modal
        title={`accountDetails - ${selectedAccount?.username}`}
        open={detailsVisible}
        onCancel={() => setDetailsVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailsVisible(false)}>
            Close
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
            ENcheck
          </Button>,
        ]}
        width={600}
      >
        {selectedAccount && (
          <div>
            <Row gutter={16}>
              <Col span={12}>
                <Card title="ENinfo" size="small">
                  <p><strong>Account ID:</strong> {selectedAccount.account_id}</p>
                  <p><strong>EN:</strong> {selectedAccount.username}</p>
                  <p><strong>ENStatus:</strong> {getStatusTag(selectedAccount.status)}</p>
                  <p><strong>Statusmessage:</strong> {selectedAccount.message}</p>
                </Card>
              </Col>
              <Col span={12}>
                <Card title="checkEN" size="small">
                  <p><strong>Last check:</strong> {new Date(selectedAccount.last_check).toLocaleString()}</p>
                  {selectedAccount.expires_in !== undefined && (
                    <p><strong>CookieEN:</strong> {selectedAccount.expires_in} EN</p>
                  )}
                </Card>
              </Col>
            </Row>
            
            <Card title="ENStatus" size="small" style={{ marginTop: 16 }}>
              {selectedAccount.details.cookie && (
                <div style={{ marginBottom: 12 }}>
                  <strong>CookieStatus:</strong> {getStatusTag(selectedAccount.details.cookie.status)}
                  <p>{selectedAccount.details.cookie.message}</p>
                </div>
              )}
              
              {selectedAccount.details.login && (
                <div style={{ marginBottom: 12 }}>
                  <strong>ENStatus:</strong> {getStatusTag(selectedAccount.details.login.status)}
                  <p>{selectedAccount.details.login.message}</p>
                  {selectedAccount.details.login.user_info && (
                    <p>ENinfo: {selectedAccount.details.login.user_info.uname} (Level {selectedAccount.details.login.user_info.level})</p>
                  )}
                </div>
              )}
              
              {selectedAccount.details.upload && (
                <div>
                  <strong>UploadEN:</strong> {getStatusTag(selectedAccount.details.upload.status)}
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