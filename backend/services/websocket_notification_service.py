"""
WebSockettranslatedservice
Providestranslatedfeature
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from ..core.websocket_manager import manager, WebSocketMessage

logger = logging.getLogger(__name__)

class WebSocketNotificationService:
    """WebSockettranslatedservice"""
    
    @staticmethod
    async def send_task_update(task_id: str, status: str, progress: Optional[int] = None,
                              message: Optional[str] = None, error: Optional[str] = None):
        """translatedtaskupdatetranslated"""
        try:
            notification = WebSocketMessage.create_task_update(
                task_id=task_id,
                status=status,
                progress=progress,
                message=message,
                error=error
            )
            
            # translatedconnect'suser
            await manager.broadcast(notification)
            
            # translatedtasktranslated'stranslated
            topic = f"task_{task_id}"
            await manager.broadcast_to_topic(notification, topic)
            
            logger.info(f"taskupdatetranslated: {task_id} - {status}")
            
        except Exception as e:
            logger.error(f"translatedtaskupdatetranslatedfailed: {e}")
    
    @staticmethod
    async def send_project_update(project_id: str, status: str, progress: Optional[int] = None,
                                message: Optional[str] = None):
        """translatedprojectupdatetranslated"""
        try:
            notification = WebSocketMessage.create_project_update(
                project_id=project_id,
                status=status,
                progress=progress,
                message=message
            )
            
            # translatedconnect'suser
            await manager.broadcast(notification)
            
            # translatedprojecttranslated'stranslated
            topic = f"project_{project_id}"
            await manager.broadcast_to_topic(notification, topic)
            
            logger.info(f"projectupdatetranslated: {project_id} - {status}")
            
        except Exception as e:
            logger.error(f"translatedprojectupdatetranslatedfailed: {e}")
    
    @staticmethod
    async def send_system_notification(notification_type: str, title: str, message: str,
                                     level: str = "info"):
        """translatedSystemtranslated"""
        try:
            notification = WebSocketMessage.create_system_notification(
                notification_type=notification_type,
                title=title,
                message=message,
                level=level
            )
            
            # translatedconnect'suser
            await manager.broadcast(notification)
            
            logger.info(f"Systemtranslated: {title} - {message}")
            
        except Exception as e:
            logger.error(f"translatedSystemtranslatedfailed: {e}")
    
    @staticmethod
    async def send_error_notification(error_type: str, error_message: str,
                                    details: Optional[Dict[str, Any]] = None):
        """translatederrortranslated"""
        try:
            notification = WebSocketMessage.create_error_notification(
                error_type=error_type,
                error_message=error_message,
                details=details
            )
            
            # translatedconnect'suser
            await manager.broadcast(notification)
            
            logger.error(f"errortranslated: {error_type} - {error_message}")
            
        except Exception as e:
            logger.error(f"translatederrortranslatedfailed: {e}")
    
    @staticmethod
    async def send_processing_start(project_id: str, task_id: str):
        """translatedprocesstranslated"""
        try:
            notification = WebSocketMessage.create_task_update(
                task_id=task_id,
                status="running",
                progress=0,
                message="translatedprocessproject"
            )
            
            # translatedconnect'suser
            await manager.broadcast(notification)
            
            # translatedprojecttranslated'stranslated
            topic = f"project_{project_id}"
            await manager.broadcast_to_topic(notification, topic)
            
            logger.info(f"processtranslated: {project_id} - {task_id}")
            
        except Exception as e:
            logger.error(f"translatedprocesstranslatedfailed: {e}")
    
    @staticmethod
    async def send_processing_progress(project_id: str, task_id: str, progress: int, message: str, 
                                     current_step: int = 0, total_steps: int = 6, step_name: str = ""):
        """translatedprocessprogresstranslated"""
        try:
            # createtranslated'sprogressupdatetranslated
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
            
            logger.info(f"translatedprogresstranslated: {notification}")
            
            # translatedconnect'suser
            await manager.broadcast(notification)
            logger.info(f"translatedprogresstranslateduser: {notification}")
            
            # translatedprojecttranslated'stranslated
            topic = f"project_{project_id}"
            await manager.broadcast_to_topic(notification, topic)
            logger.info(f"translatedprogresstranslated {topic} 'stranslated: {notification}")
            
            logger.info(f"processprogresstranslated: {project_id} - {task_id} - {progress}% - {step_name}")
            
        except Exception as e:
            logger.error(f"translatedprocessprogresstranslatedfailed: {e}")
            import traceback
            logger.error(f"errortranslated: {traceback.format_exc()}")
    
    @staticmethod
    async def send_processing_complete(project_id: str, task_id: str, result: dict):
        """translatedprocessing completedtranslated"""
        try:
            notification = WebSocketMessage.create_task_update(
                task_id=task_id,
                status="completed",
                progress=100,
                message="projectprocessing completed"
            )
            
            # translatedconnect'suser
            await manager.broadcast(notification)
            
            # translatedprojecttranslated'stranslated
            topic = f"project_{project_id}"
            await manager.broadcast_to_topic(notification, topic)
            
            logger.info(f"processing completedtranslated: {project_id} - {task_id}")
            
        except Exception as e:
            logger.error(f"translatedprocessing completedtranslatedfailed: {e}")
    
    @staticmethod
    async def send_processing_error(project_id: str, task_id: str, error_message: str):
        """translatedprocesserrortranslated"""
        try:
            notification = WebSocketMessage.create_task_update(
                task_id=task_id,
                status="failed",
                progress=0,
                error=error_message
            )
            
            # translatedconnect'suser
            await manager.broadcast(notification)
            
            # translatedprojecttranslated'stranslated
            topic = f"project_{project_id}"
            await manager.broadcast_to_topic(notification, topic)
            
            logger.info(f"processerrortranslated: {project_id} - {task_id} - {error_message}")
            
        except Exception as e:
            logger.error(f"translatedprocesserrortranslatedfailed: {e}")
    
    @staticmethod
    async def send_processing_started(project_id: str, message: str = "translatedvideoprocesstranslated"):
        """translatedprocesstranslated（translated）"""
        await WebSocketNotificationService.send_project_update(
            project_id=project_id,
            status="processing",
            progress=0,
            message=message
        )

# translatedservicetranslated
notification_service = WebSocketNotificationService()