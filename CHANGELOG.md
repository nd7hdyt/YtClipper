# EN

ENAutoClipEN。

ENBased on [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
EN [EN](https://semver.org/lang/zh-CN/)。

## [EN]

_（EN）_

## [1.3.0] - 2026-09-20

### EN
- **`autoclip` EN**：`autoclip run video.mp4 --provider ollama` One command to produce clips，`list / show / providers / doctor` EN，`--json` EN agent；EN SQLite（`pip install -e .`；`docs/CLI_AND_MCP.md`）
- **MCP server**（`autoclip mcp`，stdio）：`clip_video`、`start_clip_job` / `get_job_status`、`get_project`、`list_projects`、`list_providers`、`check_environment`，Cursor / Claude Can be called directly；Agent skill `skills/autoclip/SKILL.md`
- **EN Ollama / LM Studio**：ENProvidesEN，EN，EN API Key；Docker / CLI EN `LLM_PROVIDER=ollama`
- `GET /settings/local-presets`、`GET /settings/compatible-models?base_url=`；`POST /settings/test-api` EN `ollama` / `lmstudio`
- **EN**：EN（EN/EN/EN）EN 90 EN；EN；EN、EN top-K。EN `python -m backend.eval`
- **EN**：EN/EN/Shorts 9:16 EN B EN（EN + EN）。EN：EN「EN」、`autoclip export`、MCP `export_clip`
- **Docker / EN**：`GET/PUT /settings`、`/test-api`、`/current-provider`、`/compatible-models` EN；Web EN LLM ProvidesEN `settings.json`，api EN worker EN。EN `.env` EN `LLM_PROVIDER` / `API_MODEL_NAME`（#100）
- **EN**：LLM EN / EN / EN / EN / EN / ffmpeg EN——
  EN `failed`，EN（SUBTITLE / ANALYZE / EXPORT）EN（EN、EN）。EN `Completed · 0 EN`
  EN `processing`。`ProjectResponse` EN `error_message`（EN，CLI EN `project_metadata.last_error`），EN / EN / EN（#100 #11 #24）
- LLM EN（EN），EN
- **EN**（#45）：EN「EN / EN」EN，alibabacloud.com EN Key EN；Docker EN `DASHSCOPE_BASE_URL`。EN OpenAI EN，EN，EN SDK EN
- **EN「EN」EN**：EN API EN，EN（worker / EN）EN 0.7；EN step3 EN settings.json EN，CLI `--min-score` EN。`chunk_size` / `max_clips` EN settings，EN
- EN：`scripts/bump_version.py`（EN + CHANGELOG EN，`--check` EN）、`scripts/release_notes.py`（Release EN CHANGELOG EN）；`RELEASE_CHECKLIST.md` EN

### EN
- DashScope ProvidesEN API Key EN INFO EN
- **ENUploadEN**：`/projects/upload` EN `db`，`NameError` EN，EN pending EN「EN」（EN 2026-05 `593cc62b` EN）
- **EN SQLite EN**：EN SQLite EN `StaticPool`（EN），EN ROLLBACK EN Task EN（`ObjectDeletedError`、EN、EN）。EN + WAL，`StaticPool` EN `:memory:`
- EN Celery EN `self.update_state()` EN Redis EN（EN ConnectionRefused EN）
- **EN「EN」ENProvidesEN / EN**（#100）：Chrome / Edge EN `<font>`，React EN `removeChild NotFoundError`。EN `removeChild` / `insertBefore` EN，EN；EN
- EN `DESIGN.md` EN（ENPurple GradientEN AntD `Result`，EN + `Btn` EN），「EN」EN HashRouter EN
- macOS EN（Clash EN）EN Ollama / LM Studio EN 502：EN localhost / EN
- EN（`apiConfig.notifyListeners` EN listener EN）
- ENProvidesEN `qwen2.5:7b` EN

## [1.2.1] - 2026-09-06

> EN：EN README EN `docker compose` EN（issue #88 EN issue）。

### EN
- **OpenAI EN `base_url`**：EN OpenAI ProvidesEN「EN」，EN / DeepSeek / OpenRouter / EN Ollama、vLLM、LM Studio EN；EN key（#72 #57，EN #78）
- **Windows x64 EN**（EN，NSIS，EN）：`scripts/build_windows_x64.sh` + `desktop-build.yml` Windows job；EN macOS EN `scripts/lib/desktop_build_common.sh`（#73）
- Docker / EN LLM：`LLM_PROVIDER`、`API_MODEL_NAME`、`OPENAI_BASE_URL`、`API_{DASHSCOPE,OPENAI,GEMINI,SILICONFLOW}_API_KEY`；compose EN api EN worker，CI docker-smoke EN
- `requirements.txt` EN（EN CI / Docker EN；3.11 EN 3.13 EN）

### EN
- **EN LLM ProvidesEN**：`api_provider` / `api_base_url` EN `settings.json` EN；`/settings/current-provider` EN；EN API EN Celery worker EN mtime EN，EN
- EN（`mode="tags"`）EN，EN
- Docker EN：`.dockerignore` EN `docker-entrypoint.sh` / `docker-dev-entrypoint.sh`（#1 #4 #9 #47 #50 #88）
- Windows EN：EN `.gitattributes`，shell EN LF EN（#73 #88）
- Docker EN：compose / dev compose EN Celery worker EN `-Q`，EN；EN `celery,processing,video,notification,upload`。EN `start_autoclip.sh` EN `celery` EN `video` EN（#88）
- Docker EN：`task_submission_utils` EN `redis.Redis(host='localhost')` EN `try` EN；EN `REDIS_URL` EN warning（#88）
- YouTube EN 500：`youtube.py` EN `/Users/zhoukk/...` yt-dlp EN `cwd` EN `sys.executable -m yt_dlp` + EN；EN `fix_project_thumbnails.py` EN（#88）
- LLM EN list EN JSON EN（`_build_full_input`）（#53）
- EN 5 ENLanguageEN YouTube 429：EN `zh-Hans,zh,en`，EN `AUTOCLIP_YT_SUBTITLE_LANGS` EN（#88）

### EN
- Docker EN `python:3.9-slim` → `python:3.11-slim`（EN yt-dlp ENSupport 3.9，EN 3.9 EN 360p）
- `docker-compose.yml` EN `autoclip:local` EN，EN
- CI EN `docker-smoke` job：EN、EN redis + api + worker、ENHealth Check、yt-dlp EN、REDIS_URL EN、worker EN
- EN `AUTOCLIP_APP_VERSION`，EN `/settings` EN `1.0.0`
- EN `AUTOCLIP_APP_DIR`（macOS EN；Windows EN `%APPDATA%\AutoClip`），Windows EN `PYTHONUTF8=1` EN
- `src-tauri/Cargo.toml` EN `tauri.conf.json` EN
- `desktop-build.yml` EN macOS + Windows EN，`release` job EN，ENUpload

### EN
- EN `backend/api/v1/youtube_improved.py`

## [1.2.0] - 2026-06-03

> EN,ENAccount / EN。

### EN
- EN PostHog EN：EN/EN/EN、EN、EN、EN、EN API key EN，EN/EN/EN
- EN「EN」EN，EN（EN，EN）
- ENAnalyticsEN `docs/ANALYTICS.md` ENEnglishEN `docs/PRIVACY.md` / `docs/PRIVACY.en.md`

### EN（1.0.0 EN、EN）
- EN、BENMulti-Account ManagementENAccountEN、EN、EN、Docker EN

## [1.1.0] - 2026-05-31

> EN macOS EN、EN、EN。

### EN
- 🖥️ EN：Built-inEN Python EN + EN ffmpeg/ffprobe，EN Python/ffmpeg
- 🗣️ EN（EN）：EN「EN → EN」EN faster-whisper EN

### EN
- EN（EN vendor chunk EN React EN）
- EN「EN」（EN pytz EN 500）
- EN/EN「EN / EN」EN
- EN 0%「EN」（EN，EN Redis）
- EN（Built-in ffmpeg EN）

### EN
- AI ProvidesEN Gemini EN `google-genai` SDK
- CI EN（python-build-standalone）
- EN：EN，ENProject Structure

## [1.0.0] - 2024-01-15

### EN
- 🎬 SupportYouTubeEN
- 🎬 SupportBEN
- 🎬 SupportLocal File Upload
- 🤖 AIEN
- ✂️ EN
- 📚 Smart CollectionsEN
- 🎨 ENWebInterface
- 🚀 EN
- 📊 EN
- 🔐 BENAccount Management
- 📱 Responsive Design
- 🛠️ One-Click Start Script

### EN
- FastAPIEN
- React + TypeScriptEN
- CeleryENTask Queue
- RedisEN
- SQLiteEN
- WebSocketENCommunication
- ENAIEN

## [0.9.0] - 2024-01-01

### EN
- EN
- ENAPIEN
- ENInterface
- EN
- AIEN

### Tech Stack
- Python 3.8+
- React 18
- FastAPI
- Celery
- Redis
- SQLite

---

## EN

### EN

EN (SemVer)：

- **EN**: ENAPIEN
- **EN**: EN
- **EN**: EN

### EN

- **EN**: EN
- **EN**: EN
- **EN**: BugEN
- **EN**: EN
- **EN**: EN

### EN

- [Unreleased]: https://github.com/nd7hdyt/YtClipper/compare/v1.3.0...HEAD
- [1.3.0]: https://github.com/nd7hdyt/YtClipper/compare/v1.2.1...v1.3.0
- [1.2.1]: https://github.com/nd7hdyt/YtClipper/compare/v1.2.0...v1.2.1
- [1.2.0]: https://github.com/nd7hdyt/YtClipper/releases/tag/v1.2.0
- [1.1.0]: https://github.com/nd7hdyt/YtClipper/releases/tag/v1.1.0
- [1.0.0]: https://github.com/nd7hdyt/YtClipper/releases/tag/v1.0.0
