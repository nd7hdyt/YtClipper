#!/usr/bin/env python3
"""
EN CHANGELOG.md ENVersionEN，ENInstallEN，EN GitHub Release WhenEN。
desktop-build.yml EN release job EN；EN：

    python scripts/release_notes.py v1.3.0            # EN
    python scripts/release_notes.py v1.3.0 -o body.md

VersionEN CHANGELOG EN（ENFailed）。EN。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"

PLATFORM_NOTES = """\
### Download / Download

| EN | EN | EN |
|---|---|---|
| macOS（Apple Silicon）| `AutoClip.Desktop_{ver}_aarch64.dmg` | EN：EN → **EN** |
| Windows 10/11 x64 | `AutoClip.Desktop_{ver}_x64-setup.exe` | EN：SmartScreen → **EN → EN** |

EN Python EN ffmpeg，ENNeedEN；Windows InstallENInstall，ENNeedEN，EN WebView2 ENAutoDownload。
Intel Mac / Linux ENInstallEN，PleaseEN Docker（`DOCKER.md`）EN `pip install -e .` EN `autoclip` CLI。

Built-in portable Python + static ffmpeg, nothing to install. macOS build is ad-hoc signed (right-click → Open on first launch);
Windows build is unsigned (SmartScreen → More info → Run anyway). If a file is missing, that platform's build failed for this tag — see the Desktop Build workflow run.

### EN / Feedback
- ENCurrentStatus：#96 · Bug / EN [Issue EN](https://github.com/nd7hdyt/YtClipper/issues/new/choose) · EN GitHub EN[EN](https://my.feishu.cn/share/base/shrcn8hKUG2icIJLpNry6uWVNJe)
"""


def changelog_section(version: str) -> str | None:
    """EN `## [version]` EN `## [` EN（EN）。"""
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
        parts.append(f"_CHANGELOG.md EN [{ver}] EN；EN [CHANGELOG.md](https://github.com/nd7hdyt/YtClipper/blob/main/CHANGELOG.md)。_\n")
    parts.append(PLATFORM_NOTES.format(ver=ver))
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tag", help="EN v1.3.0")
    ap.add_argument("-o", "--output", help="EN；ENThenEN stdout")
    args = ap.parse_args(argv)

    body = build(args.tag)
    if args.output:
        Path(args.output).write_text(body, encoding="utf-8")
    else:
        sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
