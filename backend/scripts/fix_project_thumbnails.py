#!/usr/bin/env python3
"""
ENprojectEN
processingENfileENprojectEN
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
from backend.core.path_utils import get_projects_directory
import requests
import base64
import logging

logger = logging.getLogger(__name__)

def fix_project_thumbnail(project_id: str):
    """ENprojectEN"""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            print(f"❌ project {project_id} does not exist")
            return False
        
        if project.thumbnail:
            print(f"✅ project {project_id} EN，EN")
            return True
        
        print(f"🔧 ENproject {project_id} EN...")
        
        # checkprojectEN
        source_url = project.project_metadata.get('source_url') if project.project_metadata else None
        is_bilibili_project = source_url and 'bilibili.com' in source_url
        has_video_file = project.video_path and Path(project.video_path).exists()
        
        if is_bilibili_project:
            # ENproject - ENBENfetchEN
            print(f"📺 ENBENproject，ENfetchENvideoEN...")
            success = fix_bilibili_thumbnail(project, db)
        elif has_video_file:
            # fileENproject - ENvideofilegenerateEN
            print(f"📁 ENfileENproject，ENvideofilegenerateEN...")
            success = fix_file_import_thumbnail(project, db)
        else:
            # ENvideofile，ENclipgenerateEN
            print(f"🎬 ENvideofile，ENclipgenerateEN...")
            success = fix_clip_thumbnail(project, db)
        
        if success:
            print(f"✅ project {project_id} ENsucceeded")
        else:
            print(f"❌ project {project_id} ENfailed")
        
        return success
        
    except Exception as e:
        print(f"❌ ENproject {project_id} ENerror: {e}")
        return False
    finally:
        db.close()

def fix_bilibili_thumbnail(project, db):
    """ENBENprojectEN"""
    try:
        # ENprojectsettingsENfetchBEN
        if not project.processing_config:
            return False
        
        bilibili_info = project.processing_config.get('bilibili_info', {})
        if not bilibili_info:
            return False
        
        # ENBENAPIfetchEN
        # ENneedENBENAPIEN
        # ENreturnFalse，ENneedENprocessing
        print("⚠️  BENfetchneedAPIEN，EN")
        return False
        
    except Exception as e:
        logger.error(f"ENBENfailed: {e}")
        return False

def fix_file_import_thumbnail(project, db):
    """ENfileENprojectEN"""
    try:
        video_path = Path(project.video_path)
        if not video_path.exists():
            print(f"⚠️  videofiledoes not exist: {video_path}")
            return False
        
        # generateEN
        thumbnail_data = generate_project_thumbnail(project.id, video_path)
        
        if thumbnail_data:
            # saveENdatabase
            project.thumbnail = thumbnail_data
            db.commit()
            return True
        else:
            print("⚠️  ENgeneratefailed")
            return False
            
    except Exception as e:
        logger.error(f"ENfileENfailed: {e}")
        return False

def fix_clip_thumbnail(project, db):
    """ENclipgenerateEN"""
    try:
        # ENprojectdirectoryENclipfile
        project_dir = get_projects_directory() / str(project.id)
        clips_dir = project_dir / "output" / "clips"
        
        if not clips_dir.exists():
            print(f"⚠️  clipdirectorydoes not exist: {clips_dir}")
            return False
        
        # fetchENclipfile
        clip_files = list(clips_dir.glob("*.mp4"))
        if not clip_files:
            print(f"⚠️  ENclipfile")
            return False
        
        first_clip = clip_files[0]
        print(f"🎬 useclipfilegenerateEN: {first_clip.name}")
        
        # generateEN
        thumbnail_data = generate_project_thumbnail(project.id, first_clip)
        
        if thumbnail_data:
            # saveENdatabase
            project.thumbnail = thumbnail_data
            db.commit()
            return True
        else:
            print("⚠️  ENclipgenerateENfailed")
            return False
            
    except Exception as e:
        logger.error(f"ENclipgenerateENfailed: {e}")
        return False

def fix_all_project_thumbnails():
    """ENallprojectEN"""
    db = SessionLocal()
    try:
        # ENallENproject
        projects = db.query(Project).filter(Project.thumbnail.is_(None)).all()
        
        if not projects:
            print("✅ allprojectEN")
            return True
        
        print(f"📋 EN {len(projects)} ENneedENproject")
        
        success_count = 0
        for project in projects:
            if fix_project_thumbnail(project.id):
                success_count += 1
        
        print(f"🎉 EN！succeededEN {success_count}/{len(projects)} ENprojectEN")
        return True
        
    except Exception as e:
        print(f"❌ ENallprojectENerror: {e}")
        return False
    finally:
        db.close()

def main():
    """EN"""
    if len(sys.argv) > 1:
        # ENproject
        project_id = sys.argv[1]
        print(f"🚀 startENproject {project_id} EN...")
        if fix_project_thumbnail(project_id):
            print("🎉 EN！")
        else:
            print("❌ ENfailed")
            sys.exit(1)
    else:
        # ENallproject
        print("🚀 startENallprojectEN...")
        if fix_all_project_thumbnails():
            print("🎉 allEN！")
        else:
            print("❌ ENfailed")
            sys.exit(1)

if __name__ == "__main__":
    main()
