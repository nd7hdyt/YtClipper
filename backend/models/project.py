"""
projectmodel
translatedproject'stranslatedinfoAndstatus
"""

import enum
from typing import Optional
from sqlalchemy import Column, String, Text, JSON, Enum, Integer, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel

class ProjectStatus(str, enum.Enum):
    """projectstatustranslated"""
    PtranslatedDING = "pending"           # etc.translated
    PROCESSING = "processing"     # processing
    COMPLETED = "completed"       # completed
    FAILED = "failed"            # failed

class ProjectType(str, enum.Enum):
    """projecttranslated"""
    DEFAULT = "default"           # default
    KNOWLEDGE = "knowledge"       # translated
    BUSINESS = "business"         # providertranslated
    OPINION = "opinion"          # translated
    EXPERItranslatedCE = "experience"    # translated
    SPEECH = "speech"            # translated
    CONTtranslatedT_REVIEW = "content_review"  # translated
    translatedTERTAINMtranslatedT = "entertainment"    # translated

class Project(BaseModel):
    """projectmodel"""
    
    __tablename__ = "projects"
    
    # translatedinfo
    name = Column(
        String(255), 
        nullable=False, 
        comment="projecttranslated"
    )
    description = Column(
        Text, 
        nullable=True, 
        comment="projecttranslated"
    )
    
    # statusinfo
    status = Column(
        Enum(ProjectStatus), 
        default=ProjectStatus.PtranslatedDING,
        nullable=False,
        comment="projectstatus"
    )
    
    # projecttranslated
    project_type = Column(
        Enum(ProjectType), 
        default=ProjectType.DEFAULT,
        nullable=False,
        comment="projecttranslated"
    )
    video_path = Column(
        String(500), 
        nullable=True, 
        comment="videofile path"
    )
    subtitle_path = Column(
        String(500), 
        nullable=True, 
        comment="subtitlesfile path"
    )
    video_duration = Column(
        Integer, 
        nullable=True, 
        comment="videotranslated（seconds）"
    )
    thumbnail = Column(
        Text, 
        nullable=True, 
        comment="projecttranslated（base64translated）"
    )
    
    # processconfig
    processing_config = Column(
        JSON, 
        nullable=True, 
        comment="processconfigtranslated"
    )
    
    # translated
    project_metadata = Column(
        JSON, 
        nullable=True, 
        comment="projecttranslated（translated，translatedinfileSystem）"
    )
    
    # addtranslated
    @property
    def storage_initialized(self) -> bool:
        """translatedserviceIstranslated"""
        if self.project_metadata and 'storage_service_initialized' in self.project_metadata:
            return self.project_metadata['storage_service_initialized']
        return False
    
    @property
    def has_video_file(self) -> bool:
        """Istranslatedvideofile"""
        return self.video_path is not None
    
    @property
    def has_subtitle_file(self) -> bool:
        """Istranslatedsubtitlesfile"""
        return self.subtitle_path is not None
    
    # translated
    completed_at = Column(
        DateTime, 
        nullable=True, 
        comment="projecttranslated"
    )
    
    # translated
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
        """fetchcliptranslated"""
        return len(self.clips) if self.clips else 0
    
    @property
    def collections_count(self):
        """fetchcollectiontranslated"""
        return len(self.collections) if self.collections else 0
    
    @property
    def is_processing(self):
        """Istranslatedinprocess"""
        return self.status == ProjectStatus.PROCESSING
    
    @property
    def is_completed(self):
        """Istranslatedcompleted"""
        return self.status == ProjectStatus.COMPLETED
    
    @property
    def has_error(self):
        """Istranslatederror"""
        return self.status == ProjectStatus.FAILED