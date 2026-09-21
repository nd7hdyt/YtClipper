# EN（autoclip_intro）ENAutoEN

EN GitHub Pages EN `index.html`，VersionEN、DownloadEN、InstallEN（EN）。
EN；EN：

```
git tag vX.Y.0 ─▶ desktop-build.yml ─▶ Release EN
                        │
                        └─▶ repository_dispatch(autoclip-release, {tag}) ─▶ autoclip_intro/sync-release.yml
                                                                               │  python scripts/sync_release.py vX.Y.0
                                                                               │  （EN GitHub Release API，EN index.html）
                                                                               └▶ EN main ─▶ Pages EN 1 EN
```

EN：EN workflow EN 03:17 UTC EN latest release，EN token，EN。

## ENInstall（EN）

EN token EN，EN，EN：

```bash
bash scripts/website/install.sh ../autoclip_intro
cd ../autoclip_intro && git add -A && git commit -m "build: sync release info automatically" && git push
```

## EN（EN）

1. GitHub → Settings → Developer settings → Fine-grained tokens → EN：Repository access EN `autoclip_intro`，Permissions → Contents: **Read and write**。
2. EN `autoclip` → Settings → Secrets and variables → Actions → EN `WEBSITE_DISPATCH_TOKEN`。
3. EN `desktop-build.yml` EN `release` job SuccessEN `autoclip-release` EN；EN token EN，EN。

## EN

| EN | EN | EN |
|---|---|---|
| `sync_release.py` | `autoclip_intro/scripts/` | EN Release → EN `index.html`（`--check` EN） |
| `sync-release.yml` | `autoclip_intro/.github/workflows/` | EN（dispatch / cron / Manual）→ ENScript → EN |
| `install.sh` | EN | EN |

EN：`.github/workflows/desktop-build.yml` → `release` job → "Notify website" EN。
