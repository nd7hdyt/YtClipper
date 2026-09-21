"""
python -m backend.eval              # EN cases/ EN
python -m backend.eval --live       # EN：EN AUTOCLIP_LLM_CACHE_DIR

EN case ENuservideo，ENsubtitles + EN LLM timeEN。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from backend.pipeline.quality import profile_from_srt, refine_timeline
from backend.utils.text_processor import TextProcessor
from backend.eval.metrics import compute_metrics

CASES = Path(__file__).resolve().parent / "cases"


def _run_case(case_dir: Path) -> Dict:
    expect = json.loads((case_dir / "expect.json").read_text(encoding="utf-8"))
    srt = TextProcessor.parse_srt(case_dir / "input.srt")
    timeline = json.loads((case_dir / "timeline.json").read_text(encoding="utf-8"))
    profile = profile_from_srt(srt)
    refined, report = refine_timeline(timeline, srt, profile)
    video_sec = profile.total_sec
    metrics = compute_metrics(refined, expect, video_sec)
    return {
        "name": case_dir.name,
        "tier": profile.tier,
        "refine": {"in": report["input"], "out": report["output"], "dropped": len(report["dropped"])},
        **metrics,
    }


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if "--live" in argv:
        print("live EN；pleaseEN AUTOCLIP_LLM_CACHE_DIR EN。", file=sys.stderr)
        return 2
    rows = []
    for d in sorted(p for p in CASES.iterdir() if p.is_dir() and (p / "expect.json").exists()):
        rows.append(_run_case(d))
    if not rows:
        print("EN case。EN backend/eval/cases/<name>/ EN input.srt + timeline.json + expect.json")
        return 1
    ok = True
    for r in rows:
        mark = "✓" if r["ok"] else "✗"
        ok = ok and r["ok"]
        failed = [k for k, v in r["checks"].items() if not v]
        extra = f"  EN: {', '.join(failed)}" if failed else ""
        print(f"{mark} {r['name']:<20} n={r['n']}  {r['durations']}  cov={r['coverage']}{extra}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
