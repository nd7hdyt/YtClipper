"""
progressENservice
ENRedis PubSubENtaskprogressEN
"""

import json
import time
import logging
import asyncio
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from dataclasses import dataclass, asdict
import redis.asyncio as redis
from ..core.config import get_redis_url
from ..shared.progress_channels import project_progress_channel

logger = logging.getLogger(__name__)

@dataclass
class ProgressEvent:
    """progressEN"""
    task_id: str
    progress: int  # 0-100
    step: int
    total: int
    phase: str  # transcribe|analyze|clip|encode|upload
    message: str
    status: str  # PENDING|PROGRESS|DONE|FAIL
    seq: int  # EN
    ts: float  # ENtimeEN
    meta: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """EN"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProgressEvent':
        """ENcreateEN"""
        return cls(**data)

class ProgressEventService:
    """progressENservice"""
    
    def __init__(self):
        self.redis_url = get_redis_url()
        self.redis_client: Optional[redis.Redis] = None
        self.sequence_counters: Dict[str, int] = {}  # eachtask_idEN
        self.throttle_cache: Dict[str, Dict[str, Any]] = {}  # ENcache
        self.throttle_interval = 0.2  # 200msEN
        
    async def _get_redis_client(self) -> redis.Redis:
        """fetchRedisEN"""
        if self.redis_client is None:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
        return self.redis_client
    
    def _get_next_seq(self, task_id: str) -> int:
        """fetchEN"""
        if task_id not in self.sequence_counters:
            self.sequence_counters[task_id] = 0
        self.sequence_counters[task_id] += 1
        return self.sequence_counters[task_id]
    
    def _should_throttle(self, task_id: str, progress: int) -> bool:
        """checkENneedEN"""
        now = time.time()
        cache_key = f"{task_id}_{progress}"
        
        if cache_key in self.throttle_cache:
            last_time = self.throttle_cache[cache_key]['timestamp']
            if now - last_time < self.throttle_interval:
                return True
        
        # updatecache
        self.throttle_cache[cache_key] = {
            'timestamp': now,
            'progress': progress
        }
        
        # ENcache（EN1EN）
        expired_keys = [
            key for key, data in self.throttle_cache.items()
            if now - data['timestamp'] > 60
        ]
        for key in expired_keys:
            del self.throttle_cache[key]
        
        return False
    
    async def report_progress(
        self,
        task_id: str,
        progress: int,
        step: int,
        total: int,
        phase: str,
        message: str,
        status: str = "PROGRESS",
        meta: Optional[Dict[str, Any]] = None
    ) -> bool:
        """ENtaskprogress"""
        try:
            # ENcheck
            if status == "PROGRESS" and self._should_throttle(task_id, progress):
                logger.debug(f"task {task_id} progress {progress}% EN")
                return True
            
            # createprogressEN
            event = ProgressEvent(
                task_id=task_id,
                progress=progress,
                step=step,
                total=total,
                phase=phase,
                message=message,
                status=status,
                seq=self._get_next_seq(task_id),
                ts=time.time(),
                meta=meta
            )
            
            # ENRedisEN - useprojectIDENtaskID
            # ENtask_idENproject_id，orusemetaENproject_id
            project_id = meta.get("project_id") if meta else None
            if not project_id:
                # ifmetaENproject_id，ENtask_idEN
                # ENneedEN
                project_id = task_id  # ENusetask_id，ENneedEN
            channel = project_progress_channel(project_id)
            redis_client = await self._get_redis_client()
            
            # meanwhilesaveENRedis Hash
            snapshot_key = f"progress:last:{channel}"
            event_dict = event.to_dict()
            
            # ENNoneEN，ENallEN，ENRedisENerror
            filtered_dict = {}
            for k, v in event_dict.items():
                if v is not None:
                    if isinstance(v, dict):
                        # ENJSONEN
                        filtered_dict[k] = json.dumps(v, ensure_ascii=False)
                    else:
                        filtered_dict[k] = str(v)
            
            await redis_client.hset(snapshot_key, mapping=filtered_dict)
            await redis_client.expire(snapshot_key, 3600)  # 1EN
            
            # EN
            await redis_client.publish(channel, json.dumps(event_dict))
            
            logger.info(f"progressEN: {task_id} - {progress}% - {phase} - seq:{event.seq}")
            return True
            
        except Exception as e:
            logger.error(f"ENprogressENfailed: {e}")
            return False
    
    async def subscribe_to_task(
        self,
        task_id: str,
        callback: Callable[[ProgressEvent], None]
    ) -> bool:
        """ENtaskENprogressEN"""
        try:
            channel = f"progress:{task_id}"
            redis_client = await self._get_redis_client()
            
            pubsub = redis_client.pubsub()
            await pubsub.subscribe(channel)
            
            logger.info(f"ENtaskprogressEN: {channel}")
            
            # ENprocessingEN
            async def message_handler():
                try:
                    async for message in pubsub.listen():
                        if message['type'] == 'message':
                            try:
                                data = json.loads(message['data'])
                                event = ProgressEvent.from_dict(data)
                                callback(event)
                            except Exception as e:
                                logger.error(f"processingprogressENfailed: {e}")
                except Exception as e:
                    logger.error(f"ENprocessingfailed: {e}")
                finally:
                    await pubsub.unsubscribe(channel)
                    await pubsub.close()
            
            # startENprocessingEN
            asyncio.create_task(message_handler())
            return True
            
        except Exception as e:
            logger.error(f"ENtaskprogressfailed: {e}")
            return False
    
    async def get_task_snapshot(self, task_id: str) -> Optional[Dict[str, Any]]:
        """fetchtaskprogressEN"""
        try:
            redis_client = await self._get_redis_client()
            channel = f"progress:{task_id}"
            snapshot_key = f"progress:last:{channel}"
            snapshot = await redis_client.hgetall(snapshot_key)
            if snapshot:
                # ENwhenEN
                if 'progress' in snapshot:
                    snapshot['progress'] = int(snapshot['progress'])
                if 'step' in snapshot:
                    snapshot['step'] = int(snapshot['step'])
                if 'total' in snapshot:
                    snapshot['total'] = int(snapshot['total'])
                if 'seq' in snapshot:
                    snapshot['seq'] = int(snapshot['seq'])
                if 'ts' in snapshot:
                    snapshot['ts'] = float(snapshot['ts'])
                return snapshot
            return None
        except Exception as e:
            logger.error(f"fetchtaskprogressENfailed: {e}")
            return None

    async def get_task_final_state(self, task_id: str) -> Optional[Dict[str, Any]]:
        """fetchtaskENstatus（EN）"""
        try:
            redis_client = await self._get_redis_client()
            key = f"task_final_state:{task_id}"
            data = await redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"fetchtaskENstatusfailed: {e}")
            return None
    
    async def save_task_final_state(self, task_id: str, state: Dict[str, Any]) -> bool:
        """savetaskENstatus"""
        try:
            redis_client = await self._get_redis_client()
            key = f"task_final_state:{task_id}"
            await redis_client.setex(key, 3600, json.dumps(state))  # 1EN
            return True
        except Exception as e:
            logger.error(f"savetaskENstatusfailed: {e}")
            return False
    
    async def close(self):
        """ENRedisconnect"""
        if self.redis_client:
            await self.redis_client.close()

# EN
progress_event_service = ProgressEventService()

# EN
async def report_progress(
    task_id: str,
    progress: int,
    step: int,
    total: int,
    phase: str,
    message: str,
    status: str = "PROGRESS",
    meta: Optional[Dict[str, Any]] = None
) -> bool:
    """ENtaskprogressEN"""
    return await progress_event_service.report_progress(
        task_id, progress, step, total, phase, message, status, meta
    )

