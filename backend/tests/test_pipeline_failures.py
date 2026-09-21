"""
「failedtranslatedfailed」translated：LLM translatedcanuse / subtitlestranslated / translated / translated / cliptranslated，
translatedreturn failed translatedandusertranslated，translatedIsonetranslated succeeded translated `Completed · 0 clip`（#100 #11 #24）。
"""

import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest

from backend.pipeline.failures import PipelineFailure

SRT = """1
00:00:01,000 --> 00:00:05,000
No.onetranslated，translated

2
00:00:05,000 --> 00:00:12,000
No.translated，translatedusertranslated
"""


@pytest.fixture
def prompt_files(tmp_path):
    p = tmp_path / "outline.txt"
    p.write_text("translated", encoding="utf-8")
    return {"outline": p}


def _extractor(tmp_path, prompt_files, monkeypatch, responses):
    """responses: per translated'sreturntranslated；translatedcallfailed"""
    from backend.pipeline import step1_outline as step1

    calls = iter(responses)

    class FakeLLM:
        def call_with_retry(self, prompt, input_data=None, **kw):
            r = next(calls)
            if isinstance(r, BaseException):
                raise r
            return r

    monkeypatch.setattr(step1, "LLMClient", lambda: FakeLLM())
    return step1.OutlineExtractor(metadata_dir=tmp_path / "meta", prompt_files=prompt_files)


def test_step1_empty_srt_is_a_subtitle_failure(tmp_path, prompt_files, monkeypatch):
    srt = tmp_path / "empty.srt"
    srt.write_text("", encoding="utf-8")
    extractor = _extractor(tmp_path, prompt_files, monkeypatch, [])

    with pytest.raises(PipelineFailure) as exc:
        extractor.extract_outline(srt)

    assert exc.value.stage == "SUBTITLE"
    assert "translated" in exc.value.message
    assert "translated" in exc.value.hint


def test_step1_all_chunks_failing_surfaces_llm_error(tmp_path, prompt_files, monkeypatch):
    srt = tmp_path / "a.srt"
    srt.write_text(SRT, encoding="utf-8")
    extractor = _extractor(tmp_path, prompt_files, monkeypatch,
                           [ValueError("translatedconfigLLMProvidesprovider，translatedinSettings pagetranslatedconfigAPIkey")])

    with pytest.raises(PipelineFailure) as exc:
        extractor.extract_outline(srt)

    assert exc.value.stage == "ANALYZE"
    assert "1/1" in exc.value.message
    assert "translatedconfigLLMProvidesprovider" in exc.value.message
    assert "testconnect" in exc.value.hint


def test_step1_unparseable_response_is_a_failure_not_empty_list(tmp_path, prompt_files, monkeypatch):
    srt = tmp_path / "a.srt"
    srt.write_text(SRT, encoding="utf-8")
    extractor = _extractor(tmp_path, prompt_files, monkeypatch, ["translated，translatedthis task。"])

    with pytest.raises(PipelineFailure) as exc:
        extractor.extract_outline(srt)

    assert exc.value.stage == "ANALYZE"
    assert "translated" in exc.value.message


def test_step1_partial_chunk_failure_still_returns_outline(tmp_path, prompt_files, monkeypatch):
    """translatedvideotranslatedonetranslated；translatedfailedtranslated"""
    from backend.pipeline import step1_outline as step1

    srt = tmp_path / "a.srt"
    srt.write_text(SRT, encoding="utf-8")
    extractor = _extractor(tmp_path, prompt_files, monkeypatch,
                           [TimeoutError("read timeout"), "1. **translated**\n- translated"])
    # translated
    monkeypatch.setattr(extractor.text_processor, "chunk_srt_data",
                        lambda data, interval_minutes: [
                            {"chunk_index": 0, "text": "translated0", "srt_entries": data[:1]},
                            {"chunk_index": 1, "text": "translated1", "srt_entries": data[1:]},
                        ])

    outlines = extractor.extract_outline(srt)

    assert [o["title"] for o in outlines] == ["translated"]
    assert step1  # keep import used


# ----------------------------------------------------------------- adapter ---

@pytest.fixture
def adapter(tmp_path, monkeypatch):
    from backend.core import path_utils
    from backend.services import simple_pipeline_adapter as mod

    monkeypatch.delenv("AUTOCLIP_LLM_CACHE_DIR", raising=False)
    monkeypatch.setattr(path_utils, "get_project_directory", lambda pid: tmp_path / "projects" / pid)
    monkeypatch.setattr(mod, "clear_progress", lambda pid: None)
    events = []
    monkeypatch.setattr(mod, "emit_progress", lambda pid, stage, message="", subpercent=None: events.append((stage, message)))
    monkeypatch.setattr(mod.SimplePipelineAdapter, "_prompt_files", lambda self, project_dir: {})
    a = mod.SimplePipelineAdapter("proj-1", "task-1")
    a._events = events
    return a


