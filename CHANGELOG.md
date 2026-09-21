# changelog

docsAutoClipproject。

formatbased on [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
projectfollow [version](https://semver.org/lang/zh-CN/)。

## []

_（）_

## [1.3.0] - 2026-09-20

### added
- **`autoclip` **：`autoclip run video.mp4 --provider ollama` ，`list / show / providers / doctor` ，`--json`  agent；data directory SQLite（`pip install -e .`；`docs/CLI_AND_MCP.md`）
- **MCP server**（`autoclip mcp`，stdio）：`clip_video`、`start_clip_job` / `get_job_status`、`get_project`、`list_projects`、`list_providers`、`check_environment`，Cursor / Claude call；Agent skill `skills/autoclip/SKILL.md`
- **localmodel Ollama / LM Studio**：Settings pageprovideroptional，servicemodel，no need API Key；Docker / CLI available `LLM_PROVIDER=ollama`
- `GET /settings/local-presets`、`GET /settings/compatible-models?base_url=`；`POST /settings/test-api`  `ollama` / `lmstudio`
- ****：（//） 90 ；subtitles；、 top-K。 `python -m backend.eval`
- **export**：clip//Shorts 9:16  B （subtitles + ）。：「export」、`autoclip export`、MCP `export_clip`
- **Docker / localavailableSettings page**：`GET/PUT /settings`、`/test-api`、`/current-provider`、`/compatible-models` config；Web Settings page LLM providerkeydata directory `settings.json`，api  worker 。 `.env`  `LLM_PROVIDER` / `API_MODEL_NAME`（#100）
- **failedfailed**：LLM config / subtitles / outlinefailed /  /  / ffmpeg clip——
   `failed`，stage（SUBTITLE / ANALYZE / EXPORT）（settings、）。 `Completed · 0 clip`
   `processing`。`ProjectResponse` added `error_message`（failed，CLI  `project_metadata.last_error`）， / project / （#100 #11 #24）
- LLM failed（），failed
- **Qwen**（#45）：Settings pageQwenadded「 / 」，alibabacloud.com  Key ；Docker  `DASHSCOPE_BASE_URL`。 OpenAI ，， SDK 
- **Settings page「」**： API memory，（worker / local） 0.7；now step3  settings.json ，CLI `--min-score` 。`chunk_size` / `max_clips`  settings，stepintegrate
- tool：`scripts/bump_version.py`（version + CHANGELOG ，`--check` validate）、`scripts/release_notes.py`（Release  CHANGELOG generate）；`RELEASE_CHECKLIST.md` 

### fix
- DashScope provider API Key  INFO 
- **localproject**：`/projects/upload` startimport `db`，`NameError` ，project pending 「」（ 2026-05 `593cc62b` ）
- ** SQLite **：file SQLite  `StaticPool`（），import ROLLBACK  Task （`ObjectDeletedError`、、progress）。default + WAL，`StaticPool`  `:memory:`
-  Celery  `self.update_state()`  Redis backend（ ConnectionRefused import）
- **「」provider / model**（#100）：Chrome / Edge  `<font>`，React update `removeChild NotFoundError`。now `removeChild` / `insertBefore` ，；error
- error `DESIGN.md` （ AntD `Result`， + `Btn` ），「return」 HashRouter 
- macOS proxy（Clash ）local Ollama / LM Studio proxy 502： localhost / proxyenv var
- Settings pagemodel（`apiConfig.notifyListeners`  listener ）
- localcloudprovidermodel `qwen2.5:7b` localmodel

## [1.2.1] - 2026-09-06

> ： README recommend `docker compose` local（issue #88  issue）。

### added
- **OpenAI API `base_url`**：Settings page OpenAI provideradded「API」， / DeepSeek / OpenRouter / local Ollama、vLLM、LM Studio ；service key（#72 #57， #78）
- **Windows x64 install**（version，NSIS，install）：`scripts/build_windows_x64.sh` + `desktop-build.yml` Windows job； macOS  `scripts/lib/desktop_build_common.sh`（#73）
- Docker / availableenv varconfig LLM：`LLM_PROVIDER`、`API_MODEL_NAME`、`OPENAI_BASE_URL`、`API_{DASHSCOPE,OPENAI,GEMINI,SILICONFLOW}_API_KEY`；compose  api  worker，CI docker-smoke 
- `requirements.txt` dependenciesversion（ CI / Docker ；3.11  3.13 ）

### fix
- **Settings pageselect LLM provider**：`api_provider` / `api_base_url` now `settings.json` ；`/settings/current-provider` returnQwen；settings API  Celery worker file mtime ，
- model selection（`mode="tags"`）backendfailed，
- Docker build：`.dockerignore`  `docker-entrypoint.sh` / `docker-dev-entrypoint.sh`（#1 #4 #9 #47 #50 #88）
- Windows start：added `.gitattributes`，shell  LF （#73 #88）
- Docker ：compose / dev compose  Celery worker  `-Q`，default；now `celery,processing,video,notification,upload`。local `start_autoclip.sh`  `celery`  `video` （#88）
- Docker projectfailed：`task_submission_utils`  `redis.Redis(host='localhost')`  `try` ； `REDIS_URL` failed warning（#88）
- YouTube  500：`youtube.py`  `/Users/zhoukk/...` yt-dlp  `cwd`  `sys.executable -m yt_dlp` + data directory； `fix_project_thumbnails.py` Settings page（#88）
- LLM step list  JSON （`_build_full_input`）（#53）
-  5 subtitles YouTube 429：default `zh-Hans,zh,en`，available `AUTOCLIP_YT_SUBTITLE_LANGS` （#88）

### improve
- Docker  `python:3.9-slim` → `python:3.11-slim`（ yt-dlp support 3.9， 3.9  360p）
- `docker-compose.yml` service `autoclip:local` ，build
- CI added `docker-smoke` job：build、 redis + api + worker、validatecheck、yt-dlp available、REDIS_URL 、worker route
- startbackend `AUTOCLIP_APP_VERSION`，backend `/settings` return `1.0.0`
- settingsdata directory `AUTOCLIP_APP_DIR`（macOS ；Windows  `%APPDATA%\AutoClip`），Windows  `PYTHONUTF8=1` 
- `src-tauri/Cargo.toml` version `tauri.conf.json` 
- `desktop-build.yml`  macOS + Windows build，`release` job ，failed

### 
-  `backend/api/v1/youtube_improved.py`

## [1.2.0] - 2026-06-03

> integrate,account / business。

### added
- integrate PostHog ：install/start/update、import、export、failed、settings API key event，eventversion//
- Settings pageadded「」，use（，）
- addeddocs `docs/ANALYTICS.md` English `docs/PRIVACY.md` / `docs/PRIVACY.en.md`

### （1.0.0 、）
- edit、Baccountaccountstatusmonitor、、、Docker 

## [1.1.0] - 2026-05-31

>  macOS 、available、。

### added
- 🖥️ dependenciesinstall： Python  +  ffmpeg/ffprobe，no need Python/ffmpeg
- 🗣️ localsubtitles（install）：subtitles「settings → 」install faster-whisper model

### fix
- fixstart（frontend vendor chunk  React ）
- fixproject「」（ pytz dependenciesAPI 500）
- fiximport/「failed / 」
- fix 0%「」（local，dependencies Redis）
- fix（ ffmpeg versionintegratebackend）

### improve
- AI provider Gemini  `google-genai` SDK
- CI buildverify（python-build-standalone）
- ：docs，project

## [1.0.0] - 2024-01-15

### added
- 🎬 supportYouTubedownload
- 🎬 supportBdownload
- 🎬 supportlocalfile upload
- 🤖 AI
- ✂️ clip
- 📚 generate
- 🎨 Web
- 🚀 
- 📊 progressmonitor
- 🔐 Bsite account
- 📱 responsive design
- 🛠️ start

### 
- FastAPIbackend
- React + TypeScriptfrontend
- Celery
- Redisproxy
- SQLitedatabase
- WebSocket
- QwenAIintegration

## [0.9.0] - 2024-01-01

### added
- project
- APIAPI
- frontend
- 
- AIservice

### 
- Python 3.8+
- React 18
- FastAPI
- Celery
- Redis
- SQLite

---

## versionnotes

### versionformat

useversion (SemVer)：

- **version**: API
- **version**: added
- ****: issue

### 

- **added**: 
- **improve**: improve
- **fix**: Bugfix
- ****: 
- **security**: securityfix

### 

- [Unreleased]: https://github.com/zhouxiaoka/autoclip/compare/v1.3.0...HEAD
- [1.3.0]: https://github.com/zhouxiaoka/autoclip/compare/v1.2.1...v1.3.0
- [1.2.1]: https://github.com/zhouxiaoka/autoclip/compare/v1.2.0...v1.2.1
- [1.2.0]: https://github.com/zhouxiaoka/autoclip/releases/tag/v1.2.0
- [1.1.0]: https://github.com/zhouxiaoka/autoclip/releases/tag/v1.1.0
- [1.0.0]: https://github.com/zhouxiaoka/autoclip/releases/tag/v1.0.0
