"""
taskENservice
EN
"""

import logging
from typing import Dict, Any, Optional
from ..core.celery_app import celery_app

logger = logging.getLogger(__name__)

class TaskSubmissionService:
    """taskENservice"""
    
    @staticmethod
    def submit_video_pipeline_task(project_id: str, input_video_path: str, input_srt_path: str) -> Dict[str, Any]:
        """
        ENvideoENtask
        
        Args:
            project_id: projectID
            input_video_path: ENvideopath
            input_srt_path: ENSRTpath
            
        Returns:
            taskENresult
        """
        try:
            logger.info(f"ENvideoENtask: {project_id}")
            
            # ENusecelery_appENtask
            celery_task = celery_app.send_task(
                'tasks.processing.process_video_pipeline',
                args=[project_id, input_video_path, input_srt_path]
            )
            
            logger.info(f"videoENtaskEN: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': celery_task.id,
                'status': 'PENDING',
                'message': 'videoENtaskEN'
            }
            
        except Exception as e:
            logger.error(f"ENvideoENtaskfailed: {project_id}, error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'taskENfailed'
            }
    
    @staticmethod
    def submit_single_step_task(project_id: str, step: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        ENtask
        
        Args:
            project_id: projectID
            step: EN
            config: processingconfig
            
        Returns:
            taskENresult
        """
        try:
            logger.info(f"ENtask: {project_id}, {step}")
            
            # ENusecelery_appENtask
            celery_task = celery_app.send_task(
                'tasks.processing.process_single_step',
                args=[project_id, step, config]
            )
            
            logger.info(f"ENtaskEN: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': celery_task.id,
                'step': step,
                'status': 'PENDING',
                'message': f'EN {step} taskEN'
            }
            
        except Exception as e:
            logger.error(f"ENtaskfailed: {project_id}, {step}, error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'taskENfailed'
            }

