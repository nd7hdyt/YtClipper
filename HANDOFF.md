# AutoClip — EN / EN / EN

> EN：2026-09-20 · Based on `main@aaf863bb`（**v1.2.1 EN**：Release EN macOS arm64 DMG 223 MB + Windows x64 EN 145 MB；
> EN 2026-09-20 EN Windows 1136 / DMG 334 —— Windows EN）

AutoClip EN AI EN：EN BEN/YouTube EN，EN、
EN。EN；Long-term PlanEN `ROADMAP.md`。

---

## EN、EN

| EN | EN | EN |
|----|------|------|
| EN | FastAPI + Celery（EN）+ SQLite | `backend/` |
| EN | React + TypeScript + Ant Design + Vite | `frontend/` |
| EN | Tauri 2 + Rust | `src-tauri/` |
| LLM | OpenAI EN OpenAI EN（EN base_url）/ Gemini(google-genai) / EN(dashscope) / EN / EN Ollama、LM Studio | `backend/core/llm_providers.py`、`llm_manager.py`、`local_presets.py` |
| CLI / MCP | `autoclip` EN + MCP server（stdio），EN FastAPI / Celery EN | `backend/cli.py`、`mcp_server.py`、`services/local_runner.py` |

EN：**EN**（macOS arm64 DMG EN；Windows x64 EN v1.2.1 ENProvides，EN）、**Docker EN**（README EN）、
**EN**（`start_autoclip.sh`）、**CLI / MCP**（`pip install -e .`，EN agent，`docs/CLI_AND_MCP.md`）。

---

## EN、EN

### EN
- **v1.2.0（2026-06-03）**：EN DMG EN（Built-inEN Python + EN ffmpeg + EN faster-whisper），
  `desktop-build.yml` EN tag EN Release；v1.2.0 DMG EN 2000+ EN。
- **PostHog ENAnalytics** + EN + EN（`docs/ANALYTICS.md`、`docs/PRIVACY*.md`）。
- **Calm Premium VisualEN**EN（`DESIGN.md`）。
- Nightly EN（`nightly-desktop-smoke.yml`）EN。
- **Developer Mode（2026-09-07）**：
  - `autoclip run video.mp4 --provider ollama` One command to produce clips；`list / show / providers / doctor / mcp` EN；`--json` EN / agent。
    EN SQLite，CLI EN。
  - MCP server（`autoclip mcp`）7 EN：`clip_video`（EN + EN）、`start_clip_job` / `get_job_status`、`get_project`、`list_projects`、`list_providers`、`check_environment`；
    EN `mcp` 2.x stdio EN。Agent skill EN `skills/autoclip/SKILL.md`。
  - EN Ollama / LM Studio：EN、EN `/v1/models`、EN key；EN `local_presets.py` EN `openai` + `base_url`。
  - EN：`httpx` EN localhost EN（Clash）EN 502 → `is_local_url()` EN `trust_env=False`；
    `apiConfig.notifyListeners` EN listener EN `getCurrentProvider`。
  - EN `tests/test_local_presets.py`、`tests/test_cli.py`（EN 24 EN）；**EN `autoclip run`**（EN v1.3 todo）。
- **EN + EN（2026-09-07）**：EN `docs/QUALITY_AND_PUBLISH_PLAN.md`。
  - EN `DurationProfile`（EN/EN/EN）EN step1/2 EN，EN「EN 90 EN / EN 3–6 EN」。
  - `refine_timeline`：EN cue、EN、EN；`quality_report.json` EN。
  - EN：EN outline EN；EN top-K（#11 EN 0）。
  - EN adapter EN `prompt/<category>/`。`AUTOCLIP_LLM_CACHE_DIR` EN/EN。`python -m backend.eval` EN（`backend/eval/cases/short-synthetic` EN）。
  - EN：`publish_export.py`（9:16 blur/crop、EN、EN）；API `POST .../clips/{id}/export`；`autoclip export`；MCP `export_clip`；EN「EN」Dialog。EN 16:9 copy。
  - **EN 5 EN**；EN `original` EN。