def _fake_manager(monkeypatch, available: bool, display_name="Google Gemini", model="gemini-2.5-flash"):
    from backend.core import llm_manager
    info = {"provider": "gemini", "model": model, "available": available, "display_name": display_name}
    monkeypatch.setattr(llm_manager, "get_llm_manager",
                        lambda: SimpleNamespace(get_current_provider_info=lambda: info))


def test_adapter_fails_fast_when_llm_not_configured(adapter, monkeypatch, tmp_path):
    _fake_manager(monkeypatch, available=False)
    srt = tmp_path / "in.srt"
    srt.write_text(SRT, encoding="utf-8")

    result = asyncio.run(adapter.process_project_sync(str(tmp_path / "in.mp4"), str(srt)))

    assert result["status"] == "failed"
    assert result["stage"] == "ANALYZE"
    assert "Google Gemini · gemini-2.5-flash" in result["error"]
    assert "settings → model" in result["error"]
    assert result["message"] == result["error"]
    # progresstranslatedfailedtranslated，frontendfailedtranslated / translated
    assert adapter._events[-1][0] == "ANALYZE"
    assert adapter._events[-1][1].startswith("processing failed：")


def test_adapter_fails_when_no_subtitle_and_auto_transcribe_yields_nothing(adapter, monkeypatch, tmp_path):
    _fake_manager(monkeypatch, available=True)

    async def no_srt(self, video, metadata_dir):
        return None

    monkeypatch.setattr(type(adapter), "_generate_subtitle_automatically", no_srt)

    result = asyncio.run(adapter.process_project_sync(str(tmp_path / "in.mp4"), ""))

    assert result["status"] == "failed"
    assert result["stage"] == "SUBTITLE"
    assert "translatedsubtitles" in result["error"]
    assert "Whisper" in result["error"]
    # translatedone translated「succeeded」；translatedintranslated step1_outline.json
    assert not (tmp_path / "projects" / "proj-1" / "metadata" / "step1_outline.json").exists()


def test_adapter_fails_when_scoring_keeps_nothing(adapter, monkeypatch, tmp_path):
    from backend.services import simple_pipeline_adapter as mod

    _fake_manager(monkeypatch, available=True)
    srt = tmp_path / "in.srt"
    srt.write_text(SRT, encoding="utf-8")
    monkeypatch.setattr(mod, "run_step1_outline", lambda *a, **k: [{"title": "t"}])
    monkeypatch.setattr(mod, "run_step2_timeline", lambda *a, **k: [{"id": 1}, {"id": 2}])
    monkeypatch.setattr(mod, "run_step3_scoring", lambda *a, **k: [])

    result = asyncio.run(adapter.process_project_sync(str(tmp_path / "in.mp4"), str(srt)))

    assert result["status"] == "failed"
    assert result["stage"] == "ANALYZE"
    assert "2  translatedSelect" in result["error"]
    assert "translated" in result["error"]


def test_adapter_fails_when_ffmpeg_produced_no_clip(adapter, monkeypatch, tmp_path):
    from backend.services import simple_pipeline_adapter as mod

    _fake_manager(monkeypatch, available=True)
    srt = tmp_path / "in.srt"
    srt.write_text(SRT, encoding="utf-8")
    monkeypatch.setattr(mod, "run_step1_outline", lambda *a, **k: [{"title": "t"}])
    monkeypatch.setattr(mod, "run_step2_timeline", lambda *a, **k: [{"id": 1}])
    monkeypatch.setattr(mod, "run_step3_scoring", lambda *a, **k: [{"id": 1, "final_score": 0.9}])
    monkeypatch.setattr(mod, "run_step4_title", lambda *a, **k: [{"id": 1, "generated_title": "x"}])
    monkeypatch.setattr(mod, "run_step5_clustering", lambda *a, **k: [])
    monkeypatch.setattr(mod, "run_step6_video", lambda *a, **k: {"clips_generated": 0, "clip_paths": []})

    result = asyncio.run(adapter.process_project_sync(str(tmp_path / "in.mp4"), str(srt)))

    assert result["status"] == "failed"
    assert result["stage"] == "EXPORT"
    assert "ffmpeg" in result["error"]


