"""
EN（Ollama / LM Studio）。

EN OpenAI ENAPI（provider=openai + base_url），EN「provider EN → EN /
EN / EN」EN，ENsettingsEN、CLI、MCP EN `--provider ollama` EN，
EN `http://localhost:11434/v1`。

settingsfileEN `api_provider` EN `ollama` / `lmstudio`；`LLMManager` loadENthrough
`resolve_provider()` EN openai + base_url。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class LocalPreset:
    key: str
    display_name: str
    base_url: str
    default_model: str
    docs_url: str
    hint: str


LOCAL_PRESETS: Dict[str, LocalPreset] = {
    "ollama": LocalPreset(
        key="ollama",
        display_name="Ollama（EN）",
        base_url="http://localhost:11434/v1",
        default_model="qwen2.5:7b",
        docs_url="https://ollama.com/download",
        hint="ENrun Ollama EN，EN。EN `ollama pull qwen2.5:7b`（ENsubtitlesanalysisEN）。",
    ),
    "lmstudio": LocalPreset(
        key="lmstudio",
        display_name="LM Studio（EN）",
        base_url="http://localhost:1234/v1",
        default_model="",
        docs_url="https://lmstudio.ai",
        hint="EN LM Studio ENloadENstart Local Server（EN 1234），ENserviceEN。",
    ),
}

# EN
_ALIASES = {"lm-studio": "lmstudio", "lm_studio": "lmstudio", "local": "ollama"}


def normalize_preset_key(name: Optional[str]) -> Optional[str]:
    """returnEN key；ENthenreturn None。"""
    if not name:
        return None
    key = name.strip().lower()
    key = _ALIASES.get(key, key)
    return key if key in LOCAL_PRESETS else None


def resolve_provider(provider: Optional[str], base_url: Optional[str] = None) -> Tuple[str, str, Optional[str]]:
    """
    ENuserEN provider（mayEN `ollama` / `lmstudio`）EN provider EN base_url。

    return (provider_value, base_url, preset_key)。ENreturn (provider, base_url or "", None)。
    """
    preset_key = normalize_preset_key(provider)
    if not preset_key:
        return (provider or "dashscope").strip().lower(), (base_url or "").strip(), None
    preset = LOCAL_PRESETS[preset_key]
    return "openai", (base_url or "").strip() or preset.base_url, preset_key


def preset_display_name(preset_key: Optional[str]) -> Optional[str]:
    p = LOCAL_PRESETS.get(preset_key or "")
    return p.display_name if p else None


def presets_as_dicts() -> list[dict]:
    return [
        {
            "key": p.key,
            "display_name": p.display_name,
            "base_url": p.base_url,
            "default_model": p.default_model,
            "docs_url": p.docs_url,
            "hint": p.hint,
        }
        for p in LOCAL_PRESETS.values()
    ]
