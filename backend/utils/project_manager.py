"""
Project Managementtool
"""
import json
import logging
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# fixedimportissue
try:
    from ..core.shared_config import config_manager
except ImportError:
    # iftranslatedimportfailed，translatedimport
    import sys
    from pathlib import Path
    backend_path = Path(__file__).parent.parent
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    from ..core.shared_config import config_manager

logger = logging.getLogger(__name__)

class ProjectManager:
    """projecttranslated"""
    
    def __init__(self):
        self.config = config_manager
    
    def create_project(self, project_name: Optional[str] = None) -> str:
        """
        createtranslatedproject
        
        Args:
            project_name: projecttranslated（canSelect）
            
        Returns:
            projectID
        """
        project_id = str(uuid.uuid4())
        project_name = project_name or f"project_{project_id[:8]}"
        
        # ensureprojectdirectorytranslatedin
        self.config.ensure_project_directories(project_id)
        
        # createprojecttranslated
        project_metadata = {
            "project_id": project_id,
            "project_name": project_name,
            "created_at": datetime.now().isoformat(),
            "status": "created",
            "current_step": 0,
            "total_steps": 6,
            "error_message": None,
            "file_info": {
                "video_file": None,
                "srt_file": None,
                "txt_file": None
            }
        }
        
        # translatedprojecttranslated
        self._save_project_metadata(project_id, project_metadata)
        
        logger.info(f"createproject: {project_id} ({project_name})")
        return project_id
    
    def get_project_paths(self, project_id: str) -> Dict[str, Path]:
        """
        fetchprojectpathconfig
        
        Args:
            project_id: projectID
            
        Returns:
            projectpathtranslated
        """
        return self.config.get_project_paths(project_id)
    
    def validate_project_exists(self, project_id: str) -> bool:
        """
        verifyprojectIstranslatedin
        
        Args:
            project_id: projectID
            
        Returns:
            projectIstranslatedin
        """
        paths = self.get_project_paths(project_id)
        return paths["project_base"].exists()
    
    def get_project_metadata(self, project_id: str) -> Dict[str, Any]:
        """
        fetchprojecttranslated
        
        Args:
            project_id: projectID
            
        Returns:
            projecttranslated
        """
        if not self.validate_project_exists(project_id):
            raise FileIOError(f"project not found: {project_id}")
        
        metadata_file = self.get_project_paths(project_id)["metadata_dir"] / "project_metadata.json"
        
        if not metadata_file.exists():
            # iftranslatedfile not found，createdefaulttranslated
            default_metadata = {
                "project_id": project_id,
                "project_name": f"project_{project_id[:8]}",
                "created_at": datetime.now().isoformat(),
                "status": "unknown",
                "current_step": 0,
                "total_steps": 6,
                "error_message": None,
                "file_info": {
                    "video_file": None,
                    "srt_file": None,
                    "txt_file": None
                }
            }
            self._save_project_metadata(project_id, default_metadata)
            return default_metadata
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise FileIOError(f"translatedprojecttranslatedfailed: {e}")
    
    def update_project_metadata(self, project_id: str, updates: Dict[str, Any]):
        """
        updateprojecttranslated
        
        Args:
            project_id: projectID
            updates: translatedupdate'stranslated
        """
        metadata = self.get_project_metadata(project_id)
        metadata.update(updates)
        metadata["updated_at"] = datetime.now().isoformat()
        
        self._save_project_metadata(project_id, metadata)
    
    def _save_project_metadata(self, project_id: str, metadata: Dict[str, Any]) -> None:
        """translatedprojecttranslated"""
        paths = self.get_project_paths(project_id)
        metadata_dir = paths["metadata_dir"]
        metadata_file = metadata_dir / "project_metadata.json"
        
        try:
            # ensuremetadatadirectorytranslatedin
            metadata_dir.mkdir(parents=True, exist_ok=True)
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise FileIOError(f"translatedprojecttranslatedfailed: {e}")
    
    def save_input_file(self, project_id: str, file_path: Path, file_type: str) -> str:
        """
        translatedfiletranslatedprojectdirectory
        
        Args:
            project_id: projectID
            file_path: translatedfile path
            file_type: filetranslated (video, srt, txt)
            
        Returns:
            translated'sfile path
        """
        if not self.validate_project_exists(project_id):
            raise FileIOError(f"project not found: {project_id}")
        
        if not file_path.exists():
            raise FileIOError(f"translatedfile not found: {file_path}")
        
        paths = self.get_project_paths(project_id)
        input_dir = paths["input_dir"]
        
        # translatedfiletranslated
        if file_type == "video":
            target_name = "input.mp4"
        elif file_type == "srt":
            target_name = "input.srt"
        elif file_type == "txt":
            target_name = "input.txt"
        else:
            raise ValidationError(f"translatedsupport'sfiletranslated: {file_type}")
        
        target_path = input_dir / target_name
        
        try:
            # translatedfile
            shutil.copy2(file_path, target_path)
            
            # updateprojecttranslated
            metadata = self.get_project_metadata(project_id)
            metadata["file_info"][f"{file_type}_file"] = str(target_path)
            self._save_project_metadata(project_id, metadata)
            
            logger.info(f"filetranslatedproject {project_id}: {target_path}")
            return str(target_path)
            
        except Exception as e:
            raise FileIOError(f"translatedfilefailed: {e}")
    
    def get_input_files(self, project_id: str) -> Dict[str, Optional[Path]]:
        """
        fetchprojecttranslatedfile
        
        Args:
            project_id: projectID
            
        Returns:
            translatedfile pathtranslated
        """
        if not self.validate_project_exists(project_id):
            raise FileIOError(f"project not found: {project_id}")
        
        paths = self.get_project_paths(project_id)
        project_base = paths["project_base"]
        input_dir = paths["input_dir"]
        
        # checktranslated cantranslated'stranslated：inputtranslateddirectoryAndprojecttranslateddirectory
        file_names = ["input.mp4", "input.srt", "input.txt"]
        file_keys = ["video_file", "srt_file", "txt_file"]
        
        files = {}
        for key, name in zip(file_keys, file_names):
            # translatedcheckinputtranslateddirectory
            input_path = input_dir / name
            if input_path.exists():
                files[key] = input_path
            else:
                # checkprojecttranslateddirectory
                root_path = project_base / name
                if root_path.exists():
                    files[key] = root_path
                else:
                    files[key] = None
        
        return files
    
    def validate_input_files(self, project_id: str) -> Dict[str, bool]:
        """
        verifyprojecttranslatedfile
        
        Args:
            project_id: projectID
            
        Returns:
            fileverifytranslated
        """
        files = self.get_input_files(project_id)
        
        validation = {
            "has_video": files["video_file"] is not None,
            "has_srt": files["srt_file"] is not None,
            "has_txt": files["txt_file"] is not None,
            "can_process": files["video_file"] is not None and files["srt_file"] is not None
        }
        
        return validation
    
    def save_processing_result(self, project_id: str, step: int, result: Dict[str, Any]):
        """
        translatedprocesstranslated
        
        Args:
            project_id: projectID
            step: processstep
            result: processtranslated
        """
        if not self.validate_project_exists(project_id):
            raise FileIOError(f"project not found: {project_id}")
        
        paths = self.get_project_paths(project_id)
        metadata_dir = paths["metadata_dir"]
        
        # ensuremetadatadirectorytranslatedin
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        # translatedsteptranslated
        step_file = metadata_dir / f"step{step}_result.json"
        
        try:
            with open(step_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            # updateprojectstatus
            self.update_project_metadata(project_id, {
                "current_step": step,
                "status": "processing" if step < 6 else "completed"
            })
            
            logger.info(f"step {step} translatedproject {project_id}")
            
        except Exception as e:
            raise FileIOError(f"translatedprocesstranslatedfailed: {e}")
    
    def get_processing_result(self, project_id: str, step: int) -> Optional[Dict[str, Any]]:
        """
        fetchprocesstranslated
        
        Args:
            project_id: projectID
            step: processstep
            
        Returns:
            processtranslated，iftranslatednot foundtranslatedreturnNone
        """
        if not self.validate_project_exists(project_id):
            raise FileIOError(f"project not found: {project_id}")
        
        paths = self.get_project_paths(project_id)
        metadata_dir = paths["metadata_dir"]
        step_file = metadata_dir / f"step{step}_result.json"
        
        if not step_file.exists():
            return None
        
        try:
            with open(step_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise FileIOError(f"translatedprocesstranslatedfailed: {e}")
    
    def save_clip(self, project_id: str, clip_data: Dict[str, Any], clip_index: int):
        """
        translatedvideoclipinfo
        
        Args:
            project_id: projectID
            clip_data: cliptranslated
            clip_index: cliptranslated
        """
        if not self.validate_project_exists(project_id):
            raise FileIOError(f"project not found: {project_id}")
        
        paths = self.get_project_paths(project_id)
        metadata_dir = paths["metadata_dir"]
        
        # ensuremetadatadirectorytranslatedin
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        # translatedcliptranslated
        clips_file = metadata_dir / "clips_metadata.json"
        clips_data = []
        
        if clips_file.exists():
            try:
                with open(clips_file, 'r', encoding='utf-8') as f:
                    clips_data = json.load(f)
            except Exception:
                clips_data = []
        
        # addtranslatedclip
        clip_data["clip_index"] = clip_index
        clip_data["created_at"] = datetime.now().isoformat()
        
        # ensuretranslatedadd
        existing_indices = [clip["clip_index"] for clip in clips_data]
        if clip_index in existing_indices:
            # updatetranslatedclip
            for i, clip in enumerate(clips_data):
                if clip["clip_index"] == clip_index:
                    clips_data[i] = clip_data
                    break
        else:
            # addtranslatedclip
            clips_data.append(clip_data)
        
        # translatedcliptranslated
        try:
            with open(clips_file, 'w', encoding='utf-8') as f:
                json.dump(clips_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"clip {clip_index} translatedproject {project_id}")
            
        except Exception as e:
            raise FileIOError(f"translatedcliptranslatedfailed: {e}")
    
    def get_clips(self, project_id: str) -> List[Dict[str, Any]]:
        """
        fetchprojecttranslatedclip
        
        Args:
            project_id: projectID
            
        Returns:
            cliplist
        """
        if not self.validate_project_exists(project_id):
            raise FileIOError(f"project not found: {project_id}")
        
        paths = self.get_project_paths(project_id)
        metadata_dir = paths["metadata_dir"]
        clips_file = metadata_dir / "clips_metadata.json"
        
        if not clips_file.exists():
            return []
        
        try:
            with open(clips_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise FileIOError(f"translatedcliptranslatedfailed: {e}")
    
    def save_collection(self, project_id: str, collection_data: Dict[str, Any]):
        """
        translatedcollectioninfo
        
        Args:
            project_id: projectID
            collection_data: collectiontranslated
        """
        if not self.validate_project_exists(project_id):
            raise FileIOError(f"project not found: {project_id}")
        
        paths = self.get_project_paths(project_id)
        metadata_dir = paths["metadata_dir"]
        
        # ensuremetadatadirectorytranslatedin
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        # translatedcollectiontranslated
        collections_file = metadata_dir / "collections_metadata.json"
        collections_data = []
        
        if collections_file.exists():
            try:
                with open(collections_file, 'r', encoding='utf-8') as f:
                    collections_data = json.load(f)
            except Exception:
                collections_data = []
        
        # addtranslatedcollection
        collection_data["created_at"] = datetime.now().isoformat()
        collections_data.append(collection_data)
        
        # translatedcollectiontranslated
        try:
            with open(collections_file, 'w', encoding='utf-8') as f:
                json.dump(collections_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"collectiontranslatedproject {project_id}")
            
        except Exception as e:
            raise FileIOError(f"translatedcollectiontranslatedfailed: {e}")
    
    def get_collections(self, project_id: str) -> List[Dict[str, Any]]:
        """
        fetchprojecttranslatedcollection
        
        Args:
            project_id: projectID
            
        Returns:
            collectionlist
        """
        if not self.validate_project_exists(project_id):
            raise FileIOError(f"project not found: {project_id}")
        
        paths = self.get_project_paths(project_id)
        metadata_dir = paths["metadata_dir"]
        collections_file = metadata_dir / "collections_metadata.json"
        
        if not collections_file.exists():
            return []
        
        try:
            with open(collections_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise FileIOError(f"translatedcollectiontranslatedfailed: {e}")
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """
        translatedproject
        
        Returns:
            projectlist
        """
        projects = []
        uploads_dir = Path(self.config.settings.uploads_dir)
        
        if not uploads_dir.exists():
            return projects
        
        for project_dir in uploads_dir.iterdir():
            if project_dir.is_dir() and not project_dir.name.startswith('.'):
                try:
                    metadata = self.get_project_metadata(project_dir.name)
                    projects.append(metadata)
                except Exception as e:
                    logger.warning(f"translatedproject {project_dir.name} translatedfailed: {e}")
        
        # bycreatetranslated
        projects.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return projects
    
    def delete_project(self, project_id: str) -> bool:
        """
        deleteproject
        
        Args:
            project_id: projectID
            
        Returns:
            Istranslateddeletesucceeded
        """
        if not self.validate_project_exists(project_id):
            logger.warning(f"project not found: {project_id}")
            return False
        
        paths = self.get_project_paths(project_id)
        project_base = paths["project_base"]
        
        try:
            shutil.rmtree(project_base)
            logger.info(f"projecttranslateddelete: {project_id}")
            return True
        except Exception as e:
            logger.error(f"deleteprojectfailed: {e}")
            return False
    
    def get_project_summary(self, project_id: str) -> Dict[str, Any]:
        """
        fetchprojecttranslatedinfo
        
        Args:
            project_id: projectID
            
        Returns:
            projecttranslated
        """
        if not self.validate_project_exists(project_id):
            raise FileIOError(f"project not found: {project_id}")
        
        metadata = self.get_project_metadata(project_id)
        validation = self.validate_input_files(project_id)
        clips = self.get_clips(project_id)
        collections = self.get_collections(project_id)
        
        return {
            "project_info": metadata,
            "file_validation": validation,
            "clips_count": len(clips),
            "collections_count": len(collections),
            "processing_progress": {
                "current_step": metadata.get("current_step", 0),
                "total_steps": metadata.get("total_steps", 6),
                "progress_percentage": (metadata.get("current_step", 0) / metadata.get("total_steps", 6)) * 100
            }
        }

# translatedProject Managementtranslated
project_manager = ProjectManager()