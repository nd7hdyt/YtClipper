"""
translated'stranslated
supportfromdownloadtranslatedprocess'stranslated
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
    """translated"""
    DOWNLOAD_ONLY = "download_only"      # Onlytranslateddownload
    PROCESSING_ONLY = "processing_only"  # Onlytranslatedprocess
    FULL_RETRY = "full_retry"           # translated（download+process）
    SMART_RETRY = "smart_retry"         # translated（translated）

class RetryRequest(BaseModel):
    """translated"""
    strategy: Optional[RetryStrategy] = RetryStrategy.SMART_RETRY
    force_redownload: bool = False  # Istranslateddownload
    browser: Optional[str] = None   # translatedsettings（usetranslateddownload）

class RetryResponse(BaseModel):
    """translated"""
    success: bool
    message: str
    strategy_used: RetryStrategy
    project_id: str
    task_id: Optional[str] = None
    download_task_id: Optional[str] = None

def determine_retry_strategy(project: Project, force_redownload: bool = False) -> RetryStrategy:
    """translated"""
    if force_redownload:
        return RetryStrategy.FULL_RETRY
    
    # checkvideofileIstranslatedin
    video_exists = project.video_path and Path(project.video_path).exists()
    
    if not video_exists:
        return RetryStrategy.FULL_RETRY  # translatedvideofile，translated
    
    # checkprojectstatus
    if project.status == ProjectStatus.FAILED:
        return RetryStrategy.PROCESSING_ONLY  # translatedvideofiletranslatedprocessing failed，Onlytranslatedprocess
    elif project.status == ProjectStatus.PtranslatedDING:
        return RetryStrategy.PROCESSING_ONLY  # translatedvideofiletranslatedprocess，Onlytranslatedprocess
    else:
        return RetryStrategy.SMART_RETRY

async def retry_download_only(
    project_id: str, 
    browser: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Onlytranslateddownload"""
    try:
        # fetchprojectinfo
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        
        # fetchtranslateddownloadinfo（fromprojecttranslated）
        description = project.description or ""
        if "fromBsitedownload:" in description:
            # Bsiteproject
            url = description.replace("fromBsitedownload:", "").strip()
            return await retry_bilibili_download(project_id, url, browser, db)
        elif "fromYouTubedownload:" in description:
            # YouTubeproject
            url = description.replace("fromYouTubedownload:", "").strip()
            return await retry_youtube_download(project_id, url, browser, db)
        else:
            raise HTTPException(status_code=400, detail="translateddownloadtranslated")
    
    except Exception as e:
        logger.error(f"translateddownloadfailed: {e}")
        raise HTTPException(status_code=500, detail=f"translateddownloadfailed: {str(e)}")

async def retry_bilibili_download(
    project_id: str, 
    url: str, 
    browser: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """translatedBsitedownload"""
    try:
        # importBsitedownloadtranslated
        from .bilibili import process_download_task, BilibiliDownloadRequest
        from .async_task_manager import task_manager
        
        # createdownloadtranslated
        request = BilibiliDownloadRequest(
            url=url,
            project_name=db.query(Project).filter(Project.id == project_id).first().name,
            video_category="default",
            browser=browser
        )
        
        # translated'sdownloadtaskID
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
            "message": "Bsitedownloadtranslatedstart",
            "task_id": task_id
        }
    
    except Exception as e:
        logger.error(f"translatedBsitedownloadfailed: {e}")
        raise HTTPException(status_code=500, detail=f"translatedBsitedownloadfailed: {str(e)}")

async def retry_youtube_download(
    project_id: str, 
    url: str, 
    browser: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """translatedYouTubedownload"""
    try:
        # importYouTubedownloadtranslated
        from .youtube import process_youtube_download_task, YouTubeDownloadRequest
        from .async_task_manager import task_manager
        
        # createdownloadtranslated
        request = YouTubeDownloadRequest(
            url=url,
            project_name=db.query(Project).filter(Project.id == project_id).first().name,
            video_category="default",
            browser=browser
        )
        
        # translated'sdownloadtaskID
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
            "message": "YouTubedownloadtranslatedstart",
            "task_id": task_id
        }
    
    except Exception as e:
        logger.error(f"translatedYouTubedownloadfailed: {e}")
        raise HTTPException(status_code=500, detail=f"translatedYouTubedownloadfailed: {str(e)}")

