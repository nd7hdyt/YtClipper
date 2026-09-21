"""videoprocessCelerytask
PackageincludeWebSockettranslatedAndPipelinetranslated
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
    """translated'stranslated - fixedtranslated"""
    try:
        # translatedfetchtranslated'stranslated
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # iftranslatedintranslated，usetranslated
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
                return future.result(timeout=10)  # 10secondstranslated
        else:
            # iftranslated，translated
            return loop.run_until_complete(coro)
    except RuntimeError:
        # translated，createtranslated's
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

# translatedoneprojecttranslatedonetranslatedonetranslatedintranslated。translatedmulti translated（/process、/retry、
# frontendtranslatedstart、downloadtranslatedstart）cantranslatedoneproject，translatedtasktranslated Redis translated
# Sotranslated；translatedintasktranslated'stranslatedlocaltranslated，translateddatabase。
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
    processvideotranslatedtask - usePipelinetranslated
    
    Args:
        project_id: projectID
        input_video_path: translatedvideopath
        input_srt_path: translatedSRTpath
        
    Returns:
        processtranslated
    """
    task_id = self.request.id
    logger.info(f"translatedprocessvideotranslated: {project_id}, taskID: {task_id}")

    # translated：translatedoneprojecttranslatedintranslatedskiptranslated
    with _active_pipeline_lock:
        if project_id in _active_pipeline_projects:
            logger.warning(f"project {project_id} translatedintranslated，skiptranslatedtask {task_id}")
            return {
                "success": False,
                "skipped": True,
                "project_id": project_id,
                "task_id": task_id,
                "message": "translatedintranslated，translatedskiptranslatedtask",
            }
        _active_pipeline_projects.add(project_id)

    try:
        # createdatabasetranslated
        db = SessionLocal()
        
        try:
            # createtasktranslated
            task = Task(
                name=f"videoprocesstranslated",
                description=f"processproject {project_id} 'stranslatedvideotranslated",
                task_type=TaskType.VIDEO_PROCESSING,
                project_id=project_id,
                celery_task_id=task_id,
                status=TaskStatus.RUNNING,
                progress=0,
                current_step="translated",
                total_steps=6
            )
            db.add(task)
            db.commit()
            
            # translated
            run_async_notification(
                notification_service.send_processing_start(project_id, task_id)
            )
            
            # translated'sprogressSystemNo needtranslated'stranslated
            # translated'sprogressSystemtranslatedintranslatedprogresstranslated
            
            # usetranslated'sPipelinetranslated
            from backend.services.simple_pipeline_adapter import create_simple_pipeline_adapter
            pipeline_adapter = create_simple_pipeline_adapter(str(project_id), str(task.id))
            
            # translatedPipelineprocess - usetranslatedPackagetranslated
            import asyncio
            result = asyncio.run(pipeline_adapter.process_project_sync(input_video_path, input_srt_path))
            
            # checkprocesstranslated
            if result.get("status") == "failed":
                # processing failed。adapter return'sIs error（translatedthistranslated message，usertranslated'stranslatedIs「processing failed」translated translated）
                error_msg = result.get("error") or result.get("message") or "processing failed"
                task.status = TaskStatus.FAILED
                task.error_message = error_msg
                if result.get("stage"):
                    task.current_step = f"failedtranslated {result['stage']}"
                task.result_data = result
                
                # updateprojectstatustranslatedfailed
                project = db.query(Project).filter(Project.id == project_id).first()
                if project:
                    project.status = ProjectStatus.FAILED
                    project.updated_at = datetime.utcnow()
                    logger.info(f"projectstatustranslatedupdatetranslatedfailed: {project_id}")
                
                db.commit()
                
                # failedstatustranslatedprogressSystemtranslatedprocess
                
                # translatederrortranslated（translatedversion） - translateduseWebSockettranslated
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
                # processsucceeded
                task.status = TaskStatus.COMPLETED
                task.progress = 100
                task.current_step = "processing completed"
                task.result_data = result
                
                # updateprojectstatustranslatedcompleted
                project = db.query(Project).filter(Project.id == project_id).first()
                if project:
                    project.status = ProjectStatus.COMPLETED
                    project.completed_at = datetime.utcnow()
                    project.updated_at = datetime.utcnow()
                    logger.info(f"projectstatustranslatedupdatetranslatedcompleted: {project_id}")
                
                db.commit()
                
                # translatedstatustranslatedprogressSystemtranslatedprocess
                
                # translated（translatedversion） - translateduseWebSockettranslated
                # run_async_notification(
                #     notification_service.send_processing_complete(project_id, task_id, result)
                # )
            
            logger.info(f"videotranslatedprocessing completed: {project_id}")
            return {
                "success": True,
                "project_id": project_id,
                "task_id": task_id,
                "result": result,
                "message": "videoprocesstranslated"
            }
            
        finally:
            db.close()
            # translated（translatedsucceeded/failed/translatedreturntranslatedthistranslated）
            with _active_pipeline_lock:
                _active_pipeline_projects.discard(project_id)

    except Exception as e:
        error_msg = f"videotranslatedprocessing failed: {str(e)}"
        logger.error(error_msg)

        # translated（translatedpathtranslatedintranslated finally translated，thistranslated）
        with _active_pipeline_lock:
            _active_pipeline_projects.discard(project_id)

        # updatetaskstatustranslatedfailed
        try:
            db = SessionLocal()
            task = db.query(Task).filter(Task.celery_task_id == task_id).first()
            if task:
                task.status = TaskStatus.FAILED
                task.error_message = error_msg
                
                # updateprojectstatustranslatedfailed
                project = db.query(Project).filter(Project.id == project_id).first()
                if project:
                    project.status = ProjectStatus.FAILED
                    project.updated_at = datetime.utcnow()
                    logger.info(f"projectstatustranslatedupdatetranslatedfailed: {project_id}")
                
                db.commit()
            db.close()
        except Exception as db_error:
            logger.error(f"updatetaskstatusfailed: {str(db_error)}")
        
        # translatederrortranslated
        run_async_notification(
            notification_service.send_processing_error(project_id, task_id, error_msg)
        )
        
        raise

@celery_app.task(bind=True, name='backend.tasks.processing.process_single_step')
def process_single_step(self, project_id: str, step: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    processtranslated steptask
    
    Args:
        project_id: projectID
        step: steptranslated
        config: processconfig
        
    Returns:
        processtranslated
    """
    task_id = self.request.id
    logger.info(f"translatedprocesstranslated step: {project_id}, step: {step}, taskID: {task_id}")
    
    try:
        # translated
        # translatedprocesstranslated（translatedversion） - translateduseWebSockettranslated
        # run_async_notification(
        #     notification_service.send_processing_start(project_id, task_id)
        # )
        
        # createdatabasetranslated
        db = SessionLocal()
        
        try:
            # createprocessservice
            processing_service = ProcessingService(db)
            
            # translatedsteptranslated'sprocess
            if step == "outline":
                run_async_notification(
                    notification_service.send_processing_progress(project_id, task_id, 50, "translated")
                )
                result = processing_service.generate_outline(project_id, config)
                
            elif step == "timeline":
                run_async_notification(
                    notification_service.send_processing_progress(project_id, task_id, 50, "translated")
                )
                result = processing_service.extract_timeline(project_id, config)
                
            elif step == "titles":
                run_async_notification(
                    notification_service.send_processing_progress(project_id, task_id, 50, "translated")
                )
                result = processing_service.generate_titles(project_id, config)
                
            elif step == "clips":
                run_async_notification(
                    notification_service.send_processing_progress(project_id, task_id, 50, "videoclip")
                )
                result = processing_service.extract_clips(project_id, config)
                
            elif step == "collections":
                run_async_notification(
                    notification_service.send_processing_progress(project_id, task_id, 50, "translatedcollection")
                )
                result = processing_service.generate_collections(project_id, config)
                
            else:
                raise Exception(f"translated'ssteptranslated: {step}")
            
            if not result.get("success"):
                raise Exception(f"step {step} processing failed: {result.get('error')}")
            
            # translated
            run_async_notification(
                notification_service.send_processing_complete(project_id, task_id, result)
            )
            
            logger.info(f"translated stepprocessing completed: {project_id}, step: {step}")
            return result
            
        finally:
            db.close()
            
    except Exception as e:
        error_msg = f"translated stepprocessing failed: {str(e)}"
        logger.error(error_msg)
        
        # translatederrortranslated
        run_async_notification(
            notification_service.send_processing_error(project_id, task_id, error_msg)
        )
        
        raise

