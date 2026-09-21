"""
Simplified pipeline adapter - integrates the new progress system
"""

import logging
import os
from typing import Dict, Any, Optional, Callable
from pathlib import Path

from backend.services.simple_progress import emit_progress, clear_progress
from backend.pipeline.failures import (
    PipelineFailure, HINT_CHECK_LLM, HINT_SUBTITLE, HINT_LOWER_THRESHOLD, HINT_CHECK_FFMPEG,
)
from backend.pipeline.step1_outline import run_step1_outline
from backend.pipeline.step2_timeline import run_step2_timeline
from backend.pipeline.step3_scoring import run_step3_scoring
from backend.pipeline.step4_title import run_step4_title
from backend.pipeline.step5_clustering import run_step5_clustering
from backend.pipeline.step6_video import run_step6_video

logger = logging.getLogger(__name__)


class SimplePipelineAdapter:
    """Simplified pipeline adapter with a fixed-stage progress system"""
    
    def __init__(self, project_id: str, task_id: str):
        self.project_id = project_id
        self.task_id = task_id

    def _prompt_files(self, project_dir: Path):
        """Pick prompt/<category>/. The desktop client never passed a category before,
        so the category directories were effectively unused."""
        from backend.core.shared_config import get_prompt_files
        import json

        category = "default"
        meta_path = project_dir / "project.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                category = meta.get("video_category") or "default"
            except Exception:  # noqa: BLE001
                pass
        if category == "default":
            try:
                from backend.core.database import SessionLocal
                from backend.models.project import Project
                db = SessionLocal()
                try:
                    row = db.query(Project).filter(Project.id == self.project_id).first()
                    if row is not None and row.project_type is not None:
                        category = row.project_type.value if hasattr(row.project_type, "value") else str(row.project_type)
                finally:
                    db.close()
            except Exception:  # noqa: BLE001
                pass
        logger.info(f"Using category prompts: {category}")
        return get_prompt_files(category)
        
    async def _generate_subtitle_automatically(self, video_path: str, metadata_dir: Path) -> Path:
        """
        Generate the subtitle file automatically
        
        Args:
            video_path: path to the video file
            metadata_dir: metadata directory
            
        Returns:
            path of the generated SRT file, or None on failure
        """
        try:
            logger.info(f"Auto-generating subtitles for video {video_path}")
            
            # Update progress
            from backend.services.simple_progress import emit_progress
            emit_progress(self.project_id, "SUBTITLE", "Generating subtitles with AI...", subpercent=25)
            
            # Generate subtitles with the local Whisper model
            try:
                from backend.utils.speech_recognizer import generate_subtitle_for_video
                from pathlib import Path
                
                video_file_path = Path(video_path)
                if not video_file_path.exists():
                    logger.error(f"Video file not found: {video_path}")
                    return None
                
                logger.info("Trying to generate subtitles with the local Whisper model")
                output_path = metadata_dir / f"{video_file_path.stem}.srt"
                srt_path = generate_subtitle_for_video(
                    video_file_path,
                    output_path=output_path,
                    method="whisper_local",
                    model="base",
                    language="auto"
                )
                
                if srt_path and srt_path.exists():
                    logger.info(f"Whisper subtitle generation succeeded: {srt_path}")
                    emit_progress(self.project_id, "SUBTITLE", "AI subtitle generation complete", subpercent=40)
                    return srt_path
                else:
                    logger.warning("Whisper subtitle generation failed")
                    
            except Exception as e:
                logger.warning(f"Whisper subtitle generation failed: {e}")
            
            logger.error("Whisper subtitle generation failed")
            return None
            
        except Exception as e:
            logger.error(f"Error during automatic subtitle generation: {e}")
            return None
        
    @staticmethod
    def _preflight_llm() -> None:
        """Confirm a provider is available before running any LLM step; otherwise step1
        would log an error per chunk and then hand off an empty outline.
        AUTOCLIP_LLM_CACHE_DIR replay mode needs no real provider (backend/eval)."""
        if os.getenv("AUTOCLIP_LLM_CACHE_DIR"):
            return
        from backend.core.llm_manager import get_llm_manager
        info = get_llm_manager().get_current_provider_info()
        if info.get("available"):
            return
        name = info.get("display_name") or info.get("provider") or "none selected"
        model = info.get("model") or "-"
        raise PipelineFailure(
            "ANALYZE",
            f"No usable LLM provider (currently selected: {name} · {model}); missing API key or local server address.",
            HINT_CHECK_LLM,
        )

    async def process_project_sync(self, input_video_path: str, input_srt_path: str) -> Dict[str, Any]:
        """
        Process the project synchronously - with the simplified progress system
        
        Args:
            input_video_path: input video path
            input_srt_path: input SRT path
            
        Returns:
            processing result
        """
        logger.info(f"Processing project: {self.project_id}")
        
        try:
            # Clear previous progress data
            clear_progress(self.project_id)
            
            # Create the required directory layout - using the correct paths
            from backend.core.path_utils import get_project_directory
            project_dir = get_project_directory(self.project_id)
            metadata_dir = project_dir / "metadata"
            output_dir = project_dir / "output"
            metadata_dir.mkdir(parents=True, exist_ok=True)
            output_dir.mkdir(parents=True, exist_ok=True)
            # Project-local output subdirectories
            clips_output_dir = output_dir / "clips"
            collections_output_dir = output_dir / "collections"
            clips_output_dir.mkdir(parents=True, exist_ok=True)
            collections_output_dir.mkdir(parents=True, exist_ok=True)
            prompt_files = self._prompt_files(project_dir)
            
            # Stage 1: ingest. Confirm the LLM is usable first, otherwise every later
            # step runs for nothing
            emit_progress(self.project_id, "INGEST", "Ingest complete")
            self._preflight_llm()
            
            # Stage 2: subtitle processing
            emit_progress(self.project_id, "SUBTITLE", "Starting subtitle processing")
            
            if input_srt_path and Path(input_srt_path).exists():
                logger.info(f"Using existing SRT file: {input_srt_path}")
                srt_path = Path(input_srt_path)
            else:
                logger.warning("No SRT file, trying to auto-generate subtitles")
                srt_path = await self._generate_subtitle_automatically(input_video_path, metadata_dir)
                if not (srt_path and srt_path.exists()):
                    # This used to write an empty outline and "succeed" all the way
                    # through, leaving the user with Completed · 0 clips
                    raise PipelineFailure(
                        "SUBTITLE",
                        "No subtitles to analyze: the video has no embedded subtitles, and local transcription produced nothing.",
                        HINT_SUBTITLE,
                    )
                logger.info(f"Auto-generated subtitles: {srt_path}")

            # Step 1: outline extraction (empty subtitles / all-model-failed /
            # unparseable output raise PipelineFailure from step1 itself)
            logger.info("Running Step 1: outline extraction")
            outlines = run_step1_outline(srt_path, metadata_dir=metadata_dir, prompt_files=prompt_files)
            emit_progress(self.project_id, "SUBTITLE", "Subtitle processing complete", subpercent=50)
            
            # Stage 3: content analysis
            emit_progress(self.project_id, "ANALYZE", "Starting content analysis")
            
            # Step 2: timeline extraction
            logger.info("Running Step 2: timeline extraction")
            timeline_data = run_step2_timeline(
                metadata_dir / "step1_outline.json",
                metadata_dir=metadata_dir,
                prompt_files=prompt_files,
            )
            if not timeline_data:
                raise PipelineFailure(
                    "ANALYZE",
                    f"Timeline extraction came back empty: none of the {len(outlines)} topics could be aligned to the subtitle track.",
                    HINT_CHECK_LLM,
                )
            emit_progress(self.project_id, "ANALYZE", "Timeline extraction complete", subpercent=50)
            
            # Step 3: highlight scoring
            logger.info("Running Step 3: highlight scoring")
            scored_clips = run_step3_scoring(
                metadata_dir / "step2_timeline.json",
                metadata_dir=metadata_dir,
                prompt_files=prompt_files,
            )
            if not scored_clips:
                from backend.pipeline.step3_scoring import resolve_min_score_threshold
                raise PipelineFailure(
                    "ANALYZE",
                    f"No clips passed score filtering ({len(timeline_data)} candidates, threshold {resolve_min_score_threshold()}).",
                    HINT_LOWER_THRESHOLD,
                )
            emit_progress(self.project_id, "ANALYZE", "Content analysis complete", subpercent=100)
            
            # Stage 4: highlight locating
            emit_progress(self.project_id, "HIGHLIGHT", "Starting highlight locating")
            
            # Step 4: title generation
            logger.info("Running Step 4: title generation")
            titled_clips = run_step4_title(
                metadata_dir / "step3_high_score_clips.json",
                metadata_dir=str(metadata_dir),
                prompt_files=prompt_files,
            )
            emit_progress(self.project_id, "HIGHLIGHT", "Title generation complete", subpercent=40)
            
            # Step 5: topic clustering
            logger.info("Running Step 5: topic clustering")
            collections = run_step5_clustering(
                metadata_dir / "step4_titles.json",
                metadata_dir=str(metadata_dir),
                prompt_files=prompt_files,
            )
            emit_progress(self.project_id, "HIGHLIGHT", "Highlight locating complete", subpercent=100)
            
            # Stage 5: video export
            emit_progress(self.project_id, "EXPORT", "Starting video export")
            
            # Step 6: video cutting
            logger.info("Running Step 6: video cutting")
            video_result = run_step6_video(
                metadata_dir / "step4_titles.json",
                metadata_dir / "step5_collections.json",
                input_video_path,
                output_dir=output_dir,
                clips_dir=str(clips_output_dir),
                collections_dir=str(collections_output_dir),
                metadata_dir=str(metadata_dir)
            )
            if titled_clips and not video_result.get("clips_generated"):
                raise PipelineFailure(
                    "EXPORT",
                    f"Video cutting produced no files ({len(titled_clips)} clips to cut).",
                    HINT_CHECK_FFMPEG,
                )
            emit_progress(self.project_id, "EXPORT", "Video export complete", subpercent=100)
            
            # Stage 6: done
            emit_progress(self.project_id, "DONE", "Processing complete")
            
            # Auto-sync data to the database
            try:
                from backend.services.data_sync_service import DataSyncService
                from backend.core.database import SessionLocal
                
                db = SessionLocal()
                try:
                    sync_service = DataSyncService(db)
                    sync_result = sync_service.sync_project_from_filesystem(self.project_id, project_dir)
                    if sync_result.get("success"):
                        logger.info(f"Project {self.project_id} data sync succeeded: {sync_result}")
                    else:
                        logger.error(f"Project {self.project_id} data sync failed: {sync_result}")
                finally:
                    db.close()
            except Exception as e:
                logger.error(f"Data sync failed: {e}")
            
            logger.info(f"Project processing complete: {self.project_id}")
            return {
                "status": "succeeded",
                "project_id": self.project_id,
                "task_id": self.task_id,
                "result": {
                    "outlines": outlines,
                    "timeline": timeline_data,
                    "scored_clips": scored_clips,
                    "titled_clips": titled_clips,
                    "collections": collections,
                    "video_result": video_result
                }
            }
            
        except PipelineFailure as e:
            # Explicit failure: carries a stage and next-step hint, shown directly by
            # the frontend failure state / in-app feedback
            error_msg = e.user_message()
            logger.error(f"Pipeline failed at stage {e.stage}: {error_msg}")
            emit_progress(self.project_id, e.stage, f"Processing failed: {error_msg}")
            return {
                "status": "failed",
                "project_id": self.project_id,
                "task_id": self.task_id,
                "stage": e.stage,
                "error": error_msg,
                "message": error_msg,
            }
        except Exception as e:
            error_msg = f"Pipeline processing failed: {str(e)}"
            logger.exception(error_msg)
            
            # Send the failure state
            emit_progress(self.project_id, "DONE", f"Processing failed: {error_msg}")
            
            return {
                "status": "failed",
                "project_id": self.project_id,
                "task_id": self.task_id,
                "error": error_msg,
                "message": error_msg,
            }


def create_simple_pipeline_adapter(project_id: str, task_id: str) -> SimplePipelineAdapter:
    """Create a simplified pipeline adapter instance"""
    return SimplePipelineAdapter(project_id, task_id)
