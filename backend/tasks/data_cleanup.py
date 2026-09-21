"""
ENtask
ENdatabaseENfilesystemEN
"""

import os
import logging
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List
from celery import current_task, shared_task

from ..core.celery_app import celery_app
from ..core.database import SessionLocal
from ..models.task import Task, TaskStatus
from ..models.project import Project, ProjectStatus
from ..models.clip import Clip
from ..models.collection import Collection
from ..repositories.task_repository import TaskRepository
from ..repositories.project_repository import ProjectRepository

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='backend.tasks.data_cleanup.cleanup_expired_data')
def cleanup_expired_data(self, days: int = 30) -> Dict[str, Any]:
    """
    EN
    
    Args:
        days: EN，EN30EN
        
    Returns:
        ENresult
    """
    logger.info(f"startEN，EN: {days}")
    
    try:
        # createdatabaseEN
        db = SessionLocal()
        
        try:
            cleanup_results = {
                'timestamp': datetime.utcnow().isoformat(),
                'days': days,
                'tasks_cleaned': 0,
                'projects_cleaned': 0,
                'files_cleaned': 0,
                'errors': []
            }
            
            # 1. ENtask
            try:
                task_repo = TaskRepository(db)
                tasks_cleaned = task_repo.cleanup_old_tasks(days)
                cleanup_results['tasks_cleaned'] = tasks_cleaned
                logger.info(f"EN {tasks_cleaned} ENtask")
            except Exception as e:
                error_msg = f"ENtaskfailed: {str(e)}"
                logger.error(error_msg)
                cleanup_results['errors'].append(error_msg)
            
            # 2. ENproject
            try:
                projects_cleaned = _cleanup_expired_projects(db, days)
                cleanup_results['projects_cleaned'] = projects_cleaned
                logger.info(f"EN {projects_cleaned} ENproject")
            except Exception as e:
                error_msg = f"ENprojectfailed: {str(e)}"
                logger.error(error_msg)
                cleanup_results['errors'].append(error_msg)
            
            # 3. ENfile
            try:
                files_cleaned = _cleanup_orphaned_files()
                cleanup_results['files_cleaned'] = files_cleaned
                logger.info(f"EN {files_cleaned} ENfile")
            except Exception as e:
                error_msg = f"ENfilefailed: {str(e)}"
                logger.error(error_msg)
                cleanup_results['errors'].append(error_msg)
            
            # 4. ENfile
            try:
                temp_files_cleaned = _cleanup_temp_files()
                cleanup_results['temp_files_cleaned'] = temp_files_cleaned
                logger.info(f"EN {temp_files_cleaned} ENfile")
            except Exception as e:
                error_msg = f"ENfilefailed: {str(e)}"
                logger.error(error_msg)
                cleanup_results['errors'].append(error_msg)
            
            cleanup_results['success'] = len(cleanup_results['errors']) == 0
            cleanup_results['total_cleaned'] = (
                cleanup_results['tasks_cleaned'] + 
                cleanup_results['projects_cleaned'] + 
                cleanup_results['files_cleaned'] +
                cleanup_results.get('temp_files_cleaned', 0)
            )
            
            logger.info(f"EN，EN {cleanup_results['total_cleaned']} EN")
            return cleanup_results
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"ENfailed，error: {e}")
        raise