@celery_app.task(bind=True, name='backend.tasks.processing.retry_processing_step')
def retry_processing_step(self, project_id: str, step: str, config: Dict[str, Any], 
                         original_task_id: str) -> Dict[str, Any]:
    """
    translatedprocesssteptask
    
    Args:
        project_id: projectID
        step: steptranslated
        config: processconfig
        original_task_id: translatedtaskID
        
    Returns:
        processtranslated
    """
    task_id = self.request.id
    logger.info(f"translatedprocessstep: {project_id}, step: {step}, taskID: {task_id}")
    
    try:
        # translated
        # translatedprocesstranslated（translatedversion） - translateduseWebSockettranslated
        # run_async_notification(
        #     notification_service.send_processing_start(project_id, task_id)
        # )
        
        # translated
        run_async_notification(
            notification_service.send_system_notification(
                "retry_started",
                "translated",
                f"translatedintranslatedstep: {step}",
                "warning"
            )
        )
        
        # calltranslated stepprocess
        result = process_single_step.apply_async(
            args=[project_id, step, config],
            task_id=task_id
        ).get()
        
        # translatedsucceededtranslated
        run_async_notification(
            notification_service.send_system_notification(
                "retry_success",
                "translatedsucceeded",
                f"step {step} translatedsucceeded",
                "success"
            )
        )
        
        return result
        
    except Exception as e:
        error_msg = f"translatedprocessstepfailed: {str(e)}"
        logger.error(error_msg)
        
        # translatedfailedtranslated
        run_async_notification(
            notification_service.send_error_notification(
                "retry_failed",
                f"step {step} translatedfailed",
                {"project_id": project_id, "step": step, "error": str(e)}
            )
        )
        
        raise
