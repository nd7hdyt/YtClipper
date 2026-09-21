#!/usr/bin/env bash
# ENAutoEN autoclip_intro EN（EN）。
#
#   bash scripts/website/install.sh ../autoclip_intro
#
# EN autoclip_intro EN `git add -A && git commit -m "build: sync release info automatically" && git push`。
# EN repository_dispatch EN .github/workflows/desktop-build.yml EN "Notify website" EN，
# NeedEN Settings → Secrets EN WEBSITE_DISPATCH_TOKEN（fine-grained PAT：EN autoclip_intro，Contents: Read and write）。
# EN：EN workflow EN cron EN，EN。
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-}"
if [[ -z "$TARGET" || ! -f "$TARGET/index.html" ]]; then
  echo "EN: bash scripts/website/install.sh <autoclip_intro EN>（EN index.html）" >&2
  exit 1
fi

mkdir -p "$TARGET/scripts" "$TARGET/.github/workflows"
cp "$HERE/sync_release.py" "$TARGET/scripts/sync_release.py"
cp "$HERE/sync-release.yml" "$TARGET/.github/workflows/sync-release.yml"
chmod +x "$TARGET/scripts/sync_release.py"
grep -q '__pycache__' "$TARGET/.gitignore" 2>/dev/null || echo '__pycache__/' >> "$TARGET/.gitignore"

echo "EN $TARGET："
echo "  scripts/sync_release.py"
echo "  .github/workflows/sync-release.yml"
echo
echo "EN Release："
(cd "$TARGET" && python3 scripts/sync_release.py)
echo
echo "EN：cd $TARGET && git add -A && git commit -m 'build: sync release info automatically' && git push"
