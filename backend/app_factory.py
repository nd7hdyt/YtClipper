"""
EN
EN web EN desktop EN
"""
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.api.v1 import api_router
from backend.api.v1.health import router as health_router
from backend.core.database import engine
from backend.models.base import Base
from backend.core.config import get_logging_config, get_api_key
from backend.core.error_middleware import global_exception_handler

logger = logging.getLogger(__name__)

def create_app(mode: str = "web") -> FastAPI:
    """
    create FastAPI EN
    
    Args:
        mode: runEN，EN "web" EN "desktop"
    """
    # settingsEN
    os.environ["AUTOCLIP_MODE"] = mode
    
    # configlog
    logging_config = get_logging_config()
    logging.basicConfig(
        level=getattr(logging, logging_config["level"]),
        format=logging_config["format"],
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(logging_config["file"])
        ]
    )
    
    # create FastAPI EN
    app = FastAPI(
        title="AutoClip API",
        description="AIvideoclipprocessingAPI",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # settingsENstatus
    app.state.mode = mode
    
    # config CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # ENneedconfigEN
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # registerENexceptionprocessingEN
    app.add_exception_handler(Exception, global_exception_handler)
    
    # startEN
    @app.on_event("startup")
    async def startup_event():
        logger.info(f"start AutoClip API service (EN: {mode})...")
        
        # ENallENcreate
        from backend.models.bilibili import BilibiliAccount, UploadRecord
        Base.metadata.create_all(bind=engine)
        logger.info("databaseENcreateEN")
        
        # load API EN
        api_key = get_api_key()
        if api_key:
            os.environ["DASHSCOPE_API_KEY"] = api_key
            logger.info("API ENloadEN")
        else:
            logger.warning("not found API ENconfig")
        
        # ENinitialize
        if mode == "desktop":
            logger.info("EN：useENqueueEN SQLite")
        else:
            logger.info("Web EN：use Redis/Celery")
        
        logger.info("WebSocket ENserviceEN，useENprogresssystem")
    
    # EN
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("currentlyEN AutoClip API service...")
        logger.info("WebSocket ENserviceEN")
    
    # registerEN
    app.include_router(health_router, prefix="/api/health", tags=["health"])
    app.include_router(api_router, prefix="/api/v1")
    
    # EN video-categories EN（EN api_router EN）
    @app.get("/api/v1/video-categories")
    async def get_video_categories():
        """fetchvideocategoryconfig."""
        return {
            "categories": [
                {
                    "value": "default",
                    "name": "EN",
                    "description": "ENvideoENprocessing",
                    "icon": "🎬",
                    "color": "#4facfe"
                },
                {
                    "value": "knowledge",
                    "name": "EN",
                    "description": "EN、EN、EN、EN",
                    "icon": "📚",
                    "color": "#52c41a"
                },
                {
                    "value": "entertainment",
                    "name": "EN",
                    "description": "EN、EN、EN",
                    "icon": "🎮",
                    "color": "#722ed1"
                },
                {
                    "value": "business",
                    "name": "EN",
                    "description": "EN、EN、EN",
                    "icon": "💼",
                    "color": "#fa8c16"
                },
                {
                    "value": "experience",
                    "name": "EN",
                    "description": "EN、EN",
                    "icon": "🌟",
                    "color": "#eb2f96"
                },
                {
                    "value": "opinion",
                    "name": "EN",
                    "description": "EN、ENanalysisEN",
                    "icon": "💭",
                    "color": "#13c2c2"
                },
                {
                    "value": "speech",
                    "name": "EN",
                    "description": "EN、EN",
                    "icon": "🎤",
                    "color": "#f5222d"
                }
            ],
            "default_category": "default"
        }
    
    # ENcheck
    @app.get("/health")
    async def root_health():
        try:
            return {
                "status": "ok",
                "mode": mode,
                "version": "1.0.0"
            }
        except Exception as e:
            return JSONResponse(
                status_code=500, 
                content={"status": "error", "detail": str(e)}
            )
    
    return app
