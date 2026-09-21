"""
FFmpeg ENexecutepathparseEN

EN：
1) EN AUTOCLIP_FFMPEG_PATH / AUTOCLIP_FFPROBE_PATH / FFMPEG_PATH / FFPROBE_PATH
2) system PATH EN ffmpeg/ffprobe

EN：ENallcallEN ffmpeg/ffprobe path，EN。
"""

import os
import shutil
from typing import Optional


def _resolve_from_env(var_names: list[str]) -> Optional[str]:
    for var in var_names:
        value = os.getenv(var)
        if value and os.path.exists(value):
            return value
    return None


def get_ffmpeg_path() -> str:
    """return ffmpeg ENexecutefilepath（EN）。"""
    # 1) EN
    env_path = _resolve_from_env([
        "AUTOCLIP_FFMPEG_PATH",
        "FFMPEG_PATH",
    ])
    if env_path:
        return env_path

    # 2) system PATH
    which = shutil.which("ffmpeg")
    if which:
        return which

    # 3) ENreturnEN（mayENfailed，EN）
    return "ffmpeg"


def get_ffprobe_path() -> str:
    """return ffprobe ENexecutefilepath（EN）。"""
    # 1) EN
    env_path = _resolve_from_env([
        "AUTOCLIP_FFPROBE_PATH",
        "FFPROBE_PATH",
    ])
    if env_path:
        return env_path

    # 2) system PATH
    which = shutil.which("ffprobe")
    if which:
        return which

    # 3) ENreturnEN
    return "ffprobe"


