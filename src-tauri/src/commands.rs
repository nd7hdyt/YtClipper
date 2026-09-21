use crate::backend_manager::BackendStatus;
use tauri::{AppHandle, Manager, State};
use tauri_plugin_autostart::AutoLaunchManager;

#[tauri::command]
pub async fn start_backend_service(app_handle: AppHandle) -> Result<String, String> {
    let backend_manager = app_handle.state::<crate::BackendManager>();
    match backend_manager.start(app_handle.clone()) {
        Ok(_) => Ok("EN".to_string()),
        Err(e) => Err(e),
    }
}

#[tauri::command]
pub async fn stop_backend_service(app_handle: AppHandle) -> Result<String, String> {
    let backend_manager = app_handle.state::<crate::BackendManager>();
    match backend_manager.stop() {
        Ok(_) => Ok("EN".to_string()),
        Err(e) => Err(e),
    }
}

#[tauri::command]
pub async fn restart_backend_service(app_handle: AppHandle) -> Result<String, String> {
    let backend_manager = app_handle.state::<crate::BackendManager>();
    match backend_manager.restart(app_handle.clone()) {
        Ok(_) => Ok("EN".to_string()),
        Err(e) => Err(e),
    }
}

#[tauri::command]
pub async fn get_service_status(app_handle: AppHandle) -> Result<BackendStatus, String> {
    let backend_manager = app_handle.state::<crate::BackendManager>();
    Ok(backend_manager.get_status())
}

#[tauri::command]
pub async fn show_main_window(app_handle: AppHandle) -> Result<(), String> {
    if let Some(window) = app_handle.get_webview_window("main") {
        window.show().map_err(|e| e.to_string())?;
        window.set_focus().map_err(|e| e.to_string())?;
        Ok(())
    } else {
        Err("EN".to_string())
    }
}

#[tauri::command]
pub async fn quit_app(app_handle: AppHandle) -> Result<(), String> {
    // Stop backend service
    let backend_manager = app_handle.state::<crate::BackendManager>();
    let _ = backend_manager.stop();

    // EN
    app_handle.exit(0);
    Ok(())
}

#[tauri::command]
pub async fn enable_autostart(manager: State<'_, AutoLaunchManager>) -> Result<bool, String> {
    match manager.enable() {
        Ok(_) => Ok(true),
        Err(e) => Err(format!("EN: {}", e)),
    }
}

#[tauri::command]
pub async fn disable_autostart(manager: State<'_, AutoLaunchManager>) -> Result<bool, String> {
    match manager.disable() {
        Ok(_) => Ok(false),
        Err(e) => Err(format!("EN: {}", e)),
    }
}

#[tauri::command]
pub async fn is_autostart_enabled(manager: State<'_, AutoLaunchManager>) -> Result<bool, String> {
    match manager.is_enabled() {
        Ok(enabled) => Ok(enabled),
        Err(e) => Err(format!("EN: {}", e)),
    }
}
