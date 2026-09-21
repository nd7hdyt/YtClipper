"""
translatedoneerrortranslatedformat
Providestranslated'serrortranslatedAndusertranslated'serrortranslated
"""

from typing import Any, Dict, Optional, Union
from enum import Enum
from datetime import datetime
import traceback
import uuid
from fastapi import HTTPException
from fastapi.responses import JSONResponse


class ErrorCode(Enum):
    """errortranslated"""
    # translateduseerror
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    
    # translatederror
    INVALID_REQUEST = "INVALID_REQUEST"
    MISSING_PARAMETER = "MISSING_PARAMETER"
    INVALID_PARAMETER = "INVALID_PARAMETER"
    REQUEST_TOO_LARGE = "REQUEST_TOO_LARGE"
    UNSUPPORTED_MEDIA_TYPE = "UNSUPPORTED_MEDIA_TYPE"
    
    # translatederror
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDtranslated = "FORBIDDtranslated"
    TOKtranslated_EXPIRED = "TOKtranslated_EXPIRED"
    INVALID_CREDtranslatedTIALS = "INVALID_CREDtranslatedTIALS"
    
    # translatederror
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"
    
    # translatederror
    VALIDATION_ERROR = "VALIDATION_ERROR"
    PROCESSING_ERROR = "PROCESSING_ERROR"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    
    # translatedserviceerror
    EXTERNAL_API_ERROR = "EXTERNAL_API_ERROR"
    NETWORK_ERROR = "NETWORK_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    
    # fileprocesserror
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    UNSUPPORTED_FILE_FORMAT = "UNSUPPORTED_FILE_FORMAT"
    FILE_PROCESSING_ERROR = "FILE_PROCESSING_ERROR"


class ErrorLevel(Enum):
    """errortranslated"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ErrorResponse:
    """translatedoneerrortranslated"""
    
    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        user_message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        level: ErrorLevel = ErrorLevel.ERROR,
        request_id: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        self.error_code = error_code
        self.message = message
        self.user_message = user_message or self._get_user_friendly_message(error_code, message)
        self.details = details or {}
        self.level = level
        self.request_id = request_id or str(uuid.uuid4())
        self.timestamp = timestamp or datetime.utcnow()
    
    def _get_user_friendly_message(self, error_code: ErrorCode, message: str) -> str:
        """fetchusertranslated'serrortranslated"""
        friendly_messages = {
            ErrorCode.UNKNOWN_ERROR: "translatederror，translated",
            ErrorCode.INTERNAL_SERVER_ERROR: "servicetranslatederror，translated",
            ErrorCode.SERVICE_UNAVAILABLE: "servicetranslatedcanuse，translated",
            
            ErrorCode.INVALID_REQUEST: "translatedformattranslated，translatedchecktranslated",
            ErrorCode.MISSING_PARAMETER: "translated，translatedchecktranslated",
            ErrorCode.INVALID_PARAMETER: "translatedformattranslated，translatedchecktranslated",
            ErrorCode.REQUEST_TOO_LARGE: "translated，translated",
            ErrorCode.UNSUPPORTED_MEDIA_TYPE: "translatedsupport'sfileformat，translatedSelectselectsupport'sfiletranslated",
            
            ErrorCode.UNAUTHORIZED: "translated，translated",
            ErrorCode.FORBIDDtranslated: "translated，translated",
            ErrorCode.TOKtranslated_EXPIRED: "translated，translated",
            ErrorCode.INVALID_CREDtranslatedTIALS: "translatedinfotranslated，translatedchecktranslated",
            
            ErrorCode.RESOURCE_NOT_FOUND: "translated'stranslatednot found",
            ErrorCode.RESOURCE_ALREADY_EXISTS: "translatedin，translatedusetranslated",
            ErrorCode.RESOURCE_CONFLICT: "translated，translatedchecktranslated",
            
            ErrorCode.VALIDATION_ERROR: "translatedverifyfailed，translatedchecktranslated",
            ErrorCode.PROCESSING_ERROR: "processtranslatederror，translated",
            ErrorCode.QUOTA_EXCEEDED: "translatedusetranslated，translated",
            ErrorCode.RATE_LIMIT_EXCEEDED: "translated，translated",
            
            ErrorCode.EXTERNAL_API_ERROR: "translatedservicetranslatedcanuse，translated",
            ErrorCode.NETWORK_ERROR: "translatedconnectfailed，translatedchecktranslatedconnect",
            ErrorCode.TIMEOUT_ERROR: "translated，translated",
            
            ErrorCode.FILE_NOT_FOUND: "file not found，translatedcheckfile path",
            ErrorCode.FILE_TOO_LARGE: "filetranslated，translatedSelectselecttranslated'sfile",
            ErrorCode.UNSUPPORTED_FILE_FORMAT: "translatedsupport'sfileformat，translatedSelectselectsupport'sfiletranslated",
            ErrorCode.FILE_PROCESSING_ERROR: "fileprocessing failed，translatedcheckfiletranslated",
        }
        
        return friendly_messages.get(error_code, message)
    
    def to_dict(self) -> Dict[str, Any]:
        """translatedformat"""
        return {
            "error": {
                "code": self.error_code.value,
                "message": self.message,
                "user_message": self.user_message,
                "level": self.level.value,
                "request_id": self.request_id,
                "timestamp": self.timestamp.isoformat(),
                "details": self.details
            }
        }
    
    def to_json_response(self, status_code: int = 500) -> JSONResponse:
        """translatedJSONtranslated"""
        return JSONResponse(
            status_code=status_code,
            content=self.to_dict()
        )


