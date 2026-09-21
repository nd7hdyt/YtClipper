"""
EN
processingtaskEN
"""

import logging
import threading
import time
from typing import Dict, Any, Optional, Callable
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta

from .exceptions import ConcurrentError, ErrorCode

logger = logging.getLogger(__name__)


@dataclass
class LockInfo:
    """EN"""
    resource_id: str
    task_id: str
    acquired_at: datetime
    timeout: timedelta
    is_released: bool = False


class ConcurrencyManager:
    """EN"""
    
    def __init__(self):
        self._locks: Dict[str, LockInfo] = {}
        self._lock = threading.RLock()  # ENstatus
    
    def acquire_lock(self, resource_id: str, task_id: str, timeout_seconds: int = 30) -> bool:
        """
        fetchEN
        
        Args:
            resource_id: ENID
            task_id: taskID
            timeout_seconds: timeouttime（EN）
            
        Returns:
            ENsucceededfetchEN
        """
        with self._lock:
            # checkEN
            if resource_id in self._locks:
                existing_lock = self._locks[resource_id]
                
                # checkENtimeout
                if datetime.now() - existing_lock.acquired_at > existing_lock.timeout:
                    logger.warning(f"ENtimeout，EN: {resource_id}")
                    self._release_lock_internal(resource_id)
                else:
                    # checkENtask
                    if existing_lock.task_id == task_id:
                        logger.debug(f"task {task_id} EN: {resource_id}")
                        return True
                    else:
                        logger.warning(f"EN {resource_id} ENtask {existing_lock.task_id} EN")
                        return False
            
            # createEN
            lock_info = LockInfo(
                resource_id=resource_id,
                task_id=task_id,
                acquired_at=datetime.now(),
                timeout=timedelta(seconds=timeout_seconds)
            )
            
            self._locks[resource_id] = lock_info
            logger.info(f"task {task_id} succeededfetchEN: {resource_id}")
            return True
    
    def release_lock(self, resource_id: str, task_id: str) -> bool:
        """
        EN
        
        Args:
            resource_id: ENID
            task_id: taskID
            
        Returns:
            ENsucceededEN
        """
        with self._lock:
            if resource_id not in self._locks:
                logger.warning(f"ENdoes not existEN: {resource_id}")
                return False
            
            lock_info = self._locks[resource_id]
            if lock_info.task_id != task_id:
                logger.warning(f"task {task_id} EN: {resource_id}")
                return False
            
            return self._release_lock_internal(resource_id)
    
    def _release_lock_internal(self, resource_id: str) -> bool:
        """EN"""
        if resource_id in self._locks:
            lock_info = self._locks[resource_id]
            lock_info.is_released = True
            del self._locks[resource_id]
            logger.info(f"EN: {resource_id}")
            return True
        return False
    
    def is_locked(self, resource_id: str) -> bool:
        """checkEN"""
        with self._lock:
            if resource_id not in self._locks:
                return False
            
            lock_info = self._locks[resource_id]
            # checkENtimeout
            if datetime.now() - lock_info.acquired_at > lock_info.timeout:
                self._release_lock_internal(resource_id)
                return False
            
            return True
    
    def get_lock_info(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """fetchEN"""
        with self._lock:
            if resource_id not in self._locks:
                return None
            
            lock_info = self._locks[resource_id]
            return {
                "resource_id": lock_info.resource_id,
                "task_id": lock_info.task_id,
                "acquired_at": lock_info.acquired_at.isoformat(),
                "timeout": lock_info.timeout.total_seconds(),
                "is_released": lock_info.is_released
            }
    
    def cleanup_expired_locks(self):
        """EN"""
        with self._lock:
            current_time = datetime.now()
            expired_resources = []
            
            for resource_id, lock_info in self._locks.items():
                if current_time - lock_info.acquired_at > lock_info.timeout:
                    expired_resources.append(resource_id)
            
            for resource_id in expired_resources:
                self._release_lock_internal(resource_id)
                logger.info(f"EN: {resource_id}")
    
    def get_all_locks(self) -> Dict[str, Dict[str, Any]]:
        """fetchallEN"""
        with self._lock:
            return {
                resource_id: self.get_lock_info(resource_id)
                for resource_id in self._locks.keys()
            }
    
    @contextmanager
    def lock_context(self, resource_id: str, task_id: str, timeout_seconds: int = 30):
        """
        EN
        
        Usage:
            with concurrency_manager.lock_context("project_123", "task_456"):
                # executeneedEN
                pass
        """
        try:
            if not self.acquire_lock(resource_id, task_id, timeout_seconds):
                raise ConcurrentError(
                    f"cannotfetchEN: {resource_id}",
                    resource=resource_id,
                    details={"task_id": task_id, "timeout": timeout_seconds}
                )
            yield
        finally:
            self.release_lock(resource_id, task_id)


class TaskScheduler:
    """taskEN"""
    
    def __init__(self, concurrency_manager: ConcurrencyManager):
        self.concurrency_manager = concurrency_manager
        self._running_tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
    
    def can_start_task(self, project_id: str, task_id: str) -> bool:
        """checkENcanstarttask"""
        resource_id = f"project_{project_id}"
        
        # checkprojectEN
        if self.concurrency_manager.is_locked(resource_id):
            return False
        
        # checktaskENrun
        with self._lock:
            if task_id in self._running_tasks:
                return False
        
        return True
    
    def start_task(self, project_id: str, task_id: str, task_info: Dict[str, Any]) -> bool:
        """starttask"""
        resource_id = f"project_{project_id}"
        
        if not self.can_start_task(project_id, task_id):
            return False
        
        # fetchEN
        if not self.concurrency_manager.acquire_lock(resource_id, task_id):
            return False
        
        # ENrunENtask
        with self._lock:
            self._running_tasks[task_id] = {
                "project_id": project_id,
                "task_id": task_id,
                "started_at": datetime.now(),
                "task_info": task_info
            }
        
        logger.info(f"taskENstart: {task_id} (project: {project_id})")
        return True
    
    def finish_task(self, project_id: str, task_id: str):
        """ENtask"""
        resource_id = f"project_{project_id}"
        
        # EN
        self.concurrency_manager.release_lock(resource_id, task_id)
        
        # ENrunENtaskEN
        with self._lock:
            if task_id in self._running_tasks:
                del self._running_tasks[task_id]
        
        logger.info(f"taskcompleted: {task_id} (project: {project_id})")
    
    def get_running_tasks(self) -> Dict[str, Dict[str, Any]]:
        """fetchrunENtask"""
        with self._lock:
            return self._running_tasks.copy()
    
    def is_task_running(self, task_id: str) -> bool:
        """checktaskENrun"""
        with self._lock:
            return task_id in self._running_tasks


# EN
concurrency_manager = ConcurrencyManager()
task_scheduler = TaskScheduler(concurrency_manager)


def with_concurrency_control(resource_id_func: Callable = None):
    """
    EN
    
    Args:
        resource_id_func: generateENIDEN，ENuseproject_id
        
    Usage:
        @with_concurrency_control()
        def process_project(project_id: str, task_id: str, ...):
            # EN
            pass
        
        @with_concurrency_control(lambda ctx: f"custom_{ctx.project_id}")
        def custom_process(ctx: ProcessingContext):
            # EN
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # ENparametersENproject_idENtask_id
            project_id = None
            task_id = None
            context = None
            
            # checkENProcessingContextparameters
            for arg in args:
                if hasattr(arg, 'project_id') and hasattr(arg, 'task_id'):
                    context = arg
                    project_id = context.project_id
                    task_id = context.task_id
                    break
            
            # ifENcontext，ENkwargsENfetch
            if not project_id:
                project_id = kwargs.get('project_id')
                task_id = kwargs.get('task_id')
            
            # ifEN，ENfetchENparametersENproject_id
            if not project_id and len(args) > 0:
                project_id = str(args[0])
                # generateENtask_id
                task_id = f"temp_task_{project_id}"
            
            if not project_id:
                raise ValueError("cannotENproject_idENtask_id")
            
            # generateENID
            if resource_id_func:
                resource_id = resource_id_func(context or project_id)
            else:
                resource_id = f"project_{project_id}"
            
            # checkENcanstarttask
            if not task_scheduler.can_start_task(project_id, task_id):
                raise ConcurrentError(
                    f"project {project_id} currentlyENtaskprocessing",
                    resource=resource_id,
                    details={"project_id": project_id, "task_id": task_id}
                )
            
            # starttask
            if not task_scheduler.start_task(project_id, task_id, {"function": func.__name__}):
                raise ConcurrentError(
                    f"cannotstarttask: {task_id}",
                    resource=resource_id,
                    details={"project_id": project_id, "task_id": task_id}
                )
            
            try:
                # executeEN
                result = func(*args, **kwargs)
                return result
            finally:
                # ENtask
                task_scheduler.finish_task(project_id, task_id)
        
        return wrapper
    return decorator 