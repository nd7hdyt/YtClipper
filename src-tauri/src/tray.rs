use tauri::{
    menu::{MenuBuilder, MenuItem},
    tray::TrayIconBuilder,
    AppHandle, Manager,
};

pub fn setup_system_tray(app: &AppHandle) -> Result<(), Box<dyn std::error::Error>> {
    // createtranslated
    let show = MenuItem::with_id(app, "show", "translated", true, None::<&str>)?;
    let hide = MenuItem::with_id(app, "hide", "translated", true, None::<&str>)?;
    let separator = MenuItem::with_id(app, "separator1", "", false, None::<&str>)?;
    let start_backend =
        MenuItem::with_id(app, "start_backend", "startbackendservice", true, None::<&str>)?;
    let stop_backend = MenuItem::with_id(app, "stop_backend", "translatedbackendservice", true, None::<&str>)?;
    let restart_backend =
        MenuItem::with_id(app, "restart_backend", "translatedbackendservice", true, None::<&str>)?;
    let separator2 = MenuItem::with_id(app, "separator2", "", false, None::<&str>)?;
    let quit = MenuItem::with_id(app, "quit", "translateduse", true, None::<&str>)?;

    // translated
    let menu = MenuBuilder::new(app)
        .item(&show)
        .item(&hide)
        .item(&separator)
        .item(&start_backend)
        .item(&stop_backend)
        .item(&restart_backend)
        .item(&separator2)
        .item(&quit)
        .build()?;

    // createtranslated
    let _tray = TrayIconBuilder::with_id("main-tray")
        .icon(app.default_window_icon().unwrap().clone())
        .menu(&menu)
        .on_menu_event(move |app, event| {
            match event.id.as_ref() {
                "show" => {
                    if let Some(window) = app.get_webview_window("main") {
                        let _ = window.show();
                        let _ = window.set_focus();
                    }
                }
                "hide" => {
                    if let Some(window) = app.get_webview_window("main") {
                        let _ = window.hide();
                    }
                }
                "start_backend" => {
                    // startbackendservice
                    let backend_manager = app.state::<crate::BackendManager>();
                    match backend_manager.start(app.app_handle().clone()) {
                        Ok(_) => {
                            println!("backendservicestartsucceeded");
                        }
                        Err(e) => {
                            eprintln!("backendservicestartfailed: {}", e);
                        }
                    }
                }
                "stop_backend" => {
                    // translatedbackendservice
                    let backend_manager = app.state::<crate::BackendManager>();
                    match backend_manager.stop() {
                        Ok(_) => {
                            println!("backendservicetranslatedsucceeded");
                        }
                        Err(e) => {
                            eprintln!("backendservicetranslatedfailed: {}", e);
                        }
                    }
                }
                "restart_backend" => {
                    // translatedbackendservice
                    let backend_manager = app.state::<crate::BackendManager>();
                    match backend_manager.restart(app.app_handle().clone()) {
                        Ok(_) => {
                            println!("backendservicetranslatedsucceeded");
                        }
                        Err(e) => {
                            eprintln!("backendservicetranslatedfailed: {}", e);
                        }
                    }
                }
                "quit" => {
                    // translateduse
                    app.exit(0);
                }
                _ => {}
            }
        })
        .build(app)?;

    Ok(())
}
