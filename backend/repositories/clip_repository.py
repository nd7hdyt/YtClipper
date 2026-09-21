"""
clipRepository
ENclipEN
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from pathlib import Path
from .base import BaseRepository
from ..models.clip import Clip, ClipStatus

class ClipRepository(BaseRepository[Clip]):
    """clipRepositoryEN"""
    
    def __init__(self, db: Session):
        super().__init__(Clip, db)
    
    def get_by_project(self, project_id: str) -> List[Clip]:
        """
        fetchprojectENallclip
        
        Args:
            project_id: projectID
            
        Returns:
            clipEN
        """
        return self.find_by(project_id=project_id)
    
    def get_by_status(self, status: ClipStatus) -> List[Clip]:
        """
        ENstatusfetchclipEN
        
        Args:
            status: clipstatus
            
        Returns:
            clipEN
        """
        return self.find_by(status=status)
    
    def get_by_project_and_status(self, project_id: str, status: ClipStatus) -> List[Clip]:
        """
        ENprojectENstatusfetchclipEN
        
        Args:
            project_id: projectID
            status: clipstatus
            
        Returns:
            clipEN
        """
        return self.find_by(project_id=project_id, status=status)
    
    def get_high_score_clips(self, project_id: str, min_score: float = 0.7, limit: int = 10) -> List[Clip]:
        """
        fetchENclip
        
        Args:
            project_id: projectID
            min_score: ENscoring
            limit: returnEN
            
        Returns:
            ENclipEN
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.score >= min_score
        ).order_by(desc(self.model.score)).limit(limit).all()
    
    def get_clips_by_duration_range(self, project_id: str, min_duration: int, max_duration: int) -> List[Clip]:
        """
        ENdurationENfetchclip
        
        Args:
            project_id: projectID
            min_duration: ENduration（EN）
            max_duration: ENduration（EN）
            
        Returns:
            clipEN
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.duration >= min_duration,
            self.model.duration <= max_duration
        ).order_by(asc(self.model.start_time)).all()
    
    def get_clips_by_time_range(self, project_id: str, start_time: int, end_time: int) -> List[Clip]:
        """
        ENtimeENfetchclip
        
        Args:
            project_id: projectID
            start_time: starttime（EN）
            end_time: endtime（EN）
            
        Returns:
            clipEN
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.start_time >= start_time,
            self.model.end_time <= end_time
        ).order_by(asc(self.model.start_time)).all()
    
    def create_clip(self, clip_data: Dict[str, Any]) -> Clip:
        """createclipEN（EN）"""
        from ..services.storage_service import StorageService
        import uuid
        
        # generateclipID（ifEN）
        if "id" not in clip_data:
            clip_data["id"] = str(uuid.uuid4())
        
        # 1. saveclipfileENfilesystem
        storage_service = StorageService(clip_data["project_id"])
        video_path = storage_service.save_clip_file(clip_data, clip_data["id"])
        
        # 2. saveENfilesystem
        metadata_path = storage_service.save_metadata(clip_data, f"clip_{clip_data['id']}")
        
        # 3. saveENdatabase（ENpathEN）
        clip = Clip(
            id=clip_data["id"],
            project_id=clip_data["project_id"],
            title=clip_data["title"],
            description=clip_data.get("description"),
            start_time=clip_data["start_time"],
            end_time=clip_data["end_time"],
            duration=clip_data["duration"],
            score=clip_data.get("score"),
            video_path=video_path,  # ENpath
            clip_metadata={
                'metadata_file': metadata_path,  # ENfilepath
                'clip_id': clip_data["id"],
                'created_at': clip_data.get("created_at")
            }
        )
        
        self.db.add(clip)
        self.db.commit()
        return clip
    
    def get_clip_file(self, clip_id: str) -> Optional[Path]:
        """fetchclipfilepath"""
        clip = self.get_by_id(clip_id)
        if clip and clip.video_path:
            return Path(clip.video_path)
        return None
    
    def get_clip_content(self, clip_id: str) -> Optional[Dict[str, Any]]:
        """fetchclipEN"""
        clip = self.get_by_id(clip_id)
        if not clip:
            return None
        
        # ENfilesystemfetchEN
        if clip.clip_metadata and 'metadata_file' in clip.clip_metadata:
            from ..services.storage_service import StorageService
            storage_service = StorageService(clip.project_id)
            return storage_service.get_file_content(clip.clip_metadata['metadata_file'])
        
        return None
    
    def search_clips(self, project_id: str, keyword: str) -> List[Clip]:
        """
        ENclip
        
        Args:
            project_id: projectID
            keyword: EN
            
        Returns:
            ENclipEN
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            (self.model.title.contains(keyword) | 
             self.model.description.contains(keyword) |
             self.model.recommendation_reason.contains(keyword))
        ).all()
    
    def get_clips_statistics(self, project_id: str) -> dict:
        """
        fetchclipEN
        
        Args:
            project_id: projectID
            
        Returns:
            EN
        """
        total_clips = self.db.query(self.model).filter(
            self.model.project_id == project_id
        ).count()
        
        completed_clips = self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.status == ClipStatus.COMPLETED
        ).count()
        
        avg_score = self.db.query(func.avg(self.model.score)).filter(
            self.model.project_id == project_id,
            self.model.score.isnot(None)
        ).scalar()
        
        total_duration = self.db.query(func.sum(self.model.duration)).filter(
            self.model.project_id == project_id
        ).scalar()
        
        return {
            "total": total_clips,
            "completed": completed_clips,
            "avg_score": float(avg_score) if avg_score else 0.0,
            "total_duration": int(total_duration) if total_duration else 0,
            "completion_rate": (completed_clips / total_clips * 100) if total_clips > 0 else 0
        }
    
    def update_clip_status(self, clip_id: str, status: ClipStatus) -> Optional[Clip]:
        """
        updateclipstatus
        
        Args:
            clip_id: clipID
            status: ENstatus
            
        Returns:
            updateENclipENNone
        """
        return self.update(clip_id, status=status)
    
    def update_clip_score(self, clip_id: str, score: float) -> Optional[Clip]:
        """
        updateclipscoring
        
        Args:
            clip_id: clipID
            score: ENscoring
            
        Returns:
            updateENclipENNone
        """
        return self.update(clip_id, score=score)
    
    def get_clips_for_collection(self, project_id: str, collection_size: int = 5) -> List[Clip]:
        """
        fetchENcollectionENclip
        
        Args:
            project_id: projectID
            collection_size: collectionEN
            
        Returns:
            clipEN
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.status == ClipStatus.COMPLETED,
            self.model.score >= 0.7
        ).order_by(desc(self.model.score)).limit(collection_size).all()
    
    def get_clips_by_processing_step(self, project_id: str, step: int) -> List[Clip]:
        """
        ENprocessingENfetchclip
        
        Args:
            project_id: projectID
            step: processingEN
            
        Returns:
            clipEN
        """
        return self.find_by(project_id=project_id, processing_step=step)