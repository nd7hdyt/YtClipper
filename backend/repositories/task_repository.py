"""
taskRepository
ENtaskEN
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from .base import BaseRepository
from ..models.task import Task, TaskStatus, TaskType

class TaskRepository(BaseRepository[Task]):
    """taskRepositoryEN"""
    
    def __init__(self, db: Session):
        super().__init__(Task, db)
    
    def find_all(self, skip: int = 0, limit: int = 100, **filters) -> List[Task]:
        """
        fetchalltask，EN
        
        Args:
            skip: EN
            limit: returnEN
            **filters: EN
            
        Returns:
            taskEN
        """
        query = self.db.query(self.model)
        
        # EN
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.filter(getattr(self.model, key) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_project(self, project_id: str) -> List[Task]:
        """
        fetchprojectENalltask
        
        Args:
            project_id: projectID
            
        Returns:
            taskEN
        """
        return self.find_by(project_id=project_id)
    
    def get_by_status(self, status: TaskStatus) -> List[Task]:
        """
        ENstatusfetchtaskEN
        
        Args:
            status: taskstatus
            
        Returns:
            taskEN
        """
        return self.find_by(status=status)
    
    def get_by_type(self, task_type: TaskType) -> List[Task]:
        """
        ENtaskENfetchtaskEN
        
        Args:
            task_type: taskEN
            
        Returns:
            taskEN
        """
        return self.find_by(task_type=task_type)
    
    def get_by_project_and_status(self, project_id: str, status: TaskStatus) -> List[Task]:
        """
        ENprojectENstatusfetchtaskEN
        
        Args:
            project_id: projectID
            status: taskstatus
            
        Returns:
            taskEN
        """
        return self.find_by(project_id=project_id, status=status)
    
    def get_by_project_and_type(self, project_id: str, task_type: TaskType) -> List[Task]:
        """
        ENprojectENtaskENfetchtaskEN
        
        Args:
            project_id: projectID
            task_type: taskEN
            
        Returns:
            taskEN
        """
        return self.find_by(project_id=project_id, task_type=task_type)
    
    def get_pending_tasks(self) -> List[Task]:
        """
        fetchENprocessingENtask
        
        Returns:
            ENprocessingtaskEN
        """
        return self.find_by(status=TaskStatus.PENDING)
    
    def get_running_tasks(self) -> List[Task]:
        """
        fetchcurrentlyrunENtask
        
        Returns:
            currentlyrunENtaskEN
        """
        return self.find_by(status=TaskStatus.RUNNING)
    
    def get_completed_tasks(self) -> List[Task]:
        """
        fetchcompletedENtask
        
        Returns:
            completedENtaskEN
        """
        return self.find_by(status=TaskStatus.COMPLETED)
    
    def get_failed_tasks(self) -> List[Task]:
        """
        fetchfailedENtask
        
        Returns:
            failedENtaskEN
        """
        return self.find_by(status=TaskStatus.FAILED)
    
    def get_tasks_by_step(self, project_id: str, step: int) -> List[Task]:
        """
        ENprocessingENfetchtask
        
        Args:
            project_id: projectID
            step: processingEN
            
        Returns:
            taskEN
        """
        return self.find_by(project_id=project_id, step=step)
    
    def get_next_pending_task(self) -> Optional[Task]:
        """
        fetchENprocessingtask
        
        Returns:
            ENprocessingtaskENNone
        """
        return self.db.query(self.model).filter(
            self.model.status == TaskStatus.PENDING
        ).order_by(asc(self.model.created_at)).first()
    
    def get_tasks_by_priority(self, priority: int) -> List[Task]:
        """
        ENfetchtask
        
        Args:
            priority: EN
            
        Returns:
            taskEN
        """
        return self.find_by(priority=priority)
    
    def update_task_status(self, task_id: str, status: TaskStatus) -> Optional[Task]:
        """
        updatetaskstatus
        
        Args:
            task_id: taskID
            status: ENstatus
            
        Returns:
            updateENtaskENNone
        """
        return self.update(task_id, status=status)
    
    def update_task_progress(self, task_id: str, progress: float) -> Optional[Task]:
        """
        updatetaskprogress
        
        Args:
            task_id: taskID
            progress: progressEN
            
        Returns:
            updateENtaskENNone
        """
        return self.update(task_id, progress=progress)
    
    def update_task_result(self, task_id: str, result: dict) -> Optional[Task]:
        """
        updatetaskresult
        
        Args:
            task_id: taskID
            result: taskresult
            
        Returns:
            updateENtaskENNone
        """
        return self.update(task_id, result=result)
    
    def update_task_error(self, task_id: str, error_message: str) -> Optional[Task]:
        """
        updatetaskerrorEN
        
        Args:
            task_id: taskID
            error_message: errorEN
            
        Returns:
            updateENtaskENNone
        """
        return self.update(task_id, error_message=error_message, status=TaskStatus.FAILED)
    
    def get_tasks_statistics(self, project_id: str = None) -> dict:
        """
        fetchtaskEN
        
        Args:
            project_id: projectID，ifENNonethenENallproject
            
        Returns:
            EN
        """
        query = self.db.query(self.model)
        if project_id:
            query = query.filter(self.model.project_id == project_id)
        
        total_tasks = query.count()
        pending_tasks = query.filter(self.model.status == TaskStatus.PENDING).count()
        running_tasks = query.filter(self.model.status == TaskStatus.RUNNING).count()
        completed_tasks = query.filter(self.model.status == TaskStatus.COMPLETED).count()
        failed_tasks = query.filter(self.model.status == TaskStatus.FAILED).count()
        
        return {
            "total": total_tasks,
            "pending": pending_tasks,
            "running": running_tasks,
            "completed": completed_tasks,
            "failed": failed_tasks,
            "success_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
    
    def get_recent_tasks(self, limit: int = 10) -> List[Task]:
        """
        fetchENtask
        
        Args:
            limit: returnEN
            
        Returns:
            ENtaskEN
        """
        return self.db.query(self.model).order_by(
            desc(self.model.created_at)
        ).limit(limit).all()
    
    def get_tasks_by_date_range(self, start_date, end_date, project_id: str = None) -> List[Task]:
        """
        ENfetchtask
        
        Args:
            start_date: startEN
            end_date: endEN
            project_id: projectID，ifENNonethenENallproject
            
        Returns:
            taskEN
        """
        query = self.db.query(self.model).filter(
            self.model.created_at >= start_date,
            self.model.created_at <= end_date
        )
        
        if project_id:
            query = query.filter(self.model.project_id == project_id)
        
        return query.order_by(desc(self.model.created_at)).all()
    
    def get_long_running_tasks(self, max_duration_hours: int = 2) -> List[Task]:
        """
        fetchENtimerunENtask
        
        Args:
            max_duration_hours: ENruntime（EN）
            
        Returns:
            ENtimerunENtaskEN
        """
        from datetime import datetime, timedelta
        cutoff_time = datetime.utcnow() - timedelta(hours=max_duration_hours)
        
        return self.db.query(self.model).filter(
            self.model.status == TaskStatus.RUNNING,
            self.model.started_at <= cutoff_time
        ).all()
    
    def cleanup_old_tasks(self, days: int = 30) -> int:
        """
        ENtask，includeexceptionstatusENtask
        
        Args:
            days: EN
            
        Returns:
            deleteENtaskEN
        """
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        long_running_cutoff = datetime.utcnow() - timedelta(hours=24)
        
        total_deleted = 0
        
        try:
            # 1. ENcompleted/failedtask
            completed_tasks = self.db.query(self.model).filter(
                self.model.created_at < cutoff_date,
                self.model.status.in_([TaskStatus.COMPLETED, TaskStatus.FAILED])
            ).delete(synchronize_session=False)
            
            total_deleted += completed_tasks
            logger.info(f"EN {completed_tasks} ENcompleted/failedtask")
            
            # 2. ENtimerunENexceptiontask
            long_running_tasks = self.db.query(self.model).filter(
                self.model.status == TaskStatus.RUNNING,
                self.model.created_at < long_running_cutoff
            ).all()
            
            fixed_count = 0
            for task in long_running_tasks:
                task.status = TaskStatus.FAILED
                task.error_message = "tasktimeout，ENfailed"
                task.updated_at = datetime.utcnow()
                fixed_count += 1
                logger.info(f"ENtimeruntask: {task.id}")
            
            if fixed_count > 0:
                self.db.commit()
                logger.info(f"EN {fixed_count} ENtimerunENtask")
            
            # 3. ENtask（ENprojectENtask）
            from ..models.project import Project
            all_project_ids = {p.id for p in self.db.query(Project).all()}
            orphaned_tasks = self.db.query(self.model).filter(
                ~self.model.project_id.in_(all_project_ids)
            ).all()
            
            orphaned_count = 0
            for task in orphaned_tasks:
                self.db.delete(task)
                orphaned_count += 1
                logger.info(f"ENtask: {task.id}")
            
            if orphaned_count > 0:
                self.db.commit()
                logger.info(f"EN {orphaned_count} ENtask")
            
            return total_deleted + fixed_count + orphaned_count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"ENtaskfailed: {e}")
            raise