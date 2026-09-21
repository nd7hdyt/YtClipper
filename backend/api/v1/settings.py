"""
Settings management API endpoints.
Provides settings management for the Desktop client.
"""

import os
import json
import shutil
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel, Field, validator

logger = logging.getLogger(__name__)

from backend.core.desktop_config import get_desktop_config, is_desktop_mode, DesktopConfig, save_desktop_config
from backend.services.config_sync_service import config_sync_service
from pathlib import Path

router = APIRouter(prefix="/settings", tags=["settings"])


class BasicSettings(BaseModel):
    """Basic settings"""
    app_name: str = Field(default="AutoClip Desktop", description="App name")
    app_version: str = Field(default="1.0.0", description="App version")
    debug_mode: bool = Field(default=False, description="Debug mode")
    auto_start: bool = Field(default=True, description="Auto start")


class ServiceSettings(BaseModel):
    """Service settings"""
    host: str = Field(default="127.0.0.1", description="Service host")
    port: int = Field(default=8000, description="Service port")
    max_memory_usage: int = Field(default=2048, description="Max memory usage (MB)")

    @validator('port')
    def validate_port(cls, v):
        if not 1024 <= v <= 65535:
            raise ValueError('Port must be between 1024 and 65535')
        return v

    @validator('max_memory_usage')
    def validate_memory(cls, v):
        if not 512 <= v <= 8192:
            raise ValueError('Memory limit must be between 512 and 8192 MB')
        return v


class ApiKeys(BaseModel):
    """API key settings"""
    dashscope: str = Field(default="", description="Qwen API key")
    openai: str = Field(default="", description="OpenAI API key")
    gemini: str = Field(default="", description="Gemini API key")
    siliconflow: str = Field(default="", description="SiliconFlow API key")
    jimeng_access: str = Field(default="", description="Jimeng AI access key")
    jimeng_secret: str = Field(default="", description="Jimeng AI secret key")


class ApiSettings(BaseModel):
    """API settings"""
    api_keys: ApiKeys = Field(default_factory=ApiKeys, description="API keys")
    api_provider: str = Field(default="dashscope", description="Current LLM provider (dashscope / openai / gemini / siliconflow, or local presets ollama / lmstudio)")
    api_base_url: str = Field(default="", description="OpenAI-compatible base URL; empty means the official endpoint for provider=openai, or the preset default for local presets")
    api_model: str = Field(default="qwen-plus", description="Default model")
    api_max_tokens: int = Field(default=4096, description="Max tokens")
    api_timeout: int = Field(default=30, description="API timeout (seconds)")

    @validator('api_timeout')
    def validate_timeout(cls, v):
        if not 5 <= v <= 300:
            raise ValueError('API timeout must be between 5 and 300 seconds')
        return v


class ProcessingSettings(BaseModel):
    """Processing settings"""
    processing_chunk_size: int = Field(default=5000, description="Processing chunk size")
    processing_min_score: float = Field(default=0.7, description="Minimum score threshold")
    processing_max_clips: int = Field(default=5, description="Max clips per collection")
    processing_max_retries: int = Field(default=3, description="Max retries")

    @validator('processing_chunk_size')
    def validate_chunk_size(cls, v):
        if not 1000 <= v <= 10000:
            raise ValueError('Chunk size must be between 1000 and 10000')
        return v

    @validator('processing_min_score')
    def validate_min_score(cls, v):
        if not 0.1 <= v <= 1.0:
            raise ValueError('Minimum score threshold must be between 0.1 and 1.0')
        return v


class LogSettings(BaseModel):
    """Log settings"""
    log_level: str = Field(default="INFO", description="Log level")
    log_retention_days: int = Field(default=7, description="Log retention days")

    @validator('log_level')
    def validate_log_level(cls, v):
        if v not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            raise ValueError('Log level must be DEBUG, INFO, WARNING, or ERROR')
        return v

    @validator('log_retention_days')
    def validate_retention_days(cls, v):
        if not 1 <= v <= 30:
            raise ValueError('Log retention must be between 1 and 30 days')
        return v


