# EN

## EN

1. **EN**: EN0%EN，EN，EN
2. **WebSocketEN**: ENWebSocketEN，EN
3. **UIEN**: EN、ENUIEN，EN
4. **EN**: EN

## EN

### 1. EN

**EN**: `backend/services/simple_progress.py`
- 6EN，EN
- EN
- RedisEN
- SupportEN（EN）

**EN**: `backend/api/v1/simple_progress.py`
- ENAPIEN
- EN
- EN

**EN**: `backend/services/simple_pipeline_adapter.py`
- EN
- EN
- EN6EN

### 2. EN

**EN**: `frontend/src/stores/useSimpleProgressStore.ts`
- ZustandEN
- EN
- EN
- SupportEN

### 3. ENUIEN

**EN**: `frontend/src/components/UnifiedStatusBar.tsx`
- EN
- SupportEN、EN、EN、EN
- EN32px，EN
- EN，VisualEN
- EN

**EN**: `frontend/src/components/SimpleProgressDisplay.tsx`
- EN
- EN
- SupportEN

### 4. EN

**EN**: `frontend/src/components/ProjectCard.tsx`
- EN
- EN
- SupportEN
- EN

## Core Features

### EN
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

### EN
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

### EN
```json
{
  "project_id": "46ab50a6-....",
  "stage": "HIGHLIGHT",
  "percent": 70,
  "message": "EN，EN 12 EN",
  "ts": 1640995200
}
```

## UIEN

### EN
- **EN**: EN32px，EN
- **EN**: EN，EN
- **EN**: EN+EN，EN
- **EN**:
  - EN: EN (#1890ff → #40a9ff)
  - EN: EN
  - EN: EN (#52c41a → #73d13d)
  - EN: EN (#ff4d4f → #ff7875)
  - EN: EN (#d9d9d9 → #f0f0f0)

### Responsive Design
- SupportEN
- ENSpacingEN
- EN

## EN

### EN
- EN2ENAPIEN
- EN
- EN

### EN
- EN2ENAPI
- EN
- SupportEN

## EN

**EN**: `frontend/src/pages/ProgressTestPage.tsx`
- ProvidesENInterface
- EN
- ENUIEN

## EN

### EN
1. EN`SimplePipelineAdapter`EN
2. EN`emit_progress()`
3. ENWebSocketEN

### EN
1. EN`UnifiedStatusBar`EN
2. EN`useSimpleProgressStore`EN
3. ENWebSocketEN

## Performance

1. **EN**: EN
2. **EN**: EN
3. **EN**: EN
4. **EN**: EN

## EN

1. **RedisEN**: EN，EN
2. **EN**: EN，EN
3. **EN**: SupportEN，ProvidesEN

## EN

EN，EN：

✅ **EN**: Based onHTTPEN，ENWebSocket
✅ **EN**: EN，EN  
✅ **EN**: UIEN，EN
✅ **EN**: EN
✅ **EN**: EN
✅ **EN**: EN

EN，EN，EN。
