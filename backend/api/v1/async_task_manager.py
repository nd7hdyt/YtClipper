"""
translatedtasktranslated
translated'stranslatedbackendtranslated
"""

import asyncio
import logging
from typing import Callable, Any, Dict, Optional
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)

class AsyncTaskManager:
    """translatedtasktranslated"""
    
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
        createtranslated'stranslatedtask，translated
        
        Args:
            task_id: taskID
            coro: translated
            *args: translated
            **kwargs: translated
            
        Returns:
            translatedtasktranslated
        """
        
        async def safe_wrapper():
            """translatedPackagetranslated，translated"""
            try:
                logger.info(f"translatedtask: {task_id}")
                result = await coro(*args, **kwargs)
                self.task_results[task_id] = {
                    "status": "completed",
                    "result": result,
                    "completed_at": datetime.now().isoformat()
                }
                logger.info(f"tasktranslated: {task_id}")
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
                logger.error(f"errortranslated: {traceback.format_exc()}")
                
                # translated，translated
                return error_info
        
        # createtask
        task = asyncio.create_task(safe_wrapper())
        self.running_tasks[task_id] = task
        
        # addtranslated
        task.add_done_callback(lambda t: self._cleanup_task(task_id))
        
        return task
    
    def _cleanup_task(self, task_id: str):
        """cleantranslated'stask"""
        if task_id in self.running_tasks:
            del self.running_tasks[task_id]
        logger.debug(f"tasktranslatedclean: {task_id}")
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """fetchtaskstatus"""
        if task_id in self.running_tasks:
            task = self.running_tasks[task_id]
            return {
                "status": "running",
                "task_id": task_id,
                "created_at": "unknown"  # cantranslatedcreatetranslated
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
            logger.info(f"tasktranslatedcancel: {task_id}")
            return True
        return False
    
    def get_all_tasks(self) -> Dict[str, Any]:
        """fetchtranslatedtaskstatus"""
        all_tasks = {}
        
        # translated'stask
        for task_id, task in self.running_tasks.items():
            all_tasks[task_id] = {
                "status": "running",
                "task_id": task_id
            }
        
        # completed'stask
        for task_id, result in self.task_results.items():
            all_tasks[task_id] = result
        
        return all_tasks

# translatedtasktranslated
task_manager = AsyncTaskManager()

# translated
def safe_async_task(task_id: str):
    """
    translated：translatedPackagetranslated'stranslatedtask
    
    Usage:
        @safe_async_task("my_task")
        async def my_function():
            # translated
            pass
    """
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            return await task_manager.create_safe_task(task_id, func, *args, **kwargs)
        return wrapper
    return decorator

# usetranslated
async def example_usage():
    """usetranslated"""
    
    async def risky_task():
        """cantranslatedfailed'stask"""
        await asyncio.sleep(1)
        # translatedcantranslated'stranslated
        if True:  # cantranslatedFalsetranslatedtesttranslated
            raise ValueError("translatederror")
        return "tasktranslated"
    
    # createtranslatedtask
    task = await task_manager.create_safe_task("example_task", risky_task)
    
    # etc.translatedtasktranslated
    result = await task
    print(f"tasktranslated: {result}")
    
    # checktaskstatus
    status = task_manager.get_task_status("example_task")
    print(f"taskstatus: {status}")

if __name__ == "__main__":
    asyncio.run(example_usage())

