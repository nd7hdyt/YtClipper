"""
ENtranscriptionconfigvalidateservice
ENvalidateconfigEN
"""
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from backend.core.desktop_config import SpeechRecognitionSettings, WhisperConfig, ApiConfig
from backend.services.whisper_model_manager import get_model_manager, ModelStatus

logger = logging.getLogger(__name__)


class SpeechConfigValidator:
    """ENtranscriptionconfigvalidateEN"""
    
    def __init__(self):
        self.model_manager = get_model_manager()
    
    def validate_config(self, config: SpeechRecognitionSettings) -> Dict[str, any]:
        """
        validateENtranscriptionconfig
        
        Args:
            config: ENtranscriptionconfig
            
        Returns:
            validateresultEN
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        # validateEN
        method_validation = self._validate_method(config.method)
        if not method_validation["valid"]:
            result["valid"] = False
            result["errors"].extend(method_validation["errors"])
        
        # validateENconfig
        if config.method == "whisper_local":
            whisper_validation = self._validate_whisper_config(config.whisper_config)
            if not whisper_validation["valid"]:
                result["valid"] = False
                result["errors"].extend(whisper_validation["errors"])
            result["warnings"].extend(whisper_validation["warnings"])
            result["recommendations"].extend(whisper_validation["recommendations"])
        
        elif config.method in ["openai_api", "azure_speech", "google_speech", "aliyun_speech", "custom_api"]:
            api_validation = self._validate_api_config(config, config.method)
            if not api_validation["valid"]:
                result["valid"] = False
                result["errors"].extend(api_validation["errors"])
            result["warnings"].extend(api_validation["warnings"])
            result["recommendations"].extend(api_validation["recommendations"])
        
        # validateENconfig
        if config.enable_fallback:
            fallback_validation = self._validate_fallback_config(config)
            if not fallback_validation["valid"]:
                result["warnings"].extend(fallback_validation["warnings"])
        
        return result
    
    def _validate_method(self, method: str) -> Dict[str, any]:
        """validateEN"""
        valid_methods = [
            "whisper_local", "openai_api", "azure_speech", 
            "google_speech", "aliyun_speech", "custom_api"
        ]
        
        if method not in valid_methods:
            return {
                "valid": False,
                "errors": [f"EN: {method}"]
            }
        
        return {"valid": True, "errors": []}
    
    def _validate_whisper_config(self, config: WhisperConfig) -> Dict[str, any]:
        """validateWhisperconfig"""
        result = {"valid": True, "errors": [], "warnings": [], "recommendations": []}
        
        # validateEN
        valid_models = ["tiny", "base", "small", "medium", "large"]
        if config.model_name not in valid_models:
            result["valid"] = False
            result["errors"].append(f"ENWhisperEN: {config.model_name}")
        
        # checkENdownload
        model_info = self.model_manager.get_model_info(config.model_name)
        if model_info and model_info.status != ModelStatus.DOWNLOADED:
            if model_info.status == ModelStatus.AVAILABLE:
                result["warnings"].append(f"EN {config.model_name} ENdownload，ENuseENdownload")
            elif model_info.status == ModelStatus.DOWNLOADING:
                result["warnings"].append(f"EN {config.model_name} currentlydownloadEN")
            elif model_info.status == ModelStatus.ERROR:
                result["errors"].append(f"EN {config.model_name} downloadfailed")
        
        # validatetimeouttime
        if config.timeout < 60:
            result["warnings"].append("timeouttimeEN，suggestionEN60EN")
        elif config.timeout > 7200:
            result["warnings"].append("timeouttimeEN，suggestionEN2EN")
        
        # validateENdirectory
        if config.custom_models_dir:
            custom_dir = Path(config.custom_models_dir)
            if not custom_dir.exists():
                result["errors"].append(f"ENdirectorydoes not exist: {config.custom_models_dir}")
            elif not custom_dir.is_dir():
                result["errors"].append(f"ENdirectoryENdirectory: {config.custom_models_dir}")
        
        # EN
        if config.model_name == "tiny":
            result["recommendations"].append("tinyEN，suggestionENprocessing")
        elif config.model_name == "base":
            result["recommendations"].append("baseEN，ENuse")
        elif config.model_name in ["small", "medium", "large"]:
            result["recommendations"].append(f"{config.model_name}EN，EN")
        
        return result
    
    def _validate_api_config(self, config: SpeechRecognitionSettings, method: str) -> Dict[str, any]:
        """validateAPIconfig"""
        result = {"valid": True, "errors": [], "warnings": [], "recommendations": []}
        
        # fetchENAPIconfig
        if method == "openai_api":
            api_config = config.openai_config
        elif method == "azure_speech":
            api_config = config.azure_config
        elif method == "google_speech":
            api_config = config.google_config
        elif method == "aliyun_speech":
            api_config = config.aliyun_config
        elif method == "custom_api":
            api_config = config.custom_api_config
        else:
            return {"valid": False, "errors": [f"ENAPIEN: {method}"]}
        
        # validateAPIEN
        if not api_config.api_key:
            result["valid"] = False
            result["errors"].append(f"{method} APIEN")
        elif len(api_config.api_key) < 10:
            result["warnings"].append("APIEN，pleasecheckEN")
        
        # validateAzureEN
        if method == "azure_speech" and not api_config.region:
            result["valid"] = False
            result["errors"].append("Azure SpeechserviceneedEN")
        
        # validateENAPIEN
        if method == "custom_api":
            if not api_config.endpoint:
                result["valid"] = False
                result["errors"].append("ENAPIneedENURL")
            elif not api_config.endpoint.startswith(("http://", "https://")):
                result["errors"].append("APIENmustENHTTP/HTTPS URL")
        
        # EN
        if method == "openai_api":
            result["recommendations"].append("OpenAI APIEN，ENneedEN")
        elif method == "azure_speech":
            result["recommendations"].append("Azure SpeechEN，EN")
        elif method == "google_speech":
            result["recommendations"].append("Google SpeechEN，EN")
        elif method == "aliyun_speech":
            result["recommendations"].append("EN")
        
        return result
    
    def _validate_fallback_config(self, config: SpeechRecognitionSettings) -> Dict[str, any]:
        """validateENconfig"""
        result = {"valid": True, "warnings": [], "recommendations": []}
        
        # checkEN
        if config.fallback_method == config.method:
            result["warnings"].append("EN，suggestionEN")
        
        # checkEN
        if config.fallback_method == "whisper_local":
            model_info = self.model_manager.get_model_info(config.whisper_config.model_name)
            if model_info and model_info.status not in [ModelStatus.DOWNLOADED, ModelStatus.AVAILABLE]:
                result["warnings"].append("ENuseENWhisperEN")
        
        # EN
        if config.method != "whisper_local" and config.fallback_method != "whisper_local":
            result["recommendations"].append("suggestionENWhisperEN，EN")
        
        return result
    
    def get_config_recommendations(self, config: SpeechRecognitionSettings) -> List[str]:
        """fetchconfigsuggestion"""
        recommendations = []
        
        # ENuseEN
        if config.method == "whisper_local":
            if config.whisper_config.model_name == "tiny":
                recommendations.append("tinyENprocessing，EN")
            elif config.whisper_config.model_name in ["medium", "large"]:
                recommendations.append("ENprocessingtimeEN，EN")
        
        # ENsuggestion
        if config.method != "whisper_local":
            recommendations.append("useAPIserviceneedENconnect")
            if config.enable_fallback and config.fallback_method == "whisper_local":
                recommendations.append("ENconfigEN，EN")
        
        # ENsuggestion
        if config.whisper_config.enable_speaker_diarization:
            recommendations.append("ENprocessingtime")
        
        return recommendations


# ENvalidateEN
_validator: Optional[SpeechConfigValidator] = None


def get_config_validator() -> SpeechConfigValidator:
    """fetchconfigvalidateEN"""
    global _validator
    if _validator is None:
        _validator = SpeechConfigValidator()
    return _validator
