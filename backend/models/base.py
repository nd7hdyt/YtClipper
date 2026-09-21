"""
translatedmodeltranslated
Packageincludetranslatedmodel'stranslatedAndtranslated
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

# createMetaDatatranslated，ensuretranslated
metadata = MetaData()

# createtranslated
Base = declarative_base(metadata=metadata)

def get_utc_now():
    """fetchtranslatedUTCtranslated"""
    return datetime.now(timezone.utc)

class TimestampMixin:
    """translated，translatedmodeladdcreateAndupdatetranslated"""
    
    created_at = Column(
        DateTime(timezone=True), 
        default=get_utc_now, 
        nullable=False,
        comment="createtranslated"
    )
    updated_at = Column(
        DateTime(timezone=True), 
        default=get_utc_now, 
        onupdate=get_utc_now, 
        nullable=False,
        comment="updatetranslated"
    )

def generate_uuid():
    """translatedUUIDtranslated"""
    return str(uuid.uuid4())

class BaseModel(Base, TimestampMixin):
    """translatedmodeltranslated，Packageincludetranslatedusetranslated"""
    
    __abstract__ = True
    
    id = Column(
        String(36), 
        primary_key=True, 
        default=generate_uuid,
        index=True,
        comment="translatedID"
    )
    
    def __repr__(self):
        """model'stranslated"""
        return f"<{self.__class__.__name__}(id={self.id})>"
    
    def to_dict(self):
        """translated"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update_from_dict(self, data: dict):
        """fromtranslatedupdatemodel"""
        for key, value in data.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
        return self 