"""
Submission-related API routes - refactored version.
Removes the bilitool dependency in favor of direct API calls.
"""

import logging
import json
import os
import uuid
import time
import base64
import io
import aiohttp
import asyncio
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Body
from fastapi.responses import Response
from sqlalchemy.orm import Session
import qrcode

from ...core.database import get_db
from ...schemas.bilibili import (
    BilibiliAccountCreate, 
    BilibiliAccountResponse,
    UploadRequest,
    UploadRecordResponse,
    UploadStatusResponse,
    QRLoginRequest,
    QRLoginResponse
)
from ...services.bilibili_service import BilibiliAccountService, BilibiliUploadService
from ...tasks.upload import upload_clip_task

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/upload", tags=["submission-management"])

# Dict holding QR login sessions
qr_sessions = {}

# Service instances
def get_account_service(db: Session = Depends(get_db)) -> BilibiliAccountService:
    return BilibiliAccountService(db)

def get_upload_service(db: Session = Depends(get_db)) -> BilibiliUploadService:
    return BilibiliUploadService(db)


# Account management APIs
@router.get("/login-methods")
async def get_login_methods():
    """Get supported login methods"""
    return {
        "methods": [
            {
                "id": "cookie",
                "name": "Cookie import",
                "description": "Safest option; does not trigger risk controls",
                "icon": "🔐",
                "recommended": True,
                "risk_level": "low"
            },
            {
                "id": "password",
                "name": "Username/password login",
                "description": "Traditional login; may require a captcha",
                "icon": "👤",
                "recommended": True,
                "risk_level": "medium"
            },
            {
                "id": "qr",
                "name": "QR code login",
                "description": "Scan with the Bilibili app",
                "icon": "📱",
                "recommended": False,
                "risk_level": "high"
            },
            {
                "id": "wechat",
                "name": "WeChat login",
                "description": "Log in with a WeChat account",
                "icon": "💬",
                "recommended": False,
                "risk_level": "medium"
            },
            {
                "id": "qq",
                "name": "QQ login",
                "description": "Log in with a QQ account",
                "icon": "🐧",
                "recommended": False,
                "risk_level": "medium"
            }
        ]
    }


@router.post("/cookie-login", response_model=BilibiliAccountResponse)
async def cookie_login(
    request: dict = Body(...),
    account_service: BilibiliAccountService = Depends(get_account_service)
):
    """Cookie import login"""
    try:
        cookies = request.get("cookies")
        nickname = request.get("nickname")

        if not cookies:
            raise HTTPException(status_code=400, detail="Cookie must not be empty")

        # Validate the cookies
        cookie_validation = await validate_bilibili_cookies(cookies)

        if cookie_validation.get("valid"):
            # Build the cookie string for storage
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])

            account_data = BilibiliAccountCreate(
                username=cookie_validation.get("username", "cookie_user"),
                password="",
                nickname=nickname or cookie_validation.get("nickname", "Bilibili user"),
                cookie_content=cookie_str
            )

            account = await account_service.create_account(account_data)
            return BilibiliAccountResponse.from_orm(account)
        else:
            raise HTTPException(status_code=400, detail="Cookie is invalid or expired")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Cookie login failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")


@router.post("/password-login", response_model=BilibiliAccountResponse)
async def password_login(
    request: dict = Body(...),
    account_service: BilibiliAccountService = Depends(get_account_service)
):
    """Username/password login"""
    try:
        username = request.get("username")
        password = request.get("password")
        nickname = request.get("nickname")

        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password must not be empty")

        # Real password login should be implemented here
        # Currently returns mock data
        mock_cookie_data = {
            "code": 0,
            "message": "Login succeeded",
            "data": {
                "user_info": {
                    "username": username,
                    "nickname": nickname or username,
                    "mid": "12345678"
                },
                "cookie_info": {
                    "cookies": [{"name": "SESSDATA", "value": "mock_sessdata"}]
                }
            }
        }
        
        account_data = BilibiliAccountCreate(
            username=username,
            password=password,
            nickname=nickname or username,
            cookie_content=json.dumps(mock_cookie_data)
        )
        
        account = await account_service.create_account(account_data)
        return BilibiliAccountResponse.from_orm(account)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password login failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")


