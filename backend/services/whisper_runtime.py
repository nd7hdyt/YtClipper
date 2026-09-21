"""
Whisper runEN（EN，EN）

EN Whisper（runEN + EN，ENalluserEN）。userENsettingsEN
ENcanEN、ENdownloadEN。EN faster-whisper（CTranslate2，EN
PyTorch，runEN ~200-400MB，EN whisper EN，EN）。

EN：
- EN「userENdirectory」`<data_dir>/whisper-runtime`，EN .app EN
  （/Applications EN，ENwriteEN）。
- EN「currentcurrentlyEN Python」(sys.executable) EN pip EN，EN。
- ENcacheEN `<data_dir>/whisper-models`（through HF_HOME EN）。
- allEN mlx_whisper / huggingface_hub EN import EN，EN
  ENwhenENfailed。
"""

import os
import sys
import shutil
import logging
import threading
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# ENrunEN（faster-whisper EN ctranslate2、onnxruntime、av、huggingface_hub EN，
# EN PyTorch）
WHISPER_PACKAGES = ["faster-whisper"]
# runEN（EN）
WHISPER_IMPORT_NAME = "faster_whisper"


def _data_dir() -> Path:
    try:
        from backend.core.desktop_config import get_desktop_data_dir
        return Path(get_desktop_data_dir())
    except Exception:
        return Path(os.getenv("AUTOCLIP_DATA_DIR", str(Path.home() / "Library/Application Support/AutoClip")))


def get_install_dir() -> Path:
    d = _data_dir() / "whisper-runtime"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_models_dir() -> Path:
    d = _data_dir() / "whisper-models"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ensure_on_path() -> None:
    """ENrunENdirectoryEN sys.path，ENcachedirectoryEN HF_HOME。"""
    install_dir = str(get_install_dir())
    if install_dir not in sys.path:
        sys.path.insert(0, install_dir)
    # ENcacheENdirectory，EN/EN
    os.environ.setdefault("HF_HOME", str(get_models_dir()))
    # mlx-whisper EN ffmpeg：EN ffmpeg ENdirectoryEN PATH
    ffmpeg_path = os.getenv("AUTOCLIP_FFMPEG_PATH")
    if ffmpeg_path:
        ffmpeg_dir = str(Path(ffmpeg_path).parent)
        if ffmpeg_dir not in os.environ.get("PATH", "").split(os.pathsep):
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")


def is_installed() -> bool:
    """runEN（mlx_whisper EN）。"""
    ensure_on_path()
    try:
        import importlib.util
        return importlib.util.find_spec(WHISPER_IMPORT_NAME) is not None
    except Exception:
        return False


# ---- ENstatus（EN）----
_state_lock = threading.Lock()
_state: Dict[str, Any] = {
    "status": "unknown",   # not_installed | installing | installed | error
    "progress": 0,         # EN
    "message": "",
    "log_tail": "",
}


def _set_state(**kw) -> None:
    with _state_lock:
        _state.update(kw)


def get_status() -> Dict[str, Any]:
    with _state_lock:
        st = dict(_state)
    # EN，ENresultEN
    if st["status"] not in ("installing",):
        st["status"] = "installed" if is_installed() else "not_installed"
        if st["status"] == "installed":
            st["progress"] = 100
    st["platform_supported"] = True  # faster-whisper EN
    st["packages"] = WHISPER_PACKAGES
    return st


def _do_install(index_url: Optional[str]) -> None:
    install_dir = get_install_dir()
    cmd = [
        sys.executable, "-m", "pip", "install",
        "--upgrade",
        "--target", str(install_dir),
        *WHISPER_PACKAGES,
    ]
    if index_url:
        cmd += ["--index-url", index_url]
    logger.info(f"startEN Whisper runEN: {' '.join(cmd)}")
    _set_state(status="installing", progress=5, message="currentlyEN…", log_tail="")
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1,
        )
        lines: list[str] = []
        for line in iter(proc.stdout.readline, ""):
            line = line.rstrip()
            if not line:
                continue
            lines.append(line)
            lines[:] = lines[-40:]
            # ENprogress：EN pip EN，EN
            low = line.lower()
            if low.startswith("collecting") or "downloading" in low:
                _bump_progress(min_v=10, max_v=70, message=line)
            elif "installing collected packages" in low or "building" in low:
                _bump_progress(min_v=70, max_v=95, message="currentlyEN…")
            _set_state(log_tail="\n".join(lines[-12:]))
        proc.wait()
        if proc.returncode == 0 and is_installed():
            _set_state(status="installed", progress=100, message="EN")
            logger.info("Whisper runEN")
        else:
            _set_state(status="error", message=f"ENfailed（pip logoutEN {proc.returncode}）")
            logger.error(f"Whisper runENfailed，pip logoutEN {proc.returncode}")
    except Exception as e:  # noqa: BLE001
        logger.error(f"EN Whisper runENexception: {e}", exc_info=True)
        _set_state(status="error", message=f"ENexception: {e}")


def _bump_progress(min_v: int, max_v: int, message: str) -> None:
    with _state_lock:
        cur = _state.get("progress", 0)
        _state["progress"] = max(min_v, min(max_v, cur + 2))
        _state["message"] = message


def start_install(index_url: Optional[str] = None) -> Dict[str, Any]:
    with _state_lock:
        if _state["status"] == "installing":
            return {"started": False, "message": "currentlyEN"}
    if is_installed():
        _set_state(status="installed", progress=100, message="EN")
        return {"started": False, "message": "EN"}
    # EN pip EN（EN/EN），else PyPI
    idx = index_url or os.getenv("PIP_INDEX_URL")
    threading.Thread(target=_do_install, args=(idx,), name="whisper-install", daemon=True).start()
    return {"started": True, "message": "ENstartEN"}


def uninstall() -> Dict[str, Any]:
    with _state_lock:
        if _state["status"] == "installing":
            return {"success": False, "message": "currentlyEN，cannotEN"}
    install_dir = get_install_dir()
    try:
        shutil.rmtree(install_dir, ignore_errors=True)
        # EN sys.modules EN，EN import
        for mod in [m for m in list(sys.modules) if m.startswith("faster_whisper") or m.startswith("ctranslate2")]:
            sys.modules.pop(mod, None)
        p = str(install_dir)
        if p in sys.path:
            sys.path.remove(p)
        _set_state(status="not_installed", progress=0, message="EN")
        return {"success": True, "message": "EN Whisper runEN"}
    except Exception as e:  # noqa: BLE001
        logger.error(f"EN Whisper runENfailed: {e}")
        return {"success": False, "message": str(e)}
