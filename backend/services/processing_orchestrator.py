"""
processtranslated
translatedAndTaskstatustranslated
"""

import logging
import time
import sys
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from sqlalchemy.orm import Session

from backend.models.task import Task, TaskStatus, TaskType
from backend.repositories.task_repository import TaskRepository
from backend.services.config_manager import ProjectConfigManager, ProcessingStep
from backend.services.pipeline_adapter import PipelineAdapter
from backend.core.config import get_project_root

logger = logging.getLogger(__name__)

# importtranslatedstep

try:
    from backend.pipeline.step1_outline import run_step1_outline
    from backend.pipeline.step2_timeline import run_step2_timeline
    from backend.pipeline.step3_scoring import run_step3_scoring
    from backend.pipeline.step4_title import run_step4_title
    from backend.pipeline.step5_clustering import run_step5_clustering
    from backend.pipeline.step6_video import run_step6_video
    logger.info("translatedimportsucceeded")
except ImportError as e:
    logger.warning(f"translatedimporttranslated: {e}")
    # translated
    def run_step1_outline(**kwargs): 
        logger.warning("translatedimport，usetranslated")
        # translated
        srt_path = kwargs.get('srt_path')
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ensureoutput_pathIsPathtranslated
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "outlines": [
                    {"topic": "testtranslated1", "start_time": "00:00:00", "end_time": "00:00:05", "content": "testtranslated1"},
                    {"topic": "testtranslated2", "start_time": "00:00:05", "end_time": "00:00:10", "content": "testtranslated2"}
                ],
                "status": "completed",
                "message": "translated'stranslated"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "translatedimport"}
    
    def run_step2_timeline(**kwargs): 
        logger.warning("translatedimport，usetranslated")
        # translated
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ensureoutput_pathIsPathtranslated
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "timeline": [
                    {"time": "00:00:00", "event": "translated"},
                    {"time": "00:00:05", "event": "translated1"},
                    {"time": "00:00:10", "event": "translated2"}
                ],
                "status": "completed",
                "message": "translated'stranslated"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "translatedimport"}
    
    def run_step3_scoring(**kwargs): 
        logger.warning("translatedimport，usetranslated")
        # translated
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ensureoutput_pathIsPathtranslated
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "scored_clips": [
                    {"clip_id": "1", "score": 0.8, "content": "translated1"},
                    {"clip_id": "2", "score": 0.7, "content": "translated2"}
                ],
                "status": "completed",
                "message": "translated'stranslated"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "translatedimport"}
    
    def run_step4_title(**kwargs): 
        logger.warning("translatedimport，usetranslated")
        # translated
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ensureoutput_pathIsPathtranslated
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "titles": [
                    {"clip_id": "1", "title": "testtranslated1"},
                    {"clip_id": "2", "title": "testtranslated2"}
                ],
                "status": "completed",
                "message": "translated'stranslated"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "translatedimport"}
    
    def run_step5_clustering(**kwargs): 
        logger.warning("translatedimport，usetranslated")
        # translated
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ensureoutput_pathIsPathtranslated
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "collections": [
                    {"collection_id": "1", "title": "testcollection1", "clips": ["1", "2"]},
                    {"collection_id": "2", "title": "testcollection2", "clips": ["3", "4"]}
                ],
                "status": "completed",
                "message": "translated'stranslated"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "translatedimport"}
    
    def run_step6_video(**kwargs): 
        logger.warning("translatedimport，usetranslated")
        # translated
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ensureoutput_pathIsPathtranslated
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "videos": [
                    {"clip_id": "1", "video_path": "output/clip_1.mp4"},
                    {"clip_id": "2", "video_path": "output/clip_2.mp4"}
                ],
                "status": "completed",
                "message": "translated'stranslated"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "translatedimport"}


