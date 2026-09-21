"""
ENAPI
ENOpenAI、Gemini、EN、ENDashScopeEN
"""
import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

class ProviderType(Enum):
    """EN"""
    DASHSCOPE = "dashscope"  # EN
    OPENAI = "openai"        # OpenAI
    GEMINI = "gemini"        # Google Gemini
    SILICONFLOW = "siliconflow"  # EN

@dataclass
class ModelInfo:
    """EN"""
    name: str
    display_name: str
    provider: ProviderType
    max_tokens: int
    cost_per_token: Optional[float] = None
    description: Optional[str] = None

@dataclass
class LLMResponse:
    """LLMresponse"""
    content: str
    usage: Optional[Dict[str, Any]] = None
    model: Optional[str] = None
    finish_reason: Optional[str] = None

class LLMProvider(ABC):
    """LLMEN"""
    
    def __init__(self, api_key: str, model_name: str, **kwargs):
        self.api_key = api_key
        self.model_name = model_name
        self.kwargs = kwargs
    
    @abstractmethod
    def call(self, prompt: str, input_data: Any = None, **kwargs) -> LLMResponse:
        """
        callENAPI
        
        Args:
            prompt: hintEN
            input_data: EN
            **kwargs: ENparameters
            
        Returns:
            LLMResponse: ENresponse
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        ENAPIconnect
        
        Returns:
            bool: connectENsucceeded
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[ModelInfo]:
        """
        fetchEN
        
        Returns:
            List[ModelInfo]: EN
        """
        pass
    
    def _build_full_input(self, prompt: str, input_data: Any = None) -> str:
        """EN"""
        if input_data:
            if isinstance(input_data, (dict, list, tuple)):
                return f"{prompt}\n\nEN：\n{json.dumps(input_data, ensure_ascii=False, indent=2, default=str)}"
            else:
                return f"{prompt}\n\nEN：\n{input_data}"
        return prompt

class DashScopeProvider(LLMProvider):
    """ENDashScopeEN"""
    
    def __init__(self, api_key: str, model_name: str = "qwen-plus", **kwargs):
        super().__init__(api_key, model_name, **kwargs)
        # EN（alibabacloud.com，#45）EN key EN dashscope-intl EN；native SDK EN，
        # soEN base_url EN OpenAI EN，EN
        custom_base_url = normalize_base_url(kwargs.get("base_url") or os.getenv("DASHSCOPE_BASE_URL", ""))
        # EN: native (SDK Generation.call) | compatible (OpenAIEN)
        self.mode = (kwargs.get("mode") or os.getenv("DASHSCOPE_MODE") or ("compatible" if custom_base_url else "native")).lower()
        # EN base_url
        self.base_url = custom_base_url or DASHSCOPE_CN_COMPATIBLE_BASE_URL
        self.is_international = self.base_url == DASHSCOPE_INTL_COMPATIBLE_BASE_URL
        # EN SDK
        self._ds_generation = None
        if self.mode == "native":
            try:
                from dashscope import Generation
                self._ds_generation = Generation
            except ImportError:
                raise ImportError("pleaseENdashscope: pip install dashscope")
    
    def call(self, prompt: str, input_data: Any = None, **kwargs) -> LLMResponse:
        """callDashScope API（mode: native|compatible）"""
        masked_key = self.api_key[:3] + "***" + self.api_key[-2:] if self.api_key else ""
        logger.info(f"[DashScope] mode={self.mode} model={self.model_name} base_url={self.base_url if self.mode=='compatible' else 'sdk-generation'} key={masked_key}")
        logger.debug(f"[DashScope] ENkwargs: {kwargs}")
        if self.mode == "native":
            try:
                # ENuseENAPI key，ENsettingsEN
                old_api_key = os.getenv("DASHSCOPE_API_KEY")
                os.environ["DASHSCOPE_API_KEY"] = self.api_key
                
                full_input = self._build_full_input(prompt, input_data)
                resp = self._ds_generation.call(
                    model=self.model_name,
                    prompt=full_input,
                    api_key=self.api_key,
                    stream=False,
                    **kwargs
                )
                
                # EN
                if old_api_key is not None:
                    os.environ["DASHSCOPE_API_KEY"] = old_api_key
                elif "DASHSCOPE_API_KEY" in os.environ:
                    del os.environ["DASHSCOPE_API_KEY"]
                if resp and getattr(resp, 'status_code', 200) == 200:
                    if getattr(resp, 'output', None) and getattr(resp.output, 'text', None) is not None:
                        return LLMResponse(
                            content=resp.output.text,
                            model=self.model_name,
                            finish_reason=getattr(resp.output, 'finish_reason', None)
                        )
                    finish_reason = getattr(resp.output, 'finish_reason', 'unknown') if getattr(resp, 'output', None) else 'unknown'
                    logger.warning(f"APIrequestsucceeded，EN。endEN: {finish_reason}")
                    return LLMResponse(content="")
                code = getattr(resp, 'code', 'N/A')
                message = getattr(resp, 'message', 'ENAPIerror')
                raise Exception(f"APIcallfailed - Status: {getattr(resp,'status_code', 'N/A')}, Code: {code}, Message: {message}")
            except Exception as e:
                logger.error(f"DashScope(native)callfailed: {str(e)}")
                raise
        else:
            # compatible
            try:
                import requests
                full_input = self._build_full_input(prompt, input_data)
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": full_input}],
                    "stream": False,
                }
                payload.update({k: v for k, v in kwargs.items() if v is not None})
                url = f"{self.base_url}/chat/completions"
                resp = requests.post(url, headers=headers, json=payload, timeout=30)
                if resp.status_code != 200:
                    try:
                        err = resp.json()
                    except Exception:
                        err = {"message": resp.text}
                    raise Exception(f"APIcallfailed - Status: {resp.status_code}, Message: {err}")
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage")
                finish_reason = data["choices"][0].get("finish_reason")
                return LLMResponse(content=content, usage=usage, model=self.model_name, finish_reason=finish_reason)
            except Exception as e:
                logger.error(f"DashScope(compatible)callfailed: {str(e)}")
                raise
    
    def test_connection(self) -> bool:
        """ENDashScopeconnect"""
        try:
            # ENvalidateAPI KeyEN
            if not self.api_key or len(self.api_key.strip()) < 10:
                logger.error("API KeyEN")
                return False
            
            # checkAPI KeyEN（DashScope API KeyENsk-EN）
            if not self.api_key.startswith("sk-"):
                logger.warning(f"API KeyENmayEN，EN'sk-'EN，EN: {self.api_key[:10]}...")
                # ENreturnFalse，becauseENAPI KeymayEN
            
            # useENcall，ENAPIvalidate
            try:
                # ENcallcallEN
                response = self.call("EN", max_tokens=1)
                if response and response.content:
                    logger.info("DashScope APIconnectENsucceeded")
                    return True
                else:
                    logger.error("DashScope APIENreturnENresponse")
                    return False
                    
            except Exception as e:
                logger.error(f"DashScope APIENfailed: {str(e)}")
                return False
                
        except Exception as e:
            logger.error(f"DashScopeconnectENfailed: {e}")
            return False
    
    def get_available_models(self) -> List[ModelInfo]:
        """fetchDashScopeEN"""
        return [
            ModelInfo(
                name="qwen-plus",
                display_name="ENPlus",
                provider=ProviderType.DASHSCOPE,
                max_tokens=8192,
                description="ENPlusEN"
            ),
            ModelInfo(
                name="qwen-max",
                display_name="ENMax",
                provider=ProviderType.DASHSCOPE,
                max_tokens=8192,
                description="ENMaxEN"
            ),
            ModelInfo(
                name="qwen-turbo",
                display_name="ENTurbo",
                provider=ProviderType.DASHSCOPE,
                max_tokens=8192,
                description="ENTurboEN"
            )
        ]

OPENAI_OFFICIAL_BASE_URL = "https://api.openai.com/v1"
# EN/EN OpenAI ENservice（Ollama、vLLM、LM Studio EN）EN key，EN SDK EN
OPENAI_COMPATIBLE_PLACEHOLDER_KEY = "EMPTY"
# EN OpenAI ENAPI：EN / EN（alibabacloud.com EN key EN，#45）
DASHSCOPE_CN_COMPATIBLE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DASHSCOPE_INTL_COMPATIBLE_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"


def normalize_base_url(base_url: Optional[str]) -> str:
    """EN `/`，ENreturnEN（ENuseEN）"""
    return (base_url or "").strip().rstrip("/")


def is_local_url(url: Optional[str]) -> bool:
    """
    EN / EN（Ollama、LM Studio、vLLM EN）。
    ENsystemEN：macOS EN httpx ENsystemENsettings（Clash / Surge EN），
    EN localhost requestEN，resultEN 502 / timeout，userEN。
    """
    if not url:
        return False
    try:
        from urllib.parse import urlparse
        import ipaddress
        host = (urlparse(url).hostname or "").lower()
    except Exception:  # noqa: BLE001
        return False
    if host in ("localhost", "0.0.0.0", "host.docker.internal") or host.endswith(".local") or host.endswith(".localhost"):
        return True
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_loopback or ip.is_private or ip.is_link_local
    except ValueError:
        return False


def make_openai_http_client(base_url: Optional[str]):
    """EN → EN / systemEN httpx.Client；ENreturn None（EN SDK EN）。"""
    if not is_local_url(base_url):
        return None
    try:
        import httpx
        return httpx.Client(trust_env=False)
    except Exception:  # noqa: BLE001
        return None


class OpenAIProvider(LLMProvider):
    """OpenAI EN OpenAI ENAPI（EN、DeepSeek、OpenRouter、Ollama、vLLM、LM Studio EN）

    through `base_url` ENserviceEN；EN OpenAI EN。
    """
    
    def __init__(self, api_key: str, model_name: str = "gpt-4o-mini", **kwargs):
        super().__init__(api_key, model_name, **kwargs)
        self.base_url = normalize_base_url(kwargs.get("base_url") or os.getenv("OPENAI_BASE_URL"))
        self.is_custom_endpoint = bool(self.base_url) and self.base_url != OPENAI_OFFICIAL_BASE_URL
        if not api_key and self.is_custom_endpoint:
            api_key = OPENAI_COMPATIBLE_PLACEHOLDER_KEY
            self.api_key = api_key
        try:
            import openai
            client_kwargs = {"api_key": api_key}
            if self.base_url:
                client_kwargs["base_url"] = self.base_url
                http_client = make_openai_http_client(self.base_url)
                if http_client is not None:
                    client_kwargs["http_client"] = http_client
            self.client = openai.OpenAI(**client_kwargs)
        except ImportError:
            raise ImportError("pleaseENopenai: pip install openai")
    
    def call(self, prompt: str, input_data: Any = None, **kwargs) -> LLMResponse:
        """callOpenAI API"""
        try:
            full_input = self._build_full_input(prompt, input_data)
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": full_input}],
                **kwargs
            )
            
            content = response.choices[0].message.content
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            } if response.usage else None
            
            return LLMResponse(
                content=content,
                usage=usage,
                model=self.model_name,
                finish_reason=response.choices[0].finish_reason
            )
            
        except Exception as e:
            logger.error(f"OpenAIcallfailed: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """ENOpenAI / ENAPIconnect"""
        try:
            # EN OpenAI EN key EN；ENserviceEN key EN（ENneed）
            if not self.is_custom_endpoint:
                if not self.api_key or len(self.api_key.strip()) < 10:
                    logger.error("OpenAI API KeyEN")
                    return False
                if not self.api_key.startswith("sk-"):
                    logger.warning(f"OpenAI API KeyENmayEN，EN'sk-'EN，EN: {self.api_key[:10]}...")
            
            # useEN
            response = self.call("EN", max_tokens=1)
            return response and response.content is not None
        except Exception as e:
            logger.error(f"OpenAIconnectENfailed (base_url={self.base_url or OPENAI_OFFICIAL_BASE_URL}): {e}")
            return False
    
    def get_available_models(self) -> List[ModelInfo]:
        """fetchOpenAIEN（ENAPIENuserEN，EN）"""
        return [
            ModelInfo(
                name="gpt-4o-mini",
                display_name="GPT-4o mini",
                provider=ProviderType.OPENAI,
                max_tokens=128000,
                description="OpenAI GPT-4o mini（EN）"
            ),
            ModelInfo(
                name="gpt-4o",
                display_name="GPT-4o",
                provider=ProviderType.OPENAI,
                max_tokens=128000,
                description="OpenAI GPT-4o"
            ),
            ModelInfo(
                name="gpt-4-turbo",
                display_name="GPT-4 Turbo",
                provider=ProviderType.OPENAI,
                max_tokens=128000,
                description="OpenAI GPT-4 TurboEN"
            )
        ]

class GeminiProvider(LLMProvider):
    """Google GeminiEN"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash", **kwargs):
        super().__init__(api_key, model_name, **kwargs)
        try:
            # New unified Google GenAI SDK (replaces the deprecated
            # google-generativeai package).
            from google import genai
            self.client = genai.Client(api_key=api_key)
        except ImportError:
            raise ImportError("pleaseENgoogle-genai: pip install google-genai")

    def call(self, prompt: str, input_data: Any = None, **kwargs) -> LLMResponse:
        """callGemini API"""
        try:
            full_input = self._build_full_input(prompt, input_data)

            # Map a max-tokens hint onto the new SDK's config object if present.
            config = None
            max_tokens = kwargs.get("max_tokens") or kwargs.get("max_output_tokens")
            if max_tokens:
                from google.genai import types
                config = types.GenerateContentConfig(max_output_tokens=max_tokens)

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_input,
                config=config,
            )

            return LLMResponse(
                content=response.text,
                model=self.model_name,
                finish_reason=getattr(response, 'finish_reason', None)
            )

        except Exception as e:
            logger.error(f"Geminicallfailed: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """ENGeminiconnect"""
        try:
            # useENhint
            response = self.call("EN", max_tokens=10)
            # checkresponseEN
            if response and response.content:
                return True
            return False
        except Exception as e:
            logger.error(f"GeminiconnectENfailed: {e}")
            return False
    
    def get_available_models(self) -> List[ModelInfo]:
        """fetchGeminiEN"""
        return [
            ModelInfo(
                name="gemini-2.5-flash",
                display_name="Gemini 2.5 Flash",
                provider=ProviderType.GEMINI,
                max_tokens=1000000,
                description="Google Gemini 2.5 FlashEN"
            ),
            ModelInfo(
                name="gemini-1.5-pro",
                display_name="Gemini 1.5 Pro",
                provider=ProviderType.GEMINI,
                max_tokens=2000000,
                description="Google Gemini 1.5 ProEN"
            ),
            ModelInfo(
                name="gemini-1.5-flash",
                display_name="Gemini 1.5 Flash",
                provider=ProviderType.GEMINI,
                max_tokens=1000000,
                description="Google Gemini 1.5 FlashEN"
            )
        ]

class SiliconFlowProvider(LLMProvider):
    """EN"""
    
    def __init__(self, api_key: str, model_name: str = "Qwen/Qwen2.5-7B-Instruct", **kwargs):
        super().__init__(api_key, model_name, **kwargs)
        self.base_url = "https://api.siliconflow.cn/v1"
    
    def call(self, prompt: str, input_data: Any = None, **kwargs) -> LLMResponse:
        """callENAPI"""
        try:
            import requests
            
            full_input = self._build_full_input(prompt, input_data)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": full_input}],
                "stream": False,
                **kwargs
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            content = result["choices"][0]["message"]["content"]
            usage = result.get("usage")
            
            return LLMResponse(
                content=content,
                usage=usage,
                model=self.model_name,
                finish_reason=result["choices"][0].get("finish_reason")
            )
            
        except Exception as e:
            logger.error(f"ENcallfailed: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """ENconnect"""
        try:
            # useENhint
            response = self.call("EN", max_tokens=10)
            # checkresponseEN
            if response and response.content:
                return True
            return False
        except Exception as e:
            logger.error(f"ENconnectENfailed: {e}")
            return False
    
    def get_available_models(self) -> List[ModelInfo]:
        """fetchEN"""
        return [
            ModelInfo(
                name="Qwen/Qwen2.5-7B-Instruct",
                display_name="Qwen2.5-7B",
                provider=ProviderType.SILICONFLOW,
                max_tokens=32768,
                description="ENQwen2.5-7BEN"
            ),
            ModelInfo(
                name="Qwen/Qwen2.5-14B-Instruct",
                display_name="Qwen2.5-14B",
                provider=ProviderType.SILICONFLOW,
                max_tokens=32768,
                description="ENQwen2.5-14BEN"
            ),
            ModelInfo(
                name="Qwen/Qwen2.5-32B-Instruct",
                display_name="Qwen2.5-32B",
                provider=ProviderType.SILICONFLOW,
                max_tokens=32768,
                description="ENQwen2.5-32BEN"
            ),
            ModelInfo(
                name="deepseek-ai/DeepSeek-V2.5",
                display_name="DeepSeek-V2.5",
                provider=ProviderType.SILICONFLOW,
                max_tokens=65536,
                description="ENDeepSeek-V2.5EN"
            )
        ]

class LLMProviderFactory:
    """LLMEN"""
    
    _providers = {
        ProviderType.DASHSCOPE: DashScopeProvider,
        ProviderType.OPENAI: OpenAIProvider,
        ProviderType.GEMINI: GeminiProvider,
        ProviderType.SILICONFLOW: SiliconFlowProvider,
    }
    
    @classmethod
    def create_provider(cls, provider_type: ProviderType, api_key: str, model_name: str, **kwargs) -> LLMProvider:
        """createEN"""
        if provider_type not in cls._providers:
            raise ValueError(f"EN: {provider_type}")
        
        provider_class = cls._providers[provider_type]
        return provider_class(api_key, model_name, **kwargs)
    
    @classmethod
    def get_all_available_models(cls) -> Dict[ProviderType, List[ModelInfo]]:
        """fetchallEN"""
        models = {}
        for provider_type, provider_class in cls._providers.items():
            try:
                # createENfetchEN
                temp_provider = provider_class("dummy_key", "dummy_model")
                models[provider_type] = temp_provider.get_available_models()
            except Exception as e:
                logger.warning(f"cannotfetch{provider_type.value}EN: {e}")
                models[provider_type] = []
        return models
