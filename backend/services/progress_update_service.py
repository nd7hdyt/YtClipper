"""
taskprogressupdateservice
Providestranslatedprogressupdatefeature
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..models.task import Task, TaskStatus
from ..core.websocket_manager import manager as websocket_manager

logger = logging.getLogger(__name__)

class ProgressUpdateService:
    """taskprogressupdateservice"""
    
    def __init__(self):
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
    
    async def update_task_progress(
        self, 
        task_id: str, 
        progress: float, 
        current_step: str = None,
        step_details: str = None
    ):
        """updatetaskprogress"""
        try:
            # updatedatabasetranslated'staskprogress
            db = SessionLocal()
            try:
                task = db.query(Task).filter(Task.id == task_id).first()
                if task:
                    task.progress = progress
                    if current_step:
                        task.current_step = current_step
                    task.updated_at = datetime.utcnow()
                    db.commit()
                    
                    # translatedtasktranslated
                    self.active_tasks[task_id] = {
                        'progress': progress,
                        'current_step': current_step,
                        'step_details': step_details,
                        'updated_at': datetime.utcnow()
                    }
                    
                    logger.info(f"task {task_id} progressupdate: {progress}% - {current_step}")
                    
                    # translatedWebSockettranslatedprogressupdate
                    await self.broadcast_progress_update(task)
                else:
                    logger.warning(f"task {task_id} not found")
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"updatetaskprogressfailed: {e}")
    
    async def broadcast_progress_update(self, task: Task):
        """translatedprogressupdatetranslatedfrontend"""
        try:
            # translatedprogressupdatetranslated
            progress_message = {
                'type': 'task_progress_update',
                'task_id': task.id,
                'project_id': task.project_id,
                'progress': task.progress,
                'current_step': task.current_step,
                'status': task.status,
                'updated_at': task.updated_at.isoformat() if task.updated_at else None
            }
            
            # translatedconnect'stranslated
            await websocket_manager.broadcast(progress_message)
            logger.debug(f"progressupdatetranslated: {progress_message}")
            
        except Exception as e:
            logger.error(f"translatedprogressupdatefailed: {e}")
    
    async def start_progress_monitoring(self, task_id: str):
        """translatedmonitortaskprogress"""
        try:
            db = SessionLocal()
            try:
                task = db.query(Task).filter(Task.id == task_id).first()
                if task:
                    # translatedtasktranslated
                    task.status = TaskStatus.RUNNING
                    task.started_at = datetime.utcnow()
                    db.commit()
                    
                    # addtranslatedtasklist
                    self.active_tasks[task_id] = {
                        'progress': 0.0,
                        'current_step': 'translated',
                        'step_details': 'translatedprocesstask',
                        'started_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }
                    
                    logger.info(f"translatedmonitortaskprogress: {task_id}")
                    
                    # translatedtasktranslated
                    await self.broadcast_progress_update(task)
                    
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"translatedprogressmonitorfailed: {e}")
    
    async def complete_task(self, task_id: str, result: Dict[str, Any] = None, error: str = None):
        """translatedtask"""
        try:
            db = SessionLocal()
            try:
                task = db.query(Task).filter(Task.id == task_id).first()
                if task:
                    if error:
                        task.status = TaskStatus.FAILED
                        task.error_message = error
                    else:
                        task.status = TaskStatus.COMPLETED
                        task.progress = 100.0
                        task.current_step = 'translated'
                    
                    task.completed_at = datetime.utcnow()
                    task.updated_at = datetime.utcnow()
                    db.commit()
                    
                    # fromtranslatedtasklisttranslated
                    if task_id in self.active_tasks:
                        del self.active_tasks[task_id]
                    
                    logger.info(f"tasktranslated: {task_id}, status: {task.status}")
                    
                    # translatedtasktranslated
                    await self.broadcast_progress_update(task)
                    
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"translatedtaskfailed: {e}")
    
    def get_task_progress(self, task_id: str) -> Optional[Dict[str, Any]]:
        """fetchtaskprogress"""
        return self.active_tasks.get(task_id)
    
    def get_all_active_tasks(self) -> Dict[str, Dict[str, Any]]:
        """fetchtranslatedtask"""
        return self.active_tasks.copy()

# translated
progress_update_service = ProgressUpdateService()
