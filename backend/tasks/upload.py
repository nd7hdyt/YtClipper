"""
ENCelerytask
"""

import logging
from pathlib import Path
from sqlalchemy.orm import Session

from ..core.celery_app import celery_app
from ..core.database import SessionLocal
from ..services.bilibili_service import BilibiliUploadService
from ..core.path_utils import get_project_output_directory

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name='backend.tasks.upload.upload_clip_task')
def upload_clip_task(self, record_id: str, clip_id: str):
    """uploadcliptask"""
    db = SessionLocal()
    try:
        logger.info(f"startuploadclip: record_id={record_id}, clip_id={clip_id}")
        
        # fetchENservice
        upload_service = BilibiliUploadService(db)
        
        # ENrecord_idEN
        try:
            record_id_int = int(record_id)
        except ValueError:
            raise ValueError(f"ENrecord_idEN: {record_id}")
        
        # fetchEN
        upload_record = upload_service.get_upload_record_by_id(record_id_int)
        if not upload_record:
            raise ValueError(f"ENdoes not exist: {record_id}")
        
        # ENvideofilepath
        project_output_dir = get_project_output_directory(str(upload_record.project_id))
        logger.info(f"projectENdirectory: {project_output_dir}")
        
        # fetchclipENfileEN
        from ..models.clip import Clip
        clip = db.query(Clip).filter(Clip.id == clip_id).first()
        if not clip:
            raise ValueError(f"clipENdoes not exist: {clip_id}")
        
        clip_title = clip.title or clip.generated_title or ""
        logger.info(f"cliptitle: {clip_title}")
        
        # ENmayENfileEN
        possible_paths = [
            project_output_dir / "clips" / f"{clip_id}.mp4",  # EN
            project_output_dir / "clips" / f"{clip_id}_clip_{clip_id}.mp4",  # ENclipEN
            project_output_dir / "clips" / f"{clip_id}_clip.mp4",  # ENclipEN
        ]
        
        # ifclipENtitle，ENthroughtitleEN
        if clip_title:
            # ENtitleEN，ENfileEN
            import re
            clean_title = re.sub(r'[<>:"/\\|?*]', '', clip_title)
            possible_paths.extend([
                project_output_dir / "clips" / f"{clean_title}.mp4",
                project_output_dir / "clips" / f"*{clean_title}*.mp4",
            ])
        
        logger.info(f"ENfile，mayENpath: {[str(p) for p in possible_paths]}")
        
        # ENvideofile
        video_path = None
        for path in possible_paths:
            if path.exists():
                video_path = path
                logger.info(f"ENvideofile: {video_path}")
                break
        
        if not video_path:
            # ifENpathEN，ENclipsdirectoryENallmp4file
            clips_dir = project_output_dir / "clips"
            if clips_dir.exists():
                mp4_files = list(clips_dir.glob("*.mp4"))
                logger.info(f"clipsdirectoryENallmp4file: {[str(f) for f in mp4_files]}")
                
                # ifENmp4file，ENuseEN
                if len(mp4_files) == 1:
                    video_path = mp4_files[0]
                    logger.info(f"useENmp4file: {video_path}")
                else:
                    # ENthroughtitleENfileEN
                    if clip_title:
                        for mp4_file in mp4_files:
                            # checkfileENtitleEN
                            if any(keyword in mp4_file.name for keyword in clip_title.split()[:3]):  # usetitleEN3EN
                                video_path = mp4_file
                                logger.info(f"throughtitleEN: {video_path}")
                                break
                    
                    # ifEN，ENthroughclip_idEN
                    if not video_path:
                        for mp4_file in mp4_files:
                            if clip_id in mp4_file.name:
                                video_path = mp4_file
                                logger.info(f"throughclip_idEN: {video_path}")
                                break
        
        if not video_path:
            raise FileNotFoundError(f"not foundclipvideofile: {clip_id}")
        
        # checkfileEN
        file_size = video_path.stat().st_size
        logger.info(f"videofileEN: {file_size} bytes")
        
        if file_size == 0:
            raise ValueError("videofileEN")
        
        # executeupload
        logger.info(f"startuploadvideo: {video_path}")
        success = upload_service.upload_clip_sync(record_id_int, str(video_path))
        
        if success:
            logger.info(f"clipuploadsucceeded: {clip_id}")
            upload_service.update_upload_status(record_id_int, "success")
        else:
            logger.error(f"clipuploadfailed: {clip_id}")
            upload_service.update_upload_status(record_id_int, "failed", "uploadfailed")
            
    except Exception as e:
        logger.error(f"uploadcliptaskfailed: {str(e)}")
        upload_service.update_upload_status(record_id_int, "failed", str(e))
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name='backend.tasks.upload.upload_project_task')
def upload_project_task(self, record_id: str, clip_ids: list):
    """uploadprojecttask"""
    db = SessionLocal()
    try:
        logger.info(f"startuploadproject: record_id={record_id}, clip_ids={clip_ids}")
        
        # fetchENservice
        upload_service = BilibiliUploadService(db)
        
        # ENrecord_idEN
        try:
            record_id_int = int(record_id)
        except ValueError:
            raise ValueError(f"ENrecord_idEN: {record_id}")
        
        # fetchEN
        upload_record = upload_service.get_upload_record_by_id(record_id_int)
        if not upload_record:
            raise ValueError(f"ENdoes not exist: {record_id}")
        
        # ENvideofilepath
        project_output_dir = get_project_output_directory(str(upload_record.project_id))
        logger.info(f"projectENdirectory: {project_output_dir}")
        
        # ENallclipfile
        clips_dir = project_output_dir / "clips"
        if not clips_dir.exists():
            raise FileNotFoundError(f"clipsdirectorydoes not exist: {clips_dir}")
        
        # fetchallmp4file
        mp4_files = list(clips_dir.glob("*.mp4"))
        logger.info(f"ENmp4file: {[str(f) for f in mp4_files]}")
        
        if not mp4_files:
            raise FileNotFoundError("not foundENmp4file")
        
        # ifENfile，ENupload
        if len(mp4_files) == 1:
            video_path = mp4_files[0]
            logger.info(f"ENfileupload: {video_path}")
            
            # checkfileEN
            file_size = video_path.stat().st_size
            if file_size == 0:
                raise ValueError("videofileEN")
            
            # executeupload
            success = upload_service.upload_clip(record_id_int, str(video_path))
            
            if success:
                logger.info("projectuploadsucceeded")
                upload_service.update_upload_status(record_id_int, "success")
            else:
                logger.error("projectuploadfailed")
                upload_service.update_upload_status(record_id_int, "failed", "uploadfailed")
        else:
            # ENfileEN，ENcanENuploadENupload
            logger.warning(f"ENvideofile，currentENfileupload: {len(mp4_files)}")
            upload_service.update_upload_status(record_id_int, "failed", "ENfileupload")
            
    except Exception as e:
        logger.error(f"uploadprojecttaskfailed: {str(e)}")
        upload_service.update_upload_status(record_id_int, "failed", str(e))
        raise
    finally:
        db.close()