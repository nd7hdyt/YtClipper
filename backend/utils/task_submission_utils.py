"""
tasktranslatedtool
translated'stooltranslated，translatedimportissue
"""

import logging
import os
from typing import Dict, Any, Optional
from ..core.celery_app import celery_app

logger = logging.getLogger(__name__)


def _is_desktop_mode() -> bool:
    return os.getenv("AUTOCLIP_DESKTOP_MODE", "").lower() in {"1", "true", "yes"}


def _log_queue_depth(queue: str) -> Optional[int]:
    """translated Redis translated，Onlyusetranslated；translatedfailedtranslated warning，translated。"""
    try:
        import redis

        redis_url = os.getenv('REDIS_URL') or str(celery_app.conf.broker_url)
        client = redis.Redis.from_url(redis_url, socket_connect_timeout=2, socket_timeout=2)
        depth = client.llen(queue)
        logger.info(f"Redis translated {queue} translated: {depth}")
        return depth
    except Exception as e:  # noqa: BLE001
        logger.warning(f"translated Redis translated {queue} translatedfailed（Onlytranslated，translatedtask）: {e}")
        return None


def _run_pipeline_locally(project_id: str, input_video_path: str, input_srt_path: str) -> Dict[str, Any]:
    """translated：translated Redis/Celery broker，translatedintranslatedtask。

    translatedinstallPackagetranslated Redis，translateduse's core.celery_app translated redis://localhost。
    Celery task process_video_pipeline translatedIs「intasktranslated」
    （asyncio.run(pipeline_adapter...)），translatedtask，Socantranslateduse .apply()
    inlocaltranslated，progresstranslateddatabase's Task translatedfrontendtranslated。
    """
    import uuid
    import threading

    task_id = str(uuid.uuid4())

    def run():
        try:
            # translatedimport，translateddependencies
            from ..tasks.processing import process_video_pipeline
            process_video_pipeline.apply(
                args=[project_id, input_video_path, input_srt_path],
                task_id=task_id,
            )
            logger.info(f"translatedlocaltranslated: {project_id}, task_id={task_id}")
        except Exception as e:  # noqa: BLE001
            logger.error(f"translatedlocaltranslatedfailed: {project_id}, error: {e}", exc_info=True)

    threading.Thread(target=run, name=f"pipeline-{project_id[:8]}", daemon=True).start()
    logger.info(f"translated：translatedinlocaltranslatedstartvideotranslated {project_id}, task_id={task_id}")
    return {
        'success': True,
        'task_id': task_id,
        'status': 'PtranslatedDING',
        'message': 'videotranslatedtasktranslatedinlocalstart',
    }


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
    # translated Redis，translatedlocaltranslated
    if _is_desktop_mode():
        return _run_pipeline_locally(project_id, input_video_path, input_srt_path)

    try:
        logger.info(f"translatedvideotranslatedtask: {project_id}")
        
        # translatedusecelery_apptranslatedtask
        logger.info(f"translatedtasktranslated...")
        logger.info(f"tasktranslated: backend.tasks.processing.process_video_pipeline")
        logger.info(f"tasktranslated: {[project_id, input_video_path, input_srt_path]}")
        
        celery_task = celery_app.send_task(
            'backend.tasks.processing.process_video_pipeline',
            args=[project_id, input_video_path, input_srt_path]
        )
        logger.info(f"videotranslatedtasktranslated: {celery_task.id}")

        # translatedusetranslated。translated REDIS_URL（docker-compose translated Redis translatedin localhost），
        # translatedsucceeded'stask。
        _log_queue_depth('processing')

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
