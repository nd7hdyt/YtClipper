import { useState, useCallback, useRef } from 'react';
import { SystemNotificationMessage, ErrorNotificationMessage } from './useWebSocket';

export interface Notification {
  id: string;
  type: 'system' | 'error';
  title: string;
  message: string;
  level: 'info' | 'success' | 'warning' | 'error';
  timestamp: string;
  read: boolean;
}

export const useNotifications = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const notifiedKeys = useRef<Set<string>>(new Set()); // EN
  const lastNotificationTime = useRef<number>(0); // EN

  const addNotification = useCallback((notification: Omit<Notification, 'id' | 'read'>, forceAdd = false) => {
    const now = Date.now();
    const key = `${notification.type}-${notification.title}-${notification.message}`;
    
    // EN：EN，ENadd
    if (!forceAdd && notifiedKeys.current.has(key)) {
      return;
    }
    
    // EN：EN3EN
    if (!forceAdd && now - lastNotificationTime.current < 3000) {
      return;
    }
    
    const newNotification: Notification = {
      ...notification,
      id: `${Date.now()}-${Math.random()}`,
      read: false
    };

    setNotifications(prev => [newNotification, ...prev.slice(0, 49)]); // EN50EN
    setUnreadCount(prev => prev + 1);
    
    // ENkeyEN
    notifiedKeys.current.add(key);
    lastNotificationTime.current = now;
  }, []);

  const markAsRead = useCallback((notificationId: string) => {
    setNotifications(prev => 
      prev.map(notification => 
        notification.id === notificationId 
          ? { ...notification, read: true }
          : notification
      )
    );
    setUnreadCount(prev => Math.max(0, prev - 1));
  }, []);

  const markAllAsRead = useCallback(() => {
    setNotifications(prev => 
      prev.map(notification => ({ ...notification, read: true }))
    );
    setUnreadCount(0);
  }, []);

  const removeNotification = useCallback((notificationId: string) => {
    setNotifications(prev => {
      const safePrev = Array.isArray(prev) ? prev : [];
      const notification = safePrev.find(n => n.id === notificationId);
      if (notification && !notification.read) {
        setUnreadCount(count => Math.max(0, count - 1));
      }
      return safePrev.filter(n => n.id !== notificationId);
    });
  }, []);

  const clearAll = useCallback(() => {
    setNotifications([]);
    setUnreadCount(0);
  }, []);

  const handleSystemNotification = useCallback((message: SystemNotificationMessage) => {
    addNotification({
      type: 'system',
      title: message.title,
      message: message.message,
      level: message.level,
      timestamp: message.timestamp
    });
  }, [addNotification]);

  const handleErrorNotification = useCallback((message: ErrorNotificationMessage) => {
    addNotification({
      type: 'error',
      title: `Error: ${message.error_type}`,
      message: message.error_message,
      level: 'error',
      timestamp: message.timestamp
    });
  }, [addNotification]);

  const getNotificationsByLevel = useCallback((level: Notification['level']) => {
    return (notifications || []).filter(n => n.level === level);
  }, [notifications]);

  const getUnreadNotifications = useCallback(() => {
    return (notifications || []).filter(n => !n.read);
  }, [notifications]);

  const getReadNotifications = useCallback(() => {
    return (notifications || []).filter(n => n.read);
  }, [notifications]);

  return {
    notifications,
    unreadCount,
    addNotification,
    markAsRead,
    markAllAsRead,
    removeNotification,
    clearAll,
    handleSystemNotification,
    handleErrorNotification,
    getNotificationsByLevel,
    getUnreadNotifications,
    getReadNotifications
  };
}; 