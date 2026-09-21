"""
ENretryEN
ENdownloadENprocessingENretryEN
"""

import logging
import uuid
from enum import Enum
from typing import Dict, Any, Optional
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core.database import get_db
from ...models.project import Project, ProjectStatus
from ...models.task import Task, TaskStatus, TaskType
from ...services.project_service import ProjectService
from ...services.processing_service import ProcessingService
from ...core.config import get_data_directory

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/retry", tags=["Enhanced Retry"])

class RetryStrategy(str, Enum):
    """retryEN"""
    DOWNLOAD_ONLY = "download_only"      # ENretrydownload
    PROCESSING_ONLY = "processing_only"  # ENretryprocessing
    FULL_RETRY = "full_retry"           # ENretry（download+processing）
    SMART_RETRY = "smart_retry"         # ENretry（EN）

class RetryRequest(BaseModel):
    """retryrequest"""
    strategy: Optional[RetryStrategy] = RetryStrategy.SMART_RETRY
    force_redownload: bool = False  # ENdownload
    browser: Optional[str] = None   # ENsettings（ENdownload）

class RetryResponse(BaseModel):
    """retryresponse"""
    success: bool
    message: str
    strategy_used: RetryStrategy
    project_id: str
    task_id: Optional[str] = None
    download_task_id: Optional[str] = None

def determine_retry_strategy(project: Project, force_redownload: bool = False) -> RetryStrategy:
    """ENretryEN"""
    if force_redownload:
        return RetryStrategy.FULL_RETRY
    
    # checkvideofileEN
    video_exists = project.video_path and Path(project.video_path).exists()
    
    if not video_exists:
        return RetryStrategy.FULL_RETRY  # ENvideofile，ENretry
    
    # checkprojectstatus
    if project.status == ProjectStatus.FAILED:
        return RetryStrategy.PROCESSING_ONLY  # ENvideofileENprocessingfailed，ENretryprocessing
    elif project.status == ProjectStatus.PENDING:
        return RetryStrategy.PROCESSING_ONLY  # ENvideofileENprocessing，ENretryprocessing
    else:
        return RetryStrategy.SMART_RETRY

async def retry_download_only(
    project_id: str, 
    browser: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """ENretrydownload"""
    try:
        # fetchprojectEN
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="projectdoes not exist")
        
        # fetchENdownloadEN（ENprojectdescriptionEN）
        description = project.description or ""
        if "ENBENdownload:" in description:
            # BENproject
            url = description.replace("ENBENdownload:", "").strip()
            return await retry_bilibili_download(project_id, url, browser, db)
        elif "ENYouTubedownload:" in description:
            # YouTubeproject
            url = description.replace("ENYouTubedownload:", "").strip()
            return await retry_youtube_download(project_id, url, browser, db)
        else:
            raise HTTPException(status_code=400, detail="cannotENdownloadEN")
    
    except Exception as e:
        logger.error(f"retrydownloadfailed: {e}")
        raise HTTPException(status_code=500, detail=f"retrydownloadfailed: {str(e)}")

