"""
translatedoneconfigtranslated
translateduse'stranslatedconfigtranslated
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

class APISettings(BaseModel):
    """APIconfig"""
    dashscope_api_key: str = Field(default='', validation_alias=AliasChoices('API_DASHSCOPE_API_KEY'))
    model_name: str = Field(default='qwen-plus', validation_alias=AliasChoices('API_MODEL_NAME'))
    max_tokens: int = Field(default=4096, validation_alias=AliasChoices('API_MAX_TOKtranslatedS'))
    timeout: int = Field(default=30, validation_alias=AliasChoices('API_TIMEOUT'))

class DatabaseSettings(BaseModel):
    """databaseconfig"""
    url: str = Field(default='sqlite:///./data/autoclip.db', validation_alias=AliasChoices('DATABASE_URL'))

class RedisSettings(BaseModel):
    """Redisconfig"""
    url: str = Field(default='redis://localhost:6379/0', validation_alias=AliasChoices('REDIS_URL'))

class ProcessingSettings(BaseModel):
    """processconfig"""
    chunk_size: int = Field(default=5000, validation_alias=AliasChoices('PROCESSING_CHUNK_SIZE'))
    min_score_threshold: float = Field(default=0.7, validation_alias=AliasChoices('PROCESSING_MIN_SCORE_THRESHOLD'))
    max_clips_per_collection: int = Field(default=5, validation_alias=AliasChoices('PROCESSING_MAX_CLIPS_PER_COLLECTION'))
    max_retries: int = Field(default=3, validation_alias=AliasChoices('PROCESSING_MAX_RETRIES'))

class LoggingSettings(BaseModel):
    """logsconfig"""
    level: str = Field(default='INFO', validation_alias=AliasChoices('LOG_LEVEL'))
    fmt: str = Field(default='%(asctime)s - %(name)s - %(levelname)s - %(message)s', validation_alias=AliasChoices('LOG_FORMAT'))
    file: str = Field(default='backend.log', validation_alias=AliasChoices('LOG_FILE'))

class Settings(BaseSettings):
    """translatedusesettings"""
    # translated .env + translated'stranslated，translated"Extra inputs are not permitted"
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    environment: str = Field(default='development', validation_alias=AliasChoices('translatedVIRONMtranslatedT'))
    debug: bool = Field(default=True, validation_alias=AliasChoices('DEBUG'))
    encryption_key: str = Field(default='', validation_alias=AliasChoices('translatedCRYPTION_KEY'))

    # translated，translatedusetranslated'sBaseModel
    database_url: str = Field(default='sqlite:///./data/autoclip.db', validation_alias=AliasChoices('DATABASE_URL'))
    redis_url: str = Field(default='redis://localhost:6379/0', validation_alias=AliasChoices('REDIS_URL'))
    api_dashscope_api_key: str = Field(default='', validation_alias=AliasChoices('API_DASHSCOPE_API_KEY'))
    api_model_name: str = Field(default='qwen-plus', validation_alias=AliasChoices('API_MODEL_NAME'))
    api_max_tokens: int = Field(default=4096, validation_alias=AliasChoices('API_MAX_TOKtranslatedS'))
    api_timeout: int = Field(default=30, validation_alias=AliasChoices('API_TIMEOUT'))
    processing_chunk_size: int = Field(default=5000, validation_alias=AliasChoices('PROCESSING_CHUNK_SIZE'))
    processing_min_score_threshold: float = Field(default=0.7, validation_alias=AliasChoices('PROCESSING_MIN_SCORE_THRESHOLD'))
    processing_max_clips_per_collection: int = Field(default=5, validation_alias=AliasChoices('PROCESSING_MAX_CLIPS_PER_COLLECTION'))
    processing_max_retries: int = Field(default=3, validation_alias=AliasChoices('PROCESSING_MAX_RETRIES'))
    log_level: str = Field(default='INFO', validation_alias=AliasChoices('LOG_LEVEL'))
    log_format: str = Field(default='%(asctime)s - %(name)s - %(levelname)s - %(message)s', validation_alias=AliasChoices('LOG_FORMAT'))
    log_file: str = Field(default='backend.log', validation_alias=AliasChoices('LOG_FILE'))

# translatedconfigtranslated
settings = Settings()

def get_project_root() -> Path:
    """fetchprojecttranslateddirectory"""
    # usetranslated'spathtool
    from ..core.path_utils import get_project_root as get_root
    return get_root()

def get_data_directory() -> Path:
    """fetchtranslateddirectory"""
    from ..core.path_utils import get_data_directory as get_dir
    return get_dir()

def get_uploads_directory() -> Path:
    """fetchUploadfiledirectory"""
    from ..core.path_utils import get_uploads_directory as get_dir
    return get_dir()

def get_temp_directory() -> Path:
    """fetchtranslatedfiledirectory"""
    from ..core.path_utils import get_temp_directory as get_dir
    return get_dir()

def get_output_directory() -> Path:
    """fetchtranslatedfiledirectory"""
    from ..core.path_utils import get_output_directory as get_dir
    return get_dir()

def get_database_url() -> str:
    """fetchdatabaseURL"""
    return settings.database_url

def get_redis_url() -> str:
    """fetchRedis URL"""
    return settings.redis_url

def get_api_key() -> Optional[str]:
    """fetchAPIkey"""
    return settings.api_dashscope_api_key if settings.api_dashscope_api_key else None

def get_model_config() -> Dict[str, Any]:
    """fetchmodelconfig"""
    return {
        "model_name": settings.api_model_name,
        "max_tokens": settings.api_max_tokens,
        "timeout": settings.api_timeout
    }

def get_processing_config() -> Dict[str, Any]:
    """fetchprocessconfig"""
    return {
        "chunk_size": settings.processing_chunk_size,
        "min_score_threshold": settings.processing_min_score_threshold,
        "max_clips_per_collection": settings.processing_max_clips_per_collection,
        "max_retries": settings.processing_max_retries
    }

def get_logging_config() -> Dict[str, Any]:
    """fetchlogsconfig"""
    log_format = settings.log_format
    if log_format.lower() == "json":
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    return {
        "level": settings.log_level,
        "format": log_format,
        "file": settings.log_file
    }

# translatedpathconfig
def init_paths():
    """translatedpathconfig"""
    project_root = get_project_root()
    data_dir = get_data_directory()
    uploads_dir = get_uploads_directory()
    temp_dir = get_temp_directory()
    output_dir = get_output_directory()
    
    print(f"projecttranslateddirectory: {project_root}")
    print(f"translateddirectory: {data_dir}")
    print(f"Uploaddirectory: {uploads_dir}")
    print(f"translateddirectory: {temp_dir}")
    print(f"translateddirectory: {output_dir}")

if __name__ == "__main__":
    # testconfigtranslated
    init_paths()
    print(f"databaseURL: {get_database_url()}")
    print(f"Redis URL: {get_redis_url()}")
    print(f"APIconfig: {get_model_config()}")
    print(f"processconfig: {get_processing_config()}") 