- **#100 EN（2026-09-20）**：Docker Web EN + EN。EN：EN **Chrome「EN」** EN DOM（EN → `<font>`）
  EN React `removeChild NotFoundError`，EN Gemini EN；EN UI ENEnglishEN。EN：`utils/domTranslationGuard.ts` EN
  `removeChild` / `insertBefore`（facebook/react#11538 EN），`ErrorBoundary` EN `DESIGN.md` EN（ENPurple Gradient）。
  EN：`/settings` EN、`/test-api`、`/current-provider`、`/compatible-models` EN `check_desktop_mode()`，Docker / EN
  （settings.json EN `./data`，api / worker EN mtime EN；EN `.env`）。EN（EN / EN / EN / EN）EN。
  EN `tests/test_settings_web_mode.py`（6 EN）；Playwright EN：EN 4 EN，EN。

### v1.2.1（2026-09-06 EN tag）
EN：README EN `docker compose` EN 2025-09 EN
（issue #88 EN 7 EN，EN），EN issue EN"EN"EN。#89 EN：
1. `.dockerignore` EN `docker-entrypoint.sh` / `docker-dev-entrypoint.sh`（EN）
2. EN `.gitattributes`，shell EN LF（Windows EN）
3. EN `youtube.py` / `fix_project_thumbnails.py` / `SettingsPage.tsx` EN `/Users/zhoukk` EN
4. Docker EN 3.9 → 3.11（yt-dlp EN）
5. ENLanguageEN `zh-Hans,zh,en`，`AUTOCLIP_YT_SUBTITLE_LANGS` EN（EN 429）
6. `task_submission_utils` EN localhost EN Redis EN（Docker EN）
7. compose / dev compose / `start_autoclip.sh` EN worker EN `-Q celery,processing,video,notification,upload`
   （EN Docker EN）
8. `_build_full_input` list EN JSON EN（#53）
9. CI EN `docker-smoke` job EN；EN 1.2.1；EN `youtube_improved.py`

EN：
- **#90** EN 6 EN `NodeJS.Timeout` EN，`npm run typecheck` EN CI EN
- **#91** EN PR #85（EN utf-8）、#84（Gemini `-latest` EN）、#83（youtube.py EN）EN cherry-pick EN（EN；EN PR EN）
- **#94** `requirements.txt` EN
- **#92** OpenAI EN `base_url`（#72 #57，EN #78）。**EN：EN provider EN，EN dashscope**；
  LLMManager EN settings.json mtime EN，ENSupport Docker EN（`LLM_PROVIDER` / `OPENAI_BASE_URL` / `API_*_API_KEY`）
- **#93** Windows x64 EN + workflow。`workflow_dispatch` EN Windows EN `windows-latest` EN：
  EN 145 MB，EN ~22 min（`cargo install tauri-cli` EN 8 min + EN 13 min；rust-cache EN，EN）。
  **EN**（EN todo）

### EN（ROADMAP Phase 0）
| EN | EN |
|---|---|
| Apple Developer ID EN + EN | EN，`signingIdentity: null`，EN |
| EN（Windows / Intel mac / Linux） | Windows x64 EN runner EN（#93），EN v1.2.1 Release EN，**EN**；Intel mac / Linux EN |
| Sentry EN | EN |
| Tauri updater EN | EN |
| EN / EN | EN（#94）；PBS + ffmpeg EN actions/cache，Rust EN rust-cache |
| `ruff` EN CI EN `continue-on-error` | typecheck EN（#90）；ruff EN ~130 EN，EN |

---

## EN、GitHub EN（2026-09-06）

### EN PR（2026-09-06 EN，EN 0 EN open）
EN：**EN PR EN，EN**；EN cherry-pick EN PR EN。

| PR | EN |
|----|------|
| #85 #84 #83 | EN cherry-pick EN #91 EN v1.2.1 EN，EN PR EN |
| #78 Atlas Cloud provider | EN #92 EN base_url EN，EN |
| #79 README star chart | EN：EN `api.star-history.com` EN，PR EN |
| #76 TakoAPI EN | EN |
| #86 Windows `.vbs` EN | EN：Windows EN v1.2.1 Provides |
| #82 1080p60 + ENEnglish UI + EN（49 EN） | EN：EN review，ENEnglishEN；EN 1080p60 EN PR |
| #75 TwelveLabs Pegasus EN | EN：Step 3 EN；v1.4 EN |

