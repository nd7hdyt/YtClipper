"""
Whisper modeltranslatedservice（mlx-whisper）

translated mlx-community Whisper model'sdownload、statuscheck、delete。modelfrom HuggingFace translated，
translatedonecachetranslated `<data_dir>/whisper-models`（translated whisper_runtime settings HF_HOME）。
dependencies（huggingface_hub）translatedRuntimeinstalldirectory，translated import translated。
"""
import logging
import threading
from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from . import whisper_runtime

logger = logging.getLogger(__name__)


class ModelStatus(str, Enum):
    AVAILABLE = "available"      # Runtimetranslated、candownload
    DOWNLOADING = "downloading"  # downloadtranslated
    DOWNLOADED = "downloaded"    # translateddownload
    ERROR = "error"              # error（translatedIsRuntimetranslatedinstall）
    NOT_FOUND = "not_found"


@dataclass
class ModelInfo:
    name: str
    size: str
    size_bytes: int
    description: str
    accuracy: str
    speed: str
    status: ModelStatus
    repo_id: str = ""
    download_progress: Optional[int] = None
    local_path: Optional[str] = None
    error_message: Optional[str] = None


# modeltranslated -> HuggingFace translated + translatedinfo（faster-whisper / CTranslate2 model）
_MODELS = {
    "tiny": {
        "repo_id": "Systran/faster-whisper-tiny",
        "size": "~75 MB", "size_bytes": 75 * 1024 * 1024,
        "description": "translated，translated，translated", "accuracy": "translated", "speed": "translated",
    },
    "base": {
        "repo_id": "Systran/faster-whisper-base",
        "size": "~145 MB", "size_bytes": 145 * 1024 * 1024,
        "description": "translatedSelect，recommendtranslateduse", "accuracy": "translatedetc.", "speed": "translated",
    },
    "small": {
        "repo_id": "Systran/faster-whisper-small",
        "size": "~488 MB", "size_bytes": 488 * 1024 * 1024,
        "description": "translated，translated", "accuracy": "translated", "speed": "translatedetc.",
    },
    "medium": {
        "repo_id": "Systran/faster-whisper-medium",
        "size": "~1.5 GB", "size_bytes": 1500 * 1024 * 1024,
        "description": "translated，translatedusetranslated", "accuracy": "translated", "speed": "translated",
    },
    "large-v3": {
        "repo_id": "Systran/faster-whisper-large-v3",
        "size": "~3 GB", "size_bytes": 3000 * 1024 * 1024,
        "description": "translated", "accuracy": "translated", "speed": "translated",
    },
}


def repo_id_for(model_name: str) -> Optional[str]:
    cfg = _MODELS.get(model_name)
    return cfg["repo_id"] if cfg else None


