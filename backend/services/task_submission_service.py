"""
tasktranslatedservice
translatedimportissue
"""

import logging
from typing import Dict, Any, Optional
from ..core.celery_app import celery_app

logger = logging.getLogger(__name__)

class TaskSubmissionService:
    """tasktranslatedservice"""
    
    @staticmethod
    def submit_video_pipeline_task(project_id: str, input_video_path: str, input_srt_path: str) -> Dict[str, Any]:
        """
        translatedvideotranslatedtask
        
        Args:
            project_id: projectID
            input_video_path: translatedvideopath
            input_srt_path: translatedSRTpath
            
        Returns:
            tasktranslated
        """
        try:
            logger.info(f"translatedvideotranslatedtask: {project_id}")
            
            # translatedusecelery_apptranslatedtask
            celery_task = celery_app.send_task(
                'tasks.processing.process_video_pipeline',
                args=[project_id, input_video_path, input_srt_path]
            )
            
            logger.info(f"videotranslatedtasktranslated: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': celery_task.id,
                'status': 'PtranslatedDING',
                'message': 'videotranslatedtasktranslated'
            }
            
        except Exception as e:
            logger.error(f"translatedvideotranslatedtaskfailed: {project_id}, error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'tasktranslatedfailed'
            }
    
    @staticmethod
    def submit_single_step_task(project_id: str, step: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        translated steptask
        
        Args:
            project_id: projectID
            step: steptranslated
            config: processconfig
            
        Returns:
            tasktranslated
        """
        try:
            logger.info(f"translated steptask: {project_id}, {step}")
            
            # translatedusecelery_apptranslatedtask
            celery_task = celery_app.send_task(
                'tasks.processing.process_single_step',
                args=[project_id, step, config]
            )
            
            logger.info(f"translated steptasktranslated: {celery_task.id}")
            
            return {
                'success': True,
                'task_id': celery_task.id,
                'step': step,
                'status': 'PtranslatedDING',
                'message': f'step {step} tasktranslated'
            }
            
        except Exception as e:
            logger.error(f"translated steptaskfailed: {project_id}, {step}, error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'tasktranslatedfailed'
            }

