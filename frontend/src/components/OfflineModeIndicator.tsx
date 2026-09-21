import React, { useState, useEffect } from 'react';
import { Badge, Tooltip, Button, Space, Typography } from 'antd';
import { 
  WifiOutlined, 
  WifiOutlined as WifiDisconnectedOutlined,
  ReloadOutlined
} from '@ant-design/icons';

const { Text } = Typography;

interface NetworkStatus {
  isOnline: boolean;
  lastCheck: string;
  connectionQuality: 'excellent' | 'good' | 'poor' | 'offline';
  latency?: number;
}

interface OfflineModeIndicatorProps {
  onStatusChange?: (status: NetworkStatus) => void;
}

const OfflineModeIndicator: React.FC<OfflineModeIndicatorProps> = ({ onStatusChange }) => {
  const [networkStatus, setNetworkStatus] = useState<NetworkStatus>({
    isOnline: navigator.onLine,
    lastCheck: new Date().toISOString(),
    connectionQuality: navigator.onLine ? 'good' : 'offline'
  });
  const [isChecking, setIsChecking] = useState(false);

  // checktranslatedconnecttranslated
  const checkConnectionQuality = async (): Promise<NetworkStatus> => {
    const startTime = Date.now();
    
    try {
      // translatedHealth Checktranslated
      const response = await fetch('/health', {
        method: 'GET',
        timeout: 5000
      } as any);
      
      const latency = Date.now() - startTime;
      
      if (response.ok) {
        let quality: 'excellent' | 'good' | 'poor' = 'good';
        if (latency < 100) quality = 'excellent';
        else if (latency > 500) quality = 'poor';
        
        return {
          isOnline: true,
          lastCheck: new Date().toISOString(),
          connectionQuality: quality,
          latency
        };
      } else {
        return {
          isOnline: false,
          lastCheck: new Date().toISOString(),
          connectionQuality: 'offline'
        };
      }
    } catch (error) {
      return {
        isOnline: false,
        lastCheck: new Date().toISOString(),
        connectionQuality: 'offline'
      };
    }
  };

  // translatedchecktranslatedstatus
  const handleCheckNetwork = async () => {
    setIsChecking(true);
    try {
      const status = await checkConnectionQuality();
      setNetworkStatus(status);
      onStatusChange?.(status);
    } catch (error) {
      console.error('translatedcheckfailed:', error);
    } finally {
      setIsChecking(false);
    }
  };

  // translatedstatustranslated
  useEffect(() => {
    const handleOnline = () => {
      setNetworkStatus(prev => ({
        ...prev,
        isOnline: true,
        connectionQuality: 'good',
        lastCheck: new Date().toISOString()
      }));
    };

    const handleOffline = () => {
      setNetworkStatus(prev => ({
        ...prev,
        isOnline: false,
        connectionQuality: 'offline',
        lastCheck: new Date().toISOString()
      }));
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // translatedchecktranslated
    const interval = setInterval(() => {
      if (navigator.onLine) {
        checkConnectionQuality().then(status => {
          setNetworkStatus(status);
          onStatusChange?.(status);
        });
      }
    }, 30000); // per30secondscheckonetranslated

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      clearInterval(interval);
    };
  }, [onStatusChange]);

  // fetchstatustranslatedAndtranslated
  const getStatusIcon = () => {
    if (!networkStatus.isOnline) {
      return <WifiDisconnectedOutlined style={{ color: '#ff4d4f' }} />;
    }
    
    switch (networkStatus.connectionQuality) {
      case 'excellent':
        return <WifiOutlined style={{ color: '#52c41a' }} />;
      case 'good':
        return <WifiOutlined style={{ color: '#1890ff' }} />;
      case 'poor':
        return <WifiOutlined style={{ color: '#faad14' }} />;
      default:
        return <WifiOutlined style={{ color: '#d9d9d9' }} />;
    }
  };

  // fetchstatustranslated
  const getStatusText = () => {
    if (!networkStatus.isOnline) {
      return 'translated';
    }
    
    switch (networkStatus.connectionQuality) {
      case 'excellent':
        return 'translated';
      case 'good':
        return 'translated';
      case 'poor':
        return 'translated';
      default:
        return 'translated';
    }
  };

  // fetchstatustranslated
  const getStatusDescription = () => {
    if (!networkStatus.isOnline) {
      return 'translated，translatedfeaturecantranslated';
    }
    
    const latencyText = networkStatus.latency ? `translated: ${networkStatus.latency}ms` : '';
    const lastCheck = new Date(networkStatus.lastCheck).toLocaleTimeString();
    
    return `translatedcheck: ${lastCheck} ${latencyText}`.trim();
  };

  return (
    <Space>
      <Tooltip title={getStatusDescription()}>
        <Badge 
          status={networkStatus.isOnline ? 'success' : 'error'} 
          text={
            <Space>
              {getStatusIcon()}
              <Text type={networkStatus.isOnline ? 'success' : 'danger'}>
                {getStatusText()}
              </Text>
            </Space>
          }
        />
      </Tooltip>
      
      <Button
        type="text"
        size="small"
        icon={<ReloadOutlined spin={isChecking} />}
        onClick={handleCheckNetwork}
        loading={isChecking}
        title="checktranslatedstatus"
        style={{
          color: '#ffffff',
          border: '1px solid transparent',
          borderRadius: '6px',
          height: '32px',
          width: '32px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transition: 'all 0.2s ease',
          backgroundColor: 'transparent'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.1)'
          e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.2)'
          e.currentTarget.style.transform = 'scale(1.05)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.backgroundColor = 'transparent'
          e.currentTarget.style.borderColor = 'transparent'
          e.currentTarget.style.transform = 'scale(1)'
        }}
        onMouseDown={(e) => {
          e.currentTarget.style.transform = 'scale(0.95)'
        }}
        onMouseUp={(e) => {
          e.currentTarget.style.transform = 'scale(1.05)'
        }}
      />
    </Space>
  );
};

export default OfflineModeIndicator;
