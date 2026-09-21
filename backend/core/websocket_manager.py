"""
WebSocketconnecttranslated
translatedWebSocketconnectAndtranslated
"""

import json
import logging
import asyncio
from typing import Dict, Set, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """WebSocketconnecttranslated"""
    
    def __init__(self):
        # translatedconnect
        self.active_connections: Dict[str, WebSocket] = {}
        # translatedusertranslated'stranslated
        self.user_subscriptions: Dict[str, Set[str]] = {}
        # translated
        self.topic_subscribers: Dict[str, Set[str]] = {}
        # translatedAndtask
        self.send_queues: Dict[str, asyncio.Queue] = {}
        self.send_tasks: Dict[str, asyncio.Task] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """translatedWebSocketconnect"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_subscriptions[user_id] = set()
        
        # createtranslatedAndtask
        self.send_queues[user_id] = asyncio.Queue()
        self.send_tasks[user_id] = asyncio.create_task(
            self._send_worker(user_id)
        )
        
        logger.info(f"user {user_id} translatedconnect")
    
    async def disconnect(self, user_id: str):
        """translatedWebSocketconnect"""
        # translatedtask
        if user_id in self.send_tasks:
            task = self.send_tasks[user_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.send_tasks[user_id]
        
        # cleantranslated
        if user_id in self.send_queues:
            del self.send_queues[user_id]
        
        # cleanconnect
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_subscriptions:
            del self.user_subscriptions[user_id]
        
        # fromtranslateduser
        for topic in self.topic_subscribers:
            self.topic_subscribers[topic].discard(user_id)
        
        logger.info(f"user {user_id} translatedconnect")
    
    async def _send_worker(self, user_id: str):
        """translated - fromtranslatedcanceltranslated"""
        try:
            while True:
                message = await self.send_queues[user_id].get()
                if message is None:  # translated
                    break
                
                if user_id in self.active_connections:
                    try:
                        await self.active_connections[user_id].send_text(json.dumps(message))
                    except Exception as e:
                        logger.error(f"translateduser {user_id} failed: {e}")
                        break
                
                self.send_queues[user_id].task_done()
        except asyncio.CancelledError:
            logger.debug(f"user {user_id} translatedcancel")
        except Exception as e:
            logger.error(f"user {user_id} translated: {e}")

    async def send_personal_message(self, message: Dict[str, Any], user_id: str):
        """translated translated - translated"""
        if user_id in self.send_queues:
            try:
                await self.send_queues[user_id].put(message)
            except Exception as e:
                logger.error(f"translatedfailed {user_id}: {e}")
                await self.disconnect(user_id)
    
    async def broadcast(self, message: Dict[str, Any]):
        """translatedconnect"""
        disconnected_users = []
        for user_id in list(self.active_connections.keys()):
            try:
                await self.send_personal_message(message, user_id)
            except Exception as e:
                logger.error(f"translateduser {user_id} failed: {e}")
                disconnected_users.append(user_id)
        
        # cleantranslated'sconnect
        for user_id in disconnected_users:
            self.disconnect(user_id)
    
    async def broadcast_to_topic(self, message: Dict[str, Any], topic: str):
        """translated'stranslated"""
        if topic not in self.topic_subscribers:
            return
        
        disconnected_users = []
        for user_id in list(self.topic_subscribers[topic]):
            if user_id in self.active_connections:
                try:
                    await self.send_personal_message(message, user_id)
                except Exception as e:
                    logger.error(f"translateduser {user_id} failed: {e}")
                    disconnected_users.append(user_id)
        
        # cleantranslated'sconnect
        for user_id in disconnected_users:
            self.disconnect(user_id)
    
    def subscribe_to_topic(self, user_id: str, topic: str):
        """usertranslated"""
        if user_id not in self.user_subscriptions:
            self.user_subscriptions[user_id] = set()
        
        self.user_subscriptions[user_id].add(topic)
        
        if topic not in self.topic_subscribers:
            self.topic_subscribers[topic] = set()
        
        self.topic_subscribers[topic].add(user_id)
        logger.info(f"user {user_id} translated {topic}")
    
    def unsubscribe_from_topic(self, user_id: str, topic: str):
        """usercanceltranslated"""
        if user_id in self.user_subscriptions:
            self.user_subscriptions[user_id].discard(topic)
        
        if topic in self.topic_subscribers:
            self.topic_subscribers[topic].discard(user_id)
        
        logger.info(f"user {user_id} canceltranslated {topic}")
    
    def get_connection_count(self) -> int:
        """fetchtranslatedconnecttranslated"""
        return len(self.active_connections)
    
    def get_topic_subscriber_count(self, topic: str) -> int:
        """fetchtranslated"""
        return len(self.topic_subscribers.get(topic, set()))

# translatedconnecttranslated
manager = ConnectionManager()

class WebSocketMessage:
    """WebSockettranslatedtooltranslated"""
    
    @staticmethod
    def create_task_update(task_id: str, status: str, progress: Optional[int] = None, 
                          message: Optional[str] = None, error: Optional[str] = None) -> Dict[str, Any]:
        """createtaskupdatetranslated"""
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
        """createSystemtranslated"""
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
        """createprojectupdatetranslated"""
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
        """createerrortranslated"""
        return {
            "type": "error_notification",
            "error_type": error_type,
            "error_message": error_message,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        } 