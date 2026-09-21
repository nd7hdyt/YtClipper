"""
ENAPI
ENstatusEN、ENcacheEN
"""
import os
import time
import asyncio
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from backend.core.desktop_config import is_desktop_mode

router = APIRouter()

# checkEN
def check_desktop_mode():
    if not is_desktop_mode():
        raise HTTPException(status_code=400, detail="EN")

class NetworkStatus(BaseModel):
    """ENstatusEN"""
    is_online: bool
    connection_quality: str  # excellent, good, poor, offline
    latency: Optional[float] = None
    last_check: str
    error_message: Optional[str] = None

class OfflineModeStatus(BaseModel):
    """ENstatusEN"""
    is_offline_mode: bool
    auto_offline_threshold: int  # ENfailedEN
    consecutive_failures: int
    last_successful_request: Optional[str] = None
    offline_since: Optional[str] = None

class CacheItem(BaseModel):
    """cacheEN"""
    key: str
    data: Any
    created_at: str
    expires_at: Optional[str] = None
    size: int

class SyncQueueItem(BaseModel):
    """ENqueueEN"""
    id: str
    action: str  # create, update, delete
    resource_type: str  # project, clip, collection
    resource_id: str
    data: Dict[str, Any]
    created_at: str
    retry_count: int = 0
    max_retries: int = 3

# ENstatusEN（ENuseEN）
_network_status = NetworkStatus(
    is_online=True,
    connection_quality="good",
    last_check=datetime.now().isoformat()
)

_offline_mode_status = OfflineModeStatus(
    is_offline_mode=False,
    auto_offline_threshold=3,
    consecutive_failures=0
)

_cache: Dict[str, CacheItem] = {}
_sync_queue: List[SyncQueueItem] = []

@router.get("/network/status", response_model=NetworkStatus)
async def get_network_status():
    """fetchENstatus"""
    check_desktop_mode()
    
    try:
        # ENconnect
        start_time = time.time()
        response = requests.get("https://www.google.com", timeout=5)
        latency = (time.time() - start_time) * 1000  # EN
        
        if response.status_code == 200:
            # ENconnectEN
            if latency < 100:
                quality = "excellent"
            elif latency < 500:
                quality = "good"
            else:
                quality = "poor"
            
            _network_status.is_online = True
            _network_status.connection_quality = quality
            _network_status.latency = latency
            _network_status.last_check = datetime.now().isoformat()
            _network_status.error_message = None
            
            # ENfailedEN
            _offline_mode_status.consecutive_failures = 0
            _offline_mode_status.last_successful_request = datetime.now().isoformat()
            
        else:
            raise requests.RequestException(f"HTTP {response.status_code}")
            
    except Exception as e:
        # ENconnectfailed
        _network_status.is_online = False
        _network_status.connection_quality = "offline"
        _network_status.latency = None
        _network_status.last_check = datetime.now().isoformat()
        _network_status.error_message = str(e)
        
        # ENfailedEN
        _offline_mode_status.consecutive_failures += 1
        
        # checkENshouldEN
        if (_offline_mode_status.consecutive_failures >= _offline_mode_status.auto_offline_threshold 
            and not _offline_mode_status.is_offline_mode):
            _offline_mode_status.is_offline_mode = True
            _offline_mode_status.offline_since = datetime.now().isoformat()
    
    return _network_status

@router.get("/offline/status", response_model=OfflineModeStatus)
async def get_offline_mode_status():
    """fetchENstatus"""
    check_desktop_mode()
    return _offline_mode_status

@router.post("/offline/toggle")
async def toggle_offline_mode():
    """EN"""
    check_desktop_mode()
    
    _offline_mode_status.is_offline_mode = not _offline_mode_status.is_offline_mode
    
    if _offline_mode_status.is_offline_mode:
        _offline_mode_status.offline_since = datetime.now().isoformat()
    else:
        _offline_mode_status.offline_since = None
        _offline_mode_status.consecutive_failures = 0
    
    return {
        "is_offline_mode": _offline_mode_status.is_offline_mode,
        "message": "EN" if _offline_mode_status.is_offline_mode else "EN"
    }

@router.post("/offline/auto-threshold")
async def set_auto_offline_threshold(threshold: int):
    """settingsEN"""
    check_desktop_mode()
    
    if threshold < 1 or threshold > 10:
        raise HTTPException(status_code=400, detail="ENmustEN1-10EN")
    
    _offline_mode_status.auto_offline_threshold = threshold
    
    return {
        "auto_offline_threshold": threshold,
        "message": f"ENsettingsEN {threshold}"
    }

