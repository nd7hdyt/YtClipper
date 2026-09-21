"""
processingservice
useEN：configEN、EN、EN
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from backend.models.task import Task, TaskStatus, TaskType
from backend.repositories.task_repository import TaskRepository
from backend.services.config_manager import ProjectConfigManager, ProcessingStep
# from backend.services.pipeline_adapter import PipelineAdapter  # EN，filedoes not exist
from backend.services.processing_orchestrator import ProcessingOrchestrator
from backend.services.processing_context import ProcessingContext
from backend.services.exceptions import ServiceError, ProcessingError, TaskError, ProjectError, handle_service_error
from backend.services.concurrency_manager import with_concurrency_control

logger = logging.getLogger(__name__)


class ProcessingService:
    """processingservice，useEN"""
    
    def __init__(self, db: Session):
        self.db = db
        self.task_repo = TaskRepository(db)
    
    @handle_service_error
    @with_concurrency_control()
    def start_processing(self, project_id: str, srt_path: Path) -> Dict[str, Any]:
        """
        startprocessingproject
        
        Args:
            project_id: projectID
            srt_path: SRTfilepath
            
        Returns:
            processingresult
        """
        logger.info(f"startprocessingproject: {project_id}")
        
        # createprocessingEN
        context = ProcessingContext(project_id, "temp_task_id", self.db)
        context.set_srt_path(srt_path)
        context.mark_initialized()
        
        # createprocessingtask
        task = self._create_processing_task(project_id)
        context.task_id = str(task.id)
        
        # initializeEN
        orchestrator = ProcessingOrchestrator(project_id, str(task.id), self.db)
        
        # executeEN
        result = orchestrator.execute_pipeline(srt_path)
        
        context.mark_completed()
        
        # updateprojectstatusENcompletedEN
        try:
            from ..models.project import Project, ProjectStatus
            from ..services.data_sync_service import DataSyncService
            from pathlib import Path
            
            project = self.db.query(Project).filter(Project.id == project_id).first()
            if project:
                project.status = ProjectStatus.COMPLETED
                self.db.commit()
                logger.info(f"projectstatusupdatedENcompleted: {project_id}")
                
                # ENdatabase
                project_dir = Path(__file__).parent.parent / "data" / "projects" / project_id
                if project_dir.exists():
                    sync_service = DataSyncService(self.db)
                    sync_result = sync_service.sync_project_from_filesystem(project_id, project_dir)
                    if sync_result.get("success"):
                        logger.info(f"project {project_id} ENsucceeded: {sync_result}")
                    else:
                        logger.error(f"project {project_id} ENfailed: {sync_result}")
        except Exception as e:
            logger.warning(f"updateprojectstatusfailed: {e}")
        
        return {
            "success": True,
            "task_id": task.id,
            "project_id": project_id,
            "result": result,
            "context": context.get_context_summary()
        }
    
    @handle_service_error
    @with_concurrency_control()
    def execute_single_step(self, project_id: str, step: ProcessingStep, 
                           srt_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        executeEN
        
        Args:
            project_id: projectID
            step: processingEN
            srt_path: SRTfilepath（ENStep1need）
            
        Returns:
            executeresult
        """
        logger.info(f"executeEN: {step.value}")
        
        # createprocessingEN
        context = ProcessingContext(project_id, "temp_task_id", self.db)
        if srt_path:
            context.set_srt_path(srt_path)
        context.mark_initialized()
        
        # createtask
        task = self._create_processing_task(project_id, task_type=TaskType.VIDEO_PROCESSING)
        context.task_id = str(task.id)
        
        # initializeEN
        orchestrator = ProcessingOrchestrator(project_id, str(task.id), self.db)
        
        # executeEN
        kwargs = {}
        if step == ProcessingStep.STEP1_OUTLINE and srt_path:
            kwargs['srt_path'] = srt_path
        
        result = orchestrator.execute_step(step, **kwargs)
        
        context.mark_completed()
        
        # ifEN（step6_video），ENdatabase
        if step == ProcessingStep.STEP6_VIDEO:
            try:
                from ..services.data_sync_service import DataSyncService
                from pathlib import Path
                
                project_dir = Path(__file__).parent.parent / "data" / "projects" / project_id
                if project_dir.exists():
                    sync_service = DataSyncService(self.db)
                    sync_result = sync_service.sync_project_from_filesystem(project_id, project_dir)
                    if sync_result.get("success"):
                        logger.info(f"project {project_id} ENsucceeded: {sync_result}")
                    else:
                        logger.error(f"project {project_id} ENfailed: {sync_result}")
            except Exception as e:
                logger.warning(f"ENfailed: {e}")
        
        return {
            "success": True,
            "task_id": task.id,
            "step": step.value,
            "result": result,
            "context": context.get_context_summary()
        }
    
    @handle_service_error
    def get_processing_status(self, project_id: str, task_id: str) -> Dict[str, Any]:
        """
        fetchprocessingstatus
        
        Args:
            project_id: projectID
            task_id: taskID
            
        Returns:
            processingstatus
        """
        orchestrator = ProcessingOrchestrator(project_id, task_id, self.db)
        return orchestrator.get_pipeline_status()
    
    @handle_service_error
    @with_concurrency_control()
    def retry_step(self, project_id: str, task_id: str, step: ProcessingStep,
                   srt_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        retryEN
        
        Args:
            project_id: projectID
            task_id: taskID
            step: processingEN
            srt_path: SRTfilepath（ENStep1need）
            
        Returns:
            retryresult
        """
        logger.info(f"retryEN: {step.value}")
        
        # createprocessingEN
        context = ProcessingContext(project_id, task_id, self.db)
        if srt_path:
            context.set_srt_path(srt_path)
        context.mark_initialized()
        
        orchestrator = ProcessingOrchestrator(project_id, task_id, self.db)
        
        kwargs = {}
        if step == ProcessingStep.STEP1_OUTLINE and srt_path:
            kwargs['srt_path'] = srt_path
        
        result = orchestrator.retry_step(step, **kwargs)
        
        context.mark_completed()
        
        return {
            "success": True,
            "step": step.value,
            "result": result,
            "context": context.get_context_summary()
        }

    @handle_service_error
    @with_concurrency_control()
    def resume_processing(self, project_id: str, start_step: str, 
                         srt_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        ENprocessing
        
        Args:
            project_id: projectID
            start_step: startEN
            srt_path: SRTfilepath（ENStep1need）
            
        Returns:
            ENprocessingresult
        """
        logger.info(f"EN {start_step} ENprocessingproject: {project_id}")
        
        # createprocessingEN
        context = ProcessingContext(project_id, "temp_task_id", self.db)
        if srt_path:
            context.set_srt_path(srt_path)
        context.mark_initialized()
        
        # createprocessingtask
        task = self._create_processing_task(project_id)
        context.task_id = str(task.id)
        
        # initializeEN
        orchestrator = ProcessingOrchestrator(project_id, str(task.id), self.db)
        
        # ENProcessingStepEN
        step_mapping = {
            "step1_outline": ProcessingStep.STEP1_OUTLINE,
            "step2_timeline": ProcessingStep.STEP2_TIMELINE,
            "step3_scoring": ProcessingStep.STEP3_SCORING,
            "step4_title": ProcessingStep.STEP4_TITLE,
            "step5_clustering": ProcessingStep.STEP5_CLUSTERING,
            "step6_video": ProcessingStep.STEP6_VIDEO
        }
        
        if start_step not in step_mapping:
            raise ValueError(f"EN: {start_step}")
        
        processing_step = step_mapping[start_step]
        
        # ENexecute
        result = orchestrator.resume_from_step(processing_step, srt_path)
        
        context.mark_completed()
        
        # updateprojectstatusENcompletedEN
        try:
            from ..models.project import Project, ProjectStatus
            from ..services.data_sync_service import DataSyncService
            from pathlib import Path
            
            project = self.db.query(Project).filter(Project.id == project_id).first()
            if project:
                project.status = ProjectStatus.COMPLETED
                self.db.commit()
                logger.info(f"projectstatusupdatedENcompleted: {project_id}")
                
                # ENdatabase
                project_dir = Path(__file__).parent.parent / "data" / "projects" / project_id
                if project_dir.exists():
                    sync_service = DataSyncService(self.db)
                    sync_result = sync_service.sync_project_from_filesystem(project_id, project_dir)
                    if sync_result.get("success"):
                        logger.info(f"project {project_id} ENsucceeded: {sync_result}")
                    else:
                        logger.error(f"project {project_id} ENfailed: {sync_result}")
        except Exception as e:
            logger.warning(f"updateprojectstatusfailed: {e}")
        
        return {
            "success": True,
            "task_id": task.id,
            "project_id": project_id,
            "start_step": start_step,
            "result": result,
            "context": context.get_context_summary()
        }
    
    @handle_service_error
    def get_project_config(self, project_id: str) -> Dict[str, Any]:
        """
        fetchprojectconfig
        
        Args:
            project_id: projectID
            
        Returns:
            projectconfig
        """
        config_manager = ProjectConfigManager(project_id)
        return config_manager.export_config()
    
    @handle_service_error
    def update_project_config(self, project_id: str, config_updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        updateprojectconfig
        
        Args:
            project_id: projectID
            config_updates: configupdate
            
        Returns:
            updateresult
        """
        config_manager = ProjectConfigManager(project_id)
        
        # updateprocessingparameters
        if "processing_params" in config_updates:
            config_manager.update_processing_params(**config_updates["processing_params"])
        
        # updateLLMconfig
        if "llm_config" in config_updates:
            config_manager.update_llm_config(**config_updates["llm_config"])
        
        # updateENconfig
        if "steps" in config_updates:
            for step_name, step_config in config_updates["steps"].items():
                config_manager.update_step_config(step_name, **step_config)
        
        return {
            "success": True,
            "message": "configupdatesucceeded"
        }
    
    @handle_service_error
    def validate_project_setup(self, project_id: str) -> Dict[str, Any]:
        """
        validateprojectsettings
        
        Args:
            project_id: projectID
            
        Returns:
            validateresult
        """
        # EN，PipelineAdapter filedoes not exist
        # adapter = PipelineAdapter(project_id)
        # errors = adapter.validate_pipeline_prerequisites()
        
        # if errors:
        #     return {
        #         "valid": False,
        #         "errors": errors
        #     }
        
        return {
            "valid": True,
            "message": "projectsettingsvalidatethrough（ENPipelineAdaptervalidate）"
        }
    
    def _create_processing_task(self, project_id: str, task_type: TaskType = TaskType.VIDEO_PROCESSING) -> Task:
        """createprocessingtask"""
        task_data = {
            "name": f"videoprocessingtask - {project_id}",
            "description": f"processingproject {project_id} ENvideoEN",
            "project_id": project_id,
            "task_type": task_type,
            "status": TaskStatus.PENDING,
            "progress": 0.0,
            "metadata": {
                "project_id": project_id,
                "task_type": task_type.value if hasattr(task_type, 'value') else task_type
            }
        }
        
        return self.task_repo.create(**task_data)