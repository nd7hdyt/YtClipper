"""
Pipeline adapter
Coordinates the 6-step pipeline and exposes a unified interface
"""

import logging
import asyncio
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..models.project import Project
from ..models.task import Task, TaskStatus
from ..core.shared_config import config_manager, get_prompt_files
from ..pipeline.step1_outline import run_step1_outline
from ..pipeline.step2_timeline import run_step2_timeline
from ..pipeline.step3_scoring import run_step3_scoring
from ..pipeline.step4_title import run_step4_title
from ..pipeline.step5_clustering import run_step5_clustering
from ..pipeline.step6_video import run_step6_video

logger = logging.getLogger(__name__)

class PipelinePathManager:
    """Small compatibility path manager used by older tests and callers."""

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.raw_dir = self.project_dir / "raw"
        self.metadata_dir = self.project_dir / "metadata"
        self.output_dir = self.project_dir / "output"
        self.clips_dir = self.output_dir / "clips"
        self.collections_dir = self.output_dir / "collections"

    def ensure_directories(self):
        for directory in (
            self.raw_dir,
            self.metadata_dir,
            self.output_dir,
            self.clips_dir,
            self.collections_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)

    def get_srt_path(self) -> Path:
        input_srt = self.raw_dir / "input.srt"
        if input_srt.exists():
            return input_srt
        srt_files = sorted(self.raw_dir.glob("*.srt"))
        return srt_files[0] if srt_files else input_srt

    def get_video_path(self) -> Path:
        return self.raw_dir / "input.mp4"

    def get_step_output_path(self, step_name: str) -> Path:
        output_names = {
            "step1_outline": "step1_outline.json",
            "step2_timeline": "step2_timeline.json",
            "step3_scoring": "step3_high_score_clips.json",
            "step4_title": "step4_titles.json",
            "step5_clustering": "step5_collections.json",
            "step6_video": "step6_video_output.json",
        }
        return self.metadata_dir / output_names.get(step_name, f"{step_name}.json")

