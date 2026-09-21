# ENUsage Guide

## 📋 EN

EN，ProvidesEN、EN。ENRedisEN、EN，EN。

## 🏗️ System Architecture

### EN

```python
class ProgressStage(Enum):
    INGEST = "INGEST"          # EN/EN (10%)
    SUBTITLE = "SUBTITLE"      # EN/EN (15%)
    ANALYZE = "ANALYZE"        # EN/EN (20%)
    HIGHLIGHT = "HIGHLIGHT"    # EN/EN (25%)
    EXPORT = "EXPORT"          # EN/EN (20%)
    DONE = "DONE"              # EN/EN (10%)
    ERROR = "ERROR"            # EN
```

### EN

```python
class ProgressStatus(Enum):
    PENDING = "PENDING"        # EN
    RUNNING = "RUNNING"        # EN
    COMPLETED = "COMPLETED"    # EN
    FAILED = "FAILED"          # EN
    CANCELLED = "CANCELLED"    # EN
```

### EN

1. **EN**: EN，EN
2. **RedisEN**: EN，SupportEN
3. **EN**: EN，EN

## 🚀 EN

### 1. EN

```python
from backend.services.enhanced_progress_service import (
    start_progress, update_progress, complete_progress, fail_progress,
    ProgressStage, ProgressStatus
)

# EN
progress_info = start_progress(
    project_id="project_123",
    task_id="task_456",
    initial_message="EN"
)

# EN
progress_info = update_progress(
    project_id="project_123",
    stage=ProgressStage.SUBTITLE,
    message="EN",
    sub_progress=50.0  # Current Stage50%EN
)

# EN
progress_info = complete_progress(
    project_id="project_123",
    message="EN"
)

# EN
progress_info = fail_progress(
    project_id="project_123",
    error_message="EN"
)
```

### 2. EN

```python
from backend.services.enhanced_progress_service import (
    progress_service, ProgressStage
)
from backend.core.error_middleware import handle_errors, ErrorCategory

class VideoProcessingService:
    
    @handle_errors(ErrorCategory.PROCESSING)
    async def process_video(self, project_id: str, video_path: str):
        try:
            # EN
            progress_service.start_progress(
                project_id=project_id,
                initial_message="EN"
            )
            
            # EN
            progress_service.update_progress(
                project_id=project_id,
                stage=ProgressStage.INGEST,
                message="EN",
                sub_progress=100.0
            )
            
            # EN
            progress_service.update_progress(
                project_id=project_id,
                stage=ProgressStage.SUBTITLE,
                message="EN",
                sub_progress=0.0
            )
            
            # EN
            for i in range(10):
                await asyncio.sleep(1)  # EN
                progress_service.update_progress(
                    project_id=project_id,
                    stage=ProgressStage.SUBTITLE,
                    message=f"EN: {i*10}%",
                    sub_progress=i * 10.0
                )
            
            # EN
            progress_service.update_progress(
                project_id=project_id,
                stage=ProgressStage.ANALYZE,
                message="EN",
                sub_progress=0.0
            )
            
            # EN...
            
            # EN
            progress_service.complete_progress(
                project_id=project_id,
                message="EN"
            )
            
        except Exception as e:
            # EN
            progress_service.fail_progress(
                project_id=project_id,
                error_message=str(e)
            )
            raise
```

### 3. ENAPIEN

```python
from fastapi import APIRouter, HTTPException
from backend.services.enhanced_progress_service import get_progress

router = APIRouter()

@router.get("/projects/{project_id}/progress")
async def get_project_progress(project_id: str):
    """EN"""
    try:
        progress_info = get_progress(project_id)
        if not progress_info:
            raise HTTPException(status_code=404, detail="EN")
        
        return {
            "project_id": project_id,
            "progress": progress_info.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 4. EN

```python
from backend.services.enhanced_progress_service import progress_service

def progress_callback(progress_info):
    """EN"""
    print(f"EN {progress_info.project_id} EN: {progress_info.progress}%")
    
    # EN，EN：
    # - EN
    # - EN
    # - EN
    # - EN

# EN
progress_service.add_progress_callback(progress_callback)
```

## 📊 EN

```python
@dataclass
class ProgressInfo:
    project_id: str                    # ENID
    task_id: Optional[str]             # ENID
    stage: ProgressStage               # Current Stage
    status: ProgressStatus             # EN
    progress: int                      # EN (0-100)
    message: str                       # EN
    error_message: Optional[str]       # EN
    start_time: Optional[datetime]     # EN
    end_time: Optional[datetime]       # EN
    estimated_remaining: Optional[int] # EN(EN)
    metadata: Optional[Dict[str, Any]] # EN
```

### EN

- **INGESTEN**: 0-10%
- **SUBTITLEEN**: 10-25%
- **ANALYZEEN**: 25-45%
- **HIGHLIGHTEN**: 45-70%
- **EXPORTEN**: 70-90%
- **DONEEN**: 100%

EN`sub_progress`EN(0-100)EN。

## 🔧 EN

### 1. RedisEN

```python
# ENbackend/core/unified_config.pyEN
redis:
  url: "redis://localhost:6379/0"
  max_connections: 10
  socket_timeout: 5
