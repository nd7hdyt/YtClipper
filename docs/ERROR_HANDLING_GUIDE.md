# EN

## 📋 EN

EN，ProvidesEN。

## 🏗️ EN

### EN

```python
class ErrorCategory(Enum):
    CONFIGURATION = "CONFIGURATION"  # EN
    NETWORK = "NETWORK"              # EN
    API = "API"                      # APIEN
    FILE_IO = "FILE_IO"              # ENIOEN
    PROCESSING = "PROCESSING"        # EN
    VALIDATION = "VALIDATION"        # EN
    SYSTEM = "SYSTEM"                # EN
```

### EN

```python
class ErrorLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
```

## 🚀 EN

### 1. EN

```python
from backend.utils.error_handler import AutoClipsException, ErrorCategory

# EN
raise AutoClipsException(
    message="APIEN",
    category=ErrorCategory.CONFIGURATION,
    details={"config_key": "DASHSCOPE_API_KEY"}
)

# EN
raise AutoClipsException(
    message="EN",
    category=ErrorCategory.FILE_IO,
    details={"file_path": "/path/to/file.mp4"}
)
```

### 2. EN

```python
from backend.core.error_middleware import handle_errors
from backend.utils.error_handler import ErrorCategory

@handle_errors(ErrorCategory.PROCESSING)
async def process_video(video_path: str):
    # ENAutoClipsException
    if not os.path.exists(video_path):
        raise FileNotFoundError("EN")
    
    # EN...
    return result
```

### 3. EN

```python
from backend.core.error_middleware import error_context
from backend.utils.error_handler import ErrorCategory

def upload_file(file_path: str):
    with error_context(ErrorCategory.FILE_IO, {"file_path": file_path}):
        # ENAutoClipsException
        with open(file_path, 'r') as f:
            content = f.read()
        return content
```

### 4. ENAPIEN

```python
from fastapi import APIRouter, HTTPException
from backend.utils.error_handler import AutoClipsException, ErrorCategory

router = APIRouter()

@router.get("/projects/{project_id}")
async def get_project(project_id: str):
    try:
        # EN
        project = await get_project_from_db(project_id)
        if not project:
            raise AutoClipsException(
                message=f"EN: {project_id}",
                category=ErrorCategory.VALIDATION,
                details={"project_id": project_id}
            )
        return project
    except AutoClipsException:
        # EN，EN
        raise
    except Exception as e:
        # ENAutoClipsException
        raise AutoClipsException(
            message="EN",
            category=ErrorCategory.SYSTEM,
            original_exception=e
        )
```

## 📊 EN

EN：

```json
{
  "error": {
    "code": "AUTOCLIPS_VALIDATION",
    "message": "EN: abc123",
    "details": {
      "project_id": "abc123"
    },
    "request_id": "req_123456",
    "timestamp": 1640995200.0
  }
}
```

### EN

- `code`: EN，EN `AUTOCLIPS_{CATEGORY}` EN `HTTP_{STATUS_CODE}`
- `message`: EN，EN
- `details`: EN，EN
- `request_id`: ENID，EN
- `timestamp`: EN

## 🔧 HTTPEN

| EN | HTTPEN | EN |
|---------|-----------|------|
| CONFIGURATION | 500 | EN |
| NETWORK | 503 | EN |
| API | 502 | APIEN |
| FILE_IO | 500 | ENIOEN |
| PROCESSING | 500 | EN |
| VALIDATION | 400 | EN |
| SYSTEM | 500 | EN |

## 📝 EN

### 1. EN

```python
# ✅ EN
raise AutoClipsException(
    message="ENSupport，ENMP4EN",
    category=ErrorCategory.VALIDATION,
    details={"supported_formats": ["mp4", "avi", "mov"]}
)

# ❌ EN
raise AutoClipsException(
    message="Error: Invalid file",
    category=ErrorCategory.VALIDATION
)
```

### 2. EN

```python
# ✅ EN
raise AutoClipsException(
    message="EN",
    category=ErrorCategory.PROCESSING,
    details={
        "project_id": project_id,
        "step": "video_cutting",
        "error_code": "FFMPEG_ERROR",
        "file_size": file_size
    }
)
```

### 3. EN

```python
# ✅ EN
if not api_key:
    raise AutoClipsException(
        message="APIEN",
        category=ErrorCategory.CONFIGURATION  # EN
    )

if response.status_code == 429:
    raise AutoClipsException(
        message="APIEN",
        category=ErrorCategory.API  # APIEN
    )

if not os.path.exists(file_path):
    raise AutoClipsException(
        message="EN",
        category=ErrorCategory.FILE_IO  # EN
    )
```

### 4. EN

```python
# ✅ EN
try:
    result = some_risky_operation()
except Exception as e:
    raise AutoClipsException(
        message="EN",
        category=ErrorCategory.SYSTEM,
        original_exception=e  # EN
    )
```

## 🧪 EN

### 1. EN

```python
import pytest
from backend.utils.error_handler import AutoClipsException, ErrorCategory

def test_custom_exception():
    with pytest.raises(AutoClipsException) as exc_info:
        raise AutoClipsException(
            message="EN",
            category=ErrorCategory.VALIDATION
        )
    
    assert exc_info.value.category == ErrorCategory.VALIDATION
    assert exc_info.value.message == "EN"
```

### 2. ENAPIEN

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

## 🔍 EN

### 1. EN

EN，EN：

```
2024-01-01 12:00:00 - ERROR - EN: AutoClipsException: EN: abc123
request_id: req_123456
path: /api/v1/projects/abc123
method: GET
traceback: [EN]
```

### 2. EN

EN：

```bash
# EN
grep "AUTOCLIPS_" backend.log | cut -d' ' -f4 | sort | uniq -c

# EN
grep "ERROR" backend.log | wc -l
```

## 🚨 EN

### 1. EN

```python
@handle_errors(ErrorCategory.FILE_IO)
async def save_file(file_path: str, content: bytes):
    try:
        with open(file_path, 'wb') as f:
            f.write(content)
    except PermissionError:
        raise AutoClipsException(
            message="EN",
            category=ErrorCategory.FILE_IO,
            details={"file_path": file_path}
        )
    except OSError as e:
        raise AutoClipsException(
            message="EN",
            category=ErrorCategory.FILE_IO,
            details={"file_path": file_path, "os_error": str(e)}
        )
```

### 2. APIEN

```python
@handle_errors(ErrorCategory.API)
async def call_external_api(url: str, data: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 429:
                    raise AutoClipsException(
                        message="APIEN",
                        category=ErrorCategory.API,
                        details={"url": url, "status": 429}
                    )
                return await response.json()
    except aiohttp.ClientError as e:
        raise AutoClipsException(
            message="EN",
            category=ErrorCategory.NETWORK,
            details={"url": url, "error": str(e)}
        )
```

### 3. EN

```python
@handle_errors(ErrorCategory.PROCESSING)
async def process_video_data(video_path: str):
    try:
        # EN
        result = await video_processor.process(video_path)
        return result
    except VideoProcessingError as e:
        raise AutoClipsException(
            message="EN",
            category=ErrorCategory.PROCESSING,
            details={
                "video_path": video_path,
                "error_code": e.code,
                "step": e.step
            },
            original_exception=e
        )
```

## 📚 EN

- [APIEN](./API_DOCUMENTATION.md)
- [EN](./CONFIGURATION_GUIDE.md)
- [EN](./LOGGING_GUIDE.md)
