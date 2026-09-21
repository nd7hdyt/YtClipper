# 👨‍💻 AutoClip Desktop EN

## 📋 EN

- [EN](#EN)
- [EN](#EN)
- [EN](#EN)
- [EN](#EN)
- [APIEN](#apiEN)
- [EN](#EN)
- [EN](#EN)
- [TauriEN](#tauriEN)
- [EN](#EN)
- [EN](#EN)
- [Contributing](#Contributing)

## 🏗️ EN

### EN

```
AutoClip Desktop
├── Frontend (React + TypeScript + Ant Design)
├── Backend (Python + FastAPI + Celery)
├── Tauri (Rust + WebView)
└── Resources (FFmpeg + EN)
```

### Tech Stack

- **EN**: React 18, TypeScript, Ant Design, Vite
- **EN**: Python 3.10+, FastAPI, Celery, SQLAlchemy
- **EN**: Tauri 2.0, Rust
- **EN**: SQLite (EN)
- **Task Queue**: Celery with SQLite transport
- **AIEN**: OpenAI, DashScope, Google Gemini
- **EN**: Whisper, ENAPI

## 🛠️ EN

### EN

- **Node.js**: 18.0+
- **Python**: 3.10+（EN 3.11）
- **Rust**: 1.70+
- **Git**: 2.0+

### EN

1. **EN**
```bash
git clone https://github.com/your-org/autoclip-desktop.git
cd autoclip-desktop
```

2. **EN**
```bash
cd frontend
npm install
```

3. **EN**
```bash
cd ../backend
pip install -r requirements.txt
```

4. **ENTauriEN**
```bash
cd ../src-tauri
cargo install tauri-cli
```

5. **EN**
```bash
# EN
cp .env.example .env

# EN
nano .env
```

### EN

```bash
# EN
npm run dev

# EN
python backend/desktop_main.py

# ENTauriEN
npm run tauri build
```

## 📁 EN

### EN

```
frontend/
├── src/
│   ├── components/          # EN
│   │   ├── ErrorBoundary.tsx
│   │   ├── OfflineIndicator.tsx
│   │   └── ...
│   ├── pages/              # EN
│   │   ├── HomePage.tsx
│   │   ├── SettingsPage.tsx
│   │   ├── OnboardingPage.tsx
│   │   └── ...
│   ├── hooks/              # ENHooks
│   │   ├── useFirstRun.ts
│   │   ├── useDesktopConfig.ts
│   │   └── ...
│   ├── services/           # APIEN
│   │   ├── api.ts
│   │   ├── projectApi.ts
│   │   └── ...
│   ├── store/              # EN
│   │   ├── useProjectStore.ts
│   │   ├── useConfigStore.ts
│   │   └── ...
│   ├── utils/              # EN
│   │   ├── apiUtils.ts
│   │   ├── errorHandler.ts
│   │   └── ...
│   └── types/              # EN
│       ├── api.ts
│       ├── project.ts
│       └── ...
├── public/                 # EN
└── package.json
```

### EN

```
backend/
├── api/                    # APIEN
│   └── v1/
│       ├── projects.py
│       ├── settings.py
│       ├── health.py
│       └── ...
├── core/                   # EN
│   ├── desktop_config.py
│   ├── llm_providers.py
│   ├── speech_recognition.py
│   └── ...
├── services/               # EN
│   ├── project_service.py
│   ├── video_service.py
│   ├── ai_service.py
│   └── ...
├── models/                 # EN
│   ├── project.py
│   ├── clip.py
│   └── ...
├── utils/                  # EN
│   ├── error_handler.py
│   ├── performance_config.py
│   ├── chunked_upload.py
│   └── ...
├── tasks/                  # CeleryEN
│   ├── __init__.py
│   ├── video_tasks.py
│   └── ...
├── desktop_main.py         # EN
├── desktop_celery.py       # ENCeleryEN
└── requirements.txt
```

### TauriEN

```
src-tauri/
├── src/
│   ├── lib.rs              # EN
│   ├── commands.rs         # TauriEN
│   ├── backend_manager.rs  # EN
│   └── tray.rs             # EN
├── Cargo.toml              # RustEN
├── tauri.conf.json         # TauriEN
└── resources/              # EN
    └── ffmpeg/             # FFmpegEN
```

## 🔧 EN

### 1. EN

**EN**: `backend/core/desktop_config.py`

```python
class DesktopConfig:
    """EN"""
    
    def __init__(self):
        self.data_dir = self._get_desktop_data_dir()
        self.config_file = self.data_dir / "config.json"
        self.settings_file = self.data_dir / "settings.json"
    
    def save_desktop_config(self, config: 'DesktopConfig') -> bool:
        """EN"""
        try:
            config_dict = config.dict()
            # ENPathEN
            config_dict = self._convert_paths_to_strings(config_dict)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"EN: {e}")
            return False
```

### 2. EN

**EN**: `backend/core/speech_recognition.py`

```python
class SpeechRecognizer:
    """EN"""
    
    def __init__(self, config: SpeechRecognitionConfig):
        self.config = config
        self.recognizer = self._create_recognizer()
    
    def transcribe_audio(self, audio_path: str) -> str:
        """EN"""
        if self.config.provider == "whisper_local":
            return self._transcribe_with_whisper(audio_path)
        elif self.config.provider == "openai":
            return self._transcribe_with_openai(audio_path)
        # ... EN
```

### 3. Performance

**EN**: `backend/utils/performance_config.py`

```python
class PerformanceConfig:
    """EN"""
    
    def __init__(self, level: str = "medium"):
        self.level = level
        self.settings = self._get_settings_for_level(level)
    
    def _get_settings_for_level(self, level: str) -> PerformanceSettings:
        """EN"""
        levels = {
            "low": PerformanceSettings(
                max_concurrent_tasks=1,
                chunk_size_mb=5,
                upload_timeout_seconds=300
            ),
            "medium": PerformanceSettings(
                max_concurrent_tasks=2,
                chunk_size_mb=10,
                upload_timeout_seconds=600
            ),
            "high": PerformanceSettings(
                max_concurrent_tasks=4,
                chunk_size_mb=20,
                upload_timeout_seconds=1200
            )
        }
        return levels.get(level, levels["medium"])
```

## 🔌 APIEN

### Project ManagementAPI

```python
# EN
@router.post("/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate):
    """EN"""
    return await project_service.create_project(project)

# EN
@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects():
    """EN"""
    return await project_service.get_projects()

# EN
@router.get("/projects/{project_id}", response_model=ProjectDetailResponse)
async def get_project(project_id: int):
    """EN"""
    return await project_service.get_project(project_id)
```

### ENAPI

```python
# EN
@router.put("/settings", response_model=SettingsResponse)
async def update_settings(settings: DesktopSettings):
    """EN"""
    config = get_desktop_config()
    config.settings = settings
    save_desktop_config(config)
    return SettingsResponse(success=True)

# ENAPIEN
@router.post("/settings/test-api", response_model=ApiTestResponse)
async def test_api_connection(request: TestApiRequest):
    """ENAPIEN"""
    provider = create_llm_provider(request.provider, request.api_key)
    success = provider.test_connection()
    return ApiTestResponse(success=success)
```

## 🎨 EN

### EN

**EN**: `frontend/src/store/useProjectStore.ts`

```typescript
interface ProjectStore {
  projects: Project[]
  currentProject: Project | null
  loading: boolean
  error: string | null
  
  // Actions
  fetchProjects: () => Promise<void>
  createProject: (project: ProjectCreate) => Promise<void>
  updateProject: (id: number, updates: Partial<Project>) => Promise<void>
  deleteProject: (id: number) => Promise<void>
}

export const useProjectStore = create<ProjectStore>((set, get) => ({
  projects: [],
  currentProject: null,
  loading: false,
  error: null,
  
  fetchProjects: async () => {
    set({ loading: true, error: null })
    try {
      const projects = await projectApi.getProjects()
      set({ projects, loading: false })
    } catch (error) {
      set({ error: error.message, loading: false })
    }
  },
  
  // ... ENactions
}))
```

### ENHooks

**EN**: `frontend/src/hooks/useFirstRun.ts`

```typescript
export const useFirstRun = () => {
  const [isFirstRun, setIsFirstRun] = useState<boolean | null>(null)
  const [loading, setLoading] = useState(true)
  
  const checkFirstRun = async () => {
    try {
      const config = await configApi.getConfig()
      const hasApiKey = !!(config.settings?.llm?.api_key)
      setIsFirstRun(!hasApiKey)
    } catch (error) {
      console.error('EN:', error)
      setIsFirstRun(true)
    } finally {
      setLoading(false)
    }
  }
  
  useEffect(() => {
    checkFirstRun()
  }, [])
  
  return { isFirstRun, loading, refresh: checkFirstRun }
}
```

### EN

**EN**: `frontend/src/utils/errorHandler.ts`

```typescript
class ErrorHandler {
  private static instance: ErrorHandler
  
  public static getInstance(): ErrorHandler {
    if (!ErrorHandler.instance) {
      ErrorHandler.instance = new ErrorHandler()
    }
    return ErrorHandler.instance
  }
  
  public handleError(error: any, category: ErrorCategory = 'SYSTEM', context?: string) {
    let errorMessage = 'EN，EN'
    let errorLevel: 'error' | 'warning' | 'info' = 'error'
    
    if (error.response) {
      // ENHTTPEN
      errorMessage = error.response.data?.message || `EN: ${error.response.status}`
      if (error.response.status === 429) {
        errorMessage = 'EN，EN'
        errorLevel = 'warning'
      }
    } else if (error.request) {
      // EN
      errorMessage = 'EN，EN'
    } else if (error.message) {
      // EN
      errorMessage = error.message
    }
    
    const finalMessage = context ? `[${context}] ${errorMessage}` : errorMessage
    console.error(`[${category} Error] ${finalMessage}`, error)
    
    if (errorLevel === 'warning') {
      message.warning(finalMessage)
    } else {
      message.error(finalMessage)
    }
  }
}
```

## 🐍 EN

### EN

**EN**: `backend/desktop_main.py`

```python
class DesktopServiceManager:
    """EN"""
    
    def __init__(self, config: DesktopConfig):
        self.config = config
        self.is_running = False
        self.server_thread = None
        self.celery_worker_process = None
    
    def start(self):
        """EN"""
        if self.is_running:
            return
        
        try:
            # ENFastAPIEN
            self._start_fastapi_server()
            
            # ENCelery Worker
            self._start_celery_worker()
            
            self.is_running = True
            self.start_time = time.time()
            logger.info("✅ EN")
            
        except Exception as e:
            logger.error(f"❌ EN: {e}")
            self.stop()
            raise
    
    def stop(self):
        """EN"""
        if not self.is_running:
            return
        
        try:
            # ENCelery WorkerEN
            if hasattr(self, 'celery_worker_process') and self.celery_worker_process:
                self.celery_worker_process.terminate()
                self.celery_worker_process.wait(timeout=5)
            
            # ENFastAPIEN
            if self.server_thread and self.server_thread.is_alive():
                self.server_thread.join(timeout=5)
            
            self.is_running = False
            logger.info("✅ EN")
            
        except Exception as e:
            logger.error(f"❌ EN: {e}")
```

### EN

**EN**: `backend/tasks/video_tasks.py`

```python
@celery_app.task(bind=True)
def process_video_task(self, project_id: int, video_path: str):
    """EN"""
    try:
        # EN
        self.update_state(state='PROGRESS', meta={'status': 'EN'})
        
        # EN
        audio_path = extract_audio(video_path)
        self.update_state(state='PROGRESS', meta={'status': 'EN'})
        
        # EN
        transcript = transcribe_audio(audio_path)
        self.update_state(state='PROGRESS', meta={'status': 'EN'})
        
        # EN
        clips = generate_clips(transcript, video_path)
        self.update_state(state='PROGRESS', meta={'status': 'EN'})
        
        # EN
        save_project_results(project_id, clips)
        
        return {'status': 'EN', 'clips_count': len(clips)}
        
    except Exception as e:
        logger.error(f"EN: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)
```

### EN

**EN**: `backend/utils/error_handler.py`

```python
class AutoClipsException(Exception):
    """AutoClipEN"""
    
    def __init__(self, 
                 message: str, 
                 category: ErrorCategory = ErrorCategory.SYSTEM,
                 error_code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
                 details: dict = None):
        self.message = message
        self.category = category
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

def handle_autoclips_exception(exc: AutoClipsException, request_id: str = None) -> JSONResponse:
    """ENAutoClipEN"""
    status_code = 500
    if exc.category == ErrorCategory.VALIDATION:
        status_code = 422
    elif exc.category == ErrorCategory.CONFIGURATION:
        status_code = 400
    elif exc.category == ErrorCategory.NETWORK:
        status_code = 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error_code": exc.error_code.value,
            "message": exc.message,
            "details": exc.details,
            "request_id": request_id,
            "timestamp": time.time()
        }
    )
```

## 🦀 TauriEN

### EN

**EN**: `src-tauri/src/commands.rs`

```rust
#[tauri::command]
pub async fn start_backend_service(
    manager: State<'_, BackendManager>
) -> Result<BackendStatus, String> {
    match manager.start().await {
        Ok(_) => Ok(BackendStatus::Running),
        Err(e) => Err(format!("EN: {}", e)),
    }
}

#[tauri::command]
pub async fn stop_backend_service(
    manager: State<'_, BackendManager>
) -> Result<BackendStatus, String> {
    match manager.stop().await {
        Ok(_) => Ok(BackendStatus::Stopped),
        Err(e) => Err(format!("EN: {}", e)),
    }
}

#[tauri::command]
pub async fn get_service_status(
    manager: State<'_, BackendManager>
) -> Result<BackendStatus, String> {
    Ok(manager.get_status().await)
}
```

### EN

**EN**: `src-tauri/src/backend_manager.rs`

```rust
pub struct BackendManager {
    status: BackendStatus,
    process: Option<Child>,
}

impl BackendManager {
    pub fn new() -> Self {
        Self {
            status: BackendStatus::Stopped,
            process: None,
        }
    }
    
    pub async fn start(&mut self) -> Result<(), String> {
        if self.status == BackendStatus::Running {
            return Ok(());
        }
        
        // EN
        let mut cmd = Command::new("python")
            .arg("backend/desktop_main.py")
            .current_dir(std::env::current_dir().unwrap())
            .spawn()
            .map_err(|e| format!("EN: {}", e))?;
        
        self.process = Some(cmd);
        self.status = BackendStatus::Running;
        
        Ok(())
    }
    
    pub async fn stop(&mut self) -> Result<(), String> {
        if let Some(mut process) = self.process.take() {
            process.kill().map_err(|e| format!("EN: {}", e))?;
        }
        
        self.status = BackendStatus::Stopped;
        Ok(())
    }
}
```

### EN

**EN**: `src-tauri/src/tray.rs`

```rust
pub fn setup_system_tray(app_handle: &AppHandle) -> Result<(), Box<dyn std::error::Error>> {
    let tray_menu = MenuBuilder::new()
        .item(&MenuItem::new("EN", "show_main_window"))
        .separator()
        .item(&MenuItem::new("EN", "start_service"))
        .item(&MenuItem::new("EN", "stop_service"))
        .separator()
        .item(&MenuItem::new("EN", "quit_app"))
        .build()?;
    
    let _tray = TrayIconBuilder::new()
        .icon(app_handle.default_window_icon().unwrap().clone())
        .menu(&tray_menu)
        .on_menu_event(move |app, event| {
            match event.id.as_ref() {
                "show_main_window" => {
                    if let Some(window) = app.get_window("main") {
                        let _ = window.show();
                        let _ = window.set_focus();
                    }
                }
                "start_service" => {
                    // EN
                }
                "stop_service" => {
                    // EN
                }
                "quit_app" => {
                    app.exit(0);
                }
                _ => {}
            }
        })
        .build(app_handle)?;
    
    Ok(())
}
```

## 🏗️ EN

### EN

```bash
# EN
npm run dev

# EN
npm run build

# EN
npm run preview
```

### EN

```bash
# EN
pip install -r requirements.txt

# EN
pytest

# EN
flake8 backend/
black backend/
```

### TauriEN

```bash
# EN
npm run tauri dev

# EN
npm run tauri build

# EN
npm run tauri build -- --target x86_64-apple-darwin  # macOS Intel
npm run tauri build -- --target aarch64-apple-darwin # macOS ARM
npm run tauri build -- --target x86_64-pc-windows-msvc # Windows
npm run tauri build -- --target x86_64-unknown-linux-gnu # Linux
```

### EN

```bash
# EN
npm run build:all

# EN
npm run build:macos
npm run build:windows
npm run build:linux
```

## 🧪 EN

### EN

```bash
# EN
npm test

# EN
npm run test:coverage

# ENE2EEN
npm run test:e2e
```

### EN

```bash
# EN
pytest

# EN
pytest tests/test_project_service.py

# EN
pytest --cov=backend tests/

# EN
pytest tests/performance/
```

### EN

```bash
# EN
docker-compose -f docker-compose.test.yml up -d

# EN
pytest tests/integration/

# EN
docker-compose -f docker-compose.test.yml down
```

## 🤝 Contributing

### EN

1. **ForkEN**
   ```bash
   git clone https://github.com/your-username/autoclip-desktop.git
   cd autoclip-desktop
   ```

2. **EN**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **EN**
   - EN
   - EN
   - EN

4. **EN**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   git push origin feature/your-feature-name
   ```

5. **ENPull Request**
   - ENGitHubENPR
   - EN
   - ENCode Review

### EN

#### EN

- ENTypeScript
- ENESLintEN
- ENPrettierEN
- EN
- ENHooksEN

#### EN

- ENPython 3.10+
- ENPEP 8EN
- EN
- EN
- ENPydanticEN

#### RustEN

- ENRust 1.70+
- ENClippyEN
- ENrustfmtEN
- EN
- ENResultEN

### EN

```
<type>(<scope>): <subject>

<body>

<footer>
```

**EN**:
- `feat`: EN
- `fix`: ENbug
- `docs`: EN
- `style`: EN
- `refactor`: EN
- `test`: EN
- `chore`: EN/EN

**EN**:
```
feat(api): add project creation endpoint

Add new API endpoint for creating projects with validation
and error handling.

Closes #123
```

### EN

- EN
- EN80%
- EN
- EN

### EN

- EN
- ENAPIEN
- EN
- EN

## 📚 EN

- [TauriEN](https://tauri.app/)
- [FastAPIEN](https://fastapi.tiangolo.com/)
- [ReactEN](https://react.dev/)
- [Ant DesignEN](https://ant.design/)
- [RustEN](https://doc.rust-lang.org/)

## 🆘 EN

- **GitHub Issues**: ENbugEN
- **Discussions**: EN
- **Discord**: EN
- **EN**: ContactEN

---

🎉 **EN！**
