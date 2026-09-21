#!/usr/bin/env python3
"""
databaseinitializeEN
createdatabaseEN
"""

import sys
from pathlib import Path

# ENbackenddirectoryENPythonpath
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
    """createEN"""
    db = SessionLocal()
    try:
        # checkEN
        existing_projects = db.query(Project).count()
        if existing_projects > 0:
            print("databaseEN，ENcreate")
            return
        
        # createENproject
        test_project = Project(
            name="ENproject",
            description="ENproject，ENvalidatesystemEN",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.PENDING,
            processing_config={
                "chunk_size": 5000,
                "min_score_threshold": 0.7,
                "max_clips_per_collection": 5
            }
        )
        db.add(test_project)
        db.commit()
        db.refresh(test_project)
        
        # createENtask
        test_task = Task(
            name="ENtask",
            description="ENprocessingtask",
            task_type=TaskType.VIDEO_PROCESSING,
            project_id=test_project.id,
            status=TaskStatus.PENDING,
            progress=0,
            current_step="ENstart",
            total_steps=6
        )
        db.add(test_task)
        
        # createENclip
        test_clip = Clip(
            title="ENclip",
            content="ENclipEN",
            start_time=0,
            end_time=30,
            score=0.8,
            project_id=test_project.id
        )
        db.add(test_clip)
        
        # createENcollection
        test_collection = Collection(
            title="ENcollection",
            description="ENcollection",
            project_id=test_project.id
        )
        db.add(test_collection)
        
        db.commit()
        print("✅ ENcreatesucceeded")
        
    except Exception as e:
        print(f"❌ createENfailed: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """EN"""
    print("🚀 startinitializedatabase...")
    
    # initializepathconfig
    init_paths()
    
    # ENdatabaseconfig
    print(f"databaseURL: {get_database_url()}")
    print(f"ENdirectory: {get_data_directory()}")
    
    # initializedatabase
    if init_database():
        print("✅ databaseinitializesucceeded")
        
        # createEN
        create_initial_data()
        
        print("🎉 databaseinitializeEN！")
    else:
        print("❌ databaseinitializefailed")
        sys.exit(1)

if __name__ == "__main__":
    main() 