"""
ENpathconfigEN
ENallpathconfigENfetch，ENpathEN
"""

from pathlib import Path
from typing import Dict, Any

from . import path_utils

class UnifiedPathManager:
    """ENpathEN"""
    
    def __init__(self):
        self._project_root = self._get_project_root()
        self._data_dir = path_utils.get_data_directory()
        self._output_dir = path_utils.get_output_directory()
        
        # ENdirectoryEN
        self._ensure_directories()
    
    def _get_project_root(self) -> Path:
        """fetchprojectENdirectory"""
        return path_utils.get_project_root()
    
    def _ensure_directories(self):
        """ENdirectoryEN"""
        directories = [
            self._data_dir,
            self._output_dir,
            self._output_dir / "clips",
            self._output_dir / "collections",
            self._output_dir / "metadata",
            self._data_dir / "projects",
            self._data_dir / "uploads",
            self._data_dir / "temp",
            self._data_dir / "backups"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @property
    def project_root(self) -> Path:
        """projectENdirectory"""
        return self._project_root
    
    @property
    def data_directory(self) -> Path:
        """ENdirectory"""
        return self._data_dir
    
    @property
    def output_directory(self) -> Path:
        """ENdirectory"""
        return self._output_dir
    
    @property
    def clips_directory(self) -> Path:
        """clipdirectory"""
        return self._output_dir / "clips"
    
    @property
    def collections_directory(self) -> Path:
        """collectiondirectory"""
        return self._output_dir / "collections"
    
    @property
    def metadata_directory(self) -> Path:
        """ENdirectory"""
        return self._output_dir / "metadata"
    
    @property
    def projects_directory(self) -> Path:
        """projectdirectory"""
        return self._data_dir / "projects"
    
    @property
    def uploads_directory(self) -> Path:
        """uploaddirectory"""
        return self._data_dir / "uploads"
    
    @property
    def temp_directory(self) -> Path:
        """ENdirectory"""
        return self._data_dir / "temp"
    
    @property
    def backups_directory(self) -> Path:
        """ENdirectory"""
        return self._data_dir / "backups"
    
    def get_project_directory(self, project_id: str) -> Path:
        """fetchprojectdirectory"""
        project_dir = self.projects_directory / project_id
        project_dir.mkdir(exist_ok=True)
        return project_dir
    
    def get_project_raw_directory(self, project_id: str) -> Path:
        """fetchprojectENfiledirectory"""
        raw_dir = self.get_project_directory(project_id) / "raw"
        raw_dir.mkdir(exist_ok=True)
        return raw_dir
    
    def get_project_output_directory(self, project_id: str) -> Path:
        """fetchprojectENdirectory"""
        output_dir = self.get_project_directory(project_id) / "output"
        output_dir.mkdir(exist_ok=True)
        return output_dir
    
    def get_project_clips_directory(self, project_id: str) -> Path:
        """fetchprojectclipdirectory"""
        clips_dir = self.clips_directory / project_id
        clips_dir.mkdir(exist_ok=True)
        return clips_dir
    
    def get_project_collections_directory(self, project_id: str) -> Path:
        """fetchprojectcollectiondirectory"""
        collections_dir = self.collections_directory / project_id
        collections_dir.mkdir(exist_ok=True)
        return collections_dir
    
    def get_database_path(self) -> Path:
        """fetchdatabasepath"""
        return self.data_directory / "autoclip.db"
    
    def get_settings_file_path(self) -> Path:
        """fetchsettingsfilepath"""
        return self.data_directory / "settings.json"
    
    def get_clip_file_path(self, project_id: str, clip_title: str, extension: str = "mp4") -> Path:
        """fetchclipfilepath"""
        clips_dir = self.get_project_clips_directory(project_id)
        # ENfileEN，EN
        safe_title = "".join(c for c in clip_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return clips_dir / f"{safe_title}.{extension}"
    
    def get_collection_file_path(self, project_id: str, collection_title: str, extension: str = "mp4") -> Path:
        """fetchcollectionfilepath"""
        collections_dir = self.get_project_collections_directory(project_id)
        # ENfileEN，EN
        safe_title = "".join(c for c in collection_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return collections_dir / f"{safe_title}.{extension}"
    
    def get_metadata_file_path(self, project_id: str, step_name: str, filename: str) -> Path:
        """fetchENfilepath"""
        metadata_dir = self.get_project_directory(project_id) / step_name
        metadata_dir.mkdir(exist_ok=True)
        return metadata_dir / filename
    
    def validate_paths(self) -> Dict[str, Any]:
        """validateallpathconfig"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "paths": {}
        }
        
        try:
            # checkENdirectory
            key_paths = {
                "project_root": self.project_root,
                "data_directory": self.data_directory,
                "output_directory": self.output_directory,
                "clips_directory": self.clips_directory,
                "collections_directory": self.collections_directory,
                "metadata_directory": self.metadata_directory,
                "projects_directory": self.projects_directory
            }
            
            for name, path in key_paths.items():
                validation_result["paths"][name] = str(path)
                
                if not path.exists():
                    validation_result["warnings"].append(f"directorydoes not exist: {name} = {path}")
                elif not path.is_dir():
                    validation_result["errors"].append(f"pathENdirectory: {name} = {path}")
                    validation_result["valid"] = False
            
            # checkENpath
            all_paths = list(validation_result["paths"].values())
            if len(all_paths) != len(set(all_paths)):
                validation_result["errors"].append("ENpathconfig")
                validation_result["valid"] = False
            
        except Exception as e:
            validation_result["errors"].append(f"pathvalidatefailed: {str(e)}")
            validation_result["valid"] = False
        
        return validation_result
    
    def get_path_summary(self) -> Dict[str, str]:
        """fetchpathconfigEN"""
        return {
            "project_root": str(self.project_root),
            "data_directory": str(self.data_directory),
            "output_directory": str(self.output_directory),
            "clips_directory": str(self.clips_directory),
            "collections_directory": str(self.collections_directory),
            "metadata_directory": str(self.metadata_directory),
            "projects_directory": str(self.projects_directory),
            "uploads_directory": str(self.uploads_directory),
            "temp_directory": str(self.temp_directory),
            "backups_directory": str(self.backups_directory)
        }

# ENpathEN
path_manager = UnifiedPathManager()

# ENpathEN
PROJECT_ROOT = path_manager.project_root
DATA_DIR = path_manager.data_directory
OUTPUT_DIR = path_manager.output_directory
CLIPS_DIR = path_manager.clips_directory
COLLECTIONS_DIR = path_manager.collections_directory
METADATA_DIR = path_manager.metadata_directory
PROJECTS_DIR = path_manager.projects_directory
UPLOADS_DIR = path_manager.uploads_directory
TEMP_DIR = path_manager.temp_directory
BACKUPS_DIR = path_manager.backups_directory

# EN
def get_project_directory(project_id: str) -> Path:
    """fetchprojectdirectory"""
    return path_manager.get_project_directory(project_id)

def get_clip_file_path(project_id: str, clip_title: str, extension: str = "mp4") -> Path:
    """fetchclipfilepath"""
    return path_manager.get_clip_file_path(project_id, clip_title, extension)

def get_collection_file_path(project_id: str, collection_title: str, extension: str = "mp4") -> Path:
    """fetchcollectionfilepath"""
    return path_manager.get_collection_file_path(project_id, collection_title, extension)

def validate_paths() -> Dict[str, Any]:
    """validateallpathconfig"""
    return path_manager.validate_paths()

def get_path_summary() -> Dict[str, str]:
    """fetchpathconfigEN"""
    return path_manager.get_path_summary()
