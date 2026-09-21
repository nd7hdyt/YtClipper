"""
EN
ENpytestEN
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# ENPythonEN
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from backend.services.config_manager import ProjectConfigManager, ProcessingStep
from backend.services.pipeline_adapter import PipelineAdapter
from backend.services.processing_orchestrator import ProcessingOrchestrator
from backend.services.processing_service import ProcessingService
from backend.services.processing_context import ProcessingContext
from backend.services.exceptions import ServiceError, ConfigurationError, FileOperationError, ProcessingError


class TestProjectConfigManager:
    """EN"""
    
    @pytest.fixture
    def temp_project_dir(self, tmp_path):
        """EN"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        return project_dir
    
    @pytest.fixture
    def config_manager(self, temp_project_dir):
        """EN"""
        return ProjectConfigManager(str(temp_project_dir))
    
    def test_config_manager_initialization(self, config_manager):
        """EN"""
        assert config_manager.project_id is not None
        assert config_manager.config_path.parent.exists()
    
    def test_load_default_config(self, config_manager):
        """EN"""
        # EN
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_api_key'
        
        config = config_manager.config
        # EN，EN
        assert isinstance(config, dict)
    
    def test_update_processing_params(self, config_manager):
        """EN"""
        new_params = {
            "max_clips": 50,
            "min_duration": 10.0,
            "max_duration": 300.0
        }
        
        config_manager.update_processing_params(**new_params)
        config = config_manager.config
        
        for key, value in new_params.items():
            assert config["processing_params"][key] == value
    
    def test_update_llm_config(self, config_manager):
        """ENLLMEN"""
        # EN
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_api_key'
        
        llm_config = {
            "api_key": "test_key",
            "model_name": "gpt-4",
            "max_retries": 3,
            "timeout_seconds": 30
        }
        
        config_manager.update_llm_config(**llm_config)
        config = config_manager.config
        
        # EN
        assert "llm" in config
    
    def test_export_config(self, config_manager):
        """EN"""
        # EN
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_api_key'
        
        exported = config_manager.export_config()
        # EN
        assert isinstance(exported, dict)
    
    def test_config_validation(self, config_manager):
        """EN"""
        # EN
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_api_key'
        
        # EN
        validation_result = config_manager.validate_config()
        assert isinstance(validation_result, dict)


class TestPipelineAdapter:
    """EN"""
    
    @pytest.fixture
    def temp_project_dir(self, tmp_path):
        """EN"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        return project_dir
    
    @pytest.fixture
    def mock_srt_file(self, tmp_path):
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
    def adapter(self, temp_project_dir):
        """EN"""
        return PipelineAdapter(str(temp_project_dir))
    
    def test_adapter_initialization(self, adapter):
        """EN"""
        assert adapter.project_id is not None
    
    def test_validate_pipeline_prerequisites_success(self, adapter, mock_srt_file):
        """EN"""
        # EN
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_api_key'
        
        # EN
        adapter.path_manager.ensure_directories()
        
        # ENSRTEN
        srt_target_path = adapter.path_manager.get_srt_path()
        srt_target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(mock_srt_file, srt_target_path)
        
        errors = adapter.validate_pipeline_prerequisites()
        assert len(errors) == 0
    
    def test_validate_pipeline_prerequisites_missing_srt(self, adapter):
        """EN - ENSRTEN"""
        # ENSRTEN
        adapter.path_manager.ensure_directories()
        
        errors = adapter.validate_pipeline_prerequisites()
        assert len(errors) > 0
        assert any("SRTEN" in error for error in errors)
    
    def test_validate_pipeline_prerequisites_invalid_srt(self, adapter, tmp_path):
        """EN - SRTEN"""
        # EN
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_api_key'
        
        # EN
        adapter.path_manager.ensure_directories()
        
        # ENSRTEN（EN）
        srt_target_path = adapter.path_manager.get_srt_path()
        srt_target_path.write_text("ENSRTEN")
        
        # validate_pipeline_prerequisitesEN，EN
        # EN（EN）
        errors = adapter.validate_pipeline_prerequisites()
        assert len(errors) == 0  # EN，EN
    
    def test_execute_step_success(self, adapter, mock_srt_file):
        """EN"""
        # ENadapt_stepEN
        result = adapter.adapt_step("step1_outline", srt_path=mock_srt_file)
        assert isinstance(result, dict)
        assert "srt_path" in result or "input_srt" in result
    
    def test_execute_step_failure(self, adapter, mock_srt_file):
        """EN"""
        # EN
        with pytest.raises(ValueError):
            adapter.adapt_step("invalid_step", srt_path=mock_srt_file)


class TestProcessingOrchestrator:
    """EN"""
    
    @pytest.fixture
    def temp_project_dir(self, tmp_path):
        """EN"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        return project_dir
    
    @pytest.fixture
    def mock_db_session(self):
        """EN"""
        return Mock()
    
    @pytest.fixture
    def orchestrator(self, temp_project_dir, mock_db_session):
        """EN"""
        return ProcessingOrchestrator(str(temp_project_dir), "test_task", mock_db_session)
    
    def test_orchestrator_initialization(self, orchestrator):
        """EN"""
        assert orchestrator.project_id is not None
        assert orchestrator.task_id == "test_task"
    
    def test_get_pipeline_status(self, orchestrator):
        """EN"""
        status = orchestrator.get_pipeline_status()
        assert "project_id" in status
        assert "task_id" in status
        assert "pipeline_status" in status
    
    def test_execute_step_success(self, orchestrator, tmp_path):
        """EN"""
        # ENSRTEN
        srt_file = tmp_path / "test.srt"
        srt_file.write_text("1\n00:00:01,000 --> 00:00:05,000\nEN")
        
        with patch('backend.services.processing_orchestrator.PipelineAdapter') as mock_adapter_class:
            mock_adapter = Mock()
            mock_adapter.execute_step.return_value = {"status": "completed"}
            mock_adapter_class.return_value = mock_adapter
            
            result = orchestrator.execute_step(ProcessingStep.STEP1_OUTLINE, srt_path=srt_file)
            assert result["status"] == "completed"
    
    def test_execute_step_failure(self, orchestrator, tmp_path):
        """EN"""
        srt_file = tmp_path / "test.srt"
        srt_file.write_text("1\n00:00:01,000 --> 00:00:05,000\nEN")
        
        # EN
        with patch.object(orchestrator, 'step_functions') as mock_step_functions:
            mock_step_functions.__getitem__.return_value = Mock(side_effect=Exception("EN"))
            
            with pytest.raises(Exception):
                orchestrator.execute_step(ProcessingStep.STEP1_OUTLINE, srt_path=srt_file)