def get_http_status_code(error_code: ErrorCode) -> int:
    """translatederrortranslatedfetchHTTPstatustranslated"""
    status_mapping = {
        # 4xx translatederror
        ErrorCode.INVALID_REQUEST: 400,
        ErrorCode.MISSING_PARAMETER: 400,
        ErrorCode.INVALID_PARAMETER: 400,
        ErrorCode.REQUEST_TOO_LARGE: 413,
        ErrorCode.UNSUPPORTED_MEDIA_TYPE: 415,
        ErrorCode.UNAUTHORIZED: 401,
        ErrorCode.FORBIDDtranslated: 403,
        ErrorCode.TOKtranslated_EXPIRED: 401,
        ErrorCode.INVALID_CREDtranslatedTIALS: 401,
        ErrorCode.RESOURCE_NOT_FOUND: 404,
        ErrorCode.RESOURCE_ALREADY_EXISTS: 409,
        ErrorCode.RESOURCE_CONFLICT: 409,
        ErrorCode.VALIDATION_ERROR: 422,
        ErrorCode.QUOTA_EXCEEDED: 429,
        ErrorCode.RATE_LIMIT_EXCEEDED: 429,
        ErrorCode.FILE_NOT_FOUND: 404,
        ErrorCode.FILE_TOO_LARGE: 413,
        ErrorCode.UNSUPPORTED_FILE_FORMAT: 415,
        
        # 5xx servicetranslatederror
        ErrorCode.INTERNAL_SERVER_ERROR: 500,
        ErrorCode.SERVICE_UNAVAILABLE: 503,
        ErrorCode.EXTERNAL_API_ERROR: 502,
        ErrorCode.NETWORK_ERROR: 502,
        ErrorCode.TIMEOUT_ERROR: 504,
        ErrorCode.PROCESSING_ERROR: 500,
        ErrorCode.FILE_PROCESSING_ERROR: 500,
        ErrorCode.UNKNOWN_ERROR: 500,
    }
    
    return status_mapping.get(error_code, 500)


def create_error_response(
    error_code: ErrorCode,
    message: str,
    user_message: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    level: ErrorLevel = ErrorLevel.ERROR,
    request_id: Optional[str] = None
) -> JSONResponse:
    """createtranslatederrortranslated"""
    error_response = ErrorResponse(
        error_code=error_code,
        message=message,
        user_message=user_message,
        details=details,
        level=level,
        request_id=request_id
    )
    
    status_code = get_http_status_code(error_code)
    return error_response.to_json_response(status_code)


def create_validation_error_response(
    errors: list,
    request_id: Optional[str] = None
) -> JSONResponse:
    """createverifyerrortranslated"""
    error_details = []
    for error in errors:
        if hasattr(error, 'loc') and hasattr(error, 'msg'):
            error_details.append({
                "field": ".".join(str(loc) for loc in error.loc),
                "message": error.msg,
                "type": error.type if hasattr(error, 'type') else "validation_error"
            })
        else:
            error_details.append({
                "message": str(error),
                "type": "validation_error"
            })
    
    return create_error_response(
        error_code=ErrorCode.VALIDATION_ERROR,
        message="translatedverifyfailed",
        details={"validation_errors": error_details},
        request_id=request_id
    )


def create_exception_error_response(
    exception: Exception,
    request_id: Optional[str] = None,
    context: Optional[str] = None
) -> JSONResponse:
    """fromtranslatedcreateerrortranslated"""
    # translatederrortranslated
    if isinstance(exception, FileNotFoundError):
        error_code = ErrorCode.FILE_NOT_FOUND
    elif isinstance(exception, PermissionError):
        error_code = ErrorCode.FORBIDDtranslated
    elif isinstance(exception, ValueError):
        error_code = ErrorCode.INVALID_PARAMETER
    elif isinstance(exception, TimeoutError):
        error_code = ErrorCode.TIMEOUT_ERROR
    elif isinstance(exception, ConnectionError):
        error_code = ErrorCode.NETWORK_ERROR
    else:
        error_code = ErrorCode.UNKNOWN_ERROR
    
    # translatedinfo
    details = {
        "exception_type": type(exception).__name__,
        "traceback": traceback.format_exc()
    }
    
    if context:
        details["context"] = context
    
    return create_error_response(
        error_code=error_code,
        message=str(exception),
        details=details,
        request_id=request_id
    )


def create_http_exception_response(
    exc: HTTPException,
    request_id: Optional[str] = None
) -> JSONResponse:
    """fromHTTPtranslatedcreateerrortranslated"""
    # translatedstatustranslatederrortranslated
    status_code = exc.status_code
    
    if status_code == 400:
        error_code = ErrorCode.INVALID_REQUEST
    elif status_code == 401:
        error_code = ErrorCode.UNAUTHORIZED
    elif status_code == 403:
        error_code = ErrorCode.FORBIDDtranslated
    elif status_code == 404:
        error_code = ErrorCode.RESOURCE_NOT_FOUND
    elif status_code == 409:
        error_code = ErrorCode.RESOURCE_CONFLICT
    elif status_code == 413:
        error_code = ErrorCode.REQUEST_TOO_LARGE
    elif status_code == 415:
        error_code = ErrorCode.UNSUPPORTED_MEDIA_TYPE
    elif status_code == 422:
        error_code = ErrorCode.VALIDATION_ERROR
    elif status_code == 429:
        error_code = ErrorCode.RATE_LIMIT_EXCEEDED
    elif status_code >= 500:
        error_code = ErrorCode.INTERNAL_SERVER_ERROR
    else:
        error_code = ErrorCode.UNKNOWN_ERROR
    
    return create_error_response(
        error_code=error_code,
        message=exc.detail,
        request_id=request_id
    )
