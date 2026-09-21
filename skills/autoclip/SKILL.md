---
name: autoclip
description: >-
   AutoClip local（ /  /  / ）、。
  "clip"""""""""，
  localuse。 MCP tool（clip_video / start_clip_job），
   MCP  `autoclip` CLI  `--json` 。
---

# AutoClip：

AutoClip local AI cliptool：subtitles（ SRT local Whisper ）→ LLM outline →
 → ffmpeg  → 。projectdata directory， AutoClip ，。

## call

1. ** `autoclip` MCP tool** → tool，。
2. ** MCP  shell** → `autoclip run <video> --json`（ `python -m backend.cli run ...`）。
3.  → install：`pip install -e .`（） `docs/CLI_AND_MCP.md`。

## MCP tool

| tool |  |
|---|---|
| `check_environment` | 、failed：ffmpeg / Whisper / model |
| `clip_video` |  ≤ 30 minutestoolcall；returnprogress |
| `start_clip_job` + `get_job_status` | toolcalllimit； 10–20 ，`status`  `completed`  `result`  |
| `get_project` / `list_projects` | project |
| `list_providers` | "model / " |
| `export_clip` | 「 /  / Shorts」—— 9:16、subtitles、 |

（`clip_video`  `start_clip_job` ）：
- `video_path`：。。
- `srt_path`：subtitles， Whisper minutes。
- `category`：`default` / `knowledge` / `business` / `opinion` / `experience` / `speech` / `content_review` / `entertainment`，impact； `default`。
- `min_score`：0–1，default 0.7。**clips as 0  0.5 **，""。
- `provider`：model。free /  `ollama`（ Ollama，defaultmodel `qwen2.5:7b`） `lmstudio`（ `model`）。
- `model` / `base_url` / `api_key`：。

## CLI 

```bash
autoclip run talk.mp4 --json                          # modelconfig
autoclip run talk.mp4 --srt talk.srt --min-score 0.5 --json
autoclip run talk.mp4 --provider ollama --json        # local Ollama，no need key
autoclip run talk.mp4 --provider openai --base-url https://api.deepseek.com/v1 --model deepseek-chat --api-key sk-...
autoclip doctor --json                                # 
autoclip list --json / autoclip show <project_id> --json
```

`--json`  stdout  JSON ；progress stderr。 `--json`  stdout  `project_id`。
：0 succeeded，1 failed，2  / error。

## 

`clips[]` ：`title`、`start_time`、`end_time`（`HH:MM:SS,mmm`）、`score_100`（0–100）、`reason`、`file`（mp4 ）。
`collections[]`：`title`、`summary`、`clip_ids`、`file`。`clips_dir` / `collections_dir` 。

：
- clip ** ·  · **，recommend；file。
- ，notesclip。
- " AutoClip project"（data directory）。

## FAQ

- **subtitles、**：Whisper modeldownload；。Whisper not installed `check_environment.whisper.ok=false`，「settings → speech recognition」install， `srt_path`。
- **modelconnection failed**：`check_environment.llm.error` reason。`ollama`  →  `ollama serve`  `ollama pull qwen2.5:7b`；cloud provider →  key，Settings page， `api_key`。
- **clips as 0**： `min_score`  0.5； 0 notes（ / ）。
- **proxylocal 502**：AutoClip  localhost / proxy，need Clash 。
- ：MCP server ， `start_clip_job` ，phenomenon。
