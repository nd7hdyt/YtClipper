"""
WebSockettranslatedservice
translatedRedisprogresstranslatedfrontendWebSocketconnect
supporttranslated、translated、translatedetc.translated
"""

import json
import logging
import asyncio
from typing import Dict, Set, Any, Optional, Callable
from datetime import datetime
import redis.asyncio as redis
from ..core.config import get_redis_url
from ..core.websocket_manager import manager
from .progress_event_service import ProgressEvent, progress_event_service
from .progress_message_adapter import progress_adapter
from .progress_snapshot_service import snapshot_service
from ..shared.progress_channels import normalize_channel, project_progress_channel

logger = logging.getLogger(__name__)

class WebSocketGatewayService:
    """WebSockettranslatedservice"""
    
    def __init__(self):
        self.redis_url = get_redis_url()
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
        self.channels_ref: Dict[str, int] = {}  # channel -> refcount
        self.router: Dict[str, Set[Callable]] = {}  # channel -> set of senders
        self.user_subscriptions: Dict[str, Set[str]] = {}  # user_id -> set of normalized channels
        self.lock = asyncio.Lock()
        self.listen_task: Optional[asyncio.Task] = None
        self.is_running = False
        
        # translated
        self.last_progress: Dict[str, Dict[str, Any]] = {}  # channel -> {progress, timestamp}
        self.throttle_interval = 0.2  # 200mstranslated
    
    @staticmethod
    def normalize_channel(raw: str) -> str:
        """
        translated，usetranslatedone'stranslated
        
        Args:
            raw: translated
            
        Returns:
            translated'stranslated
        """
        return normalize_channel(raw)
        
    async def start(self):
        """starttranslatedservice"""
        if self.is_running:
            return
        
        try:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            self.pubsub = self.redis_client.pubsub(ignore_subscribe_messages=True)
            self.is_running = True
            
            # starttranslatedservice
            await snapshot_service.connect()
            
            # starttranslated
            self.listen_task = asyncio.create_task(self._listen_loop())
            
            logger.info("WebSockettranslatedservicetranslatedstart")
            
        except Exception as e:
            logger.error(f"startWebSockettranslatedservicefailed: {e}")
            self.is_running = False
    
    async def stop(self):
        """translatedservice"""
        self.is_running = False
        
        if self.listen_task:
            self.listen_task.cancel()
            try:
                await self.listen_task
            except asyncio.CancelledError:
                pass
        
        if self.pubsub:
            await self.pubsub.aclose()  # redis-py 5.x translated
        
        if self.redis_client:
            await self.redis_client.aclose()  # redis-py 5.x translated
        
        # translatedservice
        await snapshot_service.disconnect()
        
        logger.info("WebSockettranslatedservicetranslated")
    
    async def sync_user_subscriptions(self, user_id: str, channels: Set[str]) -> Dict[str, int]:
        """
        translatedusertranslated - translatedetc.translated
        
        Args:
            user_id: userID
            channels: translated'stranslated（translatedformat，translated）
            
        Returns:
            translated: {"added": X, "removed": Y, "unchanged": Z}
        """
        async with self.lock:
            # 1) translated
            desired = {self.normalize_channel(ch) for ch in channels}
            current = self.user_subscriptions.get(user_id, set())
            
            # 2) translated
            to_add = desired - current
            to_remove = current - desired
            unchanged = current & desired
            
            # 3) translatedinfo
            added, removed, same = len(to_add), len(to_remove), len(unchanged)
            
            # 4) processaddedtranslated
            for channel in to_add:
                try:
                    await self._subscribe_to_channel(channel)
                    current.add(channel)  # localtranslatedupdate
                    # translated
                    await self._replay_snapshot(user_id, channel)
                except Exception as e:
                    logger.error(f"translatedfailed {channel}: {e}")
            
            # 5) processtranslated
            for channel in to_remove:
                try:
                    await self._unsubscribe_from_channel(channel)
                    current.discard(channel)  # localtranslateddelete
                except Exception as e:
                    logger.error(f"canceltranslatedfailed {channel}: {e}")
            
            # 6) updateusertranslated（usetranslated'stranslated）
            self.user_subscriptions[user_id] = current
            
            # 7) logstranslated：translatedINFO
            if added or removed:
                logger.info(f"translated: user {user_id}, added {added}, translated {removed}, translated {same}")
            else:
                logger.debug(f"translated(translated): user {user_id}, translated {same}")
            
            return {
                "added": added,
                "removed": removed, 
                "unchanged": same
            }
    
    async def _subscribe_to_channel(self, channel: str):
        """translated"""
        if channel not in self.channels_ref:
            self.channels_ref[channel] = 0
            await self.pubsub.subscribe(channel)
            logger.debug(f"translated: {channel}")
        
        self.channels_ref[channel] += 1
    
    async def _unsubscribe_from_channel(self, channel: str):
        """canceltranslated"""
        if channel in self.channels_ref:
            self.channels_ref[channel] -= 1
            if self.channels_ref[channel] <= 0:
                await self.pubsub.unsubscribe(channel)
                del self.channels_ref[channel]
                logger.debug(f"translatedcanceltranslated: {channel}")
    
    async def _replay_snapshot(self, user_id: str, channel: str):
        """translated"""
        try:
            snapshot = await snapshot_service.get_snapshot(channel)
            if snapshot:
                # translated
                simple_msg = progress_adapter.to_simple(snapshot)
                simple_msg["snapshot"] = True
                
                # translateduser
                await manager.send_personal_message(simple_msg, user_id)
                logger.debug(f"translated: {user_id} -> {channel}")
        except Exception as e:
            logger.error(f"translatedfailed: {e}")
    
    async def subscribe_user_to_task(self, user_id: str, task_id: str) -> bool:
        """usertranslatedtask'sprogress"""
        try:
            # translated - useprojectIDtranslatedIstaskID
            # thistranslatedfromtask_idtranslatedproject_id，ortranslatedcalltranslated
            # translatedusetask_id，translatedproject_id
            channel = project_progress_channel(task_id)
            
            # translatedusertranslated
            if user_id not in self.user_subscriptions:
                self.user_subscriptions[user_id] = set()
            self.user_subscriptions[user_id].add(channel)
            
            # createtranslated - useuserIDtranslated
            async def sender(data: str):
                try:
                    logger.debug(f"translated: {data}")
                    message_data = json.loads(data)
                    logger.debug(f"translated'stranslated: {message_data}")
                    
                    # translatedWebSockettranslated
                    ws_message = {
                        "type": "task_progress_update",
                        "task_id": message_data.get("task_id"),
                        "progress": message_data.get("progress"),
                        "step": message_data.get("step"),
                        "total": message_data.get("total"),
                        "phase": message_data.get("phase"),
                        "message": message_data.get("message"),
                        "status": message_data.get("status"),
                        "seq": message_data.get("seq"),
                        "ts": message_data.get("ts"),
                        "meta": message_data.get("meta"),
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    await manager.send_personal_message(ws_message, user_id)
                    logger.debug(f"translateduser {user_id}")
                except Exception as e:
                    logger.error(f"translateduser {user_id} failed: {e}")
            
            # translatedaddtranslated，translated
            sender._user_id = user_id
            sender._task_id = task_id
            
            # translated
            await self._subscribe_channel(channel, sender)
            
            # translatedConfirm
            await manager.send_personal_message({
                "type": "subscription_confirmed",
                "task_id": task_id,
                "message": f"translatedtask {task_id} 'sprogressupdate",
                "timestamp": datetime.utcnow().isoformat()
            }, user_id)
            
            # translated（iftranslatedin）
            try:
                from .progress_event_service import progress_event_service
                snapshot = await progress_event_service.get_task_snapshot(task_id)
                if snapshot:
                    snapshot_message = {
                        "type": "task_progress_update",
                        **snapshot,
                        "snapshot": True  # translated
                    }
                    await manager.send_personal_message(snapshot_message, user_id)
                    logger.debug(f"translatedtask {task_id} 'stranslateduser {user_id}")
            except Exception as e:
                logger.error(f"translatedtasktranslatedfailed: {e}")
            
            logger.debug(f"user {user_id} translatedtask {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"usertranslatedtaskfailed: {e}")
            return False
    
    async def unsubscribe_user_from_task(self, user_id: str, task_id: str) -> bool:
        """usercanceltranslatedtask'sprogress"""
        try:
            channel = f"progress:{task_id}"
            
            # createtranslated（usetranslated）
            async def sender(data: str):
                try:
                    await manager.send_personal_message(json.loads(data), user_id)
                except Exception as e:
                    logger.error(f"translateduser {user_id} failed: {e}")
            
            # canceltranslated
            await self._unsubscribe_channel(channel, sender)
            
            # translatedcanceltranslatedConfirm
            await manager.send_personal_message({
                "type": "unsubscription_confirmed",
                "task_id": task_id,
                "message": f"translatedcanceltranslatedtask {task_id} 'sprogressupdate",
                "timestamp": datetime.utcnow().isoformat()
            }, user_id)
            
            logger.debug(f"user {user_id} translatedcanceltranslatedtask {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"usercanceltranslatedtaskfailed: {e}")
            return False
    
    async def unsubscribe_user_from_all_tasks(self, user_id: str):
        """usertranslatedconnecttranslated，canceltranslated"""
        if user_id in self.user_subscriptions:
            task_ids = list(self.user_subscriptions[user_id])
            for task_id in task_ids:
                await self.unsubscribe_user_from_task(user_id, task_id)
            del self.user_subscriptions[user_id]
            logger.info(f"user {user_id} translatedcanceltranslatedtasktranslated")

    async def subscribe_user_to_many_tasks(self, user_id: str, task_ids: list[str]) -> dict:
        """translatedmulti task - translatedetc.translated"""
        results = {"added": [], "already_subscribed": []}
        
        for task_id in task_ids:
            # checkIstranslated
            if user_id in self.user_subscriptions and task_id in self.user_subscriptions[user_id]:
                results["already_subscribed"].append(task_id)
                logger.debug(f"user {user_id} translatedtask {task_id}，skip")
                continue
            
            # translated
            if await self.subscribe_user_to_task(user_id, task_id):
                results["added"].append(task_id)
            else:
                logger.error(f"user {user_id} translatedtask {task_id} failed")
        
        logger.info(f"translated: user {user_id}, added {len(results['added'])}, translatedin {len(results['already_subscribed'])}")
        return results

    async def unsubscribe_user_from_many_tasks(self, user_id: str, task_ids: list[str]) -> dict:
        """translatedcanceltranslatedmulti task"""
        results = {"removed": [], "not_subscribed": []}
        
        for task_id in task_ids:
            # checkIstranslated
            if user_id not in self.user_subscriptions or task_id not in self.user_subscriptions[user_id]:
                results["not_subscribed"].append(task_id)
                logger.debug(f"user {user_id} translatedtask {task_id}，skip")
                continue
            
            # translatedcanceltranslated
            if await self.unsubscribe_user_from_task(user_id, task_id):
                results["removed"].append(task_id)
            else:
                logger.error(f"user {user_id} canceltranslatedtask {task_id} failed")
        
        logger.info(f"translatedcanceltranslated: user {user_id}, translated {len(results['removed'])}, translated {len(results['not_subscribed'])}")
        return results

    async def sync_user_subscriptions(self, user_id: str, desired_task_ids: list[str]) -> dict:
        """translatedusertranslated - translatedetc.translated"""
        current_task_ids = list(self.user_subscriptions.get(user_id, set()))
        desired_set = set(desired_task_ids)
        current_set = set(current_task_ids)
        
        # translated
        to_add = list(desired_set - current_set)
        to_remove = list(current_set - desired_set)
        
        results = {"added": [], "removed": [], "unchanged": []}
        
        # translatedadd
        if to_add:
            add_results = await self.subscribe_user_to_many_tasks(user_id, to_add)
            results["added"] = add_results["added"]
        
        # translated
        if to_remove:
            remove_results = await self.unsubscribe_user_from_many_tasks(user_id, to_remove)
            results["removed"] = remove_results["removed"]
        
        # translated's
        results["unchanged"] = list(desired_set & current_set)
        
        # translatedintranslatedINFOlogs，translated
        if len(results['added']) > 0 or len(results['removed']) > 0:
            logger.info(f"translated: user {user_id}, added {len(results['added'])}, translated {len(results['removed'])}, translated {len(results['unchanged'])}")
        else:
            logger.debug(f"translated: user {user_id}, added {len(results['added'])}, translated {len(results['removed'])}, translated {len(results['unchanged'])}")
        return results
    
    async def _subscribe_channel(self, channel: str, sender: Callable):
        """translatedRedistranslated - translatedetc.translated"""
        async with self.lock:
            # checkIstranslatedthis translated
            if sender in self.router.get(channel, set()):
                logger.debug(f"translated {channel}，skip")
                return
            
            need_sub = channel not in self.channels_ref
            self.channels_ref[channel] = self.channels_ref.get(channel, 0) + 1
            self.router.setdefault(channel, set()).add(sender)
            
            if need_sub:
                await self.pubsub.subscribe(channel)
                logger.info(f"[Redis] SUB {channel}; total={len(self.channels_ref)}")
            else:
                logger.debug(f"[Redis] translated {channel} translated，addedtranslated")
    
    async def _unsubscribe_channel(self, channel: str, sender: Callable):
        """canceltranslatedRedistranslated"""
        async with self.lock:
            if channel in self.router:
                self.router[channel].discard(sender)
            
            if channel in self.channels_ref:
                self.channels_ref[channel] -= 1
                if self.channels_ref[channel] <= 0:
                    del self.channels_ref[channel]
                    self.router.pop(channel, None)
                    await self.pubsub.unsubscribe(channel)
                    logger.info(f"[Redis] UNSUB {channel}; total={len(self.channels_ref)}")
    
    async def _listen_loop(self):
        """translatedRedistranslated'stranslated - translatedAndtranslated"""
        backoff = 0.05
        
        while self.is_running:
            try:
                # checkIstranslated'stranslated
                async with self.lock:
                    has_channels = bool(self.channels_ref)
                
                if not has_channels:
                    await asyncio.sleep(0.2)
                    continue
                
                # fetchtranslated - useredis-py 5.x'stranslated
                msg = await self.pubsub.get_message(timeout=0.1)
                
                if not msg or msg["type"] != "message":
                    await asyncio.sleep(0.05)  # translatedetc.translated，translatedCPUtranslatedusetranslated
                    continue
                
                channel = msg["channel"]
                data = msg["data"]
                
                # translated
                try:
                    message_data = json.loads(data)
                except json.JSONDecodeError as e:
                    logger.error(f"translatedfailed: {e}, translated: {data}")
                    continue
                
                # checkIstranslatedprogresstranslated
                if not progress_adapter.is_progress_message(message_data):
                    logger.debug(f"skiptranslatedprogresstranslated: {message_data.get('type', 'unknown')}")
                    continue
                
                # translated
                current_time = datetime.utcnow().timestamp()
                current_progress = message_data.get("progress", 0)
                
                if channel in self.last_progress:
                    last_data = self.last_progress[channel]
                    if progress_adapter.should_throttle(
                        last_data["progress"], current_progress,
                        last_data["timestamp"], current_time,
                        self.throttle_interval
                    ):
                        logger.debug(f"translated: {channel} - {current_progress}%")
                        continue
                
                # updatetranslated
                self.last_progress[channel] = {
                    "progress": current_progress,
                    "timestamp": current_time
                }
                
                # translated
                simple_msg = progress_adapter.to_simple(message_data)
                
                # fetchtranslateduser - fromtranslated
                async with self.lock:
                    subscribed_users = set()
                    for user_id, user_channels in self.user_subscriptions.items():
                        if channel in user_channels:
                            subscribed_users.add(user_id)
                
                # translateduser
                if subscribed_users:
                    logger.debug(f"translated {len(subscribed_users)}  user: {channel} - {simple_msg}")
                    
                    # translated
                    send_tasks = []
                    for user_id in subscribed_users:
                        send_tasks.append(
                            manager.send_personal_message(simple_msg, user_id)
                        )
                    
                    if send_tasks:
                        await asyncio.gather(*send_tasks, return_exceptions=True)
                else:
                    logger.debug(f"translated {channel} translateduser")
                
                backoff = 0.05  # translated
                
            except Exception as e:
                logger.error(f"processRedistranslatedfailed: {e}")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 1.0)  # translated，translated1seconds
    
    async def get_subscription_status(self, user_id: str) -> Dict[str, Any]:
        """fetchusertranslatedstatus"""
        async with self.lock:
            return {
                "user_id": user_id,
                "subscribed_tasks": [],  # translated
                "total_subscriptions": 0,
                "active_channels": len(self.channels_ref)
            }

# translated
websocket_gateway_service = WebSocketGatewayService()
