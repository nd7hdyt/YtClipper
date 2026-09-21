"""
WebSocketENservice
EN
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from ..core.websocket_manager import manager, WebSocketMessage

logger = logging.getLogger(__name__)

class WebSocketNotificationService:
    """WebSocketENservice"""
    
    @staticmethod
    async def send_task_update(task_id: str, status: str, progress: Optional[int] = None,
                              message: Optional[str] = None, error: Optional[str] = None):
        """sendtaskupdateEN"""
        try:
            notification = WebSocketMessage.create_task_update(
                task_id=task_id,
                status=status,
                progress=progress,
                message=message,
                error=error
            )
            
            # ENallconnectENuser
            await manager.broadcast(notification)
            
            # meanwhilesendENtaskEN
            topic = f"task_{task_id}"
            await manager.broadcast_to_topic(notification, topic)
            
            logger.info(f"taskupdateENsend: {task_id} - {status}")
            
        except Exception as e:
            logger.error(f"sendtaskupdateENfailed: {e}")
    
    @staticmethod
    async def send_project_update(project_id: str, status: str, progress: Optional[int] = None,
                                message: Optional[str] = None):
        """sendprojectupdateEN"""
        try:
            notification = WebSocketMessage.create_project_update(
                project_id=project_id,
                status=status,
                progress=progress,
                message=message
            )
            
            # ENallconnectENuser
            await manager.broadcast(notification)
            
            # meanwhilesendENprojectEN
            topic = f"project_{project_id}"
            await manager.broadcast_to_topic(notification, topic)
            
            logger.info(f"projectupdateENsend: {project_id} - {status}")
            
        except Exception as e:
            logger.error(f"sendprojectupdateENfailed: {e}")
    
    @staticmethod
    async def send_system_notification(notification_type: str, title: str, message: str,
                                     level: str = "info"):
        """sendsystemEN"""
        try:
            notification = WebSocketMessage.create_system_notification(
                notification_type=notification_type,
                title=title,
                message=message,
                level=level
            )
            
            # ENallconnectENuser
            await manager.broadcast(notification)
            
            logger.info(f"systemENsend: {title} - {message}")
            
        except Exception as e:
            logger.error(f"sendsystemENfailed: {e}")
    
    @staticmethod
    async def send_error_notification(error_type: str, error_message: str,
                                    details: Optional[Dict[str, Any]] = None):
        """senderrorEN"""
        try:
            notification = WebSocketMessage.create_error_notification(
                error_type=error_type,
                error_message=error_message,
                details=details
            )
            
            # ENallconnectENuser
            await manager.broadcast(notification)
            
            logger.error(f"errorENsend: {error_type} - {error_message}")
            
        except Exception as e:
            logger.error(f"senderrorENfailed: {e}")
    
    @staticmethod
    async def send_processing_start(project_id: str, task_id: str):
        """sendprocessingstartEN"""
        try:
            notification = WebSocketMessage.create_task_update(
                task_id=task_id,
                status="running",
                progress=0,
                message="startprocessingproject"
            )
            
            # ENallconnectENuser
            await manager.broadcast(notification)
            
            # meanwhilesendENprojectEN
            topic = f"project_{project_id}"
            await manager.broadcast_to_topic(notification, topic)
            
            logger.info(f"processingstartENsend: {project_id} - {task_id}")
            
        except Exception as e:
            logger.error(f"sendprocessingstartENfailed: {e}")
    
    @staticmethod
    async def send_processing_progress(project_id: str, task_id: str, progress: int, message: str, 
                                     current_step: int = 0, total_steps: int = 6, step_name: str = ""):
        """sendprocessingprogressEN"""
        try:
            # createENprogressupdateEN
            notification = {
                'type': 'task_progress_update',
                'task_id': task_id,
                'project_id': project_id,
                'status': 'running',
                'progress': progress,
                'current_step': current_step,
                'total_steps': total_steps,
                'step_name': step_name,
                'message': message,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"ENsendprogressEN: {notification}")
            
            # ENallconnectENuser
            await manager.broadcast(notification)
            logger.info(f"ENprogressENalluser: {notification}")
            
            # meanwhilesendENprojectEN
            topic = f"project_{project_id}"
            await manager.broadcast_to_topic(notification, topic)
            logger.info(f"ENsendprogressEN {topic} EN: {notification}")
            
            logger.info(f"processingprogressENsend: {project_id} - {task_id} - {progress}% - {step_name}")
            
        except Exception as e:
            logger.error(f"sendprocessingprogressENfailed: {e}")
            import traceback
            logger.error(f"errorEN: {traceback.format_exc()}")
    
    @staticmethod
    async def send_processing_complete(project_id: str, task_id: str, result: dict):
        """sendprocessingEN"""
        try:
            notification = WebSocketMessage.create_task_update(
                task_id=task_id,
                status="completed",
                progress=100,
                message="projectprocessingEN"
            )
            
            # ENallconnectENuser
            await manager.broadcast(notification)
            
            # meanwhilesendENprojectEN
            topic = f"project_{project_id}"
            await manager.broadcast_to_topic(notification, topic)
            
            logger.info(f"processingENsend: {project_id} - {task_id}")
            
        except Exception as e:
            logger.error(f"sendprocessingENfailed: {e}")
    
    @staticmethod
    async def send_processing_error(project_id: str, task_id: str, error_message: str):
        """sendprocessingerrorEN"""
        try:
            notification = WebSocketMessage.create_task_update(
                task_id=task_id,
                status="failed",
                progress=0,
                error=error_message
            )
            
            # ENallconnectENuser
            await manager.broadcast(notification)
            
            # meanwhilesendENprojectEN
            topic = f"project_{project_id}"
            await manager.broadcast_to_topic(notification, topic)
            
            logger.info(f"processingerrorENsend: {project_id} - {task_id} - {error_message}")
            
        except Exception as e:
            logger.error(f"sendprocessingerrorENfailed: {e}")
    
    @staticmethod
    async def send_processing_started(project_id: str, message: str = "startvideoprocessingEN"):
        """sendprocessingstartEN（EN）"""
        await WebSocketNotificationService.send_project_update(
            project_id=project_id,
            status="processing",
            progress=0,
            message=message
        )

# ENserviceEN
notification_service = WebSocketNotificationService()