# progressuse

## 📋 overview

projectprogress，progress、state managementerror handling。Rediscache、databasememorycache，progress。

## 🏗️ 

### progressstage

```python
class ProgressStage(Enum):
    INGEST = "INGEST"          # download/ (10%)
    SUBTITLE = "SUBTITLE"      # subtitles/ (15%)
    ANALYZE = "ANALYZE"        # /outline (20%)
    HIGHLIGHT = "HIGHLIGHT"    # / (25%)
    EXPORT = "EXPORT"          # export/ (20%)
    DONE = "DONE"              # validate/archive (10%)
    ERROR = "ERROR"            # errorstatus
```

### progressstatus

```python
class ProgressStatus(Enum):
    PENDING = "PENDING"        # 
    RUNNING = "RUNNING"        # 
    COMPLETED = "COMPLETED"    # completed
    FAILED = "FAILED"          # failed
    CANCELLED = "CANCELLED"    # 
```

### 

1. **memorycache**: access，progress
2. **Rediscache**: cache，support
3. **database**: ，project status

## 🚀 usage

### 1. progress

```python
from backend.services.enhanced_progress_service import (
    start_progress, update_progress, complete_progress, fail_progress,
    ProgressStage, ProgressStatus
)

# progress
progress_info = start_progress(
    project_id="project_123",
    task_id="task_456",
    initial_message=""
)

# updateprogress
progress_info = update_progress(
    project_id="project_123",
    stage=ProgressStage.SUBTITLE,
    message="generatesubtitles",
    sub_progress=50.0  # current stage50%completed
)

# completedprogress
progress_info = complete_progress(
    project_id="project_123",
    message="completed"
)

# failed
progress_info = fail_progress(
    project_id="project_123",
    error_message="file"
)
```

### 2. serviceuse

```python
from backend.services.enhanced_progress_service import (
    progress_service, ProgressStage
)
from backend.core.error_middleware import handle_errors, ErrorCategory

class VideoProcessingService:
    
    @handle_errors(ErrorCategory.PROCESSING)
    async def process_video(self, project_id: str, video_path: str):
        try:
            # progress
            progress_service.start_progress(
                project_id=project_id,
                initial_message=""
            )
            
            # downloadstage
            progress_service.update_progress(
                project_id=project_id,
                stage=ProgressStage.INGEST,
                message="downloadfile",
                sub_progress=100.0
            )
            
            # subtitlesgeneratestage
            progress_service.update_progress(
                project_id=project_id,
                stage=ProgressStage.SUBTITLE,
                message="generatesubtitles",
                sub_progress=0.0
            )
            
            # subtitlesgenerate
            for i in range(10):
                await asyncio.sleep(1)  # 
                progress_service.update_progress(
                    project_id=project_id,
                    stage=ProgressStage.SUBTITLE,
                    message=f"subtitlesgenerateprogress: {i*10}%",
                    sub_progress=i * 10.0
                )
            
            # stage
            progress_service.update_progress(
                project_id=project_id,
                stage=ProgressStage.ANALYZE,
                message="",
                sub_progress=0.0
            )
            
            # stage...
            
            # completed
            progress_service.complete_progress(
                project_id=project_id,
                message="completed"
            )
            
        except Exception as e:
            # failed
            progress_service.fail_progress(
                project_id=project_id,
                error_message=str(e)
            )
            raise
```

### 3. APIuse

```python
from fastapi import APIRouter, HTTPException
from backend.services.enhanced_progress_service import get_progress

router = APIRouter()

@router.get("/projects/{project_id}/progress")
async def get_project_progress(project_id: str):
    """fetchprojectprogress"""
    try:
        progress_info = get_progress(project_id)
        if not progress_info:
            raise HTTPException(status_code=404, detail="projectprogress")
        
        return {
            "project_id": project_id,
            "progress": progress_info.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 4. progress

```python
from backend.services.enhanced_progress_service import progress_service

def progress_callback(progress_info):
    """progress"""
    print(f"project {progress_info.project_id} progressupdate: {progress_info.progress}%")
    
    # can，：
    # - 
    # - updatefrontendstatus
    # - 
    # - service

# 
progress_service.add_progress_callback(progress_callback)
```

## 📊 progress

```python
@dataclass
class ProgressInfo:
    project_id: str                    # projectID
    task_id: Optional[str]             # ID
    stage: ProgressStage               # current stage
    status: ProgressStatus             # status
    progress: int                      # progress (0-100)
    message: str                       # 
    error_message: Optional[str]       # error
    start_time: Optional[datetime]     # 
    end_time: Optional[datetime]       # 
    estimated_remaining: Optional[int] # ()
    metadata: Optional[Dict[str, Any]] # metadata
```

### progress

- **INGESTstage**: 0-10%
- **SUBTITLEstage**: 10-25%
- **ANALYZEstage**: 25-45%
- **HIGHLIGHTstage**: 45-70%
- **EXPORTstage**: 70-90%
- **DONEstage**: 100%

stagecan`sub_progress`(0-100)progress。

## 🔧 config

### 1. Redisconfig

```python
# backend/core/unified_config.pyconfig
redis:
  url: "redis://localhost:6379/0"
  max_connections: 10
  socket_timeout: 5
