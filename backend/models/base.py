"""
EN
ENallEN
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

# createMetaDataEN，EN
metadata = MetaData()

# createEN
Base = declarative_base(metadata=metadata)

def get_utc_now():
    """fetchcurrentUTCtime"""
    return datetime.now(timezone.utc)

class TimestampMixin:
    """timeEN，ENcreateENupdatetime"""
    
    created_at = Column(
        DateTime(timezone=True), 
        default=get_utc_now, 
        nullable=False,
        comment="createtime"
    )
    updated_at = Column(
        DateTime(timezone=True), 
        default=get_utc_now, 
        onupdate=get_utc_now, 
        nullable=False,
        comment="updatetime"
    )

def generate_uuid():
    """generateUUIDEN"""
    return str(uuid.uuid4())

class BaseModel(Base, TimestampMixin):
    """EN，EN"""
    
    __abstract__ = True
    
    id = Column(
        String(36), 
        primary_key=True, 
        default=generate_uuid,
        index=True,
        comment="ENID"
    )
    
    def __repr__(self):
        """EN"""
        return f"<{self.__class__.__name__}(id={self.id})>"
    
    def to_dict(self):
        """EN"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update_from_dict(self, data: dict):
        """ENupdateEN"""
        for key, value in data.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
        return self 