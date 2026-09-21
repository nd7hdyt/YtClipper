"""
translatedstartfile
usetranslatedone's app_factory createtranslateduse，supporttranslated
"""
import os
import sys
import logging
import signal
import socket
import threading
import time
import uvicorn
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import FastAPI

# addprojecttranslateddirectorytranslatedPythonpath
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

app_data_dir = Path(os.getenv("AUTOCLIP_APP_DIR", "~/Library/Application Support/AutoClip")).expanduser()
app_data_dir.mkdir(parents=True, exist_ok=True)
(app_data_dir / "logs").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("AUTOCLIP_APP_DIR", str(app_data_dir))
os.environ.setdefault("AUTOCLIP_DATA_DIR", str(app_data_dir))
os.environ.setdefault("DATABASE_URL", f"sqlite:///{app_data_dir / 'autoclip.db'}")
os.environ.setdefault("LOG_FILE", str(app_data_dir / "logs" / "backend.log"))

from backend.app_factory import create_app
from backend.core.desktop_config import (
    get_desktop_config, 
    is_desktop_mode, 
    ensure_desktop_directories
)

class DesktopServiceManager:
    """translatedservicetranslated，translatedonetranslatedFastAPIAndCeleryservice"""
    
    def __init__(self):
        self.config = get_desktop_config()
        self.app: Optional[FastAPI] = None
        self.celery_app = None
        self.celery_worker = None
        self.server_thread: Optional[threading.Thread] = None
        self.is_running = False
        self.start_time: Optional[float] = None
        self.actual_port: Optional[int] = None
        
        # ensuredirectorytranslatedin
        if not ensure_desktop_directories():
            raise RuntimeError("createtranslateddirectoryfailed")

        # settingslogs
        self._setup_logging()
    
    def _setup_logging(self):
        """settingslogsconfig"""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.paths.data_dir / "logs" / "autoclip.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _create_fastapi_app(self) -> FastAPI:
        """createFastAPItranslateduse"""
        # usetranslatedone's app_factory
        app = create_app(mode="desktop")
        
        # addtranslatedusetranslated
        @app.get("/desktop/info")
        async def desktop_info():
            """translateduseinfo"""
            return {
                "app_name": self.config.app_name,
                "app_version": self.config.app_version,
                "data_dir": str(self.config.paths.data_dir),
                "config": self.config.dict()
            }
        
        return app
    
    def _start_celery_worker(self):
        """startCelery Worker"""
        try:
            from backend.desktop_celery import celery_app
            import subprocess
            import os
            
            self.celery_app = celery_app

            if getattr(sys, "frozen", False):
                def run_worker():
                    celery_app.worker_main([
                        "worker",
                        "--loglevel=" + self.config.log_level.lower(),
                        "--concurrency=1",
                        "--pool=solo",
                    ])

                self.celery_worker_thread = threading.Thread(
                    target=run_worker,
                    daemon=True,
                )
                self.celery_worker_thread.start()
                self.logger.info("✅ Celery Worker translatedRuntimetranslatedstartsucceeded")
                return
            
            # usesubprocessstartCelery Worker，translatedprocesstranslated
            self.celery_worker_process = subprocess.Popen([
                sys.executable, '-m', 'celery', '-A', 'backend.desktop_celery', 'worker',
                '--loglevel=' + self.config.log_level.lower(),
                '--concurrency=' + str(self.config.celery_worker_concurrency),
                '--quiet=False'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={**os.environ, "AUTOCLIP_DESKTOP_MODE": "true", "AUTOCLIP_MODE": "desktop"})
            
            self.logger.info("✅ Celery Worker startsucceeded")
            
        except Exception as e:
            self.logger.error(f"❌ Celery Worker startfailed: {e}")
            raise
    
    def _start_fastapi_server(self):
        """startFastAPIservicetranslated"""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.config.host, 0))
            server_socket.listen(128)
            self.actual_port = server_socket.getsockname()[1]

            config = uvicorn.Config(
                self.app,
                host=self.config.host,
                port=self.actual_port,
                log_level=self.config.log_level.lower(),
                access_log=False
            )
            server = uvicorn.Server(config)

            # translatedinfotranslated stdout（translated Rust translated）
            print(f"PORT={self.actual_port}", flush=True)
            print(f"BACKtranslatedD_URL=http://{self.config.host}:{self.actual_port}", flush=True)
            
            # translatedfile（translatedusetranslated）
            port_file = self.config.paths.data_dir / "backend.port"
            with open(port_file, 'w') as f:
                f.write(str(self.actual_port))
            
            self.logger.info(f"🚀 backendservicestartintranslated: {self.actual_port}")
            
            # translatedservicetranslated
            server.run(sockets=[server_socket])
            
        except Exception as e:
            self.logger.error(f"❌ FastAPI servicetranslatedstartfailed: {e}")
            print(f"BACKtranslatedD_ERROR={e}", flush=True)
            self.is_running = False
            if getattr(self, "celery_worker_process", None):
                self.celery_worker_process.terminate()
                self.celery_worker_process = None
            raise
    
    def start(self):
        """starttranslatedservice"""
        if self.is_running:
            self.logger.warning("servicetranslatedintranslated")
            return
        
        try:
            self.start_time = time.time()
            
            # createFastAPItranslateduse
            self.app = self._create_fastapi_app()
            
            # startCelery Worker
            self._start_celery_worker()
            
            self.is_running = True

            # startFastAPIservicetranslated
            self.server_thread = threading.Thread(
                target=self._start_fastapi_server,
                daemon=True
            )
            self.server_thread.start()
            
            self.logger.info(f"🚀 AutoClip Desktop servicestartsucceeded")
            self.logger.info(f"🌐 APItranslated: http://{self.config.host}:<dynamic>")
            
        except Exception as e:
            self.logger.error(f"❌ servicestartfailed: {e}")
            self.stop()
            raise
    
    def stop(self):
        """translatedservice"""
        if not self.is_running:
            return
        
        try:
            self.logger.info("🛑 translatedintranslatedservice...")
            
            # translatedCelery Workerprocess
            if hasattr(self, 'celery_worker_process') and self.celery_worker_process:
                try:
                    self.celery_worker_process.terminate()
                    # etc.translatedprocesstranslated
                    try:
                        self.celery_worker_process.wait(timeout=5)
                        self.logger.info("✅ Celery Worker translated")
                    except subprocess.TimeoutExpired:
                        self.logger.warning("Celery Worker translatedin5secondstranslated，translated")
                        self.celery_worker_process.kill()
                        self.celery_worker_process.wait()
                except Exception as e:
                    self.logger.error(f"translatedCelery Workerfailed: {e}")
                finally:
                    self.celery_worker_process = None

            if hasattr(self, 'celery_worker_thread') and self.celery_worker_thread:
                self.celery_worker_thread = None
            
            # translatedFastAPIservicetranslated - usetranslatedIstranslated
            if self.server_thread and self.server_thread.is_alive():
                # etc.translatedservicetranslated
                self.server_thread.join(timeout=5)
                if self.server_thread.is_alive():
                    self.logger.warning("servicetranslatedin5secondstranslated")
            
            self.is_running = False
            self.start_time = None
            self.logger.info("✅ servicetranslated")
            
        except Exception as e:
            self.logger.error(f"❌ translatedservicefailed: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """fetchservicestatus"""
        return {
            "is_running": self.is_running,
            "start_time": self.start_time,
            "uptime": time.time() - self.start_time if self.start_time else 0,
            "config": {
                "host": self.config.host,
                "port": self.config.port,
                "debug": self.config.debug_mode,
                "version": self.config.app_version
            }
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Health Check"""
        try:
            import requests
            port = self.actual_port or self.config.port
            response = requests.get(
                f"http://{self.config.host}:{port}/health",
                timeout=5
            )
            
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "response": response.json(),
                    "port": port
                }
            else:
                return {
                    "status": "unhealthy",
                    "error": f"HTTP {response.status_code}",
                    "port": port
                }
                
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "port": self.actual_port or self.config.port
            }