class PipelineAdapter:
    """Pipeline adapter"""
    
    def __init__(self, project_id: str, task_id: Optional[str] = None, db: Optional[Session] = None, progress_callback: Optional[Callable] = None):
        self.project_id = project_id
        self.task_id = task_id or "compat_task"
        self.db = db or SessionLocal()
        self.progress_callback = progress_callback
        self.compat_mode = task_id is None or db is None
        
        # Fetch the project config
        self.config = config_manager.get_processing_config()
        self.path_config = config_manager.get_path_config()
        
        # Project paths
        if self.compat_mode and Path(project_id).exists():
            self.path_manager = PipelinePathManager(Path(project_id))
            self.path_manager.ensure_directories()
            self.project_paths = {
                "project_base": self.path_manager.project_dir,
                "input_dir": self.path_manager.raw_dir,
                "metadata_dir": self.path_manager.metadata_dir,
                "output_dir": self.path_manager.output_dir,
                "clips_dir": self.path_manager.clips_dir,
                "collections_dir": self.path_manager.collections_dir,
            }
        else:
            self.project_paths = config_manager.get_project_paths(project_id)
            self.path_manager = PipelinePathManager(self.project_paths["project_base"])
            config_manager.ensure_project_directories(project_id)
        
        # Make sure the project directories exist
        self.path_manager.ensure_directories()
        
        # Step results
        self.step_results = {}
        
    def validate_pipeline_prerequisites(self) -> List[str]:
        """
        Validate pipeline prerequisites
        
        Returns:
            list of errors; empty means validation passed
        """
        errors = []
        
        # Check the API key
        api_config = config_manager.get_api_config()
        if not api_config.api_key and not os.getenv("DASHSCOPE_API_KEY"):
            errors.append("Missing API key configuration")
        
        # Check the project directory
        if not self.project_paths["project_base"].exists():
            errors.append(f"Project directory not found: {self.project_paths['project_base']}")
        
        # Check the input files
        input_video = self.project_paths["input_dir"] / "input.mp4"
        input_srt = self.path_manager.get_srt_path() if self.compat_mode else self.project_paths["input_dir"] / "input.srt"
        
        if not self.compat_mode and not input_video.exists():
            errors.append(f"Video file not found: {input_video}")
        
        if not input_srt.exists():
            errors.append(f"SRT file not found: {input_srt}")
        
        # Check the prompt files
        if not self.compat_mode:
            prompt_files = get_prompt_files()
            for key, path in prompt_files.items():
                if not path.exists():
                    errors.append(f"Prompt file not found: {path}")
        
        return errors

    def get_step_output_path(self, step_name: str) -> Path:
        return self.path_manager.get_step_output_path(step_name)

    def prepare_step_environment(self, step_name: str):
        self.path_manager.ensure_directories()
        return self.get_step_output_path(step_name)

    def cleanup_intermediate_files(self, step_name: str):
        output_path = self.get_step_output_path(step_name)
        output_path.unlink(missing_ok=True)

    def get_step_result(self, step_name: str) -> Any:
        output_path = self.get_step_output_path(step_name)
        if not output_path.exists():
            return None
        with open(output_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def adapt_step(self, step_name: str, **kwargs) -> Dict[str, Any]:
        adapters = {
            "step1_outline": self.adapt_step1_outline,
            "step2_timeline": self.adapt_step2_timeline,
            "step3_scoring": self.adapt_step3_scoring,
            "step4_title": self.adapt_step4_title,
            "step5_clustering": self.adapt_step5_clustering,
            "step6_video": self.adapt_step6_video,
        }
        if step_name not in adapters:
            raise ValueError(f"Unknown step: {step_name}")
        return adapters[step_name](**kwargs)

    def execute_step(self, step_name: str, **kwargs) -> Dict[str, Any]:
        return {"status": "completed", "params": self.adapt_step(step_name, **kwargs)}

    def adapt_step1_outline(self, srt_path: Optional[Path] = None, **kwargs) -> Dict[str, Any]:
        srt_path = Path(srt_path or self.path_manager.get_srt_path())
        if not srt_path.exists():
            raise FileNotFoundError(f"SRT file not found: {srt_path}")
        return {
            "srt_path": srt_path,
            "metadata_dir": self.path_manager.metadata_dir,
            "output_path": self.path_manager.get_step_output_path("step1_outline"),
        }

    def adapt_step2_timeline(self, **kwargs) -> Dict[str, Any]:
        return {
            "outline_path": self.path_manager.get_step_output_path("step1_outline"),
            "metadata_dir": self.path_manager.metadata_dir,
            "output_path": self.path_manager.get_step_output_path("step2_timeline"),
        }

    def adapt_step3_scoring(self, **kwargs) -> Dict[str, Any]:
        return {
            "timeline_path": self.path_manager.get_step_output_path("step2_timeline"),
            "metadata_dir": self.path_manager.metadata_dir,
            "output_path": self.path_manager.get_step_output_path("step3_scoring"),
        }

    def adapt_step4_title(self, **kwargs) -> Dict[str, Any]:
        return {
            "high_score_clips_path": self.path_manager.get_step_output_path("step3_scoring"),
            "metadata_dir": self.path_manager.metadata_dir,
            "output_path": self.path_manager.get_step_output_path("step4_title"),
        }

    def adapt_step5_clustering(self, **kwargs) -> Dict[str, Any]:
        return {
            "clips_with_titles_path": self.path_manager.get_step_output_path("step4_title"),
            "metadata_dir": self.path_manager.metadata_dir,
            "output_path": self.path_manager.get_step_output_path("step5_clustering"),
        }

    def adapt_step6_video(self, **kwargs) -> Dict[str, Any]:
        return {
            "clips_with_titles_path": self.path_manager.get_step_output_path("step4_title"),
            "collections_path": self.path_manager.get_step_output_path("step5_clustering"),
            "input_video": self.path_manager.get_video_path(),
            "output_dir": self.path_manager.output_dir,
            "clips_dir": str(self.path_manager.clips_dir),
            "collections_dir": str(self.path_manager.collections_dir),
            "metadata_dir": str(self.path_manager.metadata_dir),
        }
    
    async def process_project(self, input_video_path: str, input_srt_path: str) -> Dict[str, Any]:
        """
        Process the project - async version
        
        Args:
            input_video_path: input video path
            input_srt_path: input subtitle path
            
        Returns:
            processing result
        """
        try:
            logger.info(f"Processing project {self.project_id}")
            
            # Validate prerequisites
            errors = self.validate_pipeline_prerequisites()
            if errors:
                error_msg = "; ".join(errors)
                logger.error(f"Pipeline prerequisite check failed: {error_msg}")
                return {"status": "failed", "message": error_msg}
            
            # Run the 6-step pipeline
            steps = [
                ("step1_outline", "Outline extraction", self._execute_step1),
                ("step2_timeline", "Timeline extraction", self._execute_step2),
                ("step3_scoring", "Highlight scoring", self._execute_step3),
                ("step4_title", "Title generation", self._execute_step4),
                ("step5_clustering", "Topic clustering", self._execute_step5),
                ("step6_video", "Video rendering", self._execute_step6)
            ]
            
            total_steps = len(steps)
            
            for i, (step_name, step_desc, step_func) in enumerate(steps):
                try:
                    logger.info(f"Running step {i+1}/{total_steps}: {step_desc}")
                    
                    # Progress update - step started
                    progress = int((i / total_steps) * 100)
                    await self._update_progress(progress, f"Starting: {step_desc}")
                    
                    # Run the step
                    result = await step_func()
                    
                    if result.get("status") == "failed":
                        error_msg = result.get("message", "Step failed")
                        logger.error(f"Step {step_name} failed: {error_msg}")
                        return {"status": "failed", "message": f"{step_desc} failed: {error_msg}"}
                    
                    # Store the step result
                    self.step_results[step_name] = result
                    logger.info(f"Step {step_name} succeeded")
                    
                    # Progress update - step done
                    progress = int(((i + 1) / total_steps) * 100)
                    await self._update_progress(progress, f"Done: {step_desc}")
                    
                except Exception as e:
                    error_msg = f"Step {step_name} raised: {str(e)}"
                    logger.error(error_msg)
                    return {"status": "failed", "message": error_msg}
            
            # Final progress update
            await self._update_progress(100, "Processing complete")
            
            # Persist results to the database
            await self._save_results_to_database()
            
            logger.info(f"Project {self.project_id} processing complete")
            return {
                "status": "success",
                "message": "Project processing complete",
                "project_id": self.project_id,
                "results": self.step_results
            }
            
        except Exception as e:
            error_msg = f"Project processing failed: {str(e)}"
            logger.error(error_msg)
            return {"status": "failed", "message": error_msg}
    
    def process_project_sync(self, input_video_path: str, input_srt_path: str) -> Dict[str, Any]:
        """
        Process the project - sync version
        
        Args:
            input_video_path: input video path
            input_srt_path: input subtitle path
            
        Returns:
            processing result
        """
        try:
            # Try to get the current event loop
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                # Create a new one if closed
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            # Create a new one if there is none
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            return loop.run_until_complete(self.process_project(input_video_path, input_srt_path))
        finally:
            # Let Celery own the event loop; do not close it here
            pass
    
    async def _execute_step1(self) -> Dict[str, Any]:
        """Run step 1: outline extraction"""
        try:
            input_srt_path = self.project_paths["input_dir"] / "input.srt"
            output_path = self.project_paths["metadata_dir"] / "step1_outlines.json"
            
            # Get the project info to determine the video category
            project = self.db.query(Project).filter(Project.id == self.project_id).first()
            video_category = "default"
            if project and project.project_metadata:
                video_category = project.project_metadata.get("video_category", "default")
            
            # Get the matching prompt files
            prompt_files = get_prompt_files(video_category)
            
            result = run_step1_outline(
                srt_path=input_srt_path,
                metadata_dir=self.project_paths["metadata_dir"],
                output_path=output_path,
                prompt_files=prompt_files
            )
            
            return {"status": "success", "result": result, "output_path": str(output_path)}
            
        except Exception as e:
            logger.error(f"Step 1 failed: {e}")
            return {"status": "failed", "message": str(e)}
    
    async def _execute_step2(self) -> Dict[str, Any]:
        """Run step 2: timeline extraction"""
        try:
            outline_path = self.project_paths["metadata_dir"] / "step1_outlines.json"
            output_path = self.project_paths["metadata_dir"] / "step2_timeline.json"
            
            if not outline_path.exists():
                return {"status": "failed", "message": "Step 1 result file not found"}
            
            # Get the project info to determine the video category
            project = self.db.query(Project).filter(Project.id == self.project_id).first()
            video_category = "default"
            if project and project.project_metadata:
                video_category = project.project_metadata.get("video_category", "default")
            
            # Get the matching prompt files
            prompt_files = get_prompt_files(video_category)
            
            result = run_step2_timeline(
                outline_path=outline_path,
                metadata_dir=self.project_paths["metadata_dir"],
                output_path=output_path,
                prompt_files=prompt_files
            )
            
            return {"status": "success", "result": result, "output_path": str(output_path)}
            
        except Exception as e:
            logger.error(f"Step 2 failed: {e}")
            return {"status": "failed", "message": str(e)}
    
    async def _execute_step3(self) -> Dict[str, Any]:
        """Run step 3: highlight scoring"""
        try:
            timeline_path = self.project_paths["metadata_dir"] / "step2_timeline.json"
            output_path = self.project_paths["metadata_dir"] / "step3_scoring.json"
            
            if not timeline_path.exists():
                return {"status": "failed", "message": "Step 2 result file not found"}
            
            # Get the project info to determine the video category
            project = self.db.query(Project).filter(Project.id == self.project_id).first()
            video_category = "default"
            if project and project.project_metadata:
                video_category = project.project_metadata.get("video_category", "default")
            
            # Get the matching prompt files
            prompt_files = get_prompt_files(video_category)
            
            result = run_step3_scoring(
                timeline_path=timeline_path,
                metadata_dir=self.project_paths["metadata_dir"],
                output_path=output_path,
                prompt_files=prompt_files
            )
            
            return {"status": "success", "result": result, "output_path": str(output_path)}
            
        except Exception as e:
            logger.error(f"Step 3 failed: {e}")
            return {"status": "failed", "message": str(e)}
    
    async def _execute_step4(self) -> Dict[str, Any]:
        """Run step 4: title generation"""
        try:
            scoring_path = self.project_paths["metadata_dir"] / "step3_scoring.json"
            output_path = self.project_paths["metadata_dir"] / "step4_titles.json"
            
            if not scoring_path.exists():
                return {"status": "failed", "message": "Step 3 result file not found"}
            
            # Get the project info to determine the video category
            project = self.db.query(Project).filter(Project.id == self.project_id).first()
            video_category = "default"
            if project and project.project_metadata:
                video_category = project.project_metadata.get("video_category", "default")
            
            # Get the matching prompt files
            prompt_files = get_prompt_files(video_category)
            
            result = run_step4_title(
                high_score_clips_path=scoring_path,
                metadata_dir=self.project_paths["metadata_dir"],
                output_path=output_path,
                prompt_files=prompt_files
            )
            
            return {"status": "success", "result": result, "output_path": str(output_path)}
            
        except Exception as e:
            logger.error(f"Step 4 failed: {e}")
            return {"status": "failed", "message": str(e)}
    
    async def _execute_step5(self) -> Dict[str, Any]:
        """Run step 5: topic clustering"""
        try:
            titles_path = self.project_paths["metadata_dir"] / "step4_titles.json"
            output_path = self.project_paths["metadata_dir"] / "step5_collections.json"
            
            if not titles_path.exists():
                return {"status": "failed", "message": "Step 4 result file not found"}
            
            # Get the project info to determine the video category
            project = self.db.query(Project).filter(Project.id == self.project_id).first()
            video_category = "default"
            if project and project.project_metadata:
                video_category = project.project_metadata.get("video_category", "default")
            
            # Get the matching prompt files
            prompt_files = get_prompt_files(video_category)
            
            result = run_step5_clustering(
                clips_with_titles_path=titles_path,
                output_path=output_path,
                metadata_dir=self.project_paths["metadata_dir"],
                prompt_files=prompt_files
            )
            
            return {"status": "success", "result": result, "output_path": str(output_path)}
            
        except Exception as e:
            logger.error(f"Step 5 failed: {e}")
            return {"status": "failed", "message": str(e)}
    
    async def _execute_step6(self) -> Dict[str, Any]:
        """Run step 6: video rendering"""
        try:
            titles_path = self.project_paths["metadata_dir"] / "step4_titles.json"
            collections_path = self.project_paths["metadata_dir"] / "step5_collections.json"
            input_video_path = self.project_paths["input_dir"] / "input.mp4"
            
            if not titles_path.exists():
                return {"status": "failed", "message": "Step 4 result file not found"}
            if not collections_path.exists():
                return {"status": "failed", "message": "Step 5 result file not found"}
            if not input_video_path.exists():
                return {"status": "failed", "message": "Input video file not found"}
            
            result = run_step6_video(
                clips_with_titles_path=titles_path,
                collections_path=collections_path,
                input_video=input_video_path,
                output_dir=self.project_paths["output_dir"],
                clips_dir=str(self.project_paths["clips_dir"]),
                collections_dir=str(self.project_paths["collections_dir"]),
                metadata_dir=self.project_paths["metadata_dir"]
            )
            
            return {"status": "success", "result": result}
            
        except Exception as e:
            logger.error(f"Step 6 failed: {e}")
            return {"status": "failed", "message": str(e)}
    
    async def _update_progress(self, progress: int, message: str):
        """Update progress"""
        try:
            # Update the task progress in the database
            task = self.db.query(Task).filter(Task.id == self.task_id).first()
            if task:
                task.progress = progress
                task.current_step = message
                task.updated_at = datetime.utcnow()
                self.db.commit()
                logger.info(f"Task {self.task_id} progress updated: {progress}% - {message}")
            
            # Invoke the progress callback
            if self.progress_callback:
                try:
                    # Check whether the callback is async
                    import asyncio
                    if asyncio.iscoroutinefunction(self.progress_callback):
                        await self.progress_callback(self.project_id, progress, message)
                    else:
                        # Sync callback - note the argument order: project_id, progress, message
                        self.progress_callback(self.project_id, progress, message)
                except Exception as callback_error:
                    logger.error(f"Progress callback failed: {callback_error}")
                
        except Exception as e:
            logger.error(f"Progress update failed: {e}")
            import traceback
            logger.error(f"Error details: {traceback.format_exc()}")
    
    async def _save_results_to_database(self):
        """Persist results to the database"""
        try:
            # Update the project status
            project = self.db.query(Project).filter(Project.id == self.project_id).first()
            if project:
                project.status = "completed"
                self.db.commit()
                logger.info(f"Project {self.project_id} marked completed")
            
            # Sync clip and collection data to the database
            await self._sync_clips_and_collections_to_database()
                
        except Exception as e:
            logger.error(f"Failed to save results to database: {e}")
    
    async def _sync_clips_and_collections_to_database(self):
        """Sync clip and collection data to the database"""
        try:
            from ..models.clip import Clip, ClipStatus
            from ..models.collection import Collection, CollectionStatus
            from datetime import datetime
            
            # Clear existing data
            self.db.query(Clip).filter(Clip.project_id == self.project_id).delete()
            self.db.query(Collection).filter(Collection.project_id == self.project_id).delete()
            
            # Sync clip data
            clips_metadata_file = self.project_paths["metadata_dir"] / "clips_metadata.json"
            if clips_metadata_file.exists():
                with open(clips_metadata_file, 'r', encoding='utf-8') as f:
                    clips_data = json.load(f)
                
                clips_count = 0
                for clip_data in clips_data:
                    try:
                        # Build the clip file path
                        clip_filename = f"{clip_data['id']}_{clip_data['generated_title']}.mp4"
                        clip_path = self.project_paths["clips_dir"] / clip_filename
                        
                        if not clip_path.exists():
                            continue
                        
                        # Compute the duration
                        start_time_str = clip_data.get('start_time', '00:00:00,000')
                        end_time_str = clip_data.get('end_time', '00:00:00,000')
                        start_seconds = self._parse_time(start_time_str)
                        end_seconds = self._parse_time(end_time_str)
                        duration = end_seconds - start_seconds
                        
                        # Create the clip record
                        clip = Clip(
                            id=f"{self.project_id}_{clip_data['id']}",
                            project_id=self.project_id,
                            title=clip_data['generated_title'],
                            description=clip_data.get('recommend_reason', ''),
                            start_time=int(start_seconds),
                            end_time=int(end_seconds),
                            duration=int(duration),
                            video_path=str(clip_path),
                            score=clip_data.get('final_score', 0),
                            recommendation_reason=clip_data.get('recommend_reason', ''),
                            status=ClipStatus.COMPLETED,
                            clip_metadata={
                                'outline': clip_data.get('outline', ''),
                                'content': clip_data.get('content', []),
                                'chunk_index': clip_data.get('chunk_index', 0)
                            },
                            created_at=datetime.utcnow(),
                            updated_at=datetime.utcnow()
                        )
                        
                        self.db.add(clip)
                        clips_count += 1
                        
                    except Exception as e:
                        logger.error(f"Failed to sync clip: {e}")
                        continue
                
                logger.info(f"Synced {clips_count} clips to the database")
            
            # Sync collection data
            collections_metadata_file = self.project_paths["metadata_dir"] / "collections_metadata.json"
            if collections_metadata_file.exists():
                with open(collections_metadata_file, 'r', encoding='utf-8') as f:
                    collections_data = json.load(f)
                
                collections_count = 0
                for collection_data in collections_data:
                    try:
                        # Build the collection file path
                        collection_filename = f"{collection_data['collection_title']}.mp4"
                        collection_path = self.project_paths["collections_dir"] / collection_filename
                        
                        if not collection_path.exists():
                            continue
                        
                        # Map the simplified clip_ids to full clip IDs
                        simplified_clip_ids = collection_data.get('clip_ids', [])
                        full_clip_ids = []
                        for clip_id in simplified_clip_ids:
                            full_clip_id = f"{self.project_id}_{clip_id}"
                            full_clip_ids.append(full_clip_id)
                        
                        # Create the collection record
                        # NOTE: theme/tags stay Chinese — they are categorical values
                        # the frontend filters on, not free text.
                        collection = Collection(
                            id=f"{self.project_id}_collection_{collection_data['id']}",
                            project_id=self.project_id,
                            name=collection_data['collection_title'],
                            description=collection_data.get('collection_summary', ''),
                            theme="EN",
                            status=CollectionStatus.COMPLETED,
                            tags=["EN", "EN", "EN"],
                            collection_metadata={
                                'clip_ids': full_clip_ids,  # full clip IDs
                                'simplified_clip_ids': simplified_clip_ids,  # keep the original short IDs
                                'generated_by': 'pipeline'
                            },
                            created_at=datetime.utcnow(),
                            updated_at=datetime.utcnow()
                        )
                        
                        self.db.add(collection)
                        collections_count += 1
                        
                    except Exception as e:
                        logger.error(f"Failed to sync collection: {e}")
                        continue
                
                logger.info(f"Synced {collections_count} collections to the database")
            
            # Commit the transaction
            self.db.commit()
            logger.info(f"Project {self.project_id} data sync complete")
            
        except Exception as e:
            logger.error(f"Failed to sync data to database: {e}")
            self.db.rollback()
    
    def _parse_time(self, time_str: str) -> float:
        """Parse a time string into seconds"""
        try:
            if ',' in time_str:
                time_str = time_str.replace(',', '.')
            
            parts = time_str.split(':')
            if len(parts) == 3:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = float(parts[2])
                return hours * 3600 + minutes * 60 + seconds
            else:
                return 0.0
        except:
            return 0.0

def create_pipeline_adapter(db: Session, task_id: str, project_id: str, progress_callback: Optional[Callable] = None) -> PipelineAdapter:
    """
    Create a pipeline adapter instance
    
    Args:
        db: database session
        task_id: task ID
        project_id: project ID
        progress_callback: progress callback
        
    Returns:
        pipeline adapter instance
    """
    return PipelineAdapter(project_id, task_id, db, progress_callback)

def create_pipeline_adapter_sync(db: Session, task_id: str, project_id: str) -> PipelineAdapter:
    """
    Create a pipeline adapter instance (sync version)
    
    Args:
        db: database session
        task_id: task ID
        project_id: project ID
        
    Returns:
        pipeline adapter instance
    """
    return PipelineAdapter(project_id, task_id, db)
