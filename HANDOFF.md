# AutoClip — Project Status / Progress / Plan

> ：2026-09-20 ·  `main@aaf863bb`（**v1.2.1 Release**：Release  macOS arm64 DMG 223 MB + Windows x64 InstallationPackage 145 MB；
>  2026-09-20 Download Windows 1136 / DMG 334 —— Windows Is）

AutoClip Is AI ： B/YouTube ，、
。IsCurrent StatusPlan； `ROADMAP.md`。

---

## 、Architecture & Delivery

|  |  |  |
|----|------|------|
| Backend | FastAPI + Celery（）+ SQLite | `backend/` |
|  | React + TypeScript + Ant Design + Vite | `frontend/` |
|  | Tauri 2 + Rust | `src-tauri/` |
| LLM | OpenAI  OpenAI （ base_url）/ Gemini(google-genai) / (dashscope) /  /  Ollama、LM Studio | `backend/core/llm_providers.py`、`llm_manager.py`、`local_presets.py` |
| CLI / MCP | `autoclip`  + MCP server（stdio）， FastAPI / Celery  | `backend/cli.py`、`mcp_server.py`、`services/local_runner.py` |

：****（macOS arm64 DMG ；Windows x64 InstallationPackage v1.2.1 ，）、**Docker **（README Recommended）、
****（`start_autoclip.sh`）、**CLI / MCP**（`pip install -e .`， agent，`docs/CLI_AND_MCP.md`）。

---

## 、Current Status

### Completed
- **v1.2.0（2026-06-03）**： DMG To（ Python + Static ffmpeg + Installation faster-whisper），
  `desktop-build.yml`  tag  Release；v1.2.0 DMG  2000+ Download。
- **PostHog ** +  + （`docs/ANALYTICS.md`、`docs/PRIVACY*.md`）。
- **Calm Premium System**（`DESIGN.md`）。
- Nightly Backend（`nightly-desktop-smoke.yml`）。
- **（2026-09-07）**：
  - `autoclip run video.mp4 --provider ollama` ；`list / show / providers / doctor / mcp` ；`--json`  / agent。
     SQLite，CLI 。
  - MCP server（`autoclip mcp`）7  ：`clip_video`（ + Progress）、`start_clip_job` / `get_job_status`、`get_project`、`list_projects`、`list_providers`、`check_environment`；
     `mcp` 2.x stdio 。Agent skill  `skills/autoclip/SKILL.md`。
  -  Ollama / LM Studio：Select、 `/v1/models`、 key；Backend `local_presets.py`   `openai` + `base_url`。
  - ：`httpx`  localhost System（Clash） 502 → `is_local_url()`  `trust_env=False`；
    `apiConfig.notifyListeners`  listener  `getCurrentProvider`。
  -  `tests/test_local_presets.py`、`tests/test_cli.py`（ 24 ）；**To `autoclip run`**（ v1.3 todo）。
- ** + Release（2026-09-07）**： `docs/QUALITY_AND_PUBLISH_PLAN.md`。
  -  `DurationProfile`（//） step1/2 ，「 90  /  3–6 」。
  - `refine_timeline`： cue、、；`quality_report.json` 。
  - ： outline ； top-K（#11  0）。
  -  adapter  `prompt/<category>/`。`AUTOCLIP_LLM_CACHE_DIR` /。`python -m backend.eval` （`backend/eval/cases/short-synthetic` ）。
  - Release：`publish_export.py`（9:16 blur/crop、、）；API `POST .../clips/{id}/export`；`autoclip export`；MCP `export_clip`；「」Dialog。Is 16:9 copy。
  - ** 5 **； `original` 。
- **#100 （2026-09-20）**：Docker Web  + 。：Is **Chrome「」**  DOM（ → `<font>`）
   React `removeChild NotFoundError`， Gemini ； UI 。：`utils/domTranslationGuard.ts` 
  `removeChild` / `insertBefore`（facebook/react#11538 ），`ErrorBoundary`  `DESIGN.md` （）。
  ：`/settings` 、`/test-api`、`/current-provider`、`/compatible-models`  `check_desktop_mode()`，Docker / 
  （settings.json  `./data`，api / worker  mtime ； `.env`）。（ /  /  / ）。
   `tests/test_settings_web_mode.py`（6 ）；Playwright ： 4 ，。

