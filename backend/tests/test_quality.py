"""EN：EN、EN、EN（EN）"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.pipeline.quality import (
    align_scores, excerpt_between, profile_for, refine_timeline, select_clips,
    to_seconds, to_srt_time,
)


def _cue(s, e, text="x"):
    return {"start_time": to_srt_time(s), "end_time": to_srt_time(e), "text": text}


def test_profile_short_video_does_not_use_podcast_minimums():
    p = profile_for(5 * 60)
    assert p.tier == "short"
    assert p.min_clip_sec <= 30
    assert p.max_clip_sec <= 180
    assert p.topics_hint[1] <= 8
    hint = p.prompt_hint()
    assert "EN" in hint and "5 EN" in hint
    assert "90 EN" in hint  # EN


def test_profile_long_keeps_podcast_scale():
    p = profile_for(72 * 60)
    assert p.tier == "long"
    assert p.min_clip_sec >= 60
    assert p.topics_hint[0] >= 6


def test_refine_snaps_to_cue_and_drops_too_short():
    # 0–80s，EN cue 2 EN。EN min=20s。
    cues = [_cue(i, i + 2, f"c{i}") for i in range(0, 80, 2)]
    items = [
        {"outline": "EN", "start_time": "00:00:20,200", "end_time": "00:00:28,000", "content": ["b"]},
        {"outline": "EN", "start_time": "00:00:40,000", "end_time": "00:01:10,000", "content": ["c"]},
        {"outline": "EN", "start_time": "00:00:50,000", "end_time": "00:01:08,000", "content": ["d"]},
        # EN 3 EN、EN > 5s、EN cue EN → EN
        {"outline": "EN", "start_time": "00:01:17,000", "end_time": "00:01:19,400", "content": ["a"]},
    ]
    out, report = refine_timeline(items, cues, profile_for(300))
    titles = [_t(x) for x in out]
    assert "EN" not in titles
    assert any(d.get("outline") == "EN" for d in report["dropped"])
    extend = next(x for x in out if x["outline"] == "EN")
    assert extend["duration_sec"] >= 20
    assert "snap" in extend["refine"]["ops"]
    assert report["output"] <= 3
    assert any(m.get("absorbed") == "EN" for m in report["merged"])
    for x in out:
        assert x["duration_sec"] >= 20
        assert abs(to_seconds(x["start_time"]) % 2) < 1e-6


def _t(x):
    o = x.get("outline")
    return o if isinstance(o, str) else str(o)


def test_align_scores_falls_back_when_count_mismatch():
    clips = [
        {"outline": "EN", "id": "1"},
        {"outline": "EN", "id": "2"},
        {"outline": "EN", "id": "3"},
    ]
    llm = [{"outline": "EN", "final_score": 0.9, "recommend_reason": "EN"}]
    scored, stats = align_scores(clips, llm)
    assert stats["matched"] == 1 and stats["fallback"] == 2
    by = {c["outline"]: c for c in scored}
    assert by["EN"]["final_score"] == 0.9
    assert by["EN"]["score_source"] == "fallback"
    assert by["EN"]["final_score"] == 0.5


def test_align_scores_normalizes_0_10_scale():
    clips = [{"outline": "EN"}]
    scored, _ = align_scores(clips, [{"outline": "EN", "final_score": 8, "recommend_reason": "x"}])
    assert scored[0]["final_score"] == 0.8


def test_select_clips_keeps_top_k_when_all_below_threshold():
    scored = [
        {"id": "1", "final_score": 0.4, "outline": "a"},
        {"id": "2", "final_score": 0.3, "outline": "b"},
        {"id": "3", "final_score": 0.2, "outline": "c"},
    ]
    p = profile_for(300)  # min_keep=2
    chosen, info = select_clips(scored, 0.7, p)
    assert len(chosen) == 2
    assert info["fallback_selected"] == 2
    assert all(c["selected_by"] == "fallback" for c in chosen)
    assert {c["id"] for c in chosen} == {"1", "2"}


def test_excerpt_between_truncates():
    cues = [_cue(0, 2, "EN" * 20), _cue(2, 4, "EN")]
    text = excerpt_between(cues, 0, 3, max_chars=20)
    assert len(text) == 20
