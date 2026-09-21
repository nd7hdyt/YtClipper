"""
translatedconfigAndtranslatedsettings
ProvidesSystemtranslated'sconfigAndtranslated
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from enum import Enum


class PerformanceLevel(Enum):
    """translated"""
    LOW = "low"          # translated，translated
    MEDIUM = "medium"    # translatedetc.translated，translatedAndtranslateduse
    HIGH = "high"        # translated，translated
    CUSTOM = "custom"    # translatedconfig


class FileUploadConfig(BaseModel):
    """fileUploadconfig"""
    # translatedUploadconfig
    chunk_size: int = Field(default=2 * 1024 * 1024, description="translated(translated)")  # 2MB
    max_file_size: int = Field(default=2 * 1024 * 1024 * 1024, description="translatedfiletranslated(translated)")  # 2GB
    max_concurrent_uploads: int = Field(default=3, description="translatedUploadtranslated")
    upload_timeout: int = Field(default=1800, description="Uploadtranslated(seconds)")  # 30minutes
    
    # translatedconfig
    max_retries: int = Field(default=3, description="translated")
    retry_delay: int = Field(default=5, description="translated(seconds)")
    
    # support'sformat
    supported_video_formats: list = Field(
        default=['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'],
        description="support'svideoformat"
    )
    supported_subtitle_formats: list = Field(
        default=['.srt', '.vtt', '.ass', '.ssa'],
        description="support'ssubtitlesformat"
    )
    
    @validator('chunk_size')
    def validate_chunk_size(cls, v):
        if v <= 0 or v > 10 * 1024 * 1024:  # translated10MB
            raise ValueError('translatedin1translated10MBtranslated')
        return v
    
    @validator('max_file_size')
    def validate_max_file_size(cls, v):
        if v <= 0 or v > 10 * 1024 * 1024 * 1024:  # translated10GB
            raise ValueError('translatedfiletranslatedin1translated10GBtranslated')
        return v


class ProcessingConfig(BaseModel):
    """processconfig"""
    # translated
    max_concurrent_tasks: int = Field(default=2, description="translatedprocesstasktranslated")
    max_concurrent_workers: int = Field(default=4, description="translatedprocesstranslated")
    
    # translated
    max_memory_usage: int = Field(default=4 * 1024 * 1024 * 1024, description="translateduse(translated)")  # 4GB
    memory_check_interval: int = Field(default=30, description="translatedchecktranslated(seconds)")
    
    # processtranslated
    video_processing_timeout: int = Field(default=3600, description="videoprocesstranslated(seconds)")  # 1translated
    audio_processing_timeout: int = Field(default=1800, description="translatedprocesstranslated(seconds)")  # 30minutes
    ai_processing_timeout: int = Field(default=300, description="AIprocesstranslated(seconds)")  # 5minutes
    
    # translatedprocessconfig
    batch_size: int = Field(default=10, description="translatedprocesstranslated")
    batch_timeout: int = Field(default=600, description="translatedprocesstranslated(seconds)")  # 10minutes
    
    @validator('max_concurrent_tasks')
    def validate_max_concurrent_tasks(cls, v):
        if v <= 0 or v > 10:
            raise ValueError('translatedtasktranslatedin1translated10translated')
        return v


class CacheConfig(BaseModel):
    """cacheconfig"""
    # cachetranslated
    max_cache_size: int = Field(default=1024 * 1024 * 1024, description="translatedcachetranslated(translated)")  # 1GB
    cache_ttl: int = Field(default=3600, description="cachetranslated(seconds)")  # 1translated
    
    # cachetranslated
    enable_file_cache: bool = Field(default=True, description="translatedusefilecache")
    enable_result_cache: bool = Field(default=True, description="translatedusetranslatedcache")
    enable_metadata_cache: bool = Field(default=True, description="translatedusetranslatedcache")
    
    # cleantranslated
    cache_cleanup_interval: int = Field(default=1800, description="cachecleantranslated(seconds)")  # 30minutes
    cache_cleanup_threshold: float = Field(default=0.8, description="cachecleantranslated")  # 80%


class DatabaseConfig(BaseModel):
    """databaseconfig"""
    # connecttranslatedconfig
    pool_size: int = Field(default=10, description="connecttranslated")
    max_overflow: int = Field(default=20, description="translatedconnecttranslated")
    pool_timeout: int = Field(default=30, description="connecttranslated(seconds)")
    pool_recycle: int = Field(default=3600, description="connecttranslated(seconds)")
    
    # translated
    query_timeout: int = Field(default=30, description="translated(seconds)")
    enable_query_cache: bool = Field(default=True, description="translatedusetranslatedcache")
    
    @validator('pool_size')
    def validate_pool_size(cls, v):
        if v <= 0 or v > 100:
            raise ValueError('connecttranslatedin1translated100translated')
        return v


class PerformanceConfig(BaseModel):
    """translatedconfigtranslated"""
    level: PerformanceLevel = Field(default=PerformanceLevel.MEDIUM, description="translated")
    
    # translatedconfig
    file_upload: FileUploadConfig = Field(default_factory=FileUploadConfig)
    processing: ProcessingConfig = Field(default_factory=ProcessingConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    
    # translatedsettings
    enable_monitoring: bool = Field(default=True, description="translatedusetranslatedmonitor")
    monitoring_interval: int = Field(default=60, description="monitortranslated(seconds)")
    log_performance_metrics: bool = Field(default=True, description="translated")
    
    def get_config_for_level(self, level: PerformanceLevel) -> 'PerformanceConfig':
        """translatedfetchconfig"""
        if level == PerformanceLevel.LOW:
            return self._get_low_performance_config()
        elif level == PerformanceLevel.MEDIUM:
            return self._get_medium_performance_config()
        elif level == PerformanceLevel.HIGH:
            return self._get_high_performance_config()
        else:
            return self
    
    def _get_low_performance_config(self) -> 'PerformanceConfig':
        """translatedconfig"""
        return PerformanceConfig(
            level=PerformanceLevel.LOW,
            file_upload=FileUploadConfig(
                chunk_size=1024 * 1024,  # 1MB
                max_file_size=512 * 1024 * 1024,  # 512MB
                max_concurrent_uploads=1,
                upload_timeout=900,  # 15minutes
                max_retries=2
            ),
            processing=ProcessingConfig(
                max_concurrent_tasks=1,
                max_concurrent_workers=2,
                max_memory_usage=2 * 1024 * 1024 * 1024,  # 2GB
                video_processing_timeout=1800,  # 30minutes
                audio_processing_timeout=900,  # 15minutes
                ai_processing_timeout=180  # 3minutes
            ),
            cache=CacheConfig(
                max_cache_size=256 * 1024 * 1024,  # 256MB
                cache_ttl=1800,  # 30minutes
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
        """translatedetc.translatedconfig"""
        return PerformanceConfig(
            level=PerformanceLevel.MEDIUM,
            file_upload=FileUploadConfig(
                chunk_size=2 * 1024 * 1024,  # 2MB
                max_file_size=2 * 1024 * 1024 * 1024,  # 2GB
                max_concurrent_uploads=3,
                upload_timeout=1800,  # 30minutes
                max_retries=3
            ),
            processing=ProcessingConfig(
                max_concurrent_tasks=2,
                max_concurrent_workers=4,
                max_memory_usage=4 * 1024 * 1024 * 1024,  # 4GB
                video_processing_timeout=3600,  # 1translated
                audio_processing_timeout=1800,  # 30minutes
                ai_processing_timeout=300  # 5minutes
            ),
            cache=CacheConfig(
                max_cache_size=1024 * 1024 * 1024,  # 1GB
                cache_ttl=3600,  # 1translated
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
        """translatedconfig"""
        return PerformanceConfig(
            level=PerformanceLevel.HIGH,
            file_upload=FileUploadConfig(
                chunk_size=4 * 1024 * 1024,  # 4MB
                max_file_size=5 * 1024 * 1024 * 1024,  # 5GB
                max_concurrent_uploads=5,
                upload_timeout=3600,  # 1translated
                max_retries=5
            ),
            processing=ProcessingConfig(
                max_concurrent_tasks=4,
                max_concurrent_workers=8,
                max_memory_usage=8 * 1024 * 1024 * 1024,  # 8GB
                video_processing_timeout=7200,  # 2translated
                audio_processing_timeout=3600,  # 1translated
                ai_processing_timeout=600  # 10minutes
            ),
            cache=CacheConfig(
                max_cache_size=2 * 1024 * 1024 * 1024,  # 2GB
                cache_ttl=7200,  # 2translated
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
        """translated"""
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


# translatedconfigtranslated
performance_config = PerformanceConfig()

# translatedconfigtranslated
PERFORMANCE_LEVELS = {
    PerformanceLevel.LOW: performance_config._get_low_performance_config(),
    PerformanceLevel.MEDIUM: performance_config._get_medium_performance_config(),
    PerformanceLevel.HIGH: performance_config._get_high_performance_config(),
}


def get_performance_config(level: PerformanceLevel = PerformanceLevel.MEDIUM) -> PerformanceConfig:
    """fetchtranslated'stranslatedconfig"""
    return PERFORMANCE_LEVELS.get(level, performance_config._get_medium_performance_config())


def update_performance_config(config_dict: Dict[str, Any]) -> PerformanceConfig:
    """updatetranslatedconfig"""
    global performance_config
    
    # updateconfig
    if 'level' in config_dict:
        level = PerformanceLevel(config_dict['level'])
        performance_config = performance_config.get_config_for_level(level)
    
    # updatetranslatedconfig
    if 'file_upload' in config_dict:
        performance_config.file_upload = FileUploadConfig(**config_dict['file_upload'])
    
    if 'processing' in config_dict:
        performance_config.processing = ProcessingConfig(**config_dict['processing'])
    
    if 'cache' in config_dict:
        performance_config.cache = CacheConfig(**config_dict['cache'])
    
    if 'database' in config_dict:
        performance_config.database = DatabaseConfig(**config_dict['database'])
    
    # updatetranslatedsettings
    if 'enable_monitoring' in config_dict:
        performance_config.enable_monitoring = config_dict['enable_monitoring']
    
    if 'monitoring_interval' in config_dict:
        performance_config.monitoring_interval = config_dict['monitoring_interval']
    
    if 'log_performance_metrics' in config_dict:
        performance_config.log_performance_metrics = config_dict['log_performance_metrics']
    
    return performance_config
