from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from ..core.database import get_db
from ..services.upload_queue_service import UploadQueueService, TaskPriority
# from ..utils.auth import get_current_user  # EN，ENneedcanEN

router = APIRouter(prefix="/api/upload-queue", tags=["upload-queue"])

# requestEN
class UploadTaskRequest(BaseModel):
    video_path: str
    title: str
    description: str = ""
    tags: str = ""
    account_id: Optional[int] = None
    priority: str = "normal"  # low, normal, high, urgent

class BatchUploadRequest(BaseModel):
    tasks: List[UploadTaskRequest]

class TaskResponse(BaseModel):
    task_id: str
    video_path: str
    title: str
    description: str
    tags: str
    account_id: Optional[int]
    priority: int
    status: str
    created_at: str
    updated_at: str
    progress: int
    error_message: Optional[str]
    retry_count: int
    max_retries: int
    celery_task_id: Optional[str]

class QueueStatusResponse(BaseModel):
    queued_tasks: int
    processing_tasks: int
    max_concurrent: int
    queue_details: List[Dict[str, Any]]
    processing_details: List[Dict[str, Any]]

# ENqueueserviceEN
queue_services: Dict[int, UploadQueueService] = {}

def get_queue_service(db: Session = Depends(get_db)) -> UploadQueueService:
    """fetchqueueserviceEN"""
    # ENuseENuserID，ENcanEN
    user_id = 1
    
    if user_id not in queue_services:
        queue_services[user_id] = UploadQueueService(db)
    
    return queue_services[user_id]

