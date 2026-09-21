#!/usr/bin/env python3
"""
from CHANGELOG.md translated version'stranslated，translatedinstalltranslated，translated GitHub Release translated。
desktop-build.yml 's release job translated；localtranslatedcantranslated：

    python scripts/release_notes.py v1.3.0            # translated
    python scripts/release_notes.py v1.3.0 -o body.md

versionin CHANGELOG translated（translatedfailed）。translatedusetranslated。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"

PLATFORM_NOTES = """\
### download / Download

| translated | file | translated |
|---|---|---|
| macOS（Apple Silicon）| `AutoClip.Desktop_{ver}_aarch64.dmg` | translatedNotarization：translateduse → **translated** |
| Windows 10/11 x64 | `AutoClip.Desktop_{ver}_x64-setup.exe` | translatedSignature：SmartScreen → **translatedmultiinfo → translated** |

translated PackagetranslatedBuilt-intranslated Python andStatic ffmpeg，No needPre-installtranslated；Windows installPackagebyuserinstall，No needtranslated，translated WebView2 translateddownload。
Intel Mac / Linux Not yetinstallPackage，translateduse Docker（`DOCKER.md`）or `pip install -e .` translated `autoclip` CLI。

Built-in portable Python + static ffmpeg, nothing to install. macOS build is ad-hoc signed (right-click → Open on first launch);
Windows build is unsigned (SmartScreen → More info → Run anyway). If a file is missing, that platform's build failed for this tag — see the Desktop Build workflow run.

### translated / Feedback
- translatedissueandtranslatedstatus：#96 · Bug / translated [Issue translated](https://github.com/zhouxiaoka/autoclip/issues/new/choose) · translateduse GitHub cantranslated[translated](https://my.feishu.cn/share/base/shrcn8hKUG2icIJLpNry6uWVNJe)
"""


def changelog_section(version: str) -> str | None:
    """return `## [version]` translatedone  `## [` translated'stranslated（translatedincludetranslated）。"""
    if not CHANGELOG.exists():
        return None
    text = CHANGELOG.read_text(encoding="utf-8")
    m = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)", text, re.MULTILINE | re.DOTALL)
    if not m:
        return None
    body = m.group(1).strip()
    return body or None


def build(tag: str) -> str:
    ver = tag.lstrip("v")
    parts = [f"## AutoClip Desktop v{ver}\n"]
    section = changelog_section(ver)
    if section:
        parts.append(section + "\n")
    else:
        parts.append(f"_CHANGELOG.md translated [{ver}] translated；translated [CHANGELOG.md](https://github.com/zhouxiaoka/autoclip/blob/main/CHANGELOG.md)。_\n")
    parts.append(PLATFORM_NOTES.format(ver=ver))
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tag", help="if v1.3.0")
    ap.add_argument("-o", "--output", help="translatedfile；translated stdout")
    args = ap.parse_args(argv)

    body = build(args.tag)
    if args.output:
        Path(args.output).write_text(body, encoding="utf-8")
    else:
        sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
