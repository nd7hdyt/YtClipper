"""
LLMtranslated - translatedonetranslatedmulti modelProvidesprovider
"""
import json
import logging
import os
from typing import Dict, Any, Optional, List
from pathlib import Path

from .llm_providers import (
    LLMProvider, LLMProviderFactory, ProviderType, 
    ModelInfo, LLMResponse
)
from ..services.config_sync_service import config_sync_service

logger = logging.getLogger(__name__)

class LLMManager:
    """LLMtranslated"""
    
    def __init__(self, settings_file: Optional[Path] = None):
        # intranslatedconfig
        self._sync_config_if_needed()
        
        self.settings_file = settings_file or self._get_default_settings_file()
        self.current_provider: Optional[LLMProvider] = None
        self._settings_mtime: Optional[float] = None
        self.settings = self._load_settings()
        self._initialize_provider()

    def _current_settings_mtime(self) -> Optional[float]:
        try:
            return self.settings_file.stat().st_mtime
        except OSError:
            return None

    def _reload_if_settings_changed(self) -> None:
        """Settings pagetranslated settings.json translated；API processand Celery worker translatedintranslatedonetranslatedcalltranslatedconfig，
        translatedIsetc.translated。"""
        mtime = self._current_settings_mtime()
        if mtime != self._settings_mtime:
            logger.info("translated settings.json translated，translated LLM config")
            self.settings = self._load_settings()
            self._initialize_provider()
    
    def _get_default_settings_file(self) -> Path:
        """fetchdefaultsettingsfile path"""
        # translatedusetranslatedusedirectory（andfrontendtranslatedonetranslated）
        app_dir = os.getenv("AUTOCLIP_APP_DIR")
        if app_dir:
            return Path(app_dir) / "settings.json"

        # andsettings API translated'stranslatedonetranslated（path_utils.get_data_directory），
        # translatedSettings pagetranslated A、thistranslated B，translated provider translated
        try:
            from .path_utils import get_data_directory
            return get_data_directory() / "settings.json"
        except Exception as e:  # noqa: BLE001
            logger.warning(f"translated path_utils translated settings.json，translated: {e}")
        
        # translatedusedefault'suserdirectory（macOS）- translatedconfigtranslated
        default_app_dir = Path.home() / "Library" / "Application Support" / "AutoClip"
        default_settings = default_app_dir / "settings.json"
        if default_settings.exists():
            return default_settings
            
        # translatedcheckprojectdatadirectorytranslated'ssettings.json（translated）
        project_data_dir = Path(__file__).parent.parent.parent / "data"
        project_settings = project_data_dir / "settings.json"
        if project_settings.exists():
            return project_settings
            
        # iftranslatednot found，returndefaultpath
        return default_settings
    
    def _sync_config_if_needed(self):
        """checktranslatedconfig"""
        try:
            if config_sync_service.is_sync_needed():
                logger.info("translatedconfigupdate，translated...")
                if config_sync_service.sync_from_client():
                    logger.info("configtranslated")
                else:
                    logger.warning("configtranslatedfailed")
        except Exception as e:
            logger.error(f"configtranslatedcheckfailed: {e}")
    
    def _load_settings(self) -> Dict[str, Any]:
        """translatedsettings"""
        default_settings = {
            "llm_provider": "dashscope",
            "dashscope_api_key": "",
            "openai_api_key": "",
            # OpenAI translated；translated = translated。translated OPtranslatedAI_BASE_URL translated
            "openai_base_url": os.getenv("OPtranslatedAI_BASE_URL", ""),
            # translatedsite（dashscope-intl）；translated = translatedsite。Docker use DASHSCOPE_BASE_URL
            "dashscope_base_url": os.getenv("DASHSCOPE_BASE_URL", ""),
            "gemini_api_key": "",
            "siliconflow_api_key": "",
            "model_name": "qwen-plus",
            "chunk_size": 5000,
            "min_score_threshold": 0.7,
            "max_clips_per_collection": 5
        }
        
        self._settings_mtime = self._current_settings_mtime()
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    
                    # processtranslated'sconfigformat（translatedconfig）
                    if "api" in saved_settings and "api_keys" in saved_settings["api"]:
                        api = saved_settings["api"]
                        api_keys = api["api_keys"]
                        default_settings.update({
                            "dashscope_api_key": api_keys.get("dashscope", ""),
                            "openai_api_key": api_keys.get("openai", ""),
                            "gemini_api_key": api_keys.get("gemini", ""),
                            "siliconflow_api_key": api_keys.get("siliconflow", ""),
                            "model_name": api.get("api_model", "qwen-plus")
                        })
                        # Settings pagetranslated'sProvidesprovider；translated settings.json translatedthis translated，translated dashscope
                        if api.get("api_provider"):
                            default_settings["llm_provider"] = api["api_provider"]
                        if api.get("api_base_url"):
                            # translatedone translated：openai translatedIstranslated，dashscope Istranslatedsitetranslated（#45）
                            if default_settings["llm_provider"] == "dashscope":
                                default_settings["dashscope_base_url"] = api["api_base_url"]
                            else:
                                default_settings["openai_base_url"] = api["api_base_url"]
                        # Settings page「cliptranslated」：translatedin API processtranslatedonetranslated，translated（worker / localtranslated）fromtranslated
                        processing = saved_settings.get("processing") or {}
                        for src, dst in (("processing_min_score", "min_score_threshold"),
                                         ("processing_chunk_size", "chunk_size"),
                                         ("processing_max_clips", "max_clips_per_collection")):
                            if processing.get(src) is not None:
                                default_settings[dst] = processing[src]
                    else:
                        # processtranslated'sconfigformat（translated）
                        default_settings.update(saved_settings)
                        
            except Exception as e:
                logger.warning(f"translatedsettingsfilefailed: {e}")
        
        self._apply_env_fallbacks(default_settings)
        self._apply_local_preset(default_settings)
        return default_settings

    def _apply_local_preset(self, settings: Dict[str, Any]) -> None:
        """`ollama` / `lmstudio` thistranslatedlocaltranslated → openai + default base_url（translated core/local_presets.py）"""
        from backend.core.local_presets import resolve_provider, LOCAL_PRESETS
        provider, base_url, preset = resolve_provider(settings.get("llm_provider"), settings.get("openai_base_url"))
        settings["llm_provider"] = provider
        settings["llm_provider_preset"] = preset
        if preset:
            settings["openai_base_url"] = base_url
            if not settings.get("model_name") or settings.get("model_name") == "qwen-plus":
                # translateddefaultmodeltranslated dashscope 'sdefaulttranslated，translated qwen-plus translated Ollama
                default_model = LOCAL_PRESETS[preset].default_model
                if default_model:
                    settings["model_name"] = default_model

    # Docker / localtranslatedSettings pagecanuse，translated（env.example translatedIsthistranslated's），
    # translatedthistranslated settings.json，translated API_DASHSCOPE_API_KEY etc.translated。
    _translatedV_KEY_FALLBACKS = {
        "dashscope_api_key": ("API_DASHSCOPE_API_KEY", "DASHSCOPE_API_KEY"),
        "openai_api_key": ("API_OPtranslatedAI_API_KEY", "OPtranslatedAI_API_KEY"),
        "gemini_api_key": ("API_GEMINI_API_KEY", "GEMINI_API_KEY"),
        "siliconflow_api_key": ("API_SILICONFLOW_API_KEY", "SILICONFLOW_API_KEY"),
    }

    def _apply_env_fallbacks(self, settings: Dict[str, Any]) -> None:
        for setting_name, env_names in self._translatedV_KEY_FALLBACKS.items():
            if settings.get(setting_name):
                continue
            for env_name in env_names:
                value = os.getenv(env_name, "").strip()
                if value:
                    settings[setting_name] = value
                    break

        # translated settings.json translatedProvidesprovider/modeltranslated，translated
        file_has_provider = self._file_specifies("api_provider", "llm_provider")
        env_provider = os.getenv("LLM_PROVIDER", "").strip().lower()
        if env_provider and not file_has_provider:
            settings["llm_provider"] = env_provider
        env_model = os.getenv("API_MODEL_NAME", "").strip() or os.getenv("LLM_MODEL", "").strip()
        if env_model and not self._file_specifies("api_model", "model_name"):
            settings["model_name"] = env_model

    def _file_specifies(self, *field_names: str) -> bool:
        """settings.json（translatedformatortranslatedformat）translatedIstranslated translated"""
        try:
            if not self.settings_file.exists():
                return False
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return False
        api = data.get("api", {}) if isinstance(data, dict) else {}
        return any(bool(api.get(name)) or bool(data.get(name)) for name in field_names)
    
    def _save_settings(self):
        """translatedsettings"""
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"translatedsettingsfailed: {e}")
            raise
    
    def _initialize_provider(self):
        """translatedProvidesprovider"""
        try:
            provider_type = ProviderType(self.settings.get("llm_provider", "dashscope"))
            model_name = self.settings.get("model_name", "qwen-plus")
            
            # fetchtranslatedProvidesprovider'sAPIkey（localtranslatedNo need key，translatedDo not user's OpenAI key translatedlocalservice）
            api_key = "" if self.settings.get("llm_provider_preset") else self._get_api_key_for_provider(provider_type)
            provider_kwargs = self._get_provider_kwargs(provider_type)

            # translated OpenAI translatedservice（Ollama / vLLM etc.）translatedNo need key，translated base_url translated
            if api_key or (provider_type == ProviderType.OPtranslatedAI and provider_kwargs.get("base_url")):
                self.current_provider = LLMProviderFactory.create_provider(
                    provider_type, api_key or "", model_name, **provider_kwargs
                )
                logger.info(f"translated{provider_type.value}Providesprovider，model: {model_name}"
                            + (f", base_url: {provider_kwargs['base_url']}" if provider_kwargs.get("base_url") else ""))
            else:
                logger.warning(f"translated{provider_type.value}'sAPIkey")
                self.current_provider = None
                
        except Exception as e:
            logger.error(f"translatedProvidesproviderfailed: {e}")
            self.current_provider = None

    def _get_provider_kwargs(self, provider_type: ProviderType) -> Dict[str, Any]:
        """Providesprovidertranslated：OpenAI translated's base_url；translatedsitetranslatedusetranslatedone translated（translated）"""
        if provider_type == ProviderType.OPtranslatedAI:
            base_url = (self.settings.get("openai_base_url") or "").strip()
            if base_url:
                return {"base_url": base_url}
        if provider_type == ProviderType.DASHSCOPE:
            base_url = (self.settings.get("dashscope_base_url") or "").strip()
            if base_url:
                return {"base_url": base_url, "mode": "compatible"}
        return {}

    def get_processing_setting(self, name: str, default: Any = None) -> Any:
        """Settings page「cliptranslated」（min_score_threshold / chunk_size / max_clips_per_collection），translated settings.json translated"""
        self._reload_if_settings_changed()
        value = self.settings.get(name)
        return default if value is None else value
    
    def _get_api_key_for_provider(self, provider_type: ProviderType) -> Optional[str]:
        """fetchtranslatedProvidesprovider'sAPIkey"""
        key_mapping = {
            ProviderType.DASHSCOPE: "dashscope_api_key",
            ProviderType.OPtranslatedAI: "openai_api_key",
            ProviderType.GEMINI: "gemini_api_key",
            ProviderType.SILICONFLOW: "siliconflow_api_key",
        }
        
        key_name = key_mapping.get(provider_type)
        if key_name:
            return self.settings.get(key_name, "")
        return None
    
    def update_settings(self, new_settings: Dict[str, Any]):
        """updatesettings"""
        self.settings.update(new_settings)
        self._save_settings()
        self._initialize_provider()
    
    def set_provider(self, provider_type: ProviderType, api_key: str, model_name: str,
                     base_url: Optional[str] = None):
        """settingsProvidesprovider"""
        try:
            # updatesettings
            provider_settings = {
                "llm_provider": provider_type.value,
                "model_name": model_name
            }
            
            # updatetranslatedProvidesprovider'sAPIkey
            key_mapping = {
                ProviderType.DASHSCOPE: "dashscope_api_key",
                ProviderType.OPtranslatedAI: "openai_api_key",
                ProviderType.GEMINI: "gemini_api_key",
                ProviderType.SILICONFLOW: "siliconflow_api_key",
            }
            
            key_name = key_mapping.get(provider_type)
            if key_name:
                provider_settings[key_name] = api_key
            if provider_type == ProviderType.OPtranslatedAI and base_url is not None:
                provider_settings["openai_base_url"] = base_url

            # update_settings translated current_provider
            self.update_settings(provider_settings)
            
            logger.info(f"translated{provider_type.value}Providesprovider，model: {model_name}")
            
        except Exception as e:
            logger.error(f"settingsProvidesproviderfailed: {e}")
            raise
    
    def call(self, prompt: str, input_data: Any = None, **kwargs) -> str:
        """callLLM。translated AUTOCLIP_LLM_CACHE_DIR translatedby sha1(prompt+input) translated / translated，translateduse。"""
        self._reload_if_settings_changed()
        cache_path = _llm_cache_path(prompt, input_data)
        if cache_path is not None and cache_path.exists():
            logger.info(f"LLM cachetranslated: {cache_path.name}")
            return cache_path.read_text(encoding="utf-8")
        if not self.current_provider:
            raise ValueError("translatedconfigLLMProvidesprovider，translatedinSettings pagetranslatedconfigAPIkey")
        
        try:
            response = self.current_provider.call(prompt, input_data, **kwargs)
            content = response.content
            if cache_path is not None:
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                cache_path.write_text(content, encoding="utf-8")
            return content
        except Exception as e:
            logger.error(f"LLMcallfailed: {e}")
            raise
    
    def call_with_retry(self, prompt: str, input_data: Any = None, max_retries: int = 3, **kwargs) -> str:
        """translated'sLLMcall"""
        for attempt in range(max_retries):
            try:
                return self.call(prompt, input_data, **kwargs)
            except ValueError:  # iftranslatedIsAPI Keyortranslatederror，translated
                raise
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"LLMcallin{max_retries}translatedfailed。")
                    raise
                logger.warning(f"No.{attempt + 1}translatedcallfailed，translated: {str(e)}")
                import time
                time.sleep(2 ** attempt)  # translated
        return ""
    
    def test_provider_connection(self, provider_type: ProviderType, api_key: str, model_name: str,
                                 **provider_kwargs) -> bool:
        """testProvidesproviderconnect"""
        try:
            provider = LLMProviderFactory.create_provider(provider_type, api_key, model_name, **provider_kwargs)
            return provider.test_connection()
        except Exception as e:
            logger.error(f"test{provider_type.value}connectfailed: {e}")
            return False
    
    def get_current_provider_info(self) -> Dict[str, Any]:
        """fetchtranslatedProvidesproviderinfo"""
        self._reload_if_settings_changed()
        provider_value = self.settings.get("llm_provider", "dashscope")
        try:
            provider_type = ProviderType(provider_value)
        except ValueError:
            return {"provider": provider_value, "model": None, "available": False}
        model_name = self.settings.get("model_name", "qwen-plus")
        preset = self.settings.get("llm_provider_preset")
        info = {
            # Settings page / CLI translated'sIsuserSelect'stranslated（ollama / lmstudio），translatedIs openai translated
            "provider": preset or provider_type.value,
            "backend_provider": provider_type.value,
            "model": model_name,
            "available": self.current_provider is not None,
            "display_name": self._get_provider_display_name(provider_type),
        }
        if preset:
            from backend.core.local_presets import preset_display_name
            info["display_name"] = preset_display_name(preset) or info["display_name"]
        base_url = self._get_provider_kwargs(provider_type).get("base_url")
        if base_url:
            info["base_url"] = base_url
        return info
    
    def _get_provider_display_name(self, provider_type: ProviderType) -> str:
        """fetchProvidesprovidertranslated"""
        display_names = {
            ProviderType.DASHSCOPE: "translated",
            ProviderType.OPtranslatedAI: "OpenAI / translated",
            ProviderType.GEMINI: "Google Gemini",
            ProviderType.SILICONFLOW: "translated"
        }
        return display_names.get(provider_type, provider_type.value)
    
    def get_all_available_models(self) -> Dict[str, List[Dict[str, Any]]]:
        """fetchtranslatedcanusemodel"""
        all_models = LLMProviderFactory.get_all_available_models()
        result = {}
        
        for provider_type, models in all_models.items():
            provider_name = provider_type.value
            result[provider_name] = [
                {
                    "name": model.name,
                    "display_name": model.display_name,
                    "max_tokens": model.max_tokens,
                    "description": model.description
                }
                for model in models
            ]
        
        return result
    
    def parse_json_response(self, response: str) -> Any:
        """translatedJSONtranslated（translatedandtranslatedLLMClient'stranslated）"""
        if not self.current_provider:
            raise ValueError("translatedconfigLLMProvidesprovider")
        
        # thistranslatedcantranslatedusetranslatedLLMClient'sJSONtranslated
        # translated，translatedcreateone translated'sLLMClienttranslated
        from ..utils.llm_client import LLMClient
        temp_client = LLMClient()
        return temp_client.parse_json_response(response)

def _llm_cache_path(prompt: str, input_data: Any) -> Optional[Path]:
    """AUTOCLIP_LLM_CACHE_DIR translateduse；CI / eval translateduse。"""
    root = os.getenv("AUTOCLIP_LLM_CACHE_DIR")
    if not root:
        return None
    import hashlib
    payload = json.dumps({"p": prompt, "i": input_data}, ensure_ascii=False, sort_keys=True, default=str)
    return Path(root) / f"{hashlib.sha1(payload.encode('utf-8')).hexdigest()}.txt"


# translatedLLMtranslated
_llm_manager: Optional[LLMManager] = None

def get_llm_manager() -> LLMManager:
    """fetchtranslatedLLMtranslated"""
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager

def initialize_llm_manager(settings_file: Optional[Path] = None) -> LLMManager:
    """translatedLLMtranslated"""
    global _llm_manager
    _llm_manager = LLMManager(settings_file)
    return _llm_manager
