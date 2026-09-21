"""
ENprogressAPI - ENAPI
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from backend.services.simple_progress import get_multiple_progress_snapshots, get_progress_snapshot

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/simple-progress", tags=["simple-progress"])


@router.get("/snapshot")
def get_progress_snapshots(project_ids: List[str] = Query(..., description="projectIDEN")):
    """
    ENfetchprojectprogressEN
    
    Args:
        project_ids: projectIDEN
        
    Returns:
        progressEN
    """
    try:
        if not project_ids:
            return []
            
        snapshots = get_multiple_progress_snapshots(project_ids)
        logger.info(f"fetchprogressEN: {len(snapshots)} ENproject")
        return snapshots
        
    except Exception as e:
        logger.error(f"fetchprogressENfailed: {e}")
        raise HTTPException(status_code=500, detail=f"fetchprogressENfailed: {str(e)}")


@router.get("/snapshot/{project_id}")
def get_single_progress_snapshot(project_id: str):
    """
    fetchENprojectprogressEN
    
    Args:
        project_id: projectID
        
    Returns:
        progressEN
    """
    try:
        snapshot = get_progress_snapshot(project_id)
        if snapshot is None:
            # returnENstatus
            return {
                "project_id": project_id,
                "stage": "INGEST",
                "percent": 0,
                "message": "ENstart",
                "ts": 0
            }
            
        return snapshot
        
    except Exception as e:
        logger.error(f"fetchprojectprogressENfailed: {e}")
        raise HTTPException(status_code=500, detail=f"fetchprojectprogressENfailed: {str(e)}")


@router.get("/stages")
def get_available_stages():
    """
    fetchENprocessingEN
    
    Returns:
        ENconfigEN
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
