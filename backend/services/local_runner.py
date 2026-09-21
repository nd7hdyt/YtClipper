"""
localtranslated：translated FastAPI、translated Celery，intranslatedprocesstranslated onetranslatedvideotranslated。

translated `autoclip` CLI（backend/cli.py）And MCP server（backend/mcp_server.py）translateduse。
translateduse'sIstranslatedinuse's `SimplePipelineAdapter`，Artifactsdirectory、metadata、SQLite translated
translatedAndtranslateduseonetranslated——CLI translated'stranslated，translatedusetranslated。

translated：`configure_environment()` translatedin import translated `backend.core.database` translatedcall，
translated SQLAlchemy engine in import translatedby `DATABASE_URL` translated。
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import platform
import shutil
import sys
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

PROVIDER_CHOICES = ("dashscope", "openai", "gemini", "siliconflow", "ollama", "lmstudio")


# ---------------------------------------------------------------- environment ---
def default_app_dir() -> Path:
    """andtranslateduseonetranslated'stranslateddirectory：mac translated ~/Library/Application Support/AutoClip。"""
    env = os.getenv("AUTOCLIP_DATA_DIR") or os.getenv("AUTOCLIP_APP_DIR")
    if env:
        return Path(env).expanduser()
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "AutoClip"
    if system == "Windows":
        base = os.getenv("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        return Path(base) / "AutoClip"
    xdg = os.getenv("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(xdg) / "AutoClip"


def configure_environment(data_dir: Optional[Path] = None, quiet: bool = True) -> Path:
    """
    translateddirectory / database / logstranslated。returntranslateddirectory。
    translatedin import backend.core.database translatedcall。
    """
    target = (data_dir or default_app_dir()).expanduser()
    target.mkdir(parents=True, exist_ok=True)
    (target / "logs").mkdir(parents=True, exist_ok=True)
    os.environ["AUTOCLIP_APP_DIR"] = str(target)
    os.environ["AUTOCLIP_DATA_DIR"] = str(target)
    os.environ.setdefault("DATABASE_URL", f"sqlite:///{target / 'autoclip.db'}")
    os.environ.setdefault("LOG_FILE", str(target / "logs" / "cli.log"))
    # translatedlogstranslated；CLI defaulttranslatedprogress，logstranslatedfile
    if quiet:
        os.environ.setdefault("AUTOCLIP_CLI_QUIET", "1")
    # translated `backend.*` can import（fromtranslated cwd translated `python -m backend.cli`）
    root = str(Path(__file__).resolve().parent.parent.parent)
    if root not in sys.path:
        sys.path.insert(0, root)
    return target


def setup_logging(verbose: bool = False) -> None:
    """CLI logstranslated：filetranslated，translatedin --verbose translated backend logs。"""
    log_file = os.getenv("LOG_FILE")
    handlers: List[logging.Handler] = []
    if log_file:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        handlers.append(fh)
    if verbose:
        sh = logging.StreamHandler(sys.stderr)
        sh.setLevel(logging.INFO)
        sh.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        handlers.append(sh)
    logging.basicConfig(level=logging.INFO, handlers=handlers, force=True)
    if not verbose:
        # No.translated's WARNING translatedDo nottranslated
        for noisy in ("httpx", "openai", "urllib3", "faster_whisper", "sqlalchemy"):
            logging.getLogger(noisy).setLevel(logging.ERROR)


# ---------------------------------------------------------------- LLM config ---
@dataclass
class LLMOverride:
    provider: Optional[str] = None
    model: Optional[str] = None
    base_url: Optional[str] = None
    api_key: Optional[str] = None

    def is_empty(self) -> bool:
        return not any([self.provider, self.model, self.base_url, self.api_key])


def configure_llm(override: LLMOverride) -> Dict[str, Any]:
    """
    translatedusetranslated's provider / model / base_url / api_key。
    translated → translatedusetranslateduse's settings.json。
    translated → intranslateddirectorytranslatedonetranslated `cli-settings.json`（translatedformat，translateduser'stranslatedsettings），
          usetranslated LLMManager。returntranslated provider info。
    """
    from backend.core.llm_manager import get_llm_manager, initialize_llm_manager
    from backend.core.local_presets import resolve_provider, LOCAL_PRESETS
    from backend.core.path_utils import get_data_directory

    if override.is_empty():
        return get_llm_manager().get_current_provider_info()

    base = get_llm_manager()  # translatedusertranslatedsettingstranslated（key etc.）
    settings = dict(base.settings)
    settings.pop("llm_provider_preset", None)

    provider_in = (override.provider or settings.get("llm_provider") or "dashscope").lower()
    provider, base_url, preset = resolve_provider(provider_in, override.base_url or (settings.get("openai_base_url") if provider_in == "openai" else ""))
    settings["llm_provider"] = provider_in if preset else provider
    if provider == "openai":
        settings["openai_base_url"] = base_url
    if override.model:
        settings["model_name"] = override.model
    elif preset and LOCAL_PRESETS[preset].default_model and (override.provider or "").lower() in LOCAL_PRESETS:
        settings["model_name"] = LOCAL_PRESETS[preset].default_model
    if override.api_key is not None:
        key_field = {
            "dashscope": "dashscope_api_key", "openai": "openai_api_key",
            "gemini": "gemini_api_key", "siliconflow": "siliconflow_api_key",
        }.get(provider)
        if key_field:
            settings[key_field] = override.api_key

    cli_settings = get_data_directory() / "cli-settings.json"
    cli_settings.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
    manager = initialize_llm_manager(cli_settings)
    info = manager.get_current_provider_info()
    if not info.get("available"):
        raise RuntimeError(
            f"LLM Providesprovider {info.get('provider')} translated：translated API Key（orlocalservicetranslated）。"
            f" use --api-key / --base-url translated，ortranslatedintranslateduseSettings pageconfig。"
        )
    return info


def check_llm_connection() -> Dict[str, Any]:
    """usetranslated LLMManager translatedonetranslated，return {ok, provider, model, error}."""
    from backend.core.llm_manager import get_llm_manager
    m = get_llm_manager()
    info = m.get_current_provider_info()
    if not m.current_provider:
        return {"ok": False, **info, "error": "translatedconfig API Key / localservicetranslated"}
    base_url = info.get("base_url")
    if base_url:
        # local / translatedservicetranslatedonetranslated，translated SDK translatedonetranslated「connectfailed」
        try:
            import httpx
            from backend.core.llm_providers import is_local_url
            httpx.get(f"{base_url.rstrip('/')}/models", timeout=2.0, headers={"Authorization": "Bearer EMPTY"},
                      trust_env=not is_local_url(base_url))
        except Exception as e:  # noqa: BLE001
            from backend.core.local_presets import LOCAL_PRESETS
            preset = LOCAL_PRESETS.get(info.get("provider") or "")
            tip = f"translatedstart {preset.display_name.split('（')[0]}（{preset.docs_url}）" if preset else "translatedchecktranslatedIstranslated、serviceIstranslatedstart"
            return {"ok": False, **info, "error": f"{base_url} translatedcantranslated：{type(e).__name__}。{tip}"}
    try:
        ok = bool(m.current_provider.test_connection())
        return {"ok": ok, **info, "error": None if ok else "connecttestfailed"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, **info, "error": str(e)[:300]}


# ---------------------------------------------------------------- project ---
@dataclass
class RunRequest:
    video: Path
    srt: Optional[Path] = None
    name: Optional[str] = None
    category: str = "default"
    min_score: Optional[float] = None
    whisper_model: str = "base"
    register_db: bool = True
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))