### v1.2.1（2026-09-06  tag）
：README Recommended `docker compose` From 2025-09 
（issue #88  7 ，），Is issue ""。#89 ：
1. `.dockerignore`  `docker-entrypoint.sh` / `docker-dev-entrypoint.sh`（）
2.  `.gitattributes`，shell  LF（Windows ）
3.  `youtube.py` / `fix_project_thumbnails.py` / `SettingsPage.tsx`  `/Users/zhoukk` 
4. Docker  3.9 → 3.11（yt-dlp ）
5.  `zh-Hans,zh,en`，`AUTOCLIP_YT_SUBTITLE_LANGS` （ 429）
6. `task_submission_utils`  localhost  Redis （Docker ）
7. compose / dev compose / `start_autoclip.sh`  worker  `-Q celery,processing,video,notification,upload`
   （ Docker ）
8. `_build_full_input` list  JSON （#53）
9. CI  `docker-smoke` job ；To 1.2.1； `youtube_improved.py`

：
- **#90**  6   `NodeJS.Timeout` ，`npm run typecheck`  CI 
- **#91**  PR #85（ utf-8）、#84（Gemini `-latest` ）、#83（youtube.py ） cherry-pick （； PR ）
- **#94** `requirements.txt` 
- **#92** OpenAI  `base_url`（#72 #57， #78）。**：Select provider From， dashscope**；
  LLMManager  settings.json mtime ， Docker （`LLM_PROVIDER` / `OPENAI_BASE_URL` / `API_*_API_KEY`）
- **#93** Windows x64 Package + workflow。`workflow_dispatch`  Windows  `windows-latest` ：
  InstallationPackage 145 MB， ~22 min（`cargo install tauri-cli`  8 min + Package 13 min；rust-cache First，）。
  **To**（ todo）

### Pending（ROADMAP Phase 0）
|  |  |
|---|---|
| Apple Developer ID Signature + Notarization | Not done，`signingIdentity: null`，Right-clickOpen |
| Package（Windows / Intel mac / Linux） | Windows x64  runner Package（#93）， v1.2.1 Release Release，****；Intel mac / Linux Not done |
| Sentry  |  |
| Tauri updater  |  |
|  /  | （#94）；PBS + ffmpeg Download actions/cache，Rust  rust-cache |
| `ruff`  CI Is `continue-on-error` | typecheck （#90）；ruff  ~130 ， |

---

## 、GitHub TODO（2026-09-06）

###  PR（2026-09-06 ， 0   open）
：** PR ，**； cherry-pick  PR 。

| PR |  |
|----|------|
| #85 #84 #83 |  cherry-pick  #91  v1.2.1 Release， PR  |
| #78 Atlas Cloud provider |  #92  base_url ， |
| #79 README star chart | ： `api.star-history.com` ，PR Is To |
| #76 TakoAPI  |  |
| #86 Windows `.vbs`  | ：Windows InstallationPackage v1.2.1  |
| #82 1080p60 +  UI + （49 ） | ： review，； 1080p60  PR |
| #75 TwelveLabs Pegasus  | ：Step 3 Backend；v1.4  |

### Issue （2026-09-06 ）
label ： 9   +  `docker` / `windows` / `feature`。** #96**「Current Status /  / 」，
"" issue To。open From 55 → 28（ #96）， #40 #56  label。

