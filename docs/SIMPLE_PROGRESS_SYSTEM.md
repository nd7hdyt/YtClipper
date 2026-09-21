# EN

## EN

ENBased on"EN"EN，EN + EN，EN。

## Core Features

- **EN**: 6EN，EN
- **EN**: ENHTTP APIEN，ENWebSocket
- **RedisEN**: ENRedisEN，SupportEN
- **EN**: EN，EN6EN

## System Architecture

### EN

1. **`backend/services/simple_progress.py`** - EN
   - EN
   - RedisEN
   - EN

2. **`backend/api/v1/simple_progress.py`** - APIEN
   - `/api/v1/simple-progress/snapshot` - EN
   - `/api/v1/simple-progress/snapshot/{project_id}` - EN
   - `/api/v1/simple-progress/stages` - EN

3. **`backend/services/simple_pipeline_adapter.py`** - EN
   - EN
   - EN

### EN

1. **`frontend/src/stores/useSimpleProgressStore.ts`** - EN
   - ZustandEN
   - EN
   - EN

2. **`frontend/src/components/SimpleProgressBar.tsx`** - EN
   - EN
   - EN
   - EN

3. **`frontend/src/components/SimpleProjectCard.tsx`** - EN
   - EN
   - EN
   - EN

## EN

```python
STAGES = [
    ("INGEST", 10),        # EN/EN
    ("SUBTITLE", 15),      # EN/EN  
    ("ANALYZE", 20),       # EN/EN
    ("HIGHLIGHT", 25),     # EN/EN
    ("EXPORT", 20),        # EN/EN
    ("DONE", 10),          # EN/EN
]
```

## EN

```python
def compute_percent(stage: str, subpercent: Optional[float] = None) -> int:
    # EN
    done = 0
    for s in ORDER:
        if s == stage:
            break
        done += WEIGHTS[s]
    
    # Current Stage
    cur = WEIGHTS.get(stage, 0)
    
    if subpercent is None:
        return min(100, done + cur) if stage == "DONE" else min(99, done)
    else:
        return min(99, done + int(cur * subpercent / 100))
```

## EN

```json
{
  "project_id": "46ab50a6-....",
  "stage": "HIGHLIGHT", 
  "percent": 70,
  "message": "EN，EN 12 EN",
  "ts": 1640995200
}
```

## EN

### EN

1. **EN**:
```python
from backend.services.simple_progress import emit_progress

# EN
emit_progress(project_id, "ANALYZE", "EN")

# EN
emit_progress(project_id, "ANALYZE", "EN(50%)", subpercent=50)
```

2. **EN**:
```python
from backend.services.simple_pipeline_adapter import create_simple_pipeline_adapter

adapter = create_simple_pipeline_adapter(project_id, task_id)
result = adapter.process_project_sync(video_path, srt_path)
```

### EN

1. **EN**:
```typescript
import { useSimpleProgressStore } from '../stores/useSimpleProgressStore'

const { startPolling, stopPolling, getProgress } = useSimpleProgressStore()

// EN
startPolling(['project-1', 'project-2'], 2000)

// EN
const progress = getProgress('project-1')
```

2. **EN**:
```tsx
import { SimpleProgressBar } from '../components/SimpleProgressBar'

<SimpleProgressBar
  projectId="project-1"
  autoStart={true}
  pollingInterval={2000}
  showDetails={true}
  onProgressUpdate={(progress) => console.log(progress)}
/>
```

3. **EN**:
```tsx
import { SimpleProjectCard } from '../components/SimpleProjectCard'

<SimpleProjectCard
  project={project}
  onStartProcessing={handleStart}
  onViewDetails={handleView}
  onDelete={handleDelete}
  onRetry={handleRetry}
/>
```

## APIEN

### EN

```bash
# EN
GET /api/v1/simple-progress/snapshot?project_ids=project-1&project_ids=project-2

# EN
GET /api/v1/simple-progress/snapshot/project-1
```

### EN

```bash
GET /api/v1/simple-progress/stages
```

## EN

### EN
- EN: 2000ms (2EN)
- EN: 1000-5000ms
- EN

### EN
- EN: 100
- EN
- EN

## EN

### RedisEN
- EN
- EN
- EN

### EN
- EN
- EN
- EN

### EN
- SupportEN
- EN
- ProvidesEN

## Performance

1. **EN**: EN
2. **EN**: EN
3. **EN**: EN
4. **EN**: EN

## EN

1. **EN**: ENSTAGESEN
2. **EN**: EN
3. **EN**: SupportEN
4. **ENSupport**: ENSupportEN

## EN

1. **EN**: EN
2. **EN**: EN
3. **EN**: EN
4. **EN**: EN

## EN

EN：

1. **EN**:
   - ENemit_progressEN
   - ENSimplePipelineAdapterEN
   - ENWebSocketEN

2. **EN**:
   - ENuseSimpleProgressStoreEN
   - ENSimpleProgressBarEN
   - ENWebSocketEN

3. **EN**:
   - EN
   - ENRedisEN
   - EN

## EN

EN"EN"EN，ProvidesEN：

- ✅ **EN**: Based onHTTPEN，ENWebSocket
- ✅ **EN**: EN，EN
- ✅ **EN**: EN，EN
- ✅ **EN**: EN
- ✅ **EN**: EN

EN，EN，EN。
