"""
Bsitetranslateddatabasemodel
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .base import Base


class BilibiliAccount(Base):
    """BsiteAccounttranslated"""
    __tablename__ = "bilibili_accounts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    nickname = Column(String(100))
    cookies = Column(Text)  # translated'scookies
    status = Column(String(20), default="active")  # active/inactive/banned
    is_default = Column(Boolean, default=False)
    
    # Accountinfo
    uid = Column(String(50))  # BsiteuserID
    level = Column(Integer, default=0)  # useretc.translated
    is_vip = Column(Boolean, default=False)  # IstranslatedVIP
    can_upload = Column(Boolean, default=True)  # Istranslatedcantranslated
    
    # usetranslated
    last_used_at = Column(DateTime)  # translatedusetranslated
    upload_count = Column(Integer, default=0)  # Uploadtranslated
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # translated
    upload_records = relationship("BilibiliUploadRecord", back_populates="account")


class BilibiliUploadRecord(Base):
    """Bsitetranslated"""
    __tablename__ = "bilibili_upload_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(100), unique=True, index=True)  # Task QueueID
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    account_id = Column(Integer, ForeignKey("bilibili_accounts.id"), nullable=False)
    clip_id = Column(String(255))  # clipID
    
    # translated
    title = Column(String(200), nullable=False)
    description = Column(Text)
    tags = Column(Text)  # JSONtranslated
    partition_id = Column(Integer, default=17)  # translatedID，defaulttranslated
    video_path = Column(String(500))  # videofile path
    
    # translated
    bv_id = Column(String(20))  # translatedsucceededtranslated'sBVtranslated
    av_id = Column(String(20))  # AVtranslated
    status = Column(String(20), default="pending")  # pending/processing/completed/failed
    error_message = Column(Text)  # errorinfo
    
    # UploadprogressAndtranslated
    progress = Column(Integer, default=0)  # Uploadprogress 0-100
    file_size = Column(Integer)  # filetranslated（translated）
    upload_duration = Column(Integer)  # Uploadtranslated（seconds）
    
    # translated
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # translated
    account = relationship("BilibiliAccount", back_populates="upload_records")

# translated，translated'stranslated
UploadRecord = BilibiliUploadRecord

