"""
projectEN
ENprojectENstatus
"""

import enum
from typing import Optional
from sqlalchemy import Column, String, Text, JSON, Enum, Integer, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel

class ProjectStatus(str, enum.Enum):
    """projectstatusEN"""
    PENDING = "pending"           # EN
    PROCESSING = "processing"     # processing
    COMPLETED = "completed"       # completed
    FAILED = "failed"            # failed

class ProjectType(str, enum.Enum):
    """projectEN"""
    DEFAULT = "default"           # EN
    KNOWLEDGE = "knowledge"       # EN
    BUSINESS = "business"         # EN
    OPINION = "opinion"          # EN
    EXPERIENCE = "experience"    # EN
    SPEECH = "speech"            # EN
    CONTENT_REVIEW = "content_review"  # EN
    ENTERTAINMENT = "entertainment"    # EN

class Project(BaseModel):
    """projectEN"""
    
    __tablename__ = "projects"
    
    # EN
    name = Column(
        String(255), 
        nullable=False, 
        comment="projectEN"
    )
    description = Column(
        Text, 
        nullable=True, 
        comment="projectdescription"
    )
    
    # statusEN
    status = Column(
        Enum(ProjectStatus), 
        default=ProjectStatus.PENDING,
        nullable=False,
        comment="projectstatus"
    )
    
    # projectEN
    project_type = Column(
        Enum(ProjectType), 
        default=ProjectType.DEFAULT,
        nullable=False,
        comment="projectEN"
    )
    video_path = Column(
        String(500), 
        nullable=True, 
        comment="videofilepath"
    )
    subtitle_path = Column(
        String(500), 
        nullable=True, 
        comment="subtitlesfilepath"
    )
    video_duration = Column(
        Integer, 
        nullable=True, 
        comment="videoduration（EN）"
    )
    thumbnail = Column(
        Text, 
        nullable=True, 
        comment="projectEN（base64EN）"
    )
    
    # processingconfig
    processing_config = Column(
        JSON, 
        nullable=True, 
        comment="processingconfigparameters"
    )
    
    # EN
    project_metadata = Column(
        JSON, 
        nullable=True, 
        comment="projectEN（EN，ENfilesystem）"
    )
    
    # EN
    @property
    def storage_initialized(self) -> bool:
        """ENserviceENinitialize"""
        if self.project_metadata and 'storage_service_initialized' in self.project_metadata:
            return self.project_metadata['storage_service_initialized']
        return False
    
    @property
    def has_video_file(self) -> bool:
        """ENvideofile"""
        return self.video_path is not None
    
    @property
    def has_subtitle_file(self) -> bool:
        """ENsubtitlesfile"""
        return self.subtitle_path is not None
    
    # ENtime
    completed_at = Column(
        DateTime, 
        nullable=True, 
        comment="projectENtime"
    )
    
    # EN
    clips = relationship(
        "Clip", 
        back_populates="project",
        cascade="all, delete-orphan"
    )
    collections = relationship(
        "Collection", 
        back_populates="project",
        cascade="all, delete-orphan"
    )
    tasks = relationship(
        "Task", 
        back_populates="project",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status={self.status})>"
    
    @property
    def clips_count(self):
        """fetchclipEN"""
        return len(self.clips) if self.clips else 0
    
    @property
    def collections_count(self):
        """fetchcollectionEN"""
        return len(self.collections) if self.collections else 0
    
    @property
    def is_processing(self):
        """ENcurrentlyprocessing"""
        return self.status == ProjectStatus.PROCESSING
    
    @property
    def is_completed(self):
        """ENcompleted"""
        return self.status == ProjectStatus.COMPLETED
    
    @property
    def has_error(self):
        """ENerror"""
        return self.status == ProjectStatus.FAILED