class TestProcessingService:
    """EN"""
    
    @pytest.fixture
    def mock_db_session(self):
        """EN"""
        return Mock()
    
    @pytest.fixture
    def mock_task_repository(self):
        """EN"""
        mock_repo = Mock()
        mock_task = Mock()
        mock_task.id = "test_task_001"
        mock_repo.create.return_value = mock_task
        return mock_repo
    
    @pytest.fixture
    def service(self, mock_db_session, mock_task_repository):
        """EN"""
        service = ProcessingService(mock_db_session)
        service.task_repo = mock_task_repository
        return service
    
    def test_service_initialization(self, service):
        """EN"""
        assert service.db is not None
        assert service.task_repo is not None
    
    def test_start_processing_success(self, service, tmp_path):
        """EN"""
        srt_file = tmp_path / "test.srt"
        srt_file.write_text("1\n00:00:01,000 --> 00:00:05,000\nEN")
        
        with patch('backend.services.processing_service.ProcessingOrchestrator') as mock_orchestrator_class:
            mock_orchestrator = Mock()
            mock_orchestrator.execute_pipeline.return_value = {"success": True}
            mock_orchestrator_class.return_value = mock_orchestrator
            
            result = service.start_processing("test_project", srt_file)
            assert result["success"] is True
            assert "task_id" in result
    
    def test_start_processing_failure(self, service, tmp_path):
        """EN"""
        srt_file = tmp_path / "test.srt"
        srt_file.write_text("1\n00:00:01,000 --> 00:00:05,000\nEN")
        
        with patch('backend.services.processing_service.ProcessingOrchestrator') as mock_orchestrator_class:
            mock_orchestrator = Mock()
            mock_orchestrator.execute_pipeline.side_effect = ServiceError("EN")
            mock_orchestrator_class.return_value = mock_orchestrator
            
            with pytest.raises(ServiceError):
                service.start_processing("test_project", srt_file)
    
    def test_execute_single_step_success(self, service, tmp_path):
        """EN"""
        srt_file = tmp_path / "test.srt"
        srt_file.write_text("1\n00:00:01,000 --> 00:00:05,000\nEN")
        
        with patch('backend.services.processing_service.ProcessingOrchestrator') as mock_orchestrator_class:
            mock_orchestrator = Mock()
            mock_orchestrator.execute_step.return_value = {"success": True}
            mock_orchestrator_class.return_value = mock_orchestrator
            
            result = service.execute_single_step("test_project", ProcessingStep.STEP1_OUTLINE, srt_file)
            assert result["success"] is True
            assert "step" in result
    
    def test_get_processing_status(self, service):
        """EN"""
        with patch('backend.services.processing_service.ProcessingOrchestrator') as mock_orchestrator_class:
            mock_orchestrator = Mock()
            mock_orchestrator.get_pipeline_status.return_value = {"pipeline_status": {"step1_outline": {"completed": True}}}
            mock_orchestrator_class.return_value = mock_orchestrator
            
            status = service.get_processing_status("test_project", "test_task")
            assert "pipeline_status" in status