### Issue EN（2026-09-06 EN）
label EN：EN 9 EN + EN `docker` / `windows` / `feature`。**EN #96**「EN / EN / EN」，
"EN"EN issue EN。open EN 55 → 28（EN #96），EN #40 #56 EN label。

- **EN（v1.2.1 EN）**：#88 #47 #50 #53 #54 #55 #62；#51 #52（dev compose，EN）
- **EN（not planned，EN #96）**："EN"EN #7 #26 #30 #31 #32 #39 #42 #43 #59；EN #3 #13 #23 #25 #34 #41 #58 #60 #80 #87
- **EN open · Docker/EN**（`docker,bug`）：#1 #4 #5 #6 #9 #15 #21 #33 → EN，EN v1.2.1 Release EN
- **EN open · Windows**（`windows`）：#2 #19 #35 → EN v1.2.1 Release EN Windows EN（#73 EN）
- **EN open · EN**（`feature`）：#67 FunASR/SenseVoice、#45 EN（#57 #72 EN #92 EN）
- **EN open · EN bug**（`bug`）：#11 EN 0、#24 EN、#38 EN、#20 EN、#27 EN、#77 API EN
- **EN open · question**：#10 #14 #18 #36；EN #40 #56 EN

### 2026-09-20 EN（open 16 EN，EN #96）
| EN | Issue | EN |
|---|---|---|
| EN（EN） | #100 | EN「#100 EN」；EN：EN + EN |
| EN v1.2.1 EN | #24 EN 20% | EN newengine EN worker EN `-Q`，#89 EN |
| EN「EN」bug EN | #20 #38 #18（EN） | EN：ffmpeg EN cover jpg EN ffmpeg EN mjpeg EN；EN |
| EN（EN） | #27 EN pytz（v1.1.0）、#14 EN localhost（v1.2.1） | |
| EN，v1.3 EN | #11 EN 0 | EN top-K EN main EN |
| `needs-info` EN | #77 | EN |
| EN #96 EN | #10 #36 | EN |
| EN feature | #45 EN | EN「OpenAI EN」+ base_url `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` EN；v1.3 EN dashscope EN「EN」EN |
| EN，EN v1.4 | #67 SenseVoice | LauraGPT EN 123mlly fork EN PR（EN 5 EN），EN ASR EN |

EN PR（2026-09-20）：#97 `ProjectResponse` EN（EN pydantic v2 EN，`POST /projects/` EN 500，2 EN + EN）、#98 EN worker EN `-Q`（EN #89 EN）→ **EN**；
#99 EN CI EN → EN（main EN `9f81b5c` EN CI EN；EN #100 PR EN）；
#101 i18n EnglishEN（18 EN +1393，EN）→ **EN PR**：EN i18n EN（EN v1.3），EN。EN v1.3「i18n」。

### EN（2026-09-07 EN，EN QQ EN / EN）
EN：EN，EN。EN：

| EN | EN | EN | EN |
|------|------|------|--------|
| **EN** | EN GitHub EN | EN「AutoClip EN」（ENAccount `my.feishu.cn`，base `EuYLb3lQ2awwDFsTkDXchabsnbd`，EN「EN」）。EN `https://my.feishu.cn/share/base/shrcn8hKUG2icIJLpNry6uWVNJe`，EN：EN / EN / EN / EN / EN / ContactEN；EN EN / EN / EN | EN `wkfTMIXp3h6zTWNk`：EN → EN「EN」→ EN（EN「EN」EN） |
| **GitHub Issue Forms** | EN | `.github/ISSUE_TEMPLATE/`：bug（EN / EN / EN）、feature、config.yml ContactEN（#96 / Discussions / EN）。Discussions EN | `.github/workflows/issue-hygiene.yml`：EN issue EN；`needs-info` 14+7 EN；60+14 EN stale；`pinned` / `feature` EN |
| **EN `#feedback`** | EN | `autoclip_intro` FAQ EN「EN」EN，EN + Issues / Discussions；QQ / EN | — |

