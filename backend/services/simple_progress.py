"""
translated'sprogressservice - translated + translated
Based ontranslated's"translated"translated
"""

import time
import json
import logging
from typing import List, Tuple, Optional, Dict, Any
import sqlite3
import threading
import os
try:
    import redis  # canSelectdependencies
except Exception:
    redis = None

logger = logging.getLogger(__name__)

# translated - translated'sprojecttranslated
STAGES: List[Tuple[str, int]] = [
    ("INGEST", 10),        # download/translated
    ("SUBTITLE", 15),      # subtitles/translated
    ("ANALYZE", 20),       # translated/translated
    ("HIGHLIGHT", 25),     # translated/translated
    ("EXPORT", 20),        # export/translated
    ("DONE", 10),          # translated/translated
]

# translated
WEIGHTS = {name: w for name, w in STAGES}
# translated
ORDER = [name for name, _ in STAGES]

class ProgressStore:
    def save(self, project_id: str, stage: str, percent: int, message: str, ts: int):
        raise NotImplementedError

    def get(self, project_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    def delete(self, project_id: str):
        raise NotImplementedError

    def get_many(self, project_ids: List[str]) -> List[Dict[str, Any]]:
        return [s for pid in project_ids if (s := self.get(pid))]


class RedisProgressStore(ProgressStore):
    def __init__(self, redis_client):
        self.r = redis_client

    def save(self, project_id: str, stage: str, percent: int, message: str, ts: int):
        self.r.hset(f"progress:project:{project_id}", mapping={
            "stage": stage,
            "percent": str(percent),
            "message": message,
            "ts": str(ts)
        })
        payload = {"project_id": project_id, "stage": stage, "percent": percent, "message": message, "ts": ts}
        try:
            self.r.publish(f"progress:project:{project_id}", json.dumps(payload))
        except Exception:
            pass

    def get(self, project_id: str) -> Optional[Dict[str, Any]]:
        h = self.r.hgetall(f"progress:project:{project_id}")
        if not h:
            return None
        return {
            "project_id": project_id,
            "stage": h.get("stage", ""),
            "percent": int(h.get("percent", 0)),
            "message": h.get("message", ""),
            "ts": int(h.get("ts", 0))
        }

    def delete(self, project_id: str):
        self.r.delete(f"progress:project:{project_id}")


class SqliteProgressStore(ProgressStore):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS progress_snapshots (
                project_id TEXT PRIMARY KEY,
                stage TEXT,
                percent INTEGER,
                message TEXT,
                ts INTEGER
            )
            """
        )
        self._conn.commit()

    def save(self, project_id: str, stage: str, percent: int, message: str, ts: int):
        with self._lock:
            self._conn.execute(
                "REPLACE INTO progress_snapshots (project_id, stage, percent, message, ts) VALUES (?, ?, ?, ?, ?)",
                (project_id, stage, int(percent), message, int(ts))
            )
            self._conn.commit()

    def get(self, project_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            cur = self._conn.execute(
                "SELECT stage, percent, message, ts FROM progress_snapshots WHERE project_id = ?",
                (project_id,)
            )
            row = cur.fetchone()
        if not row:
            return None
        stage, percent, message, ts = row
        return {
            "project_id": project_id,
            "stage": stage or "",
            "percent": int(percent or 0),
            "message": message or "",
            "ts": int(ts or 0)
        }

    def delete(self, project_id: str):
        with self._lock:
            self._conn.execute("DELETE FROM progress_snapshots WHERE project_id = ?", (project_id,))
            self._conn.commit()

    def get_many(self, project_ids: List[str]) -> List[Dict[str, Any]]:
        if not project_ids:
            return []
        placeholders = ",".join(["?"] * len(project_ids))
        with self._lock:
            cur = self._conn.execute(
                f"SELECT project_id, stage, percent, message, ts FROM progress_snapshots WHERE project_id IN ({placeholders})",
                project_ids
            )
            rows = cur.fetchall()
        results = []
        for pid, stage, percent, message, ts in rows:
            results.append({
                "project_id": pid,
                "stage": stage or "",
                "percent": int(percent or 0),
                "message": message or "",
                "ts": int(ts or 0)
            })
        return results


# Selectselecttranslated：DesktoptranslatedSQLite；ServertranslatedRedis，failedtranslatedSQLite
store: ProgressStore
try:
    from backend.core.desktop_config import is_desktop_mode, get_desktop_paths
    if is_desktop_mode():
        paths = get_desktop_paths()
        db_file = os.path.join(str(paths.data_dir), "progress.db")
        store = SqliteProgressStore(db_file)
        logger.info(f"translateduseSQLiteprogresstranslated: {db_file}")
    else:
        if redis is None:
            raise RuntimeError("redis translatedinstall")
        # fromtranslatedfetchRedis URL，defaulttranslatedlocaltranslated
        redis_url = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
        r_client = redis.Redis.from_url(redis_url, decode_responses=True)
        r_client.ping()
        store = RedisProgressStore(r_client)
        logger.info("ServertranslateduseRedisprogresstranslated")
except Exception as e:
    # translatedSQLite
    try:
        # translatedusetranslateddirectory；translatedcanusetranslatedprojecttranslated data directory
        db_file = None
        try:
            from backend.core.desktop_config import get_desktop_paths
            db_file = os.path.join(str(get_desktop_paths().data_dir), "progress.db")
        except Exception:
            from pathlib import Path
            db_file = str((Path(__file__).parent.parent.parent / 'data' / 'progress.db').resolve())
        store = SqliteProgressStore(db_file)
        logger.warning(f"Redistranslatedcanuseortranslatedinstall，translatedSQLiteprogresstranslated: {db_file}，translated: {e}")
    except Exception as e2:
        logger.error(f"translatedprogresstranslatedfailed: {e2}")
        store = None


def compute_percent(stage: str, subpercent: Optional[float] = None) -> int:
    """
    translated'stranslated
    
    Args:
        stage: Current Stagetranslated
        subpercent: translatedprogresstranslated (0-100)，canSelect
        
    Returns:
        translatedprogresstranslated (0-100)
    """
    # translated
    done = 0
    for s in ORDER:
        if s == stage:
            break
        done += WEIGHTS[s]
    
    # Current Stage
    cur = WEIGHTS.get(stage, 0)
    
    if subpercent is None:
        # translated，translatedCurrent Stagetranslated
        return min(100, done + cur) if stage == "DONE" else min(99, done)
    else:
        # translatedprogress，bytranslated
        subpercent = max(0, min(100, subpercent))
        return min(99, done + int(cur * subpercent / 100))


# processtranslated（CLI / MCP usetranslatedprogress；API processusetranslated）
_listeners: List[Any] = []


def add_progress_listener(fn) -> None:
    """translatedprocesstranslatedprogresstranslated：fn(payload: dict)。payload include project_id / stage / percent / message / ts。"""
    if fn not in _listeners:
        _listeners.append(fn)


def remove_progress_listener(fn) -> None:
    try:
        _listeners.remove(fn)
    except ValueError:
        pass


def emit_progress(project_id: str, stage: str, message: str = "", subpercent: Optional[float] = None):
    """
    translatedprogresstranslated
    
    Args:
        project_id: projectID
        stage: Current Stage
        message: progresstranslated
        subpercent: translatedprogresstranslated，canSelect
    """
    percent = compute_percent(stage, subpercent)
    payload = {
        "project_id": project_id,
        "stage": stage,
        "percent": percent,
        "message": message,
        "ts": int(time.time())
    }

    for fn in list(_listeners):
        try:
            fn(payload)
        except Exception as e:  # noqa: BLE001
            logger.debug(f"progresstranslated: {e}")

    if not store:
        logger.warning("progresstranslated，skipprogresstranslated")
        return
    
    try:
        store.save(project_id, stage, percent, message, payload["ts"])
        logger.info(f"progresstranslated: {project_id} - {stage} ({percent}%) - {message}")
    except Exception as e:
        logger.error(f"translatedprogresstranslatedfailed: {e}")


def get_progress_snapshot(project_id: str) -> Optional[Dict[str, Any]]:
    """
    fetchprojectprogresstranslated
    
    Args:
        project_id: projectID
        
    Returns:
        progresstranslated，iftranslatednot foundreturnNone
    """
    if not store:
        return None
        
    try:
        return store.get(project_id)
    except Exception as e:
        logger.error(f"fetchprogresstranslatedfailed: {e}")
        return None


def get_multiple_progress_snapshots(project_ids: List[str]) -> List[Dict[str, Any]]:
    """
    translatedfetchmulti project'sprogresstranslated
    
    Args:
        project_ids: projectIDlist
        
    Returns:
        progresstranslatedlist
    """
    if not store:
        return []
    try:
        return store.get_many(project_ids)
    except Exception as e:
        logger.error(f"translatedfetchprogresstranslatedfailed: {e}")
        return []


def clear_progress(project_id: str):
    """
    translatedprojectprogresstranslated
    
    Args:
        project_id: projectID
    """
    if not store:
        return
    try:
        store.delete(project_id)
        logger.info(f"translatedprojectprogresstranslated: {project_id}")
    except Exception as e:
        logger.error(f"translatedprogresstranslatedfailed: {e}")


# translated（usetranslated）
STAGE_NAMES = {
    "INGEST": "translated",
    "SUBTITLE": "subtitlesprocess", 
    "ANALYZE": "translated",
    "HIGHLIGHT": "translated",
    "EXPORT": "videoexport",
    "DONE": "processing completed"
}

def get_stage_display_name(stage: str) -> str:
    """fetchtranslated'stranslated"""
    return STAGE_NAMES.get(stage, stage)
