"""
BENSchema
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Union
from uuid import UUID
from datetime import datetime


class BilibiliAccountCreate(BaseModel):
    """createBENaccount"""
    username: str = Field(default="qr_login", description="userEN")
    password: str = Field(default="", description="EN")
    nickname: Optional[str] = Field(None, description="EN")
    cookie_content: str = Field(..., description="cookiefileEN")


class BilibiliAccountResponse(BaseModel):
    """BENaccountresponse"""
    id: Union[int, str]  # ENIntegerENUUID
    username: str
    nickname: Optional[str]
    status: str
    is_default: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class QRLoginRequest(BaseModel):
    """ENloginrequest"""
    nickname: Optional[str] = Field(None, description="EN")


class QRLoginResponse(BaseModel):
    """ENloginresponse"""
    session_id: str
    status: str
    message: str


class UploadRequest(BaseModel):
    """ENrequest"""
    clip_ids: List[str] = Field(..., description="ENclipIDEN")
    account_id: Union[int, str] = Field(..., description="useENaccountID")
    title: str = Field(..., description="title")
    description: str = Field(..., description="description")
    tags: List[str] = Field(default=[], description="tagsEN")
    partition_id: int = Field(..., description="ENID")
    sub_partition_id: Optional[int] = Field(None, description="ENID（EN）")


class UploadRecordResponse(BaseModel):
    """ENresponse"""
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
    
    # EN
    account_username: Optional[str] = None
    account_nickname: Optional[str] = None
    project_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class UploadStatusResponse(BaseModel):
    """ENstatusresponse"""
    id: UUID
    status: str
    bvid: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
