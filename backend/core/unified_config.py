"""
translatedoneconfigtranslatedSystem
translatedconfigtranslated，Providestranslatedone'sconfigtranslated
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from . import path_utils

logger = logging.getLogger(__name__)


class DatabaseConfig(BaseModel):
    """databaseconfig"""
    url: str = Field(default="sqlite:///./data/autoclip.db", description="databaseconnectURL")
    echo: bool = Field(default=False, description="IstranslatedSQLtranslated")
    pool_size: int = Field(default=5, description="connecttranslated")
    max_overflow: int = Field(default=10, description="translatedconnecttranslated")


class RedisConfig(BaseModel):
    """Redisconfig"""
    url: str = Field(default="redis://localhost:6379/0", description="RedisconnectURL")
    max_connections: int = Field(default=10, description="translatedconnecttranslated")
    socket_timeout: int = Field(default=5, description="Sockettranslated")


class APIConfig(BaseModel):
    """APIconfig"""
    dashscope_api_key: str = Field(default="", description="DashScope APIkey")
    model_name: str = Field(default="qwen-plus", description="modeltranslated")
    max_tokens: int = Field(default=4096, description="translatedtokentranslated")
    timeout: int = Field(default=30, description="APItranslated")
    max_retries: int = Field(default=3, description="translated")
    
    @validator('max_tokens')
    def validate_max_tokens(cls, v):
        if v <= 0:
            raise ValueError('max_tokenstranslated0')
        return v
    
    @validator('timeout')
    def validate_timeout(cls, v):
        if v <= 0:
            raise ValueError('timeouttranslated0')
        return v


class ProcessingConfig(BaseModel):
    """processconfig"""
    chunk_size: int = Field(default=5000, description="translated")
    min_score_threshold: float = Field(default=0.7, description="translated")
    max_clips_per_collection: int = Field(default=5, description="per collectiontranslatedcliptranslated")
    max_retries: int = Field(default=3, description="translated")
    timeout_seconds: int = Field(default=30, description="processtranslated")
    
    # translated
    min_topic_duration_minutes: int = Field(default=2, description="translated(minutes)")
    max_topic_duration_minutes: int = Field(default=12, description="translated(minutes)")
    target_topic_duration_minutes: int = Field(default=5, description="translated(minutes)")
    min_topics_per_chunk: int = Field(default=3, description="per translated")
    max_topics_per_chunk: int = Field(default=8, description="per translated")
    
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


class SpeechRecognitionConfig(BaseModel):
    """translatedconfig"""
    method: str = Field(default="whisper_local", description="translated")
    language: str = Field(default="auto", description="translatedLanguage")
    model: str = Field(default="base", description="modeltranslated")
    timeout: int = Field(default=1000, description="translated")


class BilibiliConfig(BaseModel):
    """Bsiteconfig"""
    auto_upload: bool = Field(default=False, description="IstranslatedAuto Upload")
    default_tid: int = Field(default=21, description="defaulttranslatedID")
    max_concurrent_uploads: int = Field(default=3, description="translatedUploadtranslated")
    upload_timeout_minutes: int = Field(default=30, description="Uploadtranslated(minutes)")
    auto_generate_tags: bool = Field(default=True, description="Istranslated")
    tag_limit: int = Field(default=12, description="translated")


class LoggingConfig(BaseModel):
    """logsconfig"""
    level: str = Field(default="INFO", description="logstranslated")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="logsformat")
    file: str = Field(default="backend.log", description="logsfile")
    max_size: int = Field(default=10 * 1024 * 1024, description="logsfiletranslated(translated)")
    backup_count: int = Field(default=5, description="logsfiletranslated")


class PathConfig(BaseModel):
    """pathconfig"""
    project_root: Path = Field(default_factory=path_utils.get_project_root)
    data_dir: Path = Field(default_factory=path_utils.get_data_directory)
    uploads_dir: Path = Field(default_factory=path_utils.get_uploads_directory)
    output_dir: Path = Field(default_factory=path_utils.get_output_directory)
    temp_dir: Path = Field(default_factory=path_utils.get_temp_directory)
    prompt_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "prompt")
    
    def __init__(self, **data):
        super().__init__(**data)
        # ensuretranslateddirectorytranslatedin
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, Path):
                field_value.mkdir(parents=True, exist_ok=True)


class UnifiedConfig(BaseSettings):
    """translatedoneconfigtranslated"""
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_nested_delimiter='__'
    )
    
    # translatedconfig
    environment: str = Field(default="development", description="translated")
    debug: bool = Field(default=True, description="translated")
    encryption_key: str = Field(default="", description="translatedkey")
    
    # translatedconfig
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    processing: ProcessingConfig = Field(default_factory=ProcessingConfig)
    speech_recognition: SpeechRecognitionConfig = Field(default_factory=SpeechRecognitionConfig)
    bilibili: BilibiliConfig = Field(default_factory=BilibiliConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    paths: PathConfig = Field(default_factory=PathConfig)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_from_files()
        self._setup_environment()
    
    def _load_from_files(self):
        """fromconfigfiletranslatedsettings"""
        # fromdata/settings.jsontranslated
        settings_file = self.paths.data_dir / "settings.json"
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    file_settings = json.load(f)
                    self._merge_settings(file_settings)
            except Exception as e:
                logger.warning(f"translatedconfigfilefailed: {e}")
        
        # fromtranslated
        self._load_from_env()
    
    def _merge_settings(self, settings: Dict[str, Any]):
        """translatedsettingstranslatedconfigtranslated"""
        for key, value in settings.items():
            if hasattr(self, key):
                if isinstance(getattr(self, key), BaseModel):
                    # iftranslatedIstranslatedconfigtranslated，translated
                    sub_config = getattr(self, key)
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if hasattr(sub_config, sub_key):
                                setattr(sub_config, sub_key, sub_value)
                else:
                    setattr(self, key, value)
    
    def _load_from_env(self):
        """fromtranslatedconfig"""
        # databaseconfig
        if os.getenv("DATABASE_URL"):
            self.database.url = os.getenv("DATABASE_URL")
        
        # Redisconfig
        if os.getenv("REDIS_URL"):
            self.redis.url = os.getenv("REDIS_URL")
        
        # APIconfig
        if os.getenv("DASHSCOPE_API_KEY"):
            self.api.dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
        if os.getenv("API_MODEL_NAME"):
            self.api.model_name = os.getenv("API_MODEL_NAME")
        
        # processconfig
        if os.getenv("PROCESSING_CHUNK_SIZE"):
            self.processing.chunk_size = int(os.getenv("PROCESSING_CHUNK_SIZE"))
        if os.getenv("PROCESSING_MIN_SCORE_THRESHOLD"):
            self.processing.min_score_threshold = float(os.getenv("PROCESSING_MIN_SCORE_THRESHOLD"))
        
        # logsconfig
        if os.getenv("LOG_LEVEL"):
            self.logging.level = os.getenv("LOG_LEVEL")
        if os.getenv("LOG_FILE"):
            self.logging.file = os.getenv("LOG_FILE")
    
    def _setup_environment(self):
        """settingstranslated"""
        # settingsAPIkeytranslated
        if self.api.dashscope_api_key:
            os.environ["DASHSCOPE_API_KEY"] = self.api.dashscope_api_key
        
        # settingsdatabaseURL
        os.environ["DATABASE_URL"] = self.database.url
        
        # settingsRedis URL
        os.environ["REDIS_URL"] = self.redis.url
    
    def save_to_file(self, file_path: Optional[Path] = None):
        """translatedconfigtranslatedfile"""
        if file_path is None:
            file_path = self.paths.data_dir / "settings.json"
        
        try:
            # createconfigtranslated，translatedinfo
            config_dict = self._to_safe_dict()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, ensure_ascii=False, indent=2)
            
            logger.info(f"configtranslated: {file_path}")
            
        except Exception as e:
            logger.error(f"translatedconfigfilefailed: {e}")
            raise
    
    def _to_safe_dict(self) -> Dict[str, Any]:
        """translated'stranslatedformat（translatedinfo）"""
        config_dict = {}
        
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            
            if isinstance(value, BaseModel):
                config_dict[key] = value.dict()
            else:
                config_dict[key] = value
        
        # translatedinfo
        if 'api' in config_dict and 'dashscope_api_key' in config_dict['api']:
            api_key = config_dict['api']['dashscope_api_key']
            if api_key:
                config_dict['api']['dashscope_api_key'] = api_key[:8] + "..." if len(api_key) > 8 else "***"
        
        return config_dict
    
    def update_config(self, **kwargs):
        """updateconfig"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                if isinstance(getattr(self, key), BaseModel):
                    # iftranslatedIstranslatedconfigtranslated，translatedupdate
                    sub_config = getattr(self, key)
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if hasattr(sub_config, sub_key):
                                setattr(sub_config, sub_key, sub_value)
                else:
                    setattr(self, key, value)
        
        # translatedsettingstranslated
        self._setup_environment()
        
        # translatedfile
        self.save_to_file()
    
    def get_config_summary(self) -> Dict[str, Any]:
        """fetchconfigtranslated"""
        return {
            "environment": self.environment,
            "debug": self.debug,
            "database": {
                "url": self.database.url,
                "echo": self.database.echo
            },
            "redis": {
                "url": self.redis.url
            },
            "api": {
                "model_name": self.api.model_name,
                "max_tokens": self.api.max_tokens,
                "timeout": self.api.timeout,
                "has_api_key": bool(self.api.dashscope_api_key)
            },
            "processing": {
                "chunk_size": self.processing.chunk_size,
                "min_score_threshold": self.processing.min_score_threshold,
                "max_clips_per_collection": self.processing.max_clips_per_collection
            },
            "speech_recognition": {
                "method": self.speech_recognition.method,
                "language": self.speech_recognition.language,
                "model": self.speech_recognition.model
            },
            "bilibili": {
                "auto_upload": self.bilibili.auto_upload,
                "default_tid": self.bilibili.default_tid,
                "max_concurrent_uploads": self.bilibili.max_concurrent_uploads
            },
            "logging": {
                "level": self.logging.level,
                "file": self.logging.file
            },
            "paths": {
                "data_dir": str(self.paths.data_dir),
                "uploads_dir": str(self.paths.uploads_dir),
                "output_dir": str(self.paths.output_dir),
                "temp_dir": str(self.paths.temp_dir)
            }
        }
    
    def validate_config(self) -> Dict[str, Any]:
        """verifyconfig"""
        issues = []
        
        # verifyAPIconfig
        if not self.api.dashscope_api_key:
            issues.append("DashScope APIkeytranslatedconfig")
        
        # verifypath
        for path_name, path_value in self.paths.__dict__.items():
            if isinstance(path_value, Path) and not path_value.exists():
                issues.append(f"pathnot found: {path_name} = {path_value}")
        
        # verifydatabaseconnect
        if not self.database.url:
            issues.append("databaseURLtranslatedconfig")
        
        # verifyRedisconnect
        if not self.redis.url:
            issues.append("Redis URLtranslatedconfig")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }


# translatedconfigtranslated
config = UnifiedConfig()


# translated
def get_config() -> UnifiedConfig:
    """fetchtranslatedconfigtranslated"""
    return config


def get_database_url() -> str:
    """fetchdatabaseURL"""
    return config.database.url


def get_redis_url() -> str:
    """fetchRedis URL"""
    return config.redis.url


def get_api_key() -> str:
    """fetchAPIkey"""
    return config.api.dashscope_api_key


def get_data_directory() -> Path:
    """fetchtranslateddirectory"""
    return config.paths.data_dir


def get_uploads_directory() -> Path:
    """fetchUploaddirectory"""
    return config.paths.uploads_dir


def get_output_directory() -> Path:
    """fetchtranslateddirectory"""
    return config.paths.output_dir


def get_temp_directory() -> Path:
    """fetchtranslateddirectory"""
    return config.paths.temp_dir


def get_prompt_directory() -> Path:
    """fetchtranslateddirectory"""
    return config.paths.prompt_dir


def update_api_key(api_key: str):
    """updateAPIkey"""
    config.api.dashscope_api_key = api_key
    config._setup_environment()
    config.save_to_file()


def update_processing_config(**kwargs):
    """updateprocessconfig"""
    config.update_config(processing=kwargs)


def update_bilibili_config(**kwargs):
    """updateBsiteconfig"""
    config.update_config(bilibili=kwargs)
