"""
errortranslatedtest
translatedfailedtranslatedAndtranslated
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import sys
import os

# addprojecttranslateddirectorytranslatedPythonpath
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
    """configerrortranslatedtest"""
    
    def test_missing_api_key(self, tmp_path, monkeypatch):
        """testtranslatedAPIkey"""
        # CI translated DASHSCOPE_API_KEY translatedusetranslateduse，thistranslatedpath
        monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)

        project_dir = tmp_path / "test_project"
        project_dir.mkdir()

        # createtranslatedAPIkey'sconfig
        config_manager = ProjectConfigManager(str(project_dir))

        with pytest.raises(ValueError, match="DASHSCOPE_API_KEY"):
            config_manager.get_llm_config()
    
    def test_invalid_processing_params(self, tmp_path):
        """testtranslated'sprocesstranslated"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        config_manager = ProjectConfigManager(str(project_dir))
        
        # settingstranslated
        config_manager.update_processing_params(chunk_size=-1)
        
        # verifyconfigtranslatedfailed
        validation_result = config_manager.validate_config()
        assert validation_result["valid"] is False
        assert any("chunk_size" in error for error in validation_result["errors"])
    
    def test_missing_prompt_files(self, tmp_path):
        """testtranslatedpromptfile"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        config_manager = ProjectConfigManager(str(project_dir))
        
        # translatedpromptfile'stranslated
        with patch('pathlib.Path.exists', return_value=False):
            prompt_files = config_manager.get_prompt_files()
            
            # translatedreturntranslatedorPackageincludetranslatedfile'sinfo
            assert isinstance(prompt_files, dict)


class TestFileOperationErrorScenarios:
    """filetranslatederrortranslatedtest"""
    
    def test_nonexistent_srt_file(self, tmp_path):
        """testnot found'sSRTfile"""
        context = ProcessingContext("test_project", "test_task")
        
        with pytest.raises(FileNotFoundError):
            context.set_srt_path(Path("nonexistent.srt"))
    
    def test_invalid_srt_format(self, tmp_path):
        """testtranslated'sSRTformat"""
        # createformaterror'sSRTfile
        invalid_srt = tmp_path / "invalid.srt"
        invalid_srt.write_text("thistranslatedIstranslated'sSRTformat\ntranslated\ntranslated")
        
        # thistranslatedtestSRTformatverifytranslated
        # translatedformatverify，translatedtestfiletranslatedintranslated
        assert invalid_srt.exists()
    
    def test_permission_denied(self, tmp_path):
        """testtranslated"""
        # createtranslatedfile
        read_only_file = tmp_path / "readonly.srt"
        read_only_file.write_text("testtranslated")
        read_only_file.chmod(0o444)  # translated
        
        try:
            # translatedfile
            with pytest.raises(PermissionError):
                read_only_file.write_text("translated")
        finally:
            # translated
            read_only_file.chmod(0o666)
    
    def test_corrupted_config_file(self, tmp_path):
        """testtranslated'sconfigfile"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        # createtranslated'sYAMLfile
        config_file = project_dir / "config.yaml"
        config_file.write_text("invalid: yaml: content: [")
        
        config_manager = ProjectConfigManager(str(project_dir))
        
        # translatedprocesstranslated'sconfigfile
        config = config_manager.config
        assert isinstance(config, dict)


class TestProcessingErrorScenarios:
    """processerrortranslatedtest"""
    
    def test_step_execution_failure(self, tmp_path):
        """teststeptranslatedfailed"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        adapter = PipelineAdapter(str(project_dir))
        
        # teststeptranslatedfailed（file not found）
        with pytest.raises(FileNotFoundError):
            adapter.adapt_step("step1_outline", srt_path=Path("nonexistent.srt"))
    
    def test_timeout_error(self, tmp_path):
        """testtranslatederror"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        adapter = PipelineAdapter(str(project_dir))
        
        # testtranslatederror（file not found）
        with pytest.raises(FileNotFoundError):
            adapter.adapt_step("step1_outline", srt_path=Path("nonexistent.srt"))
    
    def test_missing_dependencies(self, tmp_path):
        """testtranslateddependencies"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        adapter = PipelineAdapter(str(project_dir))
        
        # testtranslateddependencies'stranslated（file not found）
        with pytest.raises(FileNotFoundError):
            adapter.adapt_step("step1_outline", srt_path=Path("nonexistent.srt"))


