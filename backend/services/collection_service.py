"""
collectionservice
ENcollectionEN
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.services.base import BaseService
from backend.repositories.collection_repository import CollectionRepository
from backend.models.collection import Collection
from backend.schemas.collection import CollectionCreate, CollectionUpdate, CollectionResponse, CollectionListResponse, CollectionFilter
from backend.schemas.base import PaginationParams, PaginationResponse


class CollectionService(BaseService[Collection, CollectionCreate, CollectionUpdate, CollectionResponse]):
    """Collection service with business logic."""
    
    def __init__(self, db: Session):
        repository = CollectionRepository(db)
        super().__init__(repository)
        self.db = db
    
    def create_collection(self, collection_data: CollectionCreate) -> Collection:
        """Create a new collection with business logic."""
        collection_dict = collection_data.model_dump()
        return self.create(**collection_dict)
    
    def update_collection(self, collection_id: str, collection_data: CollectionUpdate) -> Optional[Collection]:
        """Update a collection with business logic."""
        # fetchallEN，includeNoneEN
        all_data = collection_data.model_dump()
        
        # ENNoneEN，ENmetadataEN
        update_data = {k: v for k, v in all_data.items() if v is not None or k == 'metadata'}
        
        # ifmetadataEN，needEN
        if 'metadata' in all_data:
            # fetchcurrentcollectionENmetadata
            current_collection = self.get(collection_id)
            if current_collection:
                current_metadata = getattr(current_collection, 'collection_metadata', {}) or {}
                new_metadata = collection_data.metadata or {}
                
                # ENmetadata，EN
                merged_metadata = {**current_metadata, **new_metadata}
                # useEN collection_metadata
                update_data['collection_metadata'] = merged_metadata
                # ENerrorEN
                if 'metadata' in update_data:
                    del update_data['metadata']
        
        if not update_data:
            return self.get(collection_id)
        
        return self.update(collection_id, **update_data)
    
    def delete_collection_with_filesystem_update(self, collection_id: str) -> bool:
        """deletecollectionENupdatefilesystemENdeleteEN"""
        import logging
        import json
        from pathlib import Path
        from datetime import datetime
        from ..core.path_utils import get_project_directory
        
        logger = logging.getLogger(__name__)
        
        # fetchcollectionEN
        collection = self.get(collection_id)
        if not collection:
            return False
        
        project_id = collection.project_id
        
        # deletedatabaseEN
        success = self.delete(collection_id)
        if not success:
            return False
        
        # updatefilesystemENdeleteEN
        try:
            project_dir = get_project_directory(project_id)
            deleted_collections_file = project_dir / "deleted_collections.json"
            
            # readENdeleteEN
            deleted_collections = []
            if deleted_collections_file.exists():
                try:
                    with open(deleted_collections_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        deleted_collections = data.get('deleted_collection_ids', [])
                except Exception as e:
                    logger.warning(f"readdeleteENfilefailed: {e}")
            
            # ENdeleteEN
            if collection_id not in deleted_collections:
                deleted_collections.append(collection_id)
                
                # saveupdateENdeleteEN
                deleted_data = {
                    'deleted_collection_ids': deleted_collections,
                    'last_updated': datetime.now().isoformat()
                }
                
                with open(deleted_collections_file, 'w', encoding='utf-8') as f:
                    json.dump(deleted_data, f, ensure_ascii=False, indent=2)
                
                logger.info(f"updateddeleteENfile: {deleted_collections_file}")
            
        except Exception as e:
            logger.error(f"updatedeleteENfilefailed: {e}")
            # ENfileupdatefailed，databasedeletealreadysucceeded，soreturnTrue
        
        return True
    
    def get_collections_by_project(self, project_id: str, skip: int = 0, limit: int = 100) -> List[Collection]:
        """Get collections by project ID."""
        return self.repository.find_by(project_id=project_id)
    
    def get_collections_paginated(
        self, 
        pagination: PaginationParams,
        filters: Optional[CollectionFilter] = None
    ) -> CollectionListResponse:
        """Get paginated collections with filtering."""
        # Convert filters to dict
        filter_dict = {}
        if filters:
            filter_data = filters.model_dump()
            filter_dict = {k: v for k, v in filter_data.items() if v is not None}
        
        items, pagination_response = self.get_paginated(pagination, filter_dict)
        
        # Convert to response schemas
        collection_responses = []
        for collection in items:
            # fetchclip_ids
            clip_ids = []
            metadata = getattr(collection, 'collection_metadata', {}) or {}
            if metadata and 'clip_ids' in metadata:
                # ENusemetadataENclip_ids，ENalreadyENUUIDEN
                clip_ids = metadata['clip_ids']
            
            collection_responses.append(CollectionResponse(
                id=str(getattr(collection, 'id', '')),
                project_id=str(getattr(collection, 'project_id', '')),
                name=str(getattr(collection, 'name', '')),
                description=str(getattr(collection, 'description', '')) if getattr(collection, 'description', None) else None,
                theme=getattr(collection, 'theme', None),
                status=getattr(collection, 'status', 'created').value if hasattr(getattr(collection, 'status', 'created'), 'value') else str(getattr(collection, 'status', 'created')),
                tags=getattr(collection, 'tags', []) or [],
                metadata=getattr(collection, 'collection_metadata', {}) or {},
                video_path=getattr(collection, 'export_path', None),
                thumbnail_path=getattr(collection, 'thumbnail_path', None),
                created_at=getattr(collection, 'created_at', None),
                updated_at=getattr(collection, 'updated_at', None),
                total_clips=getattr(collection, 'clips_count', 0) or 0,
                clip_ids=clip_ids
            ))
        
        return CollectionListResponse(
            items=collection_responses,
            pagination=pagination_response
        ) 