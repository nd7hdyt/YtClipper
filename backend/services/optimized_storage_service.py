"""
translatedservice - translatedissue
databasetranslated，fileSystemtranslatedfile
"""

import json
import logging
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from ..core.config import get_data_directory
from ..models.project import Project
from ..models.clip import Clip
from ..models.collection import Collection

logger = logging.getLogger(__name__)


class OptimizedStorageService:
    """translatedservice - databasetranslated，fileSystemtranslatedfile"""
    
    def __init__(self, db: Session, project_id: str):
        self.db = db
        self.project_id = project_id
        self.data_dir = get_data_directory()
        self.project_dir = self.data_dir / "projects" / project_id
        
        # ensureprojectdirectorytranslatedin
        self._ensure_project_structure()
    
    def _ensure_project_structure(self):
        """ensureprojectdirectorytranslatedin"""
        directories = [
            self.project_dir / "raw",           # translatedfile
            self.project_dir / "processing",    # processingtranslatedfile
            self.project_dir / "output" / "clips",      # clipfile
            self.project_dir / "output" / "collections" # collectionfile
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    # ==================== projectfiletranslated ====================
    
    def save_project_file(self, file_path: Path, file_type: str = "video") -> str:
        """translatedprojectfiletranslatedfileSystem，returntranslatedpath"""
        try:
            if file_type == "video":
                target_dir = self.project_dir / "raw"
                target_name = f"input_video{file_path.suffix}"
            elif file_type == "subtitle":
                target_dir = self.project_dir / "raw"
                target_name = f"input_subtitle{file_path.suffix}"
            else:
                target_dir = self.project_dir / "raw"
                target_name = file_path.name
            
            target_path = target_dir / target_name
            shutil.copy2(file_path, target_path)
            
            # returntranslatedpath，usetranslatedindatabasetranslated
            relative_path = f"projects/{self.project_id}/raw/{target_name}"
            logger.info(f"projectfiletranslated: {relative_path}")
            return relative_path
            
        except Exception as e:
            logger.error(f"translatedprojectfilefailed: {e}")
            raise
    
    def get_project_file_path(self, relative_path: str) -> Path:
        """translatedpathfetchtranslatedfile path"""
        return self.data_dir / relative_path
    
    # ==================== clipfiletranslated ====================
    
    def save_clip_file(self, clip_data: Dict[str, Any], clip_id: str) -> str:
        """translatedclipfiletranslatedfileSystem，returntranslatedpath"""
        try:
            # thistranslatedPackageincludetranslated'sclipfiletranslated
            # translatedreturntranslatedpath
            clip_file = f"clip_{clip_id}.mp4"
            target_path = self.project_dir / "output" / "clips" / clip_file
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # createtranslatedfile（translated'sclipfile）
            target_path.touch()
            
            # returntranslatedpath
            relative_path = f"projects/{self.project_id}/output/clips/{clip_file}"
            logger.info(f"clipfiletranslated: {relative_path}")
            return relative_path
            
        except Exception as e:
            logger.error(f"translatedclipfilefailed: {e}")
            raise
    
    def save_clip_metadata(self, clip_data: Dict[str, Any], clip_id: str) -> Clip:
        """translatedcliptranslateddatabase"""
        try:
            # createcliptranslated，translated
            clip = Clip(
                id=clip_id,
                project_id=self.project_id,
                title=clip_data.get('title', ''),
                description=clip_data.get('description', ''),
                start_time=clip_data.get('start_time', 0),
                end_time=clip_data.get('end_time', 0),
                duration=clip_data.get('duration', 0),
                score=clip_data.get('score', 0.0),
                recommendation_reason=clip_data.get('recommendation_reason', ''),
                video_path=self.save_clip_file(clip_data, clip_id),  # translatedpath
                thumbnail_path=clip_data.get('thumbnail_path', ''),
                processing_step=clip_data.get('processing_step', 6),
                tags=clip_data.get('tags', []),
                clip_metadata=clip_data.get('metadata', {})  # translated
            )
            
            self.db.add(clip)
            self.db.commit()
            self.db.refresh(clip)
            
            logger.info(f"cliptranslateddatabase: {clip_id}")
            return clip
            
        except Exception as e:
            logger.error(f"translatedcliptranslatedfailed: {e}")
            self.db.rollback()
            raise
    
    # ==================== collectionfiletranslated ====================
    
    def save_collection_file(self, collection_data: Dict[str, Any], collection_id: str) -> str:
        """translatedcollectionfiletranslatedfileSystem，returntranslatedpath"""
        try:
            # thistranslatedPackageincludetranslated'scollectionfiletranslated
            # translatedreturntranslatedpath
            collection_file = f"collection_{collection_id}.mp4"
            target_path = self.project_dir / "output" / "collections" / collection_file
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # createtranslatedfile（translated'scollectionfile）
            target_path.touch()
            
            # returntranslatedpath
            relative_path = f"projects/{self.project_id}/output/collections/{collection_file}"
            logger.info(f"collectionfiletranslated: {relative_path}")
            return relative_path
            
        except Exception as e:
            logger.error(f"translatedcollectionfilefailed: {e}")
            raise
    
    def save_collection_metadata(self, collection_data: Dict[str, Any], collection_id: str) -> Collection:
        """translatedcollectiontranslateddatabase"""
        try:
            # createcollectiontranslated，translated
            collection = Collection(
                id=collection_id,
                project_id=self.project_id,
                name=collection_data.get('name', ''),
                description=collection_data.get('description', ''),
                clip_ids=collection_data.get('clip_ids', []),
                video_path=self.save_collection_file(collection_data, collection_id),  # translatedpath
                thumbnail_path=collection_data.get('thumbnail_path', ''),
                tags=collection_data.get('tags', []),
                collection_metadata=collection_data.get('metadata', {})  # translated
            )
            
            self.db.add(collection)
            self.db.commit()
            self.db.refresh(collection)
            
            logger.info(f"collectiontranslateddatabase: {collection_id}")
            return collection
            
        except Exception as e:
            logger.error(f"translatedcollectiontranslatedfailed: {e}")
            self.db.rollback()
            raise
    
    # ==================== processingtranslatedfiletranslated ====================
    
    def save_processing_metadata(self, metadata: Dict[str, Any], step: str) -> str:
        """translatedprocessingtranslatedfileSystem"""
        try:
            metadata_file = self.project_dir / "processing" / f"{step}.json"
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            logger.info(f"processtranslated: {metadata_file}")
            return str(metadata_file)
            
        except Exception as e:
            logger.error(f"translatedprocesstranslatedfailed: {e}")
            raise
    
    def get_processing_metadata(self, step: str) -> Optional[Dict[str, Any]]:
        """fetchprocessingtranslated"""
        try:
            metadata_file = self.project_dir / "processing" / f"{step}.json"
            
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
            
        except Exception as e:
            logger.error(f"fetchprocesstranslatedfailed: {e}")
            return None
    
    # ==================== translated ====================
    
    def get_project_clips(self) -> List[Clip]:
        """fetchproject'stranslatedclip（fromdatabase）"""
        return self.db.query(Clip).filter(Clip.project_id == self.project_id).all()
    
    def get_project_collections(self) -> List[Collection]:
        """fetchproject'stranslatedcollection（fromdatabase）"""
        return self.db.query(Collection).filter(Collection.project_id == self.project_id).all()
    
    def get_clip_file_path(self, clip: Clip) -> Path:
        """fetchclip'stranslatedfile path"""
        if clip.video_path:
            return self.data_dir / clip.video_path
        return None
    
    def get_collection_file_path(self, collection: Collection) -> Path:
        """fetchcollection'stranslatedfile path"""
        if collection.video_path:
            return self.data_dir / collection.video_path
        return None
    
    # ==================== cleantranslated ====================
    
    def cleanup_temp_files(self):
        """clean temp files"""
        temp_dir = self.data_dir / "temp"
        if temp_dir.exists():
            for temp_file in temp_dir.iterdir():
                if temp_file.is_file():
                    temp_file.unlink()
                    logger.info(f"clean temp files: {temp_file}")
    
    def cleanup_old_files(self, keep_days: int = 30):
        """cleantranslatedfile"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=keep_days)
            
            # cleantranslated'stranslatedfile
            temp_dir = self.data_dir / "temp"
            if temp_dir.exists():
                for temp_file in temp_dir.iterdir():
                    if temp_file.is_file() and temp_file.stat().st_mtime < cutoff_date.timestamp():
                        temp_file.unlink()
                        logger.info(f"cleantranslatedfile: {temp_file}")
            
            logger.info(f"cleantranslated，translated {keep_days} translated'sfile")
            
        except Exception as e:
            logger.error(f"cleantranslatedfilefailed: {e}")
    
    # ==================== translated ====================
    
    def migrate_from_old_storage(self, old_project_dir: Path) -> Dict[str, Any]:
        """fromtranslatedformattranslated"""
        try:
            logger.info(f"translatedprojecttranslated: {self.project_id}")
            
            migrated_files = []
            migrated_metadata = []
            
            # translatedfile
            if (old_project_dir / "raw").exists():
                for file_path in (old_project_dir / "raw").iterdir():
                    if file_path.is_file():
                        relative_path = self.save_project_file(file_path)
                        migrated_files.append(relative_path)
            
            # translatedprocesstranslated
            if (old_project_dir / "processing").exists():
                for metadata_file in (old_project_dir / "processing").iterdir():
                    if metadata_file.suffix == '.json':
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        
                        step_name = metadata_file.stem
                        self.save_processing_metadata(metadata, step_name)
                        migrated_metadata.append(step_name)
            
            # translatedfile
            if (old_project_dir / "output").exists():
                # translatedclipfile
                clips_dir = old_project_dir / "output" / "clips"
                if clips_dir.exists():
                    for clip_file in clips_dir.iterdir():
                        if clip_file.is_file():
                            target_path = self.project_dir / "output" / "clips" / clip_file.name
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(clip_file, target_path)
                            migrated_files.append(f"projects/{self.project_id}/output/clips/{clip_file.name}")
                
                # translatedcollectionfile
                collections_dir = old_project_dir / "output" / "collections"
                if collections_dir.exists():
                    for collection_file in collections_dir.iterdir():
                        if collection_file.is_file():
                            target_path = self.project_dir / "output" / "collections" / collection_file.name
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(collection_file, target_path)
                            migrated_files.append(f"projects/{self.project_id}/output/collections/{collection_file.name}")
            
            logger.info(f"translated: {len(migrated_files)}  file, {len(migrated_metadata)}  translated")
            
            return {
                "success": True,
                "migrated_files": migrated_files,
                "migrated_metadata": migrated_metadata
            }
            
        except Exception as e:
            logger.error(f"translatedfailed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