async def retry_bilibili_download(
    project_id: str, 
    url: str, 
    browser: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """retryBENdownload"""
    try:
        # ENBENdownloadEN
        from .bilibili import process_download_task, BilibiliDownloadRequest
        from .async_task_manager import task_manager
        
        # createdownloadrequest
        request = BilibiliDownloadRequest(
            url=url,
            project_name=db.query(Project).filter(Project.id == project_id).first().name,
            video_category="default",
            browser=browser
        )
        
        # generateENdownloadtaskID
        task_id = str(uuid.uuid4())
        
        # startdownloadtask
        await task_manager.create_safe_task(
            f"bilibili_retry_{task_id}",
            process_download_task,
            task_id,
            request,
            project_id
        )
        
        return {
            "success": True,
            "message": "BENdownloadretryENstart",
            "task_id": task_id
        }
    
    except Exception as e:
        logger.error(f"retryBENdownloadfailed: {e}")
        raise HTTPException(status_code=500, detail=f"retryBENdownloadfailed: {str(e)}")

async def retry_youtube_download(
    project_id: str, 
    url: str, 
    browser: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """retryYouTubedownload"""
    try:
        # ENYouTubedownloadEN
        from .youtube import process_youtube_download_task, YouTubeDownloadRequest
        from .async_task_manager import task_manager
        
        # createdownloadrequest
        request = YouTubeDownloadRequest(
            url=url,
            project_name=db.query(Project).filter(Project.id == project_id).first().name,
            video_category="default",
            browser=browser
        )
        
        # generateENdownloadtaskID
        task_id = str(uuid.uuid4())
        
        # startdownloadtask
        await task_manager.create_safe_task(
            f"youtube_retry_{task_id}",
            process_youtube_download_task,
            task_id,
            request,
            project_id
        )
        
        return {
            "success": True,
            "message": "YouTubedownloadretryENstart",
            "task_id": task_id
        }
    
    except Exception as e:
        logger.error(f"retryYouTubedownloadfailed: {e}")
        raise HTTPException(status_code=500, detail=f"retryYouTubedownloadfailed: {str(e)}")

async def retry_processing_only(
    project_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """ENretryprocessing"""
    try:
        # useENprocessingservice
        processing_service = ProcessingService(db)
        
        # fetchprojectEN
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="projectdoes not exist")
        
        # checkvideofile
        if not project.video_path or not Path(project.video_path).exists():
            raise HTTPException(status_code=400, detail="videofiledoes not exist，pleaseENretrydownload")
        
        # ENprojectstatus
        project.status = ProjectStatus.PENDING
        db.commit()
        
        # startprocessingtask
        result = processing_service.start_processing(
            project_id=project_id,
            srt_path=Path(project.video_path).parent / "input.srt" if (project.video_path and Path(project.video_path).parent / "input.srt").exists() else None
        )
        
        return {
            "success": True,
            "message": "processingretryENstart",
            "task_id": result.get("task_id")
        }
    
    except Exception as e:
        logger.error(f"retryprocessingfailed: {e}")
        raise HTTPException(status_code=500, detail=f"retryprocessingfailed: {str(e)}")

@router.post("/projects/{project_id}/smart-retry", response_model=RetryResponse)
async def smart_retry_project(
    project_id: str,
    request: RetryRequest,
    db: Session = Depends(get_db)
):
    """ENretryproject"""
    try:
        # fetchprojectEN
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="projectdoes not exist")
        
        # ENretryEN
        if request.strategy == RetryStrategy.SMART_RETRY:
            strategy = determine_retry_strategy(project, request.force_redownload)
        else:
            strategy = request.strategy
        
        logger.info(f"project {project_id} useretryEN: {strategy}")
        
        # executeretry
        if strategy == RetryStrategy.FULL_RETRY:
            # ENretry：ENretrydownload，downloadENstartprocessing
            download_result = await retry_download_only(project_id, request.browser, db)
            return RetryResponse(
                success=True,
                message="ENretryENstart（download+processing）",
                strategy_used=strategy,
                project_id=project_id,
                download_task_id=download_result.get("task_id")
            )
        
        elif strategy == RetryStrategy.DOWNLOAD_ONLY:
            # ENretrydownload
            download_result = await retry_download_only(project_id, request.browser, db)
            return RetryResponse(
                success=True,
                message="downloadretryENstart",
                strategy_used=strategy,
                project_id=project_id,
                download_task_id=download_result.get("task_id")
            )
        
        elif strategy == RetryStrategy.PROCESSING_ONLY:
            # ENretryprocessing
            processing_result = await retry_processing_only(project_id, db)
            return RetryResponse(
                success=True,
                message="processingretryENstart",
                strategy_used=strategy,
                project_id=project_id,
                task_id=processing_result.get("task_id")
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"ENretryEN: {strategy}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ENretryfailed: {e}")
        raise HTTPException(status_code=500, detail=f"ENretryfailed: {str(e)}")

@router.get("/projects/{project_id}/retry-strategy")
async def get_retry_strategy(
    project_id: str,
    force_redownload: bool = False,
    db: Session = Depends(get_db)
):
    """fetchsuggestionENretryEN"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="projectdoes not exist")
        
        strategy = determine_retry_strategy(project, force_redownload)
        
        return {
            "project_id": project_id,
            "suggested_strategy": strategy,
            "reason": _get_strategy_reason(project, strategy),
            "video_exists": project.video_path and Path(project.video_path).exists(),
            "project_status": project.status
        }
    
    except Exception as e:
        logger.error(f"fetchretryENfailed: {e}")
        raise HTTPException(status_code=500, detail=f"fetchretryENfailed: {str(e)}")

def _get_strategy_reason(project: Project, strategy: RetryStrategy) -> str:
    """fetchEN"""
    if strategy == RetryStrategy.FULL_RETRY:
        return "ENvideofileENdownload"
    elif strategy == RetryStrategy.PROCESSING_ONLY:
        return "videofileENprocessingfailedENstart"
    elif strategy == RetryStrategy.DOWNLOAD_ONLY:
        return "ENretrydownloadEN"
    else:
        return "EN"
