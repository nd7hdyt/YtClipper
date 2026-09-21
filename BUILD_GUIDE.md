# 🚀 AutoClip Desktop EN

EN**EN**EN：python-build-standalone（PBS）。EN Python EN、
EN、EN ffmpeg/ffprobe EN `.app`，EN**EN Python EN ffmpeg**。

> EN PyInstaller / prepare_resources EN（EN 6+ EN CI EN）EN，EN。

## EN（macOS Apple Silicon）

```bash
./scripts/build_macos_arm.sh
```

EN：
```
src-tauri/target/release/bundle/macos/
├── AutoClip Desktop.app                    # EN（~550M）
└── AutoClip Desktop_1.0.0_aarch64.dmg      # DMG EN（~260M）
```

EN [`scripts/README.md`](scripts/README.md)。

### EN

| EN | EN | EN |
|------|------|------|
| Node.js | 18+ | EN |
| Rust | stable | EN `aarch64-apple-darwin` target |
| cargo-tauri | 2.x | `cargo install tauri-cli` |

EN **EN** EN Python / ffmpeg —— EN（EN `build/`）。

## CI / EN（GitHub Actions）

`.github/workflows/desktop-build.yml` EN `build_macos_arm.sh`：

```bash
# EN：EN → Actions → "Desktop Build (macOS arm64)" → Run workflow

# EN tag EN，EN DMG EN GitHub Release：
git tag v1.0.0
git push origin v1.0.0
```

## EN

DMG EN ad-hoc EN（EN Apple EN），EN：

1. EN DMG，EN `AutoClip Desktop` EN Applications
2. **EN → EN「EN」** EN Gatekeeper
3. EN `~/Library/Application Support/AutoClip` EN

## Troubleshooting

EN app EN：
```bash
'/Applications/AutoClip Desktop.app/Contents/MacOS/autoclip-desktop'
```
EN `Backend started on port: XXXXX` EN `Application startup complete`。

| EN | EN |
|------|------|
| `ModuleNotFoundError: No module named 'X'` | EN `X` EN `requirements.txt` EN（EN，EN）|
| EN | EN，EN WebView EN；EN/EN |
| EN | EN `Contents/Resources/resources/ffmpeg/{ffmpeg,ffprobe}` EN |
| EN | `rm -rf src-tauri/target build/pbs-cache build/ffmpeg-cache` EN（EN）|

## EN

- EN Apple Silicon (arm64)，EN Intel / Windows / Linux EN
- ad-hoc EN、EN，EN
