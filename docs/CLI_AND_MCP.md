# AutoClip EN、MCP EN

EN，EN、EN：

| EN | EN | EN |
|---|---|---|
| CLI | `autoclip run video.mp4 --provider ollama` One command to produce clips | `backend/cli.py` |
| MCP server | EN Cursor / Claude Code / EN MCP EN AutoClip | `backend/mcp_server.py` |
| EN | EN / CLI EN Ollama、LM Studio，EN key | `backend/core/local_presets.py` |

EN `backend/services/local_runner.py`：EN FastAPI / Celery，EN `SimplePipelineAdapter`，
EN、metadata、SQLite EN——CLI EN，EN。

---

## 1. EN

```bash
git clone https://github.com/nd7hdyt/YtClipper.git && cd autoclip
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install -e .            # EN autoclip / autoclip-mcp EN
```

EN：`python -m backend.cli ...`（EN）。

EN ffmpeg EN PATH（`brew install ffmpeg`）。EN Whisper：`pip install faster-whisper`，
EN「EN → EN」EN（EN）。

EN：

```bash
autoclip doctor
# EN ~/Library/Application Support/AutoClip · Python 3.11.9
# ✓ ffmpeg   /opt/homebrew/bin/ffmpeg
# ✓ whisper  faster-whisper EN
# ✓ EN     ollama · qwen2.5:7b · http://localhost:11434/v1
```

---

## 2. CLI

```bash
autoclip run talk.mp4                                  # EN
autoclip run talk.mp4 --provider ollama                # EN Ollama（EN qwen2.5:7b，EN key）
autoclip run talk.mp4 --provider lmstudio --model qwen2.5-7b-instruct
autoclip run talk.mp4 --provider openai --base-url https://api.deepseek.com/v1 --model deepseek-chat --api-key sk-...
autoclip run talk.mp4 --srt talk.srt --category knowledge --min-score 0.6
autoclip run talk.mp4 --json                           # EN / agent：stdout EN JSON

autoclip list                                          # EN
autoclip show <project_id>                             # EN、EN、EN
autoclip providers                                     # ProvidesEN，EN
autoclip doctor --provider ollama                      # EN provider EN
autoclip mcp                                           # EN MCP server EN（EN）
autoclip export <project_id> --preset douyin           # EN 9:16 + EN + EN
autoclip export <project_id> --clip 2 --clip 5 --preset shorts --no-title
```

EN：
- EN、EN **stderr**；**stdout** EN `project_id`（EN `--json` EN JSON），EN。
- EN：`0` EN · `1` EN · `2` EN / EN。
- `--provider` EN，EN `cli-settings.json`。
- EN**EN**EN（EN），EN；`--copy` EN。
- `--no-db` EN SQLite（EN）。
- EN：EN（mac `~/Library/Application Support/AutoClip`、Windows `%APPDATA%\AutoClip`、Linux `~/.local/share/AutoClip`），
  `--data-dir` EN `AUTOCLIP_DATA_DIR` EN。EN `<EN>/logs/cli.log`，`-v` EN。
- `--min-score` EN step3 EN（0–1，EN 0.7）；**EN 0 EN 0.5**。

`--json` EN（EN）：

```json
{
  "ok": true,
  "project_id": "3f9c…",
  "name": "talk",
  "clips_dir": "…/projects/3f9c…/output/clips",
  "clips": [
    {"id": "2", "title": "EN", "start_time": "00:12:03,000", "end_time": "00:14:40,000",
     "score": 0.91, "score_100": 91, "reason": "…", "file": "…/2_EN.mp4"}
  ],
  "collections": [{"id": "1", "title": "EN", "clip_ids": ["2", "5"], "file": "…/EN.mp4"}],
  "counts": {"clips": 6, "collections": 2},
  "elapsed_sec": 412.3,
  "llm": {"provider": "ollama", "model": "qwen2.5:7b", "base_url": "http://localhost:11434/v1"}
}
```

---

