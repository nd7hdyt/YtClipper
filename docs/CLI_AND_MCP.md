# AutoClip 、MCP localmodel

，、data directory：

|  |  |  |
|---|---|---|
| CLI | `autoclip run video.mp4 --provider ollama`  | `backend/cli.py` |
| MCP server |  Cursor / Claude Code /  MCP  AutoClip | `backend/mcp_server.py` |
| localmodel | Settings page / CLI  Ollama、LM Studio， key | `backend/core/local_presets.py` |

 `backend/services/local_runner.py`： FastAPI / Celery， `SimplePipelineAdapter`，
、metadata、SQLite ——CLI ，open。

---

## 1. install

```bash
git clone https://github.com/zhouxiaoka/autoclip.git && cd autoclip
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install -e .            #  autoclip / autoclip-mcp 
```

：`python -m backend.cli ...`（）。

need ffmpeg  PATH（`brew install ffmpeg`）。subtitleslocal Whisper：`pip install faster-whisper`，
「settings → speech recognition」install（model）。

：

```bash
autoclip doctor
# data directory ~/Library/Application Support/AutoClip · Python 3.11.9
# ✓ ffmpeg   /opt/homebrew/bin/ffmpeg
# ✓ whisper  faster-whisper install
# ✓ model     ollama · qwen2.5:7b · http://localhost:11434/v1
```

---

## 2. CLI

```bash
autoclip run talk.mp4                                  # Settings pagemodel
autoclip run talk.mp4 --provider ollama                # local Ollama（default qwen2.5:7b，no need key）
autoclip run talk.mp4 --provider lmstudio --model qwen2.5-7b-instruct
autoclip run talk.mp4 --provider openai --base-url https://api.deepseek.com/v1 --model deepseek-chat --api-key sk-...
autoclip run talk.mp4 --srt talk.srt --category knowledge --min-score 0.6
autoclip run talk.mp4 --json                           #  / agent：stdout  JSON

autoclip list                                          # project
autoclip show <project_id>                             # clip、、file
autoclip providers                                     # providerlocal，
autoclip doctor --provider ollama                      #  provider 
autoclip mcp                                           #  MCP server （）
autoclip export <project_id> --preset douyin           #  9:16 + subtitles + 
autoclip export <project_id> --clip 2 --clip 5 --preset shorts --no-title
```

：
- progress、notes **stderr**；**stdout**  `project_id`（ `--json`  JSON），。
- ：`0` succeeded · `1` failed · `2`  / error。
- `--provider` modelsettings，data directory `cli-settings.json`。
- default****project（），；`--copy` 。
- `--no-db`  SQLite（project）。
- data directory：default（mac `~/Library/Application Support/AutoClip`、Windows `%APPDATA%\AutoClip`、Linux `~/.local/share/AutoClip`），
  `--data-dir`  `AUTOCLIP_DATA_DIR` 。 `<data directory>/logs/cli.log`，`-v` 。
- `--min-score`  step3 （0–1，default 0.7）；**clips as 0  0.5**。

`--json` （）：

```json
{
  "ok": true,
  "project_id": "3f9c…",
  "name": "talk",
  "clips_dir": "…/projects/3f9c…/output/clips",
  "clips": [
    {"id": "2", "title": "local", "start_time": "00:12:03,000", "end_time": "00:14:40,000",
     "score": 0.91, "score_100": 91, "reason": "…", "file": "…/2_local.mp4"}
  ],
  "collections": [{"id": "1", "title": "", "clip_ids": ["2", "5"], "file": "…/.mp4"}],
  "counts": {"clips": 6, "collections": 2},
  "elapsed_sec": 412.3,
  "llm": {"provider": "ollama", "model": "qwen2.5:7b", "base_url": "http://localhost:11434/v1"}
}
```

---

## 3. MCP server

stdio ，dependencies `mcp` Python SDK（`requirements.txt` ； 1.x `FastMCP`  2.x `MCPServer`）。

