# 👨‍💻 AutoClip Desktop 

## 📋 

- [project](#project)
- [dev environmentsettings](#dev environmentsettings)
- [](#)
- [core modules](#core modules)
- [APIAPI](#apiAPI)
- [frontend dev](#frontend dev)
- [backend dev](#backend dev)
- [Tauriintegration](#tauriintegration)
- [builddeploy](#builddeploy)
- [test](#test)
- [contributing guide](#contributing guide)

## 🏗️ project

### 

```
AutoClip Desktop
├── Frontend (React + TypeScript + Ant Design)
├── Backend (Python + FastAPI + Celery)
├── Tauri (Rust + WebView)
└── Resources (FFmpeg + modelfile)
```

### 

- **frontend**: React 18, TypeScript, Ant Design, Vite
- **backend**: Python 3.10+, FastAPI, Celery, SQLAlchemy
- ****: Tauri 2.0, Rust
- **database**: SQLite ()
- ****: Celery with SQLite transport
- **AIservice**: OpenAI, DashScope, Google Gemini
- **speech recognition**: Whisper, cloudAPI

## 🛠️ dev environmentsettings

### 

- **Node.js**: 18.0+
- **Python**: 3.10+（recommend 3.11）
- **Rust**: 1.70+
- **Git**: 2.0+

### installstep

1. **project**
```bash
git clone https://github.com/your-org/autoclip-desktop.git
cd autoclip-desktop
```

2. **installfrontenddependencies**
```bash
cd frontend
npm install
```

3. **installbackenddependencies**
```bash
cd ../backend
pip install -r requirements.txt
```

4. **installTauridependencies**
```bash
cd ../src-tauri
cargo install tauri-cli
```

5. **settingsenv var**
```bash
# env var
cp .env.example .env

# editenv var
nano .env
```

### dev environmentconfig

```bash
# startdev environment
npm run dev

# startbackendservice
python backend/desktop_main.py

# buildTauri
npm run tauri build
```

## 📁 

### frontend

```
frontend/
├── src/
│   ├── components/          # 
│   │   ├── ErrorBoundary.tsx
│   │   ├── OfflineIndicator.tsx
│   │   └── ...
│   ├── pages/              # page
│   │   ├── HomePage.tsx
│   │   ├── SettingsPage.tsx
│   │   ├── OnboardingPage.tsx
│   │   └── ...
│   ├── hooks/              # Hooks
│   │   ├── useFirstRun.ts
│   │   ├── useDesktopConfig.ts
│   │   └── ...
│   ├── services/           # APIservice
│   │   ├── api.ts
│   │   ├── projectApi.ts
│   │   └── ...
│   ├── store/              # state management
│   │   ├── useProjectStore.ts
│   │   ├── useConfigStore.ts
│   │   └── ...
│   ├── utils/              # tool
│   │   ├── apiUtils.ts
│   │   ├── errorHandler.ts
│   │   └── ...
│   └── types/              # 
│       ├── api.ts
│       ├── project.ts
│       └── ...
├── public/                 # 
└── package.json
```

### backend

```
backend/
├── api/                    # APIroute
│   └── v1/
│       ├── projects.py
│       ├── settings.py
│       ├── health.py
│       └── ...
├── core/                   # core modules
│   ├── desktop_config.py
│   ├── llm_providers.py
│   ├── speech_recognition.py
│   └── ...
├── services/               # service
│   ├── project_service.py
│   ├── video_service.py
│   ├── ai_service.py
│   └── ...
├── models/                 # model
│   ├── project.py
│   ├── clip.py
│   └── ...
├── utils/                  # tool
│   ├── error_handler.py
│   ├── performance_config.py
│   ├── chunked_upload.py
│   └── ...
├── tasks/                  # Celery
│   ├── __init__.py
│   ├── video_tasks.py
│   └── ...
├── desktop_main.py         # 
├── desktop_celery.py       # Celeryconfig
└── requirements.txt
```

### Tauri

```
src-tauri/
├── src/
│   ├── lib.rs              # 
│   ├── commands.rs         # Tauri
│   ├── backend_manager.rs  # backend
│   └── tray.rs             # 
├── Cargo.toml              # Rustdependencies
├── tauri.conf.json         # Tauriconfig
└── resources/              # file
    └── ffmpeg/             # FFmpeg
```

## 🔧 core modules

### 1. config

**file**: `backend/core/desktop_config.py`

```python
class DesktopConfig:
    """config"""
    
    def __init__(self):
        self.data_dir = self._get_desktop_data_dir()
        self.config_file = self.data_dir / "config.json"
        self.settings_file = self.data_dir / "settings.json"
    
    def save_desktop_config(self, config: 'DesktopConfig') -> bool:
        """config"""
        try:
            config_dict = config.dict()
            # Path
            config_dict = self._convert_paths_to_strings(config_dict)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"configfailed: {e}")
            return False
```

### 2. speech recognitionservice

**file**: `backend/core/speech_recognition.py`

```python
class SpeechRecognizer:
    """speech recognitionservice"""
    
    def __init__(self, config: SpeechRecognitionConfig):
        self.config = config
        self.recognizer = self._create_recognizer()
    
    def transcribe_audio(self, audio_path: str) -> str:
        """file"""
        if self.config.provider == "whisper_local":
            return self._transcribe_with_whisper(audio_path)
        elif self.config.provider == "openai":
            return self._transcribe_with_openai(audio_path)
        # ... service
```

### 3. performance

**file**: `backend/utils/performance_config.py`

```python
class PerformanceConfig:
    """config"""
    
    def __init__(self, level: str = "medium"):
        self.level = level
        self.settings = self._get_settings_for_level(level)
    
    def _get_settings_for_level(self, level: str) -> PerformanceSettings:
        """fetchsettings"""
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

## 🔌 APIAPI

### project managementAPI

```python
# createproject
@router.post("/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate):
    """createproject"""
    return await project_service.create_project(project)

# fetchproject
@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects():
    """fetchproject"""
    return await project_service.get_projects()

# fetchproject
@router.get("/projects/{project_id}", response_model=ProjectDetailResponse)
async def get_project(project_id: int):
    """fetchproject"""
    return await project_service.get_project(project_id)
```

### settingsAPI

```python
# updatesettings
@router.put("/settings", response_model=SettingsResponse)
async def update_settings(settings: DesktopSettings):
    """updatesettings"""
    config = get_desktop_config()
    config.settings = settings
    save_desktop_config(config)
    return SettingsResponse(success=True)

# testAPI
@router.post("/settings/test-api", response_model=ApiTestResponse)
async def test_api_connection(request: TestApiRequest):
    """testAPI"""
    provider = create_llm_provider(request.provider, request.api_key)
    success = provider.test_connection()
    return ApiTestResponse(success=success)
```

## 🎨 frontend dev

### state management

**file**: `frontend/src/store/useProjectStore.ts`

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
  
  // ... actions
}))
```

### Hooks

**file**: `frontend/src/hooks/useFirstRun.ts`

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
      console.error('checkstatusfailed:', error)
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

### error handling

**file**: `frontend/src/utils/errorHandler.ts`

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
    let errorMessage = 'error，'
    let errorLevel: 'error' | 'warning' | 'info' = 'error'
    
    if (error.response) {
      // HTTPerror
      errorMessage = error.response.data?.message || `servererror: ${error.response.status}`
      if (error.response.status === 429) {
        errorMessage = 'project，'
        errorLevel = 'warning'
      }
    } else if (error.request) {
      // error
      errorMessage = 'connection failed，checkbackendservice'
    } else if (error.message) {
      // error
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

## 🐍 backend dev

### service

**file**: `backend/desktop_main.py`

```python
class DesktopServiceManager:
    """service"""
    
    def __init__(self, config: DesktopConfig):
        self.config = config
        self.is_running = False
        self.server_thread = None
        self.celery_worker_process = None
    
    def start(self):
        """startservice"""
        if self.is_running:
            return
        
        try:
            # startFastAPIserver
            self._start_fastapi_server()
            
            # startCelery Worker
            self._start_celery_worker()
            
            self.is_running = True
            self.start_time = time.time()
            logger.info("✅ servicestartsucceeded")
            
        except Exception as e:
            logger.error(f"❌ servicestartfailed: {e}")
            self.stop()
            raise
    
    def stop(self):
        """service"""
        if not self.is_running:
            return
        
        try:
            # Celery Worker
            if hasattr(self, 'celery_worker_process') and self.celery_worker_process:
                self.celery_worker_process.terminate()
                self.celery_worker_process.wait(timeout=5)
            
            # FastAPIserver
            if self.server_thread and self.server_thread.is_alive():
                self.server_thread.join(timeout=5)
            
            self.is_running = False
            logger.info("✅ service")
            
        except Exception as e:
            logger.error(f"❌ servicefailed: {e}")
```

### 

**file**: `backend/tasks/video_tasks.py`

```python
@celery_app.task(bind=True)
def process_video_task(self, project_id: int, video_path: str):
    """"""
    try:
        # updatestatus
        self.update_state(state='PROGRESS', meta={'status': ''})
        
        # 
        audio_path = extract_audio(video_path)
        self.update_state(state='PROGRESS', meta={'status': 'completed'})
        
        # speech recognition
        transcript = transcribe_audio(audio_path)
        self.update_state(state='PROGRESS', meta={'status': 'speech recognitioncompleted'})
        
        # generateclip
        clips = generate_clips(transcript, video_path)
        self.update_state(state='PROGRESS', meta={'status': 'clipgeneratecompleted'})
        
        # 
        save_project_results(project_id, clips)
        
        return {'status': 'completed', 'clips_count': len(clips)}
        
    except Exception as e:
        logger.error(f"failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)
```

### error handling

**file**: `backend/utils/error_handler.py`

```python
class AutoClipsException(Exception):
    """AutoClip"""
    
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
    """AutoClip"""
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

## 🦀 Tauriintegration

### 

**file**: `src-tauri/src/commands.rs`

```rust
#[tauri::command]
pub async fn start_backend_service(
    manager: State<'_, BackendManager>
) -> Result<BackendStatus, String> {
    match manager.start().await {
        Ok(_) => Ok(BackendStatus::Running),
        Err(e) => Err(format!("startbackendservicefailed: {}", e)),
    }
}

#[tauri::command]
pub async fn stop_backend_service(
    manager: State<'_, BackendManager>
) -> Result<BackendStatus, String> {
    match manager.stop().await {
        Ok(_) => Ok(BackendStatus::Stopped),
        Err(e) => Err(format!("backendservicefailed: {}", e)),
    }
}

#[tauri::command]
pub async fn get_service_status(
    manager: State<'_, BackendManager>
) -> Result<BackendStatus, String> {
    Ok(manager.get_status().await)
}
```

### backend

**file**: `src-tauri/src/backend_manager.rs`

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
        
        // startbackend
        let mut cmd = Command::new("python")
            .arg("backend/desktop_main.py")
            .current_dir(std::env::current_dir().unwrap())
            .spawn()
            .map_err(|e| format!("startbackendfailed: {}", e))?;
        
        self.process = Some(cmd);
        self.status = BackendStatus::Running;
        
        Ok(())
    }
    
    pub async fn stop(&mut self) -> Result<(), String> {
        if let Some(mut process) = self.process.take() {
            process.kill().map_err(|e| format!("backendfailed: {}", e))?;
        }
        
        self.status = BackendStatus::Stopped;
        Ok(())
    }
}
```

### 

**file**: `src-tauri/src/tray.rs`

```rust
pub fn setup_system_tray(app_handle: &AppHandle) -> Result<(), Box<dyn std::error::Error>> {
    let tray_menu = MenuBuilder::new()
        .item(&MenuItem::new("", "show_main_window"))
        .separator()
        .item(&MenuItem::new("startservice", "start_service"))
        .item(&MenuItem::new("service", "stop_service"))
        .separator()
        .item(&MenuItem::new("", "quit_app"))
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
                    // startservice
                }
                "stop_service" => {
                    // service
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

## 🏗️ builddeploy

### frontendbuild

```bash
# dev environment
npm run dev

# build
npm run build

# build
npm run preview
```

### backendbuild

```bash
# installdependencies
pip install -r requirements.txt

# test
pytest

# check
flake8 backend/
black backend/
```

### Tauribuild

```bash
# dev mode
npm run tauri dev

# build
npm run tauri build

# build
npm run tauri build -- --target x86_64-apple-darwin  # macOS Intel
npm run tauri build -- --target aarch64-apple-darwin # macOS ARM
npm run tauri build -- --target x86_64-pc-windows-msvc # Windows
npm run tauri build -- --target x86_64-unknown-linux-gnu # Linux
```

### build

```bash
# build
npm run build:all

# build
npm run build:macos
npm run build:windows
npm run build:linux
```

## 🧪 test

### frontendtest

```bash
# test
npm test

# testgenerate
npm run test:coverage

# E2Etest
npm run test:e2e
```

### backendtest

```bash
# test
pytest

# test
pytest tests/test_project_service.py

# testgenerate
pytest --cov=backend tests/

# test
pytest tests/performance/
```

### integration test

```bash
# starttest
docker-compose -f docker-compose.test.yml up -d

# integration test
pytest tests/integration/

# test
docker-compose -f docker-compose.test.yml down
```

## 🤝 contributing guide

### 

1. **Forkproject**
   ```bash
   git clone https://github.com/your-username/autoclip-desktop.git
   cd autoclip-desktop
   ```

2. **create**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. ****
   - 
   - test
   - updatedocs

4. ****
   ```bash
   git add .
   git commit -m "feat: add your feature"
   git push origin feature/your-feature-name
   ```

5. **createPull Request**
   - GitHubcreatePR
   - 
   - 

### 

#### frontend

- useTypeScript
- followESLint
- usePrettierformat
- use
- useHooksstate management

#### backend

- usePython 3.10+
- followPEP 8
- use
- docs
- usePydanticverify

#### Rust

- useRust 1.70+
- followClippy
- userustfmtformat
- docs
- useResulterror

### 

```
<type>(<scope>): <subject>

<body>

<footer>
```

****:
- `feat`: 
- `fix`: fixbug
- `docs`: docsupdate
- `style`: format
- `refactor`: 
- `test`: test
- `chore`: build/tool

****:
```
feat(api): add project creation endpoint

Add new API endpoint for creating projects with validation
and error handling.

Closes #123
```

### test

- test
- test80%
- test
- testintegration test

### docs

- updaterelated docs
- APIdocs
- update
- 

## 📚 

- [Tauridocs](https://tauri.app/)
- [FastAPIdocs](https://fastapi.tiangolo.com/)
- [Reactdocs](https://react.dev/)
- [Ant Designdocs](https://ant.design/)
- [Rustdocs](https://doc.rust-lang.org/)

## 🆘 get help

- **GitHub Issues**: bug
- **Discussions**: issue
- **Discord**: 
- ****: 

---

🎉 **！**
