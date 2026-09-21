"""
clipEN
ENvideoclipENstatus
"""

import enum
from typing import Optional
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class ClipStatus(str, enum.Enum):
    """clipstatusEN"""
    PENDING = "pending"           # ENprocessing
    PROCESSING = "processing"     # processing
    COMPLETED = "completed"       # completed
    FAILED = "failed"            # failed

class Clip(BaseModel):
    """clipEN"""
    
    __tablename__ = "clips"
    
    # EN
    title = Column(
        String(255), 
        nullable=False, 
        comment="cliptitle"
    )
    description = Column(
        Text, 
        nullable=True, 
        comment="clipdescription"
    )
    
    # statusEN
    status = Column(
        Enum(ClipStatus), 
        default=ClipStatus.PENDING,
        nullable=False,
        comment="clipstatus"
    )
    
    # timeEN
    start_time = Column(
        Integer, 
        nullable=False, 
        comment="starttime（EN）"
    )
    end_time = Column(
        Integer, 
        nullable=False, 
        comment="endtime（EN）"
    )
    duration = Column(
        Integer, 
        nullable=False, 
        comment="clipduration（EN）"
    )
    
    # scoringEN
    score = Column(
        Float, 
        nullable=True, 
        comment="clipscoring"
    )
    recommendation_reason = Column(
        Text, 
        nullable=True, 
        comment="EN"
    )
    
    # fileEN
    video_path = Column(
        String(500), 
        nullable=True, 
        comment="clipvideofilepath"
    )
    thumbnail_path = Column(
        String(500), 
        nullable=True, 
        comment="ENfilepath"
    )
    
    # processingEN
    processing_step = Column(
        Integer, 
        nullable=True, 
        comment="processingEN（1-6）"
    )
    
    # tagsEN
    tags = Column(
        JSON, 
        nullable=True, 
        comment="cliptags"
    )
    clip_metadata = Column(
        JSON, 
        nullable=True, 
        comment="clipEN（EN，ENfilesystem）"
    )
    
    # EN
    @property
    def metadata_file_path(self) -> Optional[str]:
        """fetchENfilepath"""
        if self.clip_metadata and 'metadata_file' in self.clip_metadata:
            return self.clip_metadata['metadata_file']
        return None
    
    @property
    def has_full_content(self) -> bool:
        """ENfile"""
        return self.metadata_file_path is not None
    
    # EN
    project_id = Column(
        String(36), 
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        comment="ENprojectID"
    )
    
    # EN
    project = relationship(
        "Project", 
        back_populates="clips"
    )
    collections = relationship(
        "Collection", 
        secondary="clip_collection",
        back_populates="clips"
    )
    
    def __repr__(self):
        return f"<Clip(id={self.id}, title='{self.title}', duration={self.duration}s)>"
    
    @property
    def is_processing(self):
        """ENcurrentlyprocessing"""
        return self.status == ClipStatus.PROCESSING
    
    @property
    def is_completed(self):
        """ENcompleted"""
        return self.status == ClipStatus.COMPLETED
    
    @property
    def has_error(self):
        """ENerror"""
        return self.status == ClipStatus.FAILED
    
    def get_time_range(self) -> str:
        """fetchtimeEN"""
        try:
            start_time = int(self.start_time) if self.start_time else 0
            end_time = int(self.end_time) if self.end_time else 0
            start_min, start_sec = divmod(start_time, 60)
            end_min, end_sec = divmod(end_time, 60)
            return f"{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}"
        except (TypeError, ValueError):
            return "00:00 - 00:00"
    
    def calculate_duration(self):
        """ENclipduration"""
        self.duration = self.end_time - self.start_time
        return self.duration