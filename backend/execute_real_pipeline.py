#!/usr/bin/env python3
"""
ENexecuteEN
usePipelineAdapterEN
"""

import sys
import os
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any

# ENprojectENdirectoryENPythonpath
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ..core.database import SessionLocal
from ..models.project import Project, ProjectStatus
from ..models.task import Task, TaskStatus
from ..services.pipeline_adapter import create_pipeline_adapter_sync
import logging

# settingslog
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def execute_real_pipeline(project_id: str):
    """ENexecuteEN"""
    
    logger.info(f"startexecuteproject {project_id} EN")
    
    try:
        # createdatabaseEN
        db = SessionLocal()
        
        try:
            # validateprojectEN
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                raise ValueError(f"project {project_id} does not exist")
            
            logger.info(f"validateprojectEN: {project.name}")
            
            # createtaskEN
            task = Task(
                name=f"ENprocessing",
                description=f"useENprocessingproject {project_id}",
                task_type="VIDEO_PROCESSING",
                project_id=project_id,
                status=TaskStatus.RUNNING,
                progress=0,
                current_step="initialize",
                total_steps=6
            )
            db.add(task)
            db.commit()
            db.refresh(task)
            
            logger.info(f"taskENcreated: {task.id}")
            
            # ENfilepath
            data_root = project_root / "data" / "projects" / project_id
            input_video_path = data_root / "raw" / "input.mp4"
            input_srt_path = data_root / "raw" / "input.srt"
            
            # validatefileEN
            if not input_video_path.exists():
                raise FileNotFoundError(f"videofiledoes not exist: {input_video_path}")
            if not input_srt_path.exists():
                raise FileNotFoundError(f"subtitlesfiledoes not exist: {input_srt_path}")
            
            logger.info(f"filepathvalidatesucceeded:")
            logger.info(f"  video: {input_video_path}")
            logger.info(f"  subtitles: {input_srt_path}")
            
            # createPipelineEN
            pipeline_adapter = create_pipeline_adapter_sync(db, str(task.id), project_id)
            
            # validateEN
            logger.info("validateEN...")
            errors = pipeline_adapter.validate_pipeline_prerequisites()
            if errors:
                error_msg = "; ".join(errors)
                logger.error(f"ENvalidatefailed: {error_msg}")
                raise ValueError(f"ENvalidatefailed: {error_msg}")
            
            logger.info("ENvalidatethrough")
            
            # executeENprocessing
            logger.info("startexecuteEN...")
            result = pipeline_adapter.process_project_sync(
                project_id=project_id,
                input_video_path=str(input_video_path),
                input_srt_path=str(input_srt_path)
            )
            
            # checkprocessingresult
            if result.get('status') == 'failed':
                error_msg = result.get('message', 'processingfailed')
                logger.error(f"ENprocessingfailed: {error_msg}")
                
                # updatetaskstatusENfailed
                task.status = TaskStatus.FAILED
                task.error_message = error_msg
                db.commit()
                
                return {
                    "success": False,
                    "error": error_msg,
                    "result": result
                }
            else:
                # processingsucceeded
                logger.info("🎉 ENprocessingsucceeded！")
                logger.info(f"processingresult: {result}")
                
                # updatetaskstatusEN
                task.status = TaskStatus.COMPLETED
                task.progress = 100
                task.current_step = "processingEN"
                db.commit()
                
                return {
                    "success": True,
                    "result": result,
                    "message": "ENprocessingEN"
                }
                
        finally:
            db.close()
            
    except Exception as e:
        error_msg = f"executeENfailed: {str(e)}"
        logger.error(error_msg)
        
        # ENupdatetaskstatus
        try:
            db = SessionLocal()
            task = db.query(Task).filter(Task.project_id == project_id).order_by(Task.created_at.desc()).first()
            if task:
                task.status = TaskStatus.FAILED
                task.error_message = error_msg
                db.commit()
            db.close()
        except Exception as db_error:
            logger.error(f"updatetaskstatusfailed: {db_error}")
        
        return {
            "success": False,
            "error": error_msg
        }

async def main():
    """EN"""
    if len(sys.argv) != 2:
        print("useEN: python execute_real_pipeline.py <project_id>")
        sys.exit(1)
    
    project_id = sys.argv[1]
    
    result = await execute_real_pipeline(project_id)
    
    if result["success"]:
        print(f"✅ ENexecutesucceeded！")
        print(f"📊 result: {result['result']}")
    else:
        print(f"❌ ENexecutefailed: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
