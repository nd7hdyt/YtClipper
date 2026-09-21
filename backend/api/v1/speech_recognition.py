"""
Speech recognition config API.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
from backend.utils.speech_recognizer import (
    SpeechRecognitionMethod, 
    SpeechRecognitionConfig, 
    SpeechRecognizer,
    generate_subtitle_for_video
)
from backend.core.desktop_config import (
    get_desktop_config, 
    save_desktop_config, 
    DesktopConfig,
    SpeechRecognitionSettings,
    WhisperConfig,
    ApiConfig
)
from backend.services.whisper_model_manager import (
    get_model_manager, 
    WhisperModelManager,
    ModelInfo,
    ModelStatus
)
from backend.services.speech_config_validator import get_config_validator

logger = logging.getLogger(__name__)
router = APIRouter()

# Global speech recognizer instance
_speech_recognizer: Optional[SpeechRecognizer] = None

def get_speech_recognizer() -> SpeechRecognizer:
    """Get the speech recognizer instance"""
    global _speech_recognizer
    if _speech_recognizer is None:
        _speech_recognizer = SpeechRecognizer()
    return _speech_recognizer


# ===== Whisper runtime (installed on demand) =====

@router.get("/whisper/runtime-status")
async def whisper_runtime_status():
    """Whisper runtime install status (polled by the frontend)."""
    from backend.services import whisper_runtime
    return whisper_runtime.get_status()


@router.post("/whisper/install")
async def whisper_install():
    """Start installing the Whisper runtime (mlx-whisper) in the background."""
    from backend.services import whisper_runtime
    if sys_is_not_darwin():
        raise HTTPException(status_code=400, detail="mlx-whisper requires Apple Silicon (macOS)")
    return whisper_runtime.start_install()


@router.post("/whisper/uninstall")
async def whisper_uninstall():
    """Uninstall the Whisper runtime (downloaded model cache can be removed separately)."""
    from backend.services import whisper_runtime
    return whisper_runtime.uninstall()


def sys_is_not_darwin() -> bool:
    import sys
    return sys.platform != "darwin"

class SpeechConfigRequest(BaseModel):
    """Speech recognition config request"""
    method: str
    model: Optional[str] = "base"
    openaiApiKey: Optional[str] = None
    aliyunApiKey: Optional[str] = None
    enableTimestamps: Optional[bool] = True
    enablePunctuation: Optional[bool] = True
    enableSpeakerDiarization: Optional[bool] = False
    enableFallback: Optional[bool] = True
    fallbackMethod: Optional[str] = "whisper_local"
    timeout: Optional[int] = 1800  # 30 minutes; fits Whisper model processing
    outputFormat: Optional[str] = "srt"

class SpeechConfigResponse(BaseModel):
    """Speech recognition config response"""
    method: str
    model: str
    openaiApiKey: Optional[str] = None
    aliyunApiKey: Optional[str] = None
    enableTimestamps: bool
    enablePunctuation: bool
    enableSpeakerDiarization: bool
    enableFallback: bool
    fallbackMethod: str
    timeout: int
    outputFormat: str

class SpeechMethodStatus(BaseModel):
    """Speech recognition method status"""
    method: str
    available: bool
    message: Optional[str] = None

class WhisperModelInfo(BaseModel):
    """Whisper model info"""
    name: str
    size: str
    sizeBytes: int
    description: str
    accuracy: str
    speed: str
    status: str  # 'available' | 'downloading' | 'downloaded' | 'error'
    downloadProgress: Optional[int] = None

class TestSpeechServiceRequest(BaseModel):
    """Test speech service request"""
    method: str

class TestSpeechServiceResponse(BaseModel):
    """Test speech service response"""
    success: bool
    message: str

class DownloadModelRequest(BaseModel):
    """Download model request"""
    model: str

@router.get("/speech-recognition/config")
async def get_speech_config(config: DesktopConfig = Depends(get_desktop_config)):
    """Get the speech recognition config"""
    try:
        speech_config = config.speech_recognition
        
        return {
            "method": speech_config.method,
            "whisper_config": {
                "model_name": speech_config.whisper_config.model_name,
                "language": speech_config.whisper_config.language,
                "custom_models_dir": speech_config.whisper_config.custom_models_dir,
                "enable_timestamps": speech_config.whisper_config.enable_timestamps,
                "enable_punctuation": speech_config.whisper_config.enable_punctuation,
                "enable_speaker_diarization": speech_config.whisper_config.enable_speaker_diarization,
                "timeout": speech_config.whisper_config.timeout
            },
            "openai_config": {
                "api_key": speech_config.openai_config.api_key,
                "language": speech_config.openai_config.language,
                "enable_timestamps": speech_config.openai_config.enable_timestamps,
                "enable_punctuation": speech_config.openai_config.enable_punctuation
            },
            "azure_config": {
                "api_key": speech_config.azure_config.api_key,
                "region": speech_config.azure_config.region,
                "language": speech_config.azure_config.language,
                "enable_timestamps": speech_config.azure_config.enable_timestamps,
                "enable_punctuation": speech_config.azure_config.enable_punctuation
            },
            "google_config": {
                "api_key": speech_config.google_config.api_key,
                "language": speech_config.google_config.language,
                "enable_timestamps": speech_config.google_config.enable_timestamps,
                "enable_punctuation": speech_config.google_config.enable_punctuation
            },
            "aliyun_config": {
                "api_key": speech_config.aliyun_config.api_key,
                "language": speech_config.aliyun_config.language,
                "enable_timestamps": speech_config.aliyun_config.enable_timestamps,
                "enable_punctuation": speech_config.aliyun_config.enable_punctuation
            },
            "custom_api_config": {
                "api_key": speech_config.custom_api_config.api_key,
                "endpoint": speech_config.custom_api_config.endpoint,
                "language": speech_config.custom_api_config.language,
                "enable_timestamps": speech_config.custom_api_config.enable_timestamps,
                "enable_punctuation": speech_config.custom_api_config.enable_punctuation
            },
            "enable_fallback": speech_config.enable_fallback,
            "fallback_method": speech_config.fallback_method,
            "output_format": speech_config.output_format
        }
    except Exception as e:
        logger.error(f"Failed to get speech recognition config: {e}")
        raise HTTPException(status_code=500, detail="Failed to get speech recognition config")

class SpeechConfigUpdateRequest(BaseModel):
    """Speech recognition config update request"""
    method: str
    whisper_config: Optional[Dict[str, Any]] = None
    openai_config: Optional[Dict[str, Any]] = None
    azure_config: Optional[Dict[str, Any]] = None
    google_config: Optional[Dict[str, Any]] = None
    aliyun_config: Optional[Dict[str, Any]] = None
    custom_api_config: Optional[Dict[str, Any]] = None
    enable_fallback: Optional[bool] = None
    fallback_method: Optional[str] = None
    output_format: Optional[str] = None


@router.put("/speech-recognition/config")
async def update_speech_config(
    request: SpeechConfigUpdateRequest,
    config: DesktopConfig = Depends(get_desktop_config)
):
    """Update the speech recognition config"""
    try:
        # Validate the method
        try:
            method = SpeechRecognitionMethod(request.method)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Unsupported speech recognition method: {request.method}")

        # Validate the fallback method
        if request.fallback_method:
            try:
                fallback_method = SpeechRecognitionMethod(request.fallback_method)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Unsupported fallback method: {request.fallback_method}")

        # Update the config
        speech_config = config.speech_recognition
        speech_config.method = request.method

        # Update Whisper config
        if request.whisper_config:
            for key, value in request.whisper_config.items():
                if hasattr(speech_config.whisper_config, key):
                    setattr(speech_config.whisper_config, key, value)

        # Update API configs
        if request.openai_config:
            for key, value in request.openai_config.items():
                if hasattr(speech_config.openai_config, key):
                    setattr(speech_config.openai_config, key, value)

        if request.azure_config:
            for key, value in request.azure_config.items():
                if hasattr(speech_config.azure_config, key):
                    setattr(speech_config.azure_config, key, value)

        if request.google_config:
            for key, value in request.google_config.items():
                if hasattr(speech_config.google_config, key):
                    setattr(speech_config.google_config, key, value)

        if request.aliyun_config:
            for key, value in request.aliyun_config.items():
                if hasattr(speech_config.aliyun_config, key):
                    setattr(speech_config.aliyun_config, key, value)

        if request.custom_api_config:
            for key, value in request.custom_api_config.items():
                if hasattr(speech_config.custom_api_config, key):
                    setattr(speech_config.custom_api_config, key, value)

        # Update misc config
        if request.enable_fallback is not None:
            speech_config.enable_fallback = request.enable_fallback

        if request.fallback_method:
            speech_config.fallback_method = request.fallback_method

        if request.output_format:
            speech_config.output_format = request.output_format

        # Save the config
        if save_desktop_config(config):
            logger.info(f"Speech recognition config updated: {request.method}")
            return {"message": "Speech recognition config updated", "success": True}
        else:
            raise HTTPException(status_code=500, detail="Failed to save config")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update speech recognition config: {e}")
        raise HTTPException(status_code=500, detail="Failed to update speech recognition config")

@router.get("/speech-methods-status", response_model=List[SpeechMethodStatus])
async def get_speech_methods_status():
    """Get speech recognition method statuses"""
    try:
        recognizer = get_speech_recognizer()
        available_methods = recognizer.get_available_methods()

        status_list = []
        for method in SpeechRecognitionMethod:
            available = available_methods.get(method, False)
            message = None

            if not available:
                if method == SpeechRecognitionMethod.WHISPER_LOCAL:
                    message = "Whisper needs to be installed"
                elif method == SpeechRecognitionMethod.OPENAI_API:
                    message = "An OpenAI API key is required"
                elif method == SpeechRecognitionMethod.ALIYUN_SPEECH:
                    message = "An Alibaba Cloud API key is required"
                else:
                    message = "Service unavailable"

            status_list.append(SpeechMethodStatus(
                method=method.value,
                available=available,
                message=message
            ))

        return status_list

    except Exception as e:
        logger.error(f"Failed to get speech method statuses: {e}")
        raise HTTPException(status_code=500, detail="Failed to get speech method statuses")

@router.get("/whisper-models")
async def get_whisper_models():
    """Get Whisper model info"""
    try:
        model_manager = get_model_manager()
        models_info = model_manager.get_all_models_info()
        
        models = []
        for model_info in models_info:
            models.append({
                "name": model_info.name,
                "size": model_info.size,
                "sizeBytes": model_info.size_bytes,
                "description": model_info.description,
                "accuracy": model_info.accuracy,
                "speed": model_info.speed,
                "status": model_info.status.value,
                "downloadProgress": model_info.download_progress,
                "localPath": model_info.local_path,
                "errorMessage": model_info.error_message
            })
        
        return models
        
    except Exception as e:
        logger.error(f"Failed to get Whisper model info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get Whisper model info")

@router.post("/test-speech-service", response_model=TestSpeechServiceResponse)
async def test_speech_service(request: TestSpeechServiceRequest):
    """Test the speech recognition service"""
    try:
        recognizer = get_speech_recognizer()
        available_methods = recognizer.get_available_methods()

        try:
            method = SpeechRecognitionMethod(request.method)
        except ValueError:
            return TestSpeechServiceResponse(
                success=False,
                message=f"Unsupported speech recognition method: {request.method}"
            )

        if available_methods.get(method, False):
            return TestSpeechServiceResponse(
                success=True,
                message=f"{method.value} service is available"
            )
        else:
            return TestSpeechServiceResponse(
                success=False,
                message=f"{method.value} service is unavailable; check the configuration"
            )

    except Exception as e:
        logger.error(f"Failed to test speech service: {e}")
        return TestSpeechServiceResponse(
            success=False,
            message=f"Test failed: {str(e)}"
        )

@router.post("/whisper-models/download")
async def download_whisper_model(request: DownloadModelRequest):
    """Download a Whisper model"""
    try:
        model_manager = get_model_manager()

        # Skip if the model already exists
        model_info = model_manager.get_model_info(request.model)
        if model_info and model_info.status == ModelStatus.DOWNLOADED:
            return {"message": f"Model {request.model} already exists", "success": True}

        # Start the download
        success = await model_manager.download_model(request.model)

        if success:
            return {"message": f"Model {request.model} downloaded", "success": True}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to download model {request.model}")

    except Exception as e:
        logger.error(f"Failed to download Whisper model: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to download Whisper model: {str(e)}")

@router.delete("/whisper-models/{model_name}")
async def delete_whisper_model(model_name: str):
    """Delete a Whisper model"""
    try:
        model_manager = get_model_manager()

        # Check the model exists
        model_info = model_manager.get_model_info(model_name)
        if not model_info or model_info.status != ModelStatus.DOWNLOADED:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")

        # Delete the model
        success = model_manager.delete_model(model_name)

        if success:
            return {"message": f"Model {model_name} deleted", "success": True}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete model {model_name}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete Whisper model: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete Whisper model: {str(e)}")


@router.get("/whisper-models/{model_name}/status")
async def get_model_status(model_name: str):
    """Get model status"""
    try:
        model_manager = get_model_manager()
        model_info = model_manager.get_model_info(model_name)
        
        if not model_info:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        
        return {
            "name": model_info.name,
            "status": model_info.status.value,
            "downloadProgress": model_info.download_progress,
            "localPath": model_info.local_path,
            "errorMessage": model_info.error_message
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get model status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get model status: {str(e)}")


@router.post("/whisper-models/{model_name}/cancel-download")
async def cancel_model_download(model_name: str):
    """Cancel a model download"""
    try:
        model_manager = get_model_manager()
        success = model_manager.cancel_download(model_name)

        if success:
            return {"message": f"Download of model {model_name} cancelled", "success": True}
        else:
            return {"message": f"Model {model_name} is not downloading", "success": False}

    except Exception as e:
        logger.error(f"Failed to cancel model download: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cancel model download: {str(e)}")


@router.post("/speech-recognition/validate")
async def validate_speech_config(
    request: SpeechConfigUpdateRequest,
    config: DesktopConfig = Depends(get_desktop_config)
):
    """Validate the speech transcription config"""
    try:
        # Build a temp config object for validation
        temp_config = config.speech_recognition.copy()

        # Apply the updates
        temp_config.method = request.method

        if request.whisper_config:
            for key, value in request.whisper_config.items():
                if hasattr(temp_config.whisper_config, key):
                    setattr(temp_config.whisper_config, key, value)

        if request.openai_config:
            for key, value in request.openai_config.items():
                if hasattr(temp_config.openai_config, key):
                    setattr(temp_config.openai_config, key, value)

        if request.azure_config:
            for key, value in request.azure_config.items():
                if hasattr(temp_config.azure_config, key):
                    setattr(temp_config.azure_config, key, value)

        if request.google_config:
            for key, value in request.google_config.items():
                if hasattr(temp_config.google_config, key):
                    setattr(temp_config.google_config, key, value)

        if request.aliyun_config:
            for key, value in request.aliyun_config.items():
                if hasattr(temp_config.aliyun_config, key):
                    setattr(temp_config.aliyun_config, key, value)

        if request.custom_api_config:
            for key, value in request.custom_api_config.items():
                if hasattr(temp_config.custom_api_config, key):
                    setattr(temp_config.custom_api_config, key, value)

        if request.enable_fallback is not None:
            temp_config.enable_fallback = request.enable_fallback

        if request.fallback_method:
            temp_config.fallback_method = request.fallback_method

        if request.output_format:
            temp_config.output_format = request.output_format

        # Validate the config
        validator = get_config_validator()
        validation_result = validator.validate_config(temp_config)

        return {
            "valid": validation_result["valid"],
            "errors": validation_result["errors"],
            "warnings": validation_result["warnings"],
            "recommendations": validation_result["recommendations"]
        }

    except Exception as e:
        logger.error(f"Failed to validate speech transcription config: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to validate config: {str(e)}")


@router.get("/speech-recognition/recommendations")
async def get_speech_recommendations():
    """Get speech transcription config recommendations"""
    try:
        recommendations = {
            "scenarios": {
                "beginner": {
                    "method": "whisper_local",
                    "model": "base",
                    "description": "Free and offline; balanced accuracy and speed"
                },
                "pro": {
                    "method": "openai_api",
                    "model": "whisper-1",
                    "description": "Highest accuracy; for important content"
                },
                "chinese_content": {
                    "method": "aliyun_speech",
                    "model": "default",
                    "description": "Better recognition for Chinese content"
                },
                "enterprise": {
                    "method": "azure_speech",
                    "model": "default",
                    "description": "Enterprise-grade; stable and reliable"
                }
            },
            "model_guide": {
                "tiny": {
                    "size": "39 MB",
                    "speed": "fastest",
                    "accuracy": "lower",
                    "recommended_for": "Realtime processing, quick previews"
                },
                "base": {
                    "size": "74 MB",
                    "speed": "fast",
                    "accuracy": "medium",
                    "recommended_for": "Daily use; balanced choice"
                },
                "small": {
                    "size": "244 MB",
                    "speed": "medium",
                    "accuracy": "good",
                    "recommended_for": "Important content, knowledge videos"
                },
                "medium": {
                    "size": "769 MB",
                    "speed": "slower",
                    "accuracy": "high",
                    "recommended_for": "Professional use, speeches"
                },
                "large": {
                    "size": "1550 MB",
                    "speed": "slowest",
                    "accuracy": "highest",
                    "recommended_for": "Important projects with top quality requirements"
                }
            },
            "tips": [
                "First-time users: download the base model for testing",
                "Use local Whisper models when the network is unstable",
                "Alibaba Cloud speech recognition is recommended for Chinese content",
                "Enable the fallback mechanism for important projects",
                "Speaker diarization increases processing time",
                "Check model status regularly to keep the service available"
            ]
        }

        return recommendations

    except Exception as e:
        logger.error(f"Failed to get config recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")