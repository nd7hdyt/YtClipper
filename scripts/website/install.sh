#!/usr/bin/env bash
#  translatedthistranslated autoclip_intro translated（onetranslated）。
#
#   bash scripts/website/install.sh ../autoclip_intro
#
# translatedin autoclip_intro translated `git add -A && git commit -m "build: sync release info automatically" && git push`。
# translatedthistranslated's repository_dispatch translated .github/workflows/desktop-build.yml 's "Notify website" step，
# translatedintranslated Settings → Secrets translated WEBSITE_DISPATCH_TOKtranslated（fine-grained PAT：translated autoclip_intro，Contents: Read and write）。
# translated：translated workflow translatedpertranslated cron translated，translatedIstranslatedmultionetranslated。
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-}"
if [[ -z "$TARGET" || ! -f "$TARGET/index.html" ]]; then
  echo "usetranslated: bash scripts/website/install.sh <autoclip_intro translatedpath>（translateddirectorytranslated index.html）" >&2
  exit 1
fi

mkdir -p "$TARGET/scripts" "$TARGET/.github/workflows"
cp "$HERE/sync_release.py" "$TARGET/scripts/sync_release.py"
cp "$HERE/sync-release.yml" "$TARGET/.github/workflows/sync-release.yml"
chmod +x "$TARGET/scripts/sync_release.py"
grep -q '__pycache__' "$TARGET/.gitignore" 2>/dev/null || echo '__pycache__/' >> "$TARGET/.gitignore"

echo "translated $TARGET："
echo "  scripts/sync_release.py"
echo "  .github/workflows/sync-release.yml"
echo
echo "translatedintranslatedonetranslated Release："
(cd "$TARGET" && python3 scripts/sync_release.py)
echo
echo "translatedonetranslated：cd $TARGET && git add -A && git commit -m 'build: sync release info automatically' && git push"