**Cursor**（`~/.cursor/mcp.json`） **Claude Desktop**（`claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "autoclip": { "command": "/path/to/autoclip/venv/bin/autoclip", "args": ["mcp"] }
  }
}
```

**Claude Code**：

```bash
claude mcp add autoclip -- /path/to/autoclip/venv/bin/autoclip mcp
```

 `command`  `/path/to/autoclip/venv/bin/python`，`args`  `["-m", "backend.mcp_server"]`，
 `"env": {"PYTHONPATH": "/path/to/autoclip"}`。

tool：

| tool | notes |
|---|---|
| `clip_video(video_path, srt_path?, name?, category?, min_score?, provider?, model?, base_url?, api_key?)` | ， MCP progress progress；returnclip /  / file |
| `start_clip_job()` | ，return `project_id`（call） |
| `get_job_status(project_id)` | `status` queued / running / completed / failed，`percent` / `stage` / `message`，completed `result` |
| `get_project(project_id)` | project（） |
| `list_projects(limit=20)` | project |
| `list_providers()` | cloud provider + local + config |
| `check_environment(provider?, …)` | ffmpeg / Whisper / model |
| `export_clip(project_id, clip_id, preset?, subtitles?, title_card?)` | （douyin / xiaohongshu / shorts / bilibili / original） |

：
-  `print()`， stdout ；server start `sys.stdout`  stderr， stdout  MCP 。
-  LLM config， `threading.Lock` ；`start_clip_job` 。
- statusmemory；server  `get_job_status` project。

**Agent skill**：`skills/autoclip/SKILL.md`  agent tool、、、clips as 0 。
 `~/.cursor/skills/autoclip/`  `~/.claude/skills/autoclip/` 。

---

## 4. localmodel（Ollama / LM Studio）

 OpenAI API + `base_url`，defaultmodel、 key optional：

|  |  | defaultmodel | notes |
|---|---|---|---|
| `ollama` | `http://localhost:11434/v1` | `qwen2.5:7b` | `ollama pull qwen2.5:7b`；Chinesesubtitles |
| `lmstudio` | `http://localhost:1234/v1` | （service） | LM Studio modelstart Local Server |

**Settings page**：modelprovider「Ollama（local）」「LM Studio（local）」；service（port / ）、
 `/v1/models` optionalmodel， API Key。cloud provider model provider default。

**backend**：`settings.json`  `llm_provider`  `ollama` / `lmstudio`，`LLMManager._apply_local_preset` 
`openai` + `base_url`，API key  `EMPTY`（ OpenAI key localservice）。
`get_current_provider_info()` return `provider`（） `backend_provider`（`openai`）。

Docker / CLI env varavailable：`LLM_PROVIDER=ollama LLM_MODEL=qwen2.5:7b`（access
`OPENAI_BASE_URL=http://host.docker.internal:11434/v1`）。

**proxyissue**：macOS  Clash proxy，`httpx`  `localhost` proxy， 502 / 。
`llm_providers.is_local_url()`  loopback /  / `*.local` / `host.docker.internal` ，
create `trust_env=False`  `httpx.Client`，no needproxy。

 API（）：
- `GET /api/v1/settings/local-presets` — 
- `GET /api/v1/settings/compatible-models?base_url=…` — servicemodel
- `POST /api/v1/settings/test-api` — `provider`  `ollama` / `lmstudio`

---

## 5. test

```bash
cd backend && python -m pytest tests/test_local_presets.py tests/test_cli.py -q
```

- `test_local_presets.py`：、LLMManager 、`test-api` 、localproxy、`is_local_url`
- `test_cli.py`：、`--help` 、project SQLite （）、、progress、MCP tool

（need Ollama cloud key）：

```bash
autoclip run /path/to/talk.mp4 --provider ollama --min-score 0.5 --json
```
