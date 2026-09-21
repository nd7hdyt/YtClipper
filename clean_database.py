#!/usr/bin/env python3
"""
translateddatabasetranslated'stranslatedprojecttranslated
"""
import sys
import os
from pathlib import Path

# addprojecttranslateddirectorytranslatedPythonpath
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.core.database import get_db
from backend.models.project import Project
from backend.models.clip import Clip
from backend.models.collection import Collection
from backend.models.task import Task
from sqlalchemy.orm import Session

def clean_database():
    """translateddatabasetranslated'stranslatedprojecttranslated"""
    print("🧹 translatedcleandatabase...")
    
    # fetchdatabasetranslated
    db = next(get_db())
    
    try:
        # deletetranslated（bydependenciestranslated）
        print("deletetasktranslated...")
        deleted_tasks = db.query(Task).delete()
        print(f"✅ deletetranslated {deleted_tasks}  task")
        
        print("deletecollectiontranslated...")
        deleted_collections = db.query(Collection).delete()
        print(f"✅ deletetranslated {deleted_collections}  collection")
        
        print("deletecliptranslated...")
        deleted_clips = db.query(Clip).delete()
        print(f"✅ deletetranslated {deleted_clips}  clip")
        
        print("deleteprojecttranslated...")
        deleted_projects = db.query(Project).delete()
        print(f"✅ deletetranslated {deleted_projects}  project")
        
        # translated
        db.commit()
        
        print("\n🎉 databasecleantranslated!")
        print("translatedindatabaseIstranslated's，translatedprojecttranslated")
        
    except Exception as e:
        print(f"❌ cleandatabasetranslatederror: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_database()
