"""
taskEN
ENtaskENexecutestatus
"""

import enum
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from .base import BaseModel, TimestampMixin

class TaskStatus(str, enum.Enum):
    """taskstatusEN"""
    PENDING = "pending"           # EN
    RUNNING = "running"           # runEN
    COMPLETED = "completed"       # completed
    FAILED = "failed"            # failed
    CANCELLED = "cancelled"      # ENcancel

class TaskType(str, enum.Enum):
    """taskEN"""
    VIDEO_PROCESSING = "video_processing"    # videoprocessing
    CLIP_GENERATION = "clip_generation"      # clipgenerate
    COLLECTION_CREATION = "collection_creation"  # collectioncreate
    EXPORT = "export"                        # EN
    CLEANUP = "cleanup"                      # EN

class Task(BaseModel, TimestampMixin):
    """taskEN"""
    
    __tablename__ = "tasks"
    
    # EN
    name = Column(
        String(255), 
        nullable=False, 
        comment="taskEN"
    )
    description = Column(
        Text, 
        nullable=True, 
        comment="taskdescription"
    )
    
    # statusEN
    status = Column(
        Enum(TaskStatus), 
        default=TaskStatus.PENDING,
        nullable=False,
        comment="taskstatus"
    )
    task_type = Column(
        Enum(TaskType), 
        nullable=False,
        comment="taskEN"
    )
    
    # progressEN
    progress = Column(Float, default=0.0, comment="progressEN")
    current_step = Column(
        String(100), 
        nullable=True, 
        comment="currentEN"
    )
    total_steps = Column(
        Integer, 
        default=1,
        comment="EN"
    )
    priority = Column(
        Integer, 
        default=0,
        comment="taskEN"
    )
    
    # executeEN
    started_at = Column(
        DateTime, 
        nullable=True, 
        comment="starttime"
    )
    completed_at = Column(
        DateTime, 
        nullable=True, 
        comment="ENtime"
    )
    error_message = Column(
        Text, 
        nullable=True, 
        comment="errorEN"
    )
    
    # CelerytaskEN
    celery_task_id = Column(
        String(255), 
        nullable=True, 
        comment="CelerytaskID"
    )
    
    # configEN
    task_config = Column(
        JSON, 
        nullable=True, 
        comment="taskconfig"
    )
    result_data = Column(
        JSON, 
        nullable=True, 
        comment="resultEN"
    )
    task_metadata = Column(
        JSON, 
        nullable=True, 
        comment="taskEN"
    )
    
    # EN
    project_id = Column(
        String(36), 
        ForeignKey("projects.id"),
        nullable=False,
        comment="ENprojectID"
    )
    project = relationship(
        "Project", 
        back_populates="tasks"
    )
    
    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}', status={self.status})>"
    
    @property
    def is_running(self):
        """ENcurrentlyrun"""
        return self.status == TaskStatus.RUNNING
    
    @property
    def is_completed(self):
        """ENcompleted"""
        return self.status == TaskStatus.COMPLETED
    
    @property
    def has_error(self):
        """ENerror"""
        return self.status == TaskStatus.FAILED
    
    @property
    def duration(self):
        """taskENtime（EN）"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        elif self.started_at:
            return (datetime.utcnow() - self.started_at).total_seconds()
        return 0
    
    def start(self):
        """starttask"""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.utcnow()
        self.progress = 0.0
    
    def complete(self, result_data=None):
        """ENtask"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.progress = 100.0
        if result_data:
            self.result_data = result_data
    
    def fail(self, error_message):
        """taskfailed"""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.error_message = error_message
    
    def cancel(self):
        """canceltask"""
        self.status = TaskStatus.CANCELLED
        self.completed_at = datetime.utcnow()
    
    def update_progress(self, progress, current_step=None):
        """updateprogress"""
        self.progress = min(100.0, max(0.0, progress))
        if current_step:
            self.current_step = current_step
    
    def is_completed(self):
        """checkEN"""
        return self.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]
    
    def is_running(self):
        """checkENrunEN"""
        return self.status == TaskStatus.RUNNING
    
    def is_pending(self):
        """checkENprocessing"""
        return self.status == TaskStatus.PENDING
    
    def get_duration(self):
        """fetchtaskENtime"""
        if not self.started_at:
            return None
        
        end_time = self.completed_at or datetime.utcnow()
        return (end_time - self.started_at).total_seconds()
    
    def to_dict(self):
        """EN"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "task_type": self.task_type,
            "status": self.status,
            "project_id": self.project_id,
            "step": self.current_step,
            "total_steps": self.total_steps,
            "progress": self.progress,
            "result": self.result_data,
            "error_message": self.error_message,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "config": self.task_config,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }