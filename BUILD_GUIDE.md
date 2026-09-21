# 🚀 AutoClip Desktop 

Desktop client has only****Package：python-build-standalone（PBS）。It bundles portable Python Runtime、
Backend source、Static ffmpeg/ffprobe all packaged into `.app`，User machine**No need to pre-install Python  ffmpeg**。

> Historical PyInstaller / prepare_resources （And corresponding 6+   CI Workflow）Never produced a usable package and has been removed。

## Local Build（macOS Apple Silicon）

```bash
./scripts/build_macos_arm.sh
```

Artifacts：
```
src-tauri/target/release/bundle/macos/
├── AutoClip Desktop.app                    # Package（~550M）
└── AutoClip Desktop_1.0.0_aarch64.dmg      # DMG InstallationPackage（~260M）
```

See script steps in [`scripts/README.md`](scripts/README.md)。

### Prerequisites

|  |  |  |
|------|------|------|
| Node.js | 18+ |  |
| Rust | stable |  `aarch64-apple-darwin` target |
| cargo-tauri | 2.x | `cargo install tauri-cli` |

System **No need** Pre-install Python / ffmpeg —— Script comes with portable version（First build will download and cache to `build/`）。

## CI / Release（GitHub Actions）

`.github/workflows/desktop-build.yml` Run the same `build_macos_arm.sh`：

```bash
# Manual trigger：Repo page → Actions → "Desktop Build (macOS arm64)" → Run workflow

# Or tag tag trigger and automatically attach DMG To GitHub Release：
git tag v1.0.0
git push origin v1.0.0
```

## Installation & First Run

DMG Is ad-hoc Signature（Not done Apple Notarization），So：

1. Double-click DMG，  `AutoClip Desktop` Drag to Applications
2. **First launch: right-click the app → Select「Open」** To bypass Gatekeeper
3. Backend will auto-start at `~/Library/Application Support/AutoClip` Create data directory

## Troubleshooting

 app Backend：
```bash
'/Applications/AutoClip Desktop.app/Contents/MacOS/autoclip-desktop'
```
Should see `Backend started on port: XXXXX`  `Application startup complete`。

| Symptom | Troubleshoot |
|------|------|
| `ModuleNotFoundError: No module named 'X'` |   `X` Add to `requirements.txt` Rebuild（Build-time dependency check should have caught it; normally won't happen）|
| Black screen | Frontend not mounted, check WebView Console；Usually packaging/Resource issue |
| Video processing failed | Confirm `Contents/Resources/resources/ffmpeg/{ffmpeg,ffprobe}` Exists and is executable |
| To retry a failed build | `rm -rf src-tauri/target build/pbs-cache build/ffmpeg-cache` Then rerun（Will re-download）|

## Known Limitations

- Only Apple Silicon (arm64)，Not yet Intel / Windows / Linux Package
- ad-hoc Signature、Notarization，FirstRight-clickOpen