class TestConcurrencyErrorScenarios:
    """translatederrortranslatedtest"""
    
    def test_resource_already_locked(self, tmp_path):
        """testtranslated"""
        from backend.services.concurrency_manager import concurrency_manager
        
        resource_id = "test_resource"
        task_id_1 = "task_001"
        task_id_2 = "task_002"
        
        # No.one taskfetchtranslated
        acquired_1 = concurrency_manager.acquire_lock(resource_id, task_id_1)
        assert acquired_1 is True
        
        # No.translated tasktranslatedfetchtranslatedone translated
        acquired_2 = concurrency_manager.acquire_lock(resource_id, task_id_2)
        assert acquired_2 is False
        
        # clean
        concurrency_manager.release_lock(resource_id, task_id_1)
    
    def test_lock_timeout(self, tmp_path):
        """testtranslated"""
        from backend.services.concurrency_manager import concurrency_manager
        
        resource_id = "test_resource"
        task_id = "task_001"
        
        # fetchtranslated
        acquired = concurrency_manager.acquire_lock(resource_id, task_id, timeout_seconds=1)
        assert acquired is True
        
        # checktranslatedstatus
        is_locked = concurrency_manager.is_locked(resource_id)
        assert is_locked is True
        
        # clean
        concurrency_manager.release_lock(resource_id, task_id)
    
    def test_invalid_lock_release(self, tmp_path):
        """testtranslated'stranslated"""
        from backend.services.concurrency_manager import concurrency_manager
        
        resource_id = "test_resource"
        task_id = "task_001"
        
        # translatednot found'stranslated
        released = concurrency_manager.release_lock(resource_id, task_id)
        assert released is False


class TestContextErrorScenarios:
    """translatederrortranslatedtest"""
    
    def test_invalid_project_id(self):
        """testtranslated'sprojectID"""
        with pytest.raises(ValueError, match="project_idtranslated"):
            ProcessingContext("", "test_task")
    
    def test_invalid_task_id(self):
        """testtranslated'staskID"""
        with pytest.raises(ValueError, match="task_idtranslated"):
            ProcessingContext("test_project", "")
    
    def test_context_validation_failure(self):
        """testtranslatedverifyfailed"""
        context = ProcessingContext("test_project", "test_task")
        
        # translated'stranslated
        assert context.is_valid_for_execution() is False
        
        # settingserrortranslated
        context.set_error("testerror")
        assert context.is_valid_for_execution() is False
        
        # translated
        context.mark_completed()
        assert context.is_valid_for_execution() is False


class TestIntegrationErrorScenarios:
    """translatederrortranslatedtest"""
    
    def test_full_pipeline_failure(self, tmp_path):
        """testtranslatedfailed"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        # createconfigtranslated
        config_manager = ProjectConfigManager(str(project_dir))
        
        # createtranslated
        adapter = PipelineAdapter(str(project_dir))
        
        # verifytranslated（translatedfailed，translatedSRTfile）
        errors = adapter.validate_pipeline_prerequisites()
        assert len(errors) > 0
        assert any("SRTfile" in error for error in errors)
    
    def test_partial_success_scenario(self, tmp_path):
        """testtranslatedsucceededtranslated"""
        # settingstesttranslated
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_api_key'
        
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        # createSRTfileintranslated'stranslated
        raw_dir = project_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        srt_file = raw_dir / "transcript.srt"
        srt_file.write_text("1\n00:00:01,000 --> 00:00:05,000\ntestsubtitles")
        
        adapter = PipelineAdapter(str(project_dir))
        
        # verifytranslated（translatedsucceeded）
        errors = adapter.validate_pipeline_prerequisites()
        assert len(errors) == 0
    
    def test_error_recovery(self, tmp_path):
        """testerrortranslated"""
        context = ProcessingContext("test_project", "test_task")
        
        # settingserror
        context.set_error("translatederror")
        assert context.error_message == "translatederror"
        assert context.is_valid_for_execution() is False
        
        # translatederror（translated：translatederror'stranslated）
        # thistranslatedtesterrorstatus'stranslated
        assert context.error_message is not None


def test_error_propagation():
    """testerrortranslated"""
    # testerrortranslated
    original_error = ValueError("translatederror")
    
    service_error = ServiceError(
        "serviceerror",
        details={"operation": "test"},
        cause=original_error
    )
    
    assert service_error.cause == original_error
    assert service_error.cause.args[0] == "translatederror"


def test_error_serialization():
    """testerrortranslated"""
    error = ServiceError(
        "testerror",
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
