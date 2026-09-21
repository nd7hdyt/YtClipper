# progress

## overview

based on""progress，usestage + progress，dependencies。

## 

- **stage**: 6stage，stage
- ****: frontendHTTP APIfetchprogress，no needWebSocket
- **Redis**: backenduseRedisprogress，support
- **event**: stageevent，6

## 

### backend

1. **`backend/services/simple_progress.py`** - progressservice
   - stage
   - Redisevent
   - progress

2. **`backend/api/v1/simple_progress.py`** - APIAPI
   - `/api/v1/simple-progress/snapshot` - fetchprogress
   - `/api/v1/simple-progress/snapshot/{project_id}` - projectprogress
   - `/api/v1/simple-progress/stages` - fetchstageconfig

3. **`backend/services/simple_pipeline_adapter.py`** - 
   - integrationprogress
   - stageevent

### frontend

1. **`frontend/src/stores/useSimpleProgressStore.ts`** - state management
   - Zustandstate management
   - 
   - progresscache

2. **`frontend/src/components/SimpleProgressBar.tsx`** - progress
   - projectprogress
   - projectprogress
   - integration

3. **`frontend/src/components/SimpleProjectCard.tsx`** - project
   - integrationprogress
   - state management
   - button

## stage

```python
STAGES = [
    ("INGEST", 10),        # download/
    ("SUBTITLE", 15),      # subtitles/  
    ("ANALYZE", 20),       # /outline
    ("HIGHLIGHT", 25),     # /
    ("EXPORT", 20),        # export/
    ("DONE", 10),          # validate/archive
]
```

## progress

```python
def compute_percent(stage: str, subpercent: Optional[float] = None) -> int:
    # stage
    done = 0
    for s in ORDER:
        if s == stage:
            break
        done += WEIGHTS[s]
    
    # current stage
    cur = WEIGHTS.get(stage, 0)
    
    if subpercent is None:
        return min(100, done + cur) if stage == "DONE" else min(99, done)
    else:
        return min(99, done + int(cur * subpercent / 100))
```

## eventformat

```json
{
  "project_id": "46ab50a6-....",
  "stage": "HIGHLIGHT", 
  "percent": 70,
  "message": "completed， 12 ",
  "ts": 1640995200
}
```

## usage

### backendintegration

1. **progressevent**:
```python
from backend.services.simple_progress import emit_progress

# stage
emit_progress(project_id, "ANALYZE", "")

# progress
emit_progress(project_id, "ANALYZE", "(50%)", subpercent=50)
```

2. **use**:
```python
from backend.services.simple_pipeline_adapter import create_simple_pipeline_adapter

adapter = create_simple_pipeline_adapter(project_id, task_id)
result = adapter.process_project_sync(video_path, srt_path)
```

### frontendintegration

1. **useprogressstate management**:
```typescript
import { useSimpleProgressStore } from '../stores/useSimpleProgressStore'

const { startPolling, stopPolling, getProgress } = useSimpleProgressStore()

// 
startPolling(['project-1', 'project-2'], 2000)

// fetchprogress
const progress = getProgress('project-1')
```

2. **useprogress**:
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

3. **useproject**:
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

## APIAPI

### fetchprogress

```bash
# fetch
GET /api/v1/simple-progress/snapshot?project_ids=project-1&project_ids=project-2

# fetch
GET /api/v1/simple-progress/snapshot/project-1
```

### fetchstageconfig

```bash
GET /api/v1/simple-progress/stages
```

## config

### 
- default: 2000ms (2)
- : 1000-5000ms
- 

### stage
- : 100
- stage
- stage

## 

### Redisconnection failed
- 
- progressevent
- frontendreturn

### 
- frontend
- progresscachelocalstatus
- 

### stage
- supportfailedstatus
- failedstatus
- 

## performance

1. ****: fetchprojectprogress
2. **cache**: 
3. ****: needstart
4. ****: progress

## 

1. **addedstage**: STAGESconfig
2. ****: stage
3. ****: supportstageformat
4. **support**: configsupport

## monitor

1. ****: progressevent
2. **statuscheck**: progressstatus
3. **error**: error
4. ****: monitor

## 

progress：

1. **backend**:
   - progressemit_progresscall
   - useSimplePipelineAdapter
   - WebSocketprogress

2. **frontend**:
   - useuseSimpleProgressStorestate management
   - useSimpleProgressBarprogress
   - configWebSocket

3. ****:
   - progress
   - Redisprogress
   - updateproject status

## summary

progress""，：

- ✅ ****: based onHTTP，dependenciesWebSocket
- ✅ ****: stage，
- ✅ ****: ，cache
- ✅ ****: stage
- ✅ ****: status

，，。
