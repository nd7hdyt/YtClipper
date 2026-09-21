"""
WebSocket APItranslated
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
    """WebSocketconnecttranslated"""
    await manager.connect(websocket, user_id)
    
    try:
        # translatedconnectConfirmtranslated
        welcome_message = WebSocketMessage.create_system_notification(
            "connection",
            "connectsucceeded",
            f"user {user_id} translatedsucceededconnecttranslatedWebSocketservice",
            "success"
        )
        await manager.send_personal_message(welcome_message, user_id)
        
        # processtranslated - translated
        while True:
            try:
                # translated
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # processtranslated'stranslated
                await handle_client_message(user_id, message)
                
            except WebSocketDisconnect:
                logger.info(f"user {user_id} translatedconnect")
                break
            except json.JSONDecodeError:
                logger.error(f"user {user_id} translated'stranslatedformaterror")
                try:
                    error_message = WebSocketMessage.create_error_notification(
                        "message_format_error",
                        "translatedformaterror",
                        {"message": "translated'sJSONformattranslated"}
                    )
                    await manager.send_personal_message(error_message, user_id)
                except:
                    # iftranslatedfailed，translatedconnecttranslated，translated
                    break
            except Exception as e:
                logger.error(f"processuser {user_id} translated: {e}")
                try:
                    error_message = WebSocketMessage.create_error_notification(
                        "processing_error",
                        "translatedprocesserror",
                        {"error": str(e)}
                    )
                    await manager.send_personal_message(error_message, user_id)
                except:
                    # iftranslatedfailed，translatedconnecttranslated，translated
                    break
    
    except WebSocketDisconnect:
        logger.info(f"user {user_id} translatedconnect")
    except Exception as e:
        logger.error(f"WebSocketconnecttranslated: {e}")
    finally:
        # bytranslatedclean：translatedcanceltranslated，translatedconnect
        try:
            await websocket_gateway_service.unsubscribe_user_from_all_tasks(user_id)
        except Exception as e:
            logger.error(f"cleanusertranslatedfailed: {e}")
        
        try:
            await manager.disconnect(user_id)
        except Exception as e:
            logger.error(f"translateduserconnectfailed: {e}")

async def handle_client_message(user_id: str, message: Dict[str, Any]):
    """processtranslated"""
    message_type = message.get("type")
    
    if message_type == "sync_subscriptions":
        # translated'stranslatedetc.translated
        project_ids = message.get("project_ids", [])
        # translatedprojectID，translatedservicetranslated
        channels = set(project_ids)
        
        stats = await websocket_gateway_service.sync_user_subscriptions(user_id, channels)
        
        response = WebSocketMessage.create_system_notification(
            "subscription_sync",
            "translated",
            f"added {stats['added']} / translated {stats['removed']} / translated {stats['unchanged']}",
            "success"
        )
        await manager.send_personal_message(response, user_id)
        
    elif message_type == "subscribe":
        # translated（translatedversion）
        topic = message.get("topic")
        if topic:
            manager.subscribe_to_topic(user_id, topic)
            response = WebSocketMessage.create_system_notification(
                "subscription",
                "translatedsucceeded",
                f"translatedsucceededtranslated: {topic}",
                "success"
            )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "subscribe_task":
        # translatedtaskprogress（translatedversion）
        task_id = message.get("task_id")
        if task_id:
            success = await websocket_gateway_service.subscribe_user_to_task(user_id, task_id)
            if success:
                response = WebSocketMessage.create_system_notification(
                    "task_subscription",
                    "tasktranslatedsucceeded",
                    f"translatedsucceededtranslatedtask {task_id} 'sprogressupdate",
                    "success"
                )
            else:
                response = WebSocketMessage.create_error_notification(
                    "task_subscription_failed",
                    "tasktranslatedfailed",
                    {"task_id": task_id}
                )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "unsubscribe":
        # canceltranslated（translatedversion）
        topic = message.get("topic")
        if topic:
            manager.unsubscribe_from_topic(user_id, topic)
            response = WebSocketMessage.create_system_notification(
                "unsubscription",
                "canceltranslatedsucceeded",
                f"translatedcanceltranslated: {topic}",
                "info"
            )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "unsubscribe_task":
        # canceltranslatedtaskprogress（translatedversion）
        task_id = message.get("task_id")
        if task_id:
            success = await websocket_gateway_service.unsubscribe_user_from_task(user_id, task_id)
            if success:
                response = WebSocketMessage.create_system_notification(
                    "task_unsubscription",
                    "taskcanceltranslatedsucceeded",
                    f"translatedcanceltranslatedtask {task_id} 'sprogressupdate",
                    "info"
                )
            else:
                response = WebSocketMessage.create_error_notification(
                    "task_unsubscription_failed",
                    "taskcanceltranslatedfailed",
                    {"task_id": task_id}
                )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "subscribe_many":
        # translatedtask
        task_ids = message.get("channels", [])
        if task_ids:
            results = await websocket_gateway_service.subscribe_user_to_many_tasks(user_id, task_ids)
            response = WebSocketMessage.create_system_notification(
                "batch_subscription",
                "translated",
                f"addedtranslated: {len(results['added'])}, translatedin: {len(results['already_subscribed'])}",
                "success"
            )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "unsubscribe_many":
        # translatedcanceltranslatedtask
        task_ids = message.get("channels", [])
        if task_ids:
            results = await websocket_gateway_service.unsubscribe_user_from_many_tasks(user_id, task_ids)
            response = WebSocketMessage.create_system_notification(
                "batch_unsubscription",
                "translatedcanceltranslated",
                f"translated: {len(results['removed'])}, translated: {len(results['not_subscribed'])}",
                "success"
            )
            await manager.send_personal_message(response, user_id)
    
    elif message_type == "sync_subscriptions":
        # translated
        task_ids = message.get("channels", [])
        results = await websocket_gateway_service.sync_user_subscriptions(user_id, task_ids)
        response = WebSocketMessage.create_system_notification(
            "subscription_sync",
            "translated",
            f"added: {len(results['added'])}, translated: {len(results['removed'])}, translated: {len(results['unchanged'])}",
            "success"
        )
        await manager.send_personal_message(response, user_id)
    
    elif message_type == "ping":
        # translated
        response = {
            "type": "pong",
            "timestamp": WebSocketMessage.create_system_notification(
                "ping", "", "", "info"
            )["timestamp"]
        }
        await manager.send_personal_message(response, user_id)
        logger.debug(f"user {user_id} translated - translatedpong")
    
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
        # translated
        error_message = WebSocketMessage.create_error_notification(
            "unknown_message_type",
            "translated",
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
    """translatedconnect'suser"""
    try:
        await manager.broadcast(message)
        return {"status": "success", "message": "translatedsucceeded"}
    except Exception as e:
        logger.error(f"translatedfailed: {e}")
        raise HTTPException(status_code=500, detail=f"translatedfailed: {e}")

@router.post("/ws/broadcast/{topic}")
async def broadcast_to_topic(topic: str, message: Dict[str, Any]):
    """translated'stranslated"""
    try:
        await manager.broadcast_to_topic(message, topic)
        return {"status": "success", "message": f"translated {topic} 'stranslated"}
    except Exception as e:
        logger.error(f"translated {topic} failed: {e}")
        raise HTTPException(status_code=500, detail=f"translatedfailed: {e}")

@router.post("/ws/send/{user_id}")
async def send_to_user(user_id: str, message: Dict[str, Any]):
    """translateduser"""
    try:
        await manager.send_personal_message(message, user_id)
        return {"status": "success", "message": f"translateduser {user_id}"}
    except Exception as e:
        logger.error(f"translateduser {user_id} failed: {e}")
        raise HTTPException(status_code=500, detail=f"translatedfailed: {e}")