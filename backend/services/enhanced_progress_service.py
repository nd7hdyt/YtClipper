"""
translatedprogressservice
translatedprogressSystem，Providestranslated'serrorprocessAndstatustranslated
"""

import time
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import redis
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..models.project import Project, ProjectStatus
from ..models.task import Task, TaskStatus
from ..utils.error_handler import AutoClipsException, ErrorCategory

logger = logging.getLogger(__name__)


class ProgressStage(Enum):
    """progresstranslated"""
    INGEST = "INGEST"          # download/translated
    SUBTITLE = "SUBTITLE"      # subtitles/translated
    ANALYZE = "ANALYZE"        # translated/translated
    HIGHLIGHT = "HIGHLIGHT"    # translated/translated
    EXPORT = "EXPORT"          # export/translated
    DONE = "DONE"              # translated/translated
    ERROR = "ERROR"            # errorstatus


class ProgressStatus(Enum):
    """progressstatustranslated"""
    PtranslatedDING = "PtranslatedDING"        # etc.translated
    RUNNING = "RUNNING"        # translated
    COMPLETED = "COMPLETED"    # completed
    FAILED = "FAILED"          # failed
    CANCELLED = "CANCELLED"    # translatedcancel


@dataclass
class ProgressInfo:
    """progressinfotranslated"""
    project_id: str
    task_id: Optional[str] = None
    stage: ProgressStage = ProgressStage.INGEST
    status: ProgressStatus = ProgressStatus.PtranslatedDING
    progress: int = 0  # 0-100
    message: str = ""
    error_message: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    estimated_remaining: Optional[int] = None  # translated(seconds)
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """translatedformat"""
        data = asdict(self)
        # translated
        data['stage'] = self.stage.value
        data['status'] = self.status.value
        # translated
        if self.start_time:
            data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProgressInfo':
        """fromtranslatedcreatetranslated"""
        # translated
        if 'stage' in data and isinstance(data['stage'], str):
            data['stage'] = ProgressStage(data['stage'])
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = ProgressStatus(data['status'])
        # translated
        if 'start_time' in data and isinstance(data['start_time'], str):
            data['start_time'] = datetime.fromisoformat(data['start_time'])
        if 'end_time' in data and isinstance(data['end_time'], str):
            data['end_time'] = datetime.fromisoformat(data['end_time'])
        return cls(**data)