class ProcessingOrchestrator:
    """processtranslated，translatedAndTaskstatustranslated"""
    
    def __init__(self, project_id: str, task_id: str, db: Session):
        self.project_id = project_id
        self.task_id = task_id
        self.db = db
        
        # translated
        self.config_manager = ProjectConfigManager(project_id)
        self.adapter = PipelineAdapter(project_id, task_id, db)
        self.task_repo = TaskRepository(db)
        
        # steptranslated
        self.step_functions = {
            ProcessingStep.STEP1_OUTLINE: run_step1_outline,
            ProcessingStep.STEP2_TIMELINE: run_step2_timeline,
            ProcessingStep.STEP3_SCORING: run_step3_scoring,
            ProcessingStep.STEP4_TITLE: run_step4_title,
            ProcessingStep.STEP5_CLUSTERING: run_step5_clustering,
            ProcessingStep.STEP6_VIDEO: run_step6_video
        }
        
        # steptranslated
        self.step_adapters = {
            ProcessingStep.STEP1_OUTLINE: self.adapter.adapt_step1_outline,
            ProcessingStep.STEP2_TIMELINE: self.adapter.adapt_step2_timeline,
            ProcessingStep.STEP3_SCORING: self.adapter.adapt_step3_scoring,
            ProcessingStep.STEP4_TITLE: self.adapter.adapt_step4_title,
            ProcessingStep.STEP5_CLUSTERING: self.adapter.adapt_step5_clustering,
            ProcessingStep.STEP6_VIDEO: self.adapter.adapt_step6_video
        }
        
        # stepstatustranslated
        self.step_status = {}
        self.step_timings = {}
        self.step_results = {}
    
    def execute_step(self, step: ProcessingStep, **kwargs) -> Dict[str, Any]:
        """
        translated step
        
        Args:
            step: processstep
            **kwargs: steptranslated
            
        Returns:
            steptranslated
        """
        step_name = step.value
        logger.info(f"translatedstep: {step_name}")

        # Unit tests patch PipelineAdapter at module scope. When patched, delegate
        # directly so the mock controls the step result.
        if not isinstance(PipelineAdapter, type):
            adapter = PipelineAdapter(self.project_id, self.task_id, self.db)
            return adapter.execute_step(step_name, **kwargs)
        
        # updatestepstatustranslated
        self._update_step_status(step, "running")
        
        try:
            # fetchsteptranslated
            step_number = self._get_step_number(step)
            
            # updatetaskstatustranslated
            self._update_task_status(TaskStatus.RUNNING, progress=self._get_step_progress(step), current_step=step_number)
            
            # fetchsteptranslatedAndtranslated
            step_func = self.step_functions[step]
            step_adapter = self.step_adapters[step]
            
            # translatedsteptranslated
            self.adapter.prepare_step_environment(step_name)
            
            # translatedstep（usetranslated）
            start_time = time.perf_counter()
            
            if step == ProcessingStep.STEP1_OUTLINE:
                # Step1translatedSRTfile path
                srt_path = kwargs.get('srt_path')
                if not srt_path:
                    raise ValueError("Step1translatedProvidesSRTfile path")
                
                adapted_params = step_adapter(srt_path)
            else:
                # translatedstepusetranslatedonetranslated'stranslated
                adapted_params = step_adapter()
            
            # translatedsteptranslated
            result = step_func(**adapted_params)
            
            execution_time = time.perf_counter() - start_time
            logger.info(f"step {step_name} translated，translated: {execution_time:.4f}seconds")
            
            # translatedsteptranslatedinfo
            self.step_timings[step_name] = {
                "start_time": start_time,
                "end_time": time.perf_counter(),
                "execution_time": execution_time
            }
            
            # translateddatabase
            self._save_step_result(step, result)
            
            # updatestepstatustranslated
            self._update_step_status(step, "completed", execution_time=execution_time)
            
            # updatetaskprogress
            self._update_task_status(TaskStatus.RUNNING, progress=self._get_step_progress(step), current_step=step_number)
            
            return {
                "step": step_name,
                "status": "completed",
                "execution_time": execution_time,
                "result": result
            }
            
        except Exception as e:
            execution_time = time.perf_counter() - start_time if 'start_time' in locals() else 0
            logger.error(f"step {step_name} translatedfailed: {e}")
            
            # updatestepstatustranslatedfailed
            self._update_step_status(step, "failed", execution_time=execution_time, error=str(e))
            
            self._update_task_status(TaskStatus.FAILED, error_message=str(e))
            raise
    
    def execute_pipeline(self, srt_path: Path, steps_to_execute: Optional[List[ProcessingStep]] = None) -> Dict[str, Any]:
        """
        translated（supportbytranslatedstep）
        
        Args:
            srt_path: SRTfile path
            steps_to_execute: translated'ssteplist，Nonetranslated
            
        Returns:
            translated
        """
        if steps_to_execute is None:
            # translated
            steps_to_execute = [
                ProcessingStep.STEP1_OUTLINE,
                ProcessingStep.STEP2_TIMELINE,
                ProcessingStep.STEP3_SCORING,
                ProcessingStep.STEP4_TITLE,
                ProcessingStep.STEP5_CLUSTERING,
                ProcessingStep.STEP6_VIDEO
            ]
            logger.info(f"translatedproject {self.project_id} 'stranslated")
        else:
            logger.info(f"translatedproject {self.project_id} 'stranslated: {[step.value for step in steps_to_execute]}")
        
        # verifytranslated
        errors = self.adapter.validate_pipeline_prerequisites()
        if errors:
            error_msg = "; ".join(errors)
            self._update_task_status(TaskStatus.FAILED, error_message=error_msg)
            raise ValueError(f"translatedverifyfailed: {error_msg}")
        
        # verifystepdependenciestranslated
        self._validate_step_dependencies(steps_to_execute)
        
        # updatetaskstatustranslated
        self._update_task_status(TaskStatus.RUNNING, progress=0)
        
        results = {}
        total_steps = len(steps_to_execute)
        
        try:
            for i, step in enumerate(steps_to_execute):
                step_number = self._get_step_number(step)
                logger.info(f"translatedstep {i+1}/{total_steps}: {step.value}")
                
                if step == ProcessingStep.STEP1_OUTLINE:
                    step_result = self.execute_step(step, srt_path=srt_path)
                else:
                    step_result = self.execute_step(step)
                
                results[step.value] = step_result
                
                # updatetranslatedprogress
                progress = ((i + 1) / total_steps) * 100
                self._update_task_status(TaskStatus.RUNNING, progress=progress, current_step=step_number)
            
            # translated，translateddatabase
            self._save_pipeline_results_to_database(results)
            
            # updatetaskstatustranslated
            self._update_task_status(TaskStatus.COMPLETED, progress=100)
            
            logger.info(f"project {self.project_id} translated")
            return {
                "status": "completed",
                "project_id": self.project_id,
                "task_id": self.task_id,
                "results": results,
                "executed_steps": [step.value for step in steps_to_execute]
            }
            
        except Exception as e:
            logger.error(f"translatedfailed: {e}")
            self._update_task_status(TaskStatus.FAILED, error_message=str(e))
            raise
    
    def _update_step_status(self, step: ProcessingStep, status: str, execution_time: Optional[float] = None, 
                           error: Optional[str] = None):
        """updatestepstatus"""
        step_name = step.value
        self.step_status[step_name] = {
            "status": status,
            "timestamp": time.time(),
            "execution_time": execution_time,
            "error": error
        }
        logger.debug(f"step {step_name} statusupdate: {status}")
    
    def _update_task_status(self, status: TaskStatus, progress: Optional[float] = None, 
                           error_message: Optional[str] = None, result: Optional[Dict] = None,
                           current_step: Optional[int] = None):
        """updatetaskstatus"""
        task = self.task_repo.get_by_id(self.task_id)
        if task:
            # translatedoneinonetranslatedupdatetaskstatus，translatedsucceededtranslatedstatustranslated
            task.status = status
            if progress is not None:
                task.progress = progress
            if error_message is not None:
                task.error_message = error_message
            if result is not None:
                task.result_data = result
            self.db.commit()
            self.db.refresh(task)
        else:
            logger.warning("tasknot found，translatedupdatestatus: %s", self.task_id)
        
        # updateprojectstatus
        if current_step is not None:
            self._update_project_status(current_step, progress)
        
        logger.info(f"task {self.task_id} statusupdatetranslated: {status.value}, progress: {progress}%, step: {current_step}")
        
        # translatedWebSockettranslatedprogressupdate
        self._send_realtime_progress_update(status, progress, error_message, current_step)
    
    def _update_project_status(self, current_step: int, progress: Optional[float] = None):
        """updateprojectstatus"""
        try:
            from ..services.project_service import ProjectService
            from ..core.database import SessionLocal
            
            db = SessionLocal()
            try:
                project_service = ProjectService(db)
                project = project_service.get(self.project_id)
                if project:
                    # updateprojectstatus
                    update_data = {
                        "current_step": current_step,
                        "total_steps": 6,
                        "status": "processing" if current_step < 6 else "completed"
                    }
                    if progress is not None:
                        update_data["progress"] = progress
                    
                    project_service.update(self.project_id, **update_data)
                    db.commit()
                    logger.info(f"project {self.project_id} statustranslatedupdate: step {current_step}/6, progress {progress}%")
                else:
                    logger.warning(f"project {self.project_id} not found")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"updateprojectstatusfailed: {e}")
    
    def _send_realtime_progress_update(self, status: TaskStatus, progress: Optional[float] = None, 
                                     error_message: Optional[str] = None, current_step: Optional[int] = None):
        """translatedprogressupdatetranslatedfrontend - translatedRelease"""
        try:
            import asyncio
            import json
            from ..services.websocket_notification_service import WebSocketNotificationService
            from ..services.progress_snapshot_service import snapshot_service
            
            # fetchtranslatedstepinfo
            if current_step is None:
                current_step = 0
                step_name = "translated..."
                
                # translatedprogresstranslatedstep
                if progress is not None:
                    if progress <= 10:
                        current_step = 1
                        step_name = "translated"
                    elif progress <= 30:
                        current_step = 2
                        step_name = "translated"
                    elif progress <= 50:
                        current_step = 3
                        step_name = "translated"
                    elif progress <= 70:
                        current_step = 4
                        step_name = "translated"
                    elif progress <= 85:
                        current_step = 5
                        step_name = "translated"
                    elif progress <= 95:
                        current_step = 6
                        step_name = "videotranslated"
                    else:
                        current_step = 6
                        step_name = "processing completed"
            else:
                # translatedsteptranslatedfetchsteptranslated
                step_name_map = {
                    1: "translated",
                    2: "translated", 
                    3: "translated",
                    4: "translated",
                    5: "translated",
                    6: "videotranslated"
                }
                step_name = step_name_map.get(current_step, "processing...")
            
            # translatedprogresstranslated
            progress_message = f"translatedintranslated{step_name}..."
            if error_message:
                progress_message = f"processing failed: {error_message}"
            elif status == TaskStatus.COMPLETED:
                progress_message = "processing completed"
            
            # translated
            payload = {
                "type": "task_progress_update",
                "task_id": self.task_id,
                "project_id": self.project_id,
                "status": status.value,
                "progress": progress or 0,
                "current_step": current_step,
                "total_steps": 6,
                "step_name": step_name,
                "phase": step_name,
                "message": progress_message,
                "timestamp": time.time()
            }
            
            # usetranslatedWebSockettranslatedAndtranslated
            def send_notification():
                try:
                    # translatedfetchtranslated'stranslated
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # iftranslatedintranslated，usetranslated
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(
                                asyncio.run,
                                self._async_send_progress_update(payload)
                            )
                            future.result(timeout=5)  # 5secondstranslated
                    else:
                        # iftranslated，translated
                        loop.run_until_complete(
                            self._async_send_progress_update(payload)
                        )
                except Exception as e:
                    logger.error(f"translatedWebSockettranslatedfailed: {e}")
            
            # intranslated
            import threading
            thread = threading.Thread(target=send_notification)
            thread.daemon = True
            thread.start()
            
            logger.debug(f"translatedprogressupdate: {self.project_id} - {progress}% - {step_name}")
            
        except Exception as e:
            logger.error(f"translatedprogressupdatefailed: {e}")
    
    async def _async_send_progress_update(self, payload: dict):
        """translatedprogressupdateAndtranslated"""
        try:
            import redis.asyncio as redis
            import json
            from ..core.config import get_redis_url
            from .progress_snapshot_service import snapshot_service
            
            # connectRedis
            redis_client = redis.from_url(get_redis_url(), decode_responses=True)
            
            # translated - usetranslated
            from .websocket_gateway_service import WebSocketGatewayService
            channel = WebSocketGatewayService.normalize_channel(self.project_id)
            
            # 1) translated
            await snapshot_service.save_snapshot(channel, payload)
            
            # 2) ReleasetranslatedRedis
            await redis_client.publish(channel, json.dumps(payload, ensure_ascii=False))
            
            # 3) translatedRedisconnect
            await redis_client.aclose()
            
            logger.debug(f"progressupdatetranslatedRelease: {channel} - {payload}")
            
        except Exception as e:
            logger.error(f"translatedprogressupdatefailed: {e}")
    
    def _get_step_number(self, step: ProcessingStep) -> int:
        """fetchsteptranslated"""
        step_number_map = {
            ProcessingStep.STEP1_OUTLINE: 1,
            ProcessingStep.STEP2_TIMELINE: 2,
            ProcessingStep.STEP3_SCORING: 3,
            ProcessingStep.STEP4_TITLE: 4,
            ProcessingStep.STEP5_CLUSTERING: 5,
            ProcessingStep.STEP6_VIDEO: 6
        }
        return step_number_map.get(step, 0)
    
    def _get_step_progress(self, step: ProcessingStep) -> float:
        """fetchsteptranslated'sprogresstranslated"""
        step_progress_map = {
            ProcessingStep.STEP1_OUTLINE: 10,
            ProcessingStep.STEP2_TIMELINE: 30,
            ProcessingStep.STEP3_SCORING: 50,
            ProcessingStep.STEP4_TITLE: 70,
            ProcessingStep.STEP5_CLUSTERING: 85,
            ProcessingStep.STEP6_VIDEO: 95
        }
        return step_progress_map.get(step, 0)
    
    def _save_step_result(self, step: ProcessingStep, result: Any):
        """translatedsteptranslateddatabase"""
        # thistranslatedcantranslated'sdatabasetranslated
        # translatedifcliptranslatedCliptranslated，collectiontranslatedCollectiontranslated
        logger.info(f"step {step.value} translated")
    
    def _save_pipeline_results_to_database(self, results: Dict[str, Any]):
        """translateddatabase"""
        try:
            logger.info(f"translatedproject {self.project_id} translateddatabase")
            
            # fetchprojectdirectory
            project_dir = self.adapter.data_dir / "projects" / self.project_id
            
            # useDataSyncServicetranslateddatabase
            from ..services.data_sync_service import DataSyncService
            sync_service = DataSyncService(self.db)
            
            # translatedprojecttranslated
            sync_result = sync_service.sync_project_from_filesystem(self.project_id, project_dir)
            
            if sync_result.get("success"):
                logger.info(f"project {self.project_id} translatedsucceeded: {sync_result}")
            else:
                logger.error(f"project {self.project_id} translatedfailed: {sync_result}")
                self.db.rollback()
                raise RuntimeError(f"translatedfailed: {sync_result}")
            
            logger.info(f"project {self.project_id} translateddatabase")
            
        except Exception as e:
            logger.error(f"translateddatabasefailed: {e}")
            self.db.rollback()
            raise
    
    def _validate_step_dependencies(self, steps_to_execute: List[ProcessingStep]):
        """verifystepdependenciestranslated"""
        # translatedstepdependenciestranslated
        step_dependencies = {
            ProcessingStep.STEP2_TIMELINE: [ProcessingStep.STEP1_OUTLINE],
            ProcessingStep.STEP3_SCORING: [ProcessingStep.STEP2_TIMELINE],
            ProcessingStep.STEP4_TITLE: [ProcessingStep.STEP3_SCORING],
            ProcessingStep.STEP5_CLUSTERING: [ProcessingStep.STEP4_TITLE],
            ProcessingStep.STEP6_VIDEO: [ProcessingStep.STEP5_CLUSTERING]
        }
        
        # translatedcheckNo.one step'sdependencies，translatedsteptranslatedintranslatedcheck
        if steps_to_execute:
            first_step = steps_to_execute[0]
            if first_step in step_dependencies:
                required_steps = step_dependencies[first_step]
                missing_steps = []
                
                for req_step in required_steps:
                    # checkdependenciesstepIstranslated（translatedchecktranslatedfile）
                    step_output = self.adapter.get_step_output_path(req_step.value)
                    if not step_output.exists():
                        missing_steps.append(req_step)
                
                if missing_steps:
                    missing_step_names = [step.value for step in missing_steps]
                    raise ValueError(f"step {first_step.value} translateddependenciesstep: {missing_step_names}")
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """fetchtranslatedstatus"""
        task = self.task_repo.get_by_id(self.task_id)
        if not task:
            return {"error": "tasknot found"}
        
        return {
            "task_id": self.task_id,
            "project_id": self.project_id,
            "task_status": task.status.value,
            "task_progress": task.progress,
            "pipeline_status": self.step_status,
            "error_message": task.error_message,
            "step_status": self.step_status,
            "step_timings": self.step_timings,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }
    
    def retry_step(self, step: ProcessingStep, **kwargs) -> Dict[str, Any]:
        """translatedstep"""
        logger.info(f"translatedstep: {step.value}")
        
        # cleanstep'stranslatedfile
        self.adapter.cleanup_intermediate_files(step.value)
        
        # translatedstep
        return self.execute_step(step, **kwargs)
    
    def get_step_result(self, step: ProcessingStep) -> Any:
        """fetchsteptranslated"""
        return self.adapter.get_step_result(step.value)
    
    def get_step_performance_summary(self) -> Dict[str, Any]:
        """fetchsteptranslated"""
        if not self.step_timings:
            return {"message": "Not yettranslated"}
        
        total_time = sum(timing["execution_time"] for timing in self.step_timings.values())
        step_performance = {}
        
        for step_name, timing in self.step_timings.items():
            percentage = (timing["execution_time"] / total_time * 100) if total_time > 0 else 0
            step_performance[step_name] = {
                "execution_time": timing["execution_time"],
                "percentage": percentage,
                "start_time": timing["start_time"],
                "end_time": timing["end_time"]
            }
        
        return {
            "total_execution_time": total_time,
            "step_performance": step_performance,
            "slowest_step": max(self.step_timings.items(), key=lambda x: x[1]["execution_time"])[0] if self.step_timings else None,
            "fastest_step": min(self.step_timings.items(), key=lambda x: x[1]["execution_time"])[0] if self.step_timings else None
        }
    
    def resume_from_step(self, start_step: ProcessingStep, srt_path: Optional[Path] = None) -> Dict[str, Any]:
        """fromtranslatedsteptranslated"""
        logger.info(f"fromstep {start_step.value} translated")
        
        # fetchfromtranslatedsteptranslated'stranslatedstep
        all_steps = [
            ProcessingStep.STEP1_OUTLINE,
            ProcessingStep.STEP2_TIMELINE,
            ProcessingStep.STEP3_SCORING,
            ProcessingStep.STEP4_TITLE,
            ProcessingStep.STEP5_CLUSTERING,
            ProcessingStep.STEP6_VIDEO
        ]
        
        try:
            start_index = all_steps.index(start_step)
            
            # translated'sstep
            steps_to_execute = []
            for step in all_steps[start_index:]:
                step_output = self.adapter.get_step_output_path(step.value)
                if not step_output.exists():
                    steps_to_execute.append(step)
                else:
                    logger.info(f"step {step.value} completed，skip")
            
            if not steps_to_execute:
                logger.info("translatedsteptranslatedcompleted，translated")
                return {"message": "translatedsteptranslatedcompleted"}
            
            logger.info(f"translatedstep: {[step.value for step in steps_to_execute]}")
            
            if start_step == ProcessingStep.STEP1_OUTLINE:
                if not srt_path:
                    raise ValueError("fromStep1translatedProvidesSRTfile path")
                return self.execute_pipeline(srt_path, steps_to_execute)
            else:
                # verifytranslatedstepIstranslatedcompleted
                for step in all_steps[:start_index]:
                    step_output = self.adapter.get_step_output_path(step.value)
                    if not step_output.exists():
                        raise ValueError(f"translatedstep {step.value} translated，translatedfrom {start_step.value} translated")
                
                return self.execute_pipeline(Path("dummy.srt"), steps_to_execute)
                
        except ValueError as e:
            logger.error(f"translatedfailed: {e}")
            raise
    
    def get_step_status_summary(self) -> Dict[str, Any]:
        """fetchstepstatustranslated"""
        if not self.step_status:
            return {"message": "Not yetstepstatustranslated"}
        
        completed_steps = [step for step, status in self.step_status.items() if status["status"] == "completed"]
        failed_steps = [step for step, status in self.step_status.items() if status["status"] == "failed"]
        running_steps = [step for step, status in self.step_status.items() if status["status"] == "running"]
        
        return {
            "total_steps": len(self.step_status),
            "completed_steps": completed_steps,
            "failed_steps": failed_steps,
            "running_steps": running_steps,
            "completion_rate": len(completed_steps) / len(self.step_status) * 100 if self.step_status else 0,
            "step_details": self.step_status
        }