@router.post("/qr-login")
async def start_qr_login(
    request: dict = Body(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Start QR code login"""
    try:
        nickname = request.get("nickname")

        # Generate a session ID
        session_id = str(uuid.uuid4())

        # Create the session
        qr_sessions[session_id] = {
            "session_id": session_id,
            "status": "pending",
            "nickname": nickname,
            "created_at": time.time(),
            "qr_code": None,
            "error_message": None
        }

        # Generate the QR code in the background
        background_tasks.add_task(generate_qr_code_async, session_id)

        return {
            "session_id": session_id,
            "status": "pending",
            "message": "Generating QR code..."
        }

    except Exception as e:
        logger.error(f"Failed to start QR login: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start login")


@router.get("/qr-login/{session_id}")
async def check_qr_login_status(session_id: str):
    """Check QR login status"""
    try:
        if session_id not in qr_sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        session = qr_sessions[session_id]

        return {
            "session_id": session_id,
            "status": session["status"],
            "message": session.get("error_message", "Waiting for scan..."),
            "qr_code": session.get("qr_code")
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to check QR login status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to check login status")


@router.post("/qr-login/{session_id}/complete", response_model=BilibiliAccountResponse)
async def complete_qr_login(
    session_id: str,
    request: dict = Body(...),
    account_service: BilibiliAccountService = Depends(get_account_service)
):
    """Complete QR code login"""
    try:
        if session_id not in qr_sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        session = qr_sessions[session_id]

        if session["status"] != "success":
            raise HTTPException(status_code=400, detail="Login has not succeeded")

        nickname = request.get("nickname") or session.get("nickname")

        # Create mock cookie data
        mock_cookie_data = {
            "code": 0,
            "message": "Login succeeded",
            "data": {
                "user_info": {
                    "username": f"qr_user_{session_id[:8]}",
                    "nickname": nickname or "Bilibili user",
                    "mid": "87654321"
                },
                "cookie_info": {
                    "cookies": [{"name": "SESSDATA", "value": f"qr_sessdata_{session_id[:8]}"}]
                }
            }
        }

        account_data = BilibiliAccountCreate(
            username=f"qr_user_{session_id[:8]}",
            password="",
            nickname=nickname or "Bilibili user",
            cookie_content=json.dumps(mock_cookie_data)
        )

        account = await account_service.create_account(account_data)

        # Clean up the session
        del qr_sessions[session_id]

        return BilibiliAccountResponse.from_orm(account)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to complete QR login: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to complete login")


@router.get("/accounts")
async def get_accounts(account_service: BilibiliAccountService = Depends(get_account_service)):
    """Get all accounts"""
    try:
        accounts = account_service.get_accounts()
        return [BilibiliAccountResponse.from_orm(account) for account in accounts]
    except Exception as e:
        logger.error(f"Failed to get account list: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get account list")


@router.delete("/accounts/{account_id}")
async def delete_account(
    account_id: UUID,
    account_service: BilibiliAccountService = Depends(get_account_service)
):
    """Delete an account"""
    try:
        success = account_service.delete_account(account_id)
        if success:
            return {"message": "Account deleted"}
        else:
            raise HTTPException(status_code=404, detail="Account not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete account: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete account")


@router.post("/accounts/{account_id}/check")
async def check_account_status(
    account_id: UUID,
    account_service: BilibiliAccountService = Depends(get_account_service)
):
    """Check account status"""
    try:
        is_valid = account_service.check_account_status(account_id)
        return {
            "is_valid": is_valid,
            "message": "Account is healthy" if is_valid else "Account is unhealthy"
        }
    except Exception as e:
        logger.error(f"Failed to check account status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to check account status")


# Submission management APIs
@router.post("/projects/{project_id}/upload")
async def create_upload_task(
    project_id: UUID,
    upload_data: UploadRequest,
    upload_service: BilibiliUploadService = Depends(get_upload_service)
):
    """Create a submission task - temporarily disabled"""
    # Temporarily disabled; return an under-development notice
    raise HTTPException(status_code=503, detail="Bilibili upload is under development. Stay tuned!")

    # Original implementation disabled
    try:
        record = upload_service.create_upload_record(project_id, upload_data)

        # Start async upload tasks
        for clip_id in upload_data.clip_ids:
            upload_clip_task.delay(str(record.id), clip_id)

        return {
            "message": "Submission task created",
            "record_id": str(record.id),
            "clip_count": len(upload_data.clip_ids)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create submission task: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create submission task")


@router.post("/records/{record_id}/retry")
async def retry_upload_task(
    record_id: int,
    upload_service: BilibiliUploadService = Depends(get_upload_service)
):
    """Retry a submission task"""
    try:
        success = upload_service.retry_upload_task(record_id)
        if success:
            return {"message": "Submission retry started"}
        else:
            raise HTTPException(status_code=400, detail="Retry failed")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to retry submission task: {str(e)}")
        raise HTTPException(status_code=500, detail="Retry failed")


@router.post("/records/{record_id}/cancel")
async def cancel_upload_task(
    record_id: int,
    upload_service: BilibiliUploadService = Depends(get_upload_service)
):
    """Cancel a submission task"""
    try:
        success = upload_service.cancel_upload_task(record_id)
        if success:
            return {"message": "Submission task cancelled"}
        else:
            raise HTTPException(status_code=400, detail="Cancel failed")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to cancel submission task: {str(e)}")
        raise HTTPException(status_code=500, detail="Cancel failed")


@router.delete("/records/{record_id}")
async def delete_upload_task(
    record_id: int,
    upload_service: BilibiliUploadService = Depends(get_upload_service)
):
    """Delete a submission task"""
    try:
        success = upload_service.delete_upload_task(record_id)
        if success:
            return {"message": "Submission task deleted"}
        else:
            raise HTTPException(status_code=400, detail="Delete failed")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to delete submission task: {str(e)}")
        raise HTTPException(status_code=500, detail="Delete failed")


@router.get("/records")
async def get_upload_records(
    project_id: Optional[UUID] = None,
    upload_service: BilibiliUploadService = Depends(get_upload_service)
):
    """Get submission records"""
    try:
        records = upload_service.get_upload_records(project_id)
        return [UploadRecordResponse(**record) for record in records]
    except Exception as e:
        logger.error(f"Failed to get submission records: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get submission records")


@router.get("/records/{record_id}")
async def get_upload_record(
    record_id: UUID,
    upload_service: BilibiliUploadService = Depends(get_upload_service)
):
    """Get a single submission record"""
    try:
        record = upload_service.get_upload_record(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Submission record not found")
        return UploadRecordResponse.from_orm(record)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get submission record: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get submission record")


# Helpers
async def validate_bilibili_cookies(cookies: dict) -> dict:
    """Validate Bilibili cookies"""
    try:
        # Build the cookie string
        cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
        
        headers = {
            "Cookie": cookie_str,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.bilibili.com/"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.bilibili.com/x/web-interface/nav",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                data = await response.json()
                
                if data.get("code") == 0 and data.get("data", {}).get("isLogin"):
                    user_info = data["data"]

                    # Check required fields
                    required_fields = ['SESSDATA', 'bili_jct', 'DedeUserID']
                    missing_fields = []
                    for field in required_fields:
                        if field not in cookies:
                            missing_fields.append(field)

                    if missing_fields:
                        return {
                            "valid": False,
                            "message": f"Cookie is missing required fields: {', '.join(missing_fields)}"
                        }

                    return {
                        "valid": True,
                        "username": user_info.get("uname"),
                        "nickname": user_info.get("uname"),
                        "mid": user_info.get("mid"),
                        "level": user_info.get("level_info", {}).get("current_level", 0),
                        "can_upload": True  # True for now; finer checks can be added later
                    }
                else:
                    return {"valid": False, "message": "Cookie is invalid or expired"}

    except Exception as e:
        logger.error(f"Cookie validation failed: {e}")
        return {"valid": False, "message": f"Validation failed: {str(e)}"}


async def generate_qr_code_async(session_id: str):
    """Generate a QR code asynchronously"""
    try:
        if session_id not in qr_sessions:
            return

        session = qr_sessions[session_id]

        # Simulate QR code generation
        await asyncio.sleep(2)  # simulate network latency

        # Generate a mock QR URL
        qr_url = f"https://passport.bilibili.com/qrcode/h5/login?qrcode_key={session_id}"

        session["qr_code"] = qr_url
        session["status"] = "processing"

        # Simulate waiting for the scan
        await asyncio.sleep(30)  # wait 30 seconds

        # Simulate a successful login
        if session_id in qr_sessions:
            qr_sessions[session_id]["status"] = "success"

    except Exception as e:
        if session_id in qr_sessions:
            qr_sessions[session_id]["status"] = "failed"
            qr_sessions[session_id]["error_message"] = str(e)
        logger.error(f"Failed to generate QR code: {e}")