class EnhancedProgressService:
    """translatedprogressservice"""
    
    # translated
    STAGE_WEIGHTS = {
        ProgressStage.INGEST: 10,
        ProgressStage.SUBTITLE: 15,
        ProgressStage.ANALYZE: 20,
        ProgressStage.HIGHLIGHT: 25,
        ProgressStage.EXPORT: 20,
        ProgressStage.DONE: 10,
    }
    
    # translated
    STAGE_ORDER = [
        ProgressStage.INGEST,
        ProgressStage.SUBTITLE,
        ProgressStage.ANALYZE,
        ProgressStage.HIGHLIGHT,
        ProgressStage.EXPORT,
        ProgressStage.DONE,
    ]
    
    def __init__(self):
        self.redis_client = None
        self._init_redis()
        self.progress_cache: Dict[str, ProgressInfo] = {}
        self.progress_callbacks: List[Callable[[ProgressInfo], None]] = []
    
    def _init_redis(self):
        """translatedRedisconnect"""
        try:
            self.redis_client = redis.Redis.from_url(
                "redis://127.0.0.1:6379/0", 
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            # testconnect
            self.redis_client.ping()
            logger.info("Redisconnectsucceeded")
        except Exception as e:
            logger.warning(f"Redisconnectfailed，translatedusetranslatedcache: {e}")
            self.redis_client = None
    
    def _get_redis_key(self, project_id: str) -> str:
        """fetchRedistranslated"""
        return f"progress:{project_id}"
    
    def _calculate_progress(self, stage: ProgressStage, sub_progress: float = 0.0) -> int:
        """translatedprogresstranslated"""
        # translated'stranslated
        total_weight = 0
        current_stage_weight = 0
        
        for s in self.STAGE_ORDER:
            if s == stage:
                current_stage_weight = self.STAGE_WEIGHTS.get(s, 0)
                break
            total_weight += self.STAGE_WEIGHTS.get(s, 0)
        
        # translatedCurrent Stage'sprogress
        if stage == ProgressStage.DONE:
            return 100
        elif stage == ProgressStage.ERROR:
            return total_weight  # errortranslatedprogress
        
        # addCurrent Stage'stranslatedprogress
        current_progress = int(current_stage_weight * sub_progress / 100.0)
        total_progress = total_weight + current_progress
        
        return min(99, total_progress)
    
    def _estimate_remaining_time(self, progress_info: ProgressInfo) -> Optional[int]:
        """translated"""
        if not progress_info.start_time or progress_info.progress <= 0:
            return None
        
        elapsed = (datetime.utcnow() - progress_info.start_time).total_seconds()
        if elapsed <= 0:
            return None
        
        # Based ontranslatedprogresstranslated
        estimated_total = elapsed * 100 / progress_info.progress
        remaining = estimated_total - elapsed
        
        return max(0, int(remaining))
    
    def start_progress(self, project_id: str, task_id: Optional[str] = None, 
                      initial_message: str = "translatedprocess") -> ProgressInfo:
        """translatedprogresstranslated"""
        try:
            progress_info = ProgressInfo(
                project_id=project_id,
                task_id=task_id,
                stage=ProgressStage.INGEST,
                status=ProgressStatus.RUNNING,
                progress=0,
                message=initial_message,
                start_time=datetime.utcnow()
            )
            
            # translatedcache
            self.progress_cache[project_id] = progress_info
            
            # translatedRedis
            if self.redis_client:
                try:
                    self.redis_client.setex(
                        self._get_redis_key(project_id),
                        3600,  # 1translated
                        json.dumps(progress_info.to_dict())
                    )
                except Exception as e:
                    logger.warning(f"translatedprogresstranslatedRedisfailed: {e}")
            
            # updatedatabase
            self._update_database_progress(progress_info)
            
            # translated
            self._trigger_callbacks(progress_info)
            
            logger.info(f"translatedproject {project_id} 'sprogress")
            return progress_info
            
        except Exception as e:
            logger.error(f"translatedprogresstranslatedfailed: {e}")
            raise AutoClipsException(
                message="translatedprogresstranslatedfailed",
                category=ErrorCategory.SYSTEM,
                original_exception=e
            )
    
    def update_progress(self, project_id: str, stage: ProgressStage, 
                       message: str = "", sub_progress: float = 0.0,
                       metadata: Optional[Dict[str, Any]] = None) -> ProgressInfo:
        """updateprogress"""
        try:
            # fetchtranslatedprogressinfo
            progress_info = self.get_progress(project_id)
            if not progress_info:
                logger.warning(f"project {project_id} 'sprogressinfonot found，createtranslated's")
                progress_info = self.start_progress(project_id, message=message)
            
            # updateprogressinfo
            progress_info.stage = stage
            progress_info.message = message
            progress_info.progress = self._calculate_progress(stage, sub_progress)
            progress_info.estimated_remaining = self._estimate_remaining_time(progress_info)
            
            if metadata:
                if progress_info.metadata:
                    progress_info.metadata.update(metadata)
                else:
                    progress_info.metadata = metadata
            
            # translatedcache
            self.progress_cache[project_id] = progress_info
            
            # translatedRedis
            if self.redis_client:
                try:
                    self.redis_client.setex(
                        self._get_redis_key(project_id),
                        3600,
                        json.dumps(progress_info.to_dict())
                    )
                except Exception as e:
                    logger.warning(f"updateRedisprogressfailed: {e}")
            
            # updatedatabase
            self._update_database_progress(progress_info)
            
            # translated
            self._trigger_callbacks(progress_info)
            
            logger.info(f"project {project_id} progressupdate: {progress_info.progress}% - {stage.value}")
            return progress_info
            
        except Exception as e:
            logger.error(f"updateprogressfailed: {e}")
            raise AutoClipsException(
                message="updateprogressfailed",
                category=ErrorCategory.SYSTEM,
                original_exception=e
            )
    
    def complete_progress(self, project_id: str, message: str = "processing completed") -> ProgressInfo:
        """translatedprogress"""
        try:
            progress_info = self.get_progress(project_id)
            if not progress_info:
                logger.warning(f"project {project_id} 'sprogressinfonot found")
                return None
            
            # updatetranslatedstatus
            progress_info.stage = ProgressStage.DONE
            progress_info.status = ProgressStatus.COMPLETED
            progress_info.progress = 100
            progress_info.message = message
            progress_info.end_time = datetime.utcnow()
            progress_info.estimated_remaining = 0
            
            # translatedcache
            self.progress_cache[project_id] = progress_info
            
            # translatedRedis
            if self.redis_client:
                try:
                    self.redis_client.setex(
                        self._get_redis_key(project_id),
                        3600,
                        json.dumps(progress_info.to_dict())
                    )
                except Exception as e:
                    logger.warning(f"translatedstatustranslatedRedisfailed: {e}")
            
            # updatedatabase
            self._update_database_progress(progress_info)
            
            # translated
            self._trigger_callbacks(progress_info)
            
            logger.info(f"project {project_id} processing completed")
            return progress_info
            
        except Exception as e:
            logger.error(f"translatedprogressfailed: {e}")
            raise AutoClipsException(
                message="translatedprogressfailed",
                category=ErrorCategory.SYSTEM,
                original_exception=e
            )
    
    def fail_progress(self, project_id: str, error_message: str) -> ProgressInfo:
        """translatedprogresstranslatedfailed"""
        try:
            progress_info = self.get_progress(project_id)
            if not progress_info:
                logger.warning(f"project {project_id} 'sprogressinfonot found")
                return None
            
            # updatetranslatedfailedstatus
            progress_info.stage = ProgressStage.ERROR
            progress_info.status = ProgressStatus.FAILED
            progress_info.error_message = error_message
            progress_info.end_time = datetime.utcnow()
            progress_info.estimated_remaining = 0
            
            # translatedcache
            self.progress_cache[project_id] = progress_info
            
            # translatedRedis
            if self.redis_client:
                try:
                    self.redis_client.setex(
                        self._get_redis_key(project_id),
                        3600,
                        json.dumps(progress_info.to_dict())
                    )
                except Exception as e:
                    logger.warning(f"translatedfailedstatustranslatedRedisfailed: {e}")
            
            # updatedatabase
            self._update_database_progress(progress_info)
            
            # translated
            self._trigger_callbacks(progress_info)
            
            logger.error(f"project {project_id} processing failed: {error_message}")
            return progress_info
            
        except Exception as e:
            logger.error(f"translatedprogressfailedfailed: {e}")
            raise AutoClipsException(
                message="translatedprogressfailedfailed",
                category=ErrorCategory.SYSTEM,
                original_exception=e
            )
    
    def get_progress(self, project_id: str) -> Optional[ProgressInfo]:
        """fetchprogressinfo"""
        try:
            # translatedfromcachefetch
            if project_id in self.progress_cache:
                return self.progress_cache[project_id]
            
            # fromRedisfetch
            if self.redis_client:
                try:
                    redis_data = self.redis_client.get(self._get_redis_key(project_id))
                    if redis_data:
                        data = json.loads(redis_data)
                        progress_info = ProgressInfo.from_dict(data)
                        self.progress_cache[project_id] = progress_info
                        return progress_info
                except Exception as e:
                    logger.warning(f"fromRedisfetchprogressfailed: {e}")
            
            # fromdatabasefetch
            db = SessionLocal()
            try:
                project = db.query(Project).filter(Project.id == project_id).first()
                if project:
                    # translatedprojectstatuscreateprogressinfo
                    stage = self._map_project_status_to_stage(project.status)
                    status = self._map_project_status_to_progress_status(project.status)
                    
                    progress_info = ProgressInfo(
                        project_id=project_id,
                        stage=stage,
                        status=status,
                        progress=self._calculate_progress(stage),
                        message=f"projectstatus: {project.status}",
                        start_time=project.created_at,
                        end_time=project.updated_at if status == ProgressStatus.COMPLETED else None
                    )
                    
                    self.progress_cache[project_id] = progress_info
                    return progress_info
            finally:
                db.close()
            
            return None
            
        except Exception as e:
            logger.error(f"fetchprogressinfofailed: {e}")
            return None
    
    def _map_project_status_to_stage(self, project_status: str) -> ProgressStage:
        """translatedprojectstatustranslatedprogresstranslated"""
        status_mapping = {
            ProjectStatus.PtranslatedDING: ProgressStage.INGEST,
            ProjectStatus.PROCESSING: ProgressStage.ANALYZE,
            ProjectStatus.COMPLETED: ProgressStage.DONE,
            ProjectStatus.FAILED: ProgressStage.ERROR,
        }
        return status_mapping.get(project_status, ProgressStage.INGEST)
    
    def _map_project_status_to_progress_status(self, project_status: str) -> ProgressStatus:
        """translatedprojectstatustranslatedprogressstatus"""
        status_mapping = {
            ProjectStatus.PtranslatedDING: ProgressStatus.PtranslatedDING,
            ProjectStatus.PROCESSING: ProgressStatus.RUNNING,
            ProjectStatus.COMPLETED: ProgressStatus.COMPLETED,
            ProjectStatus.FAILED: ProgressStatus.FAILED,
        }
        return status_mapping.get(project_status, ProgressStatus.PtranslatedDING)
    
    def _update_database_progress(self, progress_info: ProgressInfo):
        """updatedatabasetranslated'sprogressinfo"""
        try:
            db = SessionLocal()
            try:
                # updateprojectstatus
                project = db.query(Project).filter(Project.id == progress_info.project_id).first()
                if project:
                    if progress_info.status == ProgressStatus.COMPLETED:
                        project.status = ProjectStatus.COMPLETED
                    elif progress_info.status == ProgressStatus.FAILED:
                        project.status = ProjectStatus.FAILED
                    elif progress_info.status == ProgressStatus.RUNNING:
                        project.status = ProjectStatus.PROCESSING
                    
                    project.updated_at = datetime.utcnow()
                    db.commit()
                
                # updatetaskstatus
                if progress_info.task_id:
                    task = db.query(Task).filter(Task.id == progress_info.task_id).first()
                    if task:
                        task.progress = progress_info.progress
                        task.current_step = progress_info.stage.value
                        task.updated_at = datetime.utcnow()
                        
                        if progress_info.status == ProgressStatus.COMPLETED:
                            task.status = TaskStatus.COMPLETED
                        elif progress_info.status == ProgressStatus.FAILED:
                            task.status = TaskStatus.FAILED
                            task.error_message = progress_info.error_message
                        
                        db.commit()
                        
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"updatedatabaseprogressfailed: {e}")
    
    def add_progress_callback(self, callback: Callable[[ProgressInfo], None]):
        """translatedAdd totranslated"""
        self.progress_callbacks.append(callback)
    
    def remove_progress_callback(self, callback: Callable[[ProgressInfo], None]):
        """translatedprogresstranslated"""
        if callback in self.progress_callbacks:
            self.progress_callbacks.remove(callback)
    
    def _trigger_callbacks(self, progress_info: ProgressInfo):
        """translatedprogresstranslated"""
        for callback in self.progress_callbacks:
            try:
                callback(progress_info)
            except Exception as e:
                logger.error(f"progresstranslatedfailed: {e}")
    
    def cleanup_old_progress(self, max_age_hours: int = 24):
        """cleantranslated'sprogressinfo"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
            cleaned_count = 0
            
            # cleancache
            for project_id, progress_info in list(self.progress_cache.items()):
                if progress_info.end_time and progress_info.end_time < cutoff_time:
                    del self.progress_cache[project_id]
                    cleaned_count += 1
            
            # cleanRedis
            if self.redis_client:
                try:
                    # fetchtranslatedprogresstranslated
                    keys = self.redis_client.keys("progress:*")
                    for key in keys:
                        try:
                            data = self.redis_client.get(key)
                            if data:
                                progress_data = json.loads(data)
                                if 'end_time' in progress_data:
                                    end_time = datetime.fromisoformat(progress_data['end_time'])
                                    if end_time < cutoff_time:
                                        self.redis_client.delete(key)
                                        cleaned_count += 1
                        except Exception as e:
                            logger.warning(f"cleanRedistranslated {key} failed: {e}")
                except Exception as e:
                    logger.warning(f"cleanRedisprogressfailed: {e}")
            
            logger.info(f"cleantranslated {cleaned_count}  translatedprogresstranslated")
            
        except Exception as e:
            logger.error(f"cleantranslatedprogressfailed: {e}")
    
    def get_all_active_progress(self) -> List[ProgressInfo]:
        """fetchtranslated'sprogressinfo"""
        try:
            active_progress = []
            
            # fromcachefetch
            for progress_info in self.progress_cache.values():
                if progress_info.status in [ProgressStatus.PtranslatedDING, ProgressStatus.RUNNING]:
                    active_progress.append(progress_info)
            
            # fromRedisfetch
            if self.redis_client:
                try:
                    keys = self.redis_client.keys("progress:*")
                    for key in keys:
                        try:
                            data = self.redis_client.get(key)
                            if data:
                                progress_data = json.loads(data)
                                progress_info = ProgressInfo.from_dict(progress_data)
                                if progress_info.status in [ProgressStatus.PtranslatedDING, ProgressStatus.RUNNING]:
                                    # translated
                                    if not any(p.project_id == progress_info.project_id for p in active_progress):
                                        active_progress.append(progress_info)
                        except Exception as e:
                            logger.warning(f"translatedRedisprogresstranslatedfailed: {e}")
                except Exception as e:
                    logger.warning(f"fetchRedisprogressfailed: {e}")
            
            return active_progress
            
        except Exception as e:
            logger.error(f"fetchtranslatedprogressfailed: {e}")
            return []


# translatedprogressservicetranslated
progress_service = EnhancedProgressService()


# translated
def start_progress(project_id: str, task_id: Optional[str] = None, 
                  initial_message: str = "translatedprocess") -> ProgressInfo:
    """translatedprogresstranslated"""
    return progress_service.start_progress(project_id, task_id, initial_message)


def update_progress(project_id: str, stage: ProgressStage, 
                   message: str = "", sub_progress: float = 0.0,
                   metadata: Optional[Dict[str, Any]] = None) -> ProgressInfo:
    """updateprogress"""
    return progress_service.update_progress(project_id, stage, message, sub_progress, metadata)


def complete_progress(project_id: str, message: str = "processing completed") -> ProgressInfo:
    """translatedprogress"""
    return progress_service.complete_progress(project_id, message)


def fail_progress(project_id: str, error_message: str) -> ProgressInfo:
    """translatedprogresstranslatedfailed"""
    return progress_service.fail_progress(project_id, error_message)


def get_progress(project_id: str) -> Optional[ProgressInfo]:
    """fetchprogressinfo"""
    return progress_service.get_progress(project_id)
