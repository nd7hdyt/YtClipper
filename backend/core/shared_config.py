"""
configfile - translatedAPIkey、file pathetc.configinfo
supporttranslated'sconfigtranslatedSystemAndtranslated
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pydantic import BaseModel, validator
from enum import Enum

from . import path_utils

# videotranslated
class VideoCategory(str, Enum):
    DEFAULT = "default"
    KNOWLEDGE = "knowledge"
    BUSINESS = "business"
    OPINION = "opinion"
    EXPERItranslatedCE = "experience"
    SPEECH = "speech"
    CONTtranslatedT_REVIEW = "content_review"
    translatedTERTAINMtranslatedT = "entertainment"

# videotranslatedconfig
VIDEO_CATEGORIES_CONFIG = {
    VideoCategory.DEFAULT: {
        "name": "default",
        "description": "translatedusevideotranslated，translatedusetranslated",
        "icon": "🎬",
        "color": "#4facfe"
    },
    VideoCategory.KNOWLEDGE: {
        "name": "translated",
        "description": "translated、translated、translatedetc.translated",
        "icon": "📚",
        "color": "#52c41a"
    },
    VideoCategory.BUSINESS: {
        "name": "providertranslated",
        "description": "providertranslated、translated、translatedetc.",
        "icon": "💼",
        "color": "#faad14"
    },
    VideoCategory.OPINION: {
        "name": "translated",
        "description": "translated、translated、translatedetc.",
        "icon": "💭",
        "color": "#722ed1"
    },
    VideoCategory.EXPERItranslatedCE: {
        "name": "translated",
        "description": "translated、translated、translatedusetranslatedetc.",
        "icon": "🌟",
        "color": "#13c2c2"
    },
    VideoCategory.SPEECH: {
        "name": "translated",
        "description": "translated、translated、translatedetc.translated",
        "icon": "🎤",
        "color": "#eb2f96"
    },
    VideoCategory.CONTtranslatedT_REVIEW: {
        "name": "translated",
        "description": "translated、translated、translatedetc.",
        "icon": "🎭",
        "color": "#f5222d"
    },
    VideoCategory.translatedTERTAINMtranslatedT: {
        "name": "translated",
        "description": "translated、translated、translatedetc.translated",
        "icon": "🎪",
        "color": "#fa8c16"
    }
}

# projecttranslateddirectory
PROJECT_ROOT = path_utils.get_project_root()

# translatedfile path
INPUT_DIR = PROJECT_ROOT / "input"
INPUT_VIDEO = INPUT_DIR / "input.mp4"
INPUT_SRT = INPUT_DIR / "input.srt"
INPUT_TXT = INPUT_DIR / "input.txt"

# translateddirectory
DATA_DIR = path_utils.get_data_directory()
OUTPUT_DIR = path_utils.get_output_directory()
CLIPS_DIR = OUTPUT_DIR / "clips"
COLLECTIONS_DIR = OUTPUT_DIR / "collections"
METADATA_DIR = OUTPUT_DIR / "metadata"

# Promptfile path
PROMPT_DIR = Path(__file__).parent.parent / "prompt"
PROMPT_FILES = {
    "outline": PROMPT_DIR / "translated.txt",
    "timeline": PROMPT_DIR / "translated.txt", 
    "recommendation": PROMPT_DIR / "recommendtranslated.txt",
    "title": PROMPT_DIR / "translated.txt",
    "clustering": PROMPT_DIR / "translated.txt",
    "collection_title": PROMPT_DIR / "collection_title.txt"
}

# APIconfig
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
MODEL_NAME = "qwen-plus"  # translatedmodeltranslated

# translatedconfig
SPEECH_RECOGNITION_METHOD = os.getenv("SPEECH_RECOGNITION_METHOD", "whisper_local")
SPEECH_RECOGNITION_LANGUAGE = os.getenv("SPEECH_RECOGNITION_LANGUAGE", "auto")
SPEECH_RECOGNITION_MODEL = os.getenv("SPEECH_RECOGNITION_MODEL", "base")
SPEECH_RECOGNITION_TIMEOUT = int(os.getenv("SPEECH_RECOGNITION_TIMEOUT", "1000"))

# processtranslated
CHUNK_SIZE = 5000  # translated
MIN_SCORE_THRESHOLD = 0.7  # translated
MAX_CLIPS_PER_COLLECTION = 5  # per collectiontranslatedcliptranslated

# added：translated
MIN_TOPIC_DURATION_MINUTES = 2  # translated（minutes）
MAX_TOPIC_DURATION_MINUTES = 12  # translated（minutes）
TARGET_TOPIC_DURATION_MINUTES = 5  # translated（minutes）
MIN_TOPICS_PER_CHUNK = 3  # per translated
MAX_TOPICS_PER_CHUNK = 8  # per translatedmultitranslated

# ensuretranslateddirectorytranslatedin
for dir_path in [CLIPS_DIR, COLLECTIONS_DIR, METADATA_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# translated'sconfigtranslatedSystem
class Settings(BaseModel):
    """Systemsettings"""
    dashscope_api_key: Optional[str] = ""
    model_name: str = "qwen-plus"
    chunk_size: int = 5000
    min_score_threshold: float = 0.7
    max_clips_per_collection: int = 5
    max_retries: int = 3
    timeout_seconds: int = 30
    # addedtranslated
    min_topic_duration_minutes: int = 2
    max_topic_duration_minutes: int = 12
    target_topic_duration_minutes: int = 5
    min_topics_per_chunk: int = 3
    max_topics_per_chunk: int = 8
    # translatedconfig
    speech_recognition_method: str = "whisper_local"
    speech_recognition_language: str = "auto"
    speech_recognition_model: str = "base"
    speech_recognition_timeout: int = 1000
    # BsiteUploadconfig (translated bilitool translatedfeature)
    # bilibili_auto_upload: bool = False
    # bilibili_default_tid: int = 21  # defaulttranslated：translated
    # bilibili_max_concurrent_uploads: int = 3
    # bilibili_upload_timeout_minutes: int = 30
    # bilibili_auto_generate_tags: bool = True
    # bilibili_tag_limit: int = 12
    
    @validator('min_score_threshold')
    def validate_score_threshold(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('translatedin0-1translated')
        return v
    
    @validator('chunk_size')
    def validate_chunk_size(cls, v):
        if v <= 0:
            raise ValueError('translated0')
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
    """processconfig"""
    chunk_size: int = 5000
    min_score_threshold: float = 0.7
    max_clips_per_collection: int = 5
    max_retries: int = 3
    timeout_seconds: int = 30

# @dataclass
# class BilibiliConfig:
#     """BsiteUploadconfig (translated bilitool translatedfeature)"""
#     auto_upload: bool = False
#     default_tid: int = 21  # defaulttranslated：translated
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
    """configtranslated"""
    
    def __init__(self):
        self.settings = Settings()
        self._load_settings()
        self._setup_prompt_files()
    
    def _load_settings(self):
        """translatedsettings"""
        # fromtranslated
        if os.getenv("DASHSCOPE_API_KEY"):
            self.settings.dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
        
        # fromconfigfiletranslated
        config_file = path_utils.get_settings_file_path()
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    for key, value in config_data.items():
                        if hasattr(self.settings, key):
                            setattr(self.settings, key, value)
            except Exception as e:
                print(f"translatedconfigfilefailed: {e}")
    
    def _setup_prompt_files(self):
        """settingstranslatedfile"""
        self.prompt_files = PROMPT_FILES.copy()
        
        # ensuretranslateddirectorytranslatedin
        PROMPT_DIR.mkdir(parents=True, exist_ok=True)
        
        # createdefaulttranslatedfile
        default_prompts = {
            "translated.txt": "translatedvideotranslated，translatedAndtranslated：\n\n{content}",
            "translated.txt": "translated'stranslated：\n\n{content}",
            "recommendtranslated.txt": "translated'stranslatedAndrecommendtranslated：\n\n{content}",
            "translated.txt": "translated'stranslated：\n\n{content}",
            "translated.txt": "translatedbytranslated：\n\n{content}"
        }
        
        for filename, content in default_prompts.items():
            file_path = PROMPT_DIR / filename
            if not file_path.exists():
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    print(f"createtranslatedfilefailed {filename}: {e}")
    
    def get_api_config(self) -> APIConfig:
        """fetchAPIconfig"""
        return APIConfig(
            model_name=self.settings.model_name,
            api_key=self.settings.dashscope_api_key
        )
    
    def get_processing_config(self) -> ProcessingConfig:
        """fetchprocessconfig"""
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
    #     """fetchBsiteUploadconfig (translated bilitool translatedfeature)"""
    #     return BilibiliConfig(
    #         auto_upload=self.settings.bilibili_auto_upload,
    #         default_tid=self.settings.bilibili_default_tid,
    #         max_concurrent_uploads=self.settings.bilibili_max_concurrent_uploads,
    #         upload_timeout_minutes=self.settings.bilibili_upload_timeout_minutes,
    #         auto_generate_tags=self.settings.bilibili_auto_generate_tags,
    #         tag_limit=self.settings.bilibili_tag_limit
    #     )
    
    def ensure_project_directories(self, project_id: str):
        """ensureprojectdirectorytranslatedin"""
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
            "input_dir": project_base / "raw",  # translatedrawdirectory
            "output_dir": project_base / "output",
            "clips_dir": project_base / "output" / "clips",
            "collections_dir": project_base / "output" / "collections",
            "metadata_dir": project_base / "output" / "metadata",
            "logs_dir": project_base / "logs",
            "temp_dir": project_base / "temp"
        }
    
    def update_api_key(self, api_key: str):
        """updateAPIkey"""
        self.settings.dashscope_api_key = api_key
        os.environ["DASHSCOPE_API_KEY"] = api_key
        
        # translatedconfigfile
        self._save_settings()
    
    def update_settings(self, **kwargs):
        """updatesettings"""
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
        
        self._save_settings()
    
    def _save_settings(self):
        """translatedsettingstranslatedfile"""
        config_file = path_utils.get_settings_file_path()
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings.dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"translatedconfigfilefailed: {e}")
    
    def export_config(self) -> Dict[str, Any]:
        """exportconfig"""
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
            # },  # translated bilitool translatedfeature
            "paths": {
                "project_root": str(self.get_path_config().project_root),
                "data_dir": str(self.get_path_config().data_dir),
                "uploads_dir": str(self.get_path_config().uploads_dir),
                "output_dir": str(self.get_path_config().output_dir),
                "prompt_dir": str(self.get_path_config().prompt_dir)
            }
        }

# translatedvideotranslatedfetchpromptfile path
def get_prompt_files(video_category: str = VideoCategory.DEFAULT) -> Dict[str, Path]:
    """
    translatedvideotranslatedfetchtranslated'spromptfile path
    iftranslateduse'spromptfile not found，translateddefaultpromptfile
    """
    category_prompt_dir = PROMPT_DIR / video_category
    default_prompt_files = PROMPT_FILES.copy()
    
    # iftranslateddirectorytranslatedin，translatedusetranslateduse'spromptfile
    if category_prompt_dir.exists():
        category_prompt_files = {}
        for key, default_path in default_prompt_files.items():
            category_file = category_prompt_dir / default_path.name
            if category_file.exists():
                category_prompt_files[key] = category_file
            else:
                # translateddefaultfile
                category_prompt_files[key] = default_path
        return category_prompt_files
    
    # iftranslateddirectorynot found，returndefaultpromptfile
    return default_prompt_files

# createtranslatedconfigtranslated
config_manager = ConfigManager()

def get_legacy_config() -> Dict[str, Any]:
    """fetchtranslated'sconfig"""
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
