"""
EN - ENservice
ENWhisper、OpenAI API、Azure Speech ServicesENservice
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
    """EN"""
    WHISPER_LOCAL = "whisper_local"
    OPENAI_API = "openai_api"
    AZURE_SPEECH = "azure_speech"
    GOOGLE_SPEECH = "google_speech"
    ALIYUN_SPEECH = "aliyun_speech"
    # ENserviceEN
    CUSTOM_API = "custom_api"


class LanguageCode(str, Enum):
    """EN"""
    # EN
    CHINESE_SIMPLIFIED = "zh"
    CHINESE_TRADITIONAL = "zh-TW"
    # EN
    ENGLISH = "en"
    ENGLISH_US = "en-US"
    ENGLISH_UK = "en-GB"
    # EN
    JAPANESE = "ja"
    # EN
    KOREAN = "ko"
    # EN
    FRENCH = "fr"
    # EN
    GERMAN = "de"
    # EN
    SPANISH = "es"
    # EN
    RUSSIAN = "ru"
    # EN
    ARABIC = "ar"
    # EN
    PORTUGUESE = "pt"
    # EN
    ITALIAN = "it"
    # EN
    AUTO = "auto"


@dataclass
class SpeechRecognitionConfig:
    """ENconfig"""
    method: SpeechRecognitionMethod = SpeechRecognitionMethod.WHISPER_LOCAL
    language: LanguageCode = LanguageCode.AUTO
    model: str = "base"  # WhisperEN
    timeout: int = 0  # timeouttime（EN），0EN
    output_format: str = "srt"  # EN
    enable_timestamps: bool = True  # ENtimeEN
    enable_punctuation: bool = True  # EN
    enable_speaker_diarization: bool = False  # EN
    enable_fallback: bool = True  # EN
    fallback_method: SpeechRecognitionMethod = SpeechRecognitionMethod.WHISPER_LOCAL  # EN
    
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
        """validateconfigparameters"""
        # validateEN
        if not isinstance(self.method, SpeechRecognitionMethod):
            try:
                self.method = SpeechRecognitionMethod(self.method)
            except ValueError:
                raise ValueError(f"EN: {self.method}")
        
        # validateEN
        if not isinstance(self.language, LanguageCode):
            try:
                self.language = LanguageCode(self.language)
            except ValueError:
                raise ValueError(f"EN: {self.language}")
        
        # validateEN
        valid_models = ["tiny", "base", "small", "medium", "large"]
        if self.model not in valid_models:
            raise ValueError(f"ENWhisperEN: {self.model}")
        
        # validatetimeouttime
        if self.timeout < 0:
            raise ValueError("timeouttimeEN")
        
        # validateEN
        valid_formats = ["srt", "vtt", "txt", "json"]
        if self.output_format not in valid_formats:
            raise ValueError(f"EN: {self.output_format}")


class SpeechRecognitionError(Exception):
    """ENerror"""
    pass


class SpeechRecognizer:
    """EN，ENservice"""
    
    def __init__(self, config: Optional[SpeechRecognitionConfig] = None):
        self.config = config or SpeechRecognitionConfig()
        self.available_methods = self._check_available_methods()
    
    def _check_available_methods(self) -> Dict[SpeechRecognitionMethod, bool]:
        """checkEN"""
        methods = {}
        
        # checkENWhisper
        methods[SpeechRecognitionMethod.WHISPER_LOCAL] = self._check_whisper_availability()
        
        # checkOpenAI API
        methods[SpeechRecognitionMethod.OPENAI_API] = self._check_openai_availability()
        
        # checkAzure Speech Services
        methods[SpeechRecognitionMethod.AZURE_SPEECH] = self._check_azure_speech_availability()
        
        # checkGoogle Speech-to-Text
        methods[SpeechRecognitionMethod.GOOGLE_SPEECH] = self._check_google_speech_availability()
        
        # checkEN
        methods[SpeechRecognitionMethod.ALIYUN_SPEECH] = self._check_aliyun_speech_availability()
        
        # checkENAPI
        methods[SpeechRecognitionMethod.CUSTOM_API] = self._check_custom_api_availability()
        
        return methods
    
    def _check_whisper_availability(self) -> bool:
        """checkEN Whisper(mlx) runEN。"""
        try:
            from backend.services import whisper_runtime
            return whisper_runtime.is_installed()
        except Exception:
            logger.warning("ENWhisperEN")
            return False
    
    def _check_openai_availability(self) -> bool:
        """checkOpenAI APIEN"""
        api_key = os.getenv("OPENAI_API_KEY")
        return api_key is not None and len(api_key.strip()) > 0
    
    def _check_azure_speech_availability(self) -> bool:
        """checkAzure Speech ServicesEN"""
        api_key = os.getenv("AZURE_SPEECH_KEY")
        region = os.getenv("AZURE_SPEECH_REGION")
        return api_key is not None and region is not None
    
    def _check_google_speech_availability(self) -> bool:
        """checkGoogle Speech-to-TextEN"""
        # checkGoogle CloudENfile
        cred_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if cred_file and Path(cred_file).exists():
            return True
        
        # checkAPIEN
        api_key = os.getenv("GOOGLE_SPEECH_API_KEY")
        return api_key is not None
    
    def _check_aliyun_speech_availability(self) -> bool:
        """checkEN"""
        try:
            # checkconfigENAPI Key
            # ENcancheckENorconfigENAPI Key
            access_key = os.getenv("ALIYUN_API_KEY") or (self.config.aliyun_access_key if hasattr(self, 'config') else None)
            return bool(access_key)
        except Exception:
            return False
    
    def _extract_audio_from_video(self, video_path: Path, output_dir: Path) -> Path:
        """
        ENvideofileEN
        
        Args:
            video_path: videofilepath
            output_dir: ENdirectory
            
        Returns:
            ENfilepath
        """
        try:
            # checkffmpegEN
            ffmpeg_bin = get_ffmpeg_path()
            result = subprocess.run([ffmpeg_bin, '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise SpeechRecognitionError("ffmpegEN，pleaseENffmpeg")
            
            # generateENfilepath
            audio_filename = f"{video_path.stem}_audio.wav"
            audio_path = output_dir / audio_filename
            
            # ifENfilealready exists，ENreturn
            if audio_path.exists():
                logger.info(f"ENfilealready exists: {audio_path}")
                return audio_path
            
            logger.info(f"currentlyENvideoEN: {video_path} -> {audio_path}")
            
            # useffmpegEN
            cmd = [
                ffmpeg_bin,
                '-i', str(video_path),
                '-vn',  # ENprocessingvideoEN
                '-acodec', 'pcm_s16le',  # usePCM 16EN
                '-ar', '16000',  # EN16kHz
                '-ac', '1',  # EN
                '-y',  # ENfile
                str(audio_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                raise SpeechRecognitionError(f"ENfailed: {result.stderr}")
            
            if not audio_path.exists():
                raise SpeechRecognitionError("ENfailed，ENfiledoes not exist")
            
            logger.info(f"ENsucceeded: {audio_path}")
            return audio_path
            
        except subprocess.TimeoutExpired:
            raise SpeechRecognitionError("ENtimeout")
        except Exception as e:
            raise SpeechRecognitionError(f"ENfailed: {e}")
    
    def generate_subtitle(self, video_path: Path, output_path: Optional[Path] = None, 
                         config: Optional[SpeechRecognitionConfig] = None) -> Path:
        """
        generatesubtitlesfile
        
        Args:
            video_path: videofilepath
            output_path: ENsubtitlesfilepath
            config: ENconfig
            
        Returns:
            generateENsubtitlesfilepath
            
        Raises:
            SpeechRecognitionError: ENfailed
        """
        if not video_path.exists():
            raise SpeechRecognitionError(f"videofiledoes not exist: {video_path}")
        
        # useENconfigENconfig
        config = config or self.config
        
        # ENpath
        if output_path is None:
            output_path = video_path.parent / f"{video_path.stem}.{config.output_format}"
        
        # ENconfigENservice，EN
        try:
            if config.method == SpeechRecognitionMethod.WHISPER_LOCAL:
                return self._generate_subtitle_whisper_local(video_path, output_path, config)
            elif config.method == SpeechRecognitionMethod.OPENAI_API:
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
                raise SpeechRecognitionError(f"EN: {config.method}")
        except SpeechRecognitionError as e:
            # ifENcurrentEN，thenEN
            if (config.enable_fallback and 
                config.method != config.fallback_method and 
                self.available_methods.get(config.fallback_method, False)):
                
                logger.warning(f"EN {config.method} failed: {e}")
                logger.info(f"EN {config.fallback_method}")
                
                # createENconfig
                fallback_config = SpeechRecognitionConfig(
                    method=config.fallback_method,
                    language=config.language,
                    model=config.model,
                    timeout=config.timeout,
                    output_format=config.output_format,
                    enable_timestamps=config.enable_timestamps,
                    enable_punctuation=config.enable_punctuation,
                    enable_speaker_diarization=config.enable_speaker_diarization,
                    enable_fallback=False  # EN
                )
                
                return self.generate_subtitle(video_path, output_path, fallback_config)
            else:
                raise
    
    def _check_custom_api_availability(self) -> bool:
        """checkENAPIEN"""
        # checkENconfigENAPI
        if self.config.custom_api_url and self.config.custom_api_key:
            try:
                # ENcheck
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
        """useEN faster-whisper generatesubtitles（ENrunEN）。"""
        from backend.services import whisper_runtime

        if not whisper_runtime.is_installed():
            raise SpeechRecognitionError(
                "EN Whisper runEN。pleaseEN「settings → EN」EN Whisper，"
                "ENdownloadEN。"
            )

        if not video_path.exists():
            raise SpeechRecognitionError(f"videofiledoes not exist: {video_path}")
        if video_path.stat().st_size == 0:
            raise SpeechRecognitionError(f"videofileEN: {video_path}")
        if output_path.exists():
            logger.info(f"subtitlesfilealready exists，ENWhisperprocessing: {output_path}")
            return output_path

        try:
            whisper_runtime.ensure_on_path()  # EN faster_whisper EN
            from faster_whisper import WhisperModel  # EN：runENdirectoryEN

            language = None if config.language == LanguageCode.AUTO else str(config.language).split("-")[0]
            models_dir = str(whisper_runtime.get_models_dir() / "hub")
            logger.info(f"use faster-whisper generatesubtitles: model={config.model} lang={language or 'auto'}")

            # device=auto：Mac EN CPU（CTranslate2），int8 EN
            model = WhisperModel(
                config.model, device="auto", compute_type="int8", download_root=models_dir,
            )
            seg_iter, _info = model.transcribe(str(video_path), language=language, vad_filter=True)
            segments = [{"start": s.start, "end": s.end, "text": s.text} for s in seg_iter]
            if not segments:
                raise SpeechRecognitionError("Whisper EN")

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(self._segments_to_srt(segments), encoding="utf-8")
            logger.info(f"EN faster-whisper subtitlesgeneratesucceeded: {output_path}")
            return output_path

        except SpeechRecognitionError:
            raise
        except ModuleNotFoundError as e:
            raise SpeechRecognitionError(
                f"Whisper runEN（{e}）。pleaseEN「settings → EN」EN Whisper。"
            )
        except Exception as e:  # noqa: BLE001
            logger.error(f"EN faster-whisper generatesubtitlesfailed: {e}", exc_info=True)
            raise SpeechRecognitionError(f"EN Whisper generatesubtitlesfailed: {e}")
    
    def _generate_subtitle_openai_api(self, video_path: Path, output_path: Path, 
                                    config: SpeechRecognitionConfig) -> Path:
        """useOpenAI APIgeneratesubtitles"""
        if not self.available_methods[SpeechRecognitionMethod.OPENAI_API]:
            raise SpeechRecognitionError("OpenAI APIEN，pleasesettingsOPENAI_API_KEYEN")
        
        try:
            logger.info(f"startuseOpenAI APIgeneratesubtitles: {video_path}")
            
            # ENneedENOpenAI APIcall
            # ENneedEN，ENexception
            raise SpeechRecognitionError("OpenAI APIEN，pleaseuseENWhisper")
            
        except Exception as e:
            error_msg = f"OpenAI APIgeneratesubtitlesENerror: {e}"
            logger.error(error_msg)
            raise SpeechRecognitionError(error_msg)
    
    def _generate_subtitle_azure_speech(self, video_path: Path, output_path: Path, 
                                      config: SpeechRecognitionConfig) -> Path:
        """useAzure Speech Servicesgeneratesubtitles"""
        if not self.available_methods[SpeechRecognitionMethod.AZURE_SPEECH]:
            raise SpeechRecognitionError("Azure Speech ServicesEN，pleasesettingsAZURE_SPEECH_KEYENAZURE_SPEECH_REGIONEN")
        
        try:
            logger.info(f"startuseAzure Speech Servicesgeneratesubtitles: {video_path}")
            
            # ENneedENAzure Speech Servicescall
            raise SpeechRecognitionError("Azure Speech ServicesEN，pleaseuseENWhisper")
            
        except Exception as e:
            error_msg = f"Azure Speech ServicesgeneratesubtitlesENerror: {e}"
            logger.error(error_msg)
            raise SpeechRecognitionError(error_msg)
    
    def _generate_subtitle_google_speech(self, video_path: Path, output_path: Path, 
                                       config: SpeechRecognitionConfig) -> Path:
        """useGoogle Speech-to-Textgeneratesubtitles"""
        if not self.available_methods[SpeechRecognitionMethod.GOOGLE_SPEECH]:
            raise SpeechRecognitionError("Google Speech-to-TextEN，pleasesettingsGOOGLE_APPLICATION_CREDENTIALSENGOOGLE_SPEECH_API_KEYEN")
        
        try:
            logger.info(f"startuseGoogle Speech-to-Textgeneratesubtitles: {video_path}")
            
            # ENneedENGoogle Speech-to-Textcall
            raise SpeechRecognitionError("Google Speech-to-TextEN，pleaseuseENWhisper")
            
        except Exception as e:
            error_msg = f"Google Speech-to-TextgeneratesubtitlesENerror: {e}"
            logger.error(error_msg)
            raise SpeechRecognitionError(error_msg)
    
    def _generate_subtitle_aliyun_speech(self, video_path: Path, output_path: Path, 
                                       config: SpeechRecognitionConfig) -> Path:
        """useENgeneratesubtitles"""
        if not self.available_methods[SpeechRecognitionMethod.ALIYUN_SPEECH]:
            raise SpeechRecognitionError("EN，pleaseconfigAPI Key")
        
        try:
            logger.info(f"startuseENgeneratesubtitles: {video_path}")
            
            # checkvideofileEN
            if not video_path.exists():
                raise SpeechRecognitionError(f"videofiledoes not exist: {video_path}")
            
            # ENfile
            audio_path = self._extract_audio_from_video(video_path, output_path.parent)
            
            # useENAPI
            # EN：ENuseENservice，ENuseqwen3-asr-flashEN
            import requests
            import base64
            
            # readENfileEN
            with open(audio_path, 'rb') as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
            
            # ENrequestEN
            request_data = {
                "model": "qwen3-asr-flash",  # useENASREN
                "input": {
                    "audio": f"data:audio/wav;base64,{audio_data}"
                },
                "parameters": {
                    "format": "srt",  # ENSRTEN
                    "enable_timestamps": config.enable_timestamps,
                    "enable_punctuation": config.enable_punctuation
                }
            }
            
            # sendrequestENAPI
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
                    # savesubtitlesfile
                    subtitle_content = result['output']['text']
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(subtitle_content)
                    
                    logger.info(f"ENsubtitlesgeneratesucceeded: {output_path}")
                    return output_path
                else:
                    raise SpeechRecognitionError("ENreturnresultEN")
            else:
                error_detail = response.json().get('message', 'Unknown error') if response.headers.get('content-type', '').startswith('application/json') else response.text
                raise SpeechRecognitionError(f"ENAPIcallfailed: {response.status_code} - {error_detail}")
            
        except Exception as e:
            error_msg = f"ENgeneratesubtitlesENerror: {e}"
            logger.error(error_msg)
            raise SpeechRecognitionError(error_msg)
    
    def _generate_subtitle_custom_api(self, video_path: Path, output_path: Path, 
                                     config: SpeechRecognitionConfig) -> Path:
        """useENAPIgeneratesubtitles"""
        if not config.custom_api_url or not config.custom_api_key:
            raise SpeechRecognitionError(
                "ENAPIconfigEN，pleaseconfig custom_api_url EN custom_api_key"
            )
        
        try:
            logger.info(f"startuseENAPIgeneratesubtitles: {video_path}")
            
            # checkvideofileEN
            if not video_path.exists():
                raise SpeechRecognitionError(f"videofiledoes not exist: {video_path}")
            
            # ENfile
            audio_path = self._extract_audio_from_video(video_path, output_path.parent)
            
            # ENAPIrequest
            headers = {
                'Authorization': f'Bearer {config.custom_api_key}',
                'Content-Type': 'audio/wav'
            }
            
            # sendENfileENAPI
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
                # savesubtitlesfile
                subtitle_content = response.text
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(subtitle_content)
                
                logger.info(f"ENAPIsubtitlesgeneratesucceeded: {output_path}")
                return output_path
            else:
                raise SpeechRecognitionError(f"ENAPIcallfailed: {response.status_code} - {response.text}")
                
        except Exception as e:
            error_msg = f"ENAPIgeneratesubtitlesENerror: {e}"
            logger.error(error_msg)
            raise SpeechRecognitionError(error_msg)
    
    def get_available_methods(self) -> Dict[SpeechRecognitionMethod, bool]:
        """fetchEN"""
        return self.available_methods.copy()
    
    def get_supported_languages(self) -> List[LanguageCode]:
        """fetchEN"""
        return list(LanguageCode)
    
    def get_whisper_models(self) -> List[str]:
        """fetchENWhisperEN"""
        return ["tiny", "base", "small", "medium", "large"]


def generate_subtitle_for_video(video_path: Path, output_path: Optional[Path] = None, 
                               method: str = "auto", language: str = "auto", 
                               model: str = "base", enable_fallback: bool = True) -> Path:
    """
    ENvideogeneratesubtitlesfileEN
    
    Args:
        video_path: videofilepath
        output_path: ENsubtitlesfilepath
        method: generateEN ("auto", "whisper_local", "openai_api", "azure_speech", "google_speech", "aliyun_speech", "custom_api")
        language: EN
        model: WhisperEN（ENwhisper_localEN）
        enable_fallback: EN
        
    Returns:
        generateENsubtitlesfilepath
        
    Raises:
        SpeechRecognitionError: ENfailed
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
        # EN
        available_methods = recognizer.get_available_methods()
        
        # EN（WhisperEN，becauseEN）
        priority_methods = [
            SpeechRecognitionMethod.WHISPER_LOCAL,
            SpeechRecognitionMethod.OPENAI_API,
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
            raise SpeechRecognitionError("ENservice，pleaseENwhisperENconfigAPIEN")
    
    return recognizer.generate_subtitle(video_path, output_path, config)


def get_available_speech_recognition_methods() -> Dict[str, bool]:
    """
    fetchEN
    
    Returns:
        EN
    """
    recognizer = SpeechRecognizer()
    available_methods = recognizer.get_available_methods()
    
    return {
        method.value: available 
        for method, available in available_methods.items()
    }


def get_supported_languages() -> List[str]:
    """
    fetchEN
    
    Returns:
        EN
    """
    return [lang.value for lang in LanguageCode]


def get_whisper_models() -> List[str]:
    """
    fetchENWhisperEN
    
    Returns:
        WhisperEN
    """
    return ["tiny", "base", "small", "medium", "large"]