class WhisperModelManager:
    def __init__(self):
        self.model_configs = _MODELS
        # model_name -> {"status","progress","error"}
        self._download_state: Dict[str, Dict] = {}
        self._lock = threading.Lock()

    # ---- path / status ----
    def _model_cache_dir(self, model_name: str) -> Path:
        repo = self.model_configs[model_name]["repo_id"]
        # HF cachedirectorytranslated：models--<org>--<name>
        return whisper_runtime.get_models_dir() / "hub" / ("models--" + repo.replace("/", "--"))

    def _is_downloaded(self, model_name: str) -> bool:
        d = self._model_cache_dir(model_name)
        snaps = d / "snapshots"
        return snaps.exists() and any(snaps.iterdir())

    def _check_model_status(self, model_name: str) -> ModelStatus:
        with self._lock:
            st = self._download_state.get(model_name)
        if st and st.get("status") == "downloading":
            return ModelStatus.DOWNLOADING
        if st and st.get("status") == "error":
            return ModelStatus.ERROR
        if self._is_downloaded(model_name):
            return ModelStatus.DOWNLOADED
        if not whisper_runtime.is_installed():
            return ModelStatus.ERROR  # Runtimetranslated，modeltranslatedusetranslated
        return ModelStatus.AVAILABLE

    def _info(self, model_name: str) -> ModelInfo:
        cfg = self.model_configs[model_name]
        status = self._check_model_status(model_name)
        with self._lock:
            st = self._download_state.get(model_name, {})
        return ModelInfo(
            name=model_name,
            size=cfg["size"], size_bytes=cfg["size_bytes"],
            description=cfg["description"], accuracy=cfg["accuracy"], speed=cfg["speed"],
            status=status, repo_id=cfg["repo_id"],
            download_progress=st.get("progress"),
            local_path=str(self._model_cache_dir(model_name)) if status == ModelStatus.DOWNLOADED else None,
            error_message=st.get("error"),
        )

    def get_all_models_info(self) -> List[ModelInfo]:
        return [self._info(name) for name in self.model_configs]

    def get_model_info(self, model_name: str) -> Optional[ModelInfo]:
        if model_name not in self.model_configs:
            return None
        return self._info(model_name)

    # ---- download（translated，translated）----
    async def download_model(self, model_name: str) -> bool:
        if model_name not in self.model_configs:
            raise ValueError(f"translatedsupport'smodel: {model_name}")
        if not whisper_runtime.is_installed():
            raise RuntimeError("translatedinstall Whisper Runtime")
        if self._is_downloaded(model_name):
            return True
        with self._lock:
            st = self._download_state.get(model_name)
            if st and st.get("status") == "downloading":
                return True
            self._download_state[model_name] = {"status": "downloading", "progress": 0, "error": None}
        threading.Thread(
            target=self._download_blocking, args=(model_name,),
            name=f"whisper-dl-{model_name}", daemon=True,
        ).start()
        return True

    def _download_blocking(self, model_name: str) -> None:
        repo_id = self.model_configs[model_name]["repo_id"]
        try:
            whisper_runtime.ensure_on_path()
            from huggingface_hub import snapshot_download
            logger.info(f"translateddownload Whisper model {model_name} ({repo_id})")
            snapshot_download(
                repo_id=repo_id,
                cache_dir=str(whisper_runtime.get_models_dir() / "hub"),
            )
            with self._lock:
                self._download_state[model_name] = {"status": "downloaded", "progress": 100, "error": None}
            logger.info(f"Whisper model {model_name} downloadtranslated")
        except Exception as e:  # noqa: BLE001
            logger.error(f"download Whisper model {model_name} failed: {e}", exc_info=True)
            with self._lock:
                self._download_state[model_name] = {"status": "error", "progress": 0, "error": str(e)}

    def get_download_progress(self, model_name: str) -> Optional[int]:
        with self._lock:
            st = self._download_state.get(model_name)
        if not st:
            return 100 if self._is_downloaded(model_name) else None
        return st.get("progress")

    def cancel_download(self, model_name: str) -> bool:
        # snapshot_download translated；thistranslatedstatus，translateddownloadtranslatedcantranslated
        with self._lock:
            if model_name in self._download_state and self._download_state[model_name].get("status") == "downloading":
                self._download_state[model_name] = {"status": "available", "progress": 0, "error": None}
                return True
        return False

    def delete_model(self, model_name: str) -> bool:
        if model_name not in self.model_configs:
            return False
        try:
            import shutil
            d = self._model_cache_dir(model_name)
            if d.exists():
                shutil.rmtree(d, ignore_errors=True)
            with self._lock:
                self._download_state.pop(model_name, None)
            logger.info(f"Whisper model {model_name} translateddelete")
            return True
        except Exception as e:  # noqa: BLE001
            logger.error(f"delete Whisper model {model_name} failed: {e}")
            return False


_model_manager: Optional[WhisperModelManager] = None


def get_model_manager() -> WhisperModelManager:
    global _model_manager
    if _model_manager is None:
        _model_manager = WhisperModelManager()
    return _model_manager
