#!/usr/bin/env python3
"""
ENallcollectiongenerateEN
"""
import sys
import os
from pathlib import Path

# ENprojectENdirectoryENPythonpath
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.core.database import get_db
from backend.models.collection import Collection
from backend.utils.video_processor import VideoProcessor
import logging

# configlog
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_collection_thumbnails():
    """ENallENcollectiongenerateEN"""
    try:
        db = next(get_db())
        
        # ENallENcollection
        collections_without_thumbnails = db.query(Collection).filter(
            Collection.thumbnail_path.is_(None)
        ).all()
        
        if not collections_without_thumbnails:
            logger.info("allcollectionENalreadyEN")
            return True
        
        logger.info(f"EN {len(collections_without_thumbnails)} ENcollection")
        
        success_count = 0
        for collection in collections_without_thumbnails:
            try:
                logger.info(f"currentlyENcollection '{collection.name}' ({collection.id}) generateEN...")
                
                # checkENvideofile
                if not collection.export_path:
                    logger.warning(f"collection '{collection.name}' ENvideofile，EN")
                    continue
                
                video_path = Path(collection.export_path)
                if not video_path.exists():
                    logger.warning(f"collection '{collection.name}' ENvideofiledoes not exist: {video_path}")
                    continue
                
                # generateENfileEN
                safe_name = "".join(c for c in collection.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_name = safe_name.replace(' ', '_')
                thumbnail_filename = f"{collection.id}_{safe_name}_thumbnail.jpg"
                thumbnail_path = video_path.parent / thumbnail_filename
                
                # useVideoProcessorgenerateEN
                thumbnail_success = VideoProcessor.extract_thumbnail(video_path, thumbnail_path, time_offset=5)
                
                if thumbnail_success:
                    # updatedatabase
                    collection.thumbnail_path = str(thumbnail_path)
                    db.commit()
                    logger.info(f"✅ collection '{collection.name}' ENgeneratesucceeded: {thumbnail_path}")
                    success_count += 1
                else:
                    logger.error(f"❌ collection '{collection.name}' ENgeneratefailed")
                    
            except Exception as e:
                logger.error(f"❌ collection '{collection.name}' processingfailed: {e}")
                db.rollback()
                continue
        
        logger.info(f"🎉 EN！succeededEN {success_count}/{len(collections_without_thumbnails)} ENcollectiongenerateEN")
        return True
        
    except Exception as e:
        logger.error(f"❌ generatecollectionENerror: {e}")
        return False
    finally:
        db.close()

def generate_thumbnail_for_collection(collection_id: str):
    """ENcollectiongenerateEN"""
    try:
        db = next(get_db())
        
        collection = db.query(Collection).filter(Collection.id == collection_id).first()
        if not collection:
            logger.error(f"collectiondoes not exist: {collection_id}")
            return False
        
        if collection.thumbnail_path:
            logger.info(f"collection '{collection.name}' alreadyEN")
            return True
        
        # checkENvideofile
        if not collection.export_path:
            logger.error(f"collection '{collection.name}' ENvideofile")
            return False
        
        video_path = Path(collection.export_path)
        if not video_path.exists():
            logger.error(f"collection '{collection.name}' ENvideofiledoes not exist: {video_path}")
            return False
        
        # generateENfileEN
        safe_name = "".join(c for c in collection.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        thumbnail_filename = f"{collection.id}_{safe_name}_thumbnail.jpg"
        thumbnail_path = video_path.parent / thumbnail_filename
        
        # useVideoProcessorgenerateEN
        thumbnail_success = VideoProcessor.extract_thumbnail(video_path, thumbnail_path, time_offset=5)
        
        if thumbnail_success:
            # updatedatabase
            collection.thumbnail_path = str(thumbnail_path)
            db.commit()
            logger.info(f"✅ collection '{collection.name}' ENgeneratesucceeded: {thumbnail_path}")
            return True
        else:
            logger.error(f"❌ collection '{collection.name}' ENgeneratefailed")
            return False
            
    except Exception as e:
        logger.error(f"❌ generatecollectionENerror: {e}")
        return False
    finally:
        db.close()

def main():
    """EN"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ENcollectiongenerateEN')
    parser.add_argument('--collection-id', help='ENcollectiongenerateEN')
    parser.add_argument('--all', action='store_true', help='ENallENcollectiongenerateEN')
    
    args = parser.parse_args()
    
    if args.collection_id:
        success = generate_thumbnail_for_collection(args.collection_id)
    elif args.all:
        success = generate_collection_thumbnails()
    else:
        print("pleaseEN --collection-id EN --all parameters")
        return
    
    if success:
        print("EN")
    else:
        print("ENfailed")
        sys.exit(1)

if __name__ == "__main__":
    main()
