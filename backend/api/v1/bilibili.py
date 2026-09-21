"""
BsitetranslatedAPItranslated
processBsitevideotranslatedAnddownloadfeature
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from pydantic import BaseModel
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from ...utils.bilibili_downloader import BilibiliDownloader, get_bilibili_video_info
from ...core.config import get_data_directory
from pathlib import Path
import uuid
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

# translateddownloadtask'sstatus
download_tasks = {}

class BilibiliParseRequest(BaseModel):
    url: str
    browser: Optional[str] = None

class BilibiliDownloadRequest(BaseModel):
    url: str
    project_name: str
    video_category: Optional[str] = "default"
    browser: Optional[str] = None

class BilibiliVideoInfo(BaseModel):
    title: str
    description: str
    duration: int
    uploader: str
    upload_date: str
    view_count: int
    like_count: int
    thumbnail: str

class BilibiliDownloadTask(BaseModel):
    id: str
    url: str
    project_name: str
    video_category: str
    status: str  # pending, processing, completed, failed
    progress: float
    error_message: Optional[str] = None
    project_id: Optional[str] = None
    created_at: str
    updated_at: str

@router.post("/parse")
async def parse_bilibili_video(
    url: str = Form(...),
    browser: Optional[str] = Form(None)
):
    """translatedBsitevideoinfo"""
    try:
        logger.info(f"translatedBsitevideo: {url}")
        
        # verifyURLformat
        downloader = BilibiliDownloader(browser=browser)
        if not downloader.validate_bilibili_url(url):
            raise HTTPException(status_code=400, detail="translated'sBsitevideotranslated")
        
        # fetchtranslated'svideoinfo
        video_info = await downloader.get_video_info(url)
        
        logger.info(f"videoinfotranslatedsucceeded: {video_info.title}")
        
        return {
            "success": True,
            "video_info": {
                "title": video_info.title,
                "description": video_info.description,
                "duration": video_info.duration,
                "uploader": video_info.uploader,
                "upload_date": video_info.upload_date,
                "view_count": video_info.view_count,
                "like_count": 0,  # BsiteAPIcantranslatedProvidestranslated
                "thumbnail": video_info.thumbnail_url
            }
        }
        
    except Exception as e:
        logger.error(f"translatedBsitevideofailed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"translatedfailed: {str(e)}")

@router.post("/download")
async def create_bilibili_download_task(request: BilibiliDownloadRequest):
    """createBsitevideodownloadtask - translatedcreateproject"""
    try:
        logger.info(f"createBsitedownloadtask: {request.url}")
        
        # translatedfetchvideoinfotranslatedfetchtranslated
        from ...utils.bilibili_downloader import BilibiliDownloader
        downloader = BilibiliDownloader(browser=request.browser)
        video_info = await downloader.get_video_info(request.url)
        
        # translatedcreateprojecttranslated
        from ...core.database import SessionLocal
        from ...services.project_service import ProjectService
        from ...schemas.project import ProjectCreate, ProjectType, ProjectStatus
        
        db = SessionLocal()
        try:
            project_service = ProjectService(db)
            
            # processtranslated - translatedusetranslated'stranslated
            thumbnail_data = None
            if video_info.thumbnail_url:
                try:
                    import requests
                    import base64
                    
                    # downloadtranslated
                    response = requests.get(video_info.thumbnail_url, timeout=10)
                    if response.status_code == 200:
                        # translatedbase64
                        thumbnail_base64 = base64.b64encode(response.content).decode('utf-8')
                        thumbnail_data = f"data:image/jpeg;base64,{thumbnail_base64}"
                        logger.info(f"Bsitetranslatedfetchsucceeded: {video_info.title}")
                    else:
                        logger.warning(f"downloadBsitetranslatedfailed: {response.status_code}")
                except Exception as e:
                    logger.error(f"processBsitetranslatedfailed: {e}")
                    # translatedprocessing failedtranslated
            
            # createprojecttranslated
            project_data = ProjectCreate(
                name=request.project_name,
                description=f"fromBsitedownload: {video_info.title}",
                project_type=ProjectType(request.video_category),
                status=ProjectStatus.PtranslatedDING,  # translatedstatustranslatedetc.translated
                source_url=request.url,
                source_file=None,  # translated，downloadtranslatedupdate
                settings={
                    "download_status": "downloading",
                    "download_progress": 0.0,
                    "bilibili_info": {
                        "url": request.url,
                        "browser": request.browser,
                        "title": video_info.title,
                        "uploader": video_info.uploader,
                        "duration": video_info.duration,
                        "view_count": video_info.view_count,
                        "thumbnail_url": video_info.thumbnail_url
                    }
                }
            )
            
            project = project_service.create_project(project_data)
            project_id = str(project.id)
            
            # settingstranslated
            if thumbnail_data:
                project.thumbnail = thumbnail_data
                db.commit()
                logger.info(f"project {project_id} translatedsettings")
            
            # createprojectdirectory
            from ...core.path_utils import get_project_directory
            project_dir = get_project_directory(project_id)
            raw_dir = project_dir / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"projecttranslatedcreate: {project_id}")
            
            # translateddownloadtaskID
            task_id = str(uuid.uuid4())
            
            # createtasktranslated
            task = BilibiliDownloadTask(
                id=task_id,
                url=request.url,
                project_name=request.project_name,
                video_category=request.video_category,
                status="pending",
                progress=0.0,
                project_id=project_id,  # translatedprojectID
                created_at=str(uuid.uuid1().time),
                updated_at=str(uuid.uuid1().time)
            )
            
            # translatedtask
            download_tasks[task_id] = task
            
            # translatedstartdownloadtask - usetranslated'stasktranslated
            from .async_task_manager import task_manager
            await task_manager.create_safe_task(
                f"bilibili_download_{task_id}", 
                process_download_task, 
                task_id, 
                request, 
                project_id
            )
            
            # returnprojectinfotranslatedIstaskinfo
            return {
                "project_id": project_id,
                "task_id": task_id,
                "status": "created",
                "message": "projecttranslatedcreate，translatedindownloadtranslated..."
            }
            
        finally:
            db.close()
        
    except Exception as e:
        logger.error(f"createdownloadtaskfailed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"createtaskfailed: {str(e)}")

@router.get("/tasks/{task_id}")
async def get_bilibili_task_status(task_id: str):
    """fetchdownloadtaskstatus"""
    if task_id not in download_tasks:
        raise HTTPException(status_code=404, detail="tasknot found")
    
    return download_tasks[task_id]

@router.get("/tasks")
async def get_all_bilibili_tasks():
    """fetchtranslateddownloadtask"""
    return list(download_tasks.values())

async def update_project_download_progress(project_id: str, progress: float, message: str):
    """updateprojectdownloadprogress"""
    try:
        from ...core.database import SessionLocal
        from ...services.project_service import ProjectService
        
        db = SessionLocal()
        try:
            project_service = ProjectService(db)
            project = project_service.get(project_id)
            
            if project:
                # updateprojectsettingstranslated'sdownloadprogress
                if not project.processing_config:
                    project.processing_config = {}
                
                project.processing_config.update({
                    "download_progress": progress,
                    "download_message": message
                })
                
                # iftranslatedprogresstranslated100%，updatestatustranslatedetc.translatedprocess
                if progress >= 100.0:
                    from ...schemas.project import ProjectStatus
                    project.status = ProjectStatus.PtranslatedDING
                
                db.commit()
                logger.info(f"project {project_id} downloadprogressupdate: {progress}% - {message}")
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"updateprojectdownloadprogressfailed: {e}")

async def process_download_task(task_id: str, request: BilibiliDownloadRequest, project_id: str):
    """processdownloadtask"""
    try:
        # updatetaskstatustranslatedprocessing
        download_tasks[task_id].status = "processing"
        download_tasks[task_id].progress = 10.0
        
        # updateprojectstatusAndprogress
        await update_project_download_progress(project_id, 10.0, "translatedinfetchvideoinfo...")
        
        # fetchvideoinfo
        video_info = await get_bilibili_video_info(request.url, request.browser)
        download_tasks[task_id].progress = 30.0
        
        # updateprojectprogress
        await update_project_download_progress(project_id, 30.0, "translatedindownloadvideo...")
        
        # downloadvideo
        data_dir = get_data_directory()
        download_dir = data_dir / "temp"
        download_dir.mkdir(exist_ok=True)
        
        from ...utils.bilibili_downloader import download_bilibili_video
        download_result = await download_bilibili_video(
            request.url, 
            download_dir, 
            request.browser
        )
        
        video_path = download_result.get('video_path', '')
        subtitle_path = download_result.get('subtitle_path', '')
        
        # updateprojectprogress
        await update_project_download_progress(project_id, 60.0, "videodownloadtranslated，translatedinprocesssubtitles...")
        
        # iftranslatedsubtitlesfile，translateduseWhispergenerate subtitles
        if not subtitle_path and video_path:
            logger.info("translateduseWhispertranslatedsubtitles")
            # updateprojectprogress
            await update_project_download_progress(project_id, 70.0, "translatedinuseWhispergenerate subtitles...")
            
            try:
                from ...utils.speech_recognizer import generate_subtitle_for_video, SpeechRecognitionError
                from pathlib import Path
                video_file_path = Path(video_path)
                
                # translatedvideoinfoSelectselecttranslated'smodel，translatedusetranslatedLanguagetranslated
                model = "base"  # defaultusetranslatedmodel
                language = "auto"  # translatedusetranslatedLanguagetranslated
                
                # cantranslatedvideotranslatedortranslated，Selectselecttranslated'smodeltranslated
                if video_info.title and any(keyword in video_info.title.lower() for keyword in ['translated', 'translated', 'translated', 'translated']):
                    model = "small"  # translatedusetranslated'smodel
                elif video_info.title and any(keyword in video_info.title.lower() for keyword in ['translated', 'translated', 'translated']):
                    model = "medium"  # translatedusetranslatedmodel
                
                logger.info(f"useWhispergenerate subtitles - Language: {language}, model: {model}")
                
                generated_subtitle = generate_subtitle_for_video(
                    video_file_path,
                    language=language,
                    model=model
                )
                subtitle_path = str(generated_subtitle)
                logger.info(f"Whispersubtitlestranslatedsucceeded: {subtitle_path}")
                
                # updateprojectprogress
                await update_project_download_progress(project_id, 90.0, "subtitlestranslated，translatedintranslatedprocess...")
                
            except SpeechRecognitionError as e:
                logger.error(f"Whispersubtitlestranslatedfailed: {e}")
                # Whisperfailedtranslated，translatedprojecttranslatedfailedstatus
                logger.error("subtitlesfile not foundtranslatedWhispertranslatedfailed，projecttranslatedfailedstatus")
                subtitle_path = None  # ensuresubtitlespathtranslated，translatedprojectfailed
            except Exception as e:
                logger.error(f"generate subtitlestranslatederror: {e}")
                subtitle_path = None  # ensuresubtitlespathtranslated，translatedprojectfailed
        
        download_tasks[task_id].progress = 80.0
        
        # updateprojectinfo（projecttranslatedintranslatedcreate）
        from ...services.project_service import ProjectService
        from ...core.database import SessionLocal
        
        db = SessionLocal()
        try:
            project_service = ProjectService(db)
            
            # fetchtranslatedcreate'sproject
            project = project_service.get(project_id)
            if not project:
                raise Exception(f"project {project_id} not found")
            
            # updateprojectinfo
            project.description = f"fromBsitedownload: {video_info.title}"
            # translated：Do notinthistranslatedsettingsvideo_path，etc.filetranslatedsettings
            
            # updateprojectsettings
            if not project.processing_config:
                project.processing_config = {}
            
            project.processing_config.update({
                "bilibili_info": {
                    "title": video_info.title,
                    "uploader": video_info.uploader,
                    "duration": video_info.duration,
                    "view_count": video_info.view_count
                },
                "subtitle_path": subtitle_path if subtitle_path else None,
                "download_status": "completed",
                "download_progress": 100.0
            })
            
            # translatedfiletranslatedprojectdirectory
            from ...core.path_utils import get_project_directory
            project_dir = get_project_directory(project_id)
            raw_dir = project_dir / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            
            # translatedvideofiletranslatedprojectdirectory
            import shutil
            from pathlib import Path
            
            if video_path:
                video_file_path = Path(video_path)
                if video_file_path.exists():
                    # translatedvideofiletranslatedinput.mp4
                    new_video_path = raw_dir / "input.mp4"
                    shutil.move(str(video_file_path), str(new_video_path))
                    logger.info(f"videofiletranslated: {new_video_path}")
                    
                    # updateprojecttranslated'svideopath
                    project.video_path = str(new_video_path)
            
            # translatedsubtitlesfiletranslatedprojectdirectory
            if subtitle_path and subtitle_path.strip():
                subtitle_file_path = Path(subtitle_path)
                if subtitle_file_path.exists():
                    # translatedsubtitlesfiletranslatedinput.srt
                    new_subtitle_path = raw_dir / "input.srt"
                    shutil.move(str(subtitle_file_path), str(new_subtitle_path))
                    logger.info(f"subtitlesfiletranslated: {new_subtitle_path}")
                    
                    # updateprojectprocessconfigtranslated'ssubtitlespath
                    if not project.processing_config:
                        project.processing_config = {}
                    project.processing_config["subtitle_path"] = str(new_subtitle_path)
            
            # translatedprojectupdate
            db.commit()
            
            # checksubtitlesfileIstranslatedin，iftranslatednot foundtranslatedprojecttranslatedfailed
            srt_file_path = raw_dir / "input.srt"
            if not srt_file_path.exists():
                logger.error(f"subtitlesfile not found: {srt_file_path}，projecttranslatedfailedstatus")
                from ...schemas.project import ProjectStatus
                project.status = ProjectStatus.FAILED
                if not project.processing_config:
                    project.processing_config = {}
                project.processing_config["error_message"] = "subtitlesfile not foundtranslatedWhispertranslatedfailed"
                db.commit()
                
                # updatetaskstatustranslatedfailed
                download_tasks[task_id].status = "failed"
                download_tasks[task_id].error_message = "subtitlesfile not foundtranslatedWhispertranslatedfailed"
                download_tasks[task_id].progress = 0.0
                download_tasks[task_id].project_id = str(project.id)
                download_tasks[task_id].updated_at = datetime.now().isoformat()
                
                # updateprojectdownloadprogresstranslatedfailed
                await update_project_download_progress(project_id, 0.0, "downloadfailed：subtitlesfile not found")
                
                logger.info(f"Bsitedownloadtaskfailed: {task_id}, projectID: {project.id}, translated: subtitlesfile not found")
                return
            
            # updateprojectdownloadprogresstranslated
            await update_project_download_progress(project_id, 100.0, "downloadtranslated，translatedprocess")
            
            # updatetaskstatus
            download_tasks[task_id].status = "completed"
            download_tasks[task_id].progress = 100.0
            download_tasks[task_id].project_id = str(project.id)
            download_tasks[task_id].updated_at = datetime.now().isoformat()
            
            logger.info(f"Bsitedownloadtasktranslated: {task_id}, projectID: {project.id}")
            
            # translatedstartprocesstranslated
            try:
                # updateprojectstatustranslatedetc.translatedprocess
                from ...schemas.project import ProjectStatus
                project.status = ProjectStatus.PtranslatedDING  # translatedPtranslatedDING，translatedservicestart
                db.commit()
                
                logger.info(f"Bsiteproject {project.id} downloadtranslated，etc.translatedstart")
                
                # translatedstarttranslated
                import asyncio
                from ...services.auto_pipeline_service import auto_pipeline_service
                
                # usecreate_taskintranslated'stranslated
                try:
                    loop = asyncio.get_running_loop()
                    # intranslated'stranslatedcreatetask
                    task = loop.create_task(
                        auto_pipeline_service.auto_start_pipeline(str(project.id))
                    )
                    # etc.translatedtasktranslated
                    pipeline_result = await task
                except RuntimeError:
                    # iftranslated'stranslated，createtranslated's
                    pipeline_result = await auto_pipeline_service.auto_start_pipeline(str(project.id))
                
                if pipeline_result['status'] == 'started':
                    logger.info(f"Bsiteproject {project.id} translatedstart: {pipeline_result}")
                else:
                    logger.warning(f"Bsiteproject {project.id} translatedstarttranslated: {pipeline_result}")
                
            except Exception as e:
                logger.error(f"startBsiteproject {project.id} translatedfailed: {str(e)}")
                # translatedprocessstartfailed，translatedreturndownloadsucceeded
                # usercantranslatedbytranslatedstartprocess
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"processdownloadtaskfailed: {str(e)}")
        download_tasks[task_id].status = "failed"
        download_tasks[task_id].error_message = str(e)
        download_tasks[task_id].progress = 0.0

        # translated 「project」translatedfailed，translatedprojecttranslatedin pending，
        # frontendtranslatedonetranslated translated「translatedstart」translated（translated'stranslatedone）。
        try:
            from ...core.database import SessionLocal
            from ...services.project_service import ProjectService
            from ...schemas.project import ProjectStatus
            db = SessionLocal()
            try:
                project_service = ProjectService(db)
                project = project_service.get(project_id)
                if project and project.status == ProjectStatus.PtranslatedDING:
                    project.status = ProjectStatus.FAILED
                    if not project.processing_config:
                        project.processing_config = {}
                    project.processing_config["error_message"] = f"downloadfailed: {e}"
                    db.commit()
                    logger.info(f"project {project_id} translatedfailed")
            finally:
                db.close()
        except Exception as inner:
            logger.error(f"translatedproject {project_id} failedstatustranslated: {inner}")
