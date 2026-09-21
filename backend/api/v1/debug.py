"""
ENAPIAPI
EN
"""

import json
import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import redis.asyncio as redis
from ...core.config import get_redis_url

logger = logging.getLogger(__name__)
router = APIRouter()

class PublishMessage(BaseModel):
    """EN"""
    task_id: str
    progress: int
    step: int = 1
    total: int = 6
    phase: str = "test"
    message: str = "EN"
    status: str = "PROGRESS"
    seq: int = 1
    meta: Dict[str, Any] = {}

@router.post("/debug/publish")
async def debug_publish_message(message: PublishMessage):
    """ENAPI：ENprogressENRedis"""
    try:
        # connectRedis
        redis_client = redis.from_url(get_redis_url(), decode_responses=True)
        
        # EN
        import time
        full_message = {
            "task_id": message.task_id,
            "progress": message.progress,
            "step": message.step,
            "total": message.total,
            "phase": message.phase,
            "message": message.message,
            "status": message.status,
            "seq": message.seq,
            "ts": time.time(),
            "meta": message.meta
        }
        
        # ENRedis
        channel = f"progress:{message.task_id}"
        result = await redis_client.publish(channel, json.dumps(full_message))
        
        await redis_client.aclose()
        
        logger.info(f"EN: {channel} -> {result} EN")
        
        return {
            "success": True,
            "channel": channel,
            "subscribers": result,
            "message": full_message
        }
        
    except Exception as e:
        logger.error(f"ENfailed: {e}")
        raise HTTPException(status_code=500, detail=f"ENfailed: {str(e)}")

@router.get("/debug/subscriptions")
async def debug_get_subscriptions():
    """ENAPI：fetchcurrentENstatus"""
    try:
        from ...services.websocket_gateway_service import websocket_gateway_service
        
        async with websocket_gateway_service.lock:
            return {
                "success": True,
                "active_channels": len(websocket_gateway_service.channels_ref),
                "channels": dict(websocket_gateway_service.channels_ref),
                "user_subscriptions": dict(websocket_gateway_service.user_subscriptions)
            }
            
    except Exception as e:
        logger.error(f"fetchENstatusfailed: {e}")
        raise HTTPException(status_code=500, detail=f"fetchfailed: {str(e)}")

@router.get("/debug/redis-info")
async def debug_redis_info():
    """ENAPI：fetchRedisconnectEN"""
    try:
        redis_url = get_redis_url()
        redis_client = redis.from_url(redis_url, decode_responses=True)
        
        # ENconnect
        await redis_client.ping()
        
        # fetchEN
        info = await redis_client.info()
        
        await redis_client.aclose()
        
        return {
            "success": True,
            "redis_url": redis_url,
            "redis_version": info.get("redis_version"),
            "connected_clients": info.get("connected_clients"),
            "used_memory": info.get("used_memory_human")
        }
        
    except Exception as e:
        logger.error(f"fetchRedisENfailed: {e}")
        raise HTTPException(status_code=500, detail=f"fetchfailed: {str(e)}")

