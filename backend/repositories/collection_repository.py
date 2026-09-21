"""
collectionRepository
Providescollectiontranslated'stranslated
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from pathlib import Path
from .base import BaseRepository
from ..models.collection import Collection, CollectionStatus

class CollectionRepository(BaseRepository[Collection]):
    """collectionRepositorytranslated"""
    
    def __init__(self, db: Session):
        super().__init__(Collection, db)
    
    def get_by_project(self, project_id: str) -> List[Collection]:
        """
        fetchproject'stranslatedcollection
        
        Args:
            project_id: projectID
            
        Returns:
            collectionlist
        """
        return self.find_by(project_id=project_id)
    
    def get_by_status(self, status: CollectionStatus) -> List[Collection]:
        """
        translatedstatusfetchcollectionlist
        
        Args:
            status: collectionstatus
            
        Returns:
            collectionlist
        """
        return self.find_by(status=status)
    
    def get_by_project_and_status(self, project_id: str, status: CollectionStatus) -> List[Collection]:
        """
        translatedprojectAndstatusfetchcollectionlist
        
        Args:
            project_id: projectID
            status: collectionstatus
            
        Returns:
            collectionlist
        """
        return self.find_by(project_id=project_id, status=status)
    
    def get_by_theme(self, project_id: str, theme: str) -> List[Collection]:
        """
        translatedfetchcollectionlist
        
        Args:
            project_id: projectID
            theme: translated
            
        Returns:
            collectionlist
        """
        return self.find_by(project_id=project_id, theme=theme)
    
    def get_completed_collections(self, project_id: str) -> List[Collection]:
        """
        fetchcompleted'scollection
        
        Args:
            project_id: projectID
            
        Returns:
            completed'scollectionlist
        """
        return self.find_by(project_id=project_id, status=CollectionStatus.COMPLETED)
    
    def search_collections(self, project_id: str, keyword: str) -> List[Collection]:
        """
        translatedcollection
        
        Args:
            project_id: projectID
            keyword: translated
            
        Returns:
            translated'scollectionlist
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            (self.model.name.contains(keyword) | 
             self.model.description.contains(keyword) |
             self.model.theme.contains(keyword))
        ).all()
    
    def get_collections_by_clips_count(self, project_id: str, min_clips: int = 1) -> List[Collection]:
        """
        translatedcliptranslatedfetchcollection
        
        Args:
            project_id: projectID
            min_clips: translatedcliptranslated
            
        Returns:
            collectionlist
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.clips_count >= min_clips
        ).order_by(desc(self.model.clips_count)).all()
    
    def create_collection(self, collection_data: Dict[str, Any]) -> Collection:
        """createcollectiontranslated（translated）"""
        from ..services.storage_service import StorageService
        import uuid
        
        # translatedcollectionID（iftranslatedProvides）
        if "id" not in collection_data:
            collection_data["id"] = str(uuid.uuid4())
        
        # 1. translatedcollectionfiletranslatedfileSystem
        storage_service = StorageService(collection_data["project_id"])
        export_path = storage_service.save_collection_file(collection_data, collection_data["id"])
        
        # 2. translatedfileSystem
        metadata_path = storage_service.save_metadata(collection_data, f"collection_{collection_data['id']}")
        
        # 3. translateddatabase（translatedpathtranslateduse）
        collection = Collection(
            id=collection_data["id"],
            project_id=collection_data["project_id"],
            name=collection_data["name"],
            description=collection_data.get("description"),
            theme=collection_data.get("theme"),
            tags=collection_data.get("tags"),
            total_duration=collection_data.get("total_duration"),
            clips_count=collection_data.get("clips_count", 0),
            export_path=export_path,  # translatedpath
            collection_metadata={
                'metadata_file': metadata_path,  # translatedfile path
                'clip_ids': collection_data.get('clip_ids', []),
                'collection_type': collection_data.get('collection_type', 'ai_recommended'),
                'collection_id': collection_data["id"],
                'created_at': collection_data.get("created_at")
            }
        )
        
        self.db.add(collection)
        self.db.commit()
        return collection
    
    def get_collection_file(self, collection_id: str) -> Optional[Path]:
        """fetchcollectionfile path"""
        collection = self.get_by_id(collection_id)
        if collection and collection.export_path:
            return Path(collection.export_path)
        return None
    
    def get_collection_content(self, collection_id: str) -> Optional[Dict[str, Any]]:
        """fetchcollectiontranslated"""
        collection = self.get_by_id(collection_id)
        if not collection:
            return None
        
        # fromfileSystemfetchtranslated
        if collection.collection_metadata and 'metadata_file' in collection.collection_metadata:
            from ..services.storage_service import StorageService
            storage_service = StorageService(collection.project_id)
            return storage_service.get_file_content(collection.collection_metadata['metadata_file'])
        
        return None
    
    def get_collections_by_duration_range(self, project_id: str, min_duration: int, max_duration: int) -> List[Collection]:
        """
        translatedfetchcollection
        
        Args:
            project_id: projectID
            min_duration: translated（seconds）
            max_duration: translated（seconds）
            
        Returns:
            collectionlist
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.total_duration >= min_duration,
            self.model.total_duration <= max_duration
        ).order_by(asc(self.model.total_duration)).all()
    
    def get_collections_statistics(self, project_id: str) -> dict:
        """
        fetchcollectiontranslatedinfo
        
        Args:
            project_id: projectID
            
        Returns:
            translatedinfotranslated
        """
        total_collections = self.db.query(self.model).filter(
            self.model.project_id == project_id
        ).count()
        
        completed_collections = self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.status == CollectionStatus.COMPLETED
        ).count()
        
        avg_clips_count = self.db.query(func.avg(self.model.clips_count)).filter(
            self.model.project_id == project_id
        ).scalar()
        
        total_duration = self.db.query(func.sum(self.model.total_duration)).filter(
            self.model.project_id == project_id
        ).scalar()
        
        return {
            "total": total_collections,
            "completed": completed_collections,
            "avg_clips_count": float(avg_clips_count) if avg_clips_count else 0.0,
            "total_duration": int(total_duration) if total_duration else 0,
            "completion_rate": (completed_collections / total_collections * 100) if total_collections > 0 else 0
        }
    
    def update_collection_status(self, collection_id: str, status: CollectionStatus) -> Optional[Collection]:
        """
        updatecollectionstatus
        
        Args:
            collection_id: collectionID
            status: translatedstatus
            
        Returns:
            updatetranslated'scollectiontranslatedorNone
        """
        return self.update(collection_id, status=status)
    
    def update_collection_clips_count(self, collection_id: str, clips_count: int) -> Optional[Collection]:
        """
        updatecollectioncliptranslated
        
        Args:
            collection_id: collectionID
            clips_count: cliptranslated
            
        Returns:
            updatetranslated'scollectiontranslatedorNone
        """
        return self.update(collection_id, clips_count=clips_count)
    
    def update_collection_duration(self, collection_id: str, total_duration: int) -> Optional[Collection]:
        """
        updatecollectiontranslated
        
        Args:
            collection_id: collectionID
            total_duration: translated（seconds）
            
        Returns:
            updatetranslated'scollectiontranslatedorNone
        """
        return self.update(collection_id, total_duration=total_duration)
    
    def get_collections_with_clips(self, project_id: str) -> List[Collection]:
        """
        fetchPackageincludeclip'scollectiontranslated
        
        Args:
            project_id: projectID
            
        Returns:
            collectionlist
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id
        ).all()
    
    def get_collection_by_theme_and_size(self, project_id: str, theme: str, target_size: int = 5) -> Optional[Collection]:
        """
        translatedAndtranslatedfetchcollection
        
        Args:
            project_id: projectID
            theme: translated
            target_size: translated
            
        Returns:
            collectiontranslatedorNone
        """
        return self.db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.theme == theme,
            self.model.clips_count == target_size
        ).first()