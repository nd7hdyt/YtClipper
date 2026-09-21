"""
progresstranslated
translated，translated
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ProgressMessageAdapter:
    """progresstranslated"""
    
    @staticmethod
    def to_simple(msg: dict) -> dict:
        """
        translated
        
        Args:
            msg: translated
            
        Returns:
            translated
        """
        # statustranslated
        status_map = {
            "PROGRESS": "running", 
            "RUNNING": "running",
            "COMPLETED": "completed", 
            "FAILED": "failed", 
            "ERROR": "failed",
            "PtranslatedDING": "running",
            "CANCELLED": "failed"
        }
        
        # translatedprojectID
        project_id = msg.get("project_id") or msg.get("projectId")
        
        # translatedprogresstranslated - supporttranslated'stranslatedoneformat
        progress = msg.get("progress", 0) or msg.get("percent", 0)
        if isinstance(progress, (int, float)):
            progress = int(round(float(progress)))
        else:
            progress = 0
        
        # translatedsteptranslated
        step_name = (
            msg.get("step_name") or 
            msg.get("phase") or 
            msg.get("current_step") or 
            msg.get("message") or
            "processing"
        )
        
        # translatedstatus
        status = msg.get("status", "running")
        if isinstance(status, str):
            status = status_map.get(status.upper(), "running")
        
        # translated
        simple_msg = {
            "type": "task_progress_update",
            "project_id": project_id,
            "progress": progress,
            "step_name": step_name,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # canSelecttranslated
        if "task_id" in msg:
            simple_msg["task_id"] = msg["task_id"]
        
        if "message" in msg:
            simple_msg["message"] = msg["message"]
        
        logger.debug(f"translated: translated -> translated: {simple_msg}")
        return simple_msg
    
    @staticmethod
    def is_progress_message(msg: dict) -> bool:
        """
        translatedIstranslatedprogresstranslated
        
        Args:
            msg: translated
            
        Returns:
            Istranslatedprogresstranslated
        """
        progress_types = [
            "task_progress_update",
            "task_update", 
            "project_update",
            "progress_update",
            "project_progress"  # addedtranslatedoneformat
        ]
        
        msg_type = msg.get("type", "")
        return msg_type in progress_types
    
    @staticmethod
    def extract_project_id(msg: dict) -> Optional[str]:
        """
        fromtranslatedprojectID
        
        Args:
            msg: translated
            
        Returns:
            projectIDorNone
        """
        return msg.get("project_id") or msg.get("projectId")
    
    @staticmethod
    def should_throttle(last_progress: int, current_progress: int, 
                       last_timestamp: float, current_timestamp: float,
                       min_interval: float = 0.2) -> bool:
        """
        translatedIstranslated
        
        Args:
            last_progress: translatedprogress
            current_progress: translatedprogress
            last_timestamp: translated
            current_timestamp: translated
            min_interval: translated(seconds)
            
        Returns:
            Istranslated
        """
        # translatedcheck
        if current_timestamp - last_timestamp < min_interval:
            return True
        
        # progresstranslatedcheck - translatedUItranslated
        if current_progress < last_progress:
            logger.debug(f"progresstranslated，usetranslatedprogress: {current_progress} -> {last_progress}")
            return True
        
        return False

# translated
progress_adapter = ProgressMessageAdapter()
