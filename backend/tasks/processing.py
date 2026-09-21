"""videoprocessingCelerytask
ENWebSocketENPipelineEN
"""

import os
import logging
import asyncio
from typing import Dict, Any, Optional
from celery import current_task
from pathlib import Path

from backend.core.celery_app import celery_app
from backend.services.websocket_notification_service import notification_service
from backend.services.processing_service import ProcessingService
from backend.services.pipeline_adapter import create_pipeline_adapter
from backend.core.database import SessionLocal
from backend.models.project import Project, ProjectStatus
from backend.models.task import Task, TaskStatus, TaskType
from datetime import datetime

logger = logging.getLogger(__name__)

def run_async_notification(coro):
    """runEN - EN"""
    try:
        # ENfetchEN
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # ifENcurrentlyrun，useENexecute
            import concurrent.futures
            import threading
            
            def run_in_thread():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return new_loop.run_until_complete(coro)
                finally:
                    new_loop.close()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_in_thread)
                return future.result(timeout=10)  # 10ENtimeout
        else:
            # ifENrun，ENrun
            return loop.run_until_complete(coro)
    except RuntimeError:
        # EN，createEN
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

# ENprojectENtimeEN。EN（/process、/retry、
# ENstart、downloadENstart）mayENproject，ENtaskEN Redis EN
# soEN；ENtaskENexecute，mustENexecuteENdatabase。
import threading as _threading
_active_pipeline_projects: set = set()
_active_pipeline_lock = _threading.Lock()


