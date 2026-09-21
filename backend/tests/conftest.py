"""
pytestEN
ENfixturesEN
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Optional
from unittest.mock import Mock, MagicMock
import sys
import os

# ENPythonEN
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))


@pytest.fixture(scope="session")
def test_data_dir(tmp_path_factory):
    """EN"""
    return tmp_path_factory.mktemp("test_data")


@pytest.fixture
def sample_srt_file(test_data_dir):
    """ENSRTEN"""
    srt_file = test_data_dir / "sample.srt"
    srt_content = """1
00:00:01,000 --> 00:00:05,000
EN

2
00:00:05,000 --> 00:00:10,000
EN

3
00:00:10,000 --> 00:00:15,000
EN
"""
    srt_file.write_text(srt_content, encoding='utf-8')
    return srt_file


@pytest.fixture
def mock_db_session():
    """EN"""
    session = Mock()
    session.commit = Mock()
    session.rollback = Mock()
    session.close = Mock()
    return session


@pytest.fixture
def mock_task_repository():
    """EN"""
    mock_repo = Mock()
    mock_task = Mock()
    mock_task.id = "test_task_001"
    mock_task.project_id = "test_project"
    mock_task.status = Mock(value="pending")
    mock_task.progress = 0.0
    mock_task.metadata = {}
    mock_repo.create.return_value = mock_task
    mock_repo.get_by_id.return_value = mock_task
    return mock_repo


@pytest.fixture
def temp_project_dir(tmp_path):
    """EN"""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir


@pytest.fixture
def mock_srt_file(tmp_path):
    """ENSRTEN"""
    srt_file = tmp_path / "test.srt"
    srt_content = """1
00:00:01,000 --> 00:00:05,000
EN

2
00:00:05,000 --> 00:00:10,000
EN
"""
    srt_file.write_text(srt_content, encoding='utf-8')
    return srt_file


@pytest.fixture
def invalid_srt_file(tmp_path):
    """ENSRTEN"""
    srt_file = tmp_path / "invalid.srt"
    srt_file.write_text("ENSRTEN")
    return srt_file


@pytest.fixture
def mock_config():
    """EN"""
    return {
        "processing_params": {
            "max_clips": 50,
            "min_duration": 10.0,
            "max_duration": 300.0
        },
        "llm": {
            "api_key": "test_api_key",
            "model_name": "qwen-plus",
            "max_retries": 3,
            "timeout_seconds": 30
        },
        "prompts": {
            "custom_paths": {}
        }
    }


@pytest.fixture
def mock_pipeline_result():
    """EN"""
    return {
        "success": True,
        "output_files": {
            "outline": "outline.json",
            "timeline": "timeline.json",
            "scoring": "scoring.json"
        },
        "statistics": {
            "total_clips": 10,
            "processed_clips": 8,
            "failed_clips": 2
        }
    }


@pytest.fixture
def mock_orchestrator_status():
    """EN"""
    return {
        "project_id": "test_project",
        "task_id": "test_task",
        "status": "running",
        "progress": 50.0,
        "current_step": "step2_timeline",
        "steps": {
            "step1_outline": {"status": "completed", "duration": 30.5},
            "step2_timeline": {"status": "running", "duration": 15.2},
            "step3_scoring": {"status": "pending", "duration": 0.0}
        },
        "error_message": None
    }


class TestDataManager:
    """EN"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.created_files = []
        self.created_dirs = []
    
    def create_srt_file(self, name: str, content: Optional[str] = None) -> Path:
        """ENSRTEN"""
        if content is None:
            content = f"""1
00:00:01,000 --> 00:00:05,000
{name} EN

2
00:00:05,000 --> 00:00:10,000
{name} EN
"""
        
        srt_file = self.base_dir / f"{name}.srt"
        srt_file.write_text(content, encoding='utf-8')
        self.created_files.append(srt_file)
        return srt_file
    
    def create_project_structure(self, project_id: str) -> Path:
        """EN"""
        project_dir = self.base_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        # EN
        subdirs = ["srt", "output", "logs", "temp"]
        for subdir in subdirs:
            (project_dir / subdir).mkdir(exist_ok=True)
            self.created_dirs.append(project_dir / subdir)
        
        self.created_dirs.append(project_dir)
        return project_dir
    
    def create_config_file(self, project_dir: Path, config: dict) -> Path:
        """EN"""
        config_file = project_dir / "config.yaml"
        import yaml
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        self.created_files.append(config_file)
        return config_file
    
    def cleanup(self):
        """EN"""
        for file_path in self.created_files:
            if file_path.exists():
                file_path.unlink()
        
        for dir_path in reversed(self.created_dirs):
            if dir_path.exists():
                shutil.rmtree(dir_path)


@pytest.fixture
def test_data_manager(tmp_path):
    """EN"""
    manager = TestDataManager(tmp_path)
    yield manager
    manager.cleanup()


def assert_file_exists(file_path: Path, description: str = ""):
    """EN"""
    assert file_path.exists(), f"EN: {file_path} {description}"


def assert_file_content(file_path: Path, expected_content: str, description: str = ""):
    """EN"""
    assert_file_exists(file_path, description)
    actual_content = file_path.read_text(encoding='utf-8')
    assert actual_content.strip() == expected_content.strip(), \
        f"EN: {file_path} {description}"


def assert_dict_contains(dict_obj: dict, expected_keys: list, description: str = ""):
    """EN"""
    for key in expected_keys:
        assert key in dict_obj, f"EN: {key} {description}"


def assert_error_contains(error: Exception, expected_message: str, description: str = ""):
    """EN"""
    assert expected_message in str(error), \
        f"EN: {expected_message} {description}" 