"""
translatedconfigverifyservice
translatedverifyconfig'stranslatedAndtranslated
"""
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from backend.core.desktop_config import SpeechRecognitionSettings, WhisperConfig, ApiConfig
from backend.services.whisper_model_manager import get_model_manager, ModelStatus

logger = logging.getLogger(__name__)


class SpeechConfigValidator:
    """translatedconfigverifytranslated"""
    
    def __init__(self):
        self.model_manager = get_model_manager()
    
    def validate_config(self, config: SpeechRecognitionSettings) -> Dict[str, any]:
        """
        verifytranslatedconfig
        
        Args:
            config: translatedconfig
            
        Returns:
            verifytranslated
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        # verifytranslated
        method_validation = self._validate_method(config.method)
        if not method_validation["valid"]:
            result["valid"] = False
            result["errors"].extend(method_validation["errors"])
        
        # verifytranslatedconfig
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
        
        # verifytranslatedconfig
        if config.enable_fallback:
            fallback_validation = self._validate_fallback_config(config)
            if not fallback_validation["valid"]:
                result["warnings"].extend(fallback_validation["warnings"])
        
        return result
    
    def _validate_method(self, method: str) -> Dict[str, any]:
        """verifytranslatedSelectselect"""
        valid_methods = [
            "whisper_local", "openai_api", "azure_speech", 
            "google_speech", "aliyun_speech", "custom_api"
        ]
        
        if method not in valid_methods:
            return {
                "valid": False,
                "errors": [f"translatedsupport'stranslated: {method}"]
            }
        
        return {"valid": True, "errors": []}
    
    def _validate_whisper_config(self, config: WhisperConfig) -> Dict[str, any]:
        """verifyWhisperconfig"""
        result = {"valid": True, "errors": [], "warnings": [], "recommendations": []}
        
        # verifymodeltranslated
        valid_models = ["tiny", "base", "small", "medium", "large"]
        if config.model_name not in valid_models:
            result["valid"] = False
            result["errors"].append(f"translatedsupport'sWhispermodel: {config.model_name}")
        
        # checkmodelIstranslateddownload
        model_info = self.model_manager.get_model_info(config.model_name)
        if model_info and model_info.status != ModelStatus.DOWNLOADED:
            if model_info.status == ModelStatus.AVAILABLE:
                result["warnings"].append(f"model {config.model_name} translateddownload，translatedusetranslateddownload")
            elif model_info.status == ModelStatus.DOWNLOADING:
                result["warnings"].append(f"model {config.model_name} translatedindownloadtranslated")
            elif model_info.status == ModelStatus.ERROR:
                result["errors"].append(f"model {config.model_name} downloadfailed")
        
        # verifytranslated
        if config.timeout < 60:
            result["warnings"].append("translated，translated60seconds")
        elif config.timeout > 7200:
            result["warnings"].append("translated，translated2translated")
        
        # verifytranslatedmodeldirectory
        if config.custom_models_dir:
            custom_dir = Path(config.custom_models_dir)
            if not custom_dir.exists():
                result["errors"].append(f"translatedmodeldirectorynot found: {config.custom_models_dir}")
            elif not custom_dir.is_dir():
                result["errors"].append(f"translatedmodeldirectorytranslatedIstranslateddirectory: {config.custom_models_dir}")
        
        # addrecommend
        if config.model_name == "tiny":
            result["recommendations"].append("tinymodeltranslated，translatedusetranslatedReal-time Processing")
        elif config.model_name == "base":
            result["recommendations"].append("basemodelIstranslatedSelectselect，recommendtranslateduse")
        elif config.model_name in ["small", "medium", "large"]:
            result["recommendations"].append(f"{config.model_name}modeltranslated，translated")
        
        return result
    
    def _validate_api_config(self, config: SpeechRecognitionSettings, method: str) -> Dict[str, any]:
        """verifyAPIconfig"""
        result = {"valid": True, "errors": [], "warnings": [], "recommendations": []}
        
        # fetchtranslated'sAPIconfig
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
            return {"valid": False, "errors": [f"translatedsupport'sAPItranslated: {method}"]}
        
        # verifyAPIkey
        if not api_config.api_key:
            result["valid"] = False
            result["errors"].append(f"{method} APIkeytranslated")
        elif len(api_config.api_key) < 10:
            result["warnings"].append("APIkeytranslated，translatedcheckIstranslated")
        
        # verifyAzuretranslated
        if method == "azure_speech" and not api_config.region:
            result["valid"] = False
            result["errors"].append("Azure Speechservicetranslated")
        
        # verifytranslatedAPItranslated
        if method == "custom_api":
            if not api_config.endpoint:
                result["valid"] = False
                result["errors"].append("translatedAPItranslatedURL")
            elif not api_config.endpoint.startswith(("http://", "https://")):
                result["errors"].append("APItranslatedIstranslated'sHTTP/HTTPS URL")
        
        # addrecommend
        if method == "openai_api":
            result["recommendations"].append("OpenAI APItranslated，translated")
        elif method == "azure_speech":
            result["recommendations"].append("Azure Speechtranslateduse，supportmultitranslatedLanguage")
        elif method == "google_speech":
            result["recommendations"].append("Google Speechfeaturetranslated，supporttranslated")
        elif method == "aliyun_speech":
            result["recommendations"].append("translated")
        
        return result
    
    def _validate_fallback_config(self, config: SpeechRecognitionSettings) -> Dict[str, any]:
        """verifytranslatedconfig"""
        result = {"valid": True, "warnings": [], "recommendations": []}
        
        # checktranslatedIstranslatedandtranslated
        if config.fallback_method == config.method:
            result["warnings"].append("translatedandtranslated，translatedSelectselecttranslated'stranslated")
        
        # checktranslatedIstranslatedcanuse
        if config.fallback_method == "whisper_local":
            model_info = self.model_manager.get_model_info(config.whisper_config.model_name)
            if model_info and model_info.status not in [ModelStatus.DOWNLOADED, ModelStatus.AVAILABLE]:
                result["warnings"].append("translateduse'sWhispermodeltranslatedcanuse")
        
        # addrecommend
        if config.method != "whisper_local" and config.fallback_method != "whisper_local":
            result["recommendations"].append("translatedWhisperlocalmodeltranslated，ensuretranslatedcanuse")
        
        return result
    
    def get_config_recommendations(self, config: SpeechRecognitionSettings) -> List[str]:
        """fetchconfigtranslated"""
        recommendations = []
        
        # translatedusetranslatedrecommend
        if config.method == "whisper_local":
            if config.whisper_config.model_name == "tiny":
                recommendations.append("tinymodeltranslatedprocess，translated")
            elif config.whisper_config.model_name in ["medium", "large"]:
                recommendations.append("translatedmodeltranslatedprocesstranslated，translated")
        
        # translated
        if config.method != "whisper_local":
            recommendations.append("useAPIservicetranslated'stranslatedconnect")
            if config.enable_fallback and config.fallback_method == "whisper_local":
                recommendations.append("translatedconfiglocaltranslated，ensuretranslatedcanuse")
        
        # translated
        if config.whisper_config.enable_speaker_diarization:
            recommendations.append("translatedfeaturetranslatedprocesstranslated")
        
        return recommendations


# translatedverifytranslated
_validator: Optional[SpeechConfigValidator] = None


def get_config_validator() -> SpeechConfigValidator:
    """fetchconfigverifytranslated"""
    global _validator
    if _validator is None:
        _validator = SpeechConfigValidator()
    return _validator
