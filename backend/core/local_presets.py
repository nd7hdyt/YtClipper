"""
localmodeltranslated（Ollama / LM Studio）。

translatedIs OpenAI translated（provider=openai + base_url），thistranslatedIs 「provider translated → defaulttranslated /
defaultmodel / translated」translated，translatedSettings page、CLI、MCP translateduse `--provider ollama` thistranslated，
translatedusetranslated `http://localhost:11434/v1`。

settingsfiletranslated  `api_provider` translated `ollama` / `lmstudio`；`LLMManager` translated
`resolve_provider()` translated openai + base_url。
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
        display_name="Ollama（local）",
        base_url="http://localhost:11434/v1",
        default_model="qwen2.5:7b",
        docs_url="https://ollama.com/download",
        hint="translated Ollama translatedcanuse，translatedkey。recommend `ollama pull qwen2.5:7b`（translatedsubtitlestranslated）。",
    ),
    "lmstudio": LocalPreset(
        key="lmstudio",
        display_name="LM Studio（local）",
        base_url="http://localhost:1234/v1",
        default_model="",
        docs_url="https://lmstudio.ai",
        hint="in LM Studio translatedmodeltranslatedstart Local Server（defaulttranslated 1234），modeltranslatedservicetranslated'sAs Standard。",
    ),
}

# translated
_ALIASES = {"lm-studio": "lmstudio", "lm_studio": "lmstudio", "local": "ollama"}


def normalize_preset_key(name: Optional[str]) -> Optional[str]:
    """returntranslated'stranslated key；translatedIstranslatedreturn None。"""
    if not name:
        return None
    key = name.strip().lower()
    key = _ALIASES.get(key, key)
    return key if key in LOCAL_PRESETS else None


def resolve_provider(provider: Optional[str], base_url: Optional[str] = None) -> Tuple[str, str, Optional[str]]:
    """
     usertranslated's provider（cantranslatedIs `ollama` / `lmstudio`）translated's provider and base_url。

    return (provider_value, base_url, preset_key)。translatedreturn (provider, base_url or "", None)。
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
