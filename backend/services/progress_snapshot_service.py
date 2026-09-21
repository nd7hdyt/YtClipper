"""
progresstranslatedservice
translatedRedistranslatedAndtranslated
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import redis.asyncio as redis
from ..core.config import get_redis_url

logger = logging.getLogger(__name__)

class ProgressSnapshotService:
    """progresstranslatedservice"""
    
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
            logger.info("progresstranslatedservicetranslatedconnectRedis")
        except Exception as e:
            logger.error(f"connectRedisfailed: {e}")
            self._connected = False
    
    async def disconnect(self):
        """translatedRedisconnect"""
        if self.redis_client:
            await self.redis_client.aclose()
            self.redis_client = None
        self._connected = False
        logger.info("progresstranslatedservicetranslatedRedis")
    
    def _get_snapshot_key(self, channel: str) -> str:
        """fetchtranslated"""
        return f"progress:last:{channel}"
    
    async def save_snapshot(self, channel: str, payload: dict) -> bool:
        """
        translatedprogresstranslated
        
        Args:
            channel: translated
            payload: translated
            
        Returns:
            Istranslatedsucceeded
        """
        if not self._connected:
            await self.connect()
        
        if not self.redis_client:
            return False
        
        try:
            snapshot_key = self._get_snapshot_key(channel)
            
            # addtranslated
            payload_with_ts = {
                **payload,
                "snapshot_timestamp": datetime.utcnow().isoformat()
            }
            
            # translatedRedis Hash
            await self.redis_client.hset(snapshot_key, mapping=payload_with_ts)
            
            # settingstranslated（24translated）
            await self.redis_client.expire(snapshot_key, 86400)
            
            logger.debug(f"translated: {channel} -> {snapshot_key}")
            return True
            
        except Exception as e:
            logger.error(f"translatedfailed: {e}")
            return False
    
    async def get_snapshot(self, channel: str) -> Optional[dict]:
        """
        fetchprogresstranslated
        
        Args:
            channel: translated
            
        Returns:
            translatedorNone
        """
        if not self._connected:
            await self.connect()
        
        if not self.redis_client:
            return None
        
        try:
            snapshot_key = self._get_snapshot_key(channel)
            snapshot_data = await self.redis_client.hgetall(snapshot_key)
            
            if snapshot_data:
                logger.debug(f"translatedfetch: {channel} -> {snapshot_data}")
                return snapshot_data
            else:
                logger.debug(f"translatednot found: {channel}")
                return None
                
        except Exception as e:
            logger.error(f"fetchtranslatedfailed: {e}")
            return None
    
    async def delete_snapshot(self, channel: str) -> bool:
        """
        deleteprogresstranslated
        
        Args:
            channel: translated
            
        Returns:
            Istranslateddeletesucceeded
        """
        if not self._connected:
            await self.connect()
        
        if not self.redis_client:
            return False
        
        try:
            snapshot_key = self._get_snapshot_key(channel)
            result = await self.redis_client.delete(snapshot_key)
            
            if result:
                logger.debug(f"translateddelete: {channel}")
            else:
                logger.debug(f"translatednot found，translateddelete: {channel}")
            
            return bool(result)
            
        except Exception as e:
            logger.error(f"deletetranslatedfailed: {e}")
            return False
    
    async def cleanup_expired_snapshots(self) -> int:
        """
        cleantranslated'stranslated
        
        Returns:
            clean'stranslated
        """
        if not self._connected:
            await self.connect()
        
        if not self.redis_client:
            return 0
        
        try:
            # translated
            pattern = "progress:last:*"
            keys = await self.redis_client.keys(pattern)
            
            cleaned_count = 0
            for key in keys:
                # checkIstranslated
                ttl = await self.redis_client.ttl(key)
                if ttl == -1:  # translatedsettingstranslated
                    await self.redis_client.expire(key, 86400)  # settings24translated
                elif ttl == -2:  # translatednot found
                    cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"cleantranslated {cleaned_count}  translated")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"cleantranslatedfailed: {e}")
            return 0

# translatedservicetranslated
snapshot_service = ProgressSnapshotService()
