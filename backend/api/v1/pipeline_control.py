"""
translatedAPI
Providestranslatedstart、translatedAndtranslatedstatus'sfeature
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from ...core.database import get_db
from ...models.project import Project, ProjectStatus
from ...models.task import Task, TaskStatus
from ...services.auto_pipeline_service import auto_pipeline_service
from ...services.progress_update_service import progress_update_service
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/start/{project_id}")
async def start_pipeline(
    project_id: str, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """translatedstartprojecttranslated"""
    try:
        # checkprojectIstranslatedin
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # checkprojectstatus
        if project.status == ProjectStatus.PROCESSING:
            return {"status": "skipped", "message": "projecttranslatedinprocessing"}
        
        if project.status == ProjectStatus.COMPLETED:
            return {"status": "skipped", "message": "projectcompleted"}
        
        # checkIstranslated'stask
        running_task = db.query(Task).filter(
            Task.project_id == project_id,
            Task.status.in_([TaskStatus.PtranslatedDING, TaskStatus.RUNNING])
        ).first()
        
        if running_task and running_task.status == TaskStatus.RUNNING:
            return {"status": "skipped", "message": "projecttranslated'stask"}
        
        # intranslatedstarttranslated
        background_tasks.add_task(
            auto_pipeline_service.auto_start_pipeline,
            project_id
        )
        
        return {
            "status": "started",
            "message": "translatedstarttasktranslated",
            "project_id": project_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"starttranslatedfailed: {str(e)}")

@router.post("/stop/{project_id}")
async def stop_pipeline(project_id: str, db: Session = Depends(get_db)):
    """translatedprojecttranslated"""
    try:
        # checkprojectIstranslatedin
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # translated'stask
        running_tasks = db.query(Task).filter(
            Task.project_id == project_id,
            Task.status.in_([TaskStatus.PtranslatedDING, TaskStatus.RUNNING])
        ).all()
        
        if not running_tasks:
            return {"status": "skipped", "message": "translated'stask"}
        
        # translated'stask
        stopped_count = 0
        for task in running_tasks:
            task.status = TaskStatus.CANCELLED
            task.updated_at = datetime.utcnow()
            
            # translatedprogressupdateservicetranslatedtasktranslated
            try:
                await progress_update_service.complete_task(
                    task_id=task.id,
                    error="tasktranslated"
                )
            except Exception as e:
                logger.warning(f"translatedtasktranslatedfailed: {e}")
            
            stopped_count += 1
        
        # updateprojectstatus
        project.status = ProjectStatus.PtranslatedDING
        project.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "status": "stopped",
            "message": f"translated {stopped_count}  task",
            "project_id": project_id,
            "stopped_tasks": stopped_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"translatedfailed: {str(e)}")

@router.post("/restart/{project_id}")
async def restart_pipeline(
    project_id: str, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """translatedprojecttranslated"""
    try:
        # translated
        stop_result = await stop_pipeline(project_id, db)
        
        # etc.translatedonetranslatedensuretranslated
        import time
        time.sleep(2)
        
        # translatedstarttranslated
        start_result = await start_pipeline(project_id, background_tasks, db)
        
        return {
            "status": "restarted",
            "message": "translated",
            "project_id": project_id,
            "stop_result": stop_result,
            "start_result": start_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"translatedfailed: {str(e)}")

@router.get("/status/{project_id}")
async def get_pipeline_status(project_id: str, db: Session = Depends(get_db)):
    """fetchprojecttranslatedstatus"""
    try:
        # checkprojectIstranslatedin
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # fetchprojecttask
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        # fetchtranslatedprogressinfo
        task_statuses = []
        for task in tasks:
            realtime_progress = progress_update_service.get_task_progress(task.id)
            
            task_info = {
                'id': task.id,
                'name': task.name,
                'status': task.status,
                'progress': task.progress,
                'current_step': task.current_step,
                'created_at': task.created_at.isoformat() if task.created_at else None,
                'started_at': task.started_at.isoformat() if task.started_at else None,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                'updated_at': task.updated_at.isoformat() if task.updated_at else None
            }
            
            if realtime_progress:
                task_info.update({
                    'realtime_progress': realtime_progress['progress'],
                    'realtime_step': realtime_progress['current_step'],
                    'step_details': realtime_progress.get('step_details')
                })
            
            task_statuses.append(task_info)
        
        return {
            'project_id': project_id,
            'project_status': project.status,
            'tasks': task_statuses,
            'total_tasks': len(tasks),
            'running_tasks': len([t for t in tasks if t.status in [TaskStatus.PtranslatedDING, TaskStatus.RUNNING]]),
            'completed_tasks': len([t for t in tasks if t.status == TaskStatus.COMPLETED]),
            'failed_tasks': len([t for t in tasks if t.status == TaskStatus.FAILED])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"fetchtranslatedstatusfailed: {str(e)}")

@router.get("/overview")
async def get_pipeline_overview(db: Session = Depends(get_db)):
    """fetchtranslated"""
    try:
        # fetchtranslatedproject
        projects = db.query(Project).all()
        
        overview = {
            'total_projects': len(projects),
            'processing_projects': 0,
            'completed_projects': 0,
            'failed_projects': 0,
            'pending_projects': 0,
            'project_details': []
        }
        
        for project in projects:
            # fetchprojecttasktranslated
            tasks = db.query(Task).filter(Task.project_id == project.id).all()
            
            project_info = {
                'id': project.id,
                'name': project.name,
                'status': project.status,
                'total_tasks': len(tasks),
                'running_tasks': len([t for t in tasks if t.status in [TaskStatus.PtranslatedDING, TaskStatus.RUNNING]]),
                'completed_tasks': len([t for t in tasks if t.status == TaskStatus.COMPLETED]),
                'failed_tasks': len([t for t in tasks if t.status == TaskStatus.FAILED])
            }
            
            overview['project_details'].append(project_info)
            
            # translatedprojectstatus
            if project.status == ProjectStatus.PROCESSING:
                overview['processing_projects'] += 1
            elif project.status == ProjectStatus.COMPLETED:
                overview['completed_projects'] += 1
            elif project.status == ProjectStatus.FAILED:
                overview['failed_projects'] += 1
            elif project.status == ProjectStatus.PtranslatedDING:
                overview['pending_projects'] += 1
        
        # fetchtranslatedservicestatus
        auto_service_status = auto_pipeline_service.get_processing_status()
        overview['auto_service'] = auto_service_status
        
        return overview
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"fetchtranslatedfailed: {str(e)}")

@router.post("/auto-start-all")
async def auto_start_all_pending_pipelines(background_tasks: BackgroundTasks):
    """translatedstarttranslatedetc.translated'stranslated"""
    try:
        # intranslatedstarttranslatedetc.translated'sproject
        background_tasks.add_task(
            auto_pipeline_service.auto_start_all_pending_pipelines
        )
        
        return {
            "status": "started",
            "message": "translatedstarttranslatedetc.translated'stasktranslated"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"translatedstartfailed: {str(e)}")