def _write_project_json(project_dir: Path, req: RunRequest, extra: Optional[Dict[str, Any]] = None) -> None:
    """`DataSyncService` translated project.json translated；translated translated。"""
    meta = {
        "project_name": req.name or req.video.stem,
        "description": f"translated autoclip CLI from {req.video} create",
        "created_at": datetime.now().isoformat(),
        "source": {"video": str(req.video), "srt": str(req.srt) if req.srt else None, "via": "cli"},
        "video_category": req.category,
        **(extra or {}),
    }
    (project_dir / "project.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def _register_project(req: RunRequest, video_path: Path) -> None:
    """in SQLite translatedprojecttranslated，thistranslatedusetranslated。"""
    from backend.core.database import SessionLocal, create_tables
    from backend.models.project import Project, ProjectStatus, ProjectType

    create_tables()
    db = SessionLocal()
    try:
        if db.query(Project).filter(Project.id == req.project_id).first():
            return
        try:
            ptype = ProjectType(req.category)
        except ValueError:
            ptype = ProjectType.DEFAULT if hasattr(ProjectType, "DEFAULT") else list(ProjectType)[0]
        thumbnail = None
        try:
            # translated；AndUploadtranslatedonetranslateduse ffmpeg translatedonetranslated base64
            from backend.utils.thumbnail_generator import generate_project_thumbnail
            thumbnail = generate_project_thumbnail(req.project_id, video_path)
        except Exception as e:  # noqa: BLE001
            logger.debug(f"translatedfailed: {e}")
        project = Project(
            id=req.project_id,
            name=req.name or req.video.stem,
            description=f"translated autoclip CLI from {req.video.name} create",
            project_type=ptype,
            status=ProjectStatus.PROCESSING,
            video_path=str(video_path),
            thumbnail=thumbnail,
            processing_config={"source": "cli"},
            project_metadata={"source_url": None, "via": "cli", "original_video": str(req.video)},
        )
        db.add(project)
        db.commit()
    finally:
        db.close()


def _set_project_status(project_id: str, status: str, error: Optional[str] = None) -> None:
    try:
        from backend.core.database import SessionLocal
        from backend.models.project import Project, ProjectStatus

        db = SessionLocal()
        try:
            p = db.query(Project).filter(Project.id == project_id).first()
            if not p:
                return
            p.status = ProjectStatus(status)
            p.updated_at = datetime.utcnow()
            if status == "completed":
                p.completed_at = datetime.utcnow()
            if error is not None:
                # Project translated error_message translated；CLI pathtranslated Task translated，Sotranslated metadata，
                # ProjectService.latest_error_message translated，translated / translated
                meta = dict(p.project_metadata or {})
                meta["last_error"] = error[:2000]
                p.project_metadata = meta
            db.commit()
        finally:
            db.close()
    except Exception as e:  # noqa: BLE001
        logger.warning(f"updateprojectstatusfailed: {e}")


def prepare_project(req: RunRequest, link: bool = True) -> Path:
    """
    translatedprojectdirectory、 videotranslated raw/（defaulttranslated，failedtranslated；`link=False` translated）。
    return raw translated'svideopath。
    """
    from backend.core.path_utils import get_project_directory

    req.video = req.video.expanduser().resolve()
    if not req.video.exists():
        raise FileNotFoundError(f"videonot found: {req.video}")
    if req.srt:
        req.srt = req.srt.expanduser().resolve()
        if not req.srt.exists():
            raise FileNotFoundError(f"subtitlesnot found: {req.srt}")

    project_dir = get_project_directory(req.project_id)
    raw_dir = project_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / f"input{req.video.suffix.lower() or '.mp4'}"
    if not target.exists():
        linked = False
        if link:
            try:
                os.link(req.video, target)
                linked = True
            except OSError:
                linked = False
        if not linked:
            shutil.copy2(req.video, target)
    if req.srt:
        srt_target = raw_dir / "input.srt"
        if not srt_target.exists():
            shutil.copy2(req.srt, srt_target)
    _write_project_json(project_dir, req)
    if req.register_db:
        _register_project(req, target)
    return target


ProgressFn = Callable[[Dict[str, Any]], None]


def run_pipeline(req: RunRequest, video_in_raw: Path, on_progress: Optional[ProgressFn] = None) -> Dict[str, Any]:
    """translated（translated）。return adapter 'stranslated dict（status: succeeded / failed）。"""
    from backend.services.simple_progress import add_progress_listener, remove_progress_listener
    from backend.services.simple_pipeline_adapter import SimplePipelineAdapter

    import backend.pipeline.step3_scoring as step3
    # CLI translated'stranslatedSettings page；translated step3 translatedSettings page / defaulttranslated
    step3.MIN_SCORE_OVERRIDE = float(req.min_score) if req.min_score is not None else None

    srt_in_raw = video_in_raw.parent / "input.srt"
    srt_arg = str(srt_in_raw) if srt_in_raw.exists() else ""

    listener = None
    if on_progress:
        def listener(payload: Dict[str, Any]) -> None:  # noqa: E306
            if payload.get("project_id") == req.project_id:
                on_progress(payload)
        add_progress_listener(listener)
    try:
        adapter = SimplePipelineAdapter(req.project_id, task_id=f"cli-{req.project_id[:8]}")
        result = asyncio.run(adapter.process_project_sync(str(video_in_raw), srt_arg))
    finally:
        if listener:
            remove_progress_listener(listener)

    if req.register_db:
        if result.get("status") == "succeeded":
            _set_project_status(req.project_id, "completed")
        else:
            _set_project_status(req.project_id, "failed", result.get("error"))
    return result


# ---------------------------------------------------------------- results ---
def _load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return default


def normalize_score(score: Any) -> Optional[int]:
    """translated 0–1 / 0–10 translated，translatedonetranslated 0–100 translated（andfrontend ClipCard onetranslated）。"""
    if not isinstance(score, (int, float)):
        return None
    s = float(score)
    if s <= 1:
        s *= 100
    elif s <= 10:
        s *= 10
    return int(round(max(0, min(100, s))))


def summarize_project(project_id: str) -> Dict[str, Any]:
    """fromprojectdirectorytranslatedclip / collection / file path，translated CLI --json And MCP return。"""
    from backend.core.path_utils import get_projects_directory

    project_dir = get_projects_directory() / project_id
    if not project_dir.exists():
        raise FileNotFoundError(f"project not found: {project_id}")
    meta_dir = project_dir / "metadata"
    out_dir = project_dir / "output"
    project_meta = _load_json(project_dir / "project.json", {})
    if not project_meta.get("project_name"):
        row = _db_projects().get(project_id)
        if row:
            project_meta["project_name"] = row.get("name")
    clips_meta: List[Dict[str, Any]] = _load_json(meta_dir / "clips_metadata.json", [])
    collections_meta: List[Dict[str, Any]] = _load_json(meta_dir / "collections_metadata.json", [])
    video_out = _load_json(out_dir / "step6_video_output.json", {})
    clip_paths: List[str] = video_out.get("clip_paths", []) or []
    collection_paths: List[str] = video_out.get("collection_paths", []) or []

    def find_path(prefix: str, pool: List[str]) -> Optional[str]:
        for p in pool:
            if Path(p).name.startswith(prefix):
                return p
        return None

    clips = []
    for c in clips_meta:
        cid = str(c.get("id"))
        clips.append({
            "id": cid,
            "title": c.get("generated_title") or c.get("title") or c.get("outline"),
            "outline": c.get("outline"),
            "start_time": c.get("start_time"),
            "end_time": c.get("end_time"),
            "score": c.get("final_score"),
            "score_100": normalize_score(c.get("final_score")),
            "reason": c.get("recommend_reason"),
            "file": find_path(f"{cid}_", clip_paths),
        })
    clips.sort(key=lambda x: -(x["score_100"] or 0))
    collections = []
    for col in collections_meta:
        title = col.get("collection_title") or ""
        collections.append({
            "id": str(col.get("id")),
            "title": title,
            "summary": col.get("collection_summary"),
            "clip_ids": [str(x) for x in col.get("clip_ids", [])],
            "file": next((p for p in collection_paths if title and title[:12] in Path(p).name), None),
        })
    return {
        "project_id": project_id,
        "name": project_meta.get("project_name") or project_id[:8],
        "project_dir": str(project_dir),
        "clips_dir": str(out_dir / "clips"),
        "collections_dir": str(out_dir / "collections"),
        "clips": clips,
        "collections": collections,
        "counts": {"clips": len(clips), "collections": len(collections)},
        "source": project_meta.get("source"),
    }


def _db_projects() -> Dict[str, Dict[str, Any]]:
    """SQLite translated'sproject（translatedusetranslated'sprojecttranslated project.json，translated / statusinthistranslated）。translatedreturntranslated。"""
    try:
        from backend.core.database import SessionLocal
        from backend.models.project import Project

        db = SessionLocal()
        try:
            rows = db.query(Project).all()
            out = {}
            for p in rows:
                status = p.status.value if hasattr(p.status, "value") else str(p.status or "")
                out[p.id] = {"name": p.name, "status": status.lower(), "video_path": p.video_path,
                             "clips": len(getattr(p, "clips", []) or [])}
            return out
        finally:
            db.close()
    except Exception as e:  # noqa: BLE001
        logger.debug(f"translateddatabaseprojectfailed: {e}")
        return {}


def list_projects(limit: int = 50) -> List[Dict[str, Any]]:
    """translateddirectorytranslated'sproject（bytranslated），translated / statustranslated SQLite，translatedfile。"""
    from backend.core.path_utils import get_projects_directory

    db_rows = _db_projects()
    items = []
    for d in get_projects_directory().iterdir():
        if not d.is_dir():
            continue
        meta = _load_json(d / "project.json", {})
        clips = _load_json(d / "metadata" / "clips_metadata.json", [])
        video_out = _load_json(d / "output" / "step6_video_output.json", {})
        fs_status = "completed" if video_out.get("clip_paths") else ("processed" if clips else "pending")
        row = db_rows.get(d.name, {})
        items.append({
            "project_id": d.name,
            "name": meta.get("project_name") or row.get("name") or d.name[:8],
            "status": row.get("status") or fs_status,
            "clips": len(clips) or row.get("clips", 0),
            "updated_at": datetime.fromtimestamp(d.stat().st_mtime).isoformat(timespec="seconds"),
            "via": (meta.get("source") or {}).get("via") if isinstance(meta.get("source"), dict) else None,
        })
    items.sort(key=lambda x: x["updated_at"], reverse=True)
    return items[:limit]


# ---------------------------------------------------------------- doctor ---
def environment_report() -> Dict[str, Any]:
    """ffmpeg / whisper Runtime / LLM config / translateddirectoryonetranslated，translated `autoclip doctor` And MCP use。"""
    from backend.core.path_utils import get_data_directory
    from backend.services import whisper_runtime

    report: Dict[str, Any] = {"data_dir": str(get_data_directory()), "python": sys.version.split()[0]}
    try:
        from backend.utils.ffmpeg_utils import get_ffmpeg_path
        ff = get_ffmpeg_path()
        report["ffmpeg"] = {"ok": bool(ff and (Path(ff).exists() or shutil.which(ff))), "path": ff}
    except Exception as e:  # noqa: BLE001
        report["ffmpeg"] = {"ok": False, "error": str(e)}
    try:
        st = whisper_runtime.get_status()
        report["whisper"] = {"ok": st.get("status") == "installed", "status": st.get("status"), "models_dir": str(whisper_runtime.get_models_dir())}
    except Exception as e:  # noqa: BLE001
        report["whisper"] = {"ok": False, "error": str(e)}
    report["llm"] = check_llm_connection()
    return report


def as_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj) if hasattr(obj, "__dataclass_fields__") else dict(obj)
