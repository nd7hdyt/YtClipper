"""
translatedoneerrorprocessingtranslated V2
usetranslated'serrortranslatedformat，Providestranslated'serrorprocessAndusertranslated
"""

import logging
import traceback
import time
import asyncio
import functools
from typing import Union
from contextlib import contextmanager
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from ..utils.error_handler import AutoClipsException, ErrorCategory, ErrorLevel
from ..services.exceptions import ServiceError
from ..utils.error_response import (
    create_error_response, 
    create_validation_error_response,
    create_exception_error_response,
    create_http_exception_response,
    ErrorCode,
    ErrorLevel as ResponseErrorLevel
)

logger = logging.getLogger(__name__)


def get_request_id(request: Request) -> str:
    """fetchtranslatedID"""
    return getattr(request.state, 'request_id', None) or str(uuid.uuid4())


def log_error(error: Exception, request: Request, context: str = None):
    """translatederrorlogs"""
    request_id = get_request_id(request)
    error_info = {
        "request_id": request_id,
        "path": request.url.path,
        "method": request.method,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context,
        "traceback": traceback.format_exc()
    }
    
    logger.error(f"Error in {context or 'unknown context'}: {error}", extra=error_info)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """translatedprocesstranslated"""
    request_id = get_request_id(request)
    
    # translated
    log_error(exc, request, "GlobalExceptionHandler")
    
    # translatedreturntranslated'serrortranslated
    if isinstance(exc, AutoClipsException):
        return handle_autoclips_exception(exc, request_id)
    elif isinstance(exc, ServiceError):
        return handle_service_error(exc, request_id)
    elif isinstance(exc, HTTPException):
        return create_http_exception_response(exc, request_id)
    elif isinstance(exc, RequestValidationError):
        return create_validation_error_response(exc.errors(), request_id)
    elif isinstance(exc, StarletteHTTPException):
        return create_http_exception_response(HTTPException(exc.status_code, exc.detail), request_id)
    else:
        return create_exception_error_response(exc, request_id, "GlobalExceptionHandler")


def handle_autoclips_exception(exc: AutoClipsException, request_id: str = None) -> JSONResponse:
    """processAutoClipsException"""
    # translatederrortranslated'serrortranslated
    error_code_mapping = {
        ErrorCategory.CONFIGURATION: ErrorCode.INVALID_PARAMETER,
        ErrorCategory.NETWORK: ErrorCode.NETWORK_ERROR,
        ErrorCategory.API: ErrorCode.EXTERNAL_API_ERROR,
        ErrorCategory.FILE_IO: ErrorCode.FILE_PROCESSING_ERROR,
        ErrorCategory.PROCESSING: ErrorCode.PROCESSING_ERROR,
        ErrorCategory.VALIDATION: ErrorCode.VALIDATION_ERROR,
        ErrorCategory.SYSTEM: ErrorCode.INTERNAL_SERVER_ERROR,
    }
    
    error_code = error_code_mapping.get(exc.category, ErrorCode.UNKNOWN_ERROR)
    
    # translatederrortranslatederrortranslated
    level_mapping = {
        ErrorLevel.DEBUG: ResponseErrorLevel.INFO,
        ErrorLevel.INFO: ResponseErrorLevel.INFO,
        ErrorLevel.WARNING: ResponseErrorLevel.WARNING,
        ErrorLevel.ERROR: ResponseErrorLevel.ERROR,
        ErrorLevel.CRITICAL: ResponseErrorLevel.CRITICAL,
    }
    
    level = level_mapping.get(exc.level, ResponseErrorLevel.ERROR)
    
    return create_error_response(
        error_code=error_code,
        message=exc.message,
        user_message=exc.user_message,
        details=exc.details,
        level=level,
        request_id=request_id
    )


def handle_service_error(exc: ServiceError, request_id: str = None) -> JSONResponse:
    """processServiceError"""
    # translatedserviceerrortranslated'serrortranslated
    error_code_mapping = {
        "CONFIGURATION_ERROR": ErrorCode.INVALID_PARAMETER,
        "NETWORK_ERROR": ErrorCode.NETWORK_ERROR,
        "API_ERROR": ErrorCode.EXTERNAL_API_ERROR,
        "FILE_IO_ERROR": ErrorCode.FILE_PROCESSING_ERROR,
        "PROCESSING_ERROR": ErrorCode.PROCESSING_ERROR,
        "VALIDATION_ERROR": ErrorCode.VALIDATION_ERROR,
        "SYSTEM_ERROR": ErrorCode.INTERNAL_SERVER_ERROR,
    }
    
    error_code = error_code_mapping.get(exc.error_code.value, ErrorCode.UNKNOWN_ERROR)
    
    return create_error_response(
        error_code=error_code,
        message=exc.message,
        details=exc.details,
        request_id=request_id
    )