class PathSettings(BaseModel):
    """Path settings"""
    data_directory: str = Field(description="Data directory")
    cache_directory: str = Field(description="Cache directory")
    temp_directory: str = Field(description="Temp directory")


class UpdateDataDirRequest(BaseModel):
    """Update data directory request"""
    new_data_directory: str = Field(description="New data directory path")
    migrate: bool = Field(default=True, description="Whether to migrate data from the old directory")


class DesktopSettings(BaseModel):
    """Full Desktop settings"""
    basic: BasicSettings = Field(default_factory=BasicSettings)
    service: ServiceSettings = Field(default_factory=ServiceSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)
    processing: ProcessingSettings = Field(default_factory=ProcessingSettings)
    logs: LogSettings = Field(default_factory=LogSettings)
    paths: Optional[PathSettings] = Field(default=None, description="Path settings")


def check_desktop_mode(relaxed: bool = False):
    """Check whether Desktop mode is active.
    With relaxed=True, allow beta installers / dev environments (return a warning instead of blocking).

    Only endpoints that truly depend on the desktop shell / local filesystem need it
    (data dir migration, backup restore, import/export, client config sync).
    Config endpoints that read settings.json, test connections, or query the current provider
    work the same in Docker / local script mode:
    settings.json lives under `get_data_directory()`, and both the API process and Celery workers
    hot-reload it by mtime.
    These endpoints used to be blocked with 400 too, forcing Docker users to edit .env (issue #100).
    """
    if not is_desktop_mode():
        if relaxed:
            return False
        raise HTTPException(status_code=400, detail="This endpoint is only available in Desktop mode")


@router.get("/desktop-mode")
async def check_desktop_mode_endpoint():
    """Check desktop mode - called by the frontend"""
    return {
        "is_desktop_mode": is_desktop_mode(),
        "environment": {
            "AUTOCLIP_DESKTOP_MODE": os.getenv("AUTOCLIP_DESKTOP_MODE"),
            "AUTOCLIP_MODE": os.getenv("AUTOCLIP_MODE"),
            "TAURI_PLATFORM": os.getenv("TAURI_PLATFORM"),
        }
    }


def _effective_llm_settings() -> Dict[str, Any]:
    """Effective provider / model / base_url seen by the LLM manager (settings.json first, then env vars).
    Returns an empty dict when unavailable; callers fall back to defaults."""
    try:
        from backend.core.llm_manager import get_llm_manager
        return get_llm_manager().get_current_provider_info()
    except Exception as e:  # noqa: BLE001
        logger.debug(f"Failed to read LLM manager state; settings page falls back to defaults: {e}")
        return {}


