"""
clipmodel
translatedvideoclip'stranslatedinfoAndstatus
"""

import enum
from typing import Optional
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class ClipStatus(str, enum.Enum):
    """clipstatustranslated"""
    PtranslatedDING = "pending"           # translatedprocess
    PROCESSING = "processing"     # processing
    COMPLETED = "completed"       # completed
    FAILED = "failed"            # failed

class Clip(BaseModel):
    """clipmodel"""
    
    __tablename__ = "clips"
    
    # translatedinfo
    title = Column(
        String(255), 
        nullable=False, 
        comment="cliptranslated"
    )
    description = Column(
        Text, 
        nullable=True, 
        comment="cliptranslated"
    )
    
    # statusinfo
    status = Column(
        Enum(ClipStatus), 
        default=ClipStatus.PtranslatedDING,
        nullable=False,
        comment="clipstatus"
    )
    
    # translatedinfo
    start_time = Column(
        Integer, 
        nullable=False, 
        comment="translated（seconds）"
    )
    end_time = Column(
        Integer, 
        nullable=False, 
        comment="translated（seconds）"
    )
    duration = Column(
        Integer, 
        nullable=False, 
        comment="cliptranslated（seconds）"
    )
    
    # translatedinfo
    score = Column(
        Float, 
        nullable=True, 
        comment="cliptranslated"
    )
    recommendation_reason = Column(
        Text, 
        nullable=True, 
        comment="recommendtranslated"
    )
    
    # fileinfo
    video_path = Column(
        String(500), 
        nullable=True, 
        comment="clipvideofile path"
    )
    thumbnail_path = Column(
        String(500), 
        nullable=True, 
        comment="translatedfile path"
    )
    
    # processinfo
    processing_step = Column(
        Integer, 
        nullable=True, 
        comment="processstep（1-6）"
    )
    
    # translatedAndtranslated
    tags = Column(
        JSON, 
        nullable=True, 
        comment="cliptranslated"
    )
    clip_metadata = Column(
        JSON, 
        nullable=True, 
        comment="cliptranslated（translated，translatedinfileSystem）"
    )
    
    # addtranslated
    @property
    def metadata_file_path(self) -> Optional[str]:
        """fetchtranslatedfile path"""
        if self.clip_metadata and 'metadata_file' in self.clip_metadata:
            return self.clip_metadata['metadata_file']
        return None
    
    @property
    def has_full_content(self) -> bool:
        """Istranslatedfile"""
        return self.metadata_file_path is not None
    
    # translated
    project_id = Column(
        String(36), 
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        comment="translatedprojectID"
    )
    
    # translated
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
        """Istranslatedinprocess"""
        return self.status == ClipStatus.PROCESSING
    
    @property
    def is_completed(self):
        """Istranslatedcompleted"""
        return self.status == ClipStatus.COMPLETED
    
    @property
    def has_error(self):
        """Istranslatederror"""
        return self.status == ClipStatus.FAILED
    
    def get_time_range(self) -> str:
        """fetchtranslated"""
        try:
            start_time = int(self.start_time) if self.start_time else 0
            end_time = int(self.end_time) if self.end_time else 0
            start_min, start_sec = divmod(start_time, 60)
            end_min, end_sec = divmod(end_time, 60)
            return f"{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}"
        except (TypeError, ValueError):
            return "00:00 - 00:00"
    
    def calculate_duration(self):
        """translatedcliptranslated"""
        self.duration = self.end_time - self.start_time
        return self.duration