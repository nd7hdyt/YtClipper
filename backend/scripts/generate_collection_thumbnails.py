#!/usr/bin/env python3
"""
translatedcollectiontranslated
"""
import sys
import os
from pathlib import Path

# addprojecttranslateddirectorytranslatedPythonpath
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.core.database import get_db
from backend.models.collection import Collection
from backend.utils.video_processor import VideoProcessor
import logging

# configlogs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_collection_thumbnails():
    """translated'scollectiontranslated"""
    try:
        db = next(get_db())
        
        # translated'scollection
        collections_without_thumbnails = db.query(Collection).filter(
            Collection.thumbnail_path.is_(None)
        ).all()
        
        if not collections_without_thumbnails:
            logger.info("translatedcollectiontranslated")
            return True
        
        logger.info(f"translated {len(collections_without_thumbnails)}  translated'scollection")
        
        success_count = 0
        for collection in collections_without_thumbnails:
            try:
                logger.info(f"translatedintranslatedcollection '{collection.name}' ({collection.id}) translated...")
                
                # checkIstranslatedexportvideofile
                if not collection.export_path:
                    logger.warning(f"collection '{collection.name}' translatedexportvideofile，skip")
                    continue
                
                video_path = Path(collection.export_path)
                if not video_path.exists():
                    logger.warning(f"collection '{collection.name}' 'svideofile not found: {video_path}")
                    continue
                
                # translatedfiletranslated
                safe_name = "".join(c for c in collection.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_name = safe_name.replace(' ', '_')
                thumbnail_filename = f"{collection.id}_{safe_name}_thumbnail.jpg"
                thumbnail_path = video_path.parent / thumbnail_filename
                
                # useVideoProcessortranslated
                thumbnail_success = VideoProcessor.extract_thumbnail(video_path, thumbnail_path, time_offset=5)
                
                if thumbnail_success:
                    # updatedatabase
                    collection.thumbnail_path = str(thumbnail_path)
                    db.commit()
                    logger.info(f"✅ collection '{collection.name}' translatedsucceeded: {thumbnail_path}")
                    success_count += 1
                else:
                    logger.error(f"❌ collection '{collection.name}' translatedfailed")
                    
            except Exception as e:
                logger.error(f"❌ collection '{collection.name}' processing failed: {e}")
                db.rollback()
                continue
        
        logger.info(f"🎉 translated！succeededtranslated {success_count}/{len(collections_without_thumbnails)}  collectiontranslated")
        return True
        
    except Exception as e:
        logger.error(f"❌ translatedcollectiontranslatederror: {e}")
        return False
    finally:
        db.close()

def generate_thumbnail_for_collection(collection_id: str):
    """translatedcollectiontranslated"""
    try:
        db = next(get_db())
        
        collection = db.query(Collection).filter(Collection.id == collection_id).first()
        if not collection:
            logger.error(f"collectionnot found: {collection_id}")
            return False
        
        if collection.thumbnail_path:
            logger.info(f"collection '{collection.name}' translated")
            return True
        
        # checkIstranslatedexportvideofile
        if not collection.export_path:
            logger.error(f"collection '{collection.name}' translatedexportvideofile")
            return False
        
        video_path = Path(collection.export_path)
        if not video_path.exists():
            logger.error(f"collection '{collection.name}' 'svideofile not found: {video_path}")
            return False
        
        # translatedfiletranslated
        safe_name = "".join(c for c in collection.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        thumbnail_filename = f"{collection.id}_{safe_name}_thumbnail.jpg"
        thumbnail_path = video_path.parent / thumbnail_filename
        
        # useVideoProcessortranslated
        thumbnail_success = VideoProcessor.extract_thumbnail(video_path, thumbnail_path, time_offset=5)
        
        if thumbnail_success:
            # updatedatabase
            collection.thumbnail_path = str(thumbnail_path)
            db.commit()
            logger.info(f"✅ collection '{collection.name}' translatedsucceeded: {thumbnail_path}")
            return True
        else:
            logger.error(f"❌ collection '{collection.name}' translatedfailed")
            return False
            
    except Exception as e:
        logger.error(f"❌ translatedcollectiontranslatederror: {e}")
        return False
    finally:
        db.close()

def main():
    """translated"""
    import argparse
    
    parser = argparse.ArgumentParser(description='translatedcollectiontranslated')
    parser.add_argument('--collection-id', help='translatedcollectiontranslated')
    parser.add_argument('--all', action='store_true', help='translated'scollectiontranslated')
    
    args = parser.parse_args()
    
    if args.collection_id:
        success = generate_thumbnail_for_collection(args.collection_id)
    elif args.all:
        success = generate_collection_thumbnails()
    else:
        print("translated --collection-id or --all translated")
        return
    
    if success:
        print("translated")
    else:
        print("translatedfailed")
        sys.exit(1)

if __name__ == "__main__":
    main()