- **（v1.2.1 ）**：#88 #47 #50 #53 #54 #55 #62；#51 #52（dev compose，）
- **（not planned，To #96）**："" #7 #26 #30 #31 #32 #39 #42 #43 #59； #3 #13 #23 #25 #34 #41 #58 #60 #80 #87
- ** open · Docker/**（`docker,bug`）：#1 #4 #5 #6 #9 #15 #21 #33 → ， v1.2.1 Release 
- ** open · Windows**（`windows`）：#2 #19 #35 → To v1.2.1 Release  Windows Package（#73 ）
- ** open · **（`feature`）：#67 FunASR/SenseVoice、#45 （#57 #72  #92 ）
- ** open ·  bug**（`bug`）：#11  0、#24 Progress、#38 、#20 、#27 、#77 API 
- ** open · question**：#10 #14 #18 #36； #40 #56 

### 2026-09-20 （open 16 ， #96）
|  | Issue |  |
|---|---|---|
| （） | #100 | 「#100 」；： +  |
|  v1.2.1  | #24 Progress 20% |  newengine Is worker  `-Q`，#89  |
| 「」bug  | #20 #38 #18（） | ：ffmpeg  cover jpg  ffmpeg  mjpeg ； |
| （） | #27  pytz（v1.1.0）、#14  localhost（v1.2.1） | |
| ，v1.3  | #11  0 |  top-K  main  |
| `needs-info`  | #77 |  |
| To #96  | #10 #36 |  |
|  feature | #45  | Select「OpenAI 」+ base_url `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` ；v1.3  dashscope 「」 |
| ， v1.4 | #67 SenseVoice | LauraGPT  123mlly fork  PR（ 5 ），Is ASR  Select |

 PR（2026-09-20）：#97 `ProjectResponse` （ pydantic v2 ，`POST /projects/`  500，2  + ）、#98  worker  `-Q`（ #89 ）→ ****；
#99  CI  → （main  `9f81b5c`  CI ； #100 PR ）；
#101 i18n （18  +1393，First）→ ** PR**： i18n （ v1.3），。 v1.3「i18n」。

### （2026-09-07 ， QQ  /  ）
：，To 。 ：

|  |  |  |  |
|------|------|------|--------|
| **** |  GitHub  | 「AutoClip 」（  `my.feishu.cn`，base `EuYLb3lQ2awwDFsTkDXchabsnbd`，「」）。 `https://my.feishu.cn/share/base/shrcn8hKUG2icIJLpNry6uWVNJe`，： /  /  /  /  / ；  /  /  |  `wkfTMIXp3h6zTWNk`： → 「」→ （「Open」） |
| **GitHub Issue Forms** |  | `.github/ISSUE_TEMPLATE/`：bug（ /  / ）、feature、config.yml （#96 / Discussions / ）。Discussions  | `.github/workflows/issue-hygiene.yml`： issue ；`needs-info` 14+7 ；60+14  stale；`pinned` / `feature`  |
| ** `#feedback`** |  | `autoclip_intro` FAQ 「」， + Issues / Discussions；QQ /  | — |

-  label：`needs-triage`（）/ `needs-info` / `stale` / `pinned`（#96 ）。
- #96 「」。
-  CLI： `lark-cli` profile `personal`（app `cli_aa9ce7782ea39bcf`）；yahaha 。
- ****（2026-09-07 ）：`frontend/src/analytics/feedback.ts` + `components/FeedbackDialog.tsx`。：「」、 ` · `、 ``、 0 。  / OS /  / provider / model /  / ； + Select。
  - ：`feedback_opened` / `feedback_submitted` / `feedback_dismissed`（PostHog）。 PostHog  **「AutoClip 」**（`FEEDBACK_SURVEY_NAME`， `VITE_PUBLIC_POSTHOG_FEEDBACK_SURVEY_ID`  id） API  Survey（ UI，、Select）， PostHog  `survey shown / sent / dismissed`， Surveys 。**Survey  PostHog **（）。
  - ， PostHog，To。
- ****：`scripts/weekly_digest.py`（Only）。 GitHub  issue（`gh`， `GH_TOKEN` REST）+ （ `lark-cli` user ； `LARK_APP_ID/SECRET` tenant token，** `base:record:read` **）+ PostHog `feedback_submitted`（`POSTHOG_PERSONAL_API_KEY` + `POSTHOG_PROJECT_ID`，HogQL）→ markdown →  webhook（`FEISHU_WEBHOOK_URL`，Select `FEISHU_WEBHOOK_SECRET`）。`--json`  agent ，`--post --message-file` 。 GitHub + 。Cursor Automation（ 09:00 ）， Automations  secrets 。

---

## 、Plan

### v1.2.1 
- [x]  #89 #90 #91 #92 #93 #94
- [x] `workflow_dispatch`  Windows ：，InstallationPackage 145 MB（run 34040814275）
- [x]  `v1.2.1` tag（`a5c20ae`）→ Desktop Build run 34042037733 （Windows 10 min / mac 14 min），
      Release  ：`AutoClip.Desktop_1.2.1_aarch64.dmg`（223 MB）、`AutoClip.Desktop_1.2.1_x64-setup.exe`（145 MB）；；#73 
- [ ]   Windows InstallationPackageTo Windows ：、 provider、
      （：NSIS   Python 、WebView2 、`%APPDATA%\AutoClip` ）
- [ ]  key  4   provider 「」+ （#92  provider Select，； openai SDK Is 3.x）
- [x]  issue、 PR #83 #84 #85 #78
- [x] label  +  #96 + ""
- [x]  PR （）

### v1.3 · Phase 0  + 
- [ ] Windows Package：Intel mac（PBS `x86_64-apple-darwin` + osxexperts intel StaticPackage， ）
- [ ] Apple Developer ID Signature + Notarization（"Right-clickOpen"）；Windows Signature（ SmartScreen ）
- [ ] Tauri updater ；Sentry 
- [ ] `ruff` ；`requirements-dev.txt`  pytest（Dockerfile / Package）
- [x]  provider  /  Tag  `DESIGN.md`  → 2026-09-07  /  /  `DESIGN.md`「App Layer」（）
- [ ] 、`ProjectTaskManager`、`CollectionPreviewModal` / `CreateCollectionModal`、B Is AntD ， `frontend/src/ui/` 
- [ ] `ProjectCard.tsx` 「 + 」（Is AntD Card + ）， `ac-card`
- [x] Docker （2026-09-20，#100）；
- [x] ****（2026-09-20）：`pipeline/failures.py#PipelineFailure(stage, message, hint)`；adapter  LLM （`AUTOCLIP_LLM_CACHE_DIR` ），
       / step1  /  /  / ffmpeg ；`tasks/processing.py`  `error`（ `message`，
      To「」 ）；`ProjectResponse.error_message`  Task，CLI  `project_metadata.last_error`。
      （、 key、 8 ）：2  failed， /  / status  。 `tests/test_pipeline_failures.py`（13 ）。
      **  main  bug**：① `/projects/upload`  `db`，From 5 From；
      ② `database.py`  SQLite  `StaticPool`， Session  ROLLBACK（`ObjectDeletedError`）→  + WAL；
      ③  `update_state()`  Redis Backend → `DesktopAwareTask.update_state` no-op
- [ ] **i18n **（：#101 + #100 ）：Windows DownloadIs DMG 、。
      —— `i18next` + `react-i18next`、`locales/{zh,en}.json`、 key 、「 → 」、AntD `ConfigProvider` locale 、
      `dayjs` locale ； `frontend/src/ui/` （）。 #101  PR
- [x] **dashscope **（#45，2026-09-20）：`DashScopeProvider(base_url=…)` （`DASHSCOPE_CN/INTL_COMPATIBLE_BASE_URL` ），
      `LLMManager`  `dashscope_base_url`（ `OPENAI_BASE_URL` ），「 / 」Segmented，`/test-api` ；
      compose / env.example / DOCKER.md  `DASHSCOPE_BASE_URL`。： →  → ，`current-provider`  intl base_url。
       DashScope   API Key  INFO 。issue 
- [x] **`min_score` To step3**（2026-09-20）：`step3.resolve_min_score_threshold()`：CLI `MIN_SCORE_OVERRIDE` > settings.json `processing.processing_min_score`（`LLMManager.get_processing_setting`，）> 0.7。
      `chunk_size` / `max_clips_per_collection`  settings  step1 / step5 ，
- [x] ****（2026-09-20）：`RELEASE_CHECKLIST.md` ；`scripts/bump_version.py`、`scripts/release_notes.py`；`desktop-build.yml` release job  `body_path`。
      ： PR +  CHANGELOG →  `bump_version.py X.Y.0 --commit` →  tag → 25 Package →  Windows Package（）
- [ ] `DESIGN.md` （`ErrorBoundary` ）：`index.css:704-712`、`assets/background.svg`、`FileUpload.tsx`、`BilibiliDownload.tsx`、
      `BilibiliManager.css`、`CreateCollectionModal.css`、`CollectionPreviewModal_fixed.tsx`  / 
- [ ] CLI / MCP To： `autoclip run --provider ollama --json`  MCP `start_clip_job` To completed；
      `autoclip`  Homebrew tap / PyPI（ `pip install -e .`）；README  CLI 
- [ ] 「Ollama 」（"To"）；`min_score` To step3（CLI ，Is 0.7）
- [ ] ： 5 、 60 ， vs  duration profile；  `backend/eval/cases/`
- [ ] Release： / Shorts / B ；、Not done

### v1.4 · 
- [ ] （#59 "5  3   2 "、#11  0、#24 Progress）
- [ ] **ASR Backend**（#67）： `utils/speech_recognizer.py`  `ASRBackend` （`transcribe(audio) -> cues`，cue 、、），
      faster-whisper ； LauraGPT / 123mlly   fork  SenseVoice （ CTC  → cue  + ） PR。
       ASR 
- [ ] **Step 3 Backend**（ #75 ）：
- [ ] Sentry To（Phase 0 ）：#77  issue 
- [ ]  `ROADMAP.md`  Phase 1（Supabase ）；Phase 0 （SignatureNotarization /  / Sentry） Phase 1

---

## 、Key Files

- Package：`scripts/build_macos_arm.sh`、`scripts/build_windows_x64.sh`， `scripts/lib/desktop_build_common.sh`（ `scripts/README.md`）；Windows  `src-tauri/tauri.windows.conf.json`
- Backend（Rust）：`src-tauri/src/backend_manager.rs`（ `AUTOCLIP_DESKTOP_MODE` / `AUTOCLIP_APP_DIR` / ffmpeg  / `AUTOCLIP_APP_VERSION`；Windows  `PYTHONUTF8=1`）
- Backend：`backend/desktop_main.py`
- （ vs Celery）：`backend/utils/task_submission_utils.py`、`backend/core/celery_app.py`（DesktopAwareTask、task_routes）
- ffmpeg ：`backend/utils/ffmpeg_utils.py`
- LLM ：`backend/core/llm_providers.py`（ `is_local_url` / `make_openai_http_client` BypassSystem）；provider / base_url Select：`backend/core/llm_manager.py`；：`backend/core/local_presets.py`； API：`backend/api/v1/settings.py`（`/local-presets`、`/compatible-models`）
- CLI / MCP：`backend/cli.py`、`backend/mcp_server.py`， `backend/services/local_runner.py`（ / LLM  /  /  / ）；Progress `services/simple_progress.py#add_progress_listener`；Package `pyproject.toml`；Agent skill `skills/autoclip/SKILL.md`； `docs/CLI_AND_MCP.md`
- ：`backend/pipeline/quality.py`（ / refine / ）， step1–3； `backend/eval/`； `docs/QUALITY_AND_PUBLISH_PLAN.md`
- Release：`backend/services/publish_export.py`；API `POST /projects/{id}/clips/{id}/export`；CLI `autoclip export`；MCP `export_clip`； `ClipCard` Dialog
- YouTube ：`backend/api/v1/youtube.py`（`AUTOCLIP_YT_SUBTITLE_LANGS`、`AUTOCLIP_YT_CLIENT`）
- Whisper Runtime（Installation）：`backend/services/whisper_runtime.py`、`whisper_model_manager.py`、
   `frontend/src/components/SpeechRecognitionConfig.tsx`
-  UI （`DESIGN.md` App Layer）：`frontend/src/ui/index.tsx` + `ui/ac.css`；：`pages/ProjectDetailPage.tsx`、`pages/SettingsPage.tsx`、`components/ClipCard.tsx`、`CollectionCard.tsx`、`SpeechRecognitionConfig.tsx`
- ：`frontend/src/analytics/feedback.ts`、`components/FeedbackDialog.tsx`；Runtime `analytics/lifecycle.ts#getRuntimeInfo`
-  / ：`frontend/src/utils/domTranslationGuard.ts`（`main.tsx` ）、`components/ErrorBoundary.tsx`；
  Web ：`backend/tests/test_settings_web_mode.py`
- ：`scripts/weekly_digest.py`
- （Backend）：`BACKEND_URL=http://127.0.0.1:PORT npm run dev`（`vite.config.ts` ）
- Docker：`Dockerfile`、`docker-compose.yml`（ `autoclip:local`）、`docker-entrypoint.sh`
- CI：`.github/workflows/ci.yml`（backend / frontend / docker-smoke）、`desktop-build.yml`（tag ）

## 、Installation（）

**Desktop（Recommended）**
1. From Releases Download DMG → Drag `AutoClip Desktop` To Applications
2. **FirstRight-click → Open**（ad-hoc Signature，Bypass Gatekeeper）
3.  LLM API key 

**Docker**
```bash
docker compose up -d --build
#  http://localhost:3000 · API http://localhost:8000/api/v1/health/
```
Linux First `mkdir -p data logs uploads && chmod -R 777 data logs uploads`
（ root ，bind mount  root ）。

Debug desktop backend via CLI：
```bash
'/Applications/AutoClip Desktop.app/Contents/MacOS/autoclip-desktop'
# Should see Backend started on port: XXXXX / Application startup complete
```