class TestProcessingContext:
    """EN"""
    
    @pytest.fixture
    def mock_db_session(self):
        """EN"""
        return Mock()
    
    @pytest.fixture
    def context(self, mock_db_session):
        """EN"""
        return ProcessingContext("test_project", "test_task", mock_db_session)
    
    def test_context_initialization(self, context):
        """EN"""
        assert context.project_id == "test_project"
        assert context.task_id == "test_task"
        assert context.is_initialized is False
        assert context.is_completed is False
    
    def test_context_validation(self, context):
        """EN"""
        # EN
        assert context.is_valid_for_execution() is False  # EN
        
        context.mark_initialized()
        assert context.is_valid_for_execution() is True
    
    def test_context_with_invalid_project_id(self, mock_db_session):
        """ENID"""
        with pytest.raises(ValueError):
            ProcessingContext("", "test_task", mock_db_session)
    
    def test_context_with_invalid_task_id(self, mock_db_session):
        """ENID"""
        with pytest.raises(ValueError):
            ProcessingContext("test_project", "", mock_db_session)
    
    def test_set_srt_path(self, context, tmp_path):
        """ENSRTEN"""
        srt_file = tmp_path / "test.srt"
        srt_file.write_text("EN")
        
        context.set_srt_path(srt_file)
        assert context.srt_path == srt_file
    
    def test_set_srt_path_nonexistent(self, context):
        """ENSRTEN"""
        with pytest.raises(FileNotFoundError):
            context.set_srt_path(Path("nonexistent.srt"))
    
    def test_context_state_management(self, context):
        """EN"""
        # EN
        assert context.is_initialized is False
        assert context.is_completed is False
        assert context.error_message is None
        
        # EN
        context.mark_initialized()
        assert context.is_initialized is True
        assert context.is_valid_for_execution() is True
        
        # EN
        context.set_error("EN")
        assert context.error_message == "EN"
        assert context.is_valid_for_execution() is False
        
        # EN
        context.mark_completed()
        assert context.is_completed is True
        assert context.is_valid_for_execution() is False
    
    def test_context_summary(self, context):
        """EN"""
        context.mark_initialized()
        context.set_debug_mode(True)
        
        summary = context.get_context_summary()
        assert "project_id" in summary
        assert "task_id" in summary
        assert "debug_mode" in summary
        assert "is_initialized" in summary
    
    def test_context_clone(self, context, tmp_path):
        """EN"""
        srt_file = tmp_path / "test.srt"
        srt_file.write_text("EN")
        context.set_srt_path(srt_file)
        context.set_debug_mode(True)
        context.mark_initialized()
        
        cloned = context.clone()
        assert cloned.project_id == context.project_id
        assert cloned.task_id == context.task_id
        assert cloned.srt_path == context.srt_path
        assert cloned.debug_mode == context.debug_mode
        assert cloned.is_initialized == context.is_initialized


class TestErrorScenarios:
    """EN"""
    
    def test_configuration_error(self):
        """EN"""
        error = ConfigurationError("EN", details={"field": "api_key"})
        assert error.error_code.value == "CONFIG_INVALID"
        assert "api_key" in error.details["field"]
    
    def test_file_operation_error(self):
        """EN"""
        error = FileOperationError("EN", file_path="/invalid/path")
        assert error.error_code.value == "FILE_NOT_FOUND"
        assert error.details["file_path"] == "/invalid/path"
    
    def test_processing_error(self):
        """EN"""
        error = ProcessingError("EN", step_name="step1_outline")
        assert error.error_code.value == "PROCESSING_FAILED"
        assert error.details["step_name"] == "step1_outline"
    
    def test_error_to_dict(self):
        """EN"""
        error = ServiceError("EN", details={"key": "value"})
        error_dict = error.to_dict()
        assert "error_code" in error_dict
        assert "message" in error_dict
        assert "details" in error_dict


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


def test_integration_basic_flow(test_data_dir, sample_srt_file):
    """EN"""
    # EN
    import os
    os.environ['DASHSCOPE_API_KEY'] = 'test_api_key'
    
    # EN
    project_dir = test_data_dir / "integration_project"
    project_dir.mkdir()
    
    # EN
    config_manager = ProjectConfigManager(str(project_dir))
    config = config_manager.config
    assert isinstance(config, dict)
    
    # EN
    adapter = PipelineAdapter(str(project_dir))
    # ENSRTEN
    project_raw_dir = project_dir / "raw"
    project_raw_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(sample_srt_file, project_raw_dir / "transcript.srt")
    
    # EN
    errors = adapter.validate_pipeline_prerequisites()
    assert len(errors) == 0


def test_error_handling_scenarios():
    """EN"""
    # EN
    with pytest.raises(ConfigurationError):
        raise ConfigurationError("EN")
    
    # EN
    with pytest.raises(FileOperationError):
        raise FileOperationError("EN", file_path="/invalid/path")
    
    # EN
    with pytest.raises(ProcessingError):
        raise ProcessingError("EN", step_name="step1")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])