# translatedservicetranslated
service_manager = None

def get_service_manager() -> DesktopServiceManager:
    """fetchservicetranslated"""
    global service_manager
    if service_manager is None:
        service_manager = DesktopServiceManager()
    return service_manager

def main():
    """translated"""
    # settingstranslated
    os.environ["AUTOCLIP_DESKTOP_MODE"] = "true"
    os.environ["AUTOCLIP_MODE"] = "desktop"
    
    # checktranslated
    if not is_desktop_mode():
        print("❌ translateduseOnlyintranslated")
        sys.exit(1)
    
    # fetchservicetranslated
    manager = get_service_manager()
    config = manager.config
    
    print(f"🚀 start AutoClip Desktop v{config.app_version}")
    print(f"📁 translateddirectory: {config.paths.data_dir}")
    print(f"🌐 servicetranslated: http://{config.host}:0 (translated)")
    
    # settingstranslatedprocess
    def signal_handler(signum, frame):
        print(f"\n🛑 translated ({signum})，translatedintranslatedservice...")
        if manager.is_running:
            manager.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # startservice
        manager.start()
        
        # translated
        while manager.is_running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 translated，translatedintranslatedservice...")
        manager.stop()
    except Exception as e:
        print(f"❌ servicetranslatedfailed: {e}")
        manager.stop()
        sys.exit(1)

if __name__ == "__main__":
    main()
