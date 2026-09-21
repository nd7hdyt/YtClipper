"""
WebSocketconnectEN
ENWebSocketconnectEN
"""

import json
import logging
import asyncio
from typing import Dict, Set, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """WebSocketconnectEN"""
    
    def __init__(self):
        # ENallENconnect
        self.active_connections: Dict[str, WebSocket] = {}
        # ENuserEN
        self.user_subscriptions: Dict[str, Set[str]] = {}
        # EN
        self.topic_subscribers: Dict[str, Set[str]] = {}
        # sendqueueENtask
        self.send_queues: Dict[str, asyncio.Queue] = {}
        self.send_tasks: Dict[str, asyncio.Task] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """ENWebSocketconnect"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_subscriptions[user_id] = set()
        
        # createsendqueueENtask
        self.send_queues[user_id] = asyncio.Queue()
        self.send_tasks[user_id] = asyncio.create_task(
            self._send_worker(user_id)
        )
        
        logger.info(f"user {user_id} ENconnect")
    
    async def disconnect(self, user_id: str):
        """disconnectWebSocketconnect"""
        # stopsendtask
        if user_id in self.send_tasks:
            task = self.send_tasks[user_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.send_tasks[user_id]
        
        # ENqueue
        if user_id in self.send_queues:
            del self.send_queues[user_id]
        
        # ENconnect
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_subscriptions:
            del self.user_subscriptions[user_id]
        
        # ENallENuser
        for topic in self.topic_subscribers:
            self.topic_subscribers[topic].discard(user_id)
        
        logger.info(f"user {user_id} ENdisconnectconnect")
    
    async def _send_worker(self, user_id: str):
        """sendEN - ENqueueENcancelENsend"""
        try:
            while True:
                message = await self.send_queues[user_id].get()
                if message is None:  # stopEN
                    break
                
                if user_id in self.active_connections:
                    try:
                        await self.active_connections[user_id].send_text(json.dumps(message))
                    except Exception as e:
                        logger.error(f"sendENuser {user_id} failed: {e}")
                        break
                
                self.send_queues[user_id].task_done()
        except asyncio.CancelledError:
            logger.debug(f"user {user_id} sendENcancel")
        except Exception as e:
            logger.error(f"user {user_id} sendENexception: {e}")

    async def send_personal_message(self, message: Dict[str, Any], user_id: str):
        """sendEN - queueENsend"""
        if user_id in self.send_queues:
            try:
                await self.send_queues[user_id].put(message)
            except Exception as e:
                logger.error(f"ENqueuefailed {user_id}: {e}")
                await self.disconnect(user_id)
    
    async def broadcast(self, message: Dict[str, Any]):
        """ENallconnect"""
        disconnected_users = []
        for user_id in list(self.active_connections.keys()):
            try:
                await self.send_personal_message(message, user_id)
            except Exception as e:
                logger.error(f"ENuser {user_id} failed: {e}")
                disconnected_users.append(user_id)
        
        # ENdisconnectENconnect
        for user_id in disconnected_users:
            self.disconnect(user_id)
    
    async def broadcast_to_topic(self, message: Dict[str, Any], topic: str):
        """EN"""
        if topic not in self.topic_subscribers:
            return
        
        disconnected_users = []
        for user_id in list(self.topic_subscribers[topic]):
            if user_id in self.active_connections:
                try:
                    await self.send_personal_message(message, user_id)
                except Exception as e:
                    logger.error(f"sendENuser {user_id} failed: {e}")
                    disconnected_users.append(user_id)
        
        # ENdisconnectENconnect
        for user_id in disconnected_users:
            self.disconnect(user_id)
    
    def subscribe_to_topic(self, user_id: str, topic: str):
        """userEN"""
        if user_id not in self.user_subscriptions:
            self.user_subscriptions[user_id] = set()
        
        self.user_subscriptions[user_id].add(topic)
        
        if topic not in self.topic_subscribers:
            self.topic_subscribers[topic] = set()
        
        self.topic_subscribers[topic].add(user_id)
        logger.info(f"user {user_id} EN {topic}")
    
    def unsubscribe_from_topic(self, user_id: str, topic: str):
        """usercancelEN"""
        if user_id in self.user_subscriptions:
            self.user_subscriptions[user_id].discard(topic)
        
        if topic in self.topic_subscribers:
            self.topic_subscribers[topic].discard(user_id)
        
        logger.info(f"user {user_id} cancelEN {topic}")
    
    def get_connection_count(self) -> int:
        """fetchcurrentconnectEN"""
        return len(self.active_connections)
    
    def get_topic_subscriber_count(self, topic: str) -> int:
        """fetchEN"""
        return len(self.topic_subscribers.get(topic, set()))

# ENconnectEN
manager = ConnectionManager()

class WebSocketMessage:
    """WebSocketEN"""
    
    @staticmethod
    def create_task_update(task_id: str, status: str, progress: Optional[int] = None, 
                          message: Optional[str] = None, error: Optional[str] = None) -> Dict[str, Any]:
        """createtaskupdateEN"""
        return {
            "type": "task_update",
            "task_id": task_id,
            "status": status,
            "progress": progress,
            "message": message,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def create_system_notification(notification_type: str, title: str, message: str, 
                                 level: str = "info") -> Dict[str, Any]:
        """createsystemEN"""
        return {
            "type": "system_notification",
            "notification_type": notification_type,
            "title": title,
            "message": message,
            "level": level,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def create_project_update(project_id: str, status: str, progress: Optional[int] = None,
                            message: Optional[str] = None) -> Dict[str, Any]:
        """createprojectupdateEN"""
        return {
            "type": "project_update",
            "project_id": project_id,
            "status": status,
            "progress": progress,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def create_error_notification(error_type: str, error_message: str, 
                                details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """createerrorEN"""
        return {
            "type": "error_notification",
            "error_type": error_type,
            "error_message": error_message,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        } 