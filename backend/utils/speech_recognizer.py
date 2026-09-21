"""
translatedtool - supportmultitranslatedservice
supportlocalWhisper、OpenAI API、Azure Speech Servicesetc.multitranslatedservice
"""
import logging
import subprocess
import json
import os
import asyncio
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from enum import Enum
import requests
from dataclasses import dataclass
from .ffmpeg_utils import get_ffmpeg_path

logger = logging.getLogger(__name__)


class SpeechRecognitionMethod(str, Enum):
    """translated"""
    WHISPER_LOCAL = "whisper_local"
    OPtranslatedAI_API = "openai_api"
    AZURE_SPEECH = "azure_speech"
    GOOGLE_SPEECH = "google_speech"
    ALIYUN_SPEECH = "aliyun_speech"
    # translatedservicetranslated
    CUSTOM_API = "custom_api"


class LanguageCode(str, Enum):
    """support'sLanguagetranslated"""
    # translated
    CHINESE_SIMPLIFIED = "zh"
    CHINESE_TRADITIONAL = "zh-TW"
    # translated
    translatedGLISH = "en"
    translatedGLISH_US = "en-US"
    translatedGLISH_UK = "en-GB"
    # translated
    JAPANESE = "ja"
    # translated
    KOREAN = "ko"
    # translated
    FRtranslatedCH = "fr"
    # translated
    GERMAN = "de"
    # translated
    SPANISH = "es"
    # translated
    RUSSIAN = "ru"
    # translated
    ARABIC = "ar"
    # translated
    PORTUGUESE = "pt"
    # translated
    ITALIAN = "it"
    # translated
    AUTO = "auto"


@dataclass
class SpeechRecognitionConfig:
    """translatedconfig"""
    method: SpeechRecognitionMethod = SpeechRecognitionMethod.WHISPER_LOCAL
    language: LanguageCode = LanguageCode.AUTO
    model: str = "base"  # Whispermodeltranslated
    timeout: int = 0  # translated（seconds），0translated
    output_format: str = "srt"  # translatedformat
    enable_timestamps: bool = True  # Istranslatedusetranslated
    enable_punctuation: bool = True  # Istranslatedusetranslated
    enable_speaker_diarization: bool = False  # Istranslatedusetranslated
    enable_fallback: bool = True  # Istranslatedusetranslated
    fallback_method: SpeechRecognitionMethod = SpeechRecognitionMethod.WHISPER_LOCAL  # translated
    
    # APIconfig
    openai_api_key: Optional[str] = None
    azure_speech_key: Optional[str] = None
    azure_speech_region: Optional[str] = None
    google_credentials_path: Optional[str] = None
    aliyun_access_key: Optional[str] = None
    aliyun_access_secret: Optional[str] = None
    custom_api_url: Optional[str] = None
    custom_api_key: Optional[str] = None
    
    def __post_init__(self):
        """verifyconfigtranslated"""
        # verifytranslated
        if not isinstance(self.method, SpeechRecognitionMethod):
            try:
                self.method = SpeechRecognitionMethod(self.method)
            except ValueError:
                raise ValueError(f"translatedsupport'stranslated: {self.method}")
        
        # verifyLanguage
        if not isinstance(self.language, LanguageCode):
            try:
                self.language = LanguageCode(self.language)
            except ValueError:
                raise ValueError(f"translatedsupport'sLanguagetranslated: {self.language}")
        
        # verifymodel
        valid_models = ["tiny", "base", "small", "medium", "large"]
        if self.model not in valid_models:
            raise ValueError(f"translatedsupport'sWhispermodel: {self.model}")
        
        # verifytranslated
        if self.timeout < 0:
            raise ValueError("translated")
        
        # verifytranslatedformat
        valid_formats = ["srt", "vtt", "txt", "json"]
        if self.output_format not in valid_formats:
            raise ValueError(f"translatedsupport'stranslatedformat: {self.output_format}")


class SpeechRecognitionError(Exception):
    """translatederror"""
    pass


