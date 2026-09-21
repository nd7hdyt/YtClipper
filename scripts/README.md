# scripts/

ENScript。EN**EN**EN（python-build-standalone，EN PBS），
EN PyInstaller / prepare_resources ENScriptEN。

## ScriptEN

| Script | EN |
|------|------|
| `build_macos_arm.sh` | EN（macOS Apple Silicon）。EN `.app` + `.dmg`。 |
| `build_windows_x64.sh` | EN（Windows x64）。EN Git Bash EN，EN NSIS InstallEN `*-setup.exe`。 |
| `lib/desktop_build_common.sh` | ENScriptEN（EN Python Download、pip、EN、DependenciesCheck、EN）。EN。 |
| `verify_desktop.sh` | ENTest：`cargo check` + EN，EN `/health` EN `/api/v1/video-categories`。EN `nightly-desktop-smoke.yml` EN。 |
| `monitor_whisper.py` | EN Whisper EN，EN `start_autoclip.sh` / `check_whisper_status.sh` EN。 |

## EN

### macOS arm64

```bash
./scripts/build_macos_arm.sh
```

EN：
```
src-tauri/target/release/bundle/macos/
├── AutoClip Desktop.app
└── AutoClip Desktop_<version>_aarch64.dmg
```

### Windows x64

EN **Git Bash** EN（Need Node.js、Rust MSVC ToolEN、Visual Studio Build Tools C++ EN、cargo-tauri）：

```bash
bash scripts/build_windows_x64.sh
```

EN：
```
src-tauri/target/release/bundle/nsis/
└── AutoClip Desktop_<version>_x64-setup.exe
```

Windows EN macOS EN：macOS EN `python/ backend/ ffmpeg/` EN `.app`
EN；Windows ENInstallEN，EN `src-tauri/tauri.windows.conf.json`
EN `bundle.resources` EN，EN Tauri EN NSIS。EN Windows EN
Tauri EN，EN macOS。

### ENScriptEN（`lib/desktop_build_common.sh`）

1. DownloadEN Python EN（python-build-standalone，EN `build/pbs-cache/`；EN，AutoEN）
2. EN Python Install `requirements.txt` ENDependencies
3. EN `src-tauri/resources/backend/`（EN / tests / EN；EN Python `shutil` EN，Windows EN rsync）
4. **DependenciesENCheck**：AST ENAllEN import，ENFailed
   （EN"EN、EN 500"）
5. EN（`npm ci && npm run build`）

ENScriptEN：EN ffmpeg/ffprobe（macOS: osxexperts arm64 EN；Windows: BtbN win64 gpl EN）、
`cargo tauri build`、EN。

### EN（`src-tauri/src/backend_manager.rs`）

- Python：`resources/python/bin/python3`（unix）EN `resources/python/python.exe`（Windows）
- ffmpeg：`resources/ffmpeg/ffmpeg[.exe]`，EN `AUTOCLIP_FFMPEG_PATH` / `AUTOCLIP_FFPROBE_PATH` EN
- EN：Rust EN `AUTOCLIP_APP_DIR=<EN>/AutoClip`
  （macOS `~/Library/Application Support/AutoClip`，Windows `%APPDATA%\AutoClip`）
- Windows EN：`PYTHONUTF8=1`（EN stdout EN emoji，Else GBK EN UnicodeEncodeError）、
  `CREATE_NO_WINDOW`（EN）

### ENDependencies

- Node.js 18+、Rust、cargo-tauri (`cargo install tauri-cli`)
- macOS：`aarch64-apple-darwin` target；Windows：MSVC ToolEN + VS Build Tools
- System **ENNeed** EN Python / ffmpeg —— ScriptEN

### EnvironmentEN

- `PIP_INDEX_URL`：pip EN，EN；CI EN `https://pypi.org/simple`
- `PBS_VERSION` / `PBS_PYTHON_VERSION`：EN Python Version（EN `lib/desktop_build_common.sh`）

## CI

`.github/workflows/desktop-build.yml`：
- `workflow_dispatch`：EN macOS EN Windows
- `v*` tag：EN，`release` job EN GitHub Release（ENFailedENUpload）

## EN（EN）

EN Tauri EN，EN：
```bash
cd src-tauri && cargo tauri dev
```
（EN :3000 + EN，EN `backend_manager.rs` EN）
