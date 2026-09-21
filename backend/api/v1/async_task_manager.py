"""
ENtaskEN
ENexceptionENrestart
"""

import asyncio
import logging
from typing import Callable, Any, Dict, Optional
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)

class AsyncTaskManager:
    """ENtaskEN"""
    
    def __init__(self):
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.task_results: Dict[str, Any] = {}
    
    async def create_safe_task(
        self, 
        task_id: str, 
        coro: Callable, 
        *args, 
        **kwargs
    ) -> asyncio.Task:
        """
        createENtask，ENexception
        
        Args:
            task_id: taskID
            coro: EN
            *args: ENparameters
            **kwargs: ENparameters
            
        Returns:
            ENtaskEN
        """
        
        async def safe_wrapper():
            """EN，ENallexception"""
            try:
                logger.info(f"startexecutetask: {task_id}")
                result = await coro(*args, **kwargs)
                self.task_results[task_id] = {
                    "status": "completed",
                    "result": result,
                    "completed_at": datetime.now().isoformat()
                }
                logger.info(f"taskEN: {task_id}")
                return result
                
            except Exception as e:
                error_info = {
                    "status": "failed",
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "traceback": traceback.format_exc(),
                    "failed_at": datetime.now().isoformat()
                }
                self.task_results[task_id] = error_info
                logger.error(f"taskfailed: {task_id}, error: {e}")
                logger.error(f"errorEN: {traceback.format_exc()}")
                
                # ENexception，EN
                return error_info
        
        # createtask
        task = asyncio.create_task(safe_wrapper())
        self.running_tasks[task_id] = task
        
        # EN
        task.add_done_callback(lambda t: self._cleanup_task(task_id))
        
        return task
    
    def _cleanup_task(self, task_id: str):
        """ENtask"""
        if task_id in self.running_tasks:
            del self.running_tasks[task_id]
        logger.debug(f"taskEN: {task_id}")
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """fetchtaskstatus"""
        if task_id in self.running_tasks:
            task = self.running_tasks[task_id]
            return {
                "status": "running",
                "task_id": task_id,
                "created_at": "unknown"  # canENcreatetime
            }
        elif task_id in self.task_results:
            return self.task_results[task_id]
        else:
            return None
    
    def cancel_task(self, task_id: str) -> bool:
        """canceltask"""
        if task_id in self.running_tasks:
            task = self.running_tasks[task_id]
            task.cancel()
            logger.info(f"taskENcancel: {task_id}")
            return True
        return False
    
    def get_all_tasks(self) -> Dict[str, Any]:
        """fetchalltaskstatus"""
        all_tasks = {}
        
        # runENtask
        for task_id, task in self.running_tasks.items():
            all_tasks[task_id] = {
                "status": "running",
                "task_id": task_id
            }
        
        # completedENtask
        for task_id, result in self.task_results.items():
            all_tasks[task_id] = result
        
        return all_tasks

# ENtaskEN
task_manager = AsyncTaskManager()

# EN
def safe_async_task(task_id: str):
    """
    EN：ENtask
    
    Usage:
        @safe_async_task("my_task")
        async def my_function():
            # EN
            pass
    """
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            return await task_manager.create_safe_task(task_id, func, *args, **kwargs)
        return wrapper
    return decorator

# useEN
async def example_usage():
    """useEN"""
    
    async def risky_task():
        """mayfailedENtask"""
        await asyncio.sleep(1)
        # ENmayENexception
        if True:  # canENFalseEN
            raise ValueError("ENerror")
        return "taskEN"
    
    # createENtask
    task = await task_manager.create_safe_task("example_task", risky_task)
    
    # ENtaskEN
    result = await task
    print(f"taskresult: {result}")
    
    # checktaskstatus
    status = task_manager.get_task_status("example_task")
    print(f"taskstatus: {status}")

if __name__ == "__main__":
    asyncio.run(example_usage())