@celery_app.task(bind=True, name='backend.tasks.processing.process_video_pipeline')
def process_video_pipeline(
    self,
    project_id: str,
    input_video_path: str,
    input_srt_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    processingvideoENtask - usePipelineEN
    
    Args:
        project_id: projectID
        input_video_path: ENvideopath
        input_srt_path: ENSRTpath
        
    Returns:
        processingresult
    """
    task_id = self.request.id
    logger.info(f"startprocessingvideoEN: {project_id}, taskID: {task_id}")

    # EN：ENprojectEN
    with _active_pipeline_lock:
        if project_id in _active_pipeline_projects:
            logger.warning(f"project {project_id} ENrun，ENtask {task_id}")
            return {
                "success": False,
                "skipped": True,
                "project_id": project_id,
                "task_id": task_id,
                "message": "ENrun，ENtask",
            }
        _active_pipeline_projects.add(project_id)

    try:
        # createdatabaseEN
        db = SessionLocal()
        
        try:
            # createtaskEN
            task = Task(
                name=f"videoprocessingEN",
                description=f"processingproject {project_id} ENvideoEN",
                task_type=TaskType.VIDEO_PROCESSING,
                project_id=project_id,
                celery_task_id=task_id,
                status=TaskStatus.RUNNING,
                progress=0,
                current_step="initialize",
                total_steps=6
            )
            db.add(task)
            db.commit()
            
            # sendstartEN
            run_async_notification(
                notification_service.send_processing_start(project_id, task_id)
            )
            
            # ENprogresssystemENneedEN
            # ENprogresssystemENsendprogressEN
            
            # useENPipelineEN
            from backend.services.simple_pipeline_adapter import create_simple_pipeline_adapter
            pipeline_adapter = create_simple_pipeline_adapter(str(project_id), str(task.id))
            
            # executePipelineprocessing - useEN
            import asyncio
            result = asyncio.run(pipeline_adapter.process_project_sync(input_video_path, input_srt_path))
            
            # checkprocessingresult
            if result.get("status") == "failed":
                # processingfailed。adapter returnEN error（EN message，userEN「processingfailed」EN）
                error_msg = result.get("error") or result.get("message") or "processingfailed"
                task.status = TaskStatus.FAILED
                task.error_message = error_msg
                if result.get("stage"):
                    task.current_step = f"failedEN {result['stage']}"
                task.result_data = result
                
                # updateprojectstatusENfailed
                project = db.query(Project).filter(Project.id == project_id).first()
                if project:
                    project.status = ProjectStatus.FAILED
                    project.updated_at = datetime.utcnow()
                    logger.info(f"projectstatusupdatedENfailed: {project_id}")
                
                db.commit()
                
                # failedstatusENprogresssystemENprocessing
                
                # senderrorEN（EN） - ENWebSocketEN
                # run_async_notification(
                #     notification_service.send_processing_error(project_id, task_id, error_msg)
                # )
                
                return {
                    "success": False,
                    "project_id": project_id,
                    "task_id": task_id,
                    "error": error_msg,
                    "result": result
                }
            else:
                # processingsucceeded
                task.status = TaskStatus.COMPLETED
                task.progress = 100
                task.current_step = "processingEN"
                task.result_data = result
                
                # updateprojectstatusENcompleted
                project = db.query(Project).filter(Project.id == project_id).first()
                if project:
                    project.status = ProjectStatus.COMPLETED
                    project.completed_at = datetime.utcnow()
                    project.updated_at = datetime.utcnow()
                    logger.info(f"projectstatusupdatedENcompleted: {project_id}")
                
                db.commit()
                
                # ENstatusENprogresssystemENprocessing
                
                # sendEN（EN） - ENWebSocketEN
                # run_async_notification(
                #     notification_service.send_processing_complete(project_id, task_id, result)
                # )
            
            logger.info(f"videoENprocessingEN: {project_id}")
            return {
                "success": True,
                "project_id": project_id,
                "task_id": task_id,
                "result": result,
                "message": "videoprocessingEN"
            }
            
        finally:
            db.close()
            # EN（ENsucceeded/failed/ENreturnEN）
            with _active_pipeline_lock:
                _active_pipeline_projects.discard(project_id)

    except Exception as e:
        error_msg = f"videoENprocessingfailed: {str(e)}"
        logger.error(error_msg)

        # EN（ENpathEN finally EN，ENexceptionEN）
        with _active_pipeline_lock:
            _active_pipeline_projects.discard(project_id)

        # updatetaskstatusENfailed
        try:
            db = SessionLocal()
            task = db.query(Task).filter(Task.celery_task_id == task_id).first()
            if task:
                task.status = TaskStatus.FAILED
                task.error_message = error_msg
                
                # updateprojectstatusENfailed
                project = db.query(Project).filter(Project.id == project_id).first()
                if project:
                    project.status = ProjectStatus.FAILED
                    project.updated_at = datetime.utcnow()
                    logger.info(f"projectstatusupdatedENfailed: {project_id}")
                
                db.commit()
            db.close()
        except Exception as db_error:
            logger.error(f"updatetaskstatusfailed: {str(db_error)}")
        
        # senderrorEN
        run_async_notification(
            notification_service.send_processing_error(project_id, task_id, error_msg)
        )
        
        raise

@celery_app.task(bind=True, name='backend.tasks.processing.process_single_step')
def process_single_step(self, project_id: str, step: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    processingENtask
    
    Args:
        project_id: projectID
        step: EN
        config: processingconfig
        
    Returns:
        processingresult
    """
    task_id = self.request.id
    logger.info(f"startprocessingEN: {project_id}, EN: {step}, taskID: {task_id}")
    
    try:
        # sendstartEN
        # sendprocessingstartEN（EN） - ENWebSocketEN
        # run_async_notification(
        #     notification_service.send_processing_start(project_id, task_id)
        # )
        
        # createdatabaseEN
        db = SessionLocal()
        
        try:
            # createprocessingservice
            processing_service = ProcessingService(db)
            
            # ENexecuteENprocessing
            if step == "outline":
                run_async_notification(
                    notification_service.send_processing_progress(project_id, task_id, 50, "generateEN")
                )
                result = processing_service.generate_outline(project_id, config)
                
            elif step == "timeline":
                run_async_notification(
                    notification_service.send_processing_progress(project_id, task_id, 50, "ENtimeEN")
                )
                result = processing_service.extract_timeline(project_id, config)
                
            elif step == "titles":
                run_async_notification(
                    notification_service.send_processing_progress(project_id, task_id, 50, "generatetitle")
                )
                result = processing_service.generate_titles(project_id, config)
                
            elif step == "clips":
                run_async_notification(
                    notification_service.send_processing_progress(project_id, task_id, 50, "videoclip")
                )
                result = processing_service.extract_clips(project_id, config)
                
            elif step == "collections":
                run_async_notification(
                    notification_service.send_processing_progress(project_id, task_id, 50, "generatecollection")
                )
                result = processing_service.generate_collections(project_id, config)
                
            else:
                raise Exception(f"EN: {step}")
            
            if not result.get("success"):
                raise Exception(f"EN {step} processingfailed: {result.get('error')}")
            
            # sendEN
            run_async_notification(
                notification_service.send_processing_complete(project_id, task_id, result)
            )
            
            logger.info(f"ENprocessingEN: {project_id}, EN: {step}")
            return result
            
        finally:
            db.close()
            
    except Exception as e:
        error_msg = f"ENprocessingfailed: {str(e)}"
        logger.error(error_msg)
        
        # senderrorEN
        run_async_notification(
            notification_service.send_processing_error(project_id, task_id, error_msg)
        )
        
        raise

@celery_app.task(bind=True, name='backend.tasks.processing.retry_processing_step')
def retry_processing_step(self, project_id: str, step: str, config: Dict[str, Any], 
                         original_task_id: str) -> Dict[str, Any]:
    """
    retryprocessingENtask
    
    Args:
        project_id: projectID
        step: EN
        config: processingconfig
        original_task_id: ENtaskID
        
    Returns:
        processingresult
    """
    task_id = self.request.id
    logger.info(f"startretryprocessingEN: {project_id}, EN: {step}, taskID: {task_id}")
    
    try:
        # sendstartEN
        # sendprocessingstartEN（EN） - ENWebSocketEN
        # run_async_notification(
        #     notification_service.send_processing_start(project_id, task_id)
        # )
        
        # sendretryEN
        run_async_notification(
            notification_service.send_system_notification(
                "retry_started",
                "retrystart",
                f"currentlyretryEN: {step}",
                "warning"
            )
        )
        
        # callENprocessing
        result = process_single_step.apply_async(
            args=[project_id, step, config],
            task_id=task_id
        ).get()
        
        # sendretrysucceededEN
        run_async_notification(
            notification_service.send_system_notification(
                "retry_success",
                "retrysucceeded",
                f"EN {step} retrysucceeded",
                "success"
            )
        )
        
        return result
        
    except Exception as e:
        error_msg = f"retryprocessingENfailed: {str(e)}"
        logger.error(error_msg)
        
        # sendretryfailedEN
        run_async_notification(
            notification_service.send_error_notification(
                "retry_failed",
                f"EN {step} retryfailed",
                {"project_id": project_id, "step": step, "error": str(e)}
            )
        )
        
        raise