# translated：translatederrorprocess
def handle_errors(error_category: ErrorCategory = ErrorCategory.SYSTEM):
    """errorprocesstranslated"""
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except AutoClipsException:
                # translatedAutoClipsException
                raise
            except ServiceError:
                # translatedServiceError
                raise
            except Exception as e:
                # translatedAutoClipsException
                raise AutoClipsException(
                    message=str(e),
                    category=error_category,
                    original_exception=e
                )
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except AutoClipsException:
                # translatedAutoClipsException
                raise
            except ServiceError:
                # translatedServiceError
                raise
            except Exception as e:
                # translatedAutoClipsException
                raise AutoClipsException(
                    message=str(e),
                    category=error_category,
                    original_exception=e
                )
        
        # translatedreturntranslated'sPackagetranslated
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# translated：errortranslated
@contextmanager
def error_context(category: ErrorCategory, context_info: dict = None):
    """errortranslated"""
    try:
        yield
    except Exception as e:
        if isinstance(e, AutoClipsException):
            # translatedIstranslated，translated
            raise
        else:
            # translated
            details = context_info or {}
            details["original_exception_type"] = type(e).__name__
            
            raise AutoClipsException(
                message=str(e),
                category=category,
                details=details,
                original_exception=e
            )


# errortranslatedAndmonitor
class ErrorMonitor:
    """errormonitortranslated"""
    
    def __init__(self):
        self.error_counts = {}
        self.error_history = []
        self.max_history_size = 1000
    
    def record_error(self, error: Exception, context: str = None):
        """translatederror"""
        error_type = type(error).__name__
        key = f"{error_type}:{context or 'unknown'}"
        
        # updateerrortranslated
        self.error_counts[key] = self.error_counts.get(key, 0) + 1
        
        # translatederrortranslated
        error_record = {
            "timestamp": time.time(),
            "error_type": error_type,
            "error_message": str(error),
            "context": context,
            "traceback": traceback.format_exc()
        }
        
        self.error_history.append(error_record)
        
        # translated
        if len(self.error_history) > self.max_history_size:
            self.error_history = self.error_history[-self.max_history_size:]
    
    def get_error_stats(self) -> dict:
        """fetcherrortranslated"""
        return {
            "error_counts": self.error_counts,
            "total_errors": sum(self.error_counts.values()),
            "recent_errors": self.error_history[-10:] if self.error_history else []
        }
    
    def clear_stats(self):
        """translatedinfo"""
        self.error_counts.clear()
        self.error_history.clear()


# translatederrormonitortranslated
error_monitor = ErrorMonitor()


# errortranslated
class ErrorRecovery:
    """errortranslated"""
    
    def __init__(self):
        self.recovery_strategies = {}
    
    def register_strategy(self, error_type: type, strategy_func):
        """translated"""
        self.recovery_strategies[error_type] = strategy_func
    
    def attempt_recovery(self, error: Exception, context: str = None) -> bool:
        """translatederrortranslated"""
        error_type = type(error)
        
        if error_type in self.recovery_strategies:
            try:
                return self.recovery_strategies[error_type](error, context)
            except Exception as recovery_error:
                logger.error(f"Recovery strategy failed: {recovery_error}")
                return False
        
        return False


# translatederrortranslated
error_recovery = ErrorRecovery()


# translatedonetranslated'stranslated
def network_error_recovery(error: Exception, context: str = None) -> bool:
    """translatederrortranslated"""
    # thistranslatedcantranslated、translateduseservicetranslatedetc.translated
    logger.info(f"Attempting network error recovery for: {context}")
    return False


def file_error_recovery(error: Exception, context: str = None) -> bool:
    """fileerrortranslated"""
    # thistranslatedcantranslatedfiletranslated、usetranslatedusefileetc.translated
    logger.info(f"Attempting file error recovery for: {context}")
    return False


# translated
error_recovery.register_strategy(ConnectionError, network_error_recovery)
error_recovery.register_strategy(FileNotFoundError, file_error_recovery)
error_recovery.register_strategy(PermissionError, file_error_recovery)
