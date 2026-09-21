# scripts/

build。****（python-build-standalone， PBS），
 PyInstaller / prepare_resources 。

## 

|  |  |
|------|------|
| `build_macos_arm.sh` | （macOS Apple Silicon）。 `.app` + `.dmg`。 |
| `build_windows_x64.sh` | （Windows x64）。 Git Bash ， NSIS install `*-setup.exe`。 |
| `lib/desktop_build_common.sh` | step（ Python download、pip、backend、dependenciescheck、frontendbuild）。。 |
| `verify_desktop.sh` | backendtest：`cargo check` + backend，validate `/health`  `/api/v1/video-categories`。 `nightly-desktop-smoke.yml` call。 |
| `monitor_whisper.py` |  Whisper monitor， `start_autoclip.sh` / `check_whisper_status.sh` call。 |

## 

### macOS arm64

```bash
./scripts/build_macos_arm.sh
```

：
```
src-tauri/target/release/bundle/macos/
├── AutoClip Desktop.app
└── AutoClip Desktop_<version>_aarch64.dmg
```

### Windows x64

 **Git Bash** （need Node.js、Rust MSVC tool、Visual Studio Build Tools C++ 、cargo-tauri）：

```bash
bash scripts/build_windows_x64.sh
```

：
```
src-tauri/target/release/bundle/nsis/
└── AutoClip Desktop_<version>_x64-setup.exe
```

Windows  macOS ：macOS build `python/ backend/ ffmpeg/`  `.app`
；Windows install， `src-tauri/tauri.windows.conf.json`
 `bundle.resources` ， Tauri  NSIS。file Windows build
Tauri ，impact macOS。

### （`lib/desktop_build_common.sh`）

1. download Python （python-build-standalone，cache `build/pbs-cache/`；，）
2.  Python install `requirements.txt` dependencies
3. backend `src-tauri/resources/backend/`（cache / tests / ； Python `shutil` ，Windows  rsync）
4. **dependenciescheck**：AST backend import，buildfailed
   （"、 500"）
5. buildfrontend（`npm ci && npm run build`）

： ffmpeg/ffprobe（macOS: osxexperts arm64 ；Windows: BtbN win64 gpl ）、
`cargo tauri build`、。

### （`src-tauri/src/backend_manager.rs`）

- Python：`resources/python/bin/python3`（unix） `resources/python/python.exe`（Windows）
- ffmpeg：`resources/ffmpeg/ffmpeg[.exe]`， `AUTOCLIP_FFMPEG_PATH` / `AUTOCLIP_FFPROBE_PATH` backend
- data directory：Rust settings `AUTOCLIP_APP_DIR=<data directory>/AutoClip`
  （macOS `~/Library/Application Support/AutoClip`，Windows `%APPDATA%\AutoClip`）
- Windows ：`PYTHONUTF8=1`（backend stdout  emoji， GBK  UnicodeEncodeError）、
  `CREATE_NO_WINDOW`（）

### dependencies

- Node.js 18+、Rust、cargo-tauri (`cargo install tauri-cli`)
- macOS：`aarch64-apple-darwin` target；Windows：MSVC tool + VS Build Tools
-  **need**  Python / ffmpeg —— 

### env var

- `PIP_INDEX_URL`：pip ，default；CI  `https://pypi.org/simple`
- `PBS_VERSION` / `PBS_PYTHON_VERSION`： Python version（default `lib/desktop_build_common.sh`）

## CI

`.github/workflows/desktop-build.yml`：
- `workflow_dispatch`：build macOS build Windows
- `v*` tag：build，`release` job  GitHub Release（failed）

## dev mode（）

 Tauri dev mode，：
```bash
cd src-tauri && cargo tauri dev
```
（frontend :3000 + backendport， `backend_manager.rs` ）