@router.post("/add-task", response_model=Dict[str, str])
async def add_upload_task(
    request: UploadTaskRequest,
    queue_service: UploadQueueService = Depends(get_queue_service)
):
    """ENuploadtask"""
    try:
        # EN
        priority_map = {
            "low": TaskPriority.LOW,
            "normal": TaskPriority.NORMAL,
            "high": TaskPriority.HIGH,
            "urgent": TaskPriority.URGENT
        }
        priority = priority_map.get(request.priority.lower(), TaskPriority.NORMAL)
        
        task_id = queue_service.add_task(
            video_path=request.video_path,
            title=request.title,
            description=request.description,
            tags=request.tags,
            account_id=request.account_id,
            priority=priority
        )
        
        return {"task_id": task_id, "message": "taskENqueue"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/add-batch-tasks", response_model=Dict[str, Any])
async def add_batch_upload_tasks(
    request: BatchUploadRequest,
    queue_service: UploadQueueService = Depends(get_queue_service)
):
    """ENuploadtask"""
    try:
        # ENtaskEN
        tasks_data = []
        priority_map = {
            "low": TaskPriority.LOW,
            "normal": TaskPriority.NORMAL,
            "high": TaskPriority.HIGH,
            "urgent": TaskPriority.URGENT
        }
        
        for task_req in request.tasks:
            priority = priority_map.get(task_req.priority.lower(), TaskPriority.NORMAL)
            tasks_data.append({
                "video_path": task_req.video_path,
                "title": task_req.title,
                "description": task_req.description,
                "tags": task_req.tags,
                "account_id": task_req.account_id,
                "priority": priority
            })
        
        task_ids = queue_service.add_batch_tasks(tasks_data)
        
        return {
            "task_ids": task_ids,
            "count": len(task_ids),
            "message": f"EN {len(task_ids)} ENtaskENqueue"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/task/{task_id}", response_model=Optional[TaskResponse])
async def get_task_status(
    task_id: str,
    queue_service: UploadQueueService = Depends(get_queue_service)
):
    """fetchtaskstatus"""
    try:
        task_status = queue_service.get_task_status(task_id)
        if not task_status:
            raise HTTPException(status_code=404, detail="taskdoes not exist")
        
        return task_status
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/task/{task_id}")
async def cancel_task(
    task_id: str,
    queue_service: UploadQueueService = Depends(get_queue_service)
):
    """canceltask"""
    try:
        success = queue_service.cancel_task(task_id)
        if not success:
            raise HTTPException(status_code=404, detail="taskdoes not existENcannotcancel")
        
        return {"message": "taskENcancel"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status", response_model=QueueStatusResponse)
async def get_queue_status(
    queue_service: UploadQueueService = Depends(get_queue_service)
):
    """fetchqueuestatus"""
    try:
        status = queue_service.get_queue_status()
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retry/{task_id}")
async def retry_failed_task(
    task_id: str,
    queue_service: UploadQueueService = Depends(get_queue_service)
):
    """retryfailedENtask"""
    try:
        # fetchtaskstatus
        task_status = queue_service.get_task_status(task_id)
        if not task_status:
            raise HTTPException(status_code=404, detail="taskdoes not exist")
        
        if task_status["status"] != "failed":
            raise HTTPException(status_code=400, detail="ENretryfailedENtask")
        
        # ENtask
        new_task_id = queue_service.add_task(
            video_path=task_status["video_path"],
            title=task_status["title"],
            description=task_status["description"],
            tags=task_status["tags"],
            account_id=task_status["account_id"],
            priority=TaskPriority(task_status["priority"])
        )
        
        return {
            "new_task_id": new_task_id,
            "message": "taskENqueue"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_upload_history(
    limit: int = 50,
    offset: int = 0,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)  # EN
):
    """fetchuploadEN"""
    try:
        from ..models.bilibili import BilibiliUploadRecord
        
        query = db.query(BilibiliUploadRecord)
        
        if status:
            query = query.filter(BilibiliUploadRecord.status == status)
        
        # ENcreatetimeEN
        records = query.order_by(BilibiliUploadRecord.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "records": [
                {
                    "id": record.id,
                    "task_id": record.task_id,
                    "title": record.title,
                    "bv_id": record.bv_id,
                    "status": record.status,
                    "account_id": record.account_id,
                    "created_at": record.created_at.isoformat(),
                    "updated_at": record.updated_at.isoformat() if record.updated_at else None,
                    "error_message": record.error_message
                }
                for record in records
            ],
            "total": query.count()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear-completed")
async def clear_completed_tasks(
    queue_service: UploadQueueService = Depends(get_queue_service)
):
    """ENcompletedENtask"""
    try:
        # ENcanEN
        # ENtaskENqueueEN，ENdatabaseEN
        return {"message": "completedtaskEN"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics")
async def get_upload_statistics(
    days: int = 7,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)  # EN
):
    """fetchuploadEN"""
    try:
        from ..models.bilibili import BilibiliUploadRecord
        from datetime import datetime, timedelta
        from sqlalchemy import func
        
        # ENtimeEN
        start_date = datetime.now() - timedelta(days=days)
        
        # EN
        total_uploads = db.query(BilibiliUploadRecord).filter(
            BilibiliUploadRecord.created_at >= start_date
        ).count()
        
        successful_uploads = db.query(BilibiliUploadRecord).filter(
            BilibiliUploadRecord.created_at >= start_date,
            BilibiliUploadRecord.status == 'completed'
        ).count()
        
        failed_uploads = db.query(BilibiliUploadRecord).filter(
            BilibiliUploadRecord.created_at >= start_date,
            BilibiliUploadRecord.status == 'failed'
        ).count()
        
        # ENaccountEN
        account_stats = db.query(
            BilibiliUploadRecord.account_id,
            func.count(BilibiliUploadRecord.id).label('count'),
            func.sum(func.case([(BilibiliUploadRecord.status == 'completed', 1)], else_=0)).label('successful')
        ).filter(
            BilibiliUploadRecord.created_at >= start_date
        ).group_by(BilibiliUploadRecord.account_id).all()
        
        return {
            "period_days": days,
            "total_uploads": total_uploads,
            "successful_uploads": successful_uploads,
            "failed_uploads": failed_uploads,
            "success_rate": round(successful_uploads / total_uploads * 100, 2) if total_uploads > 0 else 0,
            "account_statistics": [
                {
                    "account_id": stat.account_id,
                    "total_uploads": stat.count,
                    "successful_uploads": stat.successful,
                    "success_rate": round(stat.successful / stat.count * 100, 2) if stat.count > 0 else 0
                }
                for stat in account_stats
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))