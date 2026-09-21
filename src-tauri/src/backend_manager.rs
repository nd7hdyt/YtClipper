use serde::{Deserialize, Serialize};
use std::io::{BufRead, BufReader};
use std::net::{SocketAddr, TcpStream};
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use tauri::{AppHandle, Emitter, Manager};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BackendStatus {
    pub is_running: bool,
    pub port: u16,
    pub pid: Option<u32>,
    pub start_time: Option<u64>, // changed to u64 for serialization
}

impl Default for BackendStatus {
    fn default() -> Self {
        Self {
            is_running: false,
            port: 8000,
            pid: None,
            start_time: None,
        }
    }
}

pub struct BackendManager {
    status: Arc<Mutex<BackendStatus>>,
    process: Arc<Mutex<Option<Child>>>,
}

struct BackendLaunch {
    program: String,
    args: Vec<String>,
    working_dir: PathBuf,
}

impl BackendManager {
    pub fn new() -> Self {
        Self {
            status: Arc::new(Mutex::new(BackendStatus::default())),
            process: Arc::new(Mutex::new(None)),
        }
    }

    pub fn start(&self, app_handle: AppHandle) -> Result<(), String> {
        let mut status = self.status.lock().unwrap();
        if status.is_running {
            return Err("Backend service already running".to_string());
        }

        // Start backend service
        let launch = self.get_backend_launch(&app_handle)?;

        let mut cmd = Command::new(&launch.program);
        cmd.args(&launch.args)
            .current_dir(&launch.working_dir)
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .env("AUTOCLIP_DESKTOP_MODE", "true")
            .env("AUTOCLIP_MODE", "desktop")
            // Single source of truth for the version the backend reports in /settings.
            .env("AUTOCLIP_APP_VERSION", env!("CARGO_PKG_VERSION"));

        // Point the backend at the bundled ffmpeg/ffprobe when present.
        // The backend's ffmpeg_utils reads these env vars before falling back
        // to PATH, so this is what makes video processing work on machines
        // without a system ffmpeg installed.
        let ffmpeg_bin = launch
            .working_dir
            .join("ffmpeg")
            .join(Self::exe_name("ffmpeg"));
        if ffmpeg_bin.is_file() {
            cmd.env("AUTOCLIP_FFMPEG_PATH", &ffmpeg_bin);
        }
        let ffprobe_bin = launch
            .working_dir
            .join("ffmpeg")
            .join(Self::exe_name("ffprobe"));
        if ffprobe_bin.is_file() {
            cmd.env("AUTOCLIP_FFPROBE_PATH", &ffprobe_bin);
        }

        // The backend prints emoji/Chinese to stdout; with a piped stdout on
        // Windows Python falls back to the ANSI code page and dies with
        // UnicodeEncodeError before it ever reaches "PORT=". Force UTF-8.
        cmd.env("PYTHONUTF8", "1");
        cmd.env("PYTHONIOENCODING", "utf-8");

        // Backend defaults its data dir to ~/Library/Application Support/AutoClip,
        // which only makes sense on macOS. Resolve the platform data dir here
        // (%APPDATA%\AutoClip on Windows, ~/.local/share/AutoClip on Linux) —
        // on macOS this is exactly the old default, so existing installs keep
        // their data.
        if std::env::var_os("AUTOCLIP_APP_DIR").is_none() {
            if let Ok(data_dir) = app_handle.path().data_dir() {
                cmd.env("AUTOCLIP_APP_DIR", data_dir.join("AutoClip"));
            }
        }

        #[cfg(target_os = "windows")]
        {
            use std::os::windows::process::CommandExt;
            const CREATE_NO_WINDOW: u32 = 0x0800_0000;
            // Without this every launch pops a black console window for python.exe.
            cmd.creation_flags(CREATE_NO_WINDOW);
        }

        match cmd.spawn() {
            Ok(child) => {
                let pid = child.id();
                let start_time = SystemTime::now()
                    .duration_since(UNIX_EPOCH)
                    .map(|duration| duration.as_secs())
                    .unwrap_or(0);

                // Set to running at start, port unknown
                *status = BackendStatus {
                    is_running: true,
                    port: 0, // port will be updated after reading stdout
                    pid: Some(pid),
                    start_time: Some(start_time),
                };

                let mut process = self.process.lock().unwrap();
                *process = Some(child);

                // Start port reading and health check
                let status_clone = self.status.clone();
                let process_clone = self.process.clone();
                let app_handle_clone = app_handle.clone();

                thread::spawn(move || {
                    Self::read_port_and_health_check(status_clone, process_clone, app_handle_clone);
                });

                Ok(())
            }
            Err(e) => Err(format!("Failed to start backend service: {}", e)),
        }
    }

