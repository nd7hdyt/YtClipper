"""
translatedCelerytask
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
    """Uploadcliptask"""
    db = SessionLocal()
    try:
        logger.info(f"translatedUploadclip: record_id={record_id}, clip_id={clip_id}")
        
        # fetchtranslatedservice
        upload_service = BilibiliUploadService(db)
        
        # translatedrecord_idtranslated
        try:
            record_id_int = int(record_id)
        except ValueError:
            raise ValueError(f"translated'srecord_idformat: {record_id}")
        
        # fetchtranslated
        upload_record = upload_service.get_upload_record_by_id(record_id_int)
        if not upload_record:
            raise ValueError(f"translatednot found: {record_id}")
        
        # translatedvideofile path
        project_output_dir = get_project_output_directory(str(upload_record.project_id))
        logger.info(f"projecttranslateddirectory: {project_output_dir}")
        
        # fetchclipinfotranslated'sfiletranslated
        from ..models.clip import Clip
        clip = db.query(Clip).filter(Clip.id == clip_id).first()
        if not clip:
            raise ValueError(f"cliptranslatednot found: {clip_id}")
        
        clip_title = clip.title or clip.generated_title or ""
        logger.info(f"cliptranslated: {clip_title}")
        
        # translatedmultitranslatedcantranslated'sfiletranslated
        possible_paths = [
            project_output_dir / "clips" / f"{clip_id}.mp4",  # translated
            project_output_dir / "clips" / f"{clip_id}_clip_{clip_id}.mp4",  # translatedcliptranslated'stranslated
            project_output_dir / "clips" / f"{clip_id}_clip.mp4",  # translatedcliptranslated
        ]
        
        # iftranslatedcliptranslated，translated
        if clip_title:
            # cleantranslated'stranslated，usetranslatedfiletranslated
            import re
            clean_title = re.sub(r'[<>:"/\\|?*]', '', clip_title)
            possible_paths.extend([
                project_output_dir / "clips" / f"{clean_title}.mp4",
                project_output_dir / "clips" / f"*{clean_title}*.mp4",
            ])
        
        logger.info(f"translatedfile，cantranslated'spath: {[str(p) for p in possible_paths]}")
        
        # translatedvideofile
        video_path = None
        for path in possible_paths:
            if path.exists():
                video_path = path
                logger.info(f"translatedvideofile: {video_path}")
                break
        
        if not video_path:
            # iftranslatedpathtranslated，translatedinclipsdirectorytranslatedmp4file
            clips_dir = project_output_dir / "clips"
            if clips_dir.exists():
                mp4_files = list(clips_dir.glob("*.mp4"))
                logger.info(f"clipsdirectorytranslated'stranslatedmp4file: {[str(f) for f in mp4_files]}")
                
                # iftranslatedone mp4file，translatedusetranslated
                if len(mp4_files) == 1:
                    video_path = mp4_files[0]
                    logger.info(f"usetranslatedone'smp4file: {video_path}")
                else:
                    # translatedfiletranslated
                    if clip_title:
                        for mp4_file in mp4_files:
                            # checkfiletranslatedIstranslatedPackageincludetranslated'stranslated
                            if any(keyword in mp4_file.name for keyword in clip_title.split()[:3]):  # usetranslated'stranslated3 translated
                                video_path = mp4_file
                                logger.info(f"translated: {video_path}")
                                break
                    
                    # iftranslatedIstranslated，translatedclip_idtranslated
                    if not video_path:
                        for mp4_file in mp4_files:
                            if clip_id in mp4_file.name:
                                video_path = mp4_file
                                logger.info(f"translatedclip_idtranslated: {video_path}")
                                break
        
        if not video_path:
            raise FileNotFoundError(f"translatedclipvideofile: {clip_id}")
        
        # checkfiletranslated
        file_size = video_path.stat().st_size
        logger.info(f"videofiletranslated: {file_size} bytes")
        
        if file_size == 0:
            raise ValueError("videofiletranslated")
        
        # translatedUpload
        logger.info(f"translatedUploadvideo: {video_path}")
        success = upload_service.upload_clip_sync(record_id_int, str(video_path))
        
        if success:
            logger.info(f"clipUploadsucceeded: {clip_id}")
            upload_service.update_upload_status(record_id_int, "success")
        else:
            logger.error(f"clipUploadfailed: {clip_id}")
            upload_service.update_upload_status(record_id_int, "failed", "Uploadfailed")
            
    except Exception as e:
        logger.error(f"Uploadcliptaskfailed: {str(e)}")
        upload_service.update_upload_status(record_id_int, "failed", str(e))
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name='backend.tasks.upload.upload_project_task')
def upload_project_task(self, record_id: str, clip_ids: list):
    """Uploadprojecttask"""
    db = SessionLocal()
    try:
        logger.info(f"translatedUploadproject: record_id={record_id}, clip_ids={clip_ids}")
        
        # fetchtranslatedservice
        upload_service = BilibiliUploadService(db)
        
        # translatedrecord_idtranslated
        try:
            record_id_int = int(record_id)
        except ValueError:
            raise ValueError(f"translated'srecord_idformat: {record_id}")
        
        # fetchtranslated
        upload_record = upload_service.get_upload_record_by_id(record_id_int)
        if not upload_record:
            raise ValueError(f"translatednot found: {record_id}")
        
        # translatedvideofile path
        project_output_dir = get_project_output_directory(str(upload_record.project_id))
        logger.info(f"projecttranslateddirectory: {project_output_dir}")
        
        # translatedclipfile
        clips_dir = project_output_dir / "clips"
        if not clips_dir.exists():
            raise FileNotFoundError(f"clipsdirectorynot found: {clips_dir}")
        
        # fetchtranslatedmp4file
        mp4_files = list(clips_dir.glob("*.mp4"))
        logger.info(f"translated'smp4file: {[str(f) for f in mp4_files]}")
        
        if not mp4_files:
            raise FileNotFoundError("translatedmp4file")
        
        # iftranslatedone file，translatedUpload
        if len(mp4_files) == 1:
            video_path = mp4_files[0]
            logger.info(f"translated fileUpload: {video_path}")
            
            # checkfiletranslated
            file_size = video_path.stat().st_size
            if file_size == 0:
                raise ValueError("videofiletranslated")
            
            # translatedUpload
            success = upload_service.upload_clip(record_id_int, str(video_path))
            
            if success:
                logger.info("projectUploadsucceeded")
                upload_service.update_upload_status(record_id_int, "success")
            else:
                logger.error("projectUploadfailed")
                upload_service.update_upload_status(record_id_int, "failed", "Uploadfailed")
        else:
            # multi file'stranslated，thistranslatedcantranslatedUploadortranslatedUpload
            logger.warning(f"translatedmulti videofile，translatedsupporttranslated fileUpload: {len(mp4_files)}")
            upload_service.update_upload_status(record_id_int, "failed", "translatedsupportmultifileUpload")
            
    except Exception as e:
        logger.error(f"Uploadprojecttaskfailed: {str(e)}")
        upload_service.update_upload_status(record_id_int, "failed", str(e))
        raise
    finally:
        db.close()