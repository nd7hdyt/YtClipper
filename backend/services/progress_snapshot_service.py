"""
progressENservice
ENRedisEN
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import redis.asyncio as redis
from ..core.config import get_redis_url

logger = logging.getLogger(__name__)

class ProgressSnapshotService:
    """progressENservice"""
    
    def __init__(self):
        self.redis_url = get_redis_url()
        self.redis_client: Optional[redis.Redis] = None
        self._connected = False
    
    async def connect(self):
        """connectRedis"""
        if self._connected:
            return
        
        try:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            await self.redis_client.ping()
            self._connected = True
            logger.info("progressENserviceENconnectRedis")
        except Exception as e:
            logger.error(f"connectRedisfailed: {e}")
            self._connected = False
    
    async def disconnect(self):
        """disconnectRedisconnect"""
        if self.redis_client:
            await self.redis_client.aclose()
            self.redis_client = None
        self._connected = False
        logger.info("progressENserviceENdisconnectRedis")
    
    def _get_snapshot_key(self, channel: str) -> str:
        """fetchEN"""
        return f"progress:last:{channel}"
    
    async def save_snapshot(self, channel: str, payload: dict) -> bool:
        """
        saveprogressEN
        
        Args:
            channel: EN
            payload: EN
            
        Returns:
            ENsavesucceeded
        """
        if not self._connected:
            await self.connect()
        
        if not self.redis_client:
            return False
        
        try:
            snapshot_key = self._get_snapshot_key(channel)
            
            # ENtimeEN
            payload_with_ts = {
                **payload,
                "snapshot_timestamp": datetime.utcnow().isoformat()
            }
            
            # saveENRedis Hash
            await self.redis_client.hset(snapshot_key, mapping=payload_with_ts)
            
            # settingsENtime（24EN）
            await self.redis_client.expire(snapshot_key, 86400)
            
            logger.debug(f"ENsave: {channel} -> {snapshot_key}")
            return True
            
        except Exception as e:
            logger.error(f"saveENfailed: {e}")
            return False
    
    async def get_snapshot(self, channel: str) -> Optional[dict]:
        """
        fetchprogressEN
        
        Args:
            channel: EN
            
        Returns:
            ENNone
        """
        if not self._connected:
            await self.connect()
        
        if not self.redis_client:
            return None
        
        try:
            snapshot_key = self._get_snapshot_key(channel)
            snapshot_data = await self.redis_client.hgetall(snapshot_key)
            
            if snapshot_data:
                logger.debug(f"ENfetch: {channel} -> {snapshot_data}")
                return snapshot_data
            else:
                logger.debug(f"ENdoes not exist: {channel}")
                return None
                
        except Exception as e:
            logger.error(f"fetchENfailed: {e}")
            return None
    
    async def delete_snapshot(self, channel: str) -> bool:
        """
        deleteprogressEN
        
        Args:
            channel: EN
            
        Returns:
            ENdeletesucceeded
        """
        if not self._connected:
            await self.connect()
        
        if not self.redis_client:
            return False
        
        try:
            snapshot_key = self._get_snapshot_key(channel)
            result = await self.redis_client.delete(snapshot_key)
            
            if result:
                logger.debug(f"ENdeleted: {channel}")
            else:
                logger.debug(f"ENdoes not exist，ENdelete: {channel}")
            
            return bool(result)
            
        except Exception as e:
            logger.error(f"deleteENfailed: {e}")
            return False
    
    async def cleanup_expired_snapshots(self) -> int:
        """
        EN
        
        Returns:
            EN
        """
        if not self._connected:
            await self.connect()
        
        if not self.redis_client:
            return 0
        
        try:
            # ENallEN
            pattern = "progress:last:*"
            keys = await self.redis_client.keys(pattern)
            
            cleaned_count = 0
            for key in keys:
                # checkEN
                ttl = await self.redis_client.ttl(key)
                if ttl == -1:  # ENsettingsENtime
                    await self.redis_client.expire(key, 86400)  # settings24EN
                elif ttl == -2:  # ENdoes not exist
                    cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"EN {cleaned_count} EN")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"ENfailed: {e}")
            return 0

# ENserviceEN
snapshot_service = ProgressSnapshotService()
