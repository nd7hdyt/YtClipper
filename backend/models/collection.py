"""
collectionmodel
translatedvideocollection'stranslatedinfoAndtranslated
"""

import enum
from typing import Optional, List
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, JSON, DateTime, Text, Table
from sqlalchemy.orm import relationship
from .base import BaseModel

class CollectionStatus(str, enum.Enum):
    """collectionstatustranslated"""
    CREATED = "created"           # translatedcreate
    PROCESSING = "processing"     # processing
    COMPLETED = "completed"       # completed
    ERROR = "error"              # error
    DELETED = "deleted"          # translateddelete

# clipAndcollection'smultitranslatedmultitranslated
clip_collection = Table(
    'clip_collection',
    BaseModel.metadata,
    Column('clip_id', String(36), ForeignKey('clips.id', ondelete='CASCADE'), primary_key=True),
    Column('collection_id', String(36), ForeignKey('collections.id', ondelete='CASCADE'), primary_key=True),
    Column('order_index', Integer, nullable=False, default=0, comment="incollectiontranslated'stranslated")
)

class Collection(BaseModel):
    """collectionmodel"""
    
    __tablename__ = "collections"
    
    # translatedinfo
    name = Column(
        String(255), 
        nullable=False, 
        comment="collectiontranslated"
    )
    description = Column(
        Text, 
        nullable=True, 
        comment="collectiontranslated"
    )
    
    # statusinfo
    status = Column(
        Enum(CollectionStatus), 
        default=CollectionStatus.CREATED,
        nullable=False,
        comment="collectionstatus"
    )
    
    # translatedinfo
    theme = Column(
        String(255), 
        nullable=True, 
        comment="collectiontranslated"
    )
    tags = Column(
        JSON, 
        nullable=True, 
        comment="collectiontranslated"
    )
    
    # translatedinfo
    total_duration = Column(
        Integer, 
        nullable=True, 
        comment="collectiontranslated（seconds）"
    )
    clips_count = Column(
        Integer, 
        default=0, 
        comment="cliptranslated"
    )
    
    # fileinfo
    video_path = Column(
        String(500), 
        nullable=True, 
        comment="collectionvideofile path"
    )
    thumbnail_path = Column(
        String(500), 
        nullable=True, 
        comment="collectiontranslatedpath"
    )
    
    # processinfo
    processing_result = Column(
        JSON, 
        nullable=True, 
        comment="processtranslated"
    )
    
    # exportinfo
    export_path = Column(
        String(500), 
        nullable=True, 
        comment="collectionexportfile path"
    )
    
    # translated
    collection_metadata = Column(
        JSON, 
        nullable=True, 
        comment="collectiontranslated（translated，translatedinfileSystem）"
    )
    
    # addtranslated
    @property
    def metadata_file_path(self) -> Optional[str]:
        """fetchtranslatedfile path"""
        if self.collection_metadata and 'metadata_file' in self.collection_metadata:
            return self.collection_metadata['metadata_file']
        return None
    
    @property
    def has_full_content(self) -> bool:
        """Istranslatedfile"""
        return self.metadata_file_path is not None
    
    @property
    def clip_ids(self) -> List[str]:
        """fetchclipIDlist"""
        if self.collection_metadata and 'clip_ids' in self.collection_metadata:
            return self.collection_metadata['clip_ids']
        return []
    
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
        back_populates="collections"
    )
    clips = relationship(
        "Clip", 
        secondary=clip_collection,
        back_populates="collections",
        lazy="dynamic"
    )
    
    def __repr__(self):
        return f"<Collection(id={self.id}, name='{self.name}', clips_count={self.clips_count})>"
    
    @property
    def is_processing(self):
        """Istranslatedinprocess"""
        return self.status == CollectionStatus.PROCESSING
    
    @property
    def is_completed(self):
        """Istranslatedcompleted"""
        return self.status == CollectionStatus.COMPLETED
    
    @property
    def has_error(self):
        """Istranslatederror"""
        return self.status == CollectionStatus.ERROR
    
    def add_clip(self, clip, order_index=None):
        """addcliptranslatedcollection"""
        if order_index is None:
            order_index = self.clips_count
        
        # usetranslatedaddclip
        stmt = clip_collection.insert().values(
            clip_id=clip.id,
            collection_id=self.id,
            order_index=order_index
        )
        # thistranslatedindatabasetranslated
        self.clips_count += 1
        return stmt
    
    def remove_clip(self, clip):
        """fromcollectiontranslatedclip"""
        stmt = clip_collection.delete().where(
            clip_collection.c.clip_id == clip.id,
            clip_collection.c.collection_id == self.id
        )
        current_count = int(self.clips_count) if self.clips_count else 0
        self.clips_count = max(0, current_count - 1)
        return stmt
    
    def calculate_total_duration(self):
        """translatedcollectiontranslated"""
        total = 0
        for clip in self.clips:
            if clip.duration:
                total += clip.duration
        self.total_duration = total
        return total