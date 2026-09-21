"""
ENservice
ENallENuseENpathEN
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)

class UnifiedStorageManager:
    """EN"""
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        initializeEN
        
        Args:
            project_root: projectENdirectory，ifENNonethenEN
        """
        self.project_root = project_root or self._get_project_root()
        self.data_dir = self.project_root / "data"
        self.output_dir = self.data_dir / "output"
        
        # ENdirectoryEN
        self._ensure_directories()
    
    def _get_project_root(self) -> Path:
        """fetchprojectENdirectory"""
        current_path = Path(__file__).parent  # backend/core/
        
        # ENprojectENdirectory
        while current_path.parent != current_path:
            if (current_path.parent / "frontend").exists() and (current_path.parent / "backend").exists():
                return current_path.parent
            current_path = current_path.parent
        
        # ifEN，useENpath
        return Path(__file__).parent.parent.parent
    
    def _ensure_directories(self):
        """ENdirectoryEN"""
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
    
    # projectENpath
    def get_project_directory(self, project_id: str) -> Path:
        """fetchprojectdirectory"""
        project_dir = self.data_dir / "projects" / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir
    
    def get_project_raw_directory(self, project_id: str) -> Path:
        """fetchprojectENfiledirectory"""
        raw_dir = self.get_project_directory(project_id) / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        return raw_dir
    
    def get_project_output_directory(self, project_id: str) -> Path:
        """fetchprojectENdirectory"""
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
        """fetchprojectENdirectory"""
        metadata_dir = self.get_project_directory(project_id) / "metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        return metadata_dir
    
    # filepathEN
    def get_video_file_path(self, project_id: str, filename: str) -> Path:
        """fetchprojectvideofilepath"""
        return self.get_project_raw_directory(project_id) / filename
    
    def get_srt_file_path(self, project_id: str, filename: str) -> Path:
        """fetchprojectSRTfilepath"""
        return self.get_project_raw_directory(project_id) / filename
    
    def get_clip_file_path(self, project_id: str, clip_id: str, title: str) -> Path:
        """fetchclipfilepath"""
        # ENfileEN，EN
        safe_title = self._sanitize_filename(title)
        return self.get_project_clips_directory(project_id) / f"{clip_id}_{safe_title}.mp4"
    
    def get_collection_file_path(self, project_id: str, collection_id: str, title: str) -> Path:
        """fetchcollectionfilepath"""
        # ENfileEN，EN
        safe_title = self._sanitize_filename(title)
        return self.get_project_collections_directory(project_id) / f"{collection_id}_{safe_title}.mp4"
    
    def get_metadata_file_path(self, project_id: str, filename: str) -> Path:
        """fetchprojectENfilepath"""
        return self.get_project_metadata_directory(project_id) / filename
    
    # fileEN
    def save_metadata(self, project_id: str, filename: str, data: Dict[str, Any]) -> Path:
        """saveENfile"""
        metadata_file = self.get_metadata_file_path(project_id, filename)
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"ENsave: {metadata_file}")
        return metadata_file
    
    def load_metadata(self, project_id: str, filename: str) -> Optional[Dict[str, Any]]:
        """loadENfile"""
        metadata_file = self.get_metadata_file_path(project_id, filename)
        
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"loadENfailed {metadata_file}: {e}")
        
        return None
    
    def file_exists(self, file_path: Union[str, Path]) -> bool:
        """checkfileEN"""
        return Path(file_path).exists()
    
    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """fetchfileEN（EN）"""
        try:
            return Path(file_path).stat().st_size
        except Exception:
            return 0
    
    def get_file_modified_time(self, file_path: Union[str, Path]) -> Optional[datetime]:
        """fetchfileENtime"""
        try:
            timestamp = Path(file_path).stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        except Exception:
            return None
    
    # pathvalidateEN
    def validate_file_path(self, file_path: Union[str, Path]) -> bool:
        """validatefilepathEN"""
        try:
            file_path = Path(file_path).resolve()
            # checkpathENdirectoryEN
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
        ENfilepath，ENfileEN
        
        Args:
            file_path: ENfilepath
            project_id: projectID
            file_type: fileEN ("clip", "collection", "raw")
            
        Returns:
            ENfilepath，iffiledoes not existthenreturnNone
        """
        original_path = Path(file_path)
        
        # iffileENpathEN，ENreturn
        if original_path.exists() and self.validate_file_path(original_path):
            return original_path
        
        # ENfile
        if file_type == "clip":
            # ENfileENclip_idENtitle
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
            # ENfileENcollection_idENtitle
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
                # ENusefileENtitle
                title = filename.replace('.mp4', '')
                # ENneedcollection_id，ENreturnNone
                return None
        
        elif file_type == "raw":
            # ENfileENrawdirectory
            filename = original_path.name
            standard_path = self.get_project_raw_directory(project_id) / filename
            if standard_path.exists():
                return standard_path
        
        return None
    
    # EN
    def _sanitize_filename(self, filename: str) -> str:
        """ENfileEN，EN"""
        # EN
        safe_chars = []
        for char in filename:
            if char.isalnum() or char in (' ', '-', '_', '，', '。', '？', '！', '：', '；'):
                safe_chars.append(char)
            else:
                safe_chars.append('_')
        
        # EN
        result = ''.join(safe_chars).strip()
        result = result.replace(' ', '_')
        
        # EN
        while '__' in result:
            result = result.replace('__', '_')
        
        return result
    
    def get_storage_info(self, project_id: str) -> Dict[str, Any]:
        """fetchprojectEN"""
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
        
        # ENfile
        raw_dir = self.get_project_raw_directory(project_id)
        for file_path in raw_dir.iterdir():
            if file_path.is_file():
                info["raw_files"].append({
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
                info["total_size"] += file_path.stat().st_size
        
        # ENclipfile
        clips_dir = self.get_project_clips_directory(project_id)
        for file_path in clips_dir.iterdir():
            if file_path.is_file() and file_path.suffix == '.mp4':
                info["clips"].append({
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
                info["total_size"] += file_path.stat().st_size
        
        # ENcollectionfile
        collections_dir = self.get_project_collections_directory(project_id)
        for file_path in collections_dir.iterdir():
            if file_path.is_file() and file_path.suffix == '.mp4':
                info["collections"].append({
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
                info["total_size"] += file_path.stat().st_size
        
        # ENfile
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

# EN
_storage_manager = None

def get_storage_manager() -> UnifiedStorageManager:
    """fetchEN"""
    global _storage_manager
    if _storage_manager is None:
        _storage_manager = UnifiedStorageManager()
    return _storage_manager

