"""
ENpathEN
ENprojectENpathEN
"""

import os
from pathlib import Path
from typing import Optional

DESKTOP_TRUE_VALUES = {"1", "true", "yes", "on"}


def is_desktop_mode() -> bool:
    """ENcurrentENrunEN"""
    return (
        os.getenv("AUTOCLIP_DESKTOP_MODE", "").lower() in DESKTOP_TRUE_VALUES
        or os.getenv("AUTOCLIP_MODE", "").lower() == "desktop"
    )

def get_project_root() -> Path:
    """
    fetchprojectENdirectory
    ENbackenddirectoryEN，ENfrontendENbackendENdirectory
    """
    current_path = Path(__file__).parent  # backend/core/
    
    # ENprojectENdirectory
    while current_path.parent != current_path:  # ENdirectory
        if (current_path.parent / "frontend").exists() and (current_path.parent / "backend").exists():
            return current_path.parent
        current_path = current_path.parent
    
    # ifEN，useENpath
    return Path(__file__).parent.parent.parent

def get_data_directory() -> Path:
    """fetchENdirectory"""
    configured_data_dir = os.getenv("AUTOCLIP_DATA_DIR")
    if configured_data_dir:
        data_dir = Path(configured_data_dir).expanduser()
    elif is_desktop_mode():
        app_dir = os.getenv("AUTOCLIP_APP_DIR", "~/Library/Application Support/AutoClip")
        data_dir = Path(app_dir).expanduser()
    else:
        # ENuseprojectENdirectoryENdatadirectory，ENconfig.pyEN
        data_dir = get_project_root() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def get_projects_directory() -> Path:
    """fetchprojectdirectory"""
    projects_dir = get_data_directory() / "projects"
    projects_dir.mkdir(parents=True, exist_ok=True)
    return projects_dir

def get_output_directory() -> Path:
    """fetchENdirectory"""
    output_dir = get_data_directory() / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def get_project_directory(project_id: str) -> Path:
    """fetchprojectdirectory"""
    project_dir = get_projects_directory() / project_id
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir

def get_project_raw_directory(project_id: str) -> Path:
    """fetchprojectENfiledirectory"""
    raw_dir = get_project_directory(project_id) / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    return raw_dir

def get_project_output_directory(project_id: str) -> Path:
    """fetchprojectENdirectory"""
    output_dir = get_project_directory(project_id) / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def get_clips_directory() -> Path:
    """fetchclipdirectory"""
    clips_dir = get_output_directory() / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    return clips_dir

def get_collections_directory() -> Path:
    """fetchcollectiondirectory"""
    collections_dir = get_output_directory() / "collections"
    collections_dir.mkdir(parents=True, exist_ok=True)
    return collections_dir

def get_metadata_directory() -> Path:
    """fetchENdirectory"""
    metadata_dir = get_output_directory() / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    return metadata_dir

def get_settings_file_path() -> Path:
    """fetchsettingsfilepath"""
    return get_data_directory() / "settings.json"

def get_uploads_directory() -> Path:
    """fetchuploaddirectory"""
    uploads_dir = get_data_directory() / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    return uploads_dir

def get_temp_directory() -> Path:
    """fetchENdirectory"""
    temp_dir = get_data_directory() / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir

def ensure_directory_exists(path: Path) -> Path:
    """ENdirectoryEN"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_video_file_path(project_id: str, filename: str) -> Path:
    """fetchprojectvideofilepath"""
    return get_project_raw_directory(project_id) / filename

def get_srt_file_path(project_id: str, filename: str) -> Path:
    """fetchprojectSRTfilepath"""
    return get_project_raw_directory(project_id) / filename

def get_clip_file_path(clip_id: str, title: str) -> Path:
    """fetchclipfilepath"""
    # ENfileEN，EN
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')
    return get_clips_directory() / f"{clip_id}_{safe_title}.mp4"

def get_collection_file_path(collection_id: str, title: str) -> Path:
    """fetchcollectionfilepath"""
    # ENfileEN，EN
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')
    return get_collections_directory() / f"{collection_id}_{safe_title}.mp4"

def get_metadata_file_path(project_id: str) -> Path:
    """fetchprojectENfilepath"""
    return get_metadata_directory() / f"{project_id}_metadata.json"

def get_log_file_path() -> Path:
    """fetchlogfilepath"""
    configured_log_file = os.getenv("LOG_FILE")
    if configured_log_file:
        log_file = Path(configured_log_file).expanduser()
        log_file.parent.mkdir(parents=True, exist_ok=True)
        return log_file
    if is_desktop_mode() or os.getenv("AUTOCLIP_DATA_DIR"):
        logs_dir = get_data_directory() / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        return logs_dir / "backend.log"
    return get_project_root() / "backend.log"

def get_cache_directory() -> Path:
    """fetchcachedirectory"""
    cache_dir = get_data_directory() / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def get_backup_directory() -> Path:
    """fetchENdirectory"""
    backup_dir = get_data_directory() / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir

def cleanup_temp_files(max_age_hours: int = 24):
    """ENfile"""
    import time
    temp_dir = get_temp_directory()
    current_time = time.time()
    
    for file_path in temp_dir.iterdir():
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > (max_age_hours * 3600):
                try:
                    file_path.unlink()
                except Exception as e:
                    print(f"ENfilefailed: {file_path}, error: {e}")

def validate_file_path(file_path: Path) -> bool:
    """validatefilepathEN"""
    try:
        # checkpathENdirectoryEN
        allowed_dirs = [
            get_data_directory(),
            get_output_directory(),
            get_project_root()
        ]
        
        file_path = file_path.resolve()
        return any(file_path.is_relative_to(allowed_dir) for allowed_dir in allowed_dirs)
    except Exception:
        return False
