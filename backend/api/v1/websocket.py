"""
WebSocket APIEN
"""

import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.websocket_manager import manager, WebSocketMessage
from ...services.websocket_notification_service import WebSocketNotificationService
from ...services.websocket_gateway_service import websocket_gateway_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocketconnectEN"""
    await manager.connect(websocket, user_id)
    
    try:
        # sendconnectEN
        welcome_message = WebSocketMessage.create_system_notification(
            "connection",
            "connectsucceeded",
            f"user {user_id} ENsucceededconnectENWebSocketservice",
            "success"
        )
        await manager.send_personal_message(welcome_message, user_id)
        
        # processingEN - EN
        while True:
            try:
                # receiveEN
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # processingEN
                await handle_client_message(user_id, message)
                
            except WebSocketDisconnect:
                logger.info(f"user {user_id} ENdisconnectconnect")
                break
            except json.JSONDecodeError:
                logger.error(f"user {user_id} sendENerror")
                try:
                    error_message = WebSocketMessage.create_error_notification(
                        "message_format_error",
                        "ENerror",
                        {"message": "pleasesendENJSONEN"}
                    )
                    await manager.send_personal_message(error_message, user_id)
                except:
                    # ifsendfailed，ENconnectENdisconnect，ENlogout
                    break
            except Exception as e:
                logger.error(f"processinguser {user_id} EN: {e}")
                try:
                    error_message = WebSocketMessage.create_error_notification(
                        "processing_error",
                        "ENprocessingerror",
                        {"error": str(e)}
                    )
                    await manager.send_personal_message(error_message, user_id)
                except:
                    # ifsendfailed，ENconnectENdisconnect，ENlogout
                    break
    
    except WebSocketDisconnect:
        logger.info(f"user {user_id} disconnectconnect")
    except Exception as e:
        logger.error(f"WebSocketconnectexception: {e}")
    finally:
        # EN：ENcancelEN，ENdisconnectconnect
        try:
            await websocket_gateway_service.unsubscribe_user_from_all_tasks(user_id)
        except Exception as e:
            logger.error(f"ENuserENfailed: {e}")
        
        try:
            await manager.disconnect(user_id)
        except Exception as e:
            logger.error(f"disconnectuserconnectfailed: {e}")

async def handle_client_message(user_id: str, message: Dict[str, Any]):
    """processingEN"""
    message_type = message.get("type")
    
    if message_type == "sync_subscriptions":
        # EN
        project_ids = message.get("project_ids", [])
        # ENprojectID，ENserviceEN
        channels = set(project_ids)
        
        stats = await websocket_gateway_service.sync_user_subscriptions(user_id, channels)
        
        response = WebSocketMessage.create_system_notification(
            "subscription_sync",
            "EN",
            f"EN {stats['added']} / EN {stats['removed']} / EN {stats['unchanged']}",
            "success"
        )
        await manager.send_personal_message(response, user_id)
        
    elif message_type == "subscribe":
        # EN（EN）
        topic = message.get("topic")
        if topic:
            manager.subscribe_to_topic(user_id, topic)
            response = WebSocketMessage.create_system_notification(
                "subscription",
                "ENsucceeded",
                f"ENsucceededEN: {topic}",
                "success"
            )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "subscribe_task":
        # ENtaskprogress（EN）
        task_id = message.get("task_id")
        if task_id:
            success = await websocket_gateway_service.subscribe_user_to_task(user_id, task_id)
            if success:
                response = WebSocketMessage.create_system_notification(
                    "task_subscription",
                    "taskENsucceeded",
                    f"ENsucceededENtask {task_id} ENprogressupdate",
                    "success"
                )
            else:
                response = WebSocketMessage.create_error_notification(
                    "task_subscription_failed",
                    "taskENfailed",
                    {"task_id": task_id}
                )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "unsubscribe":
        # cancelEN（EN）
        topic = message.get("topic")
        if topic:
            manager.unsubscribe_from_topic(user_id, topic)
            response = WebSocketMessage.create_system_notification(
                "unsubscription",
                "cancelENsucceeded",
                f"ENcancelEN: {topic}",
                "info"
            )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "unsubscribe_task":
        # cancelENtaskprogress（EN）
        task_id = message.get("task_id")
        if task_id:
            success = await websocket_gateway_service.unsubscribe_user_from_task(user_id, task_id)
            if success:
                response = WebSocketMessage.create_system_notification(
                    "task_unsubscription",
                    "taskcancelENsucceeded",
                    f"ENcancelENtask {task_id} ENprogressupdate",
                    "info"
                )
            else:
                response = WebSocketMessage.create_error_notification(
                    "task_unsubscription_failed",
                    "taskcancelENfailed",
                    {"task_id": task_id}
                )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "subscribe_many":
        # ENtask
        task_ids = message.get("channels", [])
        if task_ids:
            results = await websocket_gateway_service.subscribe_user_to_many_tasks(user_id, task_ids)
            response = WebSocketMessage.create_system_notification(
                "batch_subscription",
                "EN",
                f"EN: {len(results['added'])}, already exists: {len(results['already_subscribed'])}",
                "success"
            )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "unsubscribe_many":
        # ENcancelENtask
        task_ids = message.get("channels", [])
        if task_ids:
            results = await websocket_gateway_service.unsubscribe_user_from_many_tasks(user_id, task_ids)
            response = WebSocketMessage.create_system_notification(
                "batch_unsubscription",
                "ENcancelEN",
                f"EN: {len(results['removed'])}, EN: {len(results['not_subscribed'])}",
                "success"
            )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "sync_subscriptions":
        # EN
        task_ids = message.get("channels", [])
        results = await websocket_gateway_service.sync_user_subscriptions(user_id, task_ids)
        response = WebSocketMessage.create_system_notification(
            "subscription_sync",
            "EN",
            f"EN: {len(results['added'])}, EN: {len(results['removed'])}, EN: {len(results['unchanged'])}",
            "success"
        )
        await manager.send_personal_message(response, user_id)
    
    elif message_type == "ping":
        # EN
        response = {
            "type": "pong",
            "timestamp": WebSocketMessage.create_system_notification(
                "ping", "", "", "info"
            )["timestamp"]
        }
        await manager.send_personal_message(response, user_id)
        logger.debug(f"user {user_id} EN - ENpong")
    
    elif message_type == "get_status":
        # fetchconnectstatus
        gateway_status = await websocket_gateway_service.get_subscription_status(user_id)
        status = {
            "type": "status",
            "user_id": user_id,
            "connected": user_id in manager.active_connections,
            "subscriptions": list(manager.user_subscriptions.get(user_id, set())),
            "task_subscriptions": gateway_status["subscribed_tasks"],
            "total_connections": manager.get_connection_count(),
            "timestamp": WebSocketMessage.create_system_notification(
                "status", "", "", "info"
            )["timestamp"]
        }
        await manager.send_personal_message(status, user_id)
    
    else:
        # EN
        error_message = WebSocketMessage.create_error_notification(
            "unknown_message_type",
            "EN",
            {"message_type": message_type, "supported_types": ["subscribe", "subscribe_task", "unsubscribe", "unsubscribe_task", "ping", "get_status"]}
        )
        await manager.send_personal_message(error_message, user_id)

@router.get("/ws/status")
async def get_websocket_status():
    """fetchWebSocketservicestatus"""
    return {
        "status": "running",
        "total_connections": manager.get_connection_count(),
        "topics": {
            topic: manager.get_topic_subscriber_count(topic)
            for topic in manager.topic_subscribers
        }
    }

@router.post("/ws/broadcast")
async def broadcast_message(message: Dict[str, Any]):
    """ENallconnectENuser"""
    try:
        await manager.broadcast(message)
        return {"status": "success", "message": "ENsucceeded"}
    except Exception as e:
        logger.error(f"ENfailed: {e}")
        raise HTTPException(status_code=500, detail=f"ENfailed: {e}")

@router.post("/ws/broadcast/{topic}")
async def broadcast_to_topic(topic: str, message: Dict[str, Any]):
    """EN"""
    try:
        await manager.broadcast_to_topic(message, topic)
        return {"status": "success", "message": f"EN {topic} EN"}
    except Exception as e:
        logger.error(f"EN {topic} failed: {e}")
        raise HTTPException(status_code=500, detail=f"ENfailed: {e}")

@router.post("/ws/send/{user_id}")
async def send_to_user(user_id: str, message: Dict[str, Any]):
    """sendENuser"""
    try:
        await manager.send_personal_message(message, user_id)
        return {"status": "success", "message": f"ENsendENuser {user_id}"}
    except Exception as e:
        logger.error(f"sendENuser {user_id} failed: {e}")
        raise HTTPException(status_code=500, detail=f"sendENfailed: {e}")