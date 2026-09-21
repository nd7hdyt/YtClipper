import logging
from pathlib import Path
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ...utils.subtitle_processor import SubtitleProcessor
from ...utils.video_editor import VideoEditor
from ...core.path_utils import get_data_directory, get_projects_directory
from ...core.database import get_db
from ...services.project_service import ProjectService
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
router = APIRouter()

# translatedAndtranslatedmodel
class SubtitleEditRequest(BaseModel):
    project_id: str
    clip_id: str
    deleted_segments: List[str]

class SubtitleEditResponse(BaseModel):
    success: bool
    message: str
    edited_video_path: Optional[str] = None
    deleted_duration: Optional[float] = None
    final_duration: Optional[float] = None

class SubtitleDataResponse(BaseModel):
    segments: List[Dict]
    total_duration: float
    word_count: int
    segment_count: int

class EditPreviewRequest(BaseModel):
    project_id: str
    clip_id: str
    deleted_segments: List[str]

# dependenciestranslated
def get_subtitle_processor() -> SubtitleProcessor:
    return SubtitleProcessor()

def get_video_editor() -> VideoEditor:
    # Subtitle Editingtranslatedusetranslatedpathtranslated（translated）
    from ...core.shared_config import CLIPS_DIR, COLLECTIONS_DIR
    return VideoEditor(clips_dir=str(CLIPS_DIR), collections_dir=str(COLLECTIONS_DIR))

def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """Dependency to get project service."""
    return ProjectService(db)

