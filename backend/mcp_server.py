"""
AutoClip MCP server (stdio) — lets Cursor / Claude Code / any MCP client call AutoClip directly.

Launch:
    autoclip mcp                       # installed package
    python -m backend.mcp_server       # inside the repo

Client config example (Cursor `~/.cursor/mcp.json` / Claude `claude mcp add`):
    { "mcpServers": { "autoclip": { "command": "autoclip", "args": ["mcp"] } } }
    or { "command": "/path/to/autoclip/venv/bin/python", "args": ["-m", "backend.mcp_server"],
         "env": { "PYTHONPATH": "/path/to/autoclip" } }

Tools:
    clip_video          synchronous clipping (minutes to tens of minutes, with progress notifications)
    start_clip_job      background clipping, returns project_id immediately
    get_job_status      check progress / fetch results
    get_project         clips, collections, and file paths of a finished project
    list_projects       recent projects
    list_providers      available model providers and local presets (ollama / lmstudio)
    check_environment   ffmpeg / Whisper / model connectivity check

Requires the `mcp` Python SDK (already in requirements.txt; compatible with 1.x FastMCP and 2.x MCPServer).
"""
from __future__ import annotations

import asyncio
import logging
import sys
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.services.local_runner import (
    LLMOverride,
    RunRequest,
    configure_environment,
    setup_logging,
)

logger = logging.getLogger(__name__)

try:  # mcp 2.x
    from mcp.server.mcpserver import MCPServer as _Server, Context  # type: ignore
except ImportError:  # mcp 1.x
    try:
        from mcp.server.fastmcp import FastMCP as _Server, Context  # type: ignore
    except ImportError as e:  # pragma: no cover
        raise SystemExit("Missing mcp SDK: pip install mcp") from e

INSTRUCTIONS = """AutoClip cuts long videos (lectures / interviews / podcast recordings) into titled, scored highlight clips and groups them into themed collections.
Typical flow: user gives a local video path -> call clip_video (or start_clip_job + poll get_job_status) ->
summarize the returned clip list (titles / time ranges / scores / file paths) for the user.
Without subtitles, local Whisper transcription is used; slower on first run. To save cost or work offline: provider="ollama" (requires Ollama installed locally).
Zero clips usually means the score threshold is too high; retry with min_score=0.5."""

server = _Server(
    name="autoclip",
    instructions=INSTRUCTIONS,
)

# ---------------------------------------------------------------- job registry ---
_jobs: Dict[str, Dict[str, Any]] = {}
_jobs_lock = threading.Lock()
_pipeline_lock = threading.Lock()  # global LLM config is process-wide; run jobs serially


def _job_update(project_id: str, **fields: Any) -> None:
    with _jobs_lock:
        _jobs.setdefault(project_id, {})
        _jobs[project_id].update(fields)


def _run_job(req: RunRequest, override: LLMOverride, link: bool) -> Dict[str, Any]:
    """Run blocking; called in a thread."""
    from backend.services.local_runner import configure_llm, prepare_project, run_pipeline, summarize_project

    with _pipeline_lock:
        try:
            info = configure_llm(override)
            video_in_raw = prepare_project(req, link=link)
            _job_update(req.project_id, status="running", llm=info, percent=0, stage="INGEST", message="Started")

            def on_progress(p: Dict[str, Any]) -> None:
                _job_update(req.project_id, percent=p.get("percent", 0), stage=p.get("stage"), message=p.get("message"))

            result = run_pipeline(req, video_in_raw, on_progress=on_progress)
            if result.get("status") != "succeeded":
                _job_update(req.project_id, status="failed", error=result.get("error") or "Processing failed")
                return _jobs[req.project_id]
            summary = summarize_project(req.project_id)
            _job_update(req.project_id, status="completed", percent=100, stage="DONE", message="Done", result=summary)
            return _jobs[req.project_id]
        except Exception as e:  # noqa: BLE001
            logger.exception("MCP job failed")
            _job_update(req.project_id, status="failed", error=str(e)[:500])
            return _jobs[req.project_id]


def _make_request(video_path: str, srt_path: Optional[str], name: Optional[str], category: str,
                  min_score: Optional[float]) -> RunRequest:
    return RunRequest(
        video=Path(video_path),
        srt=Path(srt_path) if srt_path else None,
        name=name,
        category=category or "default",
        min_score=min_score,
    )


def _make_override(provider: Optional[str], model: Optional[str], base_url: Optional[str], api_key: Optional[str]) -> LLMOverride:
    return LLMOverride(provider=provider, model=model, base_url=base_url, api_key=api_key)


