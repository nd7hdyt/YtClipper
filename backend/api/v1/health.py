"""
ENcheckAPIEN
"""

from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

router = APIRouter()


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """ENcheckEN."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@router.get("/video-categories")
async def get_video_categories() -> Dict[str, Any]:
    """fetchvideocategoryconfig."""
    return {
        "categories": [
            {
                "value": "knowledge",
                "name": "EN",
                "description": "EN、EN、EN、EN",
                "icon": "book",
                "color": "#1890ff"
            },
            {
                "value": "entertainment", 
                "name": "EN",
                "description": "EN、EN、EN、EN",
                "icon": "play-circle",
                "color": "#52c41a"
            },
            {
                "value": "experience",
                "name": "EN",
                "description": "EN、EN、EN、EN",
                "icon": "heart",
                "color": "#fa8c16"
            },
            {
                "value": "opinion",
                "name": "EN",
                "description": "EN、EN、EN",
                "icon": "message",
                "color": "#722ed1"
            },
            {
                "value": "business",
                "name": "EN",
                "description": "ENanalysis、EN、EN",
                "icon": "dollar",
                "color": "#13c2c2"
            },
            {
                "value": "speech",
                "name": "EN",
                "description": "EN、EN、EN",
                "icon": "sound",
                "color": "#eb2f96"
            }
        ],
        "default_category": "knowledge"
    } 