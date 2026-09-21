"""
ENconfigENsettings
ENsystemENconfigENparameters
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from enum import Enum


class PerformanceLevel(Enum):
    """EN"""
    LOW = "low"          # EN，EN
    MEDIUM = "medium"    # EN，ENuse
    HIGH = "high"        # EN，EN
    CUSTOM = "custom"    # ENconfig


class FileUploadConfig(BaseModel):
    """fileuploadconfig"""
    # ENuploadconfig
    chunk_size: int = Field(default=2 * 1024 * 1024, description="EN(EN)")  # 2MB
    max_file_size: int = Field(default=2 * 1024 * 1024 * 1024, description="ENfileEN(EN)")  # 2GB
    max_concurrent_uploads: int = Field(default=3, description="ENuploadEN")
    upload_timeout: int = Field(default=1800, description="uploadtimeouttime(EN)")  # 30EN
    
    # retryconfig
    max_retries: int = Field(default=3, description="ENretryEN")
    retry_delay: int = Field(default=5, description="retryEN(EN)")
    
    # EN
    supported_video_formats: list = Field(
        default=['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'],
        description="ENvideoEN"
    )
    supported_subtitle_formats: list = Field(
        default=['.srt', '.vtt', '.ass', '.ssa'],
        description="ENsubtitlesEN"
    )
    
    @validator('chunk_size')
    def validate_chunk_size(cls, v):
        if v <= 0 or v > 10 * 1024 * 1024:  # EN10MB
            raise ValueError('ENmustEN1EN10MBEN')
        return v
    
    @validator('max_file_size')
    def validate_max_file_size(cls, v):
        if v <= 0 or v > 10 * 1024 * 1024 * 1024:  # EN10GB
            raise ValueError('ENfileENmustEN1EN10GBEN')
        return v


class ProcessingConfig(BaseModel):
    """processingconfig"""
    # EN
    max_concurrent_tasks: int = Field(default=2, description="ENprocessingtaskEN")
    max_concurrent_workers: int = Field(default=4, description="EN")
    
    # EN
    max_memory_usage: int = Field(default=4 * 1024 * 1024 * 1024, description="ENuse(EN)")  # 4GB
    memory_check_interval: int = Field(default=30, description="ENcheckEN(EN)")
    
    # processingtimeout
    video_processing_timeout: int = Field(default=3600, description="videoprocessingtimeout(EN)")  # 1EN
    audio_processing_timeout: int = Field(default=1800, description="ENprocessingtimeout(EN)")  # 30EN
    ai_processing_timeout: int = Field(default=300, description="AIprocessingtimeout(EN)")  # 5EN
    
    # ENprocessingconfig
    batch_size: int = Field(default=10, description="ENprocessingEN")
    batch_timeout: int = Field(default=600, description="ENprocessingtimeout(EN)")  # 10EN
    
    @validator('max_concurrent_tasks')
    def validate_max_concurrent_tasks(cls, v):
        if v <= 0 or v > 10:
            raise ValueError('ENtaskENmustEN1EN10EN')
        return v


class CacheConfig(BaseModel):
    """cacheconfig"""
    # cacheEN
    max_cache_size: int = Field(default=1024 * 1024 * 1024, description="ENcacheEN(EN)")  # 1GB
    cache_ttl: int = Field(default=3600, description="cacheENtime(EN)")  # 1EN
    
    # cacheEN
    enable_file_cache: bool = Field(default=True, description="ENfilecache")
    enable_result_cache: bool = Field(default=True, description="ENresultcache")
    enable_metadata_cache: bool = Field(default=True, description="ENcache")
    
    # EN
    cache_cleanup_interval: int = Field(default=1800, description="cacheEN(EN)")  # 30EN
    cache_cleanup_threshold: float = Field(default=0.8, description="cacheEN")  # 80%


class DatabaseConfig(BaseModel):
    """databaseconfig"""
    # connectENconfig
    pool_size: int = Field(default=10, description="connectEN")
    max_overflow: int = Field(default=20, description="ENconnectEN")
    pool_timeout: int = Field(default=30, description="connectENtimeout(EN)")
    pool_recycle: int = Field(default=3600, description="connectENtime(EN)")
    
    # EN
    query_timeout: int = Field(default=30, description="ENtimeout(EN)")
    enable_query_cache: bool = Field(default=True, description="ENcache")
    
    @validator('pool_size')
    def validate_pool_size(cls, v):
        if v <= 0 or v > 100:
            raise ValueError('connectENmustEN1EN100EN')
        return v


class PerformanceConfig(BaseModel):
    """ENconfigEN"""
    level: PerformanceLevel = Field(default=PerformanceLevel.MEDIUM, description="EN")
    
    # ENconfig
    file_upload: FileUploadConfig = Field(default_factory=FileUploadConfig)
    processing: ProcessingConfig = Field(default_factory=ProcessingConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    
    # ENsettings
    enable_monitoring: bool = Field(default=True, description="EN")
    monitoring_interval: int = Field(default=60, description="EN(EN)")
    log_performance_metrics: bool = Field(default=True, description="EN")
    
    def get_config_for_level(self, level: PerformanceLevel) -> 'PerformanceConfig':
        """ENfetchconfig"""
        if level == PerformanceLevel.LOW:
            return self._get_low_performance_config()
        elif level == PerformanceLevel.MEDIUM:
            return self._get_medium_performance_config()
        elif level == PerformanceLevel.HIGH:
            return self._get_high_performance_config()
        else:
            return self
    
    def _get_low_performance_config(self) -> 'PerformanceConfig':
        """ENconfig"""
        return PerformanceConfig(
            level=PerformanceLevel.LOW,
            file_upload=FileUploadConfig(
                chunk_size=1024 * 1024,  # 1MB
                max_file_size=512 * 1024 * 1024,  # 512MB
                max_concurrent_uploads=1,
                upload_timeout=900,  # 15EN
                max_retries=2
            ),
            processing=ProcessingConfig(
                max_concurrent_tasks=1,
                max_concurrent_workers=2,
                max_memory_usage=2 * 1024 * 1024 * 1024,  # 2GB
                video_processing_timeout=1800,  # 30EN
                audio_processing_timeout=900,  # 15EN
                ai_processing_timeout=180  # 3EN
            ),
            cache=CacheConfig(
                max_cache_size=256 * 1024 * 1024,  # 256MB
                cache_ttl=1800,  # 30EN
                enable_file_cache=False,
                enable_result_cache=True,
                enable_metadata_cache=True
            ),
            database=DatabaseConfig(
                pool_size=5,
                max_overflow=10,
                enable_query_cache=False
            )
        )
    
    def _get_medium_performance_config(self) -> 'PerformanceConfig':
        """ENconfig"""
        return PerformanceConfig(
            level=PerformanceLevel.MEDIUM,
            file_upload=FileUploadConfig(
                chunk_size=2 * 1024 * 1024,  # 2MB
                max_file_size=2 * 1024 * 1024 * 1024,  # 2GB
                max_concurrent_uploads=3,
                upload_timeout=1800,  # 30EN
                max_retries=3
            ),
            processing=ProcessingConfig(
                max_concurrent_tasks=2,
                max_concurrent_workers=4,
                max_memory_usage=4 * 1024 * 1024 * 1024,  # 4GB
                video_processing_timeout=3600,  # 1EN
                audio_processing_timeout=1800,  # 30EN
                ai_processing_timeout=300  # 5EN
            ),
            cache=CacheConfig(
                max_cache_size=1024 * 1024 * 1024,  # 1GB
                cache_ttl=3600,  # 1EN
                enable_file_cache=True,
                enable_result_cache=True,
                enable_metadata_cache=True
            ),
            database=DatabaseConfig(
                pool_size=10,
                max_overflow=20,
                enable_query_cache=True
            )
        )
    
    def _get_high_performance_config(self) -> 'PerformanceConfig':
        """ENconfig"""
        return PerformanceConfig(
            level=PerformanceLevel.HIGH,
            file_upload=FileUploadConfig(
                chunk_size=4 * 1024 * 1024,  # 4MB
                max_file_size=5 * 1024 * 1024 * 1024,  # 5GB
                max_concurrent_uploads=5,
                upload_timeout=3600,  # 1EN
                max_retries=5
            ),
            processing=ProcessingConfig(
                max_concurrent_tasks=4,
                max_concurrent_workers=8,
                max_memory_usage=8 * 1024 * 1024 * 1024,  # 8GB
                video_processing_timeout=7200,  # 2EN
                audio_processing_timeout=3600,  # 1EN
                ai_processing_timeout=600  # 10EN
            ),
            cache=CacheConfig(
                max_cache_size=2 * 1024 * 1024 * 1024,  # 2GB
                cache_ttl=7200,  # 2EN
                enable_file_cache=True,
                enable_result_cache=True,
                enable_metadata_cache=True
            ),
            database=DatabaseConfig(
                pool_size=20,
                max_overflow=40,
                enable_query_cache=True
            )
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """EN"""
        return {
            "level": self.level.value,
            "file_upload": self.file_upload.dict(),
            "processing": self.processing.dict(),
            "cache": self.cache.dict(),
            "database": self.database.dict(),
            "enable_monitoring": self.enable_monitoring,
            "monitoring_interval": self.monitoring_interval,
            "log_performance_metrics": self.log_performance_metrics
        }


# ENconfigEN
performance_config = PerformanceConfig()

# ENconfigEN
PERFORMANCE_LEVELS = {
    PerformanceLevel.LOW: performance_config._get_low_performance_config(),
    PerformanceLevel.MEDIUM: performance_config._get_medium_performance_config(),
    PerformanceLevel.HIGH: performance_config._get_high_performance_config(),
}


def get_performance_config(level: PerformanceLevel = PerformanceLevel.MEDIUM) -> PerformanceConfig:
    """fetchENconfig"""
    return PERFORMANCE_LEVELS.get(level, performance_config._get_medium_performance_config())


def update_performance_config(config_dict: Dict[str, Any]) -> PerformanceConfig:
    """updateENconfig"""
    global performance_config
    
    # updateconfig
    if 'level' in config_dict:
        level = PerformanceLevel(config_dict['level'])
        performance_config = performance_config.get_config_for_level(level)
    
    # updateENconfig
    if 'file_upload' in config_dict:
        performance_config.file_upload = FileUploadConfig(**config_dict['file_upload'])
    
    if 'processing' in config_dict:
        performance_config.processing = ProcessingConfig(**config_dict['processing'])
    
    if 'cache' in config_dict:
        performance_config.cache = CacheConfig(**config_dict['cache'])
    
    if 'database' in config_dict:
        performance_config.database = DatabaseConfig(**config_dict['database'])
    
    # updateENsettings
    if 'enable_monitoring' in config_dict:
        performance_config.enable_monitoring = config_dict['enable_monitoring']
    
    if 'monitoring_interval' in config_dict:
        performance_config.monitoring_interval = config_dict['monitoring_interval']
    
    if 'log_performance_metrics' in config_dict:
        performance_config.log_performance_metrics = config_dict['log_performance_metrics']
    
    return performance_config
