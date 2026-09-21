# error handling

## 📋 overview

projecterror handling，errorformaterror handling。

## 🏗️ error handling

### error

```python
class ErrorCategory(Enum):
    CONFIGURATION = "CONFIGURATION"  # configerror
    NETWORK = "NETWORK"              # error
    API = "API"                      # APIerror
    FILE_IO = "FILE_IO"              # fileIOerror
    PROCESSING = "PROCESSING"        # error
    VALIDATION = "VALIDATION"        # verifyerror
    SYSTEM = "SYSTEM"                # error
```

### error

```python
class ErrorLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
```

## 🚀 usage

### 1. 

```python
from backend.utils.error_handler import AutoClipsException, ErrorCategory

# configerror
raise AutoClipsException(
    message="APIkeyconfig",
    category=ErrorCategory.CONFIGURATION,
    details={"config_key": "DASHSCOPE_API_KEY"}
)

# fileerror
raise AutoClipsException(
    message="file",
    category=ErrorCategory.FILE_IO,
    details={"file_path": "/path/to/file.mp4"}
)
```

### 2. useerror handling

```python
from backend.core.error_middleware import handle_errors
from backend.utils.error_handler import ErrorCategory

@handle_errors(ErrorCategory.PROCESSING)
async def process_video(video_path: str):
    # AutoClipsException
    if not os.path.exists(video_path):
        raise FileNotFoundError("file")
    
    # ...
    return result
```

### 3. useerror

```python
from backend.core.error_middleware import error_context
from backend.utils.error_handler import ErrorCategory

def upload_file(file_path: str):
    with error_context(ErrorCategory.FILE_IO, {"file_path": file_path}):
        # AutoClipsException
        with open(file_path, 'r') as f:
            content = f.read()
        return content
```

### 4. APIrouteuse

```python
from fastapi import APIRouter, HTTPException
from backend.utils.error_handler import AutoClipsException, ErrorCategory

router = APIRouter()

@router.get("/projects/{project_id}")
async def get_project(project_id: str):
    try:
        # 
        project = await get_project_from_db(project_id)
        if not project:
            raise AutoClipsException(
                message=f"project: {project_id}",
                category=ErrorCategory.VALIDATION,
                details={"project_id": project_id}
            )
        return project
    except AutoClipsException:
        # ，
        raise
    except Exception as e:
        # AutoClipsException
        raise AutoClipsException(
            message="fetchprojectfailed",
            category=ErrorCategory.SYSTEM,
            original_exception=e
        )
```

## 📊 errorformat

errorfollowformat：

```json
{
  "error": {
    "code": "AUTOCLIPS_VALIDATION",
    "message": "project: abc123",
    "details": {
      "project_id": "abc123"
    },
    "request_id": "req_123456",
    "timestamp": 1640995200.0
  }
}
```

### notes

- `code`: error，format `AUTOCLIPS_{CATEGORY}`  `HTTP_{STATUS_CODE}`
- `message`: error，
- `details`: error，
- `request_id`: ID，
- `timestamp`: error

## 🔧 HTTPstatus

| error | HTTPstatus | notes |
|---------|-----------|------|
| CONFIGURATION | 500 | configerror |
| NETWORK | 503 | error |
| API | 502 | APIerror |
| FILE_IO | 500 | fileIOerror |
| PROCESSING | 500 | error |
| VALIDATION | 400 | verifyerror |
| SYSTEM | 500 | error |

## 📝 best practices

### 1. error

```python
# ✅ error
raise AutoClipsException(
    message="fileformatsupport，useMP4format",
    category=ErrorCategory.VALIDATION,
    details={"supported_formats": ["mp4", "avi", "mov"]}
)

# ❌ error
raise AutoClipsException(
    message="Error: Invalid file",
    category=ErrorCategory.VALIDATION
)
```

### 2. error

```python
# ✅ 
raise AutoClipsException(
    message="failed",
    category=ErrorCategory.PROCESSING,
    details={
        "project_id": project_id,
        "step": "video_cutting",
        "error_code": "FFMPEG_ERROR",
        "file_size": file_size
    }
)
```

### 3. errorselect

```python
# ✅ errorselect
if not api_key:
    raise AutoClipsException(
        message="APIkeyconfig",
        category=ErrorCategory.CONFIGURATION  # configissue
    )

if response.status_code == 429:
    raise AutoClipsException(
        message="APIcall",
        category=ErrorCategory.API  # APIissue
    )

if not os.path.exists(file_path):
    raise AutoClipsException(
        message="file",
        category=ErrorCategory.FILE_IO  # fileissue
    )
```

### 4. 

```python
# ✅ 
try:
    result = some_risky_operation()
except Exception as e:
    raise AutoClipsException(
        message="failed",
        category=ErrorCategory.SYSTEM,
        original_exception=e  # 
    )
```

## 🧪 testerror handling

### 1. test

```python
import pytest
from backend.utils.error_handler import AutoClipsException, ErrorCategory

def test_custom_exception():
    with pytest.raises(AutoClipsException) as exc_info:
        raise AutoClipsException(
            message="testerror",
            category=ErrorCategory.VALIDATION
        )
    
    assert exc_info.value.category == ErrorCategory.VALIDATION
    assert exc_info.value.message == "testerror"
```

### 2. testAPIerror

```python
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_error_response():
    response = client.get("/api/v1/projects/nonexistent")
    
    assert response.status_code == 400
    assert "error" in response.json()
    assert response.json()["error"]["code"] == "AUTOCLIPS_VALIDATION"
```

## 🔍 errormonitor

### 1. errorformat

error，format：

```
2024-01-01 12:00:00 - ERROR - : AutoClipsException: project: abc123
request_id: req_123456
path: /api/v1/projects/abc123
method: GET
traceback: []
```

### 2. error

cantoolerror：

```bash
# error
grep "AUTOCLIPS_" backend.log | cut -d' ' -f4 | sort | uniq -c

# error
grep "ERROR" backend.log | wc -l
```

## 🚨 error handling

### 1. fileerror

```python
@handle_errors(ErrorCategory.FILE_IO)
async def save_file(file_path: str, content: bytes):
    try:
        with open(file_path, 'wb') as f:
            f.write(content)
    except PermissionError:
        raise AutoClipsException(
            message="file",
            category=ErrorCategory.FILE_IO,
            details={"file_path": file_path}
        )
    except OSError as e:
        raise AutoClipsException(
            message="file systemerror",
            category=ErrorCategory.FILE_IO,
            details={"file_path": file_path, "os_error": str(e)}
        )
```

### 2. APIcallerror

```python
@handle_errors(ErrorCategory.API)
async def call_external_api(url: str, data: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 429:
                    raise AutoClipsException(
                        message="APIcall",
                        category=ErrorCategory.API,
                        details={"url": url, "status": 429}
                    )
                return await response.json()
    except aiohttp.ClientError as e:
        raise AutoClipsException(
            message="failed",
            category=ErrorCategory.NETWORK,
            details={"url": url, "error": str(e)}
        )
```

### 3. error

```python
@handle_errors(ErrorCategory.PROCESSING)
async def process_video_data(video_path: str):
    try:
        # 
        result = await video_processor.process(video_path)
        return result
    except VideoProcessingError as e:
        raise AutoClipsException(
            message="failed",
            category=ErrorCategory.PROCESSING,
            details={
                "video_path": video_path,
                "error_code": e.code,
                "step": e.step
            },
            original_exception=e
        )
```

## 📚 related docs

- [APIdocs](./API_DOCUMENTATION.md)
- [config](./CONFIGURATION_GUIDE.md)
- [](./LOGGING_GUIDE.md)