async def retry_processing_only(
    project_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Onlytranslatedprocess"""
    try:
        # usetranslated'sprocessservice
        processing_service = ProcessingService(db)
        
        # fetchprojectinfo
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        
        # checkvideofile
        if not project.video_path or not Path(project.video_path).exists():
            raise HTTPException(status_code=400, detail="videofile not found，translateddownload")
        
        # translatedprojectstatus
        project.status = ProjectStatus.PtranslatedDING
        db.commit()
        
        # startprocesstask
        result = processing_service.start_processing(
            project_id=project_id,
            srt_path=Path(project.video_path).parent / "input.srt" if (project.video_path and Path(project.video_path).parent / "input.srt").exists() else None
        )
        
        return {
            "success": True,
            "message": "processtranslatedstart",
            "task_id": result.get("task_id")
        }
    
    except Exception as e:
        logger.error(f"translatedprocessing failed: {e}")
        raise HTTPException(status_code=500, detail=f"translatedprocessing failed: {str(e)}")

@router.post("/projects/{project_id}/smart-retry", response_model=RetryResponse)
async def smart_retry_project(
    project_id: str,
    request: RetryRequest,
    db: Session = Depends(get_db)
):
    """translatedproject"""
    try:
        # fetchprojectinfo
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        
        # translated
        if request.strategy == RetryStrategy.SMART_RETRY:
            strategy = determine_retry_strategy(project, request.force_redownload)
        else:
            strategy = request.strategy
        
        logger.info(f"project {project_id} usetranslated: {strategy}")
        
        # translated
        if strategy == RetryStrategy.FULL_RETRY:
            # translated：translateddownload，downloadtranslatedprocess
            download_result = await retry_download_only(project_id, request.browser, db)
            return RetryResponse(
                success=True,
                message="translatedstart（download+process）",
                strategy_used=strategy,
                project_id=project_id,
                download_task_id=download_result.get("task_id")
            )
        
        elif strategy == RetryStrategy.DOWNLOAD_ONLY:
            # Onlytranslateddownload
            download_result = await retry_download_only(project_id, request.browser, db)
            return RetryResponse(
                success=True,
                message="downloadtranslatedstart",
                strategy_used=strategy,
                project_id=project_id,
                download_task_id=download_result.get("task_id")
            )
        
        elif strategy == RetryStrategy.PROCESSING_ONLY:
            # Onlytranslatedprocess
            processing_result = await retry_processing_only(project_id, db)
            return RetryResponse(
                success=True,
                message="processtranslatedstart",
                strategy_used=strategy,
                project_id=project_id,
                task_id=processing_result.get("task_id")
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"translatedsupport'stranslated: {strategy}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"translatedfailed: {e}")
        raise HTTPException(status_code=500, detail=f"translatedfailed: {str(e)}")

@router.get("/projects/{project_id}/retry-strategy")
async def get_retry_strategy(
    project_id: str,
    force_redownload: bool = False,
    db: Session = Depends(get_db)
):
    """fetchtranslated'stranslated"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        
        strategy = determine_retry_strategy(project, force_redownload)
        
        return {
            "project_id": project_id,
            "suggested_strategy": strategy,
            "reason": _get_strategy_reason(project, strategy),
            "video_exists": project.video_path and Path(project.video_path).exists(),
            "project_status": project.status
        }
    
    except Exception as e:
        logger.error(f"fetchtranslatedfailed: {e}")
        raise HTTPException(status_code=500, detail=f"fetchtranslatedfailed: {str(e)}")

def _get_strategy_reason(project: Project, strategy: RetryStrategy) -> str:
    """fetchtranslatedSelectselecttranslated"""
    if strategy == RetryStrategy.FULL_RETRY:
        return "translatedvideofileortranslateddownload"
    elif strategy == RetryStrategy.PROCESSING_ONLY:
        return "videofiletranslatedintranslatedprocessing failedortranslated"
    elif strategy == RetryStrategy.DOWNLOAD_ONLY:
        return "Onlytranslateddownloadtranslated"
    else:
        return "translated"