@router.get("/{project_id}/clips/{clip_id}/subtitles")
async def get_clip_subtitles(
    project_id: str,
    clip_id: str,
    subtitle_processor: SubtitleProcessor = Depends(get_subtitle_processor),
    project_service: ProjectService = Depends(get_project_service)
):
    """fetchtranslated'stranslatedsubtitlestranslated"""
    try:
        # fetchprojectinfo
        project = project_service.get(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        
        # fetchtranslatedinfo
        from ...models.clip import Clip
        clip = project_service.db.query(Clip).filter(Clip.id == clip_id, Clip.project_id == project_id).first()
        if not clip:
            raise HTTPException(status_code=404, detail="translatednot found")
        
        # translatedSRTfile
        projects_dir = get_projects_directory()
        project_dir = projects_dir / project_id
        srt_file = project_dir / "raw" / "input.srt"
        
        if not srt_file.exists():
            raise HTTPException(status_code=404, detail="subtitlesfile not found")
        
        # translatedsubtitlestranslated
        subtitle_data = subtitle_processor.parse_srt_to_word_level(srt_file)
        
        # translated'stranslated
        # iftranslatedstart_timeAndend_timeIstranslated（seconds），translateduse
        if isinstance(clip.start_time, int):
            clip_start = clip.start_time
        else:
            clip_start = subtitle_processor._srt_time_to_seconds(
                subtitle_processor._seconds_to_srt_time_object(clip.start_time)
            )
        
        if isinstance(clip.end_time, int):
            clip_end = clip.end_time
        else:
            clip_end = subtitle_processor._srt_time_to_seconds(
                subtitle_processor._seconds_to_srt_time_object(clip.end_time)
            )
        
        # translatedsubtitlestranslated
        clip_subtitles = [
            seg for seg in subtitle_data 
            if seg['startTime'] >= clip_start and seg['endTime'] <= clip_end
        ]
        
        # translated's
        for seg in clip_subtitles:
            seg['startTime'] -= clip_start
            seg['endTime'] -= clip_start
            for word in seg['words']:
                word['startTime'] -= clip_start
                word['endTime'] -= clip_start
        
        # fetchtranslatedinfo
        stats = subtitle_processor.get_subtitle_statistics(clip_subtitles)
        
        return SubtitleDataResponse(
            segments=clip_subtitles,
            total_duration=stats['totalDuration'],
            word_count=stats['wordCount'],
            segment_count=stats['segmentCount']
        )
        
    except Exception as e:
        import traceback
        logger.error(f"fetchsubtitlestranslatedfailed: {e}")
        logger.error(f"errortranslated: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"fetchsubtitlestranslatedfailed: {str(e)}")

@router.post("/{project_id}/clips/{clip_id}/edit")
async def edit_clip_by_subtitles(
    project_id: str,
    clip_id: str,
    request: SubtitleEditRequest,
    subtitle_processor: SubtitleProcessor = Depends(get_subtitle_processor),
    video_editor: VideoEditor = Depends(get_video_editor),
    project_service: ProjectService = Depends(get_project_service)
):
    """Based onsubtitlesdeletetranslatedvideotranslated"""
    try:
        # fetchprojectinfo
        project = project_service.get(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        
        # fetchtranslatedinfo
        from ...models.clip import Clip
        clip = project_service.db.query(Clip).filter(Clip.id == clip_id, Clip.project_id == project_id).first()
        if not clip:
            raise HTTPException(status_code=404, detail="translatednot found")
        
        # fetchtranslatedvideoAndsubtitlesfile path
        projects_dir = get_projects_directory()
        project_dir = projects_dir / project_id
        
        # translatedvideofile
        video_files = list(project_dir.glob("raw/*.mp4"))
        if not video_files:
            raise HTTPException(status_code=404, detail="translatedvideofile not found")
        original_video = video_files[0]
        
        # translatedsubtitlesfile
        srt_file = project_dir / "raw" / "input.srt"
        if not srt_file.exists():
            raise HTTPException(status_code=404, detail="subtitlesfile not found")
        
        # translatedsubtitlestranslated
        subtitle_data = subtitle_processor.parse_srt_to_word_level(srt_file)
        
        # translated'stranslated
        # iftranslatedstart_timeAndend_timeIstranslated（seconds），translateduse
        if isinstance(clip.start_time, int):
            clip_start = clip.start_time
        else:
            clip_start = subtitle_processor._srt_time_to_seconds(
                subtitle_processor._seconds_to_srt_time_object(clip.start_time)
            )
        
        if isinstance(clip.end_time, int):
            clip_end = clip.end_time
        else:
            clip_end = subtitle_processor._srt_time_to_seconds(
                subtitle_processor._seconds_to_srt_time_object(clip.end_time)
            )
        
        clip_subtitles = [
            seg for seg in subtitle_data 
            if seg['startTime'] >= clip_start and seg['endTime'] <= clip_end
        ]
        
        # verifytranslated
        validation = video_editor.validate_edit_operations(
            clip_subtitles, request.deleted_segments
        )
        
        if not validation['valid']:
            raise HTTPException(status_code=400, detail=validation['error'])
        
        # createtranslateddirectory
        output_dir = project_dir / "edited_clips"
        output_dir.mkdir(exist_ok=True)
        
        # translated'svideofiletranslated
        edited_video_name = f"{clip_id}_edited.mp4"
        edited_video_path = output_dir / edited_video_name
        
        # translatedvideotranslated
        edit_result = video_editor.edit_video_by_subtitle_deletion(
            original_video,
            clip_subtitles,
            request.deleted_segments,
            edited_video_path
        )
        
        if not edit_result['success']:
            raise HTTPException(status_code=500, detail=f"videotranslatedfailed: {edit_result['error']}")
        
        # exporttranslated'ssubtitlesfile
        edited_srt_path = output_dir / f"{clip_id}_edited.srt"
        subtitle_processor.export_edited_srt(
            clip_subtitles,
            request.deleted_segments,
            edited_srt_path
        )
        
        return SubtitleEditResponse(
            success=True,
            message="videotranslatedsucceeded",
            edited_video_path=str(edited_video_path),
            deleted_duration=edit_result['totalDeletedDuration'],
            final_duration=edit_result['finalDuration']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"translatedvideotranslatedfailed: {e}")
        raise HTTPException(status_code=500, detail=f"translatedvideotranslatedfailed: {str(e)}")

@router.get("/{project_id}/clips/{clip_id}/edited-video")
async def get_edited_video(
    project_id: str,
    clip_id: str,
    project_service: ProjectService = Depends(get_project_service)
):
    """fetchtranslated'svideofile"""
    try:
        # checkprojectIstranslatedin
        project = await project_service.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        
        # translated'svideofile
        projects_dir = get_projects_directory()
        edited_video_path = projects_dir / project_id / "edited_clips" / f"{clip_id}_edited.mp4"
        
        if not edited_video_path.exists():
            raise HTTPException(status_code=404, detail="translated'svideofile not found")
        
        # returnvideofile
        return FileResponse(
            path=str(edited_video_path),
            media_type="video/mp4",
            filename=f"{clip_id}_edited.mp4"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"fetchtranslated'svideofailed: {e}")
        raise HTTPException(status_code=500, detail=f"fetchtranslated'svideofailed: {str(e)}")

@router.post("/{project_id}/clips/{clip_id}/preview")
async def create_edit_preview(
    project_id: str,
    clip_id: str,
    request: EditPreviewRequest,
    subtitle_processor: SubtitleProcessor = Depends(get_subtitle_processor),
    video_editor: VideoEditor = Depends(get_video_editor),
    project_service: ProjectService = Depends(get_project_service)
):
    """createtranslated"""
    try:
        # fetchprojectinfo
        project = project_service.get(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        
        # fetchtranslatedinfo
        from ...models.clip import Clip
        clip = project_service.db.query(Clip).filter(Clip.id == clip_id, Clip.project_id == project_id).first()
        if not clip:
            raise HTTPException(status_code=404, detail="translatednot found")
        
        # fetchtranslatedvideoAndsubtitlesfile path
        projects_dir = get_projects_directory()
        project_dir = projects_dir / project_id
        
        video_files = list(project_dir.glob("raw/*.mp4"))
        if not video_files:
            raise HTTPException(status_code=404, detail="translatedvideofile not found")
        original_video = video_files[0]
        
        srt_file = project_dir / "raw" / "input.srt"
        if not srt_file.exists():
            raise HTTPException(status_code=404, detail="subtitlesfile not found")
        
        # translatedsubtitlestranslated
        subtitle_data = subtitle_processor.parse_srt_to_word_level(srt_file)
        
        # translated'stranslated
        # iftranslatedstart_timeAndend_timeIstranslated（seconds），translateduse
        if isinstance(clip.start_time, int):
            clip_start = clip.start_time
        else:
            clip_start = subtitle_processor._srt_time_to_seconds(
                subtitle_processor._seconds_to_srt_time_object(clip.start_time)
            )
        
        if isinstance(clip.end_time, int):
            clip_end = clip.end_time
        else:
            clip_end = subtitle_processor._srt_time_to_seconds(
                subtitle_processor._seconds_to_srt_time_object(clip.end_time)
            )
        
        clip_subtitles = [
            seg for seg in subtitle_data 
            if seg['startTime'] >= clip_start and seg['endTime'] <= clip_end
        ]
        
        # createtranslateddirectory
        preview_dir = project_dir / "edit_previews" / clip_id
        preview_dir.mkdir(parents=True, exist_ok=True)
        
        # createtranslated
        preview_files = video_editor.create_preview_clips(
            original_video,
            clip_subtitles,
            request.deleted_segments,
            preview_dir
        )
        
        return {
            "success": True,
            "preview_files": [str(f) for f in preview_files],
            "count": len(preview_files)
        }
        
    except Exception as e:
        logger.error(f"createtranslatedfailed: {e}")
        raise HTTPException(status_code=500, detail=f"createtranslatedfailed: {str(e)}")

@router.get("/{project_id}/clips/{clip_id}/preview/{segment_id}")
async def get_preview_segment(
    project_id: str,
    clip_id: str,
    segment_id: str,
    project_service: ProjectService = Depends(get_project_service)
):
    """fetchtranslatedfile"""
    try:
        # checkprojectIstranslatedin
        project = project_service.get(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="project not found")
        
        # translatedfile
        projects_dir = get_projects_directory()
        preview_file = projects_dir / project_id / "edit_previews" / clip_id / f"preview_{segment_id}.mp4"
        
        if not preview_file.exists():
            raise HTTPException(status_code=404, detail="translatedfile not found")
        
        # returntranslatedfile
        return FileResponse(
            path=str(preview_file),
            media_type="video/mp4",
            filename=f"preview_{segment_id}.mp4"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"fetchtranslatedfilefailed: {e}")
        raise HTTPException(status_code=500, detail=f"fetchtranslatedfilefailed: {str(e)}")