## 3. MCP server

stdio EN，EN `mcp` Python SDK（`requirements.txt` EN；EN 1.x `FastMCP` EN 2.x `MCPServer`）。

**Cursor**（`~/.cursor/mcp.json`）EN **Claude Desktop**（`claude_desktop_config.json`）：

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

EN `command` EN `/path/to/autoclip/venv/bin/python`，`args` EN `["-m", "backend.mcp_server"]`，
EN `"env": {"PYTHONPATH": "/path/to/autoclip"}`。

EN：

| EN | EN |
|---|---|
| `clip_video(video_path, srt_path?, name?, category?, min_score?, provider?, model?, base_url?, api_key?)` | EN，EN MCP progress EN；EN / EN / EN |
| `start_clip_job(EN)` | EN，EN `project_id`（EN） |
| `get_job_status(project_id)` | `status` queued / running / completed / failed，`percent` / `stage` / `message`，EN `result` |
| `get_project(project_id)` | EN（EN） |
| `list_projects(limit=20)` | EN |
| `list_providers()` | EN provider + EN + EN |
| `check_environment(provider?, …)` | ffmpeg / Whisper / EN |
| `export_clip(project_id, clip_id, preset?, subtitles?, title_card?)` | EN（douyin / xiaohongshu / shorts / bilibili / original） |

EN：
- EN `print()`，EN stdout EN；server EN `sys.stdout` EN stderr，EN stdout EN MCP EN。
- EN LLM EN，EN `threading.Lock` EN；`start_clip_job` EN。
- EN；server EN `get_job_status` EN。

**Agent skill**：`skills/autoclip/SKILL.md` EN agent EN、EN、EN、EN 0 EN。
EN `~/.cursor/skills/autoclip/` EN `~/.claude/skills/autoclip/` EN。

---

## 4. EN（Ollama / LM Studio）

EN OpenAI EN + `base_url`，EN、EN key EN：

| EN | EN | EN | EN |
|---|---|---|---|
| `ollama` | `http://localhost:11434/v1` | `qwen2.5:7b` | `ollama pull qwen2.5:7b`；ChineseEN |
| `lmstudio` | `http://localhost:1234/v1` | （ENAs Standard） | LM Studio EN Local Server |

**EN**：ENProvidesEN「Ollama（EN）」「LM Studio（EN）」；EN（EN / EN）、
EN `/v1/models` EN，EN API Key。EN provider EN provider EN。

**EN**：`settings.json` EN `llm_provider` EN `ollama` / `lmstudio`，`LLMManager._apply_local_preset` EN
`openai` + `base_url`，API key EN `EMPTY`（EN OpenAI key EN）。
`get_current_provider_info()` EN `provider`（EN）EN `backend_provider`（`openai`）。

Docker / CLI EN：`LLM_PROVIDER=ollama LLM_MODEL=qwen2.5:7b`（EN
`OPENAI_BASE_URL=http://host.docker.internal:11434/v1`）。

**EN**：macOS EN Clash EN，`httpx` EN `localhost` EN，EN 502 / EN。
`llm_providers.is_local_url()` EN loopback / EN / `*.local` / `host.docker.internal` EN，
EN `trust_env=False` EN `httpx.Client`，EN。

EN API（EN）：
- `GET /api/v1/settings/local-presets` — EN
- `GET /api/v1/settings/compatible-models?base_url=…` — EN
- `POST /api/v1/settings/test-api` — `provider` EN `ollama` / `lmstudio`

---

## 5. EN

```bash
cd backend && python -m pytest tests/test_local_presets.py tests/test_cli.py -q
```

- `test_local_presets.py`：EN、LLMManager EN、`test-api` EN、EN、`is_local_url`
- `test_cli.py`：EN、`--help` EN、EN SQLite EN（EN）、EN、EN、MCP EN

EN（EN Ollama EN key）：

```bash
autoclip run /path/to/talk.mp4 --provider ollama --min-score 0.5 --json
```
