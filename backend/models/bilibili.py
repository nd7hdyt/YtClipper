"""
BENdatabaseEN
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .base import Base


class BilibiliAccount(Base):
    """BENaccountEN"""
    __tablename__ = "bilibili_accounts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    nickname = Column(String(100))
    cookies = Column(Text)  # ENcookies
    status = Column(String(20), default="active")  # active/inactive/banned
    is_default = Column(Boolean, default=False)
    
    # accountEN
    uid = Column(String(50))  # BENuserID
    level = Column(Integer, default=0)  # userEN
    is_vip = Column(Boolean, default=False)  # ENVIP
    can_upload = Column(Boolean, default=True)  # ENcanEN
    
    # useEN
    last_used_at = Column(DateTime)  # ENusetime
    upload_count = Column(Integer, default=0)  # uploadEN
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # EN
    upload_records = relationship("BilibiliUploadRecord", back_populates="account")


class BilibiliUploadRecord(Base):
    """BEN"""
    __tablename__ = "bilibili_upload_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(100), unique=True, index=True)  # taskqueueID
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    account_id = Column(Integer, ForeignKey("bilibili_accounts.id"), nullable=False)
    clip_id = Column(String(255))  # clipID
    
    # EN
    title = Column(String(200), nullable=False)
    description = Column(Text)
    tags = Column(Text)  # JSONEN
    partition_id = Column(Integer, default=17)  # ENID，EN
    video_path = Column(String(500))  # videofilepath
    
    # ENresult
    bv_id = Column(String(20))  # ENsucceededENBVEN
    av_id = Column(String(20))  # AVEN
    status = Column(String(20), default="pending")  # pending/processing/completed/failed
    error_message = Column(Text)  # errorEN
    
    # uploadprogressEN
    progress = Column(Integer, default=0)  # uploadprogress 0-100
    file_size = Column(Integer)  # fileEN（EN）
    upload_duration = Column(Integer)  # uploadEN（EN）
    
    # timeEN
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # EN
    account = relationship("BilibiliAccount", back_populates="upload_records")

# EN，EN
UploadRecord = BilibiliUploadRecord

