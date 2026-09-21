# EN

## EN

ENAutoClipEN，EN"EN"EN，ProvidesENProgress Feedback。

## EN

1. **EN**：EN"EN"EN
2. **EN**：EN
3. **EN**：Based onWebSocketEN
4. **EN**：EN

## EN

### EN

#### 1. InlineProgressBar EN

**EN**: `frontend/src/components/InlineProgressBar.tsx`

**EN**:
- EN，EN
- EN
- EN
- EN
- WebSocketEN

**EN**:
```typescript
interface InlineProgressBarProps {
  projectId: string;
  currentStep?: number;
  totalSteps?: number;
  status?: string;
  onProgressUpdate?: (progress: number, step: string) => void;
}
```

**VisualEN**:
- EN：EN
- EN：EN
- EN：EN → EN → EN → EN

#### 2. EN

```typescript
const PIPELINE_STEPS = [
  { id: 1, name: 'EN', description: 'EN' },
  { id: 2, name: 'EN', description: 'Based onSRTEN' },
  { id: 3, name: 'EN', description: 'EN' },
  { id: 4, name: 'EN', description: 'EN' },
  { id: 5, name: 'EN', description: 'EN' },
  { id: 6, name: 'EN', description: 'ENFFmpegEN' }
];
```

### EN

#### 1. EN

**EN**: `backend/services/processing_orchestrator.py`

**EN**:
```python
def _send_realtime_progress_update(self, status: TaskStatus, progress: Optional[float] = None, 
                                 error_message: Optional[str] = None):
    """EN"""
```

**EN**:
- EN1 (EN): 0-10%
- EN2 (EN): 10-30%
- EN3 (EN): 30-50%
- EN4 (EN): 50-70%
- EN5 (EN): 70-85%
- EN6 (EN): 85-100%

#### 2. WebSocketEN

**EN**: `backend/services/websocket_notification_service.py`

**EN**:
```json
{
  "type": "task_progress_update",
  "task_id": "task_uuid",
  "project_id": "project_uuid",
  "status": "running",
  "progress": 45,
  "current_step": 3,
  "total_steps": 6,
  "step_name": "EN",
  "message": "EN...",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### EN

#### 1. ProjectCard EN

**EN**: `frontend/src/components/ProjectCard.tsx`

**EN**:
```typescript
// EN
<div style={{...}}>
  <LoadingOutlined />
  EN
</div>

// EN
<InlineProgressBar
  projectId={project.id}
  currentStep={project.current_step}
  totalSteps={project.total_steps}
  status={normalizedStatus}
  onProgressUpdate={(progress, stepName) => {
    console.log(`EN ${project.id} EN: ${progress}% - ${stepName}`);
  }}
/>
```

## EN

### 1. VisualEN
- **EN**：EN
- **EN**：EN
- **EN**：EN

### 2. EN
- **EN**：EN（EN"EN"）
- **EN**：EN
- **EN**：ENVisual
- **EN**：EN

### 3. EN
- **WebSocketEN**：EN
- **EN**：ENUIEN
- **EN**：EN

## EN

### 1. Performance
- **EN**：EN
- **WebSocketEN**：ENHTTPEN
- **EN**：EN

### 2. EN
- **EN**：EN
- **EN**：EN
- **ENSupport**：EN

### 3. EN
- **EN**：WebSocketEN
- **EN**：EN
- **EN**：EN

## EN

### 1. EN
- ENWebSocketEN
- EN
- EN

### 2. EN
- ENWebSocketEN
- EN
- ENWebSocketEN

### 3. EN
- EN：EN
- EN：EN
- EN：ENSupport

## EN

### 1. EN
- **EN/EN**：SupportEN
- **EN**：SupportEN
- **EN**：EN

### 2. EN
- **EN**：EN
- **EN**：EN
- **EN**：Responsive DesignEN

### 3. EN
- **EN**：EN
- **ENSupport**：EN
- **EN**：EN

## EN

EN：

1. ✅ **EN**：EN
2. ✅ **EN**：EN
3. ✅ **EN**：Based onWebSocketEN
4. ✅ **EN**：ProvidesENVisualEN

ENAutoClipENProvidesEN，EN。
