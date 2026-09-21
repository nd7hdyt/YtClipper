#!/usr/bin/env python3
"""
translatedprojecttranslated'stranslated
"""

import sys
from pathlib import Path

# addprojecttranslateddirectorytranslatedPythonpath
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.core.database import SessionLocal
from backend.models.project import Project
from backend.utils.thumbnail_generator import generate_project_thumbnail
from sqlalchemy import text

def generate_thumbnails_for_projects():
    """translated'sprojecttranslated"""
    db = SessionLocal()
    try:
        # translatedvideofile'sproject
        projects = db.query(Project).filter(
            Project.thumbnail.is_(None),
            Project.video_path.isnot(None)
        ).all()
        
        if not projects:
            print("✅ translatedprojecttranslated")
            return True
        
        print(f"📋 translated {len(projects)}  translated'sproject")
        
        success_count = 0
        for project in projects:
            try:
                print(f"🎬 translatedintranslatedproject '{project.name}' ({project.id}) translated...")
                
                # checkvideofileIstranslatedin
                video_path = Path(project.video_path)
                if not video_path.exists():
                    print(f"⚠️  videofile not found: {video_path}")
                    continue
                
                # translated
                thumbnail_data = generate_project_thumbnail(project.id, video_path)
                
                if thumbnail_data:
                    # translateddatabase
                    project.thumbnail = thumbnail_data
                    db.commit()
                    print(f"✅ project '{project.name}' translatedsucceeded")
                    success_count += 1
                else:
                    print(f"❌ project '{project.name}' translatedfailed")
                    
            except Exception as e:
                print(f"❌ project '{project.name}' processing failed: {e}")
                db.rollback()
                continue
        
        print(f"🎉 translated！succeededtranslated {success_count}/{len(projects)}  projecttranslated")
        return True
        
    except Exception as e:
        print(f"❌ translatederror: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def generate_thumbnail_for_project(project_id: str):
    """translatedprojecttranslated"""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            print(f"❌ project {project_id} not found")
            return False
        
        if not project.video_path:
            print(f"❌ project {project_id} translatedvideofile")
            return False
        
        # checkvideofileIstranslatedin
        video_path = Path(project.video_path)
        if not video_path.exists():
            print(f"❌ videofile not found: {video_path}")
            return False
        
        print(f"🎬 translatedintranslatedproject '{project.name}' ({project.id}) translated...")
        
        # translated
        thumbnail_data = generate_project_thumbnail(project.id, video_path)
        
        if thumbnail_data:
            # translateddatabase
            project.thumbnail = thumbnail_data
            db.commit()
            print(f"✅ project '{project.name}' translatedsucceeded")
            return True
        else:
            print(f"❌ project '{project.name}' translatedfailed")
            return False
            
    except Exception as e:
        print(f"❌ processproject {project_id} translatederror: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    """translated"""
    if len(sys.argv) > 1:
        # translatedprojecttranslated
        project_id = sys.argv[1]
        print(f"🚀 translatedproject {project_id} translated...")
        if generate_thumbnail_for_project(project_id):
            print("🎉 translated！")
        else:
            print("❌ translatedfailed")
            sys.exit(1)
    else:
        # translatedprojecttranslated
        print("🚀 translatedprojecttranslated...")
        if generate_thumbnails_for_projects():
            print("🎉 translated！")
        else:
            print("❌ translatedfailed")
            sys.exit(1)

if __name__ == "__main__":
    main()