```

### 2. config

```python
# progress
progress_service.cleanup_old_progress(max_age_hours=24)
```

### 3. error handling

```python
from backend.utils.error_handler import AutoClipsException, ErrorCategory

try:
    progress_service.update_progress(project_id, stage, message)
except AutoClipsException as e:
    if e.category == ErrorCategory.SYSTEM:
        # error，
        logger.error(f"progressupdatefailed: {e}")
    else:
        # error，
        raise
```

## 📝 best practices

### 1. progress

```python
# ✅ progress
progress_service.update_progress(
    project_id=project_id,
    stage=ProgressStage.SUBTITLE,
    message="generatesubtitles，2minutes",
    sub_progress=60.0
)

# ❌ progress
progress_service.update_progress(
    project_id=project_id,
    stage=ProgressStage.SUBTITLE,
    message="processing...",
    sub_progress=60.0
)
```

### 2. error handling

```python
# ✅ error handling
try:
    # 
    result = await process_video(video_path)
    progress_service.complete_progress(project_id, "completed")
except Exception as e:
    # error
    error_message = f"failed: {str(e)}"
    progress_service.fail_progress(project_id, error_message)
    raise
```

### 3. metadatause

```python
# ✅ usemetadata
progress_service.update_progress(
    project_id=project_id,
    stage=ProgressStage.ANALYZE,
    message="",
    metadata={
        "video_duration": 1200,  # ()
        "analysis_method": "ai",  # method
        "estimated_clips": 5      # clip
    }
)
```

### 4. performance

```python
# ✅ updateprogress
for i, item in enumerate(items):
    if i % 10 == 0:  # 10projectupdateprogress
        progress_service.update_progress(
            project_id=project_id,
            stage=ProgressStage.PROCESSING,
            message=f"progress: {i}/{len(items)}",
            sub_progress=i / len(items) * 100
        )
```

## 🧪 testprogress

### 1. test

```python
import pytest
from backend.services.enhanced_progress_service import (
    start_progress, update_progress, complete_progress,
    ProgressStage, ProgressStatus
)

def test_progress_tracking():
    project_id = "test_project"
    
    # progress
    progress = start_progress(project_id, initial_message="test")
    assert progress.project_id == project_id
    assert progress.status == ProgressStatus.RUNNING
    assert progress.progress == 0
    
    # updateprogress
    progress = update_progress(
        project_id=project_id,
        stage=ProgressStage.SUBTITLE,
        message="testsubtitlesgenerate",
        sub_progress=50.0
    )
    assert progress.stage == ProgressStage.SUBTITLE
    assert progress.progress > 0
    
    # completedprogress
    progress = complete_progress(project_id, "testcompleted")
    assert progress.status == ProgressStatus.COMPLETED
    assert progress.progress == 100
```

### 2. integration test

```python
async def test_progress_integration():
    project_id = "integration_test"
    
    # 
    start_progress(project_id, "integration test")
    
    for stage in [ProgressStage.INGEST, ProgressStage.SUBTITLE, 
                  ProgressStage.ANALYZE, ProgressStage.HIGHLIGHT, 
                  ProgressStage.EXPORT]:
        update_progress(project_id, stage, f"test{stage.value}stage")
        await asyncio.sleep(0.1)  # 
    
    complete_progress(project_id, "integration testcompleted")
    
    # verifystatus
    final_progress = get_progress(project_id)
    assert final_progress.status == ProgressStatus.COMPLETED
    assert final_progress.progress == 100
```

## 🔍 monitor

### 1. progressmonitor

```python
# fetchprogress
active_progress = progress_service.get_all_active_progress()
for progress in active_progress:
    print(f"project {progress.project_id}: {progress.progress}% - {progress.message}")
```

### 2. 

```python
# fetchprogress
progress_info = get_progress(project_id)
if progress_info:
    print(f"projectID: {progress_info.project_id}")
    print(f"current stage: {progress_info.stage.value}")
    print(f"progress: {progress_info.progress}%")
    print(f"status: {progress_info.status.value}")
    print(f": {progress_info.message}")
    print(f": {progress_info.start_time}")
    print(f": {progress_info.estimated_remaining}")
    if progress_info.metadata:
        print(f"metadata: {progress_info.metadata}")
```

### 3. 

```python
import logging

# configprogress
progress_logger = logging.getLogger('progress')
progress_logger.setLevel(logging.INFO)

def progress_log_callback(progress_info):
    progress_logger.info(
        f"project {progress_info.project_id} progressupdate: "
        f"{progress_info.progress}% - {progress_info.message}"
    )

progress_service.add_progress_callback(progress_log_callback)
```

## 🚨 FAQ

### 1. Redisconnection failed

```python
# memorycache
# checkRedisconfig
if not progress_service.redis_client:
    logger.warning("Redisavailable，usememorycache")
```

### 2. progress

```python
# progress
# settings
progress_service.cleanup_old_progress(max_age_hours=48)  # 48
```

### 3. progressupdate

```python
# ，update
# update
for i, item in enumerate(items):
    if i % 10 == 0:  # 10update
        update_progress(project_id, stage, message, i/len(items)*100)
```

## 📚 related docs

- [error handling](./ERROR_HANDLING_GUIDE.md)
- [config](./CONFIGURATION_GUIDE.md)
- [APIdocs](./API_DOCUMENTATION.md)
