"""
taskEN
EN，EN
"""

import logging
import os
from typing import Dict, Any, Optional
from ..core.celery_app import celery_app

logger = logging.getLogger(__name__)


def _is_desktop_mode() -> bool:
    return os.getenv("AUTOCLIP_DESKTOP_MODE", "").lower() in {"1", "true", "yes"}


def _log_queue_depth(queue: str) -> Optional[int]:
    """EN Redis queueEN，EN；ENfailedEN warning，EN。"""
    try:
        import redis

        redis_url = os.getenv('REDIS_URL') or str(celery_app.conf.broker_url)
        client = redis.Redis.from_url(redis_url, socket_connect_timeout=2, socket_timeout=2)
        depth = client.llen(queue)
        logger.info(f"Redis queue {queue} EN: {depth}")
        return depth
    except Exception as e:  # noqa: BLE001
        logger.warning(f"read Redis queue {queue} ENfailed（EN，ENtask）: {e}")
        return None


def _run_pipeline_locally(project_id: str, input_video_path: str, input_srt_path: str) -> Dict[str, Any]:
    """EN：EN Redis/Celery broker，ENexecuteENtask。

    EN Redis，EN core.celery_app EN redis://localhost。
    Celery task process_video_pipeline EN「ENtaskEN」
    （asyncio.run(pipeline_adapter...)），ENtask，socanEN .apply()
    EN，progressENdatabaseEN Task EN。
    """
    import uuid
    import threading

    task_id = str(uuid.uuid4())

    def run():
        try:
            # EN，EN
            from ..tasks.processing import process_video_pipeline
            process_video_pipeline.apply(
                args=[project_id, input_video_path, input_srt_path],
                task_id=task_id,
            )
            logger.info(f"ENexecuteend: {project_id}, task_id={task_id}")
        except Exception as e:  # noqa: BLE001
            logger.error(f"ENexecutefailed: {project_id}, error: {e}", exc_info=True)

    threading.Thread(target=run, name=f"pipeline-{project_id[:8]}", daemon=True).start()
    logger.info(f"EN：ENstartvideoEN {project_id}, task_id={task_id}")
    return {
        'success': True,
        'task_id': task_id,
        'status': 'PENDING',
        'message': 'videoENtaskENstart',
    }


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
    # EN Redis，ENexecute
    if _is_desktop_mode():
        return _run_pipeline_locally(project_id, input_video_path, input_srt_path)

    try:
        logger.info(f"ENvideoENtask: {project_id}")
        
        # ENusecelery_appENtask
        logger.info(f"ENtaskENqueue...")
        logger.info(f"taskEN: backend.tasks.processing.process_video_pipeline")
        logger.info(f"taskparameters: {[project_id, input_video_path, input_srt_path]}")
        
        celery_task = celery_app.send_task(
            'backend.tasks.processing.process_video_pipeline',
            args=[project_id, input_video_path, input_srt_path]
        )
        logger.info(f"videoENtaskEN: {celery_task.id}")

        # queueEN。ENmustEN REDIS_URL（docker-compose EN Redis EN localhost），
        # ENalreadyENsucceededENtask。
        _log_queue_depth('processing')

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