    pub fn stop(&self) -> Result<(), String> {
        let mut status = self.status.lock().unwrap();
        if !status.is_running {
            return Err("Backend service not running".to_string());
        }

        let mut process = self.process.lock().unwrap();
        if let Some(mut child) = process.take() {
            if let Err(e) = child.kill() {
                return Err(format!("Failed to stop backend service: {}", e));
            }
            let _ = child.wait();
        }

        *status = BackendStatus::default();
        Ok(())
    }

    pub fn restart(&self, app_handle: AppHandle) -> Result<(), String> {
        // Stop first
        if let Err(e) = self.stop() {
            return Err(format!("Failed to stop backend service: {}", e));
        }

        // Wait one second
        std::thread::sleep(Duration::from_secs(1));

        // then start
        self.start(app_handle)
    }

    pub fn get_status(&self) -> BackendStatus {
        self.status.lock().unwrap().clone()
    }

    fn get_backend_launch(&self, app_handle: &AppHandle) -> Result<BackendLaunch, String> {
        if let Ok(resource_path) = app_handle.path().resource_dir() {
            for backend_work_dir in [resource_path.clone(), resource_path.join("resources")] {
                for backend_binary in [
                    backend_work_dir.join(Self::backend_binary_name()),
                    backend_work_dir
                        .join("autoclip-backend")
                        .join(Self::backend_binary_name()),
                ] {
                    if backend_binary.is_file() {
                        let working_dir = backend_binary
                            .parent()
                            .map(|path| path.to_path_buf())
                            .unwrap_or_else(|| backend_work_dir.clone());
                        return Ok(BackendLaunch {
                            program: backend_binary.to_string_lossy().to_string(),
                            args: Vec::new(),
                            working_dir,
                        });
                    }
                }

                let backend_dir = backend_work_dir.join("backend");
                if !backend_dir.exists() {
                    continue;
                }

                let venv_python = Self::venv_python(&backend_work_dir);
                if venv_python.exists() {
                    return Ok(Self::python_launch(
                        venv_python.to_string_lossy().to_string(),
                        backend_work_dir,
                    ));
                }

                // python-build-standalone bundle:
                //   unix:    resources/python/bin/python3
                //   windows: resources/python/python.exe
                let pbs_python = Self::pbs_python(&backend_work_dir);
                if pbs_python.exists() {
                    return Ok(Self::python_launch(
                        pbs_python.to_string_lossy().to_string(),
                        backend_work_dir,
                    ));
                }

                if let Some(system_python) = Self::system_python() {
                    return Ok(Self::python_launch(system_python, backend_work_dir));
                }
            }
        }

        // EN
        if let Ok(current_dir) = std::env::current_dir() {
            if let Some(project_root) = current_dir.parent() {
                let backend_dir = project_root.join("backend");
                if backend_dir.exists() {
                    let venv_python = Self::venv_python(project_root);
                    if venv_python.exists() {
                        return Ok(Self::python_launch(
                            venv_python.to_string_lossy().to_string(),
                            project_root.to_path_buf(),
                        ));
                    }
                    if let Some(system_python) = Self::system_python() {
                        return Ok(Self::python_launch(
                            system_python,
                            project_root.to_path_buf(),
                        ));
                    }
                }
            }
        }

        if let Ok(current_dir) = std::env::current_dir() {
            let backend_dir = current_dir.join("backend");
            if backend_dir.exists() {
                let venv_python = Self::venv_python(&current_dir);
                if venv_python.exists() {
                    return Ok(Self::python_launch(
                        venv_python.to_string_lossy().to_string(),
                        current_dir,
                    ));
                }
                if let Some(system_python) = Self::system_python() {
                    return Ok(Self::python_launch(system_python, current_dir));
                }
            }
        }

        Err("No available Python environment or backend code found".to_string())
    }

    fn exe_name(base: &str) -> String {
        if cfg!(target_os = "windows") {
            format!("{}.exe", base)
        } else {
            base.to_string()
        }
    }

