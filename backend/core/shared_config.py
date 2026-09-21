"""
configfile - ENAPIEN、filepathENconfigEN
ENconfigENsystemEN
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pydantic import BaseModel, validator
from enum import Enum

from . import path_utils

# videocategoryEN
class VideoCategory(str, Enum):
    DEFAULT = "default"
    KNOWLEDGE = "knowledge"
    BUSINESS = "business"
    OPINION = "opinion"
    EXPERIENCE = "experience"
    SPEECH = "speech"
    CONTENT_REVIEW = "content_review"
    ENTERTAINMENT = "entertainment"

# videocategoryconfig
VIDEO_CATEGORIES_CONFIG = {
    VideoCategory.DEFAULT: {
        "name": "EN",
        "description": "ENvideoEN，EN",
        "icon": "🎬",
        "color": "#4facfe"
    },
    VideoCategory.KNOWLEDGE: {
        "name": "EN",
        "description": "EN、EN、EN",
        "icon": "📚",
        "color": "#52c41a"
    },
    VideoCategory.BUSINESS: {
        "name": "EN",
        "description": "ENanalysis、EN、EN",
        "icon": "💼",
        "color": "#faad14"
    },
    VideoCategory.OPINION: {
        "name": "EN",
        "description": "EN、ENanalysis、EN",
        "icon": "💭",
        "color": "#722ed1"
    },
    VideoCategory.EXPERIENCE: {
        "name": "EN",
        "description": "EN、EN、EN",
        "icon": "🌟",
        "color": "#13c2c2"
    },
    VideoCategory.SPEECH: {
        "name": "EN",
        "description": "EN、EN、EN",
        "icon": "🎤",
        "color": "#eb2f96"
    },
    VideoCategory.CONTENT_REVIEW: {
        "name": "EN",
        "description": "EN、EN、ENanalysisEN",
        "icon": "🎭",
        "color": "#f5222d"
    },
    VideoCategory.ENTERTAINMENT: {
        "name": "EN",
        "description": "EN、EN、EN",
        "icon": "🎪",
        "color": "#fa8c16"
    }
}

# projectENdirectory
PROJECT_ROOT = path_utils.get_project_root()

# ENfilepath
INPUT_DIR = PROJECT_ROOT / "input"
INPUT_VIDEO = INPUT_DIR / "input.mp4"
INPUT_SRT = INPUT_DIR / "input.srt"
INPUT_TXT = INPUT_DIR / "input.txt"

# ENdirectory
DATA_DIR = path_utils.get_data_directory()
OUTPUT_DIR = path_utils.get_output_directory()
CLIPS_DIR = OUTPUT_DIR / "clips"
COLLECTIONS_DIR = OUTPUT_DIR / "collections"
METADATA_DIR = OUTPUT_DIR / "metadata"

# Promptfilepath
PROMPT_DIR = Path(__file__).parent.parent / "prompt"
PROMPT_FILES = {
    "outline": PROMPT_DIR / "EN.txt",
    "timeline": PROMPT_DIR / "timeEN.txt", 
    "recommendation": PROMPT_DIR / "EN.txt",
    "title": PROMPT_DIR / "titlegenerate.txt",
    "clustering": PROMPT_DIR / "EN.txt",
    "collection_title": PROMPT_DIR / "collection_title.txt"
}

# APIconfig
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
MODEL_NAME = "qwen-plus"  # EN

# ENconfig
SPEECH_RECOGNITION_METHOD = os.getenv("SPEECH_RECOGNITION_METHOD", "whisper_local")
SPEECH_RECOGNITION_LANGUAGE = os.getenv("SPEECH_RECOGNITION_LANGUAGE", "auto")
SPEECH_RECOGNITION_MODEL = os.getenv("SPEECH_RECOGNITION_MODEL", "base")
SPEECH_RECOGNITION_TIMEOUT = int(os.getenv("SPEECH_RECOGNITION_TIMEOUT", "1000"))

# processingparameters
CHUNK_SIZE = 5000  # EN
MIN_SCORE_THRESHOLD = 0.7  # ENscoringEN
MAX_CLIPS_PER_COLLECTION = 5  # eachcollectionENclipEN

# EN：ENparameters
MIN_TOPIC_DURATION_MINUTES = 2  # ENduration（EN）
MAX_TOPIC_DURATION_MINUTES = 12  # ENduration（EN）
TARGET_TOPIC_DURATION_MINUTES = 5  # ENduration（EN）
MIN_TOPICS_PER_CHUNK = 3  # eachEN
MAX_TOPICS_PER_CHUNK = 8  # eachEN

# ENdirectoryEN
for dir_path in [CLIPS_DIR, COLLECTIONS_DIR, METADATA_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ENconfigENsystem
class Settings(BaseModel):
    """systemsettings"""
    dashscope_api_key: Optional[str] = ""
    model_name: str = "qwen-plus"
    chunk_size: int = 5000
    min_score_threshold: float = 0.7
    max_clips_per_collection: int = 5
    max_retries: int = 3
    timeout_seconds: int = 30
    # ENparameters
    min_topic_duration_minutes: int = 2
    max_topic_duration_minutes: int = 12
    target_topic_duration_minutes: int = 5
    min_topics_per_chunk: int = 3
    max_topics_per_chunk: int = 8
    # ENconfig
    speech_recognition_method: str = "whisper_local"
    speech_recognition_language: str = "auto"
    speech_recognition_model: str = "base"
    speech_recognition_timeout: int = 1000
    # BENuploadconfig (EN bilitool EN)
    # bilibili_auto_upload: bool = False
    # bilibili_default_tid: int = 21  # EN：EN
    # bilibili_max_concurrent_uploads: int = 3
    # bilibili_upload_timeout_minutes: int = 30
    # bilibili_auto_generate_tags: bool = True
    # bilibili_tag_limit: int = 12
    
    @validator('min_score_threshold')
    def validate_score_threshold(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('scoringENmustEN0-1EN')
        return v
    
    @validator('chunk_size')
    def validate_chunk_size(cls, v):
        if v <= 0:
            raise ValueError('ENmustEN0')
        return v

@dataclass
class APIConfig:
    """APIconfig"""
    model_name: str = "qwen-plus"
    api_key: Optional[str] = None
    base_url: str = "https://dashscope.aliyuncs.com"
    max_tokens: int = 4096

@dataclass
class ProcessingConfig:
    """processingconfig"""
    chunk_size: int = 5000
    min_score_threshold: float = 0.7
    max_clips_per_collection: int = 5
    max_retries: int = 3
    timeout_seconds: int = 30

# @dataclass
# class BilibiliConfig:
#     """BENuploadconfig (EN bilitool EN)"""
#     auto_upload: bool = False
#     default_tid: int = 21  # EN：EN
#     max_concurrent_uploads: int = 3
#     upload_timeout_minutes: int = 30
#     auto_generate_tags: bool = True
#     tag_limit: int = 12

@dataclass
class PathConfig:
    """pathconfig"""
    project_root: Path = field(default_factory=lambda: PROJECT_ROOT)
    data_dir: Path = field(default_factory=path_utils.get_data_directory)
    uploads_dir: Path = field(default_factory=path_utils.get_uploads_directory)
    output_dir: Path = field(default_factory=path_utils.get_output_directory)
    prompt_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent / "prompt")
    temp_dir: Path = field(default_factory=path_utils.get_temp_directory)

class ConfigManager:
    """configEN"""
    
    def __init__(self):
        self.settings = Settings()
        self._load_settings()
        self._setup_prompt_files()
    
    def _load_settings(self):
        """loadsettings"""
        # ENload
        if os.getenv("DASHSCOPE_API_KEY"):
            self.settings.dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
        
        # ENconfigfileload
        config_file = path_utils.get_settings_file_path()
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    for key, value in config_data.items():
                        if hasattr(self.settings, key):
                            setattr(self.settings, key, value)
            except Exception as e:
                print(f"loadconfigfilefailed: {e}")
    
    def _setup_prompt_files(self):
        """settingshintENfile"""
        self.prompt_files = PROMPT_FILES.copy()
        
        # ENhintENdirectoryEN
        PROMPT_DIR.mkdir(parents=True, exist_ok=True)
        
        # createENhintENfile
        default_prompts = {
            "EN.txt": "pleaseanalysisbelowvideoEN，EN：\n\n{content}",
            "timeEN.txt": "pleaseENbelowENtimeEN：\n\n{content}",
            "EN.txt": "pleaseENbelowEN：\n\n{content}",
            "titlegenerate.txt": "pleaseENbelowENgenerateENtitle：\n\n{content}",
            "EN.txt": "pleaseENbelowEN：\n\n{content}"
        }
        
        for filename, content in default_prompts.items():
            file_path = PROMPT_DIR / filename
            if not file_path.exists():
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    print(f"createhintENfilefailed {filename}: {e}")
    
    def get_api_config(self) -> APIConfig:
        """fetchAPIconfig"""
        return APIConfig(
            model_name=self.settings.model_name,
            api_key=self.settings.dashscope_api_key
        )
    
    def get_processing_config(self) -> ProcessingConfig:
        """fetchprocessingconfig"""
        return ProcessingConfig(
            chunk_size=self.settings.chunk_size,
            min_score_threshold=self.settings.min_score_threshold,
            max_clips_per_collection=self.settings.max_clips_per_collection,
            max_retries=self.settings.max_retries,
            timeout_seconds=self.settings.timeout_seconds
        )
    
    def get_path_config(self) -> PathConfig:
        """fetchpathconfig"""
        return PathConfig()
    
    # def get_bilibili_config(self) -> BilibiliConfig:
    #     """fetchBENuploadconfig (EN bilitool EN)"""
    #     return BilibiliConfig(
    #         auto_upload=self.settings.bilibili_auto_upload,
    #         default_tid=self.settings.bilibili_default_tid,
    #         max_concurrent_uploads=self.settings.bilibili_max_concurrent_uploads,
    #         upload_timeout_minutes=self.settings.bilibili_upload_timeout_minutes,
    #         auto_generate_tags=self.settings.bilibili_auto_generate_tags,
    #         tag_limit=self.settings.bilibili_tag_limit
    #     )
    
    def ensure_project_directories(self, project_id: str):
        """ENprojectdirectoryEN"""
        paths = self.get_project_paths(project_id)
        
        for path in paths.values():
            if isinstance(path, Path):
                path.mkdir(parents=True, exist_ok=True)
    
    def get_project_paths(self, project_id: str) -> Dict[str, Path]:
        """fetchprojectpathconfig"""
        data_dir = self.get_path_config().data_dir
        projects_dir = data_dir / "projects"
        project_base = projects_dir / project_id
        
        return {
            "project_base": project_base,
            "input_dir": project_base / "raw",  # ENrawdirectory
            "output_dir": project_base / "output",
            "clips_dir": project_base / "output" / "clips",
            "collections_dir": project_base / "output" / "collections",
            "metadata_dir": project_base / "output" / "metadata",
            "logs_dir": project_base / "logs",
            "temp_dir": project_base / "temp"
        }
    
    def update_api_key(self, api_key: str):
        """updateAPIEN"""
        self.settings.dashscope_api_key = api_key
        os.environ["DASHSCOPE_API_KEY"] = api_key
        
        # saveENconfigfile
        self._save_settings()
    
    def update_settings(self, **kwargs):
        """updatesettings"""
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
        
        self._save_settings()
    
    def _save_settings(self):
        """savesettingsENfile"""
        config_file = path_utils.get_settings_file_path()
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings.dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"saveconfigfilefailed: {e}")
    
    def export_config(self) -> Dict[str, Any]:
        """ENconfig"""
        return {
            "api_config": {
                "model_name": self.settings.model_name,
                "api_key": self.settings.dashscope_api_key[:8] + "..." if self.settings.dashscope_api_key else None
            },
            "processing_config": {
                "chunk_size": self.settings.chunk_size,
                "min_score_threshold": self.settings.min_score_threshold,
                "max_clips_per_collection": self.settings.max_clips_per_collection,
                "max_retries": self.settings.max_retries,
                "timeout_seconds": self.settings.timeout_seconds
            },
            # "bilibili_config": {
            #     "auto_upload": self.settings.bilibili_auto_upload,
            #     "default_tid": self.settings.bilibili_default_tid,
            #     "max_concurrent_uploads": self.settings.bilibili_max_concurrent_uploads,
            #     "upload_timeout_minutes": self.settings.bilibili_upload_timeout_minutes,
            #     "auto_generate_tags": self.settings.bilibili_auto_generate_tags,
            #     "tag_limit": self.settings.bilibili_tag_limit
            # },  # EN bilitool EN
            "paths": {
                "project_root": str(self.get_path_config().project_root),
                "data_dir": str(self.get_path_config().data_dir),
                "uploads_dir": str(self.get_path_config().uploads_dir),
                "output_dir": str(self.get_path_config().output_dir),
                "prompt_dir": str(self.get_path_config().prompt_dir)
            }
        }

# ENvideocategoryfetchpromptfilepath
def get_prompt_files(video_category: str = VideoCategory.DEFAULT) -> Dict[str, Path]:
    """
    ENvideocategoryfetchENpromptfilepath
    ifcategoryENpromptfiledoes not exist，thenENpromptfile
    """
    category_prompt_dir = PROMPT_DIR / video_category
    default_prompt_files = PROMPT_FILES.copy()
    
    # ifcategorydirectoryEN，ENusecategoryENpromptfile
    if category_prompt_dir.exists():
        category_prompt_files = {}
        for key, default_path in default_prompt_files.items():
            category_file = category_prompt_dir / default_path.name
            if category_file.exists():
                category_prompt_files[key] = category_file
            else:
                # ENfile
                category_prompt_files[key] = default_path
        return category_prompt_files
    
    # ifcategorydirectorydoes not exist，returnENpromptfile
    return default_prompt_files

# createENconfigEN
config_manager = ConfigManager()

def get_legacy_config() -> Dict[str, Any]:
    """fetchENconfig"""
    return {
        'PROJECT_ROOT': PROJECT_ROOT,
        'INPUT_DIR': INPUT_DIR,
        'INPUT_VIDEO': INPUT_VIDEO,
        'INPUT_SRT': INPUT_SRT,
        'INPUT_TXT': INPUT_TXT,
        'OUTPUT_DIR': OUTPUT_DIR,
        'CLIPS_DIR': CLIPS_DIR,
        'COLLECTIONS_DIR': COLLECTIONS_DIR,
        'METADATA_DIR': METADATA_DIR,
        'PROMPT_DIR': PROMPT_DIR,
        'PROMPT_FILES': PROMPT_FILES,
        'DASHSCOPE_API_KEY': DASHSCOPE_API_KEY,
        'MODEL_NAME': MODEL_NAME,
        'CHUNK_SIZE': CHUNK_SIZE,
        'MIN_SCORE_THRESHOLD': MIN_SCORE_THRESHOLD,
        'MAX_CLIPS_PER_COLLECTION': MAX_CLIPS_PER_COLLECTION,
        'MIN_TOPIC_DURATION_MINUTES': MIN_TOPIC_DURATION_MINUTES,
        'MAX_TOPIC_DURATION_MINUTES': MAX_TOPIC_DURATION_MINUTES,
        'TARGET_TOPIC_DURATION_MINUTES': TARGET_TOPIC_DURATION_MINUTES,
        'MIN_TOPICS_PER_CHUNK': MIN_TOPICS_PER_CHUNK,
        'MAX_TOPICS_PER_CHUNK': MAX_TOPICS_PER_CHUNK
    }
