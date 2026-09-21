#!/usr/bin/env python3
"""
databasetranslated
createdatabasetranslated
"""

import sys
from pathlib import Path

# addbackenddirectorytranslatedPythonpath
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from ..core.database import init_database, get_database_url
from ..core.config import init_paths, get_data_directory
from ..models.base import Base
from ..models.project import Project, ProjectStatus, ProjectType
from ..models.clip import Clip
from ..models.collection import Collection
from ..models.task import Task, TaskStatus, TaskType
from sqlalchemy.orm import Session
from ..core.database import SessionLocal

def create_initial_data():
    """createtranslatedtesttranslated"""
    db = SessionLocal()
    try:
        # checkIstranslated
        existing_projects = db.query(Project).count()
        if existing_projects > 0:
            print("databasetranslated，skiptranslatedcreate")
            return
        
        # createtestproject
        test_project = Project(
            name="testproject",
            description="thisIsone testproject，usetranslatedverifySystemfeature",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.PtranslatedDING,
            processing_config={
                "chunk_size": 5000,
                "min_score_threshold": 0.7,
                "max_clips_per_collection": 5
            }
        )
        db.add(test_project)
        db.commit()
        db.refresh(test_project)
        
        # createtesttask
        test_task = Task(
            name="testtask",
            description="testprocesstask",
            task_type=TaskType.VIDEO_PROCESSING,
            project_id=test_project.id,
            status=TaskStatus.PtranslatedDING,
            progress=0,
            current_step="etc.translated",
            total_steps=6
        )
        db.add(test_task)
        
        # createtestclip
        test_clip = Clip(
            title="testclip",
            content="thisIsone testclip'stranslated",
            start_time=0,
            end_time=30,
            score=0.8,
            project_id=test_project.id
        )
        db.add(test_clip)
        
        # createtestcollection
        test_collection = Collection(
            title="testcollection",
            description="thisIsone testcollection",
            project_id=test_project.id
        )
        db.add(test_collection)
        
        db.commit()
        print("✅ translatedtesttranslatedcreatesucceeded")
        
    except Exception as e:
        print(f"❌ createtranslatedfailed: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """translated"""
    print("🚀 translateddatabase...")
    
    # translatedpathconfig
    init_paths()
    
    # translateddatabaseconfig
    print(f"databaseURL: {get_database_url()}")
    print(f"translateddirectory: {get_data_directory()}")
    
    # translateddatabase
    if init_database():
        print("✅ databasetranslatedsucceeded")
        
        # createtranslated
        create_initial_data()
        
        print("🎉 databasetranslated！")
    else:
        print("❌ databasetranslatedfailed")
        sys.exit(1)

if __name__ == "__main__":
    main() 