- EN label：`needs-triage`（EN）/ `needs-info` / `stale` / `pinned`（#96 EN）。
- #96 EN「EN」EN。
- EN CLI：EN `lark-cli` profile `personal`（app `cli_aa9ce7782ea39bcf`）；yahaha AccountEN。
- **EN**（2026-09-07 EN）：`frontend/src/analytics/feedback.ts` + `components/FeedbackDialog.tsx`。EN：EN「EN」EN、EN `EN · EN`、EN `EN`、EN 0 EN。EN EN / OS / EN / provider / model / EN / EN；EN + ENContactEN。
  - EN：`feedback_opened` / `feedback_submitted` / `feedback_dismissed`（PostHog）。EN PostHog EN **「AutoClip EN」**（`FEEDBACK_SURVEY_NAME`，EN `VITE_PUBLIC_POSTHOG_FEEDBACK_SURVEY_ID` EN id）EN API EN Survey（EN UI，EN、EN），EN PostHog EN `survey shown / sent / dismissed`，EN Surveys EN。**Survey EN PostHog EN**（EN）。
  - EN，EN PostHog，EN。
- **EN**：`scripts/weekly_digest.py`（EN）。EN GitHub EN issue（`gh`，EN `GH_TOKEN` REST）+ EN（EN `lark-cli` user EN；EN `LARK_APP_ID/SECRET` tenant token，**EN `base:record:read` EN**）+ PostHog `feedback_submitted`（`POSTHOG_PERSONAL_API_KEY` + `POSTHOG_PROJECT_ID`，HogQL）→ markdown → EN webhook（`FEISHU_WEBHOOK_URL`，EN `FEISHU_WEBHOOK_SECRET`）。`--json` EN agent EN，`--post --message-file` EN。EN GitHub + EN。Cursor Automation（EN 09:00 EN）EN，EN Automations EN secrets EN。

---

## EN、EN

### v1.2.1 EN
- [x] EN #89 #90 #91 #92 #93 #94
- [x] `workflow_dispatch` EN Windows EN：EN，EN 145 MB（run 34040814275）
- [x] EN `v1.2.1` tag（`a5c20ae`）→ Desktop Build run 34042037733 EN（Windows 10 min / mac 14 min），
      Release EN：`AutoClip.Desktop_1.2.1_aarch64.dmg`（223 MB）、`AutoClip.Desktop_1.2.1_x64-setup.exe`（145 MB）；EN；#73 EN
- [ ] EN Windows EN Windows EN：EN、EN provider、EN
      （EN：NSIS EN Python EN、WebView2 EN、`%APPDATA%\AutoClip` EN）
- [ ] EN key EN 4 EN provider EN「EN」+ EN（#92 EN provider EN，EN；EN openai SDK EN 3.x）
- [x] EN issue、EN PR #83 #84 #85 #78
- [x] label EN + EN #96 + "EN"EN
- [x] EN PR EN（EN）

### v1.3 · Phase 0 EN + EN
- [ ] Windows EN：Intel mac（PBS `x86_64-apple-darwin` + osxexperts intel EN，EN）
- [ ] Apple Developer ID EN + EN（EN"EN"）；Windows EN（EN SmartScreen EN）
- [ ] Tauri updater EN；Sentry EN
- [ ] `ruff` EN；`requirements-dev.txt` EN pytest（Dockerfile / EN）
- [x] EN provider EN / Colorful Tag EN `DESIGN.md` EN → 2026-09-07 EN / EN / EN `DESIGN.md`「App Layer」EN（EN）
- [ ] EN、`ProjectTaskManager`、`CollectionPreviewModal` / `CreateCollectionModal`、B EN AntD EN，EN `frontend/src/ui/` EN
- [ ] `ProjectCard.tsx` EN「EN + EN」EN（EN AntD Card + EN），EN `ac-card`
- [x] Docker EN（2026-09-20，#100）；EN
- [x] **EN**（2026-09-20）：`pipeline/failures.py#PipelineFailure(stage, message, hint)`；adapter EN LLM EN（`AUTOCLIP_LLM_CACHE_DIR` EN），
      EN / step1 EN / EN / EN / ffmpeg EN；`tasks/processing.py` EN `error`（EN `message`，
      EN「EN」EN）；`ProjectResponse.error_message` EN Task，CLI EN `project_metadata.last_error`。
      EN（EN、EN key、Upload 8 EN）：2 EN failed，EN / EN / status EN。EN `tests/test_pipeline_failures.py`（13 EN）。
      **EN main EN bug**：① `/projects/upload` EN `db`，ENUploadEN 5 EN；
      ② `database.py` EN SQLite EN `StaticPool`，EN Session EN ROLLBACK（`ObjectDeletedError`）→ EN + WAL；
      ③ EN `update_state()` EN Redis EN → `DesktopAwareTask.update_state` no-op
