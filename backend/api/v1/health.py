"""
Health CheckAPItranslated
"""

from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

router = APIRouter()


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Health Checktranslated."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@router.get("/video-categories")
async def get_video_categories() -> Dict[str, Any]:
    """fetchvideotranslatedconfig."""
    return {
        "categories": [
            {
                "value": "knowledge",
                "name": "translated",
                "description": "translated、translated、translated、translatedetc.translated",
                "icon": "book",
                "color": "#1890ff"
            },
            {
                "value": "entertainment", 
                "name": "translated",
                "description": "translated、translated、translated、translatedetc.translated",
                "icon": "play-circle",
                "color": "#52c41a"
            },
            {
                "value": "experience",
                "name": "translated",
                "description": "translated、translated、translated、translatedetc.translatedusetranslated",
                "icon": "heart",
                "color": "#fa8c16"
            },
            {
                "value": "opinion",
                "name": "translated",
                "description": "translated、translated、translatedetc.",
                "icon": "message",
                "color": "#722ed1"
            },
            {
                "value": "business",
                "name": "providertranslated",
                "description": "providertranslated、translated、translatedetc.",
                "icon": "dollar",
                "color": "#13c2c2"
            },
            {
                "value": "speech",
                "name": "translated",
                "description": "translated、translated、translatedetc.translated",
                "icon": "sound",
                "color": "#eb2f96"
            }
        ],
        "default_category": "knowledge"
    } 