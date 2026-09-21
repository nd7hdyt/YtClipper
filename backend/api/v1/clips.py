"""
clipAPItranslated
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...services.clip_service import ClipService
from ...schemas.clip import ClipCreate, ClipUpdate, ClipResponse, ClipListResponse, ClipStatus, ClipFilter
from ...schemas.base import PaginationParams
from ...models.clip import Clip
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_clip_service(db: Session = Depends(get_db)) -> ClipService:
    """Dependency to get clip service."""
    return ClipService(db)


@router.patch("/{clip_id}/title", response_model=ClipResponse)
async def update_clip_title(
    clip_id: str,
    title_data: dict,
    clip_service: ClipService = Depends(get_clip_service)
):
    """Update clip title."""
    try:
        new_title = title_data.get("title", "").strip()
        if not new_title:
            raise HTTPException(status_code=400, detail="translated")
        
        if len(new_title) > 200:
            raise HTTPException(status_code=400, detail="translated200 translated")
        
        # updatecliptranslated
        clip = clip_service.update_clip(clip_id, ClipUpdate(title=new_title))
        if not clip:
            raise HTTPException(status_code=404, detail="clipnot found")
        
        # returnupdatetranslated'sclipinfo
        return ClipResponse(
            id=str(clip.id),
            project_id=str(clip.project_id),
            title=str(clip.title),
            description=str(clip.description) if clip.description else None,
            start_time=getattr(clip, 'start_time', 0),
            end_time=getattr(clip, 'end_time', 0),
            duration=int(getattr(clip, 'duration', 0)),
            score=getattr(clip, 'score', None),
            status=getattr(clip, 'status', 'pending'),
            video_path=getattr(clip, 'video_path', None),
            tags=getattr(clip, 'tags', []) or [],
            clip_metadata=getattr(clip, 'clip_metadata', {}) or {},
            created_at=getattr(clip, 'created_at', None),
            updated_at=getattr(clip, 'updated_at', None),
            collection_ids=[]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"updatecliptranslatedfailed: {e}")
        raise HTTPException(status_code=500, detail=f"updatecliptranslatedfailed: {str(e)}")


@router.post("/{clip_id}/generate-title", response_model=dict)
async def generate_clip_title(
    clip_id: str,
    clip_service: ClipService = Depends(get_clip_service)
):
    """Generate a new title for a clip using LLM."""
    try:
        # fetchclipinfo
        clip = clip_service.get(clip_id)
        if not clip:
            raise HTTPException(status_code=404, detail="clipnot found")
        
        # translatedfromclip_metadatafetchtranslated，No needfromfileSystemfetch
        clip_metadata = getattr(clip, 'clip_metadata', {}) or {}
        
        if not clip_metadata:
            raise HTTPException(status_code=404, detail="cliptranslatednot found")
        
        # translatedLLMtranslated
        llm_input = [{
            "id": clip_id,
            "title": clip_metadata.get('outline', '') or getattr(clip, 'title', ''),
            "content": clip_metadata.get('content', []),
            "recommend_reason": clip_metadata.get('recommend_reason', '')
        }]
        
        # callLLMtranslated
        from ...utils.llm_client import LLMClient
        from ...core.shared_config import PROMPT_FILES
        
        llm_client = LLMClient()
        
        # translated
        with open(PROMPT_FILES['title'], 'r', encoding='utf-8') as f:
            title_prompt = f.read()
        
        # callLLM
        raw_response = llm_client.call_with_retry(title_prompt, llm_input)
        
        if not raw_response:
            raise HTTPException(status_code=500, detail="LLMcallfailed")
        
        # translatedLLMtranslated
        titles_map = llm_client.parse_json_response(raw_response)
        
        if not isinstance(titles_map, dict) or clip_id not in titles_map:
            raise HTTPException(status_code=500, detail="LLMreturnformaterror")
        
        generated_title = titles_map[clip_id]
        
        return {
            "clip_id": clip_id,
            "generated_title": generated_title,
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"translatedcliptranslatedfailed: {e}")
        raise HTTPException(status_code=500, detail=f"translatedcliptranslatedfailed: {str(e)}")


@router.post("/", response_model=ClipResponse)
async def create_clip(
    clip_data: ClipCreate,
    clip_service: ClipService = Depends(get_clip_service)
):
    """Create a new clip."""
    try:
        clip = clip_service.create_clip(clip_data)
        # Convert to response schema
        status_obj = getattr(clip, 'status', None)
        status_value = status_obj.value if hasattr(status_obj, 'value') else 'pending'
        
        return ClipResponse(
            id=str(getattr(clip, 'id', '')),
            project_id=str(getattr(clip, 'project_id', '')),
            title=str(getattr(clip, 'title', '')),
            description=str(getattr(clip, 'description', '')) if getattr(clip, 'description', None) else None,
            start_time=getattr(clip, 'start_time', 0),
            end_time=getattr(clip, 'end_time', 0),
            duration=getattr(clip, 'duration', 0),
            score=getattr(clip, 'score', None),
            status=status_value,
            video_path=getattr(clip, 'video_path', None),
            tags=getattr(clip, 'tags', []) or [],
            clip_metadata=getattr(clip, 'clip_metadata', {}) or {},
            created_at=getattr(clip, 'created_at', None) if isinstance(getattr(clip, 'created_at', None), (type(None), __import__('datetime').datetime)) else None,
            updated_at=getattr(clip, 'updated_at', None) if isinstance(getattr(clip, 'updated_at', None), (type(None), __import__('datetime').datetime)) else None,
            collection_ids=[]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=ClipListResponse)
async def get_clips(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    status: Optional[ClipStatus] = Query(None, description="Filter by status"),
    clip_service: ClipService = Depends(get_clip_service)
):
    """Get paginated clips with optional filtering."""
    try:
        pagination = PaginationParams(page=page, size=size)
        
        filters = None
        if project_id or status:
            filters = ClipFilter(
                project_id=project_id,
                status=status
            )
        
        return clip_service.get_clips_paginated(pagination, filters)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{clip_id}", response_model=ClipResponse)
async def get_clip(
    clip_id: str,
    clip_service: ClipService = Depends(get_clip_service)
):
    """Get a clip by ID."""
    try:
        clip = clip_service.get(clip_id)
        if not clip:
            raise HTTPException(status_code=404, detail="Clip not found")
        return clip
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{clip_id}", response_model=ClipResponse)
async def update_clip(
    clip_id: str,
    clip_data: ClipUpdate,
    clip_service: ClipService = Depends(get_clip_service)
):
    """Update a clip."""
    try:
        clip = clip_service.update_clip(clip_id, clip_data)
        if not clip:
            raise HTTPException(status_code=404, detail="Clip not found")
        return clip
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{clip_id}")
async def delete_clip(
    clip_id: str,
    clip_service: ClipService = Depends(get_clip_service)
):
    """Delete a clip."""
    try:
        success = clip_service.delete(clip_id)
        if not success:
            raise HTTPException(status_code=404, detail="Clip not found")
        return {"message": "Clip deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/cleanup-duplicates")
async def cleanup_duplicate_clips(
    project_id: str,
    db: Session = Depends(get_db)
):
    """cleanprojecttranslated'stranslatedcliptranslated"""
    try:
        from ...models.project import Project
        import json
        from pathlib import Path
        from ...core.config import get_data_directory
        
        # fetchproject
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        
        # fetchdatabasetranslated'stranslatedclip
        db_clips = db.query(Clip).filter(Clip.project_id == project_id).all()
        logger.info(f"databasetranslated {len(db_clips)}  clip")
        
        # translatedfileSystemtranslated'stranslated
        data_dir = get_data_directory()
        project_dir = data_dir / "projects" / project_id
        clips_metadata_file = project_dir / "metadata" / "clips_metadata.json"
        
        if not clips_metadata_file.exists():
            raise HTTPException(status_code=404, detail="cliptranslatedfile not found")
        
        with open(clips_metadata_file, 'r', encoding='utf-8') as f:
            original_clips = json.load(f)
        
        logger.info(f"fileSystemtranslated {len(original_clips)}  clip")
        
        # createtranslatedclip'sIDtranslated
        original_clip_ids = {clip['id']: clip for clip in original_clips}
        
        # cleantranslated
        deleted_count = 0
        kept_count = 0
        
        for db_clip in db_clips:
            metadata = db_clip.clip_metadata or {}
            original_id = metadata.get('id')
            
            if original_id and original_id in original_clip_ids:
                # this clipIstranslated's，translated
                kept_count += 1
                logger.info(f"translatedclip: {db_clip.title} (ID: {original_id})")
            else:
                # this clipIstranslated'sortranslated's，delete
                logger.info(f"deletetranslatedclip: {db_clip.title} (DB ID: {db_clip.id})")
                db.delete(db_clip)
                deleted_count += 1
        
        db.commit()
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "original_count": len(original_clips),
            "db_before_count": len(db_clips),
            "kept_count": kept_count,
            "deleted_count": deleted_count,
            "message": f"cleantranslated：translated {kept_count}  ，delete {deleted_count}  translatedclip"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"cleantranslatedclipfailed: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"cleanfailed: {str(e)}")


@router.post("/resync-project")
async def resync_project_clips(
    project_id: str,
    db: Session = Depends(get_db)
):
    """translatedproject'scliptranslated"""
    try:
        from ...models.project import Project
        from ...services.data_sync_service import DataSyncService
        from pathlib import Path
        from ...core.config import get_data_directory
        
        # fetchproject
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        
        # deletetranslated'scliptranslated
        existing_clips = db.query(Clip).filter(Clip.project_id == project_id).all()
        deleted_count = len(existing_clips)
        for clip in existing_clips:
            db.delete(clip)
        db.commit()
        logger.info(f"deletetranslated {deleted_count}  translatedclip")
        
        # translated
        data_dir = get_data_directory()
        project_dir = data_dir / "projects" / project_id
        
        sync_service = DataSyncService(db)
        synced_count = sync_service._sync_clips_from_filesystem(project_id, project_dir)
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "deleted_count": deleted_count,
            "synced_count": synced_count,
            "message": f"translated：delete {deleted_count}  ，translated {synced_count}  clip"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"translatedclipfailed: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"translatedfailed: {str(e)}")