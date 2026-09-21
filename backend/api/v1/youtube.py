"""
YouTube API routes.
Handles YouTube video parsing and downloads.
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from pydantic import BaseModel
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from ...core.config import get_data_directory
import uuid
import asyncio
from datetime import datetime
from contextlib import contextmanager
import os
import yt_dlp

logger = logging.getLogger(__name__)
router = APIRouter()

# Download task states
download_tasks = {}

# Requesting too many subtitle languages at once triggers YouTube HTTP 429 and fails the whole download;
# request Chinese + English by default, overridable via AUTOCLIP_YT_SUBTITLE_LANGS (comma-separated).
DEFAULT_SUBTITLE_LANGS = ['zh-Hans', 'zh', 'en']


def get_subtitle_langs() -> list:
    raw = os.getenv('AUTOCLIP_YT_SUBTITLE_LANGS', '')
    langs = [lang.strip() for lang in raw.split(',') if lang.strip()]
    return langs or list(DEFAULT_SUBTITLE_LANGS)


@contextmanager
def sanitized_yt_env():
    """Temporarily clear yt-dlp-related env vars so external config cannot change behavior"""
    original_env = os.environ.copy()
    try:
        for key in list(os.environ.keys()):
            upper_key = key.upper()
            if upper_key.startswith("YT_DLP") or upper_key.startswith("YTDL") or upper_key.startswith("YOUTUBE_DL") or upper_key.startswith("YOUTUBEDL"):
                os.environ.pop(key, None)
        yield
    finally:
        os.environ.clear()
        os.environ.update(original_env)

class YouTubeParseRequest(BaseModel):
    url: str
    browser: Optional[str] = None

class YouTubeDownloadRequest(BaseModel):
    url: str
    project_name: str
    video_category: Optional[str] = "default"
    browser: Optional[str] = None

class YouTubeVideoInfo(BaseModel):
    title: str
    description: str
    duration: int
    uploader: str
    upload_date: str
    view_count: int
    like_count: int
    thumbnail: str

class YouTubeDownloadTask(BaseModel):
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
async def parse_youtube_video(
    url: str = Form(...),
    browser: Optional[str] = Form(None),
    client: Optional[str] = Form(None)
):
    """Parse YouTube video info"""
    try:
        logger.info(f"Parsing YouTube video: {url}")

        # Basic URL validation
        if "youtube.com" not in url and "youtu.be" not in url:
            raise HTTPException(status_code=400, detail="Invalid YouTube video URL")

        # Log versions for troubleshooting
        try:
            logger.info(f"yt-dlp={yt_dlp.version.__version__}, py={sys.executable}")
        except Exception:
            pass

        # Call the yt-dlp CLI via subprocess to avoid Python env config side effects
        import subprocess
        import json
        import asyncio

        def extract_info_sync(url, browser):
            # Use the current interpreter's yt_dlp module to match the backend runtime (venv / Docker / portable desktop Python)
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '--ignore-config',
                '--no-warnings',
                '--no-playlist',
                '--dump-json',
                '--skip-download',  # fixed option name
                '--no-cache-dir'
            ]

            if browser:
                cmd.extend(['--cookies-from-browser', browser.lower()])

            # Optional fallback client to work around SABR
            yt_client = (client or os.getenv('AUTOCLIP_YT_CLIENT', '')).strip().lower()
            if yt_client in {"android", "ios", "tv"}:
                cmd.extend(['--extractor-args', f"youtube:player_client={yt_client}"])

            cmd.append(url)

            try:
                # Run the command (sanitized env so YT_* does not interfere)
                env = os.environ.copy()
                for k in list(env.keys()):
                    uk = k.upper()
                    if uk.startswith('YT_DLP') or uk.startswith('YTDL') or uk.startswith('YOUTUBE_DL') or uk.startswith('YOUTUBEDL'):
                        env.pop(k, None)

                logger.info(f"Running command: {' '.join(cmd)}")
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=str(get_data_directory()),
                    env=env
                )

                logger.info(f"Command exit code: {result.returncode}")
                logger.info(f"Command output (first 200 chars): {result.stdout[:200]}...")
                if result.stderr:
                    logger.info(f"Command stderr: {result.stderr}")

                if result.returncode != 0:
                    raise Exception(f"yt-dlp failed: {result.stderr or result.stdout}")

                # Parse the JSON output
                info_dict = json.loads(result.stdout)
                return info_dict
                
            except subprocess.TimeoutExpired:
                raise Exception("yt-dlp timeout")
            except json.JSONDecodeError as e:
                raise Exception(f"Failed to parse yt-dlp output: {e}")
            except Exception as e:
                raise Exception(f"yt-dlp execution failed: {e}")
        
        loop = asyncio.get_event_loop()
        info_dict = await loop.run_in_executor(None, extract_info_sync, url, browser)

        logger.info(f"YouTube video info parsed: {info_dict.get('title', 'Unknown')}")
        
        return {
            "success": True,
            "video_info": {
                "title": info_dict.get('title', 'Unknown'),
                "description": info_dict.get('description', ''),
                "duration": info_dict.get('duration', 0) or 0,
                "uploader": info_dict.get('uploader', 'Unknown'),
                "upload_date": info_dict.get('upload_date', ''),
                "view_count": info_dict.get('view_count', 0),
                "like_count": info_dict.get('like_count', 0),
                "thumbnail": info_dict.get('thumbnail', '')
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to parse YouTube video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Parse failed: {str(e)}")

@router.post("/download")
async def create_youtube_download_task(request: YouTubeDownloadRequest):
    """Create a YouTube download task - creates the project immediately"""
    try:
        logger.info(f"Creating YouTube download task: {request.url}")

        # Fetch video info first for the thumbnail
        import yt_dlp
        import asyncio
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'ignoreconfig': True,
            'noplaylist': True,
            'config_locations': [],
            'cachedir': False,
        }
        
        if request.browser:
            ydl_opts['cookiesfrombrowser'] = (request.browser.lower(),)

        # Optional fallback client
        yt_client_env = os.getenv('AUTOCLIP_YT_CLIENT', '').strip().lower()
        if yt_client_env in {"android", "ios", "tv"}:
            ydl_opts.setdefault('extractor_args', {}).setdefault('youtube', {}).setdefault('player_client', []).append(yt_client_env)

        def extract_info_sync(url, ydl_opts):
            with sanitized_yt_env():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    return ydl.extract_info(url, download=False)

        loop = asyncio.get_event_loop()
        video_info = await loop.run_in_executor(None, extract_info_sync, request.url, ydl_opts)

        # Create the project record immediately
        from ...core.database import SessionLocal
        from ...services.project_service import ProjectService
        from ...schemas.project import ProjectCreate, ProjectType, ProjectStatus

        db = SessionLocal()
        try:
            project_service = ProjectService(db)

            # Handle the thumbnail - use the parsed cover directly
            thumbnail_data = None
            thumbnail_url = video_info.get('thumbnail', '')
            if thumbnail_url:
                try:
                    import requests
                    import base64

                    # Download the thumbnail
                    response = requests.get(thumbnail_url, timeout=10)
                    if response.status_code == 200:
                        # Encode as base64
                        thumbnail_base64 = base64.b64encode(response.content).decode('utf-8')
                        thumbnail_data = f"data:image/jpeg;base64,{thumbnail_base64}"
                        logger.info(f"YouTube thumbnail fetched: {video_info.get('title', 'Unknown')}")
                    else:
                        logger.warning(f"Failed to download YouTube thumbnail: {response.status_code}")
                except Exception as e:
                    logger.error(f"Failed to process YouTube thumbnail: {e}")
                    # Thumbnail failures must not block the main flow

            # Build the project data
            project_data = ProjectCreate(
                name=request.project_name,
                description=f"Downloaded from YouTube: {video_info.get('title', 'Unknown')}",
                project_type=ProjectType(request.video_category),
                status=ProjectStatus.PENDING,  # starts as pending
                source_url=request.url,
                source_file=None,  # empty until the download finishes
                settings={
                    "download_status": "downloading",
                    "download_progress": 0.0,
                    "youtube_info": {
                        "url": request.url,
                        "browser": request.browser,
                        "title": video_info.get('title', 'Unknown'),
                        "uploader": video_info.get('uploader', 'Unknown'),
                        "duration": video_info.get('duration', 0),
                        "view_count": video_info.get('view_count', 0),
                        "thumbnail_url": thumbnail_url
                    }
                }
            )

            project = project_service.create_project(project_data)
            project_id = str(project.id)

            # Set the thumbnail
            if thumbnail_data:
                project.thumbnail = thumbnail_data
                db.commit()
                logger.info(f"Project {project_id} thumbnail set")

            # Create the project directory
            from ...core.path_utils import get_project_directory
            project_dir = get_project_directory(project_id)
            raw_dir = project_dir / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)

            logger.info(f"Project created: {project_id}")

            # Generate a download task ID
            task_id = str(uuid.uuid4())

            # Create the task record
            task = YouTubeDownloadTask(
                id=task_id,
                url=request.url,
                project_name=request.project_name,
                video_category=request.video_category,
                status="pending",
                progress=0.0,
                project_id=project_id,  # linked project ID
                created_at=str(uuid.uuid1().time),
                updated_at=str(uuid.uuid1().time)
            )

            # Store the task
            download_tasks[task_id] = task

            # Start the download in the background - via the safe task manager
            from .async_task_manager import task_manager
            await task_manager.create_safe_task(
                f"youtube_download_{task_id}",
                process_youtube_download_task,
                task_id,
                request,
                project_id
            )

            # Return project info rather than task info
            return {
                "project_id": project_id,
                "task_id": task_id,
                "status": "created",
                "message": "Project created; download in progress..."
            }

        finally:
            db.close()

    except Exception as e:
        logger.error(f"Failed to create YouTube download task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

@router.get("/tasks/{task_id}")
async def get_youtube_task_status(task_id: str):
    """Get YouTube download task status"""
    if task_id not in download_tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    return download_tasks[task_id]

@router.get("/tasks")
async def get_all_youtube_tasks():
    """Get all YouTube download tasks"""
    return list(download_tasks.values())

async def update_project_download_progress(project_id: str, progress: float, message: str):
    """Update project download progress"""
    try:
        from ...core.database import SessionLocal
        from ...services.project_service import ProjectService
        
        db = SessionLocal()
        try:
            project_service = ProjectService(db)
            project = project_service.get(project_id)
            
            if project:
                # Update download progress in the project settings
                if not project.processing_config:
                    project.processing_config = {}

                project.processing_config.update({
                    "download_progress": progress,
                    "download_message": message
                })

                # Mark as pending once progress reaches 100%
                if progress >= 100.0:
                    from ...schemas.project import ProjectStatus
                    project.status = ProjectStatus.PENDING

                db.commit()
                logger.info(f"Project {project_id} download progress: {progress}% - {message}")

        finally:
            db.close()

    except Exception as e:
        logger.error(f"Failed to update project download progress: {e}")

async def process_youtube_download_task(task_id: str, request: YouTubeDownloadRequest, project_id: str):
    """Process a YouTube download task"""
    try:
        # Mark the task as processing
        download_tasks[task_id].status = "processing"
        download_tasks[task_id].progress = 10.0

        # Update project state and progress
        await update_project_download_progress(project_id, 10.0, "Fetching video info...")

        # Download with yt-dlp
        import yt_dlp
        import asyncio
        from ...core.config import get_data_directory

        data_dir = get_data_directory()
        download_dir = data_dir / "temp"
        download_dir.mkdir(exist_ok=True)

        # Update project progress
        await update_project_download_progress(project_id, 30.0, "Downloading video...")

        # Download options
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'writesubtitles': True,
            'writeautomaticsub': True,  # download auto-generated subtitles
            'subtitleslangs': get_subtitle_langs(),
            'subtitlesformat': 'srt',
            'outtmpl': str(download_dir / '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': False,  # show warnings for debugging
            'ignoreconfig': True,
            'config_locations': [],
            'cachedir': False,
        }

        if request.browser:
            ydl_opts['cookiesfrombrowser'] = (request.browser.lower(),)

        # Optional fallback client
        yt_client_env = os.getenv('AUTOCLIP_YT_CLIENT', '').strip().lower()
        if yt_client_env in {"android", "ios", "tv"}:
            ydl_opts.setdefault('extractor_args', {}).setdefault('youtube', {}).setdefault('player_client', []).append(yt_client_env)

        def download_sync(url, ydl_opts):
            with sanitized_yt_env():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    return ydl.download([url])

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, download_sync, request.url, ydl_opts)

        # Locate the downloaded files
        video_files = list(download_dir.glob("*.mp4"))
        subtitle_files = list(download_dir.glob("*.srt"))

        if not video_files:
            raise Exception("Downloaded video file not found")

        video_path = str(video_files[0])
        subtitle_path = str(subtitle_files[0]) if subtitle_files else ""

        download_tasks[task_id].progress = 80.0

        # Update project progress
        await update_project_download_progress(project_id, 60.0, "Video downloaded; processing subtitles...")

        # Without subtitles, prefer Whisper for generation
        if not subtitle_path:
            logger.info("No subtitles found; generating high-quality subtitles with Whisper")
            # Update project progress
            await update_project_download_progress(project_id, 70.0, "Generating subtitles with Whisper...")

            try:
                from ...utils.speech_recognizer import generate_subtitle_for_video, SpeechRecognitionError
                video_file_path = Path(video_path)

                # Model choice for the video
                model = "base"  # balanced default
                language = "auto"  # auto-detect by default

                # Smarter content-type detection could go here

                logger.info(f"Generating subtitles with Whisper - language: {language}, model: {model}")

                generated_subtitle = generate_subtitle_for_video(
                    video_file_path,
                    language=language,
                    model=model
                )
                subtitle_path = str(generated_subtitle)
                logger.info(f"Whisper subtitles generated: {subtitle_path}")

                # Update project progress
                await update_project_download_progress(project_id, 90.0, "Subtitles ready; preparing to process...")

            except SpeechRecognitionError as e:
                logger.error(f"Whisper subtitle generation failed: {e}")
                # On Whisper failure, try platform subtitles as a fallback
                logger.info("Trying platform subtitles as a fallback")
                try:
                    subtitle_path = await _try_youtube_subtitle_strategies(request.url, download_dir, request.browser)
                    if subtitle_path:
                        logger.info(f"Fallback subtitles fetched: {subtitle_path}")
                    else:
                        logger.warning("All subtitle strategies failed")
                        subtitle_path = None  # keep empty; project is marked failed below
                except Exception as backup_error:
                    logger.error(f"Fallback subtitle fetch also failed: {backup_error}")
                    subtitle_path = None  # keep empty; project is marked failed below
            except Exception as e:
                logger.error(f"Unknown error while generating subtitles: {e}")
                subtitle_path = None  # keep empty; project is marked failed below

        logger.info(f"Download finished - video: {video_path}, subtitles: {subtitle_path}")

        # Update project info (project was created at the start)
        from ...services.project_service import ProjectService
        from ...core.database import SessionLocal

        db = SessionLocal()
        try:
            project_service = ProjectService(db)

            # Fetch the created project
            project = project_service.get(project_id)
            if not project:
                raise Exception(f"Project {project_id} not found")

            # Update project info
            project.description = f"Downloaded from YouTube: {request.project_name}"
            # Note: video_path is set after the files are moved

            # Update project settings
            if not project.processing_config:
                project.processing_config = {}

            project.processing_config.update({
                "youtube_info": {
                    "title": request.project_name,
                    "uploader": "YouTube",
                    "duration": 0,
                    "view_count": 0,
                    "like_count": 0
                },
                "subtitle_path": subtitle_path,
                "download_status": "completed",
                "download_progress": 100.0
            })

            # Move files into the project directory
            from ...core.path_utils import get_project_directory
            project_dir = get_project_directory(project_id)
            raw_dir = project_dir / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)

            # Move the video file
            import shutil
            from pathlib import Path

            if video_path:
                video_file_path = Path(video_path)
                if video_file_path.exists():
                    # Rename to input.mp4
                    new_video_path = raw_dir / "input.mp4"
                    shutil.move(str(video_file_path), str(new_video_path))
                    logger.info(f"Video file moved to: {new_video_path}")

                    # Update the video path on the project
                    project.video_path = str(new_video_path)

            # Move the subtitle file
            if subtitle_path:
                subtitle_file_path = Path(subtitle_path)
                if subtitle_file_path.exists():
                    # Rename to input.srt
                    new_subtitle_path = raw_dir / "input.srt"
                    shutil.move(str(subtitle_file_path), str(new_subtitle_path))
                    logger.info(f"Subtitle file moved to: {new_subtitle_path}")

                    # Update the subtitle path in the processing config
                    if not project.processing_config:
                        project.processing_config = {}
                    project.processing_config["subtitle_path"] = str(new_subtitle_path)

            # Save project updates
            db.commit()

            # Without subtitles, mark the project as failed
            srt_file_path = raw_dir / "input.srt"
            if not srt_file_path.exists():
                logger.error(f"Subtitle file missing: {srt_file_path}; project will be marked as failed")
                from ...schemas.project import ProjectStatus
                project.status = ProjectStatus.FAILED
                if not project.processing_config:
                    project.processing_config = {}
                project.processing_config["error_message"] = "No subtitle file and Whisper generation failed"
                db.commit()

                # Mark the task as failed
                download_tasks[task_id].status = "failed"
                download_tasks[task_id].error_message = "No subtitle file and Whisper generation failed"
                download_tasks[task_id].progress = 0.0
                download_tasks[task_id].project_id = str(project.id)
                download_tasks[task_id].updated_at = datetime.now().isoformat()

                # Update project download progress as failed
                await update_project_download_progress(project_id, 0.0, "Download failed: no subtitle file")

                logger.info(f"YouTube download task failed: {task_id}, project: {project.id}, reason: missing subtitles")
                return

            # Mark project download progress complete
            await update_project_download_progress(project_id, 100.0, "Download complete; ready to process")

            # Update task state
            download_tasks[task_id].status = "completed"
            download_tasks[task_id].progress = 100.0
            download_tasks[task_id].project_id = str(project.id)
            download_tasks[task_id].updated_at = datetime.now().isoformat()

            logger.info(f"YouTube download task completed: {task_id}, project: {project.id}")

            # Auto-start processing
            try:
                # Set project state to pending
                from ...schemas.project import ProjectStatus
                project.status = ProjectStatus.PENDING  # PENDING so the automation pipeline picks it up
                db.commit()

                logger.info(f"YouTube project {project.id} downloaded; waiting for the auto pipeline")

                # Start the auto pipeline asynchronously
                import asyncio
                from ...services.auto_pipeline_service import auto_pipeline_service

                # Run inside the running event loop
                try:
                    loop = asyncio.get_running_loop()
                    # Create the task in the running loop
                    task = loop.create_task(
                        auto_pipeline_service.auto_start_pipeline(str(project.id))
                    )
                    # Wait for completion
                    pipeline_result = await task
                except RuntimeError:
                    # No running loop; create a new one
                    pipeline_result = await auto_pipeline_service.auto_start_pipeline(str(project.id))

                if pipeline_result['status'] == 'started':
                    logger.info(f"YouTube project {project.id} auto pipeline started: {pipeline_result}")
                else:
                    logger.warning(f"YouTube project {project.id} auto pipeline result: {pipeline_result}")

            except Exception as e:
                logger.error(f"Failed to start auto pipeline for YouTube project {project.id}: {str(e)}")
                # A processing-start failure still counts as a successful download
                # Users can restart processing via the retry button

        except Exception as e:
            logger.error(f"Failed to create project: {str(e)}")
            # A processing-start failure still counts as a successful download
            # Users can restart processing via the retry button

        finally:
            db.close()

    except Exception as e:
        logger.error(f"Failed to process download task: {str(e)}")
        download_tasks[task_id].status = "failed"
        download_tasks[task_id].error_message = str(e)
        download_tasks[task_id].progress = 0.0
        download_tasks[task_id].updated_at = datetime.now().isoformat()


async def _try_youtube_subtitle_strategies(url: str, download_dir: Path, browser: Optional[str] = None) -> str:
    """Try multiple YouTube subtitle strategies"""
    strategies = [
        lambda: _try_download_with_different_formats(url, download_dir, browser),
        lambda: _try_download_with_different_langs(url, download_dir, browser),
        lambda: _try_extract_from_metadata(url, download_dir, browser)
    ]
    
    for strategy in strategies:
        try:
            subtitle_path = await strategy()
            if subtitle_path:
                logger.info(f"YouTube fallback subtitle strategy succeeded")
                return subtitle_path
        except Exception as e:
            logger.warning(f"YouTube fallback subtitle strategy failed: {e}")
            continue

    logger.warning("All YouTube subtitle strategies failed")
    return ""


async def _try_download_with_different_formats(url: str, download_dir: Path, browser: Optional[str] = None) -> str:
    """Try downloading subtitles in different formats"""
    import asyncio
    logger.info("Trying different YouTube subtitle formats...")

    formats = ['srt', 'vtt', 'json3']

    for fmt in formats:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': get_subtitle_langs(),
                'subtitlesformat': fmt,
                'outtmpl': str(download_dir / f'subtitle_%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'ignoreconfig': True,
                'config_locations': [],
            }

            if browser:
                ydl_opts['cookiesfrombrowser'] = (browser.lower(),)

            def download_sync(url, ydl_opts):
                with sanitized_yt_env():
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        return ydl.download([url])

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, download_sync, url, ydl_opts)

            # Look for downloaded subtitle files
            subtitle_files = list(download_dir.glob(f"*.{fmt}"))
            if subtitle_files:
                subtitle_path = str(subtitle_files[0])

                # Convert VTT to SRT
                if fmt == 'vtt':
                    srt_path = subtitle_path.replace('.vtt', '.srt')
                    await _convert_vtt_to_srt(subtitle_path, srt_path)
                    return srt_path

                return subtitle_path

        except Exception as e:
            logger.debug(f"Format {fmt} failed: {e}")
            continue

    return ""


async def _try_download_with_different_langs(url: str, download_dir: Path, browser: Optional[str] = None) -> str:
    """Try downloading subtitles in different languages"""
    import asyncio
    logger.info("Trying different YouTube subtitle languages...")

    lang_combinations = [
        ['en', 'en-US'],      # English
        ['zh-Hans', 'zh'],    # Chinese
        ['ja', 'ja-JP'],      # Japanese
        ['ko', 'ko-KR'],      # Korean
        ['auto']              # auto-detect
    ]

    for langs in lang_combinations:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': langs,
                'subtitlesformat': 'srt',
                'outtmpl': str(download_dir / f'lang_%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'ignoreconfig': True,
                'config_locations': [],
            }

            if browser:
                ydl_opts['cookiesfrombrowser'] = (browser.lower(),)

            def download_sync(url, ydl_opts):
                with sanitized_yt_env():
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        return ydl.download([url])

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, download_sync, url, ydl_opts)

            # Look for downloaded subtitle files
            subtitle_files = list(download_dir.glob("*.srt"))
            if subtitle_files:
                return str(subtitle_files[0])

        except Exception as e:
            logger.debug(f"Languages {langs} failed: {e}")
            continue

    return ""


async def _try_extract_from_metadata(url: str, download_dir: Path, browser: Optional[str] = None) -> str:
    """Try extracting subtitle info from video metadata"""
    import asyncio
    logger.info("Trying to extract subtitle info from YouTube metadata...")

    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'ignoreconfig': True,
            'config_locations': [],
        }

        if browser:
            ydl_opts['cookiesfrombrowser'] = (browser.lower(),)

        def extract_info_sync(url, ydl_opts):
            with sanitized_yt_env():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    return ydl.extract_info(url, download=False)

        loop = asyncio.get_event_loop()
        info_dict = await loop.run_in_executor(None, extract_info_sync, url, ydl_opts)

        # Check for subtitle info
        subtitles = info_dict.get('subtitles', {})
        auto_subtitles = info_dict.get('automatic_captions', {})

        if subtitles or auto_subtitles:
            logger.info(f"Found YouTube subtitle info: {list(subtitles.keys()) + list(auto_subtitles.keys())}")
            # Further subtitle handling could go here; empty for now
            return ""

        return ""

    except Exception as e:
        logger.debug(f"Failed to extract YouTube metadata: {e}")
        return ""


async def _convert_vtt_to_srt(vtt_path: str, srt_path: str):
    """Convert a VTT subtitle file to SRT"""
    try:
        with open(vtt_path, 'r', encoding='utf-8') as vtt_file:
            vtt_content = vtt_file.read()

        # Simple VTT-to-SRT conversion
        lines = vtt_content.split('\n')
        srt_lines = []
        subtitle_count = 1

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Skip VTT headers
            if line.startswith('WEBVTT') or line.startswith('NOTE') or not line:
                i += 1
                continue

            # Find timestamp lines
            if '-->' in line:
                # Convert time format (VTT uses dots, SRT uses commas)
                time_line = line.replace('.', ',')
                srt_lines.append(str(subtitle_count))
                srt_lines.append(time_line)

                # Collect subtitle text
                i += 1
                subtitle_text = []
                while i < len(lines) and lines[i].strip():
                    subtitle_text.append(lines[i].strip())
                    i += 1

                srt_lines.extend(subtitle_text)
                srt_lines.append('')  # blank separator
                subtitle_count += 1

            i += 1

        # Write the SRT file
        with open(srt_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write('\n'.join(srt_lines))

        logger.info(f"VTT to SRT conversion succeeded: {vtt_path} -> {srt_path}")

    except Exception as e:
        logger.error(f"VTT to SRT conversion failed: {e}")
        raise
