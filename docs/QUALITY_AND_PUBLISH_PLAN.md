#  ×  — 

> 2026-09-07 。status「」；progress `HANDOFF.md` 。

，：**「succeeded」，**。
#59 「 5 minutes， 2 minutes，」——
（），（）。

---

## 、：now

 `backend/pipeline/step1–6`  `prompt/*.txt`，issuemodel，：

| # | phenomenon |  | location |
|---|---|---|---|
| 1 | 5 minutes 3×2 minutes； |  60 minutes：「 90 」「target 3–6 minutes」「30 minutes 2–5 」。****， | `prompt/.txt` ；`prompt/outline.txt` ；`step1_outline.py:67`  30 minutes |
| 2 |  /  | (a)  LLM 「」， clamp，subtitles cue；(b) `-ss`  `-i`  + `-c:v copy` → ，GOP  | `step2_timeline.py:_parse_and_validate_response`；`video_processor.py:159–168` |
| 3 | clips as 0（#11） | 「」：return → ； 0.7 → 0 ；JSON failed → 。 | `step3_scoring.py:97–99`、`:160` |
| 4 |  |  `outline` + ，；「」 | `step3_scoring.py:85–92`、`prompt/recommend.txt` |
| 5 | 「 / business」 |  `SimplePipelineAdapter`  `prompt_files`，`prompt/<category>/`  | `simple_pipeline_adapter.py:122,146,154` |
| 6 |  /  | ，； LLM return | `step2_timeline.py:182–208`  |
| 7 |  | 、、LLM  | — |

：**「」 LLM **（、、、），model。

---

## 、 1：

### target
- 5 minutes 3–6  30–90 ；60 minutes 6–12  2–6 minutes（）
- subtitles cue ，
- 「clips as 0」subtitles； top-K
-  / 

### 

**A. （DurationProfile）** — `backend/pipeline/quality.py`
-  SRT  tier：`short`（< 8 min）/ `medium`（8–30）/ `long`（> 30）
-  tier ：`min_clip_sec / target / max_clip_sec / topics_hint / min_keep / max_clips`
- generateChinese「」 step1 / step2 ，**** 90  / 3–6 minutes
-  `metadata/duration_profile.json`，step

**B. （clip_refiner）** — file，、
1.  cue  `start`、 cue  `end`（±3 s ， cue）
2. ： cue  `min_clip_sec`，； →  < 5 s ，
3. ： cue  `max_clip_sec`
4. ：， >  50% → （ outline， content）； →  cue
5. ； `metadata/quality_report.json`（、 / reason、）
- integrate：`run_step2_timeline` （call—— / Celery / CLI——）

**C.  + **
-  `outline` ， 0.5 + 「（）」，
- ：`>= threshold` ； `min_keep`  `selected_by: "fallback"`； `max_clips` 
- （ ~600 ），
- `SimplePipelineAdapter` project `video_category` → `get_prompt_files(category)` 

**D. ** — `backend/eval/`
- `LLMClient`  / ：`AUTOCLIP_LLM_CACHE_DIR`  `sha1(prompt+input)`  / ；CI ， API cost、
- `eval/cases/<name>/{input.srt, expect.json}`：`expect.json` ——、、、`must_not_zero`、（optional）
- `eval/metrics.py`： /  /  /  /  / 
- `python -m backend.eval`  case， +  `eval/reports/<date>.json`；`--live` model
-  case： 3 （75 s / 3 min / 8 min）；， `.gitignore`  cache

**E.（）** Step 3 backend（ #75 ），ASR （#67），based on A/B。

---

## 、 2：「」

### target
 /  / Shorts / B ，。

### 
- **default**（ 16:9 clip，）；export**、**，
-  ffmpeg call，filter graph ， MoviePy dependencies
- ： /  /  / subtitles / 

### 

**A. exportservice** — `backend/services/publish_export.py`
- ：`-ss`  + `libx264 veryfast crf 20` + `aac 160k` + `+faststart` （solve 1 issue）
-  9:16 ：`blur`（ + ）、`crop`（）；`none`  16:9
- subtitles：project SRT 、、 SRT → `subtitles=` filter + `force_style`（ /  / ）
- ：`drawtext`  4  `generated_title`（`textfile=` ），
- ：mac  `PingFang SC`，Linux / Docker  `fonts-noto-cjk`，Windows `Microsoft YaHei`； `sans-serif` 
- ：`douyin` / `xiaohongshu`（1080×1920 blur）、`shorts`（1080×1920 crop，≤ 60 s ）、`bilibili`（1920×1080  + subtitles）、`original`（）
-  `output/exports/{clip_id}_{preset}.mp4`，（return）

**B. **
- API：`POST /projects/{id}/clips/{clip_id}/export`（，return job）、`GET /projects/{id}/exports/{job_id}`、`GET /projects/{id}/exports/{job_id}/download`
- CLI：`autoclip export <project_id> --preset douyin [--clip 2 --clip 5] [--no-subtitles] [--no-title]`
- MCP：`export_clip(project_id, clip_id, preset, ...)`

**C. ** — `ClipCard` 「」「export」：`Dialog`  `Segmented` 、subtitles / ，`ProgressLine` progress，completed `Btn` download。 `frontend/src/ui` ， `DESIGN.md`。

**D.（）** （ + ），（ + ），（B ）。

---

## 、

|  |  |
|---|---|
| 5 minutes 2 minutes | eval case `short-*`： 3–6， 20–150 s |
|  | `quality_report.snap_offsets` p90 < 0.5 s； 5  |
|  | eval  case `clips >= min_keep`；`fallback_rate`  100% |
| export | ：ffprobe 、subtitles、 4 、metadata（±0.1 s） |
|  |  139  + docker-smoke ；defaultexport stream copy  16:9 |

---

## 、

- 2026-09-07： 1 A–D、 2 A–C。
  - ：`backend/pipeline/quality.py`，step1/2/3  `SimplePipelineAdapter` integrate；LLM cache；`backend/eval`（`short-synthetic` ）；`publish_export.py` + API/CLI/MCP + ClipCard Dialog。
  -  149 （ `test_quality` / `test_publish_export`）；frontend `tsc` 。
  - ： 5 minutes、、、。
