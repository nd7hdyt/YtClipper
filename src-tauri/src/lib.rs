use crate::backend_manager::BackendManager;
use crate::commands::*;
use crate::tray::setup_system_tray;
use tauri::Manager;

mod backend_manager;
mod commands;
mod tray;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_autostart::init(
            tauri_plugin_autostart::MacosLauncher::LaunchAgent,
            None,
        ))
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            start_backend_service,
            stop_backend_service,
            restart_backend_service,
            get_service_status,
            show_main_window,
            quit_app,
            enable_autostart,
            disable_autostart,
            is_autostart_enabled
        ])
        .manage(BackendManager::new())
        .setup(|app| {
            // EN
            std::env::set_var("AUTOCLIP_DESKTOP_MODE", "true");
            std::env::set_var("AUTOCLIP_MODE", "desktop");

            // EN
            if let Err(e) = setup_system_tray(&app.handle()) {
                eprintln!("EN: {}", e);
            }

            let backend_manager = app.state::<BackendManager>();
            match backend_manager.start(app.handle().clone()) {
                Ok(_) => {
                    println!("EN");
                }
                Err(e) => {
                    eprintln!("EN: {}", e);
                    eprintln!("EN，EN");
                }
            }

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
