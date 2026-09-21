"""
EN
"""
import time
from unittest.mock import patch, MagicMock

import pytest
from backend.utils.error_handler import (
    AutoClipsException, APIError, NetworkError, ConfigurationError,
    FileIOError, ProcessingError, ValidationError,
    ErrorLevel, ErrorCategory, RetryConfig, CircuitBreaker,
    retry_with_backoff, error_context, ErrorHandler, safe_execute
)


class TestAutoClipsException:
    """EN"""
    
    def test_exception_creation(self):
        """EN"""
        error = AutoClipsException("EN", ErrorCategory.API)
        assert error.message == "EN"
        assert error.category == ErrorCategory.API
        assert error.level == ErrorLevel.ERROR
        assert error.timestamp > 0
    
    def test_exception_to_dict(self):
        """EN"""
        original_exception = ValueError("EN")
        error = AutoClipsException(
            "EN", 
            ErrorCategory.API, 
            ErrorLevel.WARNING,
            {"detail": "EN"},
            original_exception
        )
        
        error_dict = error.to_dict()
        assert error_dict["message"] == "EN"
        assert error_dict["category"] == "API"
        assert error_dict["level"] == "WARNING"
        assert error_dict["details"]["detail"] == "EN"
        assert "EN" in error_dict["original_exception"]
    
    def test_exception_str_representation(self):
        """EN"""
        error = AutoClipsException("EN", ErrorCategory.NETWORK)
        assert str(error) == "[NETWORK] EN"


class TestSpecificExceptions:
    """EN"""
    
    def test_api_error(self):
        """ENAPIEN"""
        error = APIError("APIEN", status_code=400)
        assert error.category == ErrorCategory.API
        assert error.details["status_code"] == 400
    
    def test_network_error(self):
        """EN"""
        original_exception = ConnectionError("EN")
        error = NetworkError("EN", original_exception=original_exception)
        assert error.category == ErrorCategory.NETWORK
        assert error.original_exception == original_exception
    
    def test_file_io_error(self):
        """ENIOEN"""
        error = FileIOError("EN", file_path="/test/file.txt")
        assert error.category == ErrorCategory.FILE_IO
        assert error.details["file_path"] == "/test/file.txt"
    
    def test_processing_error(self):
        """EN"""
        error = ProcessingError("EN", step="Step 1")
        assert error.category == ErrorCategory.PROCESSING
        assert error.details["step"] == "Step 1"
    
    def test_validation_error(self):
        """EN"""
        error = ValidationError("EN", field="api_key")
        assert error.category == ErrorCategory.VALIDATION
        assert error.level == ErrorLevel.WARNING
        assert error.details["field"] == "api_key"


class TestRetryConfig:
    """EN"""
    
    def test_retry_config_defaults(self):
        """EN"""
        config = RetryConfig()
        assert config.max_retries == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.exponential_base == 2.0
        assert len(config.retryable_exceptions) > 0
    
    def test_retry_config_custom_values(self):
        """EN"""
        config = RetryConfig(
            max_retries=5,
            base_delay=2.0,
            max_delay=120.0
        )
        assert config.max_retries == 5
        assert config.base_delay == 2.0
        assert config.max_delay == 120.0


class TestCircuitBreaker:
    """EN"""
    
    def test_circuit_breaker_initial_state(self):
        """EN"""
        cb = CircuitBreaker()
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0
    
    def test_circuit_breaker_successful_call(self):
        """EN"""
        cb = CircuitBreaker()
        
        def success_func():
            return "success"
        
        result = cb.call(success_func)
        assert result == "success"
        assert cb.state == "CLOSED"
    
    def test_circuit_breaker_failure_threshold(self):
        """EN"""
        cb = CircuitBreaker(failure_threshold=2)
        
        def failing_func():
            raise ValueError("EN")
        
        # EN
        with patch('time.time', return_value=1000):
            with pytest.raises(ValueError):
                cb.call(failing_func)
            assert cb.state == "CLOSED"
            assert cb.failure_count == 1
        
        # EN，EN
        with patch('time.time', return_value=1001):
            with pytest.raises(ValueError):
                cb.call(failing_func)
            assert cb.state == "OPEN"
            assert cb.failure_count == 2
    
    def test_circuit_breaker_recovery(self):
        """EN"""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=1.0)
        
        def failing_func():
            raise ValueError("EN")
        
        # EN
        with patch('time.time', return_value=1000):
            with pytest.raises(ValueError):
                cb.call(failing_func)
            assert cb.state == "OPEN"
        
        # EN，EN
        with patch('time.time', return_value=1002):  # EN
            def success_func():
                return "success"
            
            result = cb.call(success_func)
            assert result == "success"
            assert cb.state == "CLOSED"  # EN


