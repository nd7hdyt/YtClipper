"""
ENtask
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from celery import shared_task
from ..core.celery_app import celery_app
from datetime import datetime
from ..core.database import SessionLocal
from ..models.task import Task, TaskStatus
from ..services.websocket_notification_service import WebSocketNotificationService

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='backend.tasks.notification.send_processing_notification')
def send_processing_notification(self, project_id: str, task_id: str, message: str, notification_type: str = 'info') -> Dict[str, Any]:
    """
    sendprocessingEN
    
    Args:
        project_id: projectID
        task_id: taskID
        message: EN
        notification_type: EN (info, warning, error, success)
        
    Returns:
        ENresult
    """
    logger.info(f"sendprocessingEN: {project_id}, {task_id}, {notification_type}")
    
    try:
        # createdatabaseEN
        db = SessionLocal()
        
        try:
            # ENcanENsystem
            # for example：WebSocket、EN、EN
            
            # ENsend
            notification_data = {
                'project_id': project_id,
                'task_id': task_id,
                'message': message,
                'type': notification_type,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"ENsend: {notification_data}")
            
            return {
                'success': True,
                'project_id': project_id,
                'task_id': task_id,
                'notification': notification_data,
                'message': 'ENsendsucceeded'
            }
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"ENsendfailed: {project_id}, {task_id}, error: {e}")
        raise


@shared_task(bind=True, name='backend.tasks.notification.send_error_notification')
def send_error_notification(self, project_id: str, task_id: str, error_message: str, error_details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    senderrorEN
    
    Args:
        project_id: projectID
        task_id: taskID
        error_message: errorEN
        error_details: errorEN
        
    Returns:
        ENresult
    """
    logger.error(f"senderrorEN: {project_id}, {task_id}, {error_message}")
    
    try:
        # createdatabaseEN
        db = SessionLocal()
        
        try:
            # updatetaskstatus
            # task_repo = TaskRepository(db) # This line was removed as per the new_code
            # task = task_repo.get_by_id(task_id) # This line was removed as per the new_code
            # if task: # This line was removed as per the new_code
            #     task.status = TaskStatus.FAILED # This line was removed as per the new_code
            #     task.error_message = error_message # This line was removed as per the new_code
            #     db.commit() # This line was removed as per the new_code
            
            # senderrorEN
            notification_data = {
                'project_id': project_id,
                'task_id': task_id,
                'type': 'error',
                'message': error_message,
                'details': error_details,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.error(f"errorENsend: {notification_data}")
            
            return {
                'success': True,
                'project_id': project_id,
                'task_id': task_id,
                'notification': notification_data,
                'message': 'errorENsendsucceeded'
            }
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"errorENsendfailed: {project_id}, {task_id}, error: {e}")
        raise


@shared_task(bind=True, name='backend.tasks.notification.send_completion_notification')
def send_completion_notification(self, project_id: str, task_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
    """
    sendEN
    
    Args:
        project_id: projectID
        task_id: taskID
        result: processingresult
        
    Returns:
        ENresult
    """
    logger.info(f"sendEN: {project_id}, {task_id}")
    
    try:
        # createdatabaseEN
        db = SessionLocal()
        
        try:
            # updatetaskstatus
            # task_repo = TaskRepository(db) # This line was removed as per the new_code
            # task = task_repo.get_by_id(task_id) # This line was removed as per the new_code
            # if task: # This line was removed as per the new_code
            #     task.status = TaskStatus.COMPLETED # This line was removed as per the new_code
            #     task.result = result # This line was removed as per the new_code
            #     db.commit() # This line was removed as per the new_code
            
            # sendEN
            notification_data = {
                'project_id': project_id,
                'task_id': task_id,
                'type': 'success',
                'message': 'processingEN',
                'result': result,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"ENsend: {notification_data}")
            
            return {
                'success': True,
                'project_id': project_id,
                'task_id': task_id,
                'notification': notification_data,
                'message': 'ENsendsucceeded'
            }
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"ENsendfailed: {project_id}, {task_id}, error: {e}")
        raise