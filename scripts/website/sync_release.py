#!/usr/bin/env python3
"""
EN index.html ENVersionEN / DownloadEN / InstallEN（EN）Release。

    python scripts/sync_release.py            # EN zhouxiaoka/autoclip EN latest release
    python scripts/sync_release.py v1.3.0     # EN tag
    python scripts/sync_release.py --check    # EN，EN（EN 1 = EN）

EN README EN「ENVersionEN」EN：
  1. hero ENDownloadENVersionEN、DownloadEN（EN）
  2. DownloadENInstallEN
  3. hero.note ENVersionEN

EN；EN .github/workflows/sync-release.yml EN（repository_dispatch / EN cron / Manual）。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
REPO = "zhouxiaoka/autoclip"
ASSETS = {
    "mac": re.compile(r"^AutoClip\.Desktop_(?P<ver>[\d.]+)_aarch64\.dmg$"),
    "win": re.compile(r"^AutoClip\.Desktop_(?P<ver>[\d.]+)_x64-setup\.exe$"),
}


def fetch_release(tag: str | None) -> dict:
    url = f"https://api.github.com/repos/{REPO}/releases/" + (f"tags/{tag}" if tag else "latest")
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "autoclip-intro-sync"})
    token = os.getenv("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def pick_assets(release: dict) -> dict[str, dict]:
    found: dict[str, dict] = {}
    for asset in release.get("assets", []):
        for key, pattern in ASSETS.items():
            if pattern.match(asset["name"]):
                found[key] = {"name": asset["name"], "size_mb": round(asset["size"] / 1024 / 1024)}
    missing = [k for k in ASSETS if k not in found]
    if missing:
        raise SystemExit(f"Release {release.get('tag_name')} EN：{missing}（ENFailed，EN Release ENUpload）")
    return found


def current_version(html: str) -> str:
    m = re.search(r"releases/download/v(\d+\.\d+\.\d+)/", html)
    if not m:
        raise SystemExit("index.html EN releases/download/vX.Y.Z/ ENDownloadEN")
    return m.group(1)


def rewrite(html: str, old: str, new: str, assets: dict[str, dict]) -> str:
    old_re = re.escape(old)
    # 1. DownloadEN、JS EN REL / MAC / WIN、hero.note ENAllVersionEN（EN v EN Desktop_ EN，EN）
    html = re.sub(rf"(?<=/v){old_re}(?=/)", new, html)                 # releases/download/v1.2.1/
    html = re.sub(rf"(?<=Desktop_){old_re}(?=_)", new, html)           # AutoClip.Desktop_1.2.1_...
    html = re.sub(rf"\bv{old_re}\b", f"v{new}", html)                  # EN v1.2.1
    # 2. DownloadEN：<span class="ver">vX.Y.Z · NNN MB</span>，EN macOS EN，EN Windows EN
    sizes = iter([assets["mac"]["size_mb"], assets["win"]["size_mb"]])

    def _size(m: re.Match) -> str:
        return f'{m.group(1)}{next(sizes)} MB'

    html, n = re.subn(rf'(<span class="ver">v{re.escape(new)} · )\d+ MB', _size, html, count=2)
    if n != 2:
        print(f"EN：EN {n}/2 ENInstallEN", file=sys.stderr)
    return html


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tag", nargs="?", help="EN v1.3.0；ENThenEN latest")
    ap.add_argument("--check", action="store_true", help="EN，EN")
    args = ap.parse_args(argv)

    release = fetch_release(args.tag)
    tag = release["tag_name"]
    new = tag.lstrip("v")
    assets = pick_assets(release)

    html = INDEX.read_text(encoding="utf-8")
    old = current_version(html)
    print(f"ENCurrent v{old} → Release {tag}（mac {assets['mac']['size_mb']} MB / win {assets['win']['size_mb']} MB）")

    updated = rewrite(html, old, new, assets)
    if updated == html:
        print("EN，EN")
        return 0
    if args.check:
        print("EN Release")
        return 1
    INDEX.write_text(updated, encoding="utf-8")
    changed = sum(1 for a, b in zip(html.splitlines(), updated.splitlines()) if a != b)
    print(f"index.html EN（{changed} EN）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