# ---------------------------------------------------------------- tools ---
@server.tool(
    name="clip_video",
    description=(
        "Cut a local video into highlight clips (synchronous; takes minutes to tens of minutes with progress updates). "
        "Returns the clip list (title / start-end time / score / mp4 path) and collections. "
        "provider: dashscope / openai / gemini / siliconflow / ollama / lmstudio; omit to use the desktop app's configured model."
    ),
)
async def clip_video(
    video_path: str,
    ctx: Context,
    srt_path: Optional[str] = None,
    name: Optional[str] = None,
    category: str = "default",
    min_score: Optional[float] = None,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    req = _make_request(video_path, srt_path, name, category, min_score)
    override = _make_override(provider, model, base_url, api_key)
    _job_update(req.project_id, status="queued", percent=0, video=str(req.video))

    task = asyncio.create_task(asyncio.to_thread(_run_job, req, override, True))
    last_percent = -1
    while not task.done():
        await asyncio.sleep(1.0)
        job = _jobs.get(req.project_id, {})
        pct = int(job.get("percent") or 0)
        if pct != last_percent:
            last_percent = pct
            try:
                await ctx.report_progress(pct, 100, f"{job.get('stage', '')} {job.get('message', '')}".strip())
            except Exception:  # noqa: BLE001
                pass
    job = task.result()
    if job.get("status") != "completed":
        return {"ok": False, "project_id": req.project_id, "error": job.get("error", "Processing failed")}
    return {"ok": True, **job["result"], "llm": job.get("llm")}


@server.tool(
    name="start_clip_job",
    description="Start clipping in the background and return project_id immediately; then poll progress and results with get_job_status. For clients with a per-tool-call timeout.",
)
def start_clip_job(
    video_path: str,
    srt_path: Optional[str] = None,
    name: Optional[str] = None,
    category: str = "default",
    min_score: Optional[float] = None,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    req = _make_request(video_path, srt_path, name, category, min_score)
    if not req.video.expanduser().exists():
        return {"ok": False, "error": f"Video not found: {req.video}"}
    override = _make_override(provider, model, base_url, api_key)
    _job_update(req.project_id, status="queued", percent=0, video=str(req.video))
    t = threading.Thread(target=_run_job, args=(req, override, True), daemon=True, name=f"autoclip-{req.project_id[:8]}")
    t.start()
    return {"ok": True, "project_id": req.project_id, "status": "queued", "hint": "Poll with get_job_status; every 10-20 seconds is enough."}


@server.tool(name="get_job_status", description="Check a task started by start_clip_job: status (queued / running / completed / failed), percent, stage, message; result is attached on completion.")
def get_job_status(project_id: str) -> Dict[str, Any]:
    job = _jobs.get(project_id)
    if not job:
        # Possibly a project from a previous process: read straight from disk
        try:
            from backend.services.local_runner import summarize_project
            return {"ok": True, "project_id": project_id, "status": "completed", "result": summarize_project(project_id)}
        except FileNotFoundError:
            return {"ok": False, "project_id": project_id, "error": "No such job / project"}
    return {"ok": job.get("status") != "failed", "project_id": project_id, **job}


@server.tool(name="get_project", description="Read a processed project's clips (title / time / score / files), collections, and output directory.")
def get_project(project_id: str) -> Dict[str, Any]:
    from backend.services.local_runner import summarize_project

    try:
        return {"ok": True, **summarize_project(project_id)}
    except FileNotFoundError as e:
        return {"ok": False, "error": str(e)}


@server.tool(name="list_projects", description="List recent AutoClip projects (shares the data directory with the desktop app).")
def list_projects(limit: int = 20) -> List[Dict[str, Any]]:
    from backend.services.local_runner import list_projects as _list

    return _list(limit=limit)


@server.tool(name="list_providers", description="Available model providers and local presets (default URLs and models for ollama / lmstudio), plus the config currently in use.")
def list_providers() -> Dict[str, Any]:
    from backend.core.llm_manager import get_llm_manager
    from backend.core.local_presets import presets_as_dicts

    return {
        "current": get_llm_manager().get_current_provider_info(),
        "cloud": ["dashscope", "openai", "gemini", "siliconflow"],
        "local_presets": presets_as_dicts(),
    }


@server.tool(
    name="export_clip",
    description=(
        "Render a finished clip into a publish-ready video: 9:16 (Douyin/Xiaohongshu/Shorts), burned subtitles, title card. "
        "preset: douyin / xiaohongshu / shorts / bilibili / original. "
        "Returns the output path; re-exporting with the same parameters hits the cache."
    ),
)
def export_clip(
    project_id: str,
    clip_id: str,
    preset: str = "douyin",
    subtitles: bool = True,
    title_card: bool = True,
) -> Dict[str, Any]:
    from backend.services.publish_export import ExportRequest, export_clip as _export
    try:
        return _export(ExportRequest(project_id, clip_id, preset, subtitles, title_card))
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)[:500]}


@server.tool(name="check_environment", description="Health check: whether ffmpeg, the Whisper runtime, and the model connection are ready. Call once before clipping to avoid common pitfalls.")
def check_environment(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    from backend.services.local_runner import configure_llm, environment_report

    override = _make_override(provider, model, base_url, api_key)
    try:
        configure_llm(override)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)}
    rep = environment_report()
    rep["ok"] = bool(rep["ffmpeg"]["ok"] and rep["llm"]["ok"])
    return rep


# ---------------------------------------------------------------- entry ---
async def _serve_stdio() -> None:
    """
    stdout is the MCP protocol channel. The pipeline has stray print() calls, which would
    corrupt the protocol if they reached stdout, so the real stdout is handed to the MCP
    transport layer and sys.stdout is redirected to stderr.
    """
    import io
    import anyio
    from mcp.server.stdio import stdio_server

    real_stdout = anyio.wrap_file(io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True))
    real_stdin = anyio.wrap_file(io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"))
    sys.stdout = sys.stderr

    lowlevel = getattr(server, "_lowlevel_server", None) or getattr(server, "_mcp_server")
    async with stdio_server(stdin=real_stdin, stdout=real_stdout) as (read_stream, write_stream):
        await lowlevel.run(read_stream, write_stream, lowlevel.create_initialization_options())


def main() -> int:
    configure_environment()
    setup_logging(verbose=False)  # logs go to file only; keep the terminal (stderr) quiet
    import anyio

    anyio.run(_serve_stdio)
    return 0


if __name__ == "__main__":
    sys.exit(main())