class SpeechRecognizer:
    """translated，supportmultitranslatedservice"""
    
    def __init__(self, config: Optional[SpeechRecognitionConfig] = None):
        self.config = config or SpeechRecognitionConfig()
        self.available_methods = self._check_available_methods()
    
    def _check_available_methods(self) -> Dict[SpeechRecognitionMethod, bool]:
        """checkcanuse'stranslated"""
        methods = {}
        
        # checklocalWhisper
        methods[SpeechRecognitionMethod.WHISPER_LOCAL] = self._check_whisper_availability()
        
        # checkOpenAI API
        methods[SpeechRecognitionMethod.OPtranslatedAI_API] = self._check_openai_availability()
        
        # checkAzure Speech Services
        methods[SpeechRecognitionMethod.AZURE_SPEECH] = self._check_azure_speech_availability()
        
        # checkGoogle Speech-to-Text
        methods[SpeechRecognitionMethod.GOOGLE_SPEECH] = self._check_google_speech_availability()
        
        # checktranslated
        methods[SpeechRecognitionMethod.ALIYUN_SPEECH] = self._check_aliyun_speech_availability()
        
        # checktranslatedAPI
        methods[SpeechRecognitionMethod.CUSTOM_API] = self._check_custom_api_availability()
        
        return methods
    
    def _check_whisper_availability(self) -> bool:
        """checklocal Whisper(mlx) RuntimeIstranslatedinstall。"""
        try:
            from backend.services import whisper_runtime
            return whisper_runtime.is_installed()
        except Exception:
            logger.warning("localWhispertranslatedinstallortranslatedcanuse")
            return False
    
    def _check_openai_availability(self) -> bool:
        """checkOpenAI APIIstranslatedcanuse"""
        api_key = os.getenv("OPtranslatedAI_API_KEY")
        return api_key is not None and len(api_key.strip()) > 0
    
    def _check_azure_speech_availability(self) -> bool:
        """checkAzure Speech ServicesIstranslatedcanuse"""
        api_key = os.getenv("AZURE_SPEECH_KEY")
        region = os.getenv("AZURE_SPEECH_REGION")
        return api_key is not None and region is not None
    
    def _check_google_speech_availability(self) -> bool:
        """checkGoogle Speech-to-TextIstranslatedcanuse"""
        # checkGoogle Cloudtranslatedfile
        cred_file = os.getenv("GOOGLE_APPLICATION_CREDtranslatedTIALS")
        if cred_file and Path(cred_file).exists():
            return True
        
        # checkAPIkey
        api_key = os.getenv("GOOGLE_SPEECH_API_KEY")
        return api_key is not None
    
    def _check_aliyun_speech_availability(self) -> bool:
        """checktranslatedIstranslatedcanuse"""
        try:
            # checkconfigtranslated'sAPI Key
            # thistranslatedcantranslatedchecktranslatedortranslatedconfigtranslated'sAPI Key
            access_key = os.getenv("ALIYUN_API_KEY") or (self.config.aliyun_access_key if hasattr(self, 'config') else None)
            return bool(access_key)
        except Exception:
            return False
    
    def _extract_audio_from_video(self, video_path: Path, output_dir: Path) -> Path:
        """
        fromvideofiletranslated
        
        Args:
            video_path: videofile path
            output_dir: translateddirectory
            
        Returns:
            translated'stranslatedfile path
        """
        try:
            # checkffmpegIstranslatedcanuse
            ffmpeg_bin = get_ffmpeg_path()
            result = subprocess.run([ffmpeg_bin, '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise SpeechRecognitionError("ffmpegtranslatedcanuse，translatedinstallffmpeg")
            
            # translatedfile path
            audio_filename = f"{video_path.stem}_audio.wav"
            audio_path = output_dir / audio_filename
            
            # iftranslatedfiletranslatedin，translatedreturn
            if audio_path.exists():
                logger.info(f"translatedfiletranslatedin: {audio_path}")
                return audio_path
            
            logger.info(f"translatedinfromvideotranslated: {video_path} -> {audio_path}")
            
            # useffmpegtranslated
            cmd = [
                ffmpeg_bin,
                '-i', str(video_path),
                '-vn',  # translatedprocessvideotranslated
                '-acodec', 'pcm_s16le',  # usePCM 16translated
                '-ar', '16000',  # translated16kHz
                '-ac', '1',  # translated
                '-y',  # translatedfile
                str(audio_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                raise SpeechRecognitionError(f"translatedfailed: {result.stderr}")
            
            if not audio_path.exists():
                raise SpeechRecognitionError("translatedfailed，translatedfile not found")
            
            logger.info(f"translatedsucceeded: {audio_path}")
            return audio_path
            
        except subprocess.TimeoutExpired:
            raise SpeechRecognitionError("translated")
        except Exception as e:
            raise SpeechRecognitionError(f"translatedfailed: {e}")
    
    def generate_subtitle(self, video_path: Path, output_path: Optional[Path] = None, 
                         config: Optional[SpeechRecognitionConfig] = None) -> Path:
        """
        generate subtitlesfile
        
        Args:
            video_path: videofile path
            output_path: translatedsubtitlesfile path
            config: translatedconfig
            
        Returns:
            translated'ssubtitlesfile path
            
        Raises:
            SpeechRecognitionError: translatedfailed
        """
        if not video_path.exists():
            raise SpeechRecognitionError(f"videofile not found: {video_path}")
        
        # usetranslated'sconfigordefaultconfig
        config = config or self.config
        
        # translatedpath
        if output_path is None:
            output_path = video_path.parent / f"{video_path.stem}.{config.output_format}"
        
        # translatedconfig'stranslatedSelectselecttranslatedservice，supporttranslated
        try:
            if config.method == SpeechRecognitionMethod.WHISPER_LOCAL:
                return self._generate_subtitle_whisper_local(video_path, output_path, config)
            elif config.method == SpeechRecognitionMethod.OPtranslatedAI_API:
                return self._generate_subtitle_openai_api(video_path, output_path, config)
            elif config.method == SpeechRecognitionMethod.AZURE_SPEECH:
                return self._generate_subtitle_azure_speech(video_path, output_path, config)
            elif config.method == SpeechRecognitionMethod.GOOGLE_SPEECH:
                return self._generate_subtitle_google_speech(video_path, output_path, config)
            elif config.method == SpeechRecognitionMethod.ALIYUN_SPEECH:
                return self._generate_subtitle_aliyun_speech(video_path, output_path, config)
            elif config.method == SpeechRecognitionMethod.CUSTOM_API:
                return self._generate_subtitle_custom_api(video_path, output_path, config)
            else:
                raise SpeechRecognitionError(f"translatedsupport'stranslated: {config.method}")
        except SpeechRecognitionError as e:
            # iftranslatedusetranslatedIstranslated，translated
            if (config.enable_fallback and 
                config.method != config.fallback_method and 
                self.available_methods.get(config.fallback_method, False)):
                
                logger.warning(f"translated {config.method} failed: {e}")
                logger.info(f"translated {config.fallback_method}")
                
                # createtranslatedconfig
                fallback_config = SpeechRecognitionConfig(
                    method=config.fallback_method,
                    language=config.language,
                    model=config.model,
                    timeout=config.timeout,
                    output_format=config.output_format,
                    enable_timestamps=config.enable_timestamps,
                    enable_punctuation=config.enable_punctuation,
                    enable_speaker_diarization=config.enable_speaker_diarization,
                    enable_fallback=False  # translated
                )
                
                return self.generate_subtitle(video_path, output_path, fallback_config)
            else:
                raise
    
    def _check_custom_api_availability(self) -> bool:
        """checktranslatedAPIIstranslatedcanuse"""
        # checkIstranslatedconfigtranslatedAPI
        if self.config.custom_api_url and self.config.custom_api_key:
            try:
                # translated'sHealth Check
                response = requests.get(f"{self.config.custom_api_url}/health", timeout=5)
                return response.status_code == 200
            except Exception:
                return False
        return False
    
    @staticmethod
    def _format_srt_timestamp(seconds: float) -> str:
        if seconds is None or seconds < 0:
            seconds = 0.0
        ms = int(round(seconds * 1000.0))
        h, ms = divmod(ms, 3600000)
        m, ms = divmod(ms, 60000)
        s, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    @classmethod
    def _segments_to_srt(cls, segments: List[Dict[str, Any]]) -> str:
        lines = []
        for i, seg in enumerate(segments, start=1):
            text = (seg.get("text") or "").strip()
            if not text:
                continue
            start = cls._format_srt_timestamp(seg.get("start", 0.0))
            end = cls._format_srt_timestamp(seg.get("end", 0.0))
            lines.append(f"{i}\n{start} --> {end}\n{text}\n")
        return "\n".join(lines) + "\n"

    def _generate_subtitle_whisper_local(self, video_path: Path, output_path: Path,
                                       config: SpeechRecognitionConfig) -> Path:
        """uselocal faster-whisper generate subtitles（translatedbytranslatedinstall'sRuntime）。"""
        from backend.services import whisper_runtime

        if not whisper_runtime.is_installed():
            raise SpeechRecognitionError(
                "local Whisper Runtimetranslatedinstall。translated「settings → translated」translatedclickinstall Whisper，"
                "translateddownloadone modeltranslated。"
            )

        if not video_path.exists():
            raise SpeechRecognitionError(f"videofile not found: {video_path}")
        if video_path.stat().st_size == 0:
            raise SpeechRecognitionError(f"videofiletranslated: {video_path}")
        if output_path.exists():
            logger.info(f"subtitlesfiletranslatedin，skipWhisperprocess: {output_path}")
            return output_path

        try:
            whisper_runtime.ensure_on_path()  # translated faster_whisper canimport
            from faster_whisper import WhisperModel  # translatedimport：Runtimeinstalldirectorytranslated'sPackage

            language = None if config.language == LanguageCode.AUTO else str(config.language).split("-")[0]
            models_dir = str(whisper_runtime.get_models_dir() / "hub")
            logger.info(f"use faster-whisper generate subtitles: model={config.model} lang={language or 'auto'}")

            # device=auto：Mac translated CPU（CTranslate2），int8 translatedandtranslated
            model = WhisperModel(
                config.model, device="auto", compute_type="int8", download_root=models_dir,
            )
            seg_iter, _info = model.transcribe(str(video_path), language=language, vad_filter=True)
            segments = [{"start": s.start, "end": s.end, "text": s.text} for s in seg_iter]
            if not segments:
                raise SpeechRecognitionError("Whisper translated")

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(self._segments_to_srt(segments), encoding="utf-8")
            logger.info(f"local faster-whisper subtitlestranslatedsucceeded: {output_path}")
            return output_path

        except SpeechRecognitionError:
            raise
        except ModuleNotFoundError as e:
            raise SpeechRecognitionError(
                f"Whisper Runtimetranslateddependencies（{e}）。translated「settings → translated」translatedinstall Whisper。"
            )
        except Exception as e:  # noqa: BLE001
            logger.error(f"local faster-whisper generate subtitlesfailed: {e}", exc_info=True)
            raise SpeechRecognitionError(f"local Whisper generate subtitlesfailed: {e}")
    
    def _generate_subtitle_openai_api(self, video_path: Path, output_path: Path, 
                                    config: SpeechRecognitionConfig) -> Path:
        """useOpenAI APIgenerate subtitles"""
        if not self.available_methods[SpeechRecognitionMethod.OPtranslatedAI_API]:
            raise SpeechRecognitionError("OpenAI APItranslatedcanuse，translatedsettingsOPtranslatedAI_API_KEYtranslated")
        
        try:
            logger.info(f"translateduseOpenAI APIgenerate subtitles: {video_path}")
            
            # thistranslatedOpenAI APIcall
            # translated'sdependencies，thistranslated
            raise SpeechRecognitionError("OpenAI APIfeaturetranslated，translateduselocalWhisper")
            
        except Exception as e:
            error_msg = f"OpenAI APIgenerate subtitlestranslatederror: {e}"
            logger.error(error_msg)
            raise SpeechRecognitionError(error_msg)
    
    def _generate_subtitle_azure_speech(self, video_path: Path, output_path: Path, 
                                      config: SpeechRecognitionConfig) -> Path:
        """useAzure Speech Servicesgenerate subtitles"""
        if not self.available_methods[SpeechRecognitionMethod.AZURE_SPEECH]:
            raise SpeechRecognitionError("Azure Speech Servicestranslatedcanuse，translatedsettingsAZURE_SPEECH_KEYAndAZURE_SPEECH_REGIONtranslated")
        
        try:
            logger.info(f"translateduseAzure Speech Servicesgenerate subtitles: {video_path}")
            
            # thistranslatedAzure Speech Servicescall
            raise SpeechRecognitionError("Azure Speech Servicesfeaturetranslated，translateduselocalWhisper")
            
        except Exception as e:
            error_msg = f"Azure Speech Servicesgenerate subtitlestranslatederror: {e}"
            logger.error(error_msg)
            raise SpeechRecognitionError(error_msg)
    
    def _generate_subtitle_google_speech(self, video_path: Path, output_path: Path, 
                                       config: SpeechRecognitionConfig) -> Path:
        """useGoogle Speech-to-Textgenerate subtitles"""
        if not self.available_methods[SpeechRecognitionMethod.GOOGLE_SPEECH]:
            raise SpeechRecognitionError("Google Speech-to-Texttranslatedcanuse，translatedsettingsGOOGLE_APPLICATION_CREDtranslatedTIALSorGOOGLE_SPEECH_API_KEYtranslated")
        
        try:
            logger.info(f"translateduseGoogle Speech-to-Textgenerate subtitles: {video_path}")
            
            # thistranslatedGoogle Speech-to-Textcall
            raise SpeechRecognitionError("Google Speech-to-Textfeaturetranslated，translateduselocalWhisper")
            
        except Exception as e:
            error_msg = f"Google Speech-to-Textgenerate subtitlestranslatederror: {e}"
            logger.error(error_msg)
            raise SpeechRecognitionError(error_msg)
    
    def _generate_subtitle_aliyun_speech(self, video_path: Path, output_path: Path, 
                                       config: SpeechRecognitionConfig) -> Path:
        """usetranslatedgenerate subtitles"""
        if not self.available_methods[SpeechRecognitionMethod.ALIYUN_SPEECH]:
            raise SpeechRecognitionError("translatedcanuse，translatedconfigAPI Key")
        
        try:
            logger.info(f"translatedusetranslatedgenerate subtitles: {video_path}")
            
            # checkvideofileIstranslatedin
            if not video_path.exists():
                raise SpeechRecognitionError(f"videofile not found: {video_path}")
            
            # translatedfile
            audio_path = self._extract_audio_from_video(video_path, output_path.parent)
            
            # usetranslatedAPI
            # translated：thistranslatedusetranslated'stranslatedservice，defaultuseqwen3-asr-flashmodel
            import requests
            import base64
            
            # translatedfiletranslated
            with open(audio_path, 'rb') as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
            
            # translated
            request_data = {
                "model": "qwen3-asr-flash",  # usetranslated'sASRmodel
                "input": {
                    "audio": f"data:audio/wav;base64,{audio_data}"
                },
                "parameters": {
                    "format": "srt",  # translatedSRTformat
                    "enable_timestamps": config.enable_timestamps,
                    "enable_punctuation": config.enable_punctuation
                }
            }
            
            # translatedAPI
            headers = {
                'Authorization': f'Bearer {config.aliyun_access_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                'https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/asr',
                headers=headers,
                json=request_data,
                timeout=config.timeout if config.timeout > 0 else 300
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('output', {}).get('text'):
                    # translatedsubtitlesfile
                    subtitle_content = result['output']['text']
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(subtitle_content)
                    
                    logger.info(f"translatedsubtitlestranslatedsucceeded: {output_path}")
                    return output_path
                else:
                    raise SpeechRecognitionError("translatedreturntranslated")
            else:
                error_detail = response.json().get('message', 'translatederror') if response.headers.get('content-type', '').startswith('application/json') else response.text
                raise SpeechRecognitionError(f"translatedAPIcallfailed: {response.status_code} - {error_detail}")
            
        except Exception as e:
            error_msg = f"translatedgenerate subtitlestranslatederror: {e}"
            logger.error(error_msg)
            raise SpeechRecognitionError(error_msg)
    
    def _generate_subtitle_custom_api(self, video_path: Path, output_path: Path, 
                                     config: SpeechRecognitionConfig) -> Path:
        """usetranslatedAPIgenerate subtitles"""
        if not config.custom_api_url or not config.custom_api_key:
            raise SpeechRecognitionError(
                "translatedAPIconfigtranslated，translatedconfig custom_api_url And custom_api_key"
            )
        
        try:
            logger.info(f"translatedusetranslatedAPIgenerate subtitles: {video_path}")
            
            # checkvideofileIstranslatedin
            if not video_path.exists():
                raise SpeechRecognitionError(f"videofile not found: {video_path}")
            
            # translatedfile
            audio_path = self._extract_audio_from_video(video_path, output_path.parent)
            
            # translatedAPItranslated
            headers = {
                'Authorization': f'Bearer {config.custom_api_key}',
                'Content-Type': 'audio/wav'
            }
            
            # translatedfiletranslatedAPI
            with open(audio_path, 'rb') as audio_file:
                files = {'audio': audio_file}
                data = {
                    'language': config.language.value if config.language != LanguageCode.AUTO else 'auto',
                    'format': config.output_format
                }
                
                response = requests.post(
                    f"{config.custom_api_url}/transcribe",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=config.timeout if config.timeout > 0 else 300
                )
            
            if response.status_code == 200:
                # translatedsubtitlesfile
                subtitle_content = response.text
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(subtitle_content)
                
                logger.info(f"translatedAPIsubtitlestranslatedsucceeded: {output_path}")
                return output_path
            else:
                raise SpeechRecognitionError(f"translatedAPIcallfailed: {response.status_code} - {response.text}")
                
        except Exception as e:
            error_msg = f"translatedAPIgenerate subtitlestranslatederror: {e}"
            logger.error(error_msg)
            raise SpeechRecognitionError(error_msg)
    
    def get_available_methods(self) -> Dict[SpeechRecognitionMethod, bool]:
        """fetchcanuse'stranslated"""
        return self.available_methods.copy()
    
    def get_supported_languages(self) -> List[LanguageCode]:
        """fetchsupport'sLanguagelist"""
        return list(LanguageCode)
    
    def get_whisper_models(self) -> List[str]:
        """fetchcanuse'sWhispermodellist"""
        return ["tiny", "base", "small", "medium", "large"]


def generate_subtitle_for_video(video_path: Path, output_path: Optional[Path] = None, 
                               method: str = "auto", language: str = "auto", 
                               model: str = "base", enable_fallback: bool = True) -> Path:
    """
    translatedvideogenerate subtitlesfile'stranslated
    
    Args:
        video_path: videofile path
        output_path: translatedsubtitlesfile path
        method: translated ("auto", "whisper_local", "openai_api", "azure_speech", "google_speech", "aliyun_speech", "custom_api")
        language: Languagetranslated
        model: Whispermodeltranslated（Onlytranslatedwhisper_localtranslated）
        enable_fallback: Istranslatedusetranslated
        
    Returns:
        translated'ssubtitlesfile path
        
    Raises:
        SpeechRecognitionError: translatedfailed
    """
    # createconfig
    config = SpeechRecognitionConfig(
        method=SpeechRecognitionMethod(method) if method != "auto" else SpeechRecognitionMethod.WHISPER_LOCAL,
        language=LanguageCode(language),
        model=model,
        enable_fallback=enable_fallback
    )
    
    recognizer = SpeechRecognizer()
    
    if method == "auto":
        # translatedSelectselecttranslated
        available_methods = recognizer.get_available_methods()
        
        # bytranslatedSelectselecttranslated（Whisperlocaltranslated，translated）
        priority_methods = [
            SpeechRecognitionMethod.WHISPER_LOCAL,
            SpeechRecognitionMethod.OPtranslatedAI_API,
            SpeechRecognitionMethod.AZURE_SPEECH,
            SpeechRecognitionMethod.GOOGLE_SPEECH,
            SpeechRecognitionMethod.ALIYUN_SPEECH,
            SpeechRecognitionMethod.CUSTOM_API
        ]
        
        for priority_method in priority_methods:
            if available_methods.get(priority_method, False):
                config.method = priority_method
                break
        else:
            raise SpeechRecognitionError("translatedcanuse'stranslatedservice，translatedinstallwhisperorconfigAPIkey")
    
    return recognizer.generate_subtitle(video_path, output_path, config)


def get_available_speech_recognition_methods() -> Dict[str, bool]:
    """
    fetchcanuse'stranslated
    
    Returns:
        canusetranslated
    """
    recognizer = SpeechRecognizer()
    available_methods = recognizer.get_available_methods()
    
    return {
        method.value: available 
        for method, available in available_methods.items()
    }


def get_supported_languages() -> List[str]:
    """
    fetchsupport'sLanguagelist
    
    Returns:
        support'sLanguagetranslatedlist
    """
    return [lang.value for lang in LanguageCode]


def get_whisper_models() -> List[str]:
    """
    fetchcanuse'sWhispermodellist
    
    Returns:
        Whispermodellist
    """
    return ["tiny", "base", "small", "medium", "large"]

