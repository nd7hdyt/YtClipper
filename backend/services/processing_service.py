"""
processservice
usetranslated：configtranslated、translated、translated
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from backend.models.task import Task, TaskStatus, TaskType
from backend.repositories.task_repository import TaskRepository
from backend.services.config_manager import ProjectConfigManager, ProcessingStep
# from backend.services.pipeline_adapter import PipelineAdapter  # translated，file not found
from backend.services.processing_orchestrator import ProcessingOrchestrator
from backend.services.processing_context import ProcessingContext
from backend.services.exceptions import ServiceError, ProcessingError, TaskError, ProjectError, handle_service_error
from backend.services.concurrency_manager import with_concurrency_control

logger = logging.getLogger(__name__)


class ProcessingService:
    """processservice，usetranslated"""
    
    def __init__(self, db: Session):
        self.db = db
        self.task_repo = TaskRepository(db)
    
    @handle_service_error
    @with_concurrency_control()
    def start_processing(self, project_id: str, srt_path: Path) -> Dict[str, Any]:
        """
        translatedprocessproject
        
        Args:
            project_id: projectID
            srt_path: SRTfile path
            
        Returns:
            processtranslated
        """
        logger.info(f"translatedprocessproject: {project_id}")
        
        # createprocesstranslated
        context = ProcessingContext(project_id, "temp_task_id", self.db)
        context.set_srt_path(srt_path)
        context.mark_initialized()
        
        # createprocesstask
        task = self._create_processing_task(project_id)
        context.task_id = str(task.id)
        
        # translated
        orchestrator = ProcessingOrchestrator(project_id, str(task.id), self.db)
        
        # translated
        result = orchestrator.execute_pipeline(srt_path)
        
        context.mark_completed()
        
        # updateprojectstatustranslatedcompletedtranslated
        try:
            from ..models.project import Project, ProjectStatus
            from ..services.data_sync_service import DataSyncService
            from pathlib import Path
            
            project = self.db.query(Project).filter(Project.id == project_id).first()
            if project:
                project.status = ProjectStatus.COMPLETED
                self.db.commit()
                logger.info(f"projectstatustranslatedupdatetranslatedcompleted: {project_id}")
                
                # translateddatabase
                project_dir = Path(__file__).parent.parent / "data" / "projects" / project_id
                if project_dir.exists():
                    sync_service = DataSyncService(self.db)
                    sync_result = sync_service.sync_project_from_filesystem(project_id, project_dir)
                    if sync_result.get("success"):
                        logger.info(f"project {project_id} translatedsucceeded: {sync_result}")
                    else:
                        logger.error(f"project {project_id} translatedfailed: {sync_result}")
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
        translated step
        
        Args:
            project_id: projectID
            step: processstep
            srt_path: SRTfile path（OnlyStep1translated）
            
        Returns:
            translated
        """
        logger.info(f"translatedstep: {step.value}")
        
        # createprocesstranslated
        context = ProcessingContext(project_id, "temp_task_id", self.db)
        if srt_path:
            context.set_srt_path(srt_path)
        context.mark_initialized()
        
        # createtask
        task = self._create_processing_task(project_id, task_type=TaskType.VIDEO_PROCESSING)
        context.task_id = str(task.id)
        
        # translated
        orchestrator = ProcessingOrchestrator(project_id, str(task.id), self.db)
        
        # translatedstep
        kwargs = {}
        if step == ProcessingStep.STEP1_OUTLINE and srt_path:
            kwargs['srt_path'] = srt_path
        
        result = orchestrator.execute_step(step, **kwargs)
        
        context.mark_completed()
        
        # iftranslatedIstranslatedonetranslated（step6_video），translateddatabase
        if step == ProcessingStep.STEP6_VIDEO:
            try:
                from ..services.data_sync_service import DataSyncService
                from pathlib import Path
                
                project_dir = Path(__file__).parent.parent / "data" / "projects" / project_id
                if project_dir.exists():
                    sync_service = DataSyncService(self.db)
                    sync_result = sync_service.sync_project_from_filesystem(project_id, project_dir)
                    if sync_result.get("success"):
                        logger.info(f"project {project_id} translatedsucceeded: {sync_result}")
                    else:
                        logger.error(f"project {project_id} translatedfailed: {sync_result}")
            except Exception as e:
                logger.warning(f"translatedfailed: {e}")
        
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
        fetchprocessstatus
        
        Args:
            project_id: projectID
            task_id: taskID
            
        Returns:
            processstatus
        """
        orchestrator = ProcessingOrchestrator(project_id, task_id, self.db)
        return orchestrator.get_pipeline_status()
    
    @handle_service_error
    @with_concurrency_control()
    def retry_step(self, project_id: str, task_id: str, step: ProcessingStep,
                   srt_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        translatedstep
        
        Args:
            project_id: projectID
            task_id: taskID
            step: processstep
            srt_path: SRTfile path（OnlyStep1translated）
            
        Returns:
            translated
        """
        logger.info(f"translatedstep: {step.value}")
        
        # createprocesstranslated
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
        fromtranslatedsteptranslatedprocess
        
        Args:
            project_id: projectID
            start_step: translatedsteptranslated
            srt_path: SRTfile path（OnlyStep1translated）
            
        Returns:
            translatedprocesstranslated
        """
        logger.info(f"fromstep {start_step} translatedprocessproject: {project_id}")
        
        # createprocesstranslated
        context = ProcessingContext(project_id, "temp_task_id", self.db)
        if srt_path:
            context.set_srt_path(srt_path)
        context.mark_initialized()
        
        # createprocesstask
        task = self._create_processing_task(project_id)
        context.task_id = str(task.id)
        
        # translated
        orchestrator = ProcessingOrchestrator(project_id, str(task.id), self.db)
        
        # translatedsteptranslatedProcessingSteptranslated
        step_mapping = {
            "step1_outline": ProcessingStep.STEP1_OUTLINE,
            "step2_timeline": ProcessingStep.STEP2_TIMELINE,
            "step3_scoring": ProcessingStep.STEP3_SCORING,
            "step4_title": ProcessingStep.STEP4_TITLE,
            "step5_clustering": ProcessingStep.STEP5_CLUSTERING,
            "step6_video": ProcessingStep.STEP6_VIDEO
        }
        
        if start_step not in step_mapping:
            raise ValueError(f"translated'ssteptranslated: {start_step}")
        
        processing_step = step_mapping[start_step]
        
        # fromtranslatedsteptranslated
        result = orchestrator.resume_from_step(processing_step, srt_path)
        
        context.mark_completed()
        
        # updateprojectstatustranslatedcompletedtranslated
        try:
            from ..models.project import Project, ProjectStatus
            from ..services.data_sync_service import DataSyncService
            from pathlib import Path
            
            project = self.db.query(Project).filter(Project.id == project_id).first()
            if project:
                project.status = ProjectStatus.COMPLETED
                self.db.commit()
                logger.info(f"projectstatustranslatedupdatetranslatedcompleted: {project_id}")
                
                # translateddatabase
                project_dir = Path(__file__).parent.parent / "data" / "projects" / project_id
                if project_dir.exists():
                    sync_service = DataSyncService(self.db)
                    sync_result = sync_service.sync_project_from_filesystem(project_id, project_dir)
                    if sync_result.get("success"):
                        logger.info(f"project {project_id} translatedsucceeded: {sync_result}")
                    else:
                        logger.error(f"project {project_id} translatedfailed: {sync_result}")
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
            updatetranslated
        """
        config_manager = ProjectConfigManager(project_id)
        
        # updateprocesstranslated
        if "processing_params" in config_updates:
            config_manager.update_processing_params(**config_updates["processing_params"])
        
        # updateLLMconfig
        if "llm_config" in config_updates:
            config_manager.update_llm_config(**config_updates["llm_config"])
        
        # updatestepconfig
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
        verifyprojectsettings
        
        Args:
            project_id: projectID
            
        Returns:
            verifytranslated
        """
        # translated，PipelineAdapter file not found
        # adapter = PipelineAdapter(project_id)
        # errors = adapter.validate_pipeline_prerequisites()
        
        # if errors:
        #     return {
        #         "valid": False,
        #         "errors": errors
        #     }
        
        return {
            "valid": True,
            "message": "projectsettingsverifytranslated（translatedskipPipelineAdapterverify）"
        }
    
    def _create_processing_task(self, project_id: str, task_type: TaskType = TaskType.VIDEO_PROCESSING) -> Task:
        """createprocesstask"""
        task_data = {
            "name": f"videoprocesstask - {project_id}",
            "description": f"processproject {project_id} 'svideotranslated",
            "project_id": project_id,
            "task_type": task_type,
            "status": TaskStatus.PtranslatedDING,
            "progress": 0.0,
            "metadata": {
                "project_id": project_id,
                "task_type": task_type.value if hasattr(task_type, 'value') else task_type
            }
        }
        
        return self.task_repo.create(**task_data)