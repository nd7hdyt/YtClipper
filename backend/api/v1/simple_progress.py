"""
translated'sprogressAPI - Providestranslated
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from backend.services.simple_progress import get_multiple_progress_snapshots, get_progress_snapshot

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/simple-progress", tags=["simple-progress"])


@router.get("/snapshot")
def get_progress_snapshots(project_ids: List[str] = Query(..., description="projectIDlist")):
    """
    translatedfetchprojectprogresstranslated
    
    Args:
        project_ids: projectIDlist
        
    Returns:
        progresstranslatedlist
    """
    try:
        if not project_ids:
            return []
            
        snapshots = get_multiple_progress_snapshots(project_ids)
        logger.info(f"fetchprogresstranslated: {len(snapshots)}  project")
        return snapshots
        
    except Exception as e:
        logger.error(f"fetchprogresstranslatedfailed: {e}")
        raise HTTPException(status_code=500, detail=f"fetchprogresstranslatedfailed: {str(e)}")


@router.get("/snapshot/{project_id}")
def get_single_progress_snapshot(project_id: str):
    """
    fetchtranslated projectprogresstranslated
    
    Args:
        project_id: projectID
        
    Returns:
        progresstranslated
    """
    try:
        snapshot = get_progress_snapshot(project_id)
        if snapshot is None:
            # returndefaultstatus
            return {
                "project_id": project_id,
                "stage": "INGEST",
                "percent": 0,
                "message": "etc.translated",
                "ts": 0
            }
            
        return snapshot
        
    except Exception as e:
        logger.error(f"fetchprojectprogresstranslatedfailed: {e}")
        raise HTTPException(status_code=500, detail=f"fetchprojectprogresstranslatedfailed: {str(e)}")


@router.get("/stages")
def get_available_stages():
    """
    fetchcanuse'sprocesstranslatedinfo
    
    Returns:
        translatedconfiginfo
    """
    from backend.services.simple_progress import STAGES, STAGE_NAMES
    
    stages_info = []
    for stage, weight in STAGES:
        stages_info.append({
            "stage": stage,
            "weight": weight,
            "display_name": STAGE_NAMES.get(stage, stage)
        })
    
    return {
        "stages": stages_info,
        "total_weight": sum(weight for _, weight in STAGES)
    }
