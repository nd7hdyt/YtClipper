"""
translatedstartservice
translatedprojectcreatetranslatedstartvideoprocesstranslated
"""

import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal
from backend.models.project import Project, ProjectStatus
from backend.models.task import Task, TaskStatus
from backend.services.progress_update_service import progress_update_service
# from backend.services.pipeline_adapter import PipelineAdapter  # translated，file not found
from backend.utils.task_submission_utils import submit_video_pipeline_task

logger = logging.getLogger(__name__)

class AutoPipelineService:
    """translatedstartservice"""
    
    def __init__(self):
        self.processing_projects = set()
    
    async def auto_start_pipeline(self, project_id: str) -> Dict[str, Any]:
        """
        translatedstartprojecttranslatedprocess
        
        Args:
            project_id: projectID
            
        Returns:
            starttranslated
        """
        try:
            logger.info(f"translatedstartprojecttranslated: {project_id}")
            
            # checkprojectIstranslatedinprocessing
            if project_id in self.processing_projects:
                logger.warning(f"project {project_id} translatedinprocessing，skip")
                return {"status": "skipped", "message": "projecttranslatedinprocessing"}
            
            # translatedprojecttranslatedprocessing
            self.processing_projects.add(project_id)
            
            # fetchprojectinfo
            db = SessionLocal()
            try:
                project = db.query(Project).filter(Project.id == project_id).first()
                if not project:
                    raise ValueError(f"project {project_id} not found")
                
                # checkprojectstatus
                if project.status != ProjectStatus.PtranslatedDING:
                    logger.info(f"project {project_id} statustranslated {project.status}，skiptranslatedstart")
                    return {"status": "skipped", "message": f"projectstatustranslated {project.status}"}
                
                # checkprojectfile
                if not project.video_path:
                    raise ValueError(f"project {project_id} translatedvideofile")
                
                # translatedsubtitlesfile
                srt_file = self._find_srt_file(project_id)
                if not srt_file:
                    logger.warning(f"project {project_id} translatedsubtitlesfile，translated")
                
                # checkIstranslatedintranslated'stask
                existing_task = db.query(Task).filter(
                    Task.project_id == project_id,
                    Task.name == "translatedvideoprocesstranslated",
                    Task.status.in_([TaskStatus.PtranslatedDING, TaskStatus.RUNNING])
                ).first()
                
                if existing_task:
                    # usetranslatedtask
                    task = existing_task
                    logger.info(f"usetranslatedtask: {task.id}")
                else:
                    # createtranslatedtasktranslated
                    task = self._create_processing_task(db, project_id)
                    if not task:
                        raise ValueError("createtasktranslatedfailed")
                
                # updateprojectstatus
                project.status = ProjectStatus.PROCESSING
                project.updated_at = datetime.utcnow()
                db.commit()
                
                logger.info(f"project {project_id} statustranslatedupdatetranslatedprocessing")
                
                # startprogressmonitor
                await progress_update_service.start_progress_monitoring(task.id)
                
                # translatedCelerytask
                logger.info(f"translatedCelerytask: {project_id}")
                
                # translatedprojectfile path
                from ..core.config import get_data_directory
                data_dir = get_data_directory()
                project_dir = Path(data_dir) / "projects" / project_id
                input_video_path = str(project_dir / "raw" / "input.mp4")
                input_srt_path = str(project_dir / "raw" / "input.srt")
                
                # checkfileIstranslatedin
                if not Path(input_video_path).exists():
                    raise ValueError(f"videofile not found: {input_video_path}")
                
                logger.info(f"videofile: {input_video_path}")
                logger.info(f"subtitlesfile: {input_srt_path if Path(input_srt_path).exists() else 'not found'}")
                
                # translatedCelerytask
                task_result = submit_video_pipeline_task(project_id, input_video_path, input_srt_path)
                logger.info(f"Celerytasktranslated: {task_result}")
                
                if task_result.get('success'):
                    celery_task_id = task_result['task_id']
                    logger.info(f"Celerytasktranslated: {celery_task_id}")
                    
                    # updatetasktranslated
                    task.celery_task_id = celery_task_id
                    task.status = TaskStatus.RUNNING
                    task.started_at = datetime.utcnow()
                    db.commit()
                    
                    result = {
                        "status": "started",
                        "message": "translatedprocesstranslatedstart",
                        "project_id": project_id,
                        "task_id": task.id,
                        "celery_task_id": celery_task_id
                    }
                else:
                    error_msg = task_result.get('error', 'translatederror')
                    raise ValueError(f"translatedCelerytaskfailed: {error_msg}")
                
                return result
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"translatedstarttranslatedfailed: {e}")
            # translatedprocessingtranslated
            self.processing_projects.discard(project_id)
            
            # updateprojectstatustranslatedfailed
            await self._mark_project_failed(project_id, str(e))
            
            return {"status": "failed", "message": f"startfailed: {str(e)}"}
    
    def _find_srt_file(self, project_id: str) -> Optional[str]:
        """translatedproject'ssubtitlesfile"""
        try:
            from ..core.path_utils import get_project_directory
            project_dir = get_project_directory(project_id)
            
            # translatedcantranslated'ssubtitlesfile
            srt_files = list(project_dir.glob("**/*.srt"))
            if srt_files:
                return str(srt_files[0])
            
            # translateddirectory
            raw_dir = project_dir / "raw"
            if raw_dir.exists():
                srt_files = list(raw_dir.glob("*.srt"))
                if srt_files:
                    return str(srt_files[0])
            
            return None
            
        except Exception as e:
            logger.warning(f"translatedsubtitlesfilefailed: {e}")
            return None
    
    def _create_processing_task(self, db: Session, project_id: str) -> Optional[Task]:
        """createprocesstasktranslated"""
        try:
            task = Task(
                project_id=project_id,
                name="translatedvideoprocesstranslated",
                task_type="video_processing",
                status=TaskStatus.PtranslatedDING,
                progress=0.0,
                current_step="translated",
                priority=0,
                metadata={
                    "auto_started": True,
                    "started_at": datetime.utcnow().isoformat()
                }
            )
            
            db.add(task)
            db.commit()
            db.refresh(task)
            
            logger.info(f"createprocesstask: {task.id}")
            return task
            
        except Exception as e:
            logger.error(f"createtasktranslatedfailed: {e}")
            db.rollback()
            return None
    
    async def _mark_project_failed(self, project_id: str, error_message: str):
        """translatedprojecttranslatedfailedstatus"""
        try:
            db = SessionLocal()
            try:
                project = db.query(Project).filter(Project.id == project_id).first()
                if project:
                    project.status = ProjectStatus.FAILED
                    project.updated_at = datetime.utcnow()
                    db.commit()
                    logger.info(f"project {project_id} translatedfailed")
                    
                    # fromprocessingprojecttranslated
                    self.processing_projects.discard(project_id)
                    logger.info(f"project {project_id} translatedfromprocessingtranslated")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"translatedprojectfailedstatustranslated: {e}")
    
    async def check_and_restart_failed_pipelines(self):
        """checktranslatedfailed'stranslated"""
        try:
            db = SessionLocal()
            try:
                # translatedfailed'sproject
                failed_projects = db.query(Project).filter(
                    Project.status == ProjectStatus.FAILED
                ).all()
                
                for project in failed_projects:
                    logger.info(f"checkfailedproject: {project.id}")
                    
                    # checkIstranslated'stask
                    incomplete_tasks = db.query(Task).filter(
                        Task.project_id == project.id,
                        Task.status.in_([TaskStatus.PtranslatedDING, TaskStatus.RUNNING])
                    ).all()
                    
                    if not incomplete_tasks:
                        logger.info(f"project {project.id} translatedtask，translated")
                        await self.auto_start_pipeline(project.id)
                    else:
                        logger.info(f"project {project.id} translatedtask，skiptranslated")
                        
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"checkfailedtranslated: {e}")
    
    async def auto_start_all_pending_pipelines(self):
        """translatedstarttranslatedetc.translated'stranslated"""
        try:
            db = SessionLocal()
            try:
                # translatedetc.translated'sproject
                pending_projects = db.query(Project).filter(
                    Project.status == ProjectStatus.PtranslatedDING
                ).all()
                
                logger.info(f"translated {len(pending_projects)}  etc.translated'sproject")
                
                for project in pending_projects:
                    try:
                        logger.info(f"translatedstartprojecttranslated: {project.id}")
                        result = await self.auto_start_pipeline(project.id)
                        logger.info(f"project {project.id} starttranslated: {result}")
                        
                        # translatedstarttranslatedmultiproject
                        await asyncio.sleep(1)
                        
                    except Exception as e:
                        logger.error(f"translatedstartproject {project.id} failed: {e}")
                        continue
                        
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"translatedstarttranslatedetc.translated: {e}")
    
    def get_processing_status(self) -> Dict[str, Any]:
        """fetchprocessstatus"""
        return {
            "processing_projects": list(self.processing_projects),
            "total_processing": len(self.processing_projects)
        }

# translated
auto_pipeline_service = AutoPipelineService()