def test_adapter_happy_path_still_succeeds(adapter, monkeypatch, tmp_path):
    from backend.services import simple_pipeline_adapter as mod

    _fake_manager(monkeypatch, available=True)
    srt = tmp_path / "in.srt"
    srt.write_text(SRT, encoding="utf-8")
    monkeypatch.setattr(mod, "run_step1_outline", lambda *a, **k: [{"title": "t"}])
    monkeypatch.setattr(mod, "run_step2_timeline", lambda *a, **k: [{"id": 1}])
    monkeypatch.setattr(mod, "run_step3_scoring", lambda *a, **k: [{"id": 1, "final_score": 0.9}])
    monkeypatch.setattr(mod, "run_step4_title", lambda *a, **k: [{"id": 1, "generated_title": "x"}])
    monkeypatch.setattr(mod, "run_step5_clustering", lambda *a, **k: [{"id": "c1"}])
    monkeypatch.setattr(mod, "run_step6_video", lambda *a, **k: {"clips_generated": 1, "clip_paths": ["/x/1.mp4"]})

    class _DB:
        def close(self): pass

    monkeypatch.setattr("backend.core.database.SessionLocal", lambda: _DB())
    monkeypatch.setattr("backend.services.data_sync_service.DataSyncService",
                        lambda db: SimpleNamespace(sync_project_from_filesystem=lambda pid, d: {"success": True}))

    result = asyncio.run(adapter.process_project_sync(str(tmp_path / "in.mp4"), str(srt)))

    assert result["status"] == "succeeded"
    assert result["result"]["video_result"]["clips_generated"] == 1
    assert adapter._events[-1] == ("DONE", "processing completed")


def test_adapter_replay_mode_skips_llm_preflight(adapter, monkeypatch, tmp_path):
    """backend/eval use AUTOCLIP_LLM_CACHE_DIR translated，No needtranslatedProvidesprovider"""
    from backend.services import simple_pipeline_adapter as mod

    monkeypatch.setenv("AUTOCLIP_LLM_CACHE_DIR", str(tmp_path / "cache"))
    _fake_manager(monkeypatch, available=False)
    srt = tmp_path / "in.srt"
    srt.write_text(SRT, encoding="utf-8")
    monkeypatch.setattr(mod, "run_step1_outline", lambda *a, **k: [{"title": "t"}])
    monkeypatch.setattr(mod, "run_step2_timeline", lambda *a, **k: [{"id": 1}])
    monkeypatch.setattr(mod, "run_step3_scoring", lambda *a, **k: [])

    result = asyncio.run(adapter.process_project_sync(str(tmp_path / "in.mp4"), str(srt)))

    # translated preflight，translatedintranslated——translated preflight translatedskip
    assert result["stage"] == "ANALYZE" and "translatedSelect" in result["error"]


# ------------------------------------------------------- error surfacing ---

def test_project_response_exposes_latest_task_error(monkeypatch):
    from backend.services.project_service import ProjectService

    class Q:
        def __init__(self, rows): self.rows = rows
        def filter(self, *a, **k): return self
        def order_by(self, *a, **k): return self
        def first(self): return self.rows[0] if self.rows else None

    task = SimpleNamespace(error_message="translatedSelect（3  translatedSelect，translated 0.7）。translated「settings → model → translated」translated。")
    svc = ProjectService.__new__(ProjectService)
    svc.db = SimpleNamespace(query=lambda model: Q([task]))
    project = SimpleNamespace(id="p1", status="failed", project_metadata={})

    assert svc.latest_error_message(project) == task.error_message
    assert svc.latest_error_message(SimpleNamespace(id="p1", status="completed", project_metadata={})) is None


def test_project_response_falls_back_to_metadata_for_cli_runs():
    from backend.services.project_service import ProjectService

    class Q:
        def filter(self, *a, **k): return self
        def order_by(self, *a, **k): return self
        def first(self): return None

    svc = ProjectService.__new__(ProjectService)
    svc.db = SimpleNamespace(query=lambda model: Q())
    project = SimpleNamespace(id="p1", status=SimpleNamespace(value="failed"),
                              project_metadata={"last_error": "translatedcanuse's LLM Providesprovider"})

    assert svc.latest_error_message(project) == "translatedcanuse's LLM Providesprovider"


def test_processing_task_reads_error_field_from_adapter_result():
    """tasks/processing.py translated message，adapter return'sIs error → usertranslated「processing failed」"""
    src = (Path(__file__).resolve().parents[1] / "tasks" / "processing.py").read_text(encoding="utf-8")
    assert 'result.get("error") or result.get("message")' in src
