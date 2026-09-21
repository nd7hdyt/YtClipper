"""
translatedonetranslatedservice
ensuretranslatedusetranslated'spathtranslatedAndtranslated
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)

class UnifiedStorageManager:
    """translatedonetranslated"""
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        translatedonetranslated
        
        Args:
            project_root: projecttranslateddirectory，iftranslatedNonetranslated
        """
        self.project_root = project_root or self._get_project_root()
        self.data_dir = self.project_root / "data"
        self.output_dir = self.data_dir / "output"
        
        # ensuretranslateddirectorytranslatedin
        self._ensure_directories()
    
    def _get_project_root(self) -> Path:
        """fetchprojecttranslateddirectory"""
        current_path = Path(__file__).parent  # backend/core/
        
        # translatedprojecttranslateddirectory
        while current_path.parent != current_path:
            if (current_path.parent / "frontend").exists() and (current_path.parent / "backend").exists():
                return current_path.parent
            current_path = current_path.parent
        
        # iftranslated，usedefaultpath
        return Path(__file__).parent.parent.parent
    
    def _ensure_directories(self):
        """ensuretranslateddirectorytranslatedin"""
        directories = [
            self.data_dir,
            self.output_dir,
            self.output_dir / "clips",
            self.output_dir / "collections",
            self.output_dir / "metadata",
            self.data_dir / "projects",
            self.data_dir / "uploads",
            self.data_dir / "temp",
            self.data_dir / "backups"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    # projecttranslatedpath
    def get_project_directory(self, project_id: str) -> Path:
        """fetchprojectdirectory"""
        project_dir = self.data_dir / "projects" / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir
    
    def get_project_raw_directory(self, project_id: str) -> Path:
        """fetchprojecttranslatedfiledirectory"""
        raw_dir = self.get_project_directory(project_id) / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        return raw_dir
    
    def get_project_output_directory(self, project_id: str) -> Path:
        """fetchprojecttranslateddirectory"""
        output_dir = self.get_project_directory(project_id) / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    def get_project_clips_directory(self, project_id: str) -> Path:
        """fetchprojectclipdirectory"""
        clips_dir = self.get_project_output_directory(project_id) / "clips"
        clips_dir.mkdir(parents=True, exist_ok=True)
        return clips_dir
    
    def get_project_collections_directory(self, project_id: str) -> Path:
        """fetchprojectcollectiondirectory"""
        collections_dir = self.get_project_output_directory(project_id) / "collections"
        collections_dir.mkdir(parents=True, exist_ok=True)
        return collections_dir
    
    def get_project_metadata_directory(self, project_id: str) -> Path:
        """fetchprojecttranslateddirectory"""
        metadata_dir = self.get_project_directory(project_id) / "metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        return metadata_dir
    
    # file pathtranslated
    def get_video_file_path(self, project_id: str, filename: str) -> Path:
        """fetchprojectvideofile path"""
        return self.get_project_raw_directory(project_id) / filename
    
    def get_srt_file_path(self, project_id: str, filename: str) -> Path:
        """fetchprojectSRTfile path"""
        return self.get_project_raw_directory(project_id) / filename
    
    def get_clip_file_path(self, project_id: str, clip_id: str, title: str) -> Path:
        """fetchclipfile path"""
        # cleanfiletranslated，translated
        safe_title = self._sanitize_filename(title)
        return self.get_project_clips_directory(project_id) / f"{clip_id}_{safe_title}.mp4"
    
    def get_collection_file_path(self, project_id: str, collection_id: str, title: str) -> Path:
        """fetchcollectionfile path"""
        # cleanfiletranslated，translated
        safe_title = self._sanitize_filename(title)
        return self.get_project_collections_directory(project_id) / f"{collection_id}_{safe_title}.mp4"
    
    def get_metadata_file_path(self, project_id: str, filename: str) -> Path:
        """fetchprojecttranslatedfile path"""
        return self.get_project_metadata_directory(project_id) / filename
    
    # filetranslated
    def save_metadata(self, project_id: str, filename: str, data: Dict[str, Any]) -> Path:
        """translatedfile"""
        metadata_file = self.get_metadata_file_path(project_id, filename)
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"translated: {metadata_file}")
        return metadata_file
    
    def load_metadata(self, project_id: str, filename: str) -> Optional[Dict[str, Any]]:
        """translatedfile"""
        metadata_file = self.get_metadata_file_path(project_id, filename)
        
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"translatedfailed {metadata_file}: {e}")
        
        return None
    
    def file_exists(self, file_path: Union[str, Path]) -> bool:
        """checkfileIstranslatedin"""
        return Path(file_path).exists()
    
    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """fetchfiletranslated（translated）"""
        try:
            return Path(file_path).stat().st_size
        except Exception:
            return 0
    
    def get_file_modified_time(self, file_path: Union[str, Path]) -> Optional[datetime]:
        """fetchfiletranslated"""
        try:
            timestamp = Path(file_path).stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        except Exception:
            return None
    
    # pathverifyAndfixed
    def validate_file_path(self, file_path: Union[str, Path]) -> bool:
        """verifyfile pathIstranslated"""
        try:
            file_path = Path(file_path).resolve()
            # checkpathIstranslatedintranslated'sdirectorytranslated
            allowed_dirs = [
                self.data_dir,
                self.output_dir,
                self.project_root
            ]
            
            return any(file_path.is_relative_to(allowed_dir) for allowed_dir in allowed_dirs)
        except Exception:
            return False
    
    def fix_file_path(self, file_path: Union[str, Path], project_id: str, file_type: str = "clip") -> Optional[Path]:
        """
        fixedfile path，ensurefileintranslated'stranslated
        
        Args:
            file_path: translatedfile path
            project_id: projectID
            file_type: filetranslated ("clip", "collection", "raw")
            
        Returns:
            fixedtranslated'sfile path，iftranslatedfile not foundtranslatedreturnNone
        """
        original_path = Path(file_path)
        
        # iftranslatedfiletranslatedintranslatedpathtranslated，translatedreturn
        if original_path.exists() and self.validate_file_path(original_path):
            return original_path
        
        # translatedintranslatedfile
        if file_type == "clip":
            # fromfiletranslatedclip_idAndtitle
            filename = original_path.name
            if '_' in filename:
                parts = filename.split('_', 1)
                if len(parts) == 2:
                    clip_id = parts[0]
                    title = parts[1].replace('.mp4', '')
                    standard_path = self.get_clip_file_path(project_id, clip_id, title)
                    if standard_path.exists():
                        return standard_path
        
        elif file_type == "collection":
            # fromfiletranslatedcollection_idAndtitle
            filename = original_path.name
            if '_' in filename:
                parts = filename.split('_', 1)
                if len(parts) == 2:
                    collection_id = parts[0]
                    title = parts[1].replace('.mp4', '')
                    standard_path = self.get_collection_file_path(project_id, collection_id, title)
                    if standard_path.exists():
                        return standard_path
            else:
                # translatedusefiletranslatedtitle
                title = filename.replace('.mp4', '')
                # thistranslatedcollection_id，translatedreturnNone
                return None
        
        elif file_type == "raw":
            # translatedfiletranslatedinrawdirectory
            filename = original_path.name
            standard_path = self.get_project_raw_directory(project_id) / filename
            if standard_path.exists():
                return standard_path
        
        return None
    
    # tooltranslated
    def _sanitize_filename(self, filename: str) -> str:
        """cleanfiletranslated，translated"""
        # translatedortranslated
        safe_chars = []
        for char in filename:
            if char.isalnum() or char in (' ', '-', '_', '，', '。', '？', '！', '：', '；'):
                safe_chars.append(char)
            else:
                safe_chars.append('_')
        
        # translatedmultitranslated'stranslatedAndtranslated
        result = ''.join(safe_chars).strip()
        result = result.replace(' ', '_')
        
        # translated'stranslated
        while '__' in result:
            result = result.replace('__', '_')
        
        return result
    
    def get_storage_info(self, project_id: str) -> Dict[str, Any]:
        """fetchprojecttranslatedinfo"""
        project_dir = self.get_project_directory(project_id)
        
        info = {
            "project_id": project_id,
            "project_directory": str(project_dir),
            "raw_files": [],
            "clips": [],
            "collections": [],
            "metadata_files": [],
            "total_size": 0
        }
        
        # translatedfile
        raw_dir = self.get_project_raw_directory(project_id)
        for file_path in raw_dir.iterdir():
            if file_path.is_file():
                info["raw_files"].append({
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
                info["total_size"] += file_path.stat().st_size
        
        # translatedclipfile
        clips_dir = self.get_project_clips_directory(project_id)
        for file_path in clips_dir.iterdir():
            if file_path.is_file() and file_path.suffix == '.mp4':
                info["clips"].append({
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
                info["total_size"] += file_path.stat().st_size
        
        # translatedcollectionfile
        collections_dir = self.get_project_collections_directory(project_id)
        for file_path in collections_dir.iterdir():
            if file_path.is_file() and file_path.suffix == '.mp4':
                info["collections"].append({
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
                info["total_size"] += file_path.stat().st_size
        
        # translatedfile
        metadata_dir = self.get_project_metadata_directory(project_id)
        for file_path in metadata_dir.iterdir():
            if file_path.is_file() and file_path.suffix == '.json':
                info["metadata_files"].append({
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
                info["total_size"] += file_path.stat().st_size
        
        return info

# translated
_storage_manager = None

def get_storage_manager() -> UnifiedStorageManager:
    """fetchtranslated"""
    global _storage_manager
    if _storage_manager is None:
        _storage_manager = UnifiedStorageManager()
    return _storage_manager

