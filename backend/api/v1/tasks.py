"""
tasktranslatedAPItranslated
"""
import logging
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.task import Task
from backend.schemas.task import TaskResponse, TaskCreate, TaskUpdate
from backend.services.task_service import TaskService
from backend.services.task_queue_service import TaskQueueService

router = APIRouter()
logger = logging.getLogger(__name__)


def _get_task_config_value(task, key: str, default=None):
    config = task.task_config or {}
    return config.get(key, default)

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """fetchtasklist"""
    try:
        task_service = TaskService(db)
        tasks = task_service.get_tasks(
            skip=skip,
            limit=limit,
            status=status,
            project_id=project_id
        )
        return tasks
    except Exception as e:
        logger.exception("fetchtasklistfailed")
        raise HTTPException(status_code=500, detail="fetchtasklistfailed，translated")

@router.get("/project/{project_id}", response_model=List[TaskResponse])
async def get_project_tasks(
    project_id: str,
    db: Session = Depends(get_db)
):
    """fetchtranslatedproject'stasklist"""
    try:
        task_service = TaskService(db)
        tasks = task_service.get_tasks_by_project_id(project_id)
        return tasks
    except Exception as e:
        logger.exception("fetchprojecttaskfailed: %s", project_id)
        raise HTTPException(status_code=500, detail="fetchprojecttaskfailed，translated")

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """fetchtranslated tasktranslated"""
    try:
        task_service = TaskService(db)
        task = task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="tasknot found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("fetchtasktranslatedfailed: %s", task_id)
        raise HTTPException(status_code=500, detail="fetchtasktranslatedfailed，translated")

@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    """createtranslatedtask"""
    try:
        task_service = TaskService(db)
        task = task_service.create_task(task_data)
        return task
    except Exception as e:
        logger.exception("createtaskfailed")
        raise HTTPException(status_code=500, detail="createtaskfailed，translated")

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """updatetask"""
    try:
        task_service = TaskService(db)
        task = task_service.update_task(task_id, task_data)
        if not task:
            raise HTTPException(status_code=404, detail="tasknot found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("updatetaskfailed: %s", task_id)
        raise HTTPException(status_code=500, detail="updatetaskfailed，translated")

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """deletetask"""
    try:
        task_service = TaskService(db)
        success = task_service.delete_task(task_id)
        if not success:
            raise HTTPException(status_code=404, detail="tasknot found")
        return {"message": "taskdeletesucceeded"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("deletetaskfailed: %s", task_id)
        raise HTTPException(status_code=500, detail="deletetaskfailed，translated")

@router.post("/{task_id}/submit")
async def submit_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """translatedtasktranslated"""
    try:
        task_service = TaskService(db)
        task = task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="tasknot found")
        
        queue_service = TaskQueueService(db)
        task_type = str(task.task_type.value if hasattr(task.task_type, "value") else task.task_type)

        if task_type == "video_processing":
            input_video_path = _get_task_config_value(task, "input_video_path")
            input_srt_path = _get_task_config_value(task, "input_srt_path")
            if not input_video_path:
                raise HTTPException(status_code=400, detail="tasktranslated input_video_path config")
            result = queue_service.submit_video_processing_task(
                project_id=task.project_id,
                input_video_path=input_video_path,
                input_srt_path=input_srt_path,
            )
        elif task_type == "clip_generation":
            clip_data = _get_task_config_value(task, "clip_data", [])
            result = queue_service.submit_video_clips_task(task.project_id, clip_data)
        elif task_type == "collection_creation":
            collection_data = _get_task_config_value(task, "collection_data", [])
            result = queue_service.submit_collection_generation_task(task.project_id, collection_data)
        else:
            raise HTTPException(status_code=400, detail=f"translatedsupport'stasktranslated: {task_type}")
        
        return {
            "message": "tasktranslated",
            "task_id": task_id,
            "queue_task_id": result.get("task_id"),
            "celery_task_id": result.get("celery_task_id"),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("translatedtaskfailed: %s", task_id)
        raise HTTPException(status_code=500, detail="translatedtaskfailed，translated")

@router.post("/{task_id}/retry")
async def retry_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """translatedfailed'stask"""
    try:
        task_service = TaskService(db)
        task = task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="tasknot found")
        
        # translatedtaskstatustranslated
        task_service.update_task(task_id, TaskUpdate(status="pending", progress=0))
        
        queue_service = TaskQueueService(db)
        task_type = str(task.task_type.value if hasattr(task.task_type, "value") else task.task_type)

        if task_type == "video_processing":
            input_video_path = _get_task_config_value(task, "input_video_path")
            input_srt_path = _get_task_config_value(task, "input_srt_path")
            if not input_video_path:
                raise HTTPException(status_code=400, detail="tasktranslated input_video_path config")
            result = queue_service.submit_video_processing_task(
                project_id=task.project_id,
                input_video_path=input_video_path,
                input_srt_path=input_srt_path,
            )
        elif task_type == "clip_generation":
            clip_data = _get_task_config_value(task, "clip_data", [])
            result = queue_service.submit_video_clips_task(task.project_id, clip_data)
        elif task_type == "collection_creation":
            collection_data = _get_task_config_value(task, "collection_data", [])
            result = queue_service.submit_collection_generation_task(task.project_id, collection_data)
        else:
            raise HTTPException(status_code=400, detail=f"translatedsupport'stasktranslated: {task_type}")
        
        return {
            "message": "tasktranslated",
            "task_id": task_id,
            "queue_task_id": result.get("task_id"),
            "celery_task_id": result.get("celery_task_id"),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("translatedtaskfailed: %s", task_id)
        raise HTTPException(status_code=500, detail="translatedtaskfailed，translated")

@router.get("/{task_id}/status")
async def get_task_status(
    task_id: str,
    db: Session = Depends(get_db)
):
    """fetchtaskstatus"""
    try:
        task_service = TaskService(db)
        task = task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="tasknot found")
        
        return {
            "task_id": task_id,
            "status": task.status,
            "progress": task.progress,
            "message": task.name,
            "error": task.error_message,
            "updated_at": task.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("fetchtaskstatusfailed: %s", task_id)
        raise HTTPException(status_code=500, detail="fetchtaskstatusfailed，translated")

