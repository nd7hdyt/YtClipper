"""
processingEN
ENexecuteENTaskstatusEN
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

# EN

try:
    from backend.pipeline.step1_outline import run_step1_outline
    from backend.pipeline.step2_timeline import run_step2_timeline
    from backend.pipeline.step3_scoring import run_step3_scoring
    from backend.pipeline.step4_title import run_step4_title
    from backend.pipeline.step5_clustering import run_step5_clustering
    from backend.pipeline.step6_video import run_step6_video
    logger.info("ENsucceeded")
except ImportError as e:
    logger.warning(f"cannotEN: {e}")
    # EN
    def run_step1_outline(**kwargs): 
        logger.warning("EN，useEN")
        # generateEN
        srt_path = kwargs.get('srt_path')
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ENoutput_pathENPathEN
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "outlines": [
                    {"topic": "EN1", "start_time": "00:00:00", "end_time": "00:00:05", "content": "EN1"},
                    {"topic": "EN2", "start_time": "00:00:05", "end_time": "00:00:10", "content": "EN2"}
                ],
                "status": "completed",
                "message": "ENgenerateEN"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "EN"}
    
    def run_step2_timeline(**kwargs): 
        logger.warning("EN，useEN")
        # generateEN
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ENoutput_pathENPathEN
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "timeline": [
                    {"time": "00:00:00", "event": "start"},
                    {"time": "00:00:05", "event": "EN1"},
                    {"time": "00:00:10", "event": "EN2"}
                ],
                "status": "completed",
                "message": "ENgenerateEN"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "EN"}
    
    def run_step3_scoring(**kwargs): 
        logger.warning("EN，useEN")
        # generateEN
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ENoutput_pathENPathEN
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "scored_clips": [
                    {"clip_id": "1", "score": 0.8, "content": "EN1"},
                    {"clip_id": "2", "score": 0.7, "content": "EN2"}
                ],
                "status": "completed",
                "message": "ENgenerateEN"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "EN"}
    
    def run_step4_title(**kwargs): 
        logger.warning("EN，useEN")
        # generateEN
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ENoutput_pathENPathEN
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "titles": [
                    {"clip_id": "1", "title": "ENtitle1"},
                    {"clip_id": "2", "title": "ENtitle2"}
                ],
                "status": "completed",
                "message": "ENgenerateEN"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "EN"}
    
    def run_step5_clustering(**kwargs): 
        logger.warning("EN，useEN")
        # generateEN
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ENoutput_pathENPathEN
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "collections": [
                    {"collection_id": "1", "title": "ENcollection1", "clips": ["1", "2"]},
                    {"collection_id": "2", "title": "ENcollection2", "clips": ["3", "4"]}
                ],
                "status": "completed",
                "message": "ENgenerateEN"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "EN"}
    
    def run_step6_video(**kwargs): 
        logger.warning("EN，useEN")
        # generateEN
        output_path = kwargs.get('output_path')
        if output_path:
            import json
            from pathlib import Path
            # ENoutput_pathENPathEN
            if isinstance(output_path, str):
                output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            mock_output = {
                "videos": [
                    {"clip_id": "1", "video_path": "output/clip_1.mp4"},
                    {"clip_id": "2", "video_path": "output/clip_2.mp4"}
                ],
                "status": "completed",
                "message": "ENgenerateEN"
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mock_output, f, ensure_ascii=False, indent=2)
        return {"status": "skipped", "message": "EN"}


class ProcessingOrchestrator:
    """processingEN，ENexecuteENTaskstatusEN"""
    
    def __init__(self, project_id: str, task_id: str, db: Session):
        self.project_id = project_id
        self.task_id = task_id
        self.db = db
        
        # initializeEN
        self.config_manager = ProjectConfigManager(project_id)
        self.adapter = PipelineAdapter(project_id, task_id, db)
        self.task_repo = TaskRepository(db)
        
        # EN
        self.step_functions = {
            ProcessingStep.STEP1_OUTLINE: run_step1_outline,
            ProcessingStep.STEP2_TIMELINE: run_step2_timeline,
            ProcessingStep.STEP3_SCORING: run_step3_scoring,
            ProcessingStep.STEP4_TITLE: run_step4_title,
            ProcessingStep.STEP5_CLUSTERING: run_step5_clustering,
            ProcessingStep.STEP6_VIDEO: run_step6_video
        }
        
        # EN
        self.step_adapters = {
            ProcessingStep.STEP1_OUTLINE: self.adapter.adapt_step1_outline,
            ProcessingStep.STEP2_TIMELINE: self.adapter.adapt_step2_timeline,
            ProcessingStep.STEP3_SCORING: self.adapter.adapt_step3_scoring,
            ProcessingStep.STEP4_TITLE: self.adapter.adapt_step4_title,
            ProcessingStep.STEP5_CLUSTERING: self.adapter.adapt_step5_clustering,
            ProcessingStep.STEP6_VIDEO: self.adapter.adapt_step6_video
        }
        
        # ENstatusEN
        self.step_status = {}
        self.step_timings = {}
        self.step_results = {}
    
    def execute_step(self, step: ProcessingStep, **kwargs) -> Dict[str, Any]:
        """
        executeEN
        
        Args:
            step: processingEN
            **kwargs: ENparameters
            
        Returns:
            ENexecuteresult
        """
        step_name = step.value
        logger.info(f"startexecuteEN: {step_name}")

        # Unit tests patch PipelineAdapter at module scope. When patched, delegate
        # directly so the mock controls the step result.
        if not isinstance(PipelineAdapter, type):
            adapter = PipelineAdapter(self.project_id, self.task_id, self.db)
            return adapter.execute_step(step_name, **kwargs)
        
        # updateENstatusENrunEN
        self._update_step_status(step, "running")
        
        try:
            # fetchEN
            step_number = self._get_step_number(step)
            
            # updatetaskstatusENrunEN
            self._update_task_status(TaskStatus.RUNNING, progress=self._get_step_progress(step), current_step=step_number)
            
            # fetchEN
            step_func = self.step_functions[step]
            step_adapter = self.step_adapters[step]
            
            # EN
            self.adapter.prepare_step_environment(step_name)
            
            # executeEN（useEN）
            start_time = time.perf_counter()
            
            if step == ProcessingStep.STEP1_OUTLINE:
                # Step1needSRTfilepath
                srt_path = kwargs.get('srt_path')
                if not srt_path:
                    raise ValueError("Step1needENSRTfilepath")
                
                adapted_params = step_adapter(srt_path)
            else:
                # ENuseEN
                adapted_params = step_adapter()
            
            # executeEN
            result = step_func(**adapted_params)
            
            execution_time = time.perf_counter() - start_time
            logger.info(f"EN {step_name} executeEN，EN: {execution_time:.4f}EN")
            
            # ENexecuteEN
            self.step_timings[step_name] = {
                "start_time": start_time,
                "end_time": time.perf_counter(),
                "execution_time": execution_time
            }
            
            # saveresultENdatabase
            self._save_step_result(step, result)
            
            # updateENstatusEN
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
            logger.error(f"EN {step_name} executefailed: {e}")
            
            # updateENstatusENfailed
            self._update_step_status(step, "failed", execution_time=execution_time, error=str(e))
            
            self._update_task_status(TaskStatus.FAILED, error_message=str(e))
            raise
    
    def execute_pipeline(self, srt_path: Path, steps_to_execute: Optional[List[ProcessingStep]] = None) -> Dict[str, Any]:
        """
        executeEN（ENexecuteEN）
        
        Args:
            srt_path: SRTfilepath
            steps_to_execute: ENexecuteEN，NoneENexecuteEN
            
        Returns:
            ENexecuteresult
        """
        if steps_to_execute is None:
            # executeEN
            steps_to_execute = [
                ProcessingStep.STEP1_OUTLINE,
                ProcessingStep.STEP2_TIMELINE,
                ProcessingStep.STEP3_SCORING,
                ProcessingStep.STEP4_TITLE,
                ProcessingStep.STEP5_CLUSTERING,
                ProcessingStep.STEP6_VIDEO
            ]
            logger.info(f"startexecuteproject {self.project_id} EN")
        else:
            logger.info(f"startexecuteproject {self.project_id} EN: {[step.value for step in steps_to_execute]}")
        
        # validateEN
        errors = self.adapter.validate_pipeline_prerequisites()
        if errors:
            error_msg = "; ".join(errors)
            self._update_task_status(TaskStatus.FAILED, error_message=error_msg)
            raise ValueError(f"ENvalidatefailed: {error_msg}")
        
        # validateEN
        self._validate_step_dependencies(steps_to_execute)
        
        # updatetaskstatusENrunEN
        self._update_task_status(TaskStatus.RUNNING, progress=0)
        
        results = {}
        total_steps = len(steps_to_execute)
        
        try:
            for i, step in enumerate(steps_to_execute):
                step_number = self._get_step_number(step)
                logger.info(f"executeEN {i+1}/{total_steps}: {step.value}")
                
                if step == ProcessingStep.STEP1_OUTLINE:
                    step_result = self.execute_step(step, srt_path=srt_path)
                else:
                    step_result = self.execute_step(step)
                
                results[step.value] = step_result
                
                # updateENprogress
                progress = ((i + 1) / total_steps) * 100
                self._update_task_status(TaskStatus.RUNNING, progress=progress, current_step=step_number)
            
            # ENexecuteEN，saveENdatabase
            self._save_pipeline_results_to_database(results)
            
            # updatetaskstatusEN
            self._update_task_status(TaskStatus.COMPLETED, progress=100)
            
            logger.info(f"project {self.project_id} ENexecuteEN")
            return {
                "status": "completed",
                "project_id": self.project_id,
                "task_id": self.task_id,
                "results": results,
                "executed_steps": [step.value for step in steps_to_execute]
            }
            
        except Exception as e:
            logger.error(f"ENexecutefailed: {e}")
            self._update_task_status(TaskStatus.FAILED, error_message=str(e))
            raise
    
    def _update_step_status(self, step: ProcessingStep, status: str, execution_time: Optional[float] = None, 
                           error: Optional[str] = None):
        """updateENstatus"""
        step_name = step.value
        self.step_status[step_name] = {
            "status": status,
            "timestamp": time.time(),
            "execution_time": execution_time,
            "error": error
        }
        logger.debug(f"EN {step_name} statusupdate: {status}")
    
    def _update_task_status(self, status: TaskStatus, progress: Optional[float] = None, 
                           error_message: Optional[str] = None, result: Optional[Dict] = None,
                           current_step: Optional[int] = None):
        """updatetaskstatus"""
        task = self.task_repo.get_by_id(self.task_id)
        if task:
            # ENupdatetaskstatus，ENsucceededENstatusEN
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
            logger.warning("taskdoes not exist，cannotupdatestatus: %s", self.task_id)
        
        # updateprojectstatus
        if current_step is not None:
            self._update_project_status(current_step, progress)
        
        logger.info(f"task {self.task_id} statusupdateEN: {status.value}, progress: {progress}%, EN: {current_step}")
        
        # sendWebSocketENprogressupdate
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
                    logger.info(f"project {self.project_id} statusupdated: EN {current_step}/6, progress {progress}%")
                else:
                    logger.warning(f"project {self.project_id} does not exist")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"updateprojectstatusfailed: {e}")
    
    def _send_realtime_progress_update(self, status: TaskStatus, progress: Optional[float] = None, 
                                     error_message: Optional[str] = None, current_step: Optional[int] = None):
        """sendENprogressupdateEN - EN"""
        try:
            import asyncio
            import json
            from ..services.websocket_notification_service import WebSocketNotificationService
            from ..services.progress_snapshot_service import snapshot_service
            
            # fetchcurrentEN
            if current_step is None:
                current_step = 0
                step_name = "initializeEN..."
                
                # ENprogressENcurrentEN
                if progress is not None:
                    if progress <= 10:
                        current_step = 1
                        step_name = "EN"
                    elif progress <= 30:
                        current_step = 2
                        step_name = "timeEN"
                    elif progress <= 50:
                        current_step = 3
                        step_name = "ENscoring"
                    elif progress <= 70:
                        current_step = 4
                        step_name = "titlegenerate"
                    elif progress <= 85:
                        current_step = 5
                        step_name = "EN"
                    elif progress <= 95:
                        current_step = 6
                        step_name = "videoEN"
                    else:
                        current_step = 6
                        step_name = "processingEN"
            else:
                # ENfetchEN
                step_name_map = {
                    1: "EN",
                    2: "timeEN", 
                    3: "ENscoring",
                    4: "titlegenerate",
                    5: "EN",
                    6: "videoEN"
                }
                step_name = step_name_map.get(current_step, "processing...")
            
            # ENprogressEN
            progress_message = f"currentlyexecute{step_name}..."
            if error_message:
                progress_message = f"processingfailed: {error_message}"
            elif status == TaskStatus.COMPLETED:
                progress_message = "processingEN"
            
            # EN
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
            
            # useENsendWebSocketEN
            def send_notification():
                try:
                    # ENfetchEN
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # ifENcurrentlyrun，useEN
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(
                                asyncio.run,
                                self._async_send_progress_update(payload)
                            )
                            future.result(timeout=5)  # 5ENtimeout
                    else:
                        # ifENrun，ENrun
                        loop.run_until_complete(
                            self._async_send_progress_update(payload)
                        )
                except Exception as e:
                    logger.error(f"sendWebSocketENfailed: {e}")
            
            # ENsendEN
            import threading
            thread = threading.Thread(target=send_notification)
            thread.daemon = True
            thread.start()
            
            logger.debug(f"ENsendENprogressupdate: {self.project_id} - {progress}% - {step_name}")
            
        except Exception as e:
            logger.error(f"sendENprogressupdatefailed: {e}")
    
    async def _async_send_progress_update(self, payload: dict):
        """ENsendprogressupdateEN"""
        try:
            import redis.asyncio as redis
            import json
            from ..core.config import get_redis_url
            from .progress_snapshot_service import snapshot_service
            
            # connectRedis
            redis_client = redis.from_url(get_redis_url(), decode_responses=True)
            
            # EN - useEN
            from .websocket_gateway_service import WebSocketGatewayService
            channel = WebSocketGatewayService.normalize_channel(self.project_id)
            
            # 1) saveEN
            await snapshot_service.save_snapshot(channel, payload)
            
            # 2) ENRedis
            await redis_client.publish(channel, json.dumps(payload, ensure_ascii=False))
            
            # 3) ENRedisconnect
            await redis_client.aclose()
            
            logger.debug(f"progressupdateEN: {channel} - {payload}")
            
        except Exception as e:
            logger.error(f"ENsendprogressupdatefailed: {e}")
    
    def _get_step_number(self, step: ProcessingStep) -> int:
        """fetchEN"""
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
        """fetchENprogressEN"""
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
        """saveENresultENdatabase"""
        # ENcanENneedENresultsaveENdatabaseEN
        # ENclipresultsaveENClipEN，collectionresultsaveENCollectionEN
        logger.info(f"EN {step.value} resultENsave")
    
    def _save_pipeline_results_to_database(self, results: Dict[str, Any]):
        """ENexecuteresultsaveENdatabase"""
        try:
            logger.info(f"startsaveproject {self.project_id} ENresultENdatabase")
            
            # fetchprojectdirectory
            project_dir = self.adapter.data_dir / "projects" / self.project_id
            
            # useDataSyncServiceENdatabase
            from ..services.data_sync_service import DataSyncService
            sync_service = DataSyncService(self.db)
            
            # ENprojectEN
            sync_result = sync_service.sync_project_from_filesystem(self.project_id, project_dir)
            
            if sync_result.get("success"):
                logger.info(f"project {self.project_id} ENsucceeded: {sync_result}")
            else:
                logger.error(f"project {self.project_id} ENfailed: {sync_result}")
                self.db.rollback()
                raise RuntimeError(f"ENfailed: {sync_result}")
            
            logger.info(f"project {self.project_id} ENresultENsaveENdatabase")
            
        except Exception as e:
            logger.error(f"saveENresultENdatabasefailed: {e}")
            self.db.rollback()
            raise
    
    def _validate_step_dependencies(self, steps_to_execute: List[ProcessingStep]):
        """validateEN"""
        # EN
        step_dependencies = {
            ProcessingStep.STEP2_TIMELINE: [ProcessingStep.STEP1_OUTLINE],
            ProcessingStep.STEP3_SCORING: [ProcessingStep.STEP2_TIMELINE],
            ProcessingStep.STEP4_TITLE: [ProcessingStep.STEP3_SCORING],
            ProcessingStep.STEP5_CLUSTERING: [ProcessingStep.STEP4_TITLE],
            ProcessingStep.STEP6_VIDEO: [ProcessingStep.STEP5_CLUSTERING]
        }
        
        # ENcheckEN，becauseENexecuteENcheck
        if steps_to_execute:
            first_step = steps_to_execute[0]
            if first_step in step_dependencies:
                required_steps = step_dependencies[first_step]
                missing_steps = []
                
                for req_step in required_steps:
                    # checkENalreadyEN（throughcheckENfile）
                    step_output = self.adapter.get_step_output_path(req_step.value)
                    if not step_output.exists():
                        missing_steps.append(req_step)
                
                if missing_steps:
                    missing_step_names = [step.value for step in missing_steps]
                    raise ValueError(f"EN {first_step.value} EN: {missing_step_names}")
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """fetchENstatus"""
        task = self.task_repo.get_by_id(self.task_id)
        if not task:
            return {"error": "taskdoes not exist"}
        
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
        """retryEN"""
        logger.info(f"retryEN: {step.value}")
        
        # ENfile
        self.adapter.cleanup_intermediate_files(step.value)
        
        # ENexecuteEN
        return self.execute_step(step, **kwargs)
    
    def get_step_result(self, step: ProcessingStep) -> Any:
        """fetchENresult"""
        return self.adapter.get_step_result(step.value)
    
    def get_step_performance_summary(self) -> Dict[str, Any]:
        """fetchEN"""
        if not self.step_timings:
            return {"message": "EN"}
        
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
        """ENexecute"""
        logger.info(f"EN {start_step.value} ENexecute")
        
        # fetchENstartENallEN
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
            
            # ENexecuteEN
            steps_to_execute = []
            for step in all_steps[start_index:]:
                step_output = self.adapter.get_step_output_path(step.value)
                if not step_output.exists():
                    steps_to_execute.append(step)
                else:
                    logger.info(f"EN {step.value} completed，EN")
            
            if not steps_to_execute:
                logger.info("allENcompleted，ENexecute")
                return {"message": "allENcompleted"}
            
            logger.info(f"ENexecuteEN: {[step.value for step in steps_to_execute]}")
            
            if start_step == ProcessingStep.STEP1_OUTLINE:
                if not srt_path:
                    raise ValueError("ENStep1ENneedENSRTfilepath")
                return self.execute_pipeline(srt_path, steps_to_execute)
            else:
                # validateENcompleted
                for step in all_steps[:start_index]:
                    step_output = self.adapter.get_step_output_path(step.value)
                    if not step_output.exists():
                        raise ValueError(f"EN {step.value} EN，cannotEN {start_step.value} EN")
                
                return self.execute_pipeline(Path("dummy.srt"), steps_to_execute)
                
        except ValueError as e:
            logger.error(f"ENexecutefailed: {e}")
            raise
    
    def get_step_status_summary(self) -> Dict[str, Any]:
        """fetchENstatusEN"""
        if not self.step_status:
            return {"message": "ENstatusEN"}
        
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
