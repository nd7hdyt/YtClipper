#!/usr/bin/env python3
"""
ENprojectgenerateEN
"""

import sys
from pathlib import Path

# ENprojectENdirectoryENPythonpath
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.core.database import SessionLocal
from backend.models.project import Project
from backend.utils.thumbnail_generator import generate_project_thumbnail
from sqlalchemy import text

def generate_thumbnails_for_projects():
    """ENallENprojectgenerateEN"""
    db = SessionLocal()
    try:
        # ENallENvideofileENproject
        projects = db.query(Project).filter(
            Project.thumbnail.is_(None),
            Project.video_path.isnot(None)
        ).all()
        
        if not projects:
            print("✅ allprojectEN")
            return True
        
        print(f"📋 EN {len(projects)} ENneedgenerateENproject")
        
        success_count = 0
        for project in projects:
            try:
                print(f"🎬 currentlyENproject '{project.name}' ({project.id}) generateEN...")
                
                # checkvideofileEN
                video_path = Path(project.video_path)
                if not video_path.exists():
                    print(f"⚠️  videofiledoes not exist: {video_path}")
                    continue
                
                # generateEN
                thumbnail_data = generate_project_thumbnail(project.id, video_path)
                
                if thumbnail_data:
                    # saveENdatabase
                    project.thumbnail = thumbnail_data
                    db.commit()
                    print(f"✅ project '{project.name}' ENgeneratesucceeded")
                    success_count += 1
                else:
                    print(f"❌ project '{project.name}' ENgeneratefailed")
                    
            except Exception as e:
                print(f"❌ project '{project.name}' processingfailed: {e}")
                db.rollback()
                continue
        
        print(f"🎉 EN！succeededEN {success_count}/{len(projects)} ENprojectgenerateEN")
        return True
        
    except Exception as e:
        print(f"❌ generateENerror: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def generate_thumbnail_for_project(project_id: str):
    """ENprojectgenerateEN"""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            print(f"❌ project {project_id} does not exist")
            return False
        
        if not project.video_path:
            print(f"❌ project {project_id} ENvideofile")
            return False
        
        # checkvideofileEN
        video_path = Path(project.video_path)
        if not video_path.exists():
            print(f"❌ videofiledoes not exist: {video_path}")
            return False
        
        print(f"🎬 currentlyENproject '{project.name}' ({project.id}) generateEN...")
        
        # generateEN
        thumbnail_data = generate_project_thumbnail(project.id, video_path)
        
        if thumbnail_data:
            # saveENdatabase
            project.thumbnail = thumbnail_data
            db.commit()
            print(f"✅ project '{project.name}' ENgeneratesucceeded")
            return True
        else:
            print(f"❌ project '{project.name}' ENgeneratefailed")
            return False
            
    except Exception as e:
        print(f"❌ processingproject {project_id} ENerror: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    """EN"""
    if len(sys.argv) > 1:
        # ENprojectgenerateEN
        project_id = sys.argv[1]
        print(f"🚀 startENproject {project_id} generateEN...")
        if generate_thumbnail_for_project(project_id):
            print("🎉 ENgenerateEN！")
        else:
            print("❌ ENgeneratefailed")
            sys.exit(1)
    else:
        # ENallprojectgenerateEN
        print("🚀 startENallprojectgenerateEN...")
        if generate_thumbnails_for_projects():
            print("🎉 allENgenerateEN！")
        else:
            print("❌ ENgeneratefailed")
            sys.exit(1)

if __name__ == "__main__":
    main()
