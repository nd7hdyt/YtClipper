"""
taskqueueENservice
ENCelerytaskEN、ENstatusEN
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
    """taskqueueENservice"""
    
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
        ENvideoprocessingtask
        
        Args:
            project_id: projectID
            input_video_path: ENvideopath
            input_srt_path: ENSRTpath
            
        Returns:
            taskENresult
        """
        logger.info(f"ENvideoprocessingtask: {project_id}")
        
        try:
            # createENsavetaskEN
            task = self.task_repo.create(
                project_id=project_id,
                name="videoENprocessing",
                description=f"processingproject {project_id} ENvideoEN",
                task_type=TaskType.VIDEO_PROCESSING,
                status=TaskStatus.PENDING,
                priority=1
            )
            
            # ENCelerytask
            celery_task = process_video_pipeline.delay(
                project_id=project_id,
                input_video_path=input_video_path,
                input_srt_path=input_srt_path,
            )
            
            # updatetaskEN
            task.celery_task_id = celery_task.id
            self.db.commit()
            
            logger.info(f"videoprocessingtaskEN: {task.id}, CelerytaskID: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': task.id,
                'celery_task_id': celery_task.id,
                'status': 'PENDING',
                'message': 'videoprocessingtaskEN'
            }
            
        except Exception as e:
            logger.error(f"ENvideoprocessingtaskfailed: {project_id}, error: {e}")
            raise
    
    def submit_single_step_task(
        self,
        project_id: str,
        step_name: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        ENprocessingtask
        
        Args:
            project_id: projectID
            step_name: EN
            config: ENconfigparameters
            
        Returns:
            taskENresult
        """
        logger.info(f"ENtask: {project_id}, {step_name}")
        
        try:
            # createENsavetaskEN
            task = self.task_repo.create(
                project_id=project_id,
                name=f"ENprocessing: {step_name}",
                description=f"processingproject {project_id} EN {step_name}",
                task_type=TaskType.VIDEO_PROCESSING,
                status=TaskStatus.PENDING,
                priority=2
            )
            
            # ENCelerytask
            celery_task = process_single_step.delay(project_id, step_name, config or {})
            
            # updatetaskEN
            task.celery_task_id = celery_task.id
            self.db.commit()
            
            logger.info(f"ENtaskEN: {task.id}, CelerytaskID: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': task.id,
                'celery_task_id': celery_task.id,
                'step': step_name,
                'status': 'PENDING',
                'message': f'EN {step_name} processingtaskEN'
            }
            
        except Exception as e:
            logger.error(f"ENtaskfailed: {project_id}, {step_name}, error: {e}")
            raise
    
    def submit_retry_task(
        self,
        project_id: str,
        task_id: str,
        step_name: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        ENretrytask
        
        Args:
            project_id: projectID
            task_id: taskID
            step_name: EN
            config: ENconfigparameters
            
        Returns:
            taskENresult
        """
        logger.info(f"ENretrytask: {project_id}, {task_id}, {step_name}")
        
        try:
            # createENsavetaskEN
            task = self.task_repo.create(
                project_id=project_id,
                name=f"retryEN: {step_name}",
                description=f"retryproject {project_id} EN {step_name}",
                task_type=TaskType.VIDEO_PROCESSING,
                status=TaskStatus.PENDING,
                priority=3
            )
            
            # ENCelerytask
            celery_task = retry_processing_step.delay(project_id, step_name, config or {}, task_id)
            
            # updatetaskEN
            task.celery_task_id = celery_task.id
            self.db.commit()
            
            logger.info(f"retrytaskEN: {task.id}, CelerytaskID: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': task.id,
                'celery_task_id': celery_task.id,
                'original_task_id': task_id,
                'step': step_name,
                'status': 'PENDING',
                'message': f'EN {step_name} retrytaskEN'
            }
            
        except Exception as e:
            logger.error(f"ENretrytaskfailed: {project_id}, {task_id}, {step_name}, error: {e}")
            raise
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        fetchtaskstatus
        
        Args:
            task_id: taskID
            
        Returns:
            taskstatusEN
        """
        try:
            # fetchdatabasetaskEN
            task = self.task_repo.get_by_id(task_id)
            if not task:
                return {'error': 'taskdoes not exist'}
            
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
        fetchprojectENalltask
        
        Args:
            project_id: projectID
            
        Returns:
            taskEN
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
            cancelresult
        """
        try:
            task = self.task_repo.get_by_id(task_id)
            if not task:
                return {'error': 'taskdoes not exist'}
            
            # cancelCelerytask
            if task.celery_task_id:
                celery_result = AsyncResult(task.celery_task_id, app=celery_app)
                celery_result.revoke(terminate=True)
            
            # updatetaskstatus
            task.status = TaskStatus.CANCELLED
            self.db.commit()
            
            logger.info(f"taskENcancel: {task_id}")
            return {
                'success': True,
                'task_id': task_id,
                'status': 'CANCELLED',
                'message': 'taskENcancel'
            }
            
        except Exception as e:
            logger.error(f"canceltaskfailed: {task_id}, error: {e}")
            return {'error': f'canceltaskfailed: {e}'}
    
    def submit_video_clips_task(self, project_id: str, clip_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        ENvideoENtask
        
        Args:
            project_id: projectID
            clip_data: EN
            
        Returns:
            taskENresult
        """
        logger.info(f"ENvideoENtask: {project_id}")
        
        try:
            # createENsavetaskEN
            task = self.task_repo.create(
                project_id=project_id,
                name="videoEN",
                description=f"ENproject {project_id} ENvideoEN",
                task_type=TaskType.VIDEO_PROCESSING,
                status=TaskStatus.PENDING,
                priority=2
            )
            
            # ENCelerytask
            celery_task = extract_video_clips.delay(project_id, clip_data)
            
            # updatetaskEN
            task.celery_task_id = celery_task.id
            self.db.commit()
            
            logger.info(f"videoENtaskEN: {task.id}, CelerytaskID: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': task.id,
                'celery_task_id': celery_task.id,
                'clip_count': len(clip_data),
                'status': 'PENDING',
                'message': f'videoENtaskEN，EN {len(clip_data)} EN'
            }
            
        except Exception as e:
            logger.error(f"ENvideoENtaskfailed: {project_id}, error: {e}")
            raise
    
    def submit_collection_generation_task(self, project_id: str, collection_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        ENcollectiongeneratetask
        
        Args:
            project_id: projectID
            collection_data: collectionEN
            
        Returns:
            taskENresult
        """
        logger.info(f"ENcollectiongeneratetask: {project_id}")
        
        try:
            # createENsavetaskEN
            task = self.task_repo.create(
                project_id=project_id,
                name="videocollectiongenerate",
                description=f"generateproject {project_id} ENvideocollection",
                task_type=TaskType.VIDEO_PROCESSING,
                status=TaskStatus.PENDING,
                priority=2
            )
            
            # ENCelerytask
            celery_task = generate_video_collections.delay(project_id, collection_data)
            
            # updatetaskEN
            task.celery_task_id = celery_task.id
            self.db.commit()
            
            logger.info(f"collectiongeneratetaskEN: {task.id}, CelerytaskID: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': task.id,
                'celery_task_id': celery_task.id,
                'collection_count': len(collection_data),
                'status': 'PENDING',
                'message': f'videocollectiongeneratetaskEN，EN {len(collection_data)} ENcollection'
            }
            
        except Exception as e:
            logger.error(f"ENcollectiongeneratetaskfailed: {project_id}, error: {e}")
            raise 