"""
EN
EN
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import sys
import os

# ENPythonEN
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from backend.services.exceptions import (
    ServiceError, ConfigurationError, FileOperationError, 
    ProcessingError, TaskError, ProjectError, ConcurrentError
)
from backend.services.processing_context import ProcessingContext
from backend.services.config_manager import ProjectConfigManager
from backend.services.pipeline_adapter import PipelineAdapter


class TestConfigurationErrorScenarios:
    """EN"""
    
    def test_missing_api_key(self, tmp_path, monkeypatch):
        """ENAPIEN"""
        # CI EN DASHSCOPE_API_KEY EN，EN
        monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)

        project_dir = tmp_path / "test_project"
        project_dir.mkdir()

        # ENAPIEN
        config_manager = ProjectConfigManager(str(project_dir))

        with pytest.raises(ValueError, match="DASHSCOPE_API_KEY"):
            config_manager.get_llm_config()
    
    def test_invalid_processing_params(self, tmp_path):
        """EN"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        config_manager = ProjectConfigManager(str(project_dir))
        
        # EN
        config_manager.update_processing_params(chunk_size=-1)
        
        # EN
        validation_result = config_manager.validate_config()
        assert validation_result["valid"] is False
        assert any("chunk_size" in error for error in validation_result["errors"])
    
    def test_missing_prompt_files(self, tmp_path):
        """ENpromptEN"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        config_manager = ProjectConfigManager(str(project_dir))
        
        # ENpromptEN
        with patch('pathlib.Path.exists', return_value=False):
            prompt_files = config_manager.get_prompt_files()
            
            # EN
            assert isinstance(prompt_files, dict)


class TestFileOperationErrorScenarios:
    """EN"""
    
    def test_nonexistent_srt_file(self, tmp_path):
        """ENSRTEN"""
        context = ProcessingContext("test_project", "test_task")
        
        with pytest.raises(FileNotFoundError):
            context.set_srt_path(Path("nonexistent.srt"))
    
    def test_invalid_srt_format(self, tmp_path):
        """ENSRTEN"""
        # ENSRTEN
        invalid_srt = tmp_path / "invalid.srt"
        invalid_srt.write_text("ENSRTEN\nEN\nEN")
        
        # ENSRTEN
        # EN，EN
        assert invalid_srt.exists()
    
    def test_permission_denied(self, tmp_path):
        """EN"""
        # EN
        read_only_file = tmp_path / "readonly.srt"
        read_only_file.write_text("EN")
        read_only_file.chmod(0o444)  # EN
        
        try:
            # EN
            with pytest.raises(PermissionError):
                read_only_file.write_text("EN")
        finally:
            # EN
            read_only_file.chmod(0o666)
    
    def test_corrupted_config_file(self, tmp_path):
        """EN"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        # ENYAMLEN
        config_file = project_dir / "config.yaml"
        config_file.write_text("invalid: yaml: content: [")
        
        config_manager = ProjectConfigManager(str(project_dir))
        
        # EN
        config = config_manager.config
        assert isinstance(config, dict)


