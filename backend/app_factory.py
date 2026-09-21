"""
translatedone'sbackendtranslatedusetranslated
support web And desktop translated
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
    create FastAPI translatedusetranslated
    
    Args:
        mode: translated，support "web" or "desktop"
    """
    # settingstranslated
    os.environ["AUTOCLIP_MODE"] = mode
    
    # configlogs
    logging_config = get_logging_config()
    logging.basicConfig(
        level=getattr(logging, logging_config["level"]),
        format=logging_config["format"],
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(logging_config["file"])
        ]
    )
    
    # create FastAPI translateduse
    app = FastAPI(
        title="AutoClip API",
        description="AIvideoclipprocessAPI",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # settingstranslatedusestatus
    app.state.mode = mode
    
    # config CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # translatedconfigtranslated
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # translatedprocesstranslated
    app.add_exception_handler(Exception, global_exception_handler)
    
    # starttranslated
    @app.on_event("startup")
    async def startup_event():
        logger.info(f"start AutoClip API service (translated: {mode})...")
        
        # importtranslatedmodeltranslatedensuretranslatedcreate
        from backend.models.bilibili import BilibiliAccount, UploadRecord
        Base.metadata.create_all(bind=engine)
        logger.info("databasetranslatedcreatetranslated")
        
        # translated API keytranslated
        api_key = get_api_key()
        if api_key:
            os.environ["DASHSCOPE_API_KEY"] = api_key
            logger.info("API keytranslated")
        else:
            logger.warning("translated API keyconfig")
        
        # translated'stranslated
        if mode == "desktop":
            logger.info("translated：uselocaltranslatedAnd SQLite")
        else:
            logger.info("Web translated：use Redis/Celery")
        
        logger.info("WebSocket translatedservicetranslateduse，usetranslated'stranslatedprogressSystem")
    
    # translated
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("translatedintranslated AutoClip API service...")
        logger.info("WebSocket translatedservicetranslateduse")
    
    # translated
    app.include_router(health_router, prefix="/api/health", tags=["health"])
    app.include_router(api_router, prefix="/api/v1")
    
    # add video-categories translated（translatedonetranslated api_router translated）
    @app.get("/api/v1/video-categories")
    async def get_video_categories():
        """fetchvideotranslatedconfig."""
        return {
            "categories": [
                {
                    "value": "default",
                    "name": "default",
                    "description": "translatedusevideotranslatedprocess",
                    "icon": "🎬",
                    "color": "#4facfe"
                },
                {
                    "value": "knowledge",
                    "name": "translated",
                    "description": "translated、translated、translated、translatedetc.translated",
                    "icon": "📚",
                    "color": "#52c41a"
                },
                {
                    "value": "entertainment",
                    "name": "translated",
                    "description": "translated、translated、translatedetc.translated",
                    "icon": "🎮",
                    "color": "#722ed1"
                },
                {
                    "value": "business",
                    "name": "providertranslated",
                    "description": "providertranslated、translated、translatedetc.providertranslated",
                    "icon": "💼",
                    "color": "#fa8c16"
                },
                {
                    "value": "experience",
                    "name": "translated",
                    "description": " translated、translatedetc.translated",
                    "icon": "🌟",
                    "color": "#eb2f96"
                },
                {
                    "value": "opinion",
                    "name": "translated",
                    "description": "translated、translatedetc.translated",
                    "icon": "💭",
                    "color": "#13c2c2"
                },
                {
                    "value": "speech",
                    "name": "translated",
                    "description": "translated、translatedetc.translated",
                    "icon": "🎤",
                    "color": "#f5222d"
                }
            ],
            "default_category": "default"
        }
    
    # translatedHealth Check
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