class TestRetryDecorator:
    """EN"""
    
    def test_retry_success_on_first_try(self):
        """EN"""
        @retry_with_backoff()
        def success_func():
            return "success"
        
        result = success_func()
        assert result == "success"
    
    def test_retry_success_after_failures(self):
        """EN"""
        call_count = 0
        
        @retry_with_backoff(RetryConfig(max_retries=2, base_delay=0.1))
        def failing_then_success():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise NetworkError("EN")
            return "success"
        
        result = failing_then_success()
        assert result == "success"
        assert call_count == 3
    
    def test_retry_max_attempts_exceeded(self):
        """EN"""
        @retry_with_backoff(RetryConfig(max_retries=1, base_delay=0.1))
        def always_failing():
            raise APIError("APIEN")
        
        with pytest.raises(APIError):
            always_failing()


class TestErrorContext:
    """EN"""
    
    def test_error_context_no_exception(self):
        """EN"""
        with error_context(ErrorCategory.API):
            result = "success"
        
        assert result == "success"
    
    def test_error_context_with_exception(self):
        """EN"""
        with pytest.raises(APIError):
            with error_context(ErrorCategory.API):
                raise ValueError("EN")
    
    def test_error_context_preserves_auto_clips_exception(self):
        """ENAutoClipsException"""
        original_error = APIError("APIEN")
        with pytest.raises(APIError) as exc_info:
            with error_context(ErrorCategory.NETWORK):
                raise original_error
        
        assert exc_info.value == original_error


class TestErrorHandler:
    """EN"""
    
    def test_error_handler_initialization(self):
        """EN"""
        handler = ErrorHandler()
        assert len(handler.error_log) == 0
        assert len(handler.circuit_breakers) == 0
    
    def test_error_handler_handle_error(self):
        """EN"""
        handler = ErrorHandler()
        error = APIError("ENAPIEN")
        
        with patch('logging.Logger.error') as mock_logger:
            handler.handle_error(error, "EN")
            
            assert len(handler.error_log) == 1
            assert handler.error_log[0] == error
            mock_logger.assert_called_once()
    
    def test_error_handler_get_circuit_breaker(self):
        """EN"""
        handler = ErrorHandler()
        
        cb1 = handler.get_circuit_breaker("test")
        cb2 = handler.get_circuit_breaker("test")
        
        assert cb1 is cb2  # EN
        assert len(handler.circuit_breakers) == 1
    
    def test_error_handler_get_error_summary(self):
        """EN"""
        handler = ErrorHandler()
        
        # EN
        summary = handler.get_error_summary()
        assert summary["total_errors"] == 0
        
        # EN
        handler.handle_error(APIError("APIEN1"))
        handler.handle_error(NetworkError("EN"))
        handler.handle_error(APIError("APIEN2"))
        
        summary = handler.get_error_summary()
        assert summary["total_errors"] == 3
        assert summary["error_counts"]["API"] == 2
        assert summary["error_counts"]["NETWORK"] == 1
        assert summary["latest_error"] is not None
    
    def test_error_handler_clear_error_log(self):
        """EN"""
        handler = ErrorHandler()
        handler.handle_error(APIError("EN"))
        assert len(handler.error_log) == 1
        
        handler.clear_error_log()
        assert len(handler.error_log) == 0


class TestSafeExecute:
    """EN"""
    
    def test_safe_execute_success(self):
        """EN"""
        def success_func():
            return "success"
        
        result = safe_execute(success_func, context="EN")
        assert result == "success"
    
    def test_safe_execute_with_retry(self):
        """EN"""
        call_count = 0
        
        def failing_then_success():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise NetworkError("EN")
            return "success"
        
        retry_config = RetryConfig(max_retries=1, base_delay=0.1)
        result = safe_execute(failing_then_success, context="EN", retry_config=retry_config)
        assert result == "success"
        assert call_count == 2
    
    def test_safe_execute_handles_auto_clips_exception(self):
        """ENAutoClipsException"""
        def raise_auto_clips_error():
            raise APIError("APIEN")
        
        with pytest.raises(APIError):
            safe_execute(raise_auto_clips_error, context="EN")
    
    def test_safe_execute_converts_generic_exception(self):
        """EN"""
        def raise_generic_error():
            raise ValueError("EN")
        
        with pytest.raises(AutoClipsException) as exc_info:
            safe_execute(raise_generic_error, context="EN")
        
        assert exc_info.value.category == ErrorCategory.SYSTEM
        assert "EN" in str(exc_info.value)


# EN
def test_error_level_enum():
    """EN"""
    assert ErrorLevel.DEBUG.value == "DEBUG"
    assert ErrorLevel.ERROR.value == "ERROR"
    assert ErrorLevel.CRITICAL.value == "CRITICAL"


def test_error_category_enum():
    """EN"""
    assert ErrorCategory.API.value == "API"
    assert ErrorCategory.NETWORK.value == "NETWORK"
    assert ErrorCategory.CONFIGURATION.value == "CONFIGURATION"


if __name__ == '__main__':
    pytest.main([__file__]) 