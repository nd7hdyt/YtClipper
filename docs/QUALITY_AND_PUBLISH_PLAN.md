# EN × EN — EN

> 2026-09-07 EN。EN「EN」；EN `HANDOFF.md` As Standard。

EN，EN：**EN「EN」，EN**。
#59 EN「EN 5 EN，EN 2 EN，EN」EN——
EN（EN），EN（EN）。

---

## EN、EN：EN

EN `backend/pipeline/step1–6` EN `prompt/*.txt`，EN，EN：

| # | EN | EN | EN |
|---|---|---|---|
| 1 | 5 EN 3×2 EN；EN | EN 60 EN：「EN 90 EN」「EN 3–6 EN」「30 EN 2–5 EN」。**EN**，EN | `prompt/EN.txt` EN；`prompt/EN.txt` EN；`step1_outline.py:67` EN 30 EN |
| 2 | EN / EN | (a) EN LLM 「EN」，EN clamp，EN cue；(b) `-ss` EN `-i` EN + `-c:v copy` → EN，GOP EN | `step2_timeline.py:_parse_and_validate_response`；`video_processor.py:159–168` |
| 3 | EN 0（#11） | EN「EN」：EN → EN；EN 0.7 → 0 EN；JSON EN → EN。EN | `step3_scoring.py:97–99`、`:160` |
| 4 | EN | EN `outline` + EN，EN；「EN」EN | `step3_scoring.py:85–92`、`prompt/EN.txt` |
| 5 | EN「EN / EN」EN | EN `SimplePipelineAdapter` EN `prompt_files`，`prompt/<category>/` EN | `simple_pipeline_adapter.py:122,146,154` |
| 6 | EN / EN | EN，EN；EN LLM EN | `step2_timeline.py:182–208` EN |
| 7 | EN | EN、EN、LLM EN | — |

EN：**EN「EN」EN LLM EN**（EN、EN、EN、EN），EN。

---

## EN、EN 1：EN

### EN
- 5 EN 3–6 EN 30–90 EN；60 EN 6–12 EN 2–6 EN（EN）
- EN cue EN，EN
- 「EN 0」EN；EN top-K
- EN / EN

### EN

**A. EN（DurationProfile）** — `backend/pipeline/quality.py`
- EN SRT EN tier：`short`（< 8 min）/ `medium`（8–30）/ `long`（> 30）
- EN tier EN：`min_clip_sec / target / max_clip_sec / topics_hint / min_keep / max_clips`
- ENChinese「EN」EN step1 / step2 EN，**EN**EN 90 EN / 3–6 EN
- EN `metadata/duration_profile.json`，EN

**B. EN（clip_refiner）** — EN，EN、EN
1. EN cue EN `start`、EN cue EN `end`（±3 s EN，EN cue）
2. EN：EN cue EN `min_clip_sec`，EN；EN → EN < 5 s EN，EN
3. EN：EN cue EN `max_clip_sec`
4. EN：EN，EN > EN 50% → EN（EN outline，EN content）；EN → EN cue
5. EN；EN `metadata/quality_report.json`（EN、EN / EN、EN）
- EN：`run_step2_timeline` EN（EN——EN / Celery / CLI——EN）

**C. EN + EN**
- EN `outline` EN，EN 0.5 + 「EN（EN）」，EN
- EN：`>= threshold` EN；EN `min_keep` EN `selected_by: "fallback"`；EN `max_clips` EN
- EN（EN ~600 EN），EN
- `SimplePipelineAdapter` EN `video_category` → `get_prompt_files(category)` EN

**D. EN** — `backend/eval/`
- `LLMClient` EN / EN：`AUTOCLIP_LLM_CACHE_DIR` EN `sha1(prompt+input)` EN / EN；CI EN，EN API EN、EN
- `eval/cases/<name>/{input.srt, expect.json}`：`expect.json` EN——EN、EN、EN、`must_not_zero`、（EN）EN
- `eval/metrics.py`：EN / EN / EN / EN / EN / EN
- `python -m backend.eval` EN case，EN + EN `eval/reports/<date>.json`；`--live` EN
- EN case：EN 3 EN（75 s / 3 min / 8 min）EN；EN，EN `.gitignore` EN cache

**E.（EN）** Step 3 EN（EN #75 EN），ASR EN（#67），Based onEN A/B。

---

## EN、EN 2：EN「EN」

### EN
ENUploadEN / EN / Shorts / B EN，EN。

### EN
- **EN**（EN 16:9 EN，EN）；EN**EN、EN**，EN
- EN ffmpeg EN，filter graph EN，EN MoviePy EN
- EN：EN / EN / EN / EN / EN

### EN

**A. EN** — `backend/services/publish_export.py`
- EN：`-ss` EN + `libx264 veryfast crf 20` + `aac 160k` + `+faststart` EN（EN 1 EN）
- EN 9:16 EN：`blur`（EN + EN）、`crop`（EN）；`none` EN 16:9
- EN：EN SRT EN、EN、EN SRT → `subtitles=` filter + `force_style`（EN / EN / EN）
- EN：`drawtext` EN 4 EN `generated_title`（`textfile=` EN），EN
- Typography：mac EN `PingFang SC`，Linux / Docker EN `fonts-noto-cjk`，Windows `Microsoft YaHei`；EN `sans-serif` EN
- EN：`douyin` / `xiaohongshu`（1080×1920 blur）、`shorts`（1080×1920 crop，≤ 60 s EN）、`bilibili`（1920×1080 EN + EN）、`original`（EN）
- EN `output/exports/{clip_id}_{preset}.mp4`，EN（EN）

**B. EN**
- API：`POST /projects/{id}/clips/{clip_id}/export`（EN，EN job）、`GET /projects/{id}/exports/{job_id}`、`GET /projects/{id}/exports/{job_id}/download`
- CLI：`autoclip export <project_id> --preset douyin [--clip 2 --clip 5] [--no-subtitles] [--no-title]`
- MCP：`export_clip(project_id, clip_id, preset, ...)`

**C. EN** — `ClipCard` EN「EN」EN「EN」：`Dialog` EN `Segmented` EN、EN / EN，`ProgressLine` EN，EN `Btn` EN。EN `frontend/src/ui` EN，EN `DESIGN.md`。

**D.（EN）** EN（EN + EN），EN（EN + EN），EN（B EN）。

---

## EN、EN

| EN | EN |
|---|---|
| 5 EN 2 EN | eval case `short-*`：EN 3–6，EN 20–150 s |
| EN | `quality_report.snap_offsets` p90 < 0.5 s；EN 5 EN |
| EN | eval EN case `clips >= min_keep`；`fallback_rate` EN 100% |
| EN | EN：ffprobe EN、EN、EN 4 EN、EN（±0.1 s） |
| EN | EN 139 EN + docker-smoke EN；EN stream copy EN 16:9 |

---

## EN、EN

- 2026-09-07：EN 1 A–D、EN 2 A–C。
  - EN：`backend/pipeline/quality.py`，step1/2/3 EN `SimplePipelineAdapter` EN；LLM EN；`backend/eval`（`short-synthetic` EN）；`publish_export.py` + API/CLI/MCP + ClipCard Dialog。
  - EN 149 EN（EN `test_quality` / `test_publish_export`）；frontend `tsc` EN。
  - EN：EN 5 EN、EN、EN、EN。