- [ ] **i18n EN**（EN：#101 + #100 EN）：Windows EN DMG EN、EN。EN
      —— `i18next` + `react-i18next`、`locales/{zh,en}.json`、EN key EN、LanguageEN「EN → EN」、AntD `ConfigProvider` locale EN、
      `dayjs` locale EN；EN `frontend/src/ui/` EN（EN）。EN #101 EN PR
- [x] **dashscope EN**（#45，2026-09-20）：`DashScopeProvider(base_url=…)` EN（`DASHSCOPE_CN/INTL_COMPATIBLE_BASE_URL` EN），
      `LLMManager` EN `dashscope_base_url`（EN `OPENAI_BASE_URL` EN），EN「EN / EN」Segmented，`/test-api` EN；
      compose / env.example / DOCKER.md EN `DASHSCOPE_BASE_URL`。EN：EN → EN → EN，`current-provider` EN intl base_url。
      EN DashScope EN API Key EN INFO EN。issue EN
- [x] **`min_score` EN step3**（2026-09-20）：`step3.resolve_min_score_threshold()`：CLI `MIN_SCORE_OVERRIDE` > settings.json `processing.processing_min_score`（`LLMManager.get_processing_setting`，EN）> 0.7。
      `chunk_size` / `max_clips_per_collection` EN settings EN step1 / step5 EN，EN
- [x] **EN**（2026-09-20）：`RELEASE_CHECKLIST.md` EN；`scripts/bump_version.py`、`scripts/release_notes.py`；`desktop-build.yml` release job EN `body_path`。
      EN：EN PR + EN CHANGELOG → EN `bump_version.py X.Y.0 --commit` → EN tag → 25 EN → EN Windows EN（EN）
- [ ] `DESIGN.md` EN（`ErrorBoundary` EN）：`index.css:704-712`、`assets/background.svg`、`FileUpload.tsx`、`BilibiliDownload.tsx`、
      `BilibiliManager.css`、`CreateCollectionModal.css`、`CollectionPreviewModal_fixed.tsx` EN / EN
- [ ] CLI / MCP EN：EN `autoclip run --provider ollama --json` EN MCP `start_clip_job` EN completed；
      `autoclip` EN Homebrew tap / PyPI（EN `pip install -e .`）；README EN CLI EN
- [ ] EN「Ollama EN」EN（EN"EN"）；`min_score` EN step3（CLI EN，EN 0.7）
- [ ] EN：EN 5 EN、EN 60 EN，EN vs EN duration profile；EN `backend/eval/cases/`
- [ ] EN：EN / Shorts / B EN；EN、EN

### v1.4 · EN
- [ ] EN（#59 "5 EN 3 EN 2 EN"、#11 EN 0、#24 EN）
- [ ] **ASR EN**（#67）：EN `utils/speech_recognizer.py` EN `ASRBackend` EN（`transcribe(audio) -> cues`，cue EN、EN、EN），
      faster-whisper EN；EN LauraGPT / 123mlly EN fork EN SenseVoice EN（EN CTC EN → cue EN + EN）EN PR。
      EN ASR EN
- [ ] **Step 3 EN**（EN #75 EN）：EN
- [ ] Sentry EN（Phase 0 EN）：#77 EN issue EN
- [ ] EN `ROADMAP.md` EN Phase 1（Supabase AccountEN）；Phase 0 EN（EN / EN / Sentry）EN Phase 1

