#!/usr/bin/env python3
"""
bytranslated'stranslated
usePipelineAdapterAndtranslated'stranslatedstep
"""

import sys
import os
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any

# addprojecttranslateddirectorytranslatedPythonpath
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ..core.database import SessionLocal
from ..models.project import Project, ProjectStatus
from ..models.task import Task, TaskStatus
from ..services.pipeline_adapter import create_pipeline_adapter_sync
import logging

# settingslogs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def execute_real_pipeline(project_id: str):
    """bytranslated"""
    
    logger.info(f"translatedproject {project_id} 'stranslated")
    
    try:
        # createdatabasetranslated
        db = SessionLocal()
        
        try:
            # verifyprojectIstranslatedin
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                raise ValueError(f"project {project_id} not found")
            
            logger.info(f"verifyprojecttranslatedin: {project.name}")
            
            # createtasktranslated
            task = Task(
                name=f"translatedprocess",
                description=f"usetranslatedprocessproject {project_id}",
                task_type="VIDEO_PROCESSING",
                project_id=project_id,
                status=TaskStatus.RUNNING,
                progress=0,
                current_step="translated",
                total_steps=6
            )
            db.add(task)
            db.commit()
            db.refresh(task)
            
            logger.info(f"tasktranslatedcreate: {task.id}")
            
            # translatedfile path
            data_root = project_root / "data" / "projects" / project_id
            input_video_path = data_root / "raw" / "input.mp4"
            input_srt_path = data_root / "raw" / "input.srt"
            
            # verifyfiletranslatedin
            if not input_video_path.exists():
                raise FileNotFoundError(f"videofile not found: {input_video_path}")
            if not input_srt_path.exists():
                raise FileNotFoundError(f"subtitlesfile not found: {input_srt_path}")
            
            logger.info(f"file pathverifysucceeded:")
            logger.info(f"  video: {input_video_path}")
            logger.info(f"  subtitles: {input_srt_path}")
            
            # createPipelinetranslated
            pipeline_adapter = create_pipeline_adapter_sync(db, str(task.id), project_id)
            
            # verifytranslated
            logger.info("verifytranslated...")
            errors = pipeline_adapter.validate_pipeline_prerequisites()
            if errors:
                error_msg = "; ".join(errors)
                logger.error(f"translatedverifyfailed: {error_msg}")
                raise ValueError(f"translatedverifyfailed: {error_msg}")
            
            logger.info("translatedverifytranslated")
            
            # translated'stranslatedprocess
            logger.info("translated...")
            result = pipeline_adapter.process_project_sync(
                project_id=project_id,
                input_video_path=str(input_video_path),
                input_srt_path=str(input_srt_path)
            )
            
            # checkprocesstranslated
            if result.get('status') == 'failed':
                error_msg = result.get('message', 'processing failed')
                logger.error(f"translatedprocessing failed: {error_msg}")
                
                # updatetaskstatustranslatedfailed
                task.status = TaskStatus.FAILED
                task.error_message = error_msg
                db.commit()
                
                return {
                    "success": False,
                    "error": error_msg,
                    "result": result
                }
            else:
                # processsucceeded
                logger.info("🎉 translatedprocesssucceeded！")
                logger.info(f"processtranslated: {result}")
                
                # updatetaskstatustranslated
                task.status = TaskStatus.COMPLETED
                task.progress = 100
                task.current_step = "processing completed"
                db.commit()
                
                return {
                    "success": True,
                    "result": result,
                    "message": "translatedprocessing completed"
                }
                
        finally:
            db.close()
            
    except Exception as e:
        error_msg = f"translatedfailed: {str(e)}"
        logger.error(error_msg)
        
        # translatedupdatetaskstatus
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
    """translated"""
    if len(sys.argv) != 2:
        print("usetranslated: python execute_real_pipeline.py <project_id>")
        sys.exit(1)
    
    project_id = sys.argv[1]
    
    result = await execute_real_pipeline(project_id)
    
    if result["success"]:
        print(f"✅ translatedsucceeded！")
        print(f"📊 translated: {result['result']}")
    else:
        print(f"❌ translatedfailed: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
