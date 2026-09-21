#!/usr/bin/env python3
"""
ENAllProjectEN
"""
import sys
import os
from pathlib import Path

# ENProjectENPythonEN
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.core.database import get_db
from backend.models.project import Project
from backend.models.clip import Clip
from backend.models.collection import Collection
from backend.models.task import Task
from sqlalchemy.orm import Session

def clean_database():
    """ENAllProjectEN"""
    print("🧹 EN...")
    
    # EN
    db = next(get_db())
    
    try:
        # ENAllEN（ENDependenciesEN）
        print("EN...")
        deleted_tasks = db.query(Task).delete()
        print(f"✅ EN {deleted_tasks} EN")
        
        print("EN...")
        deleted_collections = db.query(Collection).delete()
        print(f"✅ EN {deleted_collections} EN")
        
        print("EN...")
        deleted_clips = db.query(Clip).delete()
        print(f"✅ EN {deleted_clips} EN")
        
        print("ENProjectEN...")
        deleted_projects = db.query(Project).delete()
        print(f"✅ EN {deleted_projects} ENProject")
        
        # EN
        db.commit()
        
        print("\n🎉 ENCompleted!")
        print("EN，ENProjectEN")
        
    except Exception as e:
        print(f"❌ ENError: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_database()