@router.get("/cache", response_model=List[CacheItem])
async def get_cache_items():
    """fetchcacheEN"""
    check_desktop_mode()
    
    # ENcache
    current_time = datetime.now()
    expired_keys = []
    
    for key, item in _cache.items():
        if item.expires_at:
            expires_at = datetime.fromisoformat(item.expires_at)
            if current_time > expires_at:
                expired_keys.append(key)
    
    for key in expired_keys:
        del _cache[key]
    
    return list(_cache.values())

@router.post("/cache")
async def add_cache_item(key: str, data: Any, expires_in_seconds: Optional[int] = None):
    """ENcacheEN"""
    check_desktop_mode()
    
    created_at = datetime.now().isoformat()
    expires_at = None
    
    if expires_in_seconds:
        expires_at = (datetime.now() + timedelta(seconds=expires_in_seconds)).isoformat()
    
    # EN（EN）
    size = len(str(data))
    
    _cache[key] = CacheItem(
        key=key,
        data=data,
        created_at=created_at,
        expires_at=expires_at,
        size=size
    )
    
    return {
        "key": key,
        "message": "cacheEN",
        "expires_at": expires_at
    }

@router.delete("/cache/{key}")
async def remove_cache_item(key: str):
    """deletecacheEN"""
    check_desktop_mode()
    
    if key in _cache:
        del _cache[key]
        return {"message": f"cacheEN {key} deleted"}
    else:
        raise HTTPException(status_code=404, detail="cacheENdoes not exist")

@router.get("/sync-queue", response_model=List[SyncQueueItem])
async def get_sync_queue():
    """fetchENqueue"""
    check_desktop_mode()
    return _sync_queue

@router.post("/sync-queue")
async def add_sync_queue_item(
    action: str,
    resource_type: str,
    resource_id: str,
    data: Dict[str, Any]
):
    """ENqueueEN"""
    check_desktop_mode()
    
    if action not in ["create", "update", "delete"]:
        raise HTTPException(status_code=400, detail="EN")
    
    if resource_type not in ["project", "clip", "collection"]:
        raise HTTPException(status_code=400, detail="EN")
    
    item = SyncQueueItem(
        id=f"{resource_type}_{resource_id}_{int(time.time())}",
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        data=data,
        created_at=datetime.now().isoformat()
    )
    
    _sync_queue.append(item)
    
    return {
        "id": item.id,
        "message": "ENqueueEN"
    }

@router.post("/sync-queue/process")
async def process_sync_queue():
    """processingENqueue"""
    check_desktop_mode()
    
    if _offline_mode_status.is_offline_mode:
        return {
            "message": "currentEN，cannotprocessingENqueue",
            "queue_size": len(_sync_queue)
        }
    
    processed = 0
    failed = 0
    
    for item in _sync_queue[:]:  # useclipEN
        try:
            # ENshouldcallENAPIEN
            # EN，weENprocessingEN
            await simulate_sync_operation(item)
            
            _sync_queue.remove(item)
            processed += 1
            
        except Exception as e:
            item.retry_count += 1
            if item.retry_count >= item.max_retries:
                _sync_queue.remove(item)
                failed += 1
            else:
                # ENqueueENretry
                pass
    
    return {
        "processed": processed,
        "failed": failed,
        "remaining": len(_sync_queue),
        "message": f"processingEN：succeeded {processed} EN，failed {failed} EN"
    }

async def simulate_sync_operation(item: SyncQueueItem):
    """EN"""
    # EN，ENshouldcallENAPIEN
    # for example：createproject、updateEN、deletecollectionEN
    await asyncio.sleep(0.1)  # EN
    
    # ENfailed
    import random
    if random.random() < 0.1:  # 10% ENfailedEN
        raise Exception("ENerror")

@router.delete("/sync-queue/clear")
async def clear_sync_queue():
    """ENqueue"""
    check_desktop_mode()
    
    count = len(_sync_queue)
    _sync_queue.clear()
    
    return {
        "message": f"ENqueueEN，deleteEN {count} ENproject"
    }

@router.get("/offline/summary")
async def get_offline_summary():
    """fetchEN"""
    check_desktop_mode()
    
    return {
        "network_status": _network_status,
        "offline_mode_status": _offline_mode_status,
        "cache_stats": {
            "total_items": len(_cache),
            "total_size": sum(item.size for item in _cache.values()),
            "expired_items": len([
                item for item in _cache.values() 
                if item.expires_at and datetime.fromisoformat(item.expires_at) < datetime.now()
            ])
        },
        "sync_queue_stats": {
            "total_items": len(_sync_queue),
            "pending_items": len([item for item in _sync_queue if item.retry_count < item.max_retries]),
            "failed_items": len([item for item in _sync_queue if item.retry_count >= item.max_retries])
        }
    }
