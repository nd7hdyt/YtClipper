"""
Task Queuetranslatedservice
translatedCelerytask'stranslated、monitorAndstatustranslated
"""

import logging
from typing import Dict, Any, Optional, List
from celery.result import AsyncResult
from sqlalchemy.orm import Session

from ..core.celery_app import celery_app
from ..core.database import SessionLocal
from ..models.task import Task, TaskStatus, TaskType
from ..repositories.task_repository import TaskRepository
from ..tasks.processing import process_video_pipeline, process_single_step, retry_processing_step
from ..tasks.video import extract_video_clips, generate_video_collections, optimize_video_quality
from ..tasks.notification import send_processing_notification, send_error_notification, send_completion_notification
from ..tasks.maintenance import cleanup_expired_tasks, health_check, backup_project_data

logger = logging.getLogger(__name__)


class TaskQueueService:
    """Task Queuetranslatedservice"""
    
    def __init__(self, db: Session):
        self.db = db
        self.task_repo = TaskRepository(db)
    
    def submit_video_processing_task(
        self,
        project_id: str,
        input_video_path: str,
        input_srt_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        translatedvideoprocesstask
        
        Args:
            project_id: projectID
            input_video_path: translatedvideopath
            input_srt_path: translatedSRTpath
            
        Returns:
            tasktranslated
        """
        logger.info(f"translatedvideoprocesstask: {project_id}")
        
        try:
            # createtranslatedtasktranslated
            task = self.task_repo.create(
                project_id=project_id,
                name="videotranslatedprocess",
                description=f"processproject {project_id} 'svideotranslated",
                task_type=TaskType.VIDEO_PROCESSING,
                status=TaskStatus.PtranslatedDING,
                priority=1
            )
            
            # translatedCelerytask
            celery_task = process_video_pipeline.delay(
                project_id=project_id,
                input_video_path=input_video_path,
                input_srt_path=input_srt_path,
            )
            
            # updatetasktranslated
            task.celery_task_id = celery_task.id
            self.db.commit()
            
            logger.info(f"videoprocesstasktranslated: {task.id}, CelerytaskID: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': task.id,
                'celery_task_id': celery_task.id,
                'status': 'PtranslatedDING',
                'message': 'videoprocesstasktranslated'
            }
            
        except Exception as e:
            logger.error(f"translatedvideoprocesstaskfailed: {project_id}, error: {e}")
            raise
    
    def submit_single_step_task(
        self,
        project_id: str,
        step_name: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        translated stepprocesstask
        
        Args:
            project_id: projectID
            step_name: steptranslated
            config: stepconfigtranslated
            
        Returns:
            tasktranslated
        """
        logger.info(f"translated steptask: {project_id}, {step_name}")
        
        try:
            # createtranslatedtasktranslated
            task = self.task_repo.create(
                project_id=project_id,
                name=f"stepprocess: {step_name}",
                description=f"processproject {project_id} 'sstep {step_name}",
                task_type=TaskType.VIDEO_PROCESSING,
                status=TaskStatus.PtranslatedDING,
                priority=2
            )
            
            # translatedCelerytask
            celery_task = process_single_step.delay(project_id, step_name, config or {})
            
            # updatetasktranslated
            task.celery_task_id = celery_task.id
            self.db.commit()
            
            logger.info(f"translated steptasktranslated: {task.id}, CelerytaskID: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': task.id,
                'celery_task_id': celery_task.id,
                'step': step_name,
                'status': 'PtranslatedDING',
                'message': f'step {step_name} processtasktranslated'
            }
            
        except Exception as e:
            logger.error(f"translated steptaskfailed: {project_id}, {step_name}, error: {e}")
            raise
    
    def submit_retry_task(
        self,
        project_id: str,
        task_id: str,
        step_name: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        translatedtask
        
        Args:
            project_id: projectID
            task_id: taskID
            step_name: steptranslated
            config: stepconfigtranslated
            
        Returns:
            tasktranslated
        """
        logger.info(f"translatedtask: {project_id}, {task_id}, {step_name}")
        
        try:
            # createtranslatedtasktranslated
            task = self.task_repo.create(
                project_id=project_id,
                name=f"translatedstep: {step_name}",
                description=f"translatedproject {project_id} 'sstep {step_name}",
                task_type=TaskType.VIDEO_PROCESSING,
                status=TaskStatus.PtranslatedDING,
                priority=3
            )
            
            # translatedCelerytask
            celery_task = retry_processing_step.delay(project_id, step_name, config or {}, task_id)
            
            # updatetasktranslated
            task.celery_task_id = celery_task.id
            self.db.commit()
            
            logger.info(f"translatedtasktranslated: {task.id}, CelerytaskID: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': task.id,
                'celery_task_id': celery_task.id,
                'original_task_id': task_id,
                'step': step_name,
                'status': 'PtranslatedDING',
                'message': f'step {step_name} translatedtasktranslated'
            }
            
        except Exception as e:
            logger.error(f"translatedtaskfailed: {project_id}, {task_id}, {step_name}, error: {e}")
            raise
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        fetchtaskstatus
        
        Args:
            task_id: taskID
            
        Returns:
            taskstatusinfo
        """
        try:
            # fetchdatabasetasktranslated
            task = self.task_repo.get_by_id(task_id)
            if not task:
                return {'error': 'tasknot found'}
            
            # fetchCelerytaskstatus
            celery_status = {}
            if task.celery_task_id:
                celery_result = AsyncResult(task.celery_task_id, app=celery_app)
                celery_status = {
                    'celery_task_id': task.celery_task_id,
                    'celery_status': celery_result.status,
                    'celery_result': celery_result.result if celery_result.ready() else None,
                    'celery_info': celery_result.info if hasattr(celery_result, 'info') else None
                }
            
            return {
                'task_id': task.id,
                'project_id': task.project_id,
                'name': task.name,
                'status': task.status.value,
                'task_type': task.task_type.value,
                'progress': task.progress,
                'error_message': task.error_message,
                'result': task.result_data,
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat(),
                'celery_status': celery_status
            }
            
        except Exception as e:
            logger.error(f"fetchtaskstatusfailed: {task_id}, error: {e}")
            return {'error': f'fetchtaskstatusfailed: {e}'}
    
    def get_project_tasks(self, project_id: str) -> List[Dict[str, Any]]:
        """
        fetchproject'stranslatedtask
        
        Args:
            project_id: projectID
            
        Returns:
            tasklist
        """
        try:
            tasks = self.task_repo.get_by_project(project_id)
            return [
                {
                    'task_id': task.id,
                    'name': task.name,
                    'status': task.status.value,
                    'task_type': task.task_type.value,
                    'progress': task.progress,
                    'created_at': task.created_at.isoformat(),
                    'updated_at': task.updated_at.isoformat()
                }
                for task in tasks
            ]
            
        except Exception as e:
            logger.error(f"fetchprojecttaskfailed: {project_id}, error: {e}")
            return []
    
    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """
        canceltask
        
        Args:
            task_id: taskID
            
        Returns:
            canceltranslated
        """
        try:
            task = self.task_repo.get_by_id(task_id)
            if not task:
                return {'error': 'tasknot found'}
            
            # cancelCelerytask
            if task.celery_task_id:
                celery_result = AsyncResult(task.celery_task_id, app=celery_app)
                celery_result.revoke(terminate=True)
            
            # updatetaskstatus
            task.status = TaskStatus.CANCELLED
            self.db.commit()
            
            logger.info(f"tasktranslatedcancel: {task_id}")
            return {
                'success': True,
                'task_id': task_id,
                'status': 'CANCELLED',
                'message': 'tasktranslatedcancel'
            }
            
        except Exception as e:
            logger.error(f"canceltaskfailed: {task_id}, error: {e}")
            return {'error': f'canceltaskfailed: {e}'}
    
    def submit_video_clips_task(self, project_id: str, clip_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        translatedvideotranslatedtask
        
        Args:
            project_id: projectID
            clip_data: translated
            
        Returns:
            tasktranslated
        """
        logger.info(f"translatedvideotranslatedtask: {project_id}")
        
        try:
            # createtranslatedtasktranslated
            task = self.task_repo.create(
                project_id=project_id,
                name="videotranslated",
                description=f"translatedproject {project_id} 'svideotranslated",
                task_type=TaskType.VIDEO_PROCESSING,
                status=TaskStatus.PtranslatedDING,
                priority=2
            )
            
            # translatedCelerytask
            celery_task = extract_video_clips.delay(project_id, clip_data)
            
            # updatetasktranslated
            task.celery_task_id = celery_task.id
            self.db.commit()
            
            logger.info(f"videotranslatedtasktranslated: {task.id}, CelerytaskID: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': task.id,
                'celery_task_id': celery_task.id,
                'clip_count': len(clip_data),
                'status': 'PtranslatedDING',
                'message': f'videotranslatedtasktranslated，translated {len(clip_data)}  translated'
            }
            
        except Exception as e:
            logger.error(f"translatedvideotranslatedtaskfailed: {project_id}, error: {e}")
            raise
    
    def submit_collection_generation_task(self, project_id: str, collection_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        translatedcollectiontranslatedtask
        
        Args:
            project_id: projectID
            collection_data: collectiontranslated
            
        Returns:
            tasktranslated
        """
        logger.info(f"translatedcollectiontranslatedtask: {project_id}")
        
        try:
            # createtranslatedtasktranslated
            task = self.task_repo.create(
                project_id=project_id,
                name="videocollectiontranslated",
                description=f"translatedproject {project_id} 'svideocollection",
                task_type=TaskType.VIDEO_PROCESSING,
                status=TaskStatus.PtranslatedDING,
                priority=2
            )
            
            # translatedCelerytask
            celery_task = generate_video_collections.delay(project_id, collection_data)
            
            # updatetasktranslated
            task.celery_task_id = celery_task.id
            self.db.commit()
            
            logger.info(f"collectiontranslatedtasktranslated: {task.id}, CelerytaskID: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': task.id,
                'celery_task_id': celery_task.id,
                'collection_count': len(collection_data),
                'status': 'PtranslatedDING',
                'message': f'videocollectiontranslatedtasktranslated，translated {len(collection_data)}  collection'
            }
            
        except Exception as e:
            logger.error(f"translatedcollectiontranslatedtaskfailed: {project_id}, error: {e}")
            raise 