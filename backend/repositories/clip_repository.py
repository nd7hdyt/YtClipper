"""
clipRepository
Providescliptranslated'stranslated
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from pathlib import Path
from .base import BaseRepository
from ..models.clip import Clip, ClipStatus

class ClipRepository(BaseRepository[Clip]):
    """clipRepositorytranslated"""
    
    def __init__(self, db: Session):
        super().__init__(Clip, db)
    
    def get_by_project(self, project_id: str) -> List[Clip]:
        """
        fetchproject'stranslatedclip
        
        Args:
            project_id: projectID
            
        Returns:
            cliplist
        """
        return self.find_by(project_id=project_id)
    
    def get_by_status(self, status: ClipStatus) -> List[Clip]:
        """
        translatedstatusfetchcliplist
        
        Args:
            status: clipstatus
            
        Returns:
            cliplist
        """
        return self.find_by(status=status)
    
    def get_by_project_and_status(self, project_id: str, status: ClipStatus) -> List[Clip]:
        """
        translatedprojectAndstatusfetchcliplist
        
        Args:
            project_id: projectID
            status: clipstatus
            
        Returns:
            cliplist
        """
        return self.find_by(project_id=project_id, status=status)
    
    def get_high_score_clips(self, project_id: str, min_score: float = 0.7, limit: int = 10) -> List[Clip]:
        """
        fetchtranslatedclip
        
        Args:
            project_id: projectID
            min_score: translated
            limit: returntranslated
            
        Returns:
            translatedcliplist
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.score >= min_score
        ).order_by(desc(self.model.score)).limit(limit).all()
    
    def get_clips_by_duration_range(self, project_id: str, min_duration: int, max_duration: int) -> List[Clip]:
        """
        translatedfetchclip
        
        Args:
            project_id: projectID
            min_duration: translated（seconds）
            max_duration: translated（seconds）
            
        Returns:
            cliplist
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.duration >= min_duration,
            self.model.duration <= max_duration
        ).order_by(asc(self.model.start_time)).all()
    
    def get_clips_by_time_range(self, project_id: str, start_time: int, end_time: int) -> List[Clip]:
        """
        translatedfetchclip
        
        Args:
            project_id: projectID
            start_time: translated（seconds）
            end_time: translated（seconds）
            
        Returns:
            cliplist
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.start_time >= start_time,
            self.model.end_time <= end_time
        ).order_by(asc(self.model.start_time)).all()
    
    def create_clip(self, clip_data: Dict[str, Any]) -> Clip:
        """createcliptranslated（translated）"""
        from ..services.storage_service import StorageService
        import uuid
        
        # translatedclipID（iftranslatedProvides）
        if "id" not in clip_data:
            clip_data["id"] = str(uuid.uuid4())
        
        # 1. translatedclipfiletranslatedfileSystem
        storage_service = StorageService(clip_data["project_id"])
        video_path = storage_service.save_clip_file(clip_data, clip_data["id"])
        
        # 2. translatedfileSystem
        metadata_path = storage_service.save_metadata(clip_data, f"clip_{clip_data['id']}")
        
        # 3. translateddatabase（translatedpathtranslateduse）
        clip = Clip(
            id=clip_data["id"],
            project_id=clip_data["project_id"],
            title=clip_data["title"],
            description=clip_data.get("description"),
            start_time=clip_data["start_time"],
            end_time=clip_data["end_time"],
            duration=clip_data["duration"],
            score=clip_data.get("score"),
            video_path=video_path,  # translatedpath
            clip_metadata={
                'metadata_file': metadata_path,  # translatedfile path
                'clip_id': clip_data["id"],
                'created_at': clip_data.get("created_at")
            }
        )
        
        self.db.add(clip)
        self.db.commit()
        return clip
    
    def get_clip_file(self, clip_id: str) -> Optional[Path]:
        """fetchclipfile path"""
        clip = self.get_by_id(clip_id)
        if clip and clip.video_path:
            return Path(clip.video_path)
        return None
    
    def get_clip_content(self, clip_id: str) -> Optional[Dict[str, Any]]:
        """fetchcliptranslated"""
        clip = self.get_by_id(clip_id)
        if not clip:
            return None
        
        # fromfileSystemfetchtranslated
        if clip.clip_metadata and 'metadata_file' in clip.clip_metadata:
            from ..services.storage_service import StorageService
            storage_service = StorageService(clip.project_id)
            return storage_service.get_file_content(clip.clip_metadata['metadata_file'])
        
        return None
    
    def search_clips(self, project_id: str, keyword: str) -> List[Clip]:
        """
        translatedclip
        
        Args:
            project_id: projectID
            keyword: translated
            
        Returns:
            translated'scliplist
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            (self.model.title.contains(keyword) | 
             self.model.description.contains(keyword) |
             self.model.recommendation_reason.contains(keyword))
        ).all()
    
    def get_clips_statistics(self, project_id: str) -> dict:
        """
        fetchcliptranslatedinfo
        
        Args:
            project_id: projectID
            
        Returns:
            translatedinfotranslated
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
            status: translatedstatus
            
        Returns:
            updatetranslated'scliptranslatedorNone
        """
        return self.update(clip_id, status=status)
    
    def update_clip_score(self, clip_id: str, score: float) -> Optional[Clip]:
        """
        updatecliptranslated
        
        Args:
            clip_id: clipID
            score: translated
            
        Returns:
            updatetranslated'scliptranslatedorNone
        """
        return self.update(clip_id, score=score)
    
    def get_clips_for_collection(self, project_id: str, collection_size: int = 5) -> List[Clip]:
        """
        fetchtranslatedcollection'sclip
        
        Args:
            project_id: projectID
            collection_size: collectiontranslated
            
        Returns:
            cliplist
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.status == ClipStatus.COMPLETED,
            self.model.score >= 0.7
        ).order_by(desc(self.model.score)).limit(collection_size).all()
    
    def get_clips_by_processing_step(self, project_id: str, step: int) -> List[Clip]:
        """
        translatedprocessstepfetchclip
        
        Args:
            project_id: projectID
            step: processstep
            
        Returns:
            cliplist
        """
        return self.find_by(project_id=project_id, processing_step=step)