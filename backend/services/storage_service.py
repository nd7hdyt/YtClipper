"""
translatedonetranslatedservice
"""

import json
import logging
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from ..core.config import get_data_directory

logger = logging.getLogger(__name__)

class StorageService:
    """translatedonetranslatedservice"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.data_dir = get_data_directory()
        self.project_dir = self.data_dir / "projects" / project_id
        
        # ensureprojectdirectorytranslatedin
        self._ensure_project_structure()
    
    def _ensure_project_structure(self):
        """ensureprojectdirectorytranslatedin"""
        directories = [
            self.project_dir / "raw",
            self.project_dir / "processing",
            self.project_dir / "output" / "clips",
            self.project_dir / "output" / "collections"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def save_metadata(self, metadata: Dict[str, Any], step: str) -> str:
        """translatedprocesstranslatedfileSystem"""
        metadata_file = self.project_dir / "processing" / f"{step}.json"
        self._atomic_write_json(metadata_file, metadata)
        
        logger.info(f"translated: {metadata_file}")
        return str(metadata_file)
    
    def get_metadata(self, step: str) -> Optional[Dict[str, Any]]:
        """fetchprocesstranslated"""
        metadata_file = self.project_dir / "processing" / f"{step}.json"
        
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def save_file(self, file_path: Path, target_name: str, file_type: str = "raw") -> str:
        """translatedfiletranslatedprojectdirectory"""
        if file_type == "raw":
            target_path = self.project_dir / "raw" / target_name
        elif file_type == "clip":
            target_path = self.project_dir / "output" / "clips" / target_name
        elif file_type == "collection":
            target_path = self.project_dir / "output" / "collections" / target_name
        else:
            raise ValueError(f"translatedsupport'sfiletranslated: {file_type}")
        
        # ensuretranslateddirectorytranslatedin
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # translatedfile
        shutil.copy2(file_path, target_path)
        logger.info(f"translatedfile: {target_path}")
        return str(target_path)
    
    def save_processing_result(self, step: str, result: Dict[str, Any]) -> str:
        """translatedprocesstranslatedfileSystem"""
        return self.save_metadata(result, step)
    
    def save_clip_file(self, clip_data: Dict[str, Any], clip_id: str) -> str:
        """translatedclipfiletranslatedreturnpath"""
        # fetchtranslatedcleanfiletranslated
        title = clip_data.get('title', f'clip_{clip_id}')
        from ..utils.video_processor import VideoProcessor
        safe_title = VideoProcessor.sanitize_filename(title)
        
        # usetranslatedone'stranslatedformat：{clip_id}_{safe_title}.mp4
        clip_file = f"{clip_id}_{safe_title}.mp4"
        target_path = self.project_dir / "output" / "clips" / clip_file
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # createtranslatedfile（usetranslated/translated）
        self._atomic_touch_file(target_path)
        logger.info(f"translatedclipfile: {target_path}")
        return str(target_path)
    
    def save_collection_file(self, collection_data: Dict[str, Any], collection_id: str) -> str:
        """translatedcollectionfiletranslatedreturnpath"""
        # thistranslatedPackageincludetranslated'scollectionfiletranslated
        # translatedreturntranslatedpath
        collection_file = f"collection_{collection_id}.mp4"
        target_path = self.project_dir / "output" / "collections" / collection_file
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # createtranslatedfile（usetranslated/translated）
        self._atomic_touch_file(target_path)
        logger.info(f"translatedcollectionfile: {target_path}")
        return str(target_path)

    def _atomic_write_json(self, target_path: Path, payload: Dict[str, Any]) -> None:
        """translatedJSON，translatedfile。"""
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            dir=target_path.parent,
            delete=False,
        ) as temp_file:
            json.dump(payload, temp_file, ensure_ascii=False, indent=2)
            temp_file.flush()
            temp_path = Path(temp_file.name)
        temp_path.replace(target_path)

    def _atomic_touch_file(self, target_path: Path) -> None:
        """translatedcreatetranslatedfile。"""
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode='wb',
            dir=target_path.parent,
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
        temp_path.replace(target_path)
    
    def get_file_content(self, file_path: str) -> Optional[Dict[str, Any]]:
        """fetchfiletranslated"""
        try:
            file_path_obj = Path(file_path)
            if file_path_obj.exists() and file_path_obj.suffix == '.json':
                with open(file_path_obj, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"translatedfiletranslatedfailed: {e}")
            return None
    
    def get_file_path(self, file_type: str, file_name: str) -> Optional[Path]:
        """fetchfile path"""
        if file_type == "raw":
            return self.project_dir / "raw" / file_name
        elif file_type == "clip":
            return self.project_dir / "output" / "clips" / file_name
        elif file_type == "collection":
            return self.project_dir / "output" / "collections" / file_name
        else:
            return None
    
    def cleanup_temp_files(self):
        """clean temp files"""
        temp_dir = self.data_dir / "temp"
        if temp_dir.exists():
            for temp_file in temp_dir.iterdir():
                if temp_file.is_file():
                    temp_file.unlink()
                    logger.info(f"clean temp files: {temp_file}")
    
    def cleanup_old_files(self, project_id: str, keep_days: int = 30):
        """cleantranslatedfile"""
        try:
            from datetime import datetime, timedelta
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            
            project_dir = self.data_dir / "projects" / project_id
            if not project_dir.exists():
                return
            
            # cleanprocessingtranslatedfile
            processing_dir = project_dir / "processing"
            if processing_dir.exists():
                for file_path in processing_dir.iterdir():
                    if file_path.is_file():
                        file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if file_time < cutoff_date:
                            file_path.unlink()
                            logger.info(f"cleantranslatedfile: {file_path}")
            
            logger.info(f"project {project_id} translatedfilecleantranslated")
            
        except Exception as e:
            logger.error(f"cleantranslatedfilefailed: {e}")
    
    def get_project_storage_info(self) -> Dict[str, Any]:
        """fetchprojecttranslatedinfo"""
        try:
            total_size = 0
            file_count = 0
            
            for file_path in self.project_dir.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    file_count += 1
            
            return {
                "project_id": self.project_id,
                "total_size": total_size,
                "file_count": file_count,
                "project_dir": str(self.project_dir)
            }
            
        except Exception as e:
            logger.error(f"fetchtranslatedinfofailed: {e}")
            return {}