---

## EN、EN

- EN：`scripts/build_macos_arm.sh`、`scripts/build_windows_x64.sh`，EN `scripts/lib/desktop_build_common.sh`（EN `scripts/README.md`）；Windows EN `src-tauri/tauri.windows.conf.json`
- EN（Rust）：`src-tauri/src/backend_manager.rs`（EN `AUTOCLIP_DESKTOP_MODE` / `AUTOCLIP_APP_DIR` / ffmpeg EN / `AUTOCLIP_APP_VERSION`；Windows EN `PYTHONUTF8=1`）
- EN：`backend/desktop_main.py`
- EN（EN vs Celery）：`backend/utils/task_submission_utils.py`、`backend/core/celery_app.py`（DesktopAwareTask、task_routes）
- ffmpeg EN：`backend/utils/ffmpeg_utils.py`
- LLM ProvidesEN：`backend/core/llm_providers.py`（EN `is_local_url` / `make_openai_http_client` EN）；provider / base_url EN：`backend/core/llm_manager.py`；EN：`backend/core/local_presets.py`；EN API：`backend/api/v1/settings.py`（`/local-presets`、`/compatible-models`）
- CLI / MCP：`backend/cli.py`、`backend/mcp_server.py`，EN `backend/services/local_runner.py`（EN / LLM EN / EN / EN / EN）；EN `services/simple_progress.py#add_progress_listener`；EN `pyproject.toml`；Agent skill `skills/autoclip/SKILL.md`；EN `docs/CLI_AND_MCP.md`
- EN：`backend/pipeline/quality.py`（EN / refine / EN），EN step1–3；EN `backend/eval/`；EN `docs/QUALITY_AND_PUBLISH_PLAN.md`
- EN：`backend/services/publish_export.py`；API `POST /projects/{id}/clips/{id}/export`；CLI `autoclip export`；MCP `export_clip`；EN `ClipCard` Dialog
- YouTube EN：`backend/api/v1/youtube.py`（`AUTOCLIP_YT_SUBTITLE_LANGS`、`AUTOCLIP_YT_CLIENT`）
- Whisper EN（EN）：`backend/services/whisper_runtime.py`、`whisper_model_manager.py`、
  EN `frontend/src/components/SpeechRecognitionConfig.tsx`
- EN UI EN（`DESIGN.md` App Layer）：`frontend/src/ui/index.tsx` + `ui/ac.css`；EN：`pages/ProjectDetailPage.tsx`、`pages/SettingsPage.tsx`、`components/ClipCard.tsx`、`CollectionCard.tsx`、`SpeechRecognitionConfig.tsx`
- EN：`frontend/src/analytics/feedback.ts`、`components/FeedbackDialog.tsx`；EN `analytics/lifecycle.ts#getRuntimeInfo`
- EN / EN：`frontend/src/utils/domTranslationGuard.ts`（`main.tsx` EN）、`components/ErrorBoundary.tsx`；
  Web EN：`backend/tests/test_settings_web_mode.py`
- EN：`scripts/weekly_digest.py`
- EN（EN）：`BACKEND_URL=http://127.0.0.1:PORT npm run dev`（`vite.config.ts` EN）
- Docker：`Dockerfile`、`docker-compose.yml`（EN `autoclip:local`）、`docker-entrypoint.sh`
- CI：`.github/workflows/ci.yml`（backend / frontend / docker-smoke）、`desktop-build.yml`（tag EN）

## EN、EN（EN）

**EN（EN）**
1. EN Releases EN DMG → EN `AutoClip Desktop` EN Applications
2. **EN → EN**（ad-hoc EN，EN Gatekeeper）
3. EN LLM API key EN

**Docker**
```bash
docker compose up -d --build
# EN http://localhost:3000 · API http://localhost:8000/api/v1/health/
```
Linux EN `mkdir -p data logs uploads && chmod -R 777 data logs uploads`
（EN root EN，bind mount EN root EN）。

EN：
```bash
'/Applications/AutoClip Desktop.app/Contents/MacOS/autoclip-desktop'
# EN Backend started on port: XXXXX / Application startup complete
```