```

### 2. EN

```python
# EN
progress_service.cleanup_old_progress(max_age_hours=24)
```

### 3. EN

```python
from backend.utils.error_handler import AutoClipsException, ErrorCategory

try:
    progress_service.update_progress(project_id, stage, message)
except AutoClipsException as e:
    if e.category == ErrorCategory.SYSTEM:
        # EN，EN
        logger.error(f"EN: {e}")
    else:
        # EN，EN
        raise
```

## 📝 EN

### 1. EN

```python
# ✅ EN
progress_service.update_progress(
    project_id=project_id,
    stage=ProgressStage.SUBTITLE,
    message="EN，EN2EN",
    sub_progress=60.0
)

# ❌ EN
progress_service.update_progress(
    project_id=project_id,
    stage=ProgressStage.SUBTITLE,
    message="EN...",
    sub_progress=60.0
)
```

### 2. EN

```python
# ✅ EN
try:
    # EN
    result = await process_video(video_path)
    progress_service.complete_progress(project_id, "EN")
except Exception as e:
    # EN
    error_message = f"EN: {str(e)}"
    progress_service.fail_progress(project_id, error_message)
    raise
```

### 3. EN

```python
# ✅ EN
progress_service.update_progress(
    project_id=project_id,
    stage=ProgressStage.ANALYZE,
    message="EN",
    metadata={
        "video_duration": 1200,  # EN(EN)
        "analysis_method": "ai",  # EN
        "estimated_clips": 5      # EN
    }
)
```

### 4. Performance

```python
# ✅ EN
for i, item in enumerate(items):
    if i % 10 == 0:  # EN10EN
        progress_service.update_progress(
            project_id=project_id,
            stage=ProgressStage.PROCESSING,
            message=f"EN: {i}/{len(items)}",
            sub_progress=i / len(items) * 100
        )
```

## 🧪 EN

### 1. EN

```python
import pytest
from backend.services.enhanced_progress_service import (
    start_progress, update_progress, complete_progress,
    ProgressStage, ProgressStatus
)

def test_progress_tracking():
    project_id = "test_project"
    
    # EN
    progress = start_progress(project_id, initial_message="EN")
    assert progress.project_id == project_id
    assert progress.status == ProgressStatus.RUNNING
    assert progress.progress == 0
    
    # EN
    progress = update_progress(
        project_id=project_id,
        stage=ProgressStage.SUBTITLE,
        message="EN",
        sub_progress=50.0
    )
    assert progress.stage == ProgressStage.SUBTITLE
    assert progress.progress > 0
    
    # EN
    progress = complete_progress(project_id, "EN")
    assert progress.status == ProgressStatus.COMPLETED
    assert progress.progress == 100
```

### 2. EN

```python
async def test_progress_integration():
    project_id = "integration_test"
    
    # EN
    start_progress(project_id, "EN")
    
    for stage in [ProgressStage.INGEST, ProgressStage.SUBTITLE, 
                  ProgressStage.ANALYZE, ProgressStage.HIGHLIGHT, 
                  ProgressStage.EXPORT]:
        update_progress(project_id, stage, f"EN{stage.value}EN")
        await asyncio.sleep(0.1)  # EN
    
    complete_progress(project_id, "EN")
    
    # EN
    final_progress = get_progress(project_id)
    assert final_progress.status == ProgressStatus.COMPLETED
    assert final_progress.progress == 100
```

## 🔍 EN

### 1. EN

```python
# EN
active_progress = progress_service.get_all_active_progress()
for progress in active_progress:
    print(f"EN {progress.project_id}: {progress.progress}% - {progress.message}")
```

### 2. EN

```python
# EN
progress_info = get_progress(project_id)
if progress_info:
    print(f"ENID: {progress_info.project_id}")
    print(f"Current Stage: {progress_info.stage.value}")
    print(f"EN: {progress_info.progress}%")
    print(f"EN: {progress_info.status.value}")
    print(f"EN: {progress_info.message}")
    print(f"EN: {progress_info.start_time}")
    print(f"EN: {progress_info.estimated_remaining}EN")
    if progress_info.metadata:
        print(f"EN: {progress_info.metadata}")
```

### 3. EN

```python
import logging

# EN
progress_logger = logging.getLogger('progress')
progress_logger.setLevel(logging.INFO)

def progress_log_callback(progress_info):
    progress_logger.info(
        f"EN {progress_info.project_id} EN: "
        f"{progress_info.progress}% - {progress_info.message}"
    )

progress_service.add_progress_callback(progress_log_callback)
```

## 🚨 FAQ

### 1. RedisEN

```python
# EN
# ENRedisEN
if not progress_service.redis_client:
    logger.warning("RedisEN，EN")
```

### 2. EN

```python
# EN
# EN
progress_service.cleanup_old_progress(max_age_hours=48)  # 48EN
```

### 3. EN

```python
# ENBuilt-inEN，EN
# EN
for i, item in enumerate(items):
    if i % 10 == 0:  # EN10EN
        update_progress(project_id, stage, message, i/len(items)*100)
```

## 📚 EN

- [EN](./ERROR_HANDLING_GUIDE.md)
- [EN](./CONFIGURATION_GUIDE.md)
- [APIEN](./API_DOCUMENTATION.md)