def _cleanup_expired_projects(db: SessionLocal, days: int) -> int:
    """ENproject"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # ENcompletedproject
    expired_projects = db.query(Project).filter(
        Project.status == ProjectStatus.COMPLETED,
        Project.updated_at < cutoff_date
    ).all()
    
    cleaned_count = 0
    for project in expired_projects:
        try:
            # deleteprojectEN
            _delete_project_data(db, project.id)
            cleaned_count += 1
            logger.info(f"ENproject: {project.id}")
        except Exception as e:
            logger.error(f"ENproject {project.id} failed: {e}")
    
    return cleaned_count


def _delete_project_data(db: SessionLocal, project_id: str):
    """deleteprojectEN"""
    # deleteENtask
    db.query(Task).filter(Task.project_id == project_id).delete()
    
    # deleteENclip
    db.query(Clip).filter(Clip.project_id == project_id).delete()
    
    # deleteENcollection
    db.query(Collection).filter(Collection.project_id == project_id).delete()
    
    # deleteprojectEN
    db.query(Project).filter(Project.id == project_id).delete()
    
    # deleteprojectfile
    project_dir = Path(f"data/projects/{project_id}")
    if project_dir.exists():
        shutil.rmtree(project_dir)
    
    # ENprogressEN
    try:
        from ..services.simple_progress import clear_progress
        clear_progress(project_id)
    except Exception as e:
        logger.warning(f"ENprogressENfailed: {e}")
    
    db.commit()


def _cleanup_orphaned_files() -> int:
    """ENfile"""
    cleaned_count = 0
    
    try:
        # fetchdatabaseENprojectID
        db = SessionLocal()
        try:
            db_projects = {p.id for p in db.query(Project).all()}
        finally:
            db.close()
        
        # ENprojectdirectory
        projects_dir = Path("data/projects")
        if projects_dir.exists():
            for project_dir in projects_dir.iterdir():
                if project_dir.is_dir() and project_dir.name not in db_projects:
                    if not project_dir.name.startswith('.'):
                        shutil.rmtree(project_dir)
                        cleaned_count += 1
                        logger.info(f"ENprojectdirectory: {project_dir.name}")
        
        # ENfile
        output_dir = Path("data/output")
        if output_dir.exists():
            for file_path in output_dir.rglob("*"):
                if file_path.is_file():
                    # checkfileENproject
                    file_name = file_path.name
                    is_orphaned = True
                    
                    for project_id in db_projects:
                        if project_id in file_name:
                            is_orphaned = False
                            break
                    
                    if is_orphaned:
                        file_path.unlink()
                        cleaned_count += 1
                        logger.info(f"ENfile: {file_path}")
        
    except Exception as e:
        logger.error(f"ENfilefailed: {e}")
    
    return cleaned_count


def _cleanup_temp_files() -> int:
    """ENfile"""
    cleaned_count = 0
    
    try:
        temp_dir = Path("data/temp")
        if temp_dir.exists():
            for file_path in temp_dir.iterdir():
                if file_path.is_file():
                    # checkfileEN1EN
                    file_age = datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_age > timedelta(hours=1):
                        file_path.unlink()
                        cleaned_count += 1
                        logger.info(f"ENfile: {file_path}")
        
        # ENprocessingENfile
        projects_dir = Path("data/projects")
        if projects_dir.exists():
            for project_dir in projects_dir.iterdir():
                if project_dir.is_dir():
                    processing_dir = project_dir / "processing"
                    if processing_dir.exists():
                        for file_path in processing_dir.iterdir():
                            if file_path.is_file():
                                # checkfileEN24EN
                                file_age = datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)
                                if file_age > timedelta(hours=24):
                                    file_path.unlink()
                                    cleaned_count += 1
                                    logger.info(f"ENprocessingENfile: {file_path}")
        
    except Exception as e:
        logger.error(f"ENfilefailed: {e}")
    
    return cleaned_count


@shared_task(bind=True, name='backend.tasks.data_cleanup.check_data_consistency')
def check_data_consistency(self) -> Dict[str, Any]:
    """
    checkEN
    
    Returns:
        ENcheckresult
    """
    logger.info("startENcheck")
    
    try:
        # createdatabaseEN
        db = SessionLocal()
        
        try:
            issues = []
            
            # 1. checkprojectEN
            db_projects = {p.id for p in db.query(Project).all()}
            fs_projects = set()
            
            projects_dir = Path("data/projects")
            if projects_dir.exists():
                for project_dir in projects_dir.iterdir():
                    if project_dir.is_dir() and not project_dir.name.startswith('.'):
                        fs_projects.add(project_dir.name)
            
            # checkENfile
            orphaned_files = fs_projects - db_projects
            if orphaned_files:
                issues.append({
                    "type": "orphaned_files",
                    "count": len(orphaned_files),
                    "details": list(orphaned_files)
                })
            
            # checkENfile
            missing_files = db_projects - fs_projects
            if missing_files:
                issues.append({
                    "type": "missing_files",
                    "count": len(missing_files),
                    "details": list(missing_files)
                })
            
            # 2. checktaskEN
            orphaned_tasks = db.query(Task).filter(
                ~Task.project_id.in_(db_projects)
            ).count()
            
            if orphaned_tasks > 0:
                issues.append({
                    "type": "orphaned_tasks",
                    "count": orphaned_tasks,
                    "details": []
                })
            
            # 3. checkclipEN
            orphaned_clips = db.query(Clip).filter(
                ~Clip.project_id.in_(db_projects)
            ).count()
            
            if orphaned_clips > 0:
                issues.append({
                    "type": "orphaned_clips",
                    "count": orphaned_clips,
                    "details": []
                })
            
            # 4. checkcollectionEN
            orphaned_collections = db.query(Collection).filter(
                ~Collection.project_id.in_(db_projects)
            ).count()
            
            if orphaned_collections > 0:
                issues.append({
                    "type": "orphaned_collections",
                    "count": orphaned_collections,
                    "details": []
                })
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'total_issues': len(issues),
                'issues': issues,
                'status': 'healthy' if len(issues) == 0 else 'unhealthy'
            }
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"ENcheckfailed，error: {e}")
        raise


@shared_task(bind=True, name='backend.tasks.data_cleanup.cleanup_orphaned_data')
def cleanup_orphaned_data(self) -> Dict[str, Any]:
    """
    EN
    
    Returns:
        ENresult
    """
    logger.info("startEN")
    
    try:
        # createdatabaseEN
        db = SessionLocal()
        
        try:
            cleanup_results = {
                'timestamp': datetime.utcnow().isoformat(),
                'orphaned_tasks_cleaned': 0,
                'orphaned_clips_cleaned': 0,
                'orphaned_collections_cleaned': 0,
                'orphaned_files_cleaned': 0
            }
            
            # fetchallprojectID
            db_projects = {p.id for p in db.query(Project).all()}
            
            # 1. ENtask
            orphaned_tasks = db.query(Task).filter(
                ~Task.project_id.in_(db_projects)
            ).all()
            
            for task in orphaned_tasks:
                db.delete(task)
                cleanup_results['orphaned_tasks_cleaned'] += 1
                logger.info(f"ENtask: {task.id}")
            
            # 2. ENclip
            orphaned_clips = db.query(Clip).filter(
                ~Clip.project_id.in_(db_projects)
            ).all()
            
            for clip in orphaned_clips:
                db.delete(clip)
                cleanup_results['orphaned_clips_cleaned'] += 1
                logger.info(f"ENclip: {clip.id}")
            
            # 3. ENcollection
            orphaned_collections = db.query(Collection).filter(
                ~Collection.project_id.in_(db_projects)
            ).all()
            
            for collection in orphaned_collections:
                db.delete(collection)
                cleanup_results['orphaned_collections_cleaned'] += 1
                logger.info(f"ENcollection: {collection.id}")
            
            # 4. ENfile
            cleanup_results['orphaned_files_cleaned'] = _cleanup_orphaned_files()
            
            db.commit()
            
            total_cleaned = (
                cleanup_results['orphaned_tasks_cleaned'] +
                cleanup_results['orphaned_clips_cleaned'] +
                cleanup_results['orphaned_collections_cleaned'] +
                cleanup_results['orphaned_files_cleaned']
            )
            
            cleanup_results['total_cleaned'] = total_cleaned
            cleanup_results['success'] = True
            
            logger.info(f"EN，EN {total_cleaned} EN")
            return cleanup_results
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"ENfailed，error: {e}")
        raise
