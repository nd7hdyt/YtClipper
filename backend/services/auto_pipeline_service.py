"""
ENstartservice
whenENprojectcreateENstartvideoprocessingEN
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
# from backend.services.pipeline_adapter import PipelineAdapter  # EN，filedoes not exist
from backend.utils.task_submission_utils import submit_video_pipeline_task

logger = logging.getLogger(__name__)

class AutoPipelineService:
    """ENstartservice"""
    
    def __init__(self):
        self.processing_projects = set()
    
    async def auto_start_pipeline(self, project_id: str) -> Dict[str, Any]:
        """
        ENstartprojectENprocessing
        
        Args:
            project_id: projectID
            
        Returns:
            startresult
        """
        try:
            logger.info(f"ENstartprojectEN: {project_id}")
            
            # checkprojectENalreadyENprocessing
            if project_id in self.processing_projects:
                logger.warning(f"project {project_id} ENprocessing，EN")
                return {"status": "skipped", "message": "projectENprocessing"}
            
            # ENprojectENprocessing
            self.processing_projects.add(project_id)
            
            # fetchprojectEN
            db = SessionLocal()
            try:
                project = db.query(Project).filter(Project.id == project_id).first()
                if not project:
                    raise ValueError(f"project {project_id} does not exist")
                
                # checkprojectstatus
                if project.status != ProjectStatus.PENDING:
                    logger.info(f"project {project_id} statusEN {project.status}，ENstart")
                    return {"status": "skipped", "message": f"projectstatusEN {project.status}"}
                
                # checkprojectfile
                if not project.video_path:
                    raise ValueError(f"project {project_id} ENvideofile")
                
                # ENsubtitlesfile
                srt_file = self._find_srt_file(project_id)
                if not srt_file:
                    logger.warning(f"project {project_id} ENsubtitlesfile，ENgenerate")
                
                # checkENcurrentlyrunENtask
                existing_task = db.query(Task).filter(
                    Task.project_id == project_id,
                    Task.name == "ENvideoprocessingEN",
                    Task.status.in_([TaskStatus.PENDING, TaskStatus.RUNNING])
                ).first()
                
                if existing_task:
                    # useENtask
                    task = existing_task
                    logger.info(f"useENtask: {task.id}")
                else:
                    # createENtaskEN
                    task = self._create_processing_task(db, project_id)
                    if not task:
                        raise ValueError("createtaskENfailed")
                
                # updateprojectstatus
                project.status = ProjectStatus.PROCESSING
                project.updated_at = datetime.utcnow()
                db.commit()
                
                logger.info(f"project {project_id} statusupdatedENprocessing")
                
                # startprogressEN
                await progress_update_service.start_progress_monitoring(task.id)
                
                # ENCelerytask
                logger.info(f"ENCelerytask: {project_id}")
                
                # ENprojectfilepath
                from ..core.config import get_data_directory
                data_dir = get_data_directory()
                project_dir = Path(data_dir) / "projects" / project_id
                input_video_path = str(project_dir / "raw" / "input.mp4")
                input_srt_path = str(project_dir / "raw" / "input.srt")
                
                # checkfileEN
                if not Path(input_video_path).exists():
                    raise ValueError(f"videofiledoes not exist: {input_video_path}")
                
                logger.info(f"videofile: {input_video_path}")
                logger.info(f"subtitlesfile: {input_srt_path if Path(input_srt_path).exists() else 'does not exist'}")
                
                # ENCelerytask
                task_result = submit_video_pipeline_task(project_id, input_video_path, input_srt_path)
                logger.info(f"CelerytaskENresult: {task_result}")
                
                if task_result.get('success'):
                    celery_task_id = task_result['task_id']
                    logger.info(f"CelerytaskEN: {celery_task_id}")
                    
                    # updatetaskEN
                    task.celery_task_id = celery_task_id
                    task.status = TaskStatus.RUNNING
                    task.started_at = datetime.utcnow()
                    db.commit()
                    
                    result = {
                        "status": "started",
                        "message": "ENprocessingENstart",
                        "project_id": project_id,
                        "task_id": task.id,
                        "celery_task_id": celery_task_id
                    }
                else:
                    error_msg = task_result.get('error', 'Unknown error')
                    raise ValueError(f"ENCelerytaskfailed: {error_msg}")
                
                return result
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"ENstartENfailed: {e}")
            # ENprocessingEN
            self.processing_projects.discard(project_id)
            
            # updateprojectstatusENfailed
            await self._mark_project_failed(project_id, str(e))
            
            return {"status": "failed", "message": f"startfailed: {str(e)}"}
    
    def _find_srt_file(self, project_id: str) -> Optional[str]:
        """ENprojectENsubtitlesfile"""
        try:
            from ..core.path_utils import get_project_directory
            project_dir = get_project_directory(project_id)
            
            # ENmayENsubtitlesfile
            srt_files = list(project_dir.glob("**/*.srt"))
            if srt_files:
                return str(srt_files[0])
            
            # ENdirectory
            raw_dir = project_dir / "raw"
            if raw_dir.exists():
                srt_files = list(raw_dir.glob("*.srt"))
                if srt_files:
                    return str(srt_files[0])
            
            return None
            
        except Exception as e:
            logger.warning(f"ENsubtitlesfilefailed: {e}")
            return None
    
    def _create_processing_task(self, db: Session, project_id: str) -> Optional[Task]:
        """createprocessingtaskEN"""
        try:
            task = Task(
                project_id=project_id,
                name="ENvideoprocessingEN",
                task_type="video_processing",
                status=TaskStatus.PENDING,
                progress=0.0,
                current_step="initialize",
                priority=0,
                metadata={
                    "auto_started": True,
                    "started_at": datetime.utcnow().isoformat()
                }
            )
            
            db.add(task)
            db.commit()
            db.refresh(task)
            
            logger.info(f"createprocessingtask: {task.id}")
            return task
            
        except Exception as e:
            logger.error(f"createtaskENfailed: {e}")
            db.rollback()
            return None
    
    async def _mark_project_failed(self, project_id: str, error_message: str):
        """ENprojectENfailedstatus"""
        try:
            db = SessionLocal()
            try:
                project = db.query(Project).filter(Project.id == project_id).first()
                if project:
                    project.status = ProjectStatus.FAILED
                    project.updated_at = datetime.utcnow()
                    db.commit()
                    logger.info(f"project {project_id} ENfailed")
                    
                    # ENprocessingprojectEN
                    self.processing_projects.discard(project_id)
                    logger.info(f"project {project_id} ENprocessingEN")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"ENprojectfailedstatusEN: {e}")
    
    async def check_and_restart_failed_pipelines(self):
        """checkENrestartfailedEN"""
        try:
            db = SessionLocal()
            try:
                # ENfailedENproject
                failed_projects = db.query(Project).filter(
                    Project.status == ProjectStatus.FAILED
                ).all()
                
                for project in failed_projects:
                    logger.info(f"checkfailedproject: {project.id}")
                    
                    # checkENtask
                    incomplete_tasks = db.query(Task).filter(
                        Task.project_id == project.id,
                        Task.status.in_([TaskStatus.PENDING, TaskStatus.RUNNING])
                    ).all()
                    
                    if not incomplete_tasks:
                        logger.info(f"project {project.id} ENtask，ENrestart")
                        await self.auto_start_pipeline(project.id)
                    else:
                        logger.info(f"project {project.id} ENtask，ENrestart")
                        
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"checkfailedEN: {e}")
    
    async def auto_start_all_pending_pipelines(self):
        """ENstartallEN"""
        try:
            db = SessionLocal()
            try:
                # ENallENproject
                pending_projects = db.query(Project).filter(
                    Project.status == ProjectStatus.PENDING
                ).all()
                
                logger.info(f"EN {len(pending_projects)} ENproject")
                
                for project in pending_projects:
                    try:
                        logger.info(f"ENstartprojectEN: {project.id}")
                        result = await self.auto_start_pipeline(project.id)
                        logger.info(f"project {project.id} startresult: {result}")
                        
                        # ENmeanwhilestartENproject
                        await asyncio.sleep(1)
                        
                    except Exception as e:
                        logger.error(f"ENstartproject {project.id} failed: {e}")
                        continue
                        
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"ENstartallEN: {e}")
    
    def get_processing_status(self) -> Dict[str, Any]:
        """fetchprocessingstatus"""
        return {
            "processing_projects": list(self.processing_projects),
            "total_processing": len(self.processing_projects)
        }

# EN
auto_pipeline_service = AutoPipelineService()
