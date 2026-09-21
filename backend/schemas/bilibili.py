"""
BsitetranslatedSchema
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Union
from uuid import UUID
from datetime import datetime


class BilibiliAccountCreate(BaseModel):
    """createBsiteAccount"""
    username: str = Field(default="qr_login", description="usertranslated")
    password: str = Field(default="", description="translated")
    nickname: Optional[str] = Field(None, description="translated")
    cookie_content: str = Field(..., description="cookiefiletranslated")


class BilibiliAccountResponse(BaseModel):
    """BsiteAccounttranslated"""
    id: Union[int, str]  # supportIntegerAndUUID
    username: str
    nickname: Optional[str]
    status: str
    is_default: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class QRLoginRequest(BaseModel):
    """translated"""
    nickname: Optional[str] = Field(None, description="translated")


class QRLoginResponse(BaseModel):
    """translated"""
    session_id: str
    status: str
    message: str


class UploadRequest(BaseModel):
    """translated"""
    clip_ids: List[str] = Field(..., description="translated'sclipIDlist")
    account_id: Union[int, str] = Field(..., description="use'sAccountID")
    title: str = Field(..., description="translated")
    description: str = Field(..., description="translated")
    tags: List[str] = Field(default=[], description="translatedlist")
    partition_id: int = Field(..., description="translatedID")
    sub_partition_id: Optional[int] = Field(None, description="translatedID（canSelect）")


class UploadRecordResponse(BaseModel):
    """translated"""
    id: Union[int, str]
    task_id: Optional[str]
    project_id: Optional[UUID]
    account_id: Union[int, str]
    clip_id: str
    title: str
    description: Optional[str]
    tags: Optional[str]
    partition_id: int
    video_path: Optional[str]
    bv_id: Optional[str]
    av_id: Optional[str]
    status: str
    error_message: Optional[str]
    progress: int
    file_size: Optional[int]
    upload_duration: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    # translatedinfo
    account_username: Optional[str] = None
    account_nickname: Optional[str] = None
    project_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class UploadStatusResponse(BaseModel):
    """translatedstatustranslated"""
    id: UUID
    status: str
    bvid: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
