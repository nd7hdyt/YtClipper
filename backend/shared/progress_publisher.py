"""
translatedone'sprogressReleaseservice
Providestranslated'sprogresstranslatedReleasetranslated
"""

import json
import time
import logging
import asyncio
from typing import Dict, Any, Optional
import redis.asyncio as redis
from .progress_channels import project_progress_channel
from ..core.config import get_redis_url

logger = logging.getLogger(__name__)

class ProgressPublisher:
    """translatedone'sprogressReleasetranslated"""
    
    def __init__(self):
        self.redis_url = get_redis_url()
        self.redis_client: Optional[redis.Redis] = None
    
    async def _get_redis_client(self) -> redis.Redis:
        """fetchRedistranslated"""
        if self.redis_client is None:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
        return self.redis_client
    
    async def publish_project_progress(
        self, 
        project_id: str, 
        step: int, 
        total_steps: int, 
        percent: float, 
        message: str, 
        status: str = "running",
        task_id: Optional[str] = None
    ) -> bool:
        """
        Releaseprojectprogresstranslated
        
        Args:
            project_id: projectID
            step: translatedstep
            total_steps: translatedsteptranslated
            percent: progresstranslated (0-100)
            message: progresstranslated
            status: status (running/succeeded/failed)
            task_id: taskID（canSelect）
            
        Returns:
            IstranslatedReleasesucceeded
        """
        try:
            channel = project_progress_channel(project_id)
            payload = {
                "type": "project_progress",
                "projectId": project_id,
                "step": step,
                "totalSteps": total_steps,
                "percent": percent,
                "message": message,
                "status": status,
                "ts": time.time()
            }
            
            if task_id:
                payload["taskId"] = task_id
            
            redis_client = await self._get_redis_client()
            await redis_client.publish(channel, json.dumps(payload, ensure_ascii=False))
            
            logger.info(f"progresstranslatedRelease: {project_id} - {percent}% - {message}")
            return True
            
        except Exception as e:
            logger.error(f"Releaseprogresstranslatedfailed: {e}")
            return False
    
    async def close(self):
        """translatedRedisconnect"""
        if self.redis_client:
            await self.redis_client.close()

# translated
progress_publisher = ProgressPublisher()

# translated
async def publish_project_progress(
    project_id: str, 
    step: int, 
    total_steps: int, 
    percent: float, 
    message: str, 
    status: str = "running",
    task_id: Optional[str] = None
) -> bool:
    """Releaseprojectprogress'stranslated"""
    return await progress_publisher.publish_project_progress(
        project_id, step, total_steps, percent, message, status, task_id
    )
