"""
taskRepository
Providestasktranslated'stranslated
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from .base import BaseRepository
from ..models.task import Task, TaskStatus, TaskType

class TaskRepository(BaseRepository[Task]):
    """taskRepositorytranslated"""
    
    def __init__(self, db: Session):
        super().__init__(Task, db)
    
    def find_all(self, skip: int = 0, limit: int = 100, **filters) -> List[Task]:
        """
        fetchtranslatedtask，supporttranslatedAndtranslated
        
        Args:
            skip: skip'stranslated
            limit: return'stranslated
            **filters: translated
            
        Returns:
            tasklist
        """
        query = self.db.query(self.model)
        
        # translatedusetranslated
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.filter(getattr(self.model, key) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_project(self, project_id: str) -> List[Task]:
        """
        fetchproject'stranslatedtask
        
        Args:
            project_id: projectID
            
        Returns:
            tasklist
        """
        return self.find_by(project_id=project_id)
    
    def get_by_status(self, status: TaskStatus) -> List[Task]:
        """
        translatedstatusfetchtasklist
        
        Args:
            status: taskstatus
            
        Returns:
            tasklist
        """
        return self.find_by(status=status)
    
    def get_by_type(self, task_type: TaskType) -> List[Task]:
        """
        translatedtasktranslatedfetchtasklist
        
        Args:
            task_type: tasktranslated
            
        Returns:
            tasklist
        """
        return self.find_by(task_type=task_type)
    
    def get_by_project_and_status(self, project_id: str, status: TaskStatus) -> List[Task]:
        """
        translatedprojectAndstatusfetchtasklist
        
        Args:
            project_id: projectID
            status: taskstatus
            
        Returns:
            tasklist
        """
        return self.find_by(project_id=project_id, status=status)
    
    def get_by_project_and_type(self, project_id: str, task_type: TaskType) -> List[Task]:
        """
        translatedprojectAndtasktranslatedfetchtasklist
        
        Args:
            project_id: projectID
            task_type: tasktranslated
            
        Returns:
            tasklist
        """
        return self.find_by(project_id=project_id, task_type=task_type)
    
    def get_pending_tasks(self) -> List[Task]:
        """
        fetchtranslatedprocess'stask
        
        Returns:
            translatedprocesstasklist
        """
        return self.find_by(status=TaskStatus.PtranslatedDING)
    
    def get_running_tasks(self) -> List[Task]:
        """
        fetchtranslatedintranslated'stask
        
        Returns:
            translatedintranslated'stasklist
        """
        return self.find_by(status=TaskStatus.RUNNING)
    
    def get_completed_tasks(self) -> List[Task]:
        """
        fetchcompleted'stask
        
        Returns:
            completed'stasklist
        """
        return self.find_by(status=TaskStatus.COMPLETED)
    
    def get_failed_tasks(self) -> List[Task]:
        """
        fetchfailed'stask
        
        Returns:
            failed'stasklist
        """
        return self.find_by(status=TaskStatus.FAILED)
    
    def get_tasks_by_step(self, project_id: str, step: int) -> List[Task]:
        """
        translatedprocessstepfetchtask
        
        Args:
            project_id: projectID
            step: processstep
            
        Returns:
            tasklist
        """
        return self.find_by(project_id=project_id, step=step)
    
    def get_next_pending_task(self) -> Optional[Task]:
        """
        fetchtranslatedone translatedprocesstask
        
        Returns:
            translatedone translatedprocesstaskorNone
        """
        return self.db.query(self.model).filter(
            self.model.status == TaskStatus.PtranslatedDING
        ).order_by(asc(self.model.created_at)).first()
    
    def get_tasks_by_priority(self, priority: int) -> List[Task]:
        """
        translatedfetchtask
        
        Args:
            priority: translated
            
        Returns:
            tasklist
        """
        return self.find_by(priority=priority)
    
    def update_task_status(self, task_id: str, status: TaskStatus) -> Optional[Task]:
        """
        updatetaskstatus
        
        Args:
            task_id: taskID
            status: translatedstatus
            
        Returns:
            updatetranslated'stasktranslatedorNone
        """
        return self.update(task_id, status=status)
    
    def update_task_progress(self, task_id: str, progress: float) -> Optional[Task]:
        """
        updatetaskprogress
        
        Args:
            task_id: taskID
            progress: progresstranslated
            
        Returns:
            updatetranslated'stasktranslatedorNone
        """
        return self.update(task_id, progress=progress)
    
    def update_task_result(self, task_id: str, result: dict) -> Optional[Task]:
        """
        updatetasktranslated
        
        Args:
            task_id: taskID
            result: tasktranslated
            
        Returns:
            updatetranslated'stasktranslatedorNone
        """
        return self.update(task_id, result=result)
    
    def update_task_error(self, task_id: str, error_message: str) -> Optional[Task]:
        """
        updatetaskerrorinfo
        
        Args:
            task_id: taskID
            error_message: errorinfo
            
        Returns:
            updatetranslated'stasktranslatedorNone
        """
        return self.update(task_id, error_message=error_message, status=TaskStatus.FAILED)
    
    def get_tasks_statistics(self, project_id: str = None) -> dict:
        """
        fetchtasktranslatedinfo
        
        Args:
            project_id: projectID，iftranslatedNonetranslatedproject
            
        Returns:
            translatedinfotranslated
        """
        query = self.db.query(self.model)
        if project_id:
            query = query.filter(self.model.project_id == project_id)
        
        total_tasks = query.count()
        pending_tasks = query.filter(self.model.status == TaskStatus.PtranslatedDING).count()
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
        fetchtranslated'stask
        
        Args:
            limit: returntranslated
            
        Returns:
            translated'stasklist
        """
        return self.db.query(self.model).order_by(
            desc(self.model.created_at)
        ).limit(limit).all()
    
    def get_tasks_by_date_range(self, start_date, end_date, project_id: str = None) -> List[Task]:
        """
        translatedfetchtask
        
        Args:
            start_date: translated
            end_date: translated
            project_id: projectID，iftranslatedNonetranslatedproject
            
        Returns:
            tasklist
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
        fetchtranslated'stask
        
        Args:
            max_duration_hours: translatedRuntimetranslated（translated）
            
        Returns:
            translated'stasklist
        """
        from datetime import datetime, timedelta
        cutoff_time = datetime.utcnow() - timedelta(hours=max_duration_hours)
        
        return self.db.query(self.model).filter(
            self.model.status == TaskStatus.RUNNING,
            self.model.started_at <= cutoff_time
        ).all()
    
    def cleanup_old_tasks(self, days: int = 30) -> int:
        """
        cleantranslatedtask，Packagetranslatedstatus'stask
        
        Args:
            days: translated
            
        Returns:
            delete'stasktranslated
        """
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        long_running_cutoff = datetime.utcnow() - timedelta(hours=24)
        
        total_deleted = 0
        
        try:
            # 1. cleantranslated'scompleted/failedtask
            completed_tasks = self.db.query(self.model).filter(
                self.model.created_at < cutoff_date,
                self.model.status.in_([TaskStatus.COMPLETED, TaskStatus.FAILED])
            ).delete(synchronize_session=False)
            
            total_deleted += completed_tasks
            logger.info(f"cleantranslated {completed_tasks}  translated'scompleted/failedtask")
            
            # 2. fixedtranslated'stranslatedtask
            long_running_tasks = self.db.query(self.model).filter(
                self.model.status == TaskStatus.RUNNING,
                self.model.created_at < long_running_cutoff
            ).all()
            
            fixed_count = 0
            for task in long_running_tasks:
                task.status = TaskStatus.FAILED
                task.error_message = "tasktranslated，translatedfailed"
                task.updated_at = datetime.utcnow()
                fixed_count += 1
                logger.info(f"fixedtranslatedtask: {task.id}")
            
            if fixed_count > 0:
                self.db.commit()
                logger.info(f"fixedtranslated {fixed_count}  translated'stask")
            
            # 3. cleantranslated'stask（translatedproject'stask）
            from ..models.project import Project
            all_project_ids = {p.id for p in self.db.query(Project).all()}
            orphaned_tasks = self.db.query(self.model).filter(
                ~self.model.project_id.in_(all_project_ids)
            ).all()
            
            orphaned_count = 0
            for task in orphaned_tasks:
                self.db.delete(task)
                orphaned_count += 1
                logger.info(f"cleantranslatedtask: {task.id}")
            
            if orphaned_count > 0:
                self.db.commit()
                logger.info(f"cleantranslated {orphaned_count}  translatedtask")
            
            return total_deleted + fixed_count + orphaned_count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"cleantaskfailed: {e}")
            raise