"""ProjectResponse EN

create_project / update_project EN video_path / thumbnail，
schema EN Optional EN default，EN Pydantic EN 500。
"""
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.schemas.project import ProjectResponse


def _minimal_kwargs():
    """EN backend/api/v1/projects.py EN create_project EN"""
    return {
        "id": "test-project-id",
        "name": "test project",
        "description": None,
        "project_type": "default",
        "status": "pending",
        "source_url": "https://example.com/video",
        "source_file": None,
        "settings": {},
        "created_at": datetime(2026, 9, 7, 0, 0, 0),
        "updated_at": datetime(2026, 9, 7, 0, 0, 0),
        "completed_at": None,
    }


def test_project_response_allows_missing_video_path_and_thumbnail():
    response = ProjectResponse(**_minimal_kwargs())

    assert response.video_path is None
    assert response.thumbnail is None


def test_project_response_still_accepts_video_path_and_thumbnail():
    kwargs = _minimal_kwargs()
    kwargs["video_path"] = "/data/projects/x/raw/input.mp4"
    kwargs["thumbnail"] = "data:image/png;base64,xxx"

    response = ProjectResponse(**kwargs)

    assert response.video_path == "/data/projects/x/raw/input.mp4"
    assert response.thumbnail == "data:image/png;base64,xxx"
