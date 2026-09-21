---
name: autoclip
description: >-
  EN AutoClip EN（EN / EN / EN / EN）EN、EN。
  WhenEN"EN""EN""EN""EN""EN"，
  EN。EN MCP Tool（clip_video / start_clip_job），
  EN MCP EN `autoclip` CLI EN `--json` EN。
---

# AutoClip：EN

AutoClip EN AI ENTool：EN（EN SRT EN Whisper EN）→ LLM EN →
EN → ffmpeg EN → EN。ENProjectEN，EN AutoClip EN，EN。

## EN

1. **EN `autoclip` MCP Tool** → ENTool，EN。
2. **EN MCP EN shell** → `autoclip run <video> --json`（EN `python -m backend.cli run ...`）。
3. EN → ENInstall：`pip install -e .`（EN）EN `docs/CLI_AND_MCP.md`。

## MCP ToolEN

| Tool | EN |
|---|---|
| `check_environment` | EN、ENFailedEN：ffmpeg / Whisper / EN |
| `clip_video` | EN ≤ 30 ENToolEN；EN |
| `start_clip_job` + `get_job_status` | ENToolEN；EN 10–20 EN，`status` EN `completed` EN `result` EN |
| `get_project` / `list_projects` | ENProject |
| `list_providers` | EN"EN / EN" |
| `export_clip` | EN「EN / EN / Shorts」——EN 9:16、EN、EN |

EN（`clip_video` EN `start_clip_job` EN）：
- `video_path`：EN。EN。
- `srt_path`：EN，EN Whisper EN。
- `category`：`default` / `knowledge` / `business` / `opinion` / `experience` / `speech` / `content_review` / `entertainment`，EN；EN `default`。
- `min_score`：0–1，EN 0.7。**EN 0 EN 0.5 EN**，EN"EN"。
- `provider`：EN。EN / EN `ollama`（EN Ollama，EN `qwen2.5:7b`）EN `lmstudio`（EN `model`）。
- `model` / `base_url` / `api_key`：EN。

## CLI EN

```bash
autoclip run talk.mp4 --json                          # ENConfig
autoclip run talk.mp4 --srt talk.srt --min-score 0.5 --json
autoclip run talk.mp4 --provider ollama --json        # EN Ollama，EN key
autoclip run talk.mp4 --provider openai --base-url https://api.deepseek.com/v1 --model deepseek-chat --api-key sk-...
autoclip doctor --json                                # EN
autoclip list --json / autoclip show <project_id> --json
```

`--json` EN stdout EN JSON EN；EN stderr。EN `--json` EN stdout EN `project_id`。
EN：0 Success，1 ENFailed，2 EN / EnvironmentError。

## EN

`clips[]` EN：`title`、`start_time`、`end_time`（`HH:MM:SS,mmm`）、`score_100`（0–100）、`reason`、`file`（mp4 EN）。
`collections[]`：`title`、`summary`、`clip_ids`、`file`。`clips_dir` / `collections_dir` EN。

EN：
- ENEachEN **EN · EN · EN**，EN；EN。
- EN，EN。
- EN"EN AutoClip ENProject"（EN）。

## EN

- **EN、EN**：Whisper ENDownload；EN。Whisper ENInstallEN `check_environment.whisper.ok=false`，EN「EN → EN」ENInstall，EN `srt_path`。
- **ENFailed**：`check_environment.llm.error` EN。`ollama` EN → EN `ollama serve` EN `ollama pull qwen2.5:7b`；EN provider → EN key，EN，EN `api_key`。
- **EN 0**：EN `min_score` EN 0.5；EN 0 EN（EN / EN）。
- **SystemEN 502**：AutoClip EN localhost / ENAutoEN，ENNeedEN Clash ENThen。
- EN：MCP server EN，EN `start_clip_job` EN，EN。
