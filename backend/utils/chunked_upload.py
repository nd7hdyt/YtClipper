"""
ENuploadEN
ENfileENuploadEN
"""

import os
import hashlib
import shutil
import asyncio
import aiofiles
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class UploadStatus(Enum):
    """uploadstatus"""
    PENDING = "pending"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ChunkInfo:
    """EN"""
    chunk_number: int
    chunk_size: int
    total_chunks: int
    file_hash: str
    chunk_hash: str
    upload_id: str
    created_at: datetime
    status: UploadStatus = UploadStatus.PENDING


@dataclass
class UploadSession:
    """uploadEN"""
    upload_id: str
    filename: str
    file_size: int
    chunk_size: int
    total_chunks: int
    file_hash: str
    created_at: datetime
    status: UploadStatus = UploadStatus.PENDING
    uploaded_chunks: List[int] = None
    temp_dir: str = None
    
    def __post_init__(self):
        if self.uploaded_chunks is None:
            self.uploaded_chunks = []
        if self.temp_dir is None:
            self.temp_dir = f"/tmp/uploads/{self.upload_id}"


class ChunkedUploadManager:
    """ENuploadEN"""
    
    def __init__(self, base_dir: str = "/tmp/uploads", max_file_size: int = 2 * 1024 * 1024 * 1024):
        self.base_dir = Path(base_dir)
        self.max_file_size = max_file_size
        self.active_sessions: Dict[str, UploadSession] = {}
        self.chunk_info_cache: Dict[str, List[ChunkInfo]] = {}
        
        # ENdirectoryEN
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_upload_id(self, filename: str, file_size: int) -> str:
        """generateuploadID"""
        timestamp = datetime.now().isoformat()
        content = f"{filename}_{file_size}_{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """ENfileEN"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _calculate_chunk_hash(self, chunk_data: bytes) -> str:
        """EN"""
        return hashlib.md5(chunk_data).hexdigest()
    
    def _validate_file_size(self, file_size: int) -> bool:
        """validatefileEN"""
        return file_size <= self.max_file_size
    
    def _validate_file_type(self, filename: str) -> bool:
        """validatefileEN"""
        allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.srt', '.vtt', '.ass', '.ssa']
        return any(filename.lower().endswith(ext) for ext in allowed_extensions)
    
    async def create_upload_session(
        self, 
        filename: str, 
        file_size: int, 
        file_hash: str,
        chunk_size: int = 2 * 1024 * 1024  # 2MB
    ) -> UploadSession:
        """createuploadEN"""
        
        # validatefileEN
        if not self._validate_file_size(file_size):
            raise ValueError(f"fileEN: {file_size} > {self.max_file_size}")
        
        # validatefileEN
        if not self._validate_file_type(filename):
            raise ValueError(f"ENfileEN: {filename}")
        
        # generateuploadID
        upload_id = self._generate_upload_id(filename, file_size)
        
        # EN
        total_chunks = (file_size + chunk_size - 1) // chunk_size
        
        # createuploadEN
        session = UploadSession(
            upload_id=upload_id,
            filename=filename,
            file_size=file_size,
            chunk_size=chunk_size,
            total_chunks=total_chunks,
            file_hash=file_hash,
            created_at=datetime.now()
        )
        
        # createENdirectory
        session.temp_dir = str(self.base_dir / upload_id)
        Path(session.temp_dir).mkdir(parents=True, exist_ok=True)
        
        # saveEN
        self.active_sessions[upload_id] = session
        
        logger.info(f"createuploadEN: {upload_id}, file: {filename}, EN: {file_size}, EN: {total_chunks}")
        
        return session
    
    async def upload_chunk(
        self, 
        upload_id: str, 
        chunk_number: int, 
        chunk_data: bytes,
        chunk_hash: str
    ) -> bool:
        """uploadEN"""
        
        # fetchuploadEN
        session = self.active_sessions.get(upload_id)
        if not session:
            raise ValueError(f"uploadENdoes not exist: {upload_id}")
        
        # validateEN
        if chunk_number < 0 or chunk_number >= session.total_chunks:
            raise ValueError(f"EN: {chunk_number}")
        
        # validateEN
        expected_size = session.chunk_size
        if chunk_number == session.total_chunks - 1:  # EN
            expected_size = session.file_size - (session.total_chunks - 1) * session.chunk_size
        
        if len(chunk_data) != expected_size:
            raise ValueError(f"EN: EN {expected_size}, EN {len(chunk_data)}")
        
        # validateEN
        calculated_hash = self._calculate_chunk_hash(chunk_data)
        if calculated_hash != chunk_hash:
            raise ValueError(f"EN: EN {chunk_hash}, EN {calculated_hash}")
        
        # saveEN
        chunk_path = Path(session.temp_dir) / f"chunk_{chunk_number:06d}"
        
        async with aiofiles.open(chunk_path, 'wb') as f:
            await f.write(chunk_data)
        
        # updateENstatus
        if chunk_number not in session.uploaded_chunks:
            session.uploaded_chunks.append(chunk_number)
        
        # checkENallENupload
        if len(session.uploaded_chunks) == session.total_chunks:
            session.status = UploadStatus.COMPLETED
        
        logger.info(f"uploadENsucceeded: {upload_id}, EN: {chunk_number}, progress: {len(session.uploaded_chunks)}/{session.total_chunks}")
        
        return True
    
    async def merge_chunks(self, upload_id: str, output_path: str) -> bool:
        """EN"""
        
        # fetchuploadEN
        session = self.active_sessions.get(upload_id)
        if not session:
            raise ValueError(f"uploadENdoes not exist: {upload_id}")
        
        # checkENallENupload
        if len(session.uploaded_chunks) != session.total_chunks:
            raise ValueError(f"ENuploadEN: {len(session.uploaded_chunks)}/{session.total_chunks}")
        
        # ENdirectoryEN
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # EN
        logger.info(f"startEN: {upload_id}")
        
        with open(output_path, 'wb') as output_file:
            for chunk_number in range(session.total_chunks):
                chunk_path = Path(session.temp_dir) / f"chunk_{chunk_number:06d}"
                
                if not chunk_path.exists():
                    raise FileNotFoundError(f"ENfiledoes not exist: {chunk_path}")
                
                with open(chunk_path, 'rb') as chunk_file:
                    shutil.copyfileobj(chunk_file, output_file)
        
        # validateENfile
        if output_path.stat().st_size != session.file_size:
            raise ValueError(f"ENfileEN: EN {session.file_size}, EN {output_path.stat().st_size}")
        
        # validatefileEN
        merged_hash = self._calculate_file_hash(str(output_path))
        if merged_hash != session.file_hash:
            raise ValueError(f"ENfileEN: EN {session.file_hash}, EN {merged_hash}")
        
        logger.info(f"EN: {upload_id}, EN: {output_path}")
        
        return True
    
    async def cleanup_session(self, upload_id: str) -> bool:
        """ENuploadEN"""
        
        # fetchuploadEN
        session = self.active_sessions.get(upload_id)
        if not session:
            return False
        
        # deleteENdirectory
        temp_dir = Path(session.temp_dir)
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        
        # EN
        del self.active_sessions[upload_id]
        
        logger.info(f"ENuploadEN: {upload_id}")
        
        return True
    
    def get_upload_progress(self, upload_id: str) -> Dict[str, Any]:
        """fetchuploadprogress"""
        
        session = self.active_sessions.get(upload_id)
        if not session:
            return {"error": "uploadENdoes not exist"}
        
        progress = len(session.uploaded_chunks) / session.total_chunks * 100
        
        return {
            "upload_id": upload_id,
            "filename": session.filename,
            "file_size": session.file_size,
            "total_chunks": session.total_chunks,
            "uploaded_chunks": len(session.uploaded_chunks),
            "progress": round(progress, 2),
            "status": session.status.value,
            "created_at": session.created_at.isoformat()
        }
    
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """fetchallEN"""
        
        sessions = []
        for session in self.active_sessions.values():
            progress = len(session.uploaded_chunks) / session.total_chunks * 100
            sessions.append({
                "upload_id": session.upload_id,
                "filename": session.filename,
                "file_size": session.file_size,
                "total_chunks": session.total_chunks,
                "uploaded_chunks": len(session.uploaded_chunks),
                "progress": round(progress, 2),
                "status": session.status.value,
                "created_at": session.created_at.isoformat()
            })
        
        return sessions
    
    async def cancel_upload(self, upload_id: str) -> bool:
        """cancelupload"""
        
        session = self.active_sessions.get(upload_id)
        if not session:
            return False
        
        # updatestatus
        session.status = UploadStatus.CANCELLED
        
        # ENfile
        await self.cleanup_session(upload_id)
        
        logger.info(f"cancelupload: {upload_id}")
        
        return True
    
    def cleanup_expired_sessions(self, max_age_hours: int = 24) -> int:
        """EN"""
        
        from datetime import timedelta
        
        expired_sessions = []
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        for upload_id, session in self.active_sessions.items():
            if session.created_at < cutoff_time:
                expired_sessions.append(upload_id)
        
        # EN
        for upload_id in expired_sessions:
            asyncio.create_task(self.cleanup_session(upload_id))
        
        logger.info(f"EN: {len(expired_sessions)} EN")
        
        return len(expired_sessions)


# ENuploadEN
chunked_upload_manager = ChunkedUploadManager()