    fn venv_python(root: &std::path::Path) -> PathBuf {
        if cfg!(target_os = "windows") {
            root.join("venv").join("Scripts").join("python.exe")
        } else {
            root.join("venv").join("bin").join("python")
        }
    }

    fn pbs_python(root: &std::path::Path) -> PathBuf {
        if cfg!(target_os = "windows") {
            root.join("python").join("python.exe")
        } else {
            root.join("python").join("bin").join("python3")
        }
    }

    /// First interpreter on PATH that answers `--version`. On Windows `python3`
    /// is usually the Microsoft Store stub, so prefer plain `python` there.
    fn system_python() -> Option<String> {
        let candidates: [&str; 2] = if cfg!(target_os = "windows") {
            ["python", "python3"]
        } else {
            ["python3", "python"]
        };
        candidates
            .iter()
            .find(|name| Command::new(name).arg("--version").output().is_ok())
            .map(|name| name.to_string())
    }

    fn python_launch(program: String, working_dir: PathBuf) -> BackendLaunch {
        BackendLaunch {
            program,
            args: vec!["-m".to_string(), "backend.desktop_main".to_string()],
            working_dir,
        }
    }

    fn backend_binary_name() -> &'static str {
        if cfg!(target_os = "windows") {
            "autoclip-backend.exe"
        } else {
            "autoclip-backend"
        }
    }

    fn read_port_and_health_check(
        status: Arc<Mutex<BackendStatus>>,
        process: Arc<Mutex<Option<Child>>>,
        app_handle: AppHandle,
    ) {
        let (stdout, stderr) = {
            let mut process_guard = process.lock().unwrap();
            if let Some(child) = process_guard.as_mut() {
                (child.stdout.take(), child.stderr.take())
            } else {
                (None, None)
            }
        };

        if let Some(stderr) = stderr {
            thread::spawn(move || {
                let reader = BufReader::new(stderr);
                for line in reader.lines().flatten() {
                    eprintln!("Backend error: {}", line);
                }
            });
        }

        if let Some(stdout) = stdout {
            let reader = BufReader::new(stdout);
            let mut emitted_started = false;

            for line in reader.lines().flatten() {
                println!("Backend output: {}", line);

                if !emitted_started && line.starts_with("PORT=") {
                    if let Some(port_str) = line.strip_prefix("PORT=") {
                        if let Ok(port) = port_str.parse::<u16>() {
                            let backend_status = {
                                let mut status_guard = status.lock().unwrap();
                                status_guard.port = port;
                                BackendStatus {
                                    is_running: true,
                                    port,
                                    pid: status_guard.pid,
                                    start_time: status_guard.start_time,
                                }
                            };

                            let _ = app_handle.emit("backend-started", backend_status);
                            println!("Backend started on port: {}", port);

                            let status_health = status.clone();
                            let process_health = process.clone();
                            thread::spawn(move || {
                                Self::health_check_loop(status_health, process_health);
                            });

                            emitted_started = true;
                        }
                    }
                }
            }
        }
    }

    fn health_check_loop(status: Arc<Mutex<BackendStatus>>, process: Arc<Mutex<Option<Child>>>) {
        loop {
            thread::sleep(Duration::from_secs(5));

            // Check status
            let should_continue = {
                let status_guard = status.lock().unwrap();
                status_guard.is_running
            };

            if !should_continue {
                break;
            }

            // Check if process still running
            let process_exited = {
                let mut process_guard = process.lock().unwrap();
                if let Some(ref mut child) = process_guard.as_mut() {
                    match child.try_wait() {
                        Ok(Some(_)) => {
                            // Process exited
                            *process_guard = None;
                            true
                        }
                        Ok(None) => false, // Process still running
                        Err(_) => {
                            // Failed to check process status
                            *process_guard = None;
                            true
                        }
                    }
                } else {
                    true
                }
            };

            if process_exited {
                // Update status
                let mut status_guard = status.lock().unwrap();
                *status_guard = BackendStatus::default();
                break;
            }

            // Health check
            let port = {
                let status_guard = status.lock().unwrap();
                status_guard.port
            };

            if port > 0 {
                let addr = SocketAddr::from(([127, 0, 0, 1], port));
                if TcpStream::connect_timeout(&addr, Duration::from_secs(2)).is_err() {
                    eprintln!("Backend health check failed: port {} unreachable", port);
                }
            }
        }
    }
}
