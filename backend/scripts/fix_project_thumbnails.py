#!/usr/bin/env python3
"""
fixedprojecttranslated
processtranslatedimportAndfileimportproject'stranslatedissue
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
from backend.core.path_utils import get_projects_directory
import requests
import base64
import logging

logger = logging.getLogger(__name__)

def fix_project_thumbnail(project_id: str):
    """fixedtranslatedproject'stranslated"""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            print(f"❌ project {project_id} not found")
            return False
        
        if project.thumbnail:
            print(f"✅ project {project_id} translated，skip")
            return True
        
        print(f"🔧 fixedproject {project_id} 'stranslated...")
        
        # checkprojecttranslatedAndtranslated
        source_url = project.project_metadata.get('source_url') if project.project_metadata else None
        is_bilibili_project = source_url and 'bilibili.com' in source_url
        has_video_file = project.video_path and Path(project.video_path).exists()
        
        if is_bilibili_project:
            # translatedimportproject - translatedfromBsitefetchtranslated
            print(f"📺 translatedBsiteproject，translatedfetchtranslatedvideotranslated...")
            success = fix_bilibili_thumbnail(project, db)
        elif has_video_file:
            # fileimportproject - fromvideofiletranslated
            print(f"📁 translatedfileimportproject，fromvideofiletranslated...")
            success = fix_file_import_thumbnail(project, db)
        else:
            # translatedvideofile，translatedfromcliptranslated
            print(f"🎬 translatedvideofile，translatedfromcliptranslated...")
            success = fix_clip_thumbnail(project, db)
        
        if success:
            print(f"✅ project {project_id} translatedfixedsucceeded")
        else:
            print(f"❌ project {project_id} translatedfixedfailed")
        
        return success
        
    except Exception as e:
        print(f"❌ fixedproject {project_id} translatederror: {e}")
        return False
    finally:
        db.close()

def fix_bilibili_thumbnail(project, db):
    """fixedBsiteproject'stranslated"""
    try:
        # fromprojectsettingstranslatedfetchBsiteinfo
        if not project.processing_config:
            return False
        
        bilibili_info = project.processing_config.get('bilibili_info', {})
        if not bilibili_info:
            return False
        
        # translatedfromBsiteAPIfetchtranslated
        # thistranslated'sBsiteAPItranslated
        # translatedreturnFalse，translatedprocess
        print("⚠️  BsitetranslatedfetchtranslatedAPIsupport，translatedskip")
        return False
        
    except Exception as e:
        logger.error(f"fixedBsitetranslatedfailed: {e}")
        return False

def fix_file_import_thumbnail(project, db):
    """fixedfileimportproject'stranslated"""
    try:
        video_path = Path(project.video_path)
        if not video_path.exists():
            print(f"⚠️  videofile not found: {video_path}")
            return False
        
        # translated
        thumbnail_data = generate_project_thumbnail(project.id, video_path)
        
        if thumbnail_data:
            # translateddatabase
            project.thumbnail = thumbnail_data
            db.commit()
            return True
        else:
            print("⚠️  translatedfailed")
            return False
            
    except Exception as e:
        logger.error(f"fixedfileimporttranslatedfailed: {e}")
        return False

def fix_clip_thumbnail(project, db):
    """fromcliptranslated"""
    try:
        # translatedprojectdirectorytranslated'sclipfile
        project_dir = get_projects_directory() / str(project.id)
        clips_dir = project_dir / "output" / "clips"
        
        if not clips_dir.exists():
            print(f"⚠️  clipdirectorynot found: {clips_dir}")
            return False
        
        # fetchNo.one clipfile
        clip_files = list(clips_dir.glob("*.mp4"))
        if not clip_files:
            print(f"⚠️  translatedclipfile")
            return False
        
        first_clip = clip_files[0]
        print(f"🎬 useclipfiletranslated: {first_clip.name}")
        
        # translated
        thumbnail_data = generate_project_thumbnail(project.id, first_clip)
        
        if thumbnail_data:
            # translateddatabase
            project.thumbnail = thumbnail_data
            db.commit()
            return True
        else:
            print("⚠️  fromcliptranslatedfailed")
            return False
            
    except Exception as e:
        logger.error(f"fromcliptranslatedfailed: {e}")
        return False

def fix_all_project_thumbnails():
    """fixedtranslatedproject'stranslated"""
    db = SessionLocal()
    try:
        # translated'sproject
        projects = db.query(Project).filter(Project.thumbnail.is_(None)).all()
        
        if not projects:
            print("✅ translatedprojecttranslated")
            return True
        
        print(f"📋 translated {len(projects)}  translatedfixedtranslated'sproject")
        
        success_count = 0
        for project in projects:
            if fix_project_thumbnail(project.id):
                success_count += 1
        
        print(f"🎉 translated！succeededfixed {success_count}/{len(projects)}  project'stranslated")
        return True
        
    except Exception as e:
        print(f"❌ fixedtranslatedprojecttranslatederror: {e}")
        return False
    finally:
        db.close()

def main():
    """translated"""
    if len(sys.argv) > 1:
        # fixedtranslatedproject
        project_id = sys.argv[1]
        print(f"🚀 translatedfixedproject {project_id} 'stranslated...")
        if fix_project_thumbnail(project_id):
            print("🎉 translatedfixedtranslated！")
        else:
            print("❌ translatedfixedfailed")
            sys.exit(1)
    else:
        # fixedtranslatedproject
        print("🚀 translatedfixedtranslatedproject'stranslated...")
        if fix_all_project_thumbnails():
            print("🎉 translatedfixedtranslated！")
        else:
            print("❌ translatedfixedfailed")
            sys.exit(1)

if __name__ == "__main__":
    main()
