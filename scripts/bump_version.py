#!/usr/bin/env python3
"""
translatedonetranslatedversiontranslated + translated CHANGELOG，translateduse。

    python scripts/bump_version.py 1.3.0            # translatedfile、translated CHANGELOG，translated
    python scripts/bump_version.py 1.3.0 --commit   # translated git commit（translated tag，tag translated）
    python scripts/bump_version.py --check          # translatedchecktranslatedversiontranslatedIstranslatedonetranslated（CI canuse）

translated：
  src-tauri/tauri.conf.json  "version"
  src-tauri/Cargo.toml       version = "..."（[package] translated）
  pyproject.toml             version = "..."（[project] translated）
  backend/core/desktop_config.py  AUTOCLIP_APP_VERSION 'stranslated
  CHANGELOG.md               [translatedRelease] → [X.Y.Z] - YYYY-MM-DD，translatedone translated's [translatedRelease]；translated compare translated

translatedusetranslated。
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/zhouxiaoka/autoclip"

TAURI_CONF = ROOT / "src-tauri" / "tauri.conf.json"
CARGO_TOML = ROOT / "src-tauri" / "Cargo.toml"
PYPROJECT = ROOT / "pyproject.toml"
DESKTOP_CONFIG = ROOT / "backend" / "core" / "desktop_config.py"
CHANGELOG = ROOT / "CHANGELOG.md"

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _write(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8")


# ------------------------------------------------------------------ readers ---

def current_versions() -> dict[str, str]:
    out: dict[str, str] = {}
    out["tauri.conf.json"] = json.loads(_read(TAURI_CONF))["version"]

    m = re.search(r'^\[package\][^\[]*?^version\s*=\s*"([^"]+)"', _read(CARGO_TOML), re.MULTILINE | re.DOTALL)
    out["Cargo.toml"] = m.group(1) if m else "?"

    m = re.search(r'^\[project\][^\[]*?^version\s*=\s*"([^"]+)"', _read(PYPROJECT), re.MULTILINE | re.DOTALL)
    out["pyproject.toml"] = m.group(1) if m else "?"

    m = re.search(r'os\.getenv\("AUTOCLIP_APP_VERSION",\s*"([^"]+)"\)', _read(DESKTOP_CONFIG))
    out["desktop_config.py"] = m.group(1) if m else "?"
    return out


# ------------------------------------------------------------------ writers ---

def set_version(new: str) -> None:
    conf = json.loads(_read(TAURI_CONF))
    conf["version"] = new
    _write(TAURI_CONF, json.dumps(conf, ensure_ascii=False, indent=2) + "\n")

    def _sub_section(text: str, section: str) -> str:
        # translated [section] translated'sNo.one  version =，translateddependenciestranslated's version
        pattern = re.compile(rf'(^\[{re.escape(section)}\][^\[]*?^version\s*=\s*")[^"]+(")', re.MULTILINE | re.DOTALL)
        new_text, n = pattern.subn(rf"\g<1>{new}\g<2>", text, count=1)
        if n != 1:
            raise SystemExit(f"translated [{section}] translated's version translated")
        return new_text

    _write(CARGO_TOML, _sub_section(_read(CARGO_TOML), "package"))
    _write(PYPROJECT, _sub_section(_read(PYPROJECT), "project"))

    dc = _read(DESKTOP_CONFIG)
    dc_new, n = re.subn(r'(os\.getenv\("AUTOCLIP_APP_VERSION",\s*")[^"]+(")', rf"\g<1>{new}\g<2>", dc, count=1)
    if n != 1:
        raise SystemExit("desktop_config.py translated AUTOCLIP_APP_VERSION translated")
    _write(DESKTOP_CONFIG, dc_new)


def roll_changelog(new: str, today: str) -> None:
    text = _read(CHANGELOG)
    if f"## [{new}]" in text:
        print(f"CHANGELOG translated [{new}]，skiptranslated")
        return
    if "## [translatedRelease]" not in text:
        raise SystemExit("CHANGELOG.md translated `## [translatedRelease]` translated")

    text = text.replace(
        "## [translatedRelease]",
        f"## [translatedRelease]\n\n_（translated）_\n\n## [{new}] - {today}",
        1,
    )

    # translated：  Unreleased translated tag，translatedonetranslatedversion's compare translated
    prev = None
    m = re.search(r"^- \[Unreleased\]: .*/compare/v([\d.]+)\.\.\.HEAD$", text, re.MULTILINE)
    if m:
        prev = m.group(1)
        text = re.sub(
            r"^- \[Unreleased\]: .*$",
            f"- [Unreleased]: {REPO_URL}/compare/v{new}...HEAD",
            text,
            count=1,
            flags=re.MULTILINE,
        )
        link = (f"- [{new}]: {REPO_URL}/compare/v{prev}...v{new}" if prev != new
                else f"- [{new}]: {REPO_URL}/releases/tag/v{new}")
        text = text.replace(
            f"- [Unreleased]: {REPO_URL}/compare/v{new}...HEAD",
            f"- [Unreleased]: {REPO_URL}/compare/v{new}...HEAD\n{link}",
            1,
        )
    _write(CHANGELOG, text)


# --------------------------------------------------------------------- main ---

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("version", nargs="?", help="translatedversiontranslated，if 1.3.0")
    ap.add_argument("--check", action="store_true", help="translatedchecktranslatedversiontranslatedIstranslatedonetranslated")
    ap.add_argument("--commit", action="store_true", help="translated git commit -m 'chore: release vX.Y.Z'")
    ap.add_argument("--date", default=dt.datetime.now(tz=dt.timezone.utc).astimezone().date().isoformat(), help="CHANGELOG use'stranslated，defaulttranslated")
    args = ap.parse_args(argv)

    versions = current_versions()
    if args.check or not args.version:
        distinct = set(versions.values())
        for k, v in versions.items():
            print(f"{k:20s} {v}")
        if len(distinct) != 1:
            print("versiontranslatedonetranslated", file=sys.stderr)
            return 1
        print(f"onetranslated：{distinct.pop()}")
        return 0

    new = args.version.lstrip("v")
    if not SEMVER.match(new):
        raise SystemExit(f"versiontranslatedIs X.Y.Z：{args.version}")

    set_version(new)
    roll_changelog(new, args.date)
    print(f"translated  {', '.join(versions)} translated {new}，CHANGELOG translated [{new}] - {args.date}")

    if args.commit:
        files = [str(p.relative_to(ROOT)) for p in (TAURI_CONF, CARGO_TOML, PYPROJECT, DESKTOP_CONFIG, CHANGELOG)]
        subprocess.run(["git", "add", *files], cwd=ROOT, check=True)
        subprocess.run(["git", "commit", "-m", f"chore: release v{new}"], cwd=ROOT, check=True)
        print(f"translated。translatedonetranslated：git tag v{new} && git push origin main v{new}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
