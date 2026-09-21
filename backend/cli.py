#!/usr/bin/env python3
"""
autoclip — clip videos from the command line.

    autoclip run video.mp4                         # use the model configured in the desktop app
    autoclip run video.mp4 --provider ollama       # local Ollama (default qwen2.5:7b, no key needed)
    autoclip run video.mp4 --provider lmstudio --model qwen2.5-7b-instruct
    autoclip run video.mp4 --provider openai --base-url https://api.deepseek.com/v1 --model deepseek-chat --api-key sk-...
    autoclip run video.mp4 --srt video.srt --min-score 0.6 --json
    autoclip list / show <project_id> / providers / doctor

Artifacts share the same data directory as the desktop app (macOS: ~/Library/Application Support/AutoClip),
so finished runs show up on the desktop app home screen. Use --data-dir or AUTOCLIP_DATA_DIR to change it.

No install needed: `python -m backend.cli ...`; after `pip install -e .` the `autoclip` command is available.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

# Only import things that do not trigger DB / model initialization; heavy work runs inside subcommands after configure_environment
from backend.services.local_runner import (
    PROVIDER_CHOICES,
    LLMOverride,
    RunRequest,
    configure_environment,
    setup_logging,
)

STAGE_NAMES = {
    "INGEST": "Ingest", "SUBTITLE": "Subtitles", "ANALYZE": "Analyze",
    "HIGHLIGHT": "Highlights", "EXPORT": "Export", "DONE": "Done",
}
_TTY = sys.stderr.isatty()


def _c(code: str, s: str) -> str:
    return f"\033[{code}m{s}\033[0m" if _TTY else s


def _dim(s: str) -> str:
    return _c("2", s)


def _bold(s: str) -> str:
    return _c("1", s)


def _err(msg: str) -> None:
    print(_c("31", "error: ") + msg, file=sys.stderr)


def _add_llm_args(p: argparse.ArgumentParser) -> None:
    g = p.add_argument_group("Model (leave empty to use the desktop app settings page)")
    g.add_argument("--provider", choices=PROVIDER_CHOICES, help="dashscope / openai / gemini / siliconflow, or local presets ollama / lmstudio")
    g.add_argument("--model", help="Model name, e.g. qwen-plus, gpt-4o-mini, qwen2.5:7b")
    g.add_argument("--base-url", help="OpenAI-compatible base URL (used with provider=openai; ollama/lmstudio have defaults)")
    g.add_argument("--api-key", help="API key (optional for local models). Also reads AUTOCLIP_API_KEY")


def _llm_override(args: argparse.Namespace) -> LLMOverride:
    return LLMOverride(
        provider=getattr(args, "provider", None),
        model=getattr(args, "model", None),
        base_url=getattr(args, "base_url", None),
        api_key=getattr(args, "api_key", None) or os.getenv("AUTOCLIP_API_KEY"),
    )


# ---------------------------------------------------------------- run ---
def cmd_run(args: argparse.Namespace) -> int:
    from backend.services.local_runner import configure_llm, prepare_project, run_pipeline, summarize_project

    t0 = time.time()
    try:
        info = configure_llm(_llm_override(args))
    except Exception as e:  # noqa: BLE001
        _err(str(e))
        return 2

    req = RunRequest(
        video=Path(args.video),
        srt=Path(args.srt) if args.srt else None,
        name=args.name,
        category=args.category,
        min_score=args.min_score,
        register_db=not args.no_db,
    )
    try:
        video_in_raw = prepare_project(req, link=not args.copy)
    except FileNotFoundError as e:
        _err(str(e))
        return 2

    if not args.json:
        model_desc = f"{info.get('provider')} · {info.get('model')}"
        if info.get("base_url"):
            model_desc += f" · {info['base_url']}"
        print(_bold(req.name or req.video.stem) + _dim(f"  {req.project_id}"), file=sys.stderr)
        print(_dim(f"Model {model_desc}"), file=sys.stderr)
        if not req.srt:
            print(_dim("No subtitle file; local Whisper transcription will be used (downloads the model on first run)"), file=sys.stderr)

    last = {"line": ""}

    def on_progress(p: Dict[str, Any]) -> None:
        if args.json:
            return
        stage = STAGE_NAMES.get(p.get("stage", ""), p.get("stage", ""))
        line = f"[{p.get('percent', 0):3d}%] {stage:<3} {p.get('message', '')}"
        if line != last["line"]:
            print(line, file=sys.stderr)
            last["line"] = line

    result = run_pipeline(req, video_in_raw, on_progress=on_progress)
    elapsed = time.time() - t0

    if result.get("status") != "succeeded":
        if args.json:
            print(json.dumps({"ok": False, "project_id": req.project_id, "error": result.get("error")}, ensure_ascii=False))
        else:
            _err(result.get("error") or "Processing failed")
            print(_dim(f"Log: {os.getenv('LOG_FILE')}"), file=sys.stderr)
        return 1

    summary = summarize_project(req.project_id)
    summary["elapsed_sec"] = round(elapsed, 1)
    summary["llm"] = {k: info.get(k) for k in ("provider", "model", "base_url") if info.get(k)}
    if args.json:
        print(json.dumps({"ok": True, **summary}, ensure_ascii=False, indent=2))
        return 0

    print(file=sys.stderr)
    n_clips, n_cols = summary["counts"]["clips"], summary["counts"]["collections"]
    print(_bold(f"Done  {n_clips} clips · {n_cols} collections · {elapsed:.0f}s"), file=sys.stderr)
    for c in summary["clips"]:
        score = str(c["score_100"]) if c.get("score_100") is not None else "-"
        print(f"  {score:>4}  {c['start_time']} → {c['end_time']}  {c['title']}", file=sys.stderr)
    if n_clips == 0:
        print(_dim("  No segments met the score threshold; try --min-score 0.5"), file=sys.stderr)
    print(_dim(f"Output directory {summary['clips_dir']}"), file=sys.stderr)
    # stdout carries only the project id for easy shell piping
    print(req.project_id)
    return 0


# ---------------------------------------------------------------- list / show ---
def cmd_list(args: argparse.Namespace) -> int:
    from backend.services.local_runner import list_projects

    items = list_projects(limit=args.limit)
    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return 0
    if not items:
        print(_dim("No projects yet. Start with autoclip run <video>."))
        return 0
    for it in items:
        print(f"{it['project_id']}  {it['status']:<9} {it['clips']:>3} clips  {it['updated_at'][:16]}  {it['name']}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    from backend.services.local_runner import summarize_project

    try:
        s = summarize_project(args.project_id)
    except FileNotFoundError as e:
        _err(str(e))
        return 2
    if args.json:
        print(json.dumps(s, ensure_ascii=False, indent=2))
        return 0
    print(_bold(s["name"]) + _dim(f"  {s['project_id']}"))
    print(_dim(f"{s['counts']['clips']} clips · {s['counts']['collections']} collections · {s['project_dir']}"))
    for c in s["clips"]:
        score = str(c["score_100"]) if c.get("score_100") is not None else "-"
        print(f"  {score:>4}  {c['start_time']} → {c['end_time']}  {c['title']}")
        if c.get("file"):
            print(_dim(f"        {c['file']}"))
    for col in s["collections"]:
        print(f"  Collection  {col['title']}  {_dim('clips ' + ', '.join(col['clip_ids']))}")
        if col.get("file"):
            print(_dim(f"        {col['file']}"))
    return 0


# ---------------------------------------------------------------- providers / doctor ---
def cmd_providers(args: argparse.Namespace) -> int:
    from backend.core.local_presets import LOCAL_PRESETS
    from backend.core.llm_manager import get_llm_manager

    rows = [
        ("dashscope", "Alibaba Qwen", "Requires key; direct connection in China, qwen-plus is good value"),
        ("openai", "OpenAI / compatible API", "Requires key; --base-url can point to DeepSeek / Zhipu / OpenRouter / vLLM"),
        ("gemini", "Google Gemini", "Requires key"),
        ("siliconflow", "SiliconFlow", "Requires key; DeepSeek / Qwen open models"),
    ] + [
        (p.key, p.display_name, f"No key needed; default {p.base_url}" + (f", default model {p.default_model}" if p.default_model else ""))
        for p in LOCAL_PRESETS.values()
    ]
    info = get_llm_manager().get_current_provider_info()
    if args.json:
        print(json.dumps({"current": info, "providers": [dict(zip(("key", "name", "note"), r)) for r in rows]}, ensure_ascii=False, indent=2))
        return 0
    for key, name, note in rows:
        mark = "●" if key == info.get("provider") else " "
        print(f"{mark} {key:<12} {name:<18} {_dim(note)}")
    cur = f"{info.get('provider')} · {info.get('model')}" + (f" · {info['base_url']}" if info.get("base_url") else "")
    print(_dim(f"\nCurrent: {cur}  ({'available' if info.get('available') else 'no key configured'})"))
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    from backend.services.local_runner import configure_llm, environment_report

    try:
        configure_llm(_llm_override(args))
    except Exception as e:  # noqa: BLE001
        _err(str(e))
    rep = environment_report()
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0 if rep["ffmpeg"]["ok"] and rep["llm"]["ok"] else 1

    def line(ok: Optional[bool], label: str, detail: str) -> None:
        mark = _c("32", "✓") if ok else _c("31", "✗")
        print(f"{mark} {label:<8} {detail}")

    print(_dim(f"Data directory {rep['data_dir']} · Python {rep['python']}"))
    line(rep["ffmpeg"]["ok"], "ffmpeg", rep["ffmpeg"].get("path") or rep["ffmpeg"].get("error", ""))
    w = rep["whisper"]
    line(w["ok"], "whisper", ("faster-whisper installed" if w["ok"] else "not installed (required for videos without subtitles; install via Settings > Transcription in the desktop app)"))
    llm = rep["llm"]
    llm_desc = f"{llm.get('provider')} · {llm.get('model')}" + (f" · {llm['base_url']}" if llm.get("base_url") else "")
    line(llm["ok"], "model", llm_desc + ("" if llm["ok"] else f"  {_dim(llm.get('error') or '')}"))
    return 0 if rep["ffmpeg"]["ok"] and llm["ok"] else 1


# ---------------------------------------------------------------- export ---
def cmd_export(args: argparse.Namespace) -> int:
    from backend.services.publish_export import ExportRequest, export_clip, list_presets, load_clip_meta
    from backend.services.local_runner import summarize_project

    if args.list_presets:
        rows = list_presets()
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            for p in rows:
                print(f"{p['key']:<14} {p['label']:<16} {p.get('w') or '-'}x{p.get('h') or '-'}  {p.get('layout')}")
        return 0

    clip_ids = list(args.clip or [])
    if not clip_ids:
        try:
            summary = summarize_project(args.project_id)
        except FileNotFoundError as e:
            _err(str(e))
            return 2
        clip_ids = [c["id"] for c in summary["clips"]]
        if not clip_ids:
            _err("This project has no clips")
            return 2

    results = []
    for cid in clip_ids:
        try:
            load_clip_meta(args.project_id, cid)
            r = export_clip(ExportRequest(
                project_id=args.project_id, clip_id=cid, preset=args.preset,
                subtitles=not args.no_subtitles, title_card=not args.no_title,
            ))
            results.append(r)
            if not args.json:
                print(f"{'cached' if r.get('cached') else 'ok':<8} {cid}  {r.get('path')}", file=sys.stderr)
        except Exception as e:  # noqa: BLE001
            results.append({"ok": False, "clip_id": cid, "error": str(e)[:400]})
            _err(f"{cid}: {e}")

    if args.json:
        print(json.dumps({"ok": all(r.get("ok") for r in results), "exports": results}, ensure_ascii=False, indent=2))
    return 0 if all(r.get("ok") for r in results) else 1


# ---------------------------------------------------------------- mcp ---
def cmd_mcp(args: argparse.Namespace) -> int:
    from backend.mcp_server import main as mcp_main

    return mcp_main()


# ---------------------------------------------------------------- parser ---
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="autoclip",
        description="AutoClip CLI: turn a long video into highlight clips with one command.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("\n\n", 1)[1] if __doc__ else None,
    )
    p.add_argument("--data-dir", help="Data directory (shared with the desktop app by default; also AUTOCLIP_DATA_DIR)")
    p.add_argument("-v", "--verbose", action="store_true", help="Print backend logs to the terminal")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="Process one video into clips and collections")
    r.add_argument("video", help="Video file path")
    r.add_argument("--srt", help="Existing subtitle file (local Whisper transcription is used when omitted)")
    r.add_argument("--name", help="Project name (defaults to the file name)")
    r.add_argument("--category", default="default",
                   choices=["default", "knowledge", "business", "opinion", "experience", "speech", "content_review", "entertainment"],
                   help="Content type; affects prompts")
    r.add_argument("--min-score", type=float, help="Minimum score threshold 0-1 (default 0.7; lower it when you get 0 clips)")
    r.add_argument("--copy", action="store_true", help="Copy the video into the project directory (default is a hard link, no extra space)")
    r.add_argument("--no-db", action="store_true", help="Skip SQLite writes (project will not show in the desktop app)")
    r.add_argument("--json", action="store_true", help="Output results as JSON (for scripts / agents)")
    _add_llm_args(r)
    r.set_defaults(func=cmd_run)

    l = sub.add_parser("list", help="List projects")
    l.add_argument("--limit", type=int, default=30)
    l.add_argument("--json", action="store_true")
    l.set_defaults(func=cmd_list)

    s = sub.add_parser("show", help="Show one project's clips and file paths")
    s.add_argument("project_id")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_show)

    pr = sub.add_parser("providers", help="List available model providers and local presets")
    pr.add_argument("--json", action="store_true")
    pr.set_defaults(func=cmd_providers)

    d = sub.add_parser("doctor", help="Check ffmpeg / Whisper / model connectivity")
    d.add_argument("--json", action="store_true")
    _add_llm_args(d)
    d.set_defaults(func=cmd_doctor)

    m = sub.add_parser("mcp", help="Run as an MCP server (stdio) for Cursor / Claude")
    m.set_defaults(func=cmd_mcp)

    e = sub.add_parser("export", help="Render clips into publish-ready videos (9:16 / burned subtitles / title cards)")
    e.add_argument("project_id")
    e.add_argument("--preset", default="douyin", choices=["douyin", "xiaohongshu", "shorts", "bilibili", "original"])
    e.add_argument("--clip", action="append", help="Clip id, repeatable; exports all clips when omitted")
    e.add_argument("--no-subtitles", action="store_true")
    e.add_argument("--no-title", action="store_true")
    e.add_argument("--list-presets", action="store_true")
    e.add_argument("--json", action="store_true")
    e.set_defaults(func=cmd_export)
    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_environment(Path(args.data_dir) if args.data_dir else None)
    setup_logging(verbose=args.verbose)
    try:
        return int(args.func(args) or 0)
    except KeyboardInterrupt:
        print(file=sys.stderr)
        _err("Interrupted")
        return 130


if __name__ == "__main__":
    sys.exit(main())
