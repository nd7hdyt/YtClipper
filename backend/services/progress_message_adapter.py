"""
progressEN
EN，EN
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ProgressMessageAdapter:
    """progressEN"""
    
    @staticmethod
    def to_simple(msg: dict) -> dict:
        """
        EN
        
        Args:
            msg: EN
            
        Returns:
            EN
        """
        # statusEN
        status_map = {
            "PROGRESS": "running", 
            "RUNNING": "running",
            "COMPLETED": "completed", 
            "FAILED": "failed", 
            "ERROR": "failed",
            "PENDING": "running",
            "CANCELLED": "failed"
        }
        
        # ENprojectID
        project_id = msg.get("project_id") or msg.get("projectId")
        
        # ENprogressEN - EN
        progress = msg.get("progress", 0) or msg.get("percent", 0)
        if isinstance(progress, (int, float)):
            progress = int(round(float(progress)))
        else:
            progress = 0
        
        # EN
        step_name = (
            msg.get("step_name") or 
            msg.get("phase") or 
            msg.get("current_step") or 
            msg.get("message") or
            "processing"
        )
        
        # ENstatus
        status = msg.get("status", "running")
        if isinstance(status, str):
            status = status_map.get(status.upper(), "running")
        
        # EN
        simple_msg = {
            "type": "task_progress_update",
            "project_id": project_id,
            "progress": progress,
            "step_name": step_name,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # EN
        if "task_id" in msg:
            simple_msg["task_id"] = msg["task_id"]
        
        if "message" in msg:
            simple_msg["message"] = msg["message"]
        
        logger.debug(f"EN: EN -> EN: {simple_msg}")
        return simple_msg
    
    @staticmethod
    def is_progress_message(msg: dict) -> bool:
        """
        ENprogressEN
        
        Args:
            msg: EN
            
        Returns:
            ENprogressEN
        """
        progress_types = [
            "task_progress_update",
            "task_update", 
            "project_update",
            "progress_update",
            "project_progress"  # EN
        ]
        
        msg_type = msg.get("type", "")
        return msg_type in progress_types
    
    @staticmethod
    def extract_project_id(msg: dict) -> Optional[str]:
        """
        ENprojectID
        
        Args:
            msg: EN
            
        Returns:
            projectIDENNone
        """
        return msg.get("project_id") or msg.get("projectId")
    
    @staticmethod
    def should_throttle(last_progress: int, current_progress: int, 
                       last_timestamp: float, current_timestamp: float,
                       min_interval: float = 0.2) -> bool:
        """
        ENshouldENsend
        
        Args:
            last_progress: ENprogress
            current_progress: currentprogress
            last_timestamp: ENtimeEN
            current_timestamp: currenttimeEN
            min_interval: EN(EN)
            
        Returns:
            ENshouldEN
        """
        # timeENcheck
        if current_timestamp - last_timestamp < min_interval:
            return True
        
        # progressENcheck - ENUIEN
        if current_progress < last_progress:
            logger.debug(f"progressEN，useENprogress: {current_progress} -> {last_progress}")
            return True
        
        return False

# EN
progress_adapter = ProgressMessageAdapter()