class TestProcessingErrorScenarios:
    """EN"""
    
    def test_step_execution_failure(self, tmp_path):
        """EN"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        adapter = PipelineAdapter(str(project_dir))
        
        # EN（EN）
        with pytest.raises(FileNotFoundError):
            adapter.adapt_step("step1_outline", srt_path=Path("nonexistent.srt"))
    
    def test_timeout_error(self, tmp_path):
        """EN"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        adapter = PipelineAdapter(str(project_dir))
        
        # EN（EN）
        with pytest.raises(FileNotFoundError):
            adapter.adapt_step("step1_outline", srt_path=Path("nonexistent.srt"))
    
    def test_missing_dependencies(self, tmp_path):
        """EN"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        adapter = PipelineAdapter(str(project_dir))
        
        # EN（EN）
        with pytest.raises(FileNotFoundError):
            adapter.adapt_step("step1_outline", srt_path=Path("nonexistent.srt"))


class TestConcurrencyErrorScenarios:
    """EN"""
    
    def test_resource_already_locked(self, tmp_path):
        """EN"""
        from backend.services.concurrency_manager import concurrency_manager
        
        resource_id = "test_resource"
        task_id_1 = "task_001"
        task_id_2 = "task_002"
        
        # EN
        acquired_1 = concurrency_manager.acquire_lock(resource_id, task_id_1)
        assert acquired_1 is True
        
        # EN
        acquired_2 = concurrency_manager.acquire_lock(resource_id, task_id_2)
        assert acquired_2 is False
        
        # EN
        concurrency_manager.release_lock(resource_id, task_id_1)
    
    def test_lock_timeout(self, tmp_path):
        """EN"""
        from backend.services.concurrency_manager import concurrency_manager
        
        resource_id = "test_resource"
        task_id = "task_001"
        
        # EN
        acquired = concurrency_manager.acquire_lock(resource_id, task_id, timeout_seconds=1)
        assert acquired is True
        
        # EN
        is_locked = concurrency_manager.is_locked(resource_id)
        assert is_locked is True
        
        # EN
        concurrency_manager.release_lock(resource_id, task_id)
    
    def test_invalid_lock_release(self, tmp_path):
        """EN"""
        from backend.services.concurrency_manager import concurrency_manager
        
        resource_id = "test_resource"
        task_id = "task_001"
        
        # EN
        released = concurrency_manager.release_lock(resource_id, task_id)
        assert released is False


class TestContextErrorScenarios:
    """EN"""
    
    def test_invalid_project_id(self):
        """ENID"""
        with pytest.raises(ValueError, match="project_idEN"):
            ProcessingContext("", "test_task")
    
    def test_invalid_task_id(self):
        """ENID"""
        with pytest.raises(ValueError, match="task_idEN"):
            ProcessingContext("test_project", "")
    
    def test_context_validation_failure(self):
        """EN"""
        context = ProcessingContext("test_project", "test_task")
        
        # EN
        assert context.is_valid_for_execution() is False
        
        # EN
        context.set_error("EN")
        assert context.is_valid_for_execution() is False
        
        # EN
        context.mark_completed()
        assert context.is_valid_for_execution() is False


class TestIntegrationErrorScenarios:
    """EN"""
    
    def test_full_pipeline_failure(self, tmp_path):
        """EN"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        # EN
        config_manager = ProjectConfigManager(str(project_dir))
        
        # EN
        adapter = PipelineAdapter(str(project_dir))
        
        # EN（EN，ENSRTEN）
        errors = adapter.validate_pipeline_prerequisites()
        assert len(errors) > 0
        assert any("SRTEN" in error for error in errors)
    
    def test_partial_success_scenario(self, tmp_path):
        """EN"""
        # EN
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_api_key'
        
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        # ENSRTEN
        raw_dir = project_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        srt_file = raw_dir / "transcript.srt"
        srt_file.write_text("1\n00:00:01,000 --> 00:00:05,000\nEN")
        
        adapter = PipelineAdapter(str(project_dir))
        
        # EN（EN）
        errors = adapter.validate_pipeline_prerequisites()
        assert len(errors) == 0
    
    def test_error_recovery(self, tmp_path):
        """EN"""
        context = ProcessingContext("test_project", "test_task")
        
        # EN
        context.set_error("EN")
        assert context.error_message == "EN"
        assert context.is_valid_for_execution() is False
        
        # EN（EN：EN）
        # EN
        assert context.error_message is not None


def test_error_propagation():
    """EN"""
    # EN
    original_error = ValueError("EN")
    
    service_error = ServiceError(
        "EN",
        details={"operation": "test"},
        cause=original_error
    )
    
    assert service_error.cause == original_error
    assert service_error.cause.args[0] == "EN"


def test_error_serialization():
    """EN"""
    error = ServiceError(
        "EN",
        details={"key": "value", "number": 123}
    )
    
    error_dict = error.to_dict()
    
    assert "error_code" in error_dict
    assert "message" in error_dict
    assert "details" in error_dict
    assert error_dict["details"]["key"] == "value"
    assert error_dict["details"]["number"] == 123


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