@router.get("/", response_model=DesktopSettings)
async def get_settings():
    """Get all settings"""
    try:
        config = get_desktop_config()

        # Try reading the saved settings file
        settings_file = config.paths.data_dir / "settings.json"
        logger.debug(f"Settings file path: {settings_file} (exists: {settings_file.exists()})")

        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)

                # Validate and return the saved settings
                settings = DesktopSettings(**saved_settings)
                return settings
            except Exception as e:
                # Fall back to defaults when reading fails
                logger.warning(f"Failed to read settings file; falling back to defaults: {e}")

        # No settings.json saved yet: in Docker / script mode the provider, model, and base_url come from env vars
        # (LLM_PROVIDER / API_MODEL_NAME / OPENAI_BASE_URL); the settings page should reflect them
        # instead of always showing Qwen
        effective = _effective_llm_settings()

        # Build path settings
        paths = PathSettings(
            data_directory=str(config.paths.data_dir),
            cache_directory=str(config.paths.cache_dir),
            temp_directory=str(config.paths.temp_dir)
        )

        # Build the full settings
        settings = DesktopSettings(
            basic=BasicSettings(
                app_name=config.app_name,
                app_version=config.app_version,
                debug_mode=config.debug_mode,
                auto_start=True  # default
            ),
            service=ServiceSettings(
                host=config.host,
                port=config.port,
                max_memory_usage=config.max_memory_usage
            ),
            api=ApiSettings(
                api_keys=ApiKeys(
                    dashscope=config.dashscope_api_key,
                    openai=config.openai_api_key,
                    gemini=config.gemini_api_key,
                    siliconflow=config.siliconflow_api_key,
                    jimeng_access="",  # default
                    jimeng_secret=""   # default
                ),
                api_provider=effective.get("provider") or "dashscope",
                api_base_url=effective.get("base_url") or "",
                api_model=effective.get("model") or config.default_model,
                api_max_tokens=config.max_tokens,
                api_timeout=config.timeout
            ),
            processing=ProcessingSettings(
                processing_chunk_size=config.chunk_size,
                processing_min_score=config.min_score_threshold,
                processing_max_clips=config.max_clips_per_collection,
                processing_max_retries=config.max_retries
            ),
            logs=LogSettings(
                log_level=config.log_level,
                log_retention_days=config.log_retention_days
            ),
            paths=paths
        )
        
        return settings

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get settings: {str(e)}")


@router.post("/paths/data-directory")
async def update_data_directory(
    new_path: str,
    migrate_data: bool = True
):
    """Update the data directory"""
    check_desktop_mode()

    try:
        from backend.core.desktop_config import set_data_dir

        result = set_data_dir(new_path, migrate_data)

        if result["success"]:
            return {
                "message": result["message"],
                "new_path": result["new_path"],
                "migrated_files": result.get("migrated_files", []),
                "failed_files": result.get("failed_files", [])
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update data directory: {str(e)}")

@router.get("/paths/data-directory")
async def get_data_directory_info():
    """Get data directory info"""
    check_desktop_mode()

    try:
        from backend.core.desktop_config import get_data_dir_info

        return get_data_dir_info()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get data directory info: {str(e)}")

@router.delete("/")
async def clear_settings(
    config: DesktopConfig = Depends(get_desktop_config)
):
    """Clear all settings"""
    try:
        # Reset config to defaults
        config.dashscope_api_key = ""
        config.openai_api_key = ""
        config.gemini_api_key = ""
        config.siliconflow_api_key = ""
        config.jimeng_access_key = ""
        config.jimeng_secret_key = ""

        # Save the config
        save_desktop_config(config)

        return {"message": "Settings cleared", "success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear settings: {str(e)}")

class TestApiRequest(BaseModel):
    provider: str
    api_key: str = ""
    base_url: Optional[str] = None   # openai only: compatible endpoint URL
    model: Optional[str] = None      # model to probe (must exist on the compatible server)

@router.post("/test-api")
async def test_api_connection(request: TestApiRequest):
    """Test the API connection"""
    try:
        from backend.core.llm_providers import normalize_base_url, OPENAI_OFFICIAL_BASE_URL
        from backend.core.local_presets import resolve_provider
        # ollama / lmstudio presets -> openai + default URL
        requested_provider = request.provider
        resolved_provider, resolved_base_url, _preset = resolve_provider(request.provider, request.base_url)
        request.provider = resolved_provider
        custom_base_url = normalize_base_url(resolved_base_url) if request.provider == "openai" else ""
        if custom_base_url == OPENAI_OFFICIAL_BASE_URL:
            custom_base_url = ""

        # Key format checks apply to official services only; self-hosted OpenAI-compatible
        # services (Ollama / vLLM etc.) often need no key
        if not custom_base_url:
            if not request.api_key or len(request.api_key.strip()) < 10:
                return {
                    "success": False,
                    "error": "API key is empty or too short; check your input",
                    "provider": request.provider
                }
            if request.provider in ["dashscope", "openai"] and not request.api_key.startswith("sk-"):
                return {
                    "success": False,
                    "error": f"{request.provider} API key format looks wrong; it usually starts with 'sk-'",
                    "provider": request.provider
                }

        model_kwargs = {"model_name": request.model} if request.model else {}

        # Test the connection per provider
        if request.provider == "dashscope":
            from backend.core.llm_providers import DashScopeProvider
            # International endpoint uses compat mode (#45); empty = China native SDK
            dashscope_base_url = normalize_base_url(request.base_url) or None
            provider_instance = DashScopeProvider(api_key=request.api_key, base_url=dashscope_base_url, **model_kwargs)
        elif request.provider == "openai":
            from backend.core.llm_providers import OpenAIProvider
            provider_instance = OpenAIProvider(api_key=request.api_key, base_url=custom_base_url or None, **model_kwargs)
        elif request.provider == "gemini":
            from backend.core.llm_providers import GeminiProvider
            provider_instance = GeminiProvider(api_key=request.api_key, **model_kwargs)
        elif request.provider == "siliconflow":
            from backend.core.llm_providers import SiliconFlowProvider
            provider_instance = SiliconFlowProvider(api_key=request.api_key, **model_kwargs)
        else:
            raise HTTPException(status_code=400, detail="Unsupported API provider")

        # Test the connection
        test_result = provider_instance.test_connection()

        if test_result:
            return {
                "success": True,
                "message": "API connection test succeeded",
                "provider": requested_provider
            }
        else:
            # More detailed error info
            error_msg = f"API connection test failed"
            if request.provider == "dashscope":
                error_msg += ". Check that the API key is correct; DashScope keys usually start with 'sk-'"
            elif request.provider == "openai" and custom_base_url:
                error_msg += f". Check that {custom_base_url} is reachable, the model name exists, and whether the service needs an API key"
            elif request.provider == "openai":
                error_msg += ". Check that the API key is correct; OpenAI keys usually start with 'sk-'"
            elif request.provider == "gemini":
                error_msg += ". Check that the API key is correct"
            elif request.provider == "siliconflow":
                error_msg += ". Check that the API key is correct"

            return {
                "success": False,
                "error": error_msg,
                "provider": request.provider
            }

    except Exception as e:
        logger.error(f"API connection test error: {str(e)}")
        return {
            "success": False,
            "error": f"API connection test failed: {str(e)}",
            "provider": request.provider
        }

@router.put("/", response_model=Dict[str, Any])
async def update_settings(settings: DesktopSettings):
    """Update settings"""
    try:
        config = get_desktop_config()

        # Update config
        config.debug_mode = settings.basic.debug_mode
        config.host = settings.service.host
        config.port = settings.service.port
        config.max_memory_usage = settings.service.max_memory_usage

        # Update API settings
        config.dashscope_api_key = settings.api.api_keys.dashscope
        config.openai_api_key = settings.api.api_keys.openai
        config.gemini_api_key = settings.api.api_keys.gemini
        config.siliconflow_api_key = settings.api.api_keys.siliconflow
        config.default_model = settings.api.api_model
        config.max_tokens = settings.api.api_max_tokens
        config.timeout = settings.api.api_timeout

        # Update processing settings
        config.chunk_size = settings.processing.processing_chunk_size
        config.min_score_threshold = settings.processing.processing_min_score
        config.max_clips_per_collection = settings.processing.processing_max_clips
        config.max_retries = settings.processing.processing_max_retries

        # Update log settings
        config.log_level = settings.logs.log_level

        # Save settings to file
        settings_file = config.paths.data_dir / "settings.json"
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings.dict(), f, indent=2, ensure_ascii=False)

        # Switch this process's LLM manager to the new provider / base_url / model now (workers pick it up via mtime)
        try:
            from backend.core.llm_manager import get_llm_manager
            get_llm_manager()._reload_if_settings_changed()
        except Exception as e:  # noqa: BLE001
            logger.warning(f"Failed to refresh LLM manager (it will reload on next call): {e}")

        # Persist the main config file so keys and other critical settings survive restarts
        from backend.core.desktop_config import save_desktop_config
        if not save_desktop_config(config):
            raise HTTPException(status_code=500, detail="Failed to save main config file")

        return {"message": "Settings updated", "settings_file": str(settings_file)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")


@router.post("/reset")
async def reset_settings():
    """Reset settings to defaults"""
    try:
        config = get_desktop_config()

        # Delete the settings file
        settings_file = config.paths.data_dir / "settings.json"
        if settings_file.exists():
            settings_file.unlink()

        # Reload defaults
        config._settings = None
        config._paths = None

        return {"message": "Settings reset to defaults"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset settings: {str(e)}")


@router.post("/paths/data-directory", response_model=Dict[str, Any])
async def update_data_directory(payload: UpdateDataDirRequest):
    """Update the data directory (optionally migrating data). Called by the first-run wizard or settings page."""
    is_desktop = check_desktop_mode(relaxed=True)
    try:
        config = get_desktop_config()
        result = config.set_data_dir(Path(payload.new_data_directory), migrate_from_old=payload.migrate)

        # Return the new path config
        paths = {
            "data_directory": str(config.paths.data_dir),
            "cache_directory": str(config.paths.cache_dir),
            "temp_directory": str(config.paths.temp_dir),
            "database_url": config.paths.database_url,
        }

        resp = {"message": "Data directory updated", "result": result, "paths": paths}
        if not is_desktop:
            resp["warning"] = "Not in Desktop mode, but the path config was updated"
        return resp
    except Exception as e:
        # Return details to help diagnose permission / path / lock issues
        return {
            "message": "Failed to update data directory (skipped in beta mode)",
            "error": str(e),
            "hint": "Make sure the target directory is writable and not restricted by the system; pick a path under your home directory if needed",
        }


@router.post("/export")
async def export_settings():
    """Export settings"""
    check_desktop_mode()

    try:
        config = get_desktop_config()
        settings = await get_settings()

        # Create the export file
        export_file = config.paths.data_dir / "autoclip-settings-export.json"
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(settings.dict(), f, indent=2, ensure_ascii=False)

        return {
            "message": "Settings exported",
            "export_file": str(export_file),
            "download_url": f"/api/v1/settings/download/{export_file.name}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export settings: {str(e)}")


@router.post("/import")
async def import_settings(file: UploadFile = File(...)):
    """Import settings"""
    check_desktop_mode()

    try:
        # Read the uploaded file
        content = await file.read()
        settings_data = json.loads(content.decode('utf-8'))

        # Validate the format
        settings = DesktopSettings(**settings_data)

        # Apply the settings
        result = await update_settings(settings)

        return {
            "message": "Settings imported",
            "imported_settings": settings.dict()
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Settings file has an invalid format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import settings: {str(e)}")


# Removed the duplicate test_api_connection function


@router.get("/validation")
async def validate_settings():
    """Validate current settings"""
    try:
        config = get_desktop_config()
        validation_result = config.validate_config()

        return {
            "valid": validation_result["valid"],
            "errors": validation_result.get("errors", []),
            "warnings": validation_result.get("warnings", []),
            "recommendations": []
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Settings validation failed: {str(e)}")


@router.get("/backup")
async def backup_settings():
    """Back up settings"""
    check_desktop_mode()

    try:
        config = get_desktop_config()
        backup_dir = config.paths.data_dir / "backups"
        backup_dir.mkdir(exist_ok=True)

        # Create the backup
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"settings_backup_{timestamp}.json"

        settings = await get_settings()
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(settings.dict(), f, indent=2, ensure_ascii=False)

        return {
            "message": "Settings backed up",
            "backup_file": str(backup_file),
            "backup_time": timestamp
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to back up settings: {str(e)}")


@router.get("/backups")
async def list_backups():
    """List all backups"""
    check_desktop_mode()

    try:
        config = get_desktop_config()
        backup_dir = config.paths.data_dir / "backups"

        if not backup_dir.exists():
            return {"backups": []}

        backups = []
        for backup_file in backup_dir.glob("settings_backup_*.json"):
            stat = backup_file.stat()
            backups.append({
                "filename": backup_file.name,
                "path": str(backup_file),
                "size": stat.st_size,
                "created_time": stat.st_ctime,
                "modified_time": stat.st_mtime
            })

        # Sort by creation time
        backups.sort(key=lambda x: x["created_time"], reverse=True)

        return {"backups": backups}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list backups: {str(e)}")


@router.get("/available-models")
async def get_available_models():
    """Get the available model list"""
    try:
        # Return models grouped by provider
        models = {
            "dashscope": [
                {"name": "qwen-plus", "display_name": "Qwen Plus", "max_tokens": 8192, "description": "Good for complex reasoning and creative tasks"},
                {"name": "qwen-turbo", "display_name": "Qwen Turbo", "max_tokens": 8192, "description": "Balanced performance and cost"},
                {"name": "qwen-max", "display_name": "Qwen Max", "max_tokens": 8192, "description": "Strongest performance for complex tasks"},
                {"name": "qwen-long", "display_name": "Qwen Long", "max_tokens": 100000, "description": "Handles extra-long text"}
            ],
            "openai": [
                {"name": "gpt-4o", "display_name": "GPT-4 Omni", "max_tokens": 128000, "description": "Latest multimodal model"},
                {"name": "gpt-4o-mini", "display_name": "GPT-4 Omni Mini", "max_tokens": 128000, "description": "Lightweight multimodal model"},
                {"name": "gpt-4-turbo", "display_name": "GPT-4 Turbo", "max_tokens": 128000, "description": "High-performance version"},
                {"name": "gpt-4", "display_name": "GPT-4", "max_tokens": 8192, "description": "Classic version"},
                {"name": "gpt-3.5-turbo", "display_name": "GPT-3.5 Turbo", "max_tokens": 16384, "description": "Budget-friendly version"}
            ],
            "gemini": [
                {"name": "gemini-1.5-pro", "display_name": "Gemini 1.5 Pro", "max_tokens": 2000000, "description": "Latest pro version"},
                {"name": "gemini-1.5-flash", "display_name": "Gemini 1.5 Flash", "max_tokens": 1000000, "description": "Fast-response version"},
                {"name": "gemini-pro", "display_name": "Gemini Pro", "max_tokens": 30720, "description": "Classic pro version"}
            ],
            "siliconflow": [
                {"name": "deepseek-chat", "display_name": "DeepSeek Chat", "max_tokens": 32768, "description": "DeepSeek chat model"},
                {"name": "deepseek-coder", "display_name": "DeepSeek Coder", "max_tokens": 16384, "description": "Code generation model"},
                {"name": "qwen-plus", "display_name": "Qwen Plus", "max_tokens": 8192, "description": "Via SiliconFlow"},
                {"name": "qwen-turbo", "display_name": "Qwen Turbo", "max_tokens": 8192, "description": "Via SiliconFlow"}
            ],
        }

        return {"models": models}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get model list: {str(e)}")


@router.get("/local-presets")
async def get_local_presets():
    """Local model presets (Ollama / LM Studio): default URLs, default models, helper copy."""
    from backend.core.local_presets import presets_as_dicts
    return {"presets": presets_as_dicts()}


@router.get("/compatible-models")
async def list_compatible_models(base_url: str = "", provider: str = "openai", api_key: str = ""):
    """
    List the models an OpenAI-compatible service (Ollama / LM Studio / vLLM...) actually serves (GET {base_url}/models).
    The settings page uses it to populate the model dropdown for local presets so users don't have
    to type names like `qwen2.5:7b` by hand.
    """
    from backend.core.local_presets import resolve_provider
    from backend.core.llm_providers import normalize_base_url, is_local_url, OPENAI_COMPATIBLE_PLACEHOLDER_KEY
    _provider, resolved_base_url, _preset = resolve_provider(provider, base_url)
    url = normalize_base_url(resolved_base_url)
    if not url:
        raise HTTPException(status_code=400, detail="Missing base_url")
    try:
        import httpx
        headers = {"Authorization": f"Bearer {api_key or OPENAI_COMPATIBLE_PLACEHOLDER_KEY}"}
        # Local URLs bypass the system proxy (otherwise tools like Clash on macOS cause 502s)
        async with httpx.AsyncClient(timeout=5.0, trust_env=not is_local_url(url)) as client:
            resp = await client.get(f"{url}/models", headers=headers)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("data", data) if isinstance(data, dict) else data
        models = sorted({str(m.get("id") or m.get("name")) for m in items if isinstance(m, dict) and (m.get("id") or m.get("name"))})
        return {"reachable": True, "base_url": url, "models": models}
    except Exception as e:  # noqa: BLE001
        # Service down / wrong URL: not a server error; the frontend shows a "service not running" hint
        return {"reachable": False, "base_url": url, "models": [], "error": str(e)[:200]}


@router.get("/current-provider")
async def get_current_provider():
    """Get current provider info"""
    try:
        # Use the LLM manager's live state (it reads the settings.json saved by the settings page),
        # instead of always returning dashscope — which made the settings page snap back to Qwen on every open.
        from backend.core.llm_manager import get_llm_manager
        info = get_llm_manager().get_current_provider_info()
        display_name = info.get("display_name") or info.get("provider") or "Alibaba Qwen"
        provider_info = {
            "provider": info.get("provider") or "dashscope",
            "model": info.get("model") or "qwen-plus",
            "available": bool(info.get("available")),
            "display_name": display_name,
            "description": f"{display_name} model service",
        }
        if info.get("base_url"):
            provider_info["base_url"] = info["base_url"]

        return provider_info

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get current provider info: {str(e)}")


@router.post("/restore/{backup_filename}")
async def restore_backup(backup_filename: str):
    """Restore settings from a backup"""
    check_desktop_mode()

    try:
        config = get_desktop_config()
        backup_file = config.paths.data_dir / "backups" / backup_filename

        if not backup_file.exists():
            raise HTTPException(status_code=404, detail="Backup file not found")

        # Read the backup file
        with open(backup_file, 'r', encoding='utf-8') as f:
            settings_data = json.load(f)

        # Validate and restore
        settings = DesktopSettings(**settings_data)
        result = await update_settings(settings)

        return {
            "message": "Settings restored",
            "restored_from": backup_filename,
            "restored_settings": settings.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restore settings: {str(e)}")


@router.post("/sync-config")
async def sync_config():
    """Manually sync client config to the backend"""
    check_desktop_mode()

    try:
        if config_sync_service.sync_from_client():
            return {
                "status": "success",
                "message": "Config synced"
            }
        else:
            return {
                "status": "error",
                "message": "Config sync failed"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Config sync failed: {str(e)}"
        }


@router.get("/config-status")
async def get_config_status():
    """Get config sync status"""
    check_desktop_mode()

    try:
        client_time = config_sync_service.get_client_config_timestamp()
        backup_time = config_sync_service.get_backup_config_timestamp()
        sync_needed = config_sync_service.is_sync_needed()

        return {
            "client_config_exists": client_time is not None,
            "backup_config_exists": backup_time is not None,
            "client_config_time": client_time,
            "backup_config_time": backup_time,
            "sync_needed": sync_needed,
            "client_config_path": str(config_sync_service.client_config_path),
            "backup_config_path": str(config_sync_service.backup_config_path)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get config status: {str(e)}"
        }