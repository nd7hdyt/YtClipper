# official site（autoclip_intro）auto-update

official site GitHub Pages file `index.html`，version、download、install（）。
；now：

```
git tag vX.Y.0 ─▶ desktop-build.yml ─▶ Release 
                        │
                        └─▶ repository_dispatch(autoclip-release, {tag}) ─▶ autoclip_intro/sync-release.yml
                                                                               │  python scripts/sync_release.py vX.Y.0
                                                                               │  （ GitHub Release API， index.html）
                                                                               └▶  main ─▶ Pages  1 minutes
```

：official site workflow  03:17 UTC  latest release， token，official site。

## install（official site）

 token official site，file，：

```bash
bash scripts/website/install.sh ../autoclip_intro
cd ../autoclip_intro && git add -A && git commit -m "build: sync release info automatically" && git push
```

## （optional）

1. GitHub → Settings → Developer settings → Fine-grained tokens → ：Repository access  `autoclip_intro`，Permissions → Contents: **Read and write**。
2.  `autoclip` → Settings → Secrets and variables → Actions →  `WEBSITE_DISPATCH_TOKEN`。
3.  `desktop-build.yml`  `release` job succeeded `autoclip-release` event； token step，impact。

## file

| file |  |  |
|---|---|---|
| `sync_release.py` | `autoclip_intro/scripts/` |  Release →  `index.html`（`--check` ） |
| `sync-release.yml` | `autoclip_intro/.github/workflows/` | （dispatch / cron / ）→  →  |
| `install.sh` |  | file |

：`.github/workflows/desktop-build.yml` → `release` job → "Notify website" step。
