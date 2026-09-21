"""
projectservice
Providesprojecttranslated'stranslated
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
import shutil
import logging
from pathlib import Path

from ..services.base import BaseService
from ..repositories.project_repository import ProjectRepository
from ..models.project import Project
from ..models.task import Task
from ..models.clip import Clip
from ..models.collection import Collection
from ..schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse, ProjectFilter
from ..schemas.base import PaginationParams, PaginationResponse
from ..schemas.project import ProjectType, ProjectStatus
from ..schemas.task import TaskStatus

logger = logging.getLogger(__name__)


class ProjectService(BaseService[Project, ProjectCreate, ProjectUpdate, ProjectResponse]):
    """Project service with business logic."""
    
    def __init__(self, db: Session):
        repository = ProjectRepository(db)
        super().__init__(repository)
        self.db = db
    
    def create_project(self, project_data: ProjectCreate) -> Project:
        """Create a new project with business logic."""
        # Convert Pydantic schema to dict for repository
        project_dict = project_data.model_dump()
        
        # Map Pydantic fields to ORM fields
        orm_data = {
            "name": project_dict["name"],
            "description": project_dict.get("description"),
            "project_type": project_dict.get("project_type", "default").value if hasattr(project_dict.get("project_type", "default"), 'value') else project_dict.get("project_type", "default"),  # Map project_type to project_type
            "status": "pending",  # defaultstatustranslated pending
            "video_path": project_dict.get("source_file"),  # Map source_file to video_path
            "processing_config": project_dict.get("settings", {}),  # Map settings to processing_config
            "project_metadata": {"source_url": project_dict.get("source_url")}  # Map source_url to metadata
        }
        
        return self.create(**orm_data)
    
    def update_project(self, project_id: str, project_data: ProjectUpdate) -> Optional[Project]:
        """Update a project with business logic."""
        # Filter out None values
        update_data = {k: v for k, v in project_data.model_dump().items() if v is not None}
        if not update_data:
            return self.get(project_id)
        
        # Map schema fields to ORM fields
        orm_data = {}
        for key, value in update_data.items():
            if key == "settings":
                orm_data["processing_config"] = value
            elif key == "processing_config":
                orm_data["processing_config"] = value
            else:
                orm_data[key] = value
        
        return self.update(project_id, **orm_data)
    
    def latest_error_message(self, project, status=None) -> Optional[str]:
        """projectfailedtranslated'serrortranslated：translatedonetranslatedtask's Task.error_message，translated project_metadata.last_error（CLI path）。
        Project translated error_message translated。"""
        status = status if status is not None else getattr(project, 'status', None)
        status_value = getattr(status, "value", status)
        if str(status_value).lower() != "failed":
            return None
        from ..models.task import Task
        project_id = str(getattr(project, 'id', ''))
        task = (
            self.db.query(Task)
            .filter(Task.project_id == project_id, Task.error_message.isnot(None))
            .order_by(Task.created_at.desc())
            .first()
        )
        if task and task.error_message:
            return task.error_message
        meta = getattr(project, 'project_metadata', None) or {}
        return meta.get("last_error") or None

    def get_project_with_stats(self, project_id: str) -> Optional[ProjectResponse]:
        """Get project with statistics."""
        project = self.get(project_id)
        if not project:
            return None
        
        # Get actual statistics from database
        from ..models.clip import Clip
        from ..models.collection import Collection
        from ..models.task import Task
        
        total_clips = self.db.query(Clip).filter(Clip.project_id == project_id).count()
        total_collections = self.db.query(Collection).filter(Collection.project_id == project_id).count()
        total_tasks = self.db.query(Task).filter(Task.project_id == project_id).count()
        
        # Convert to response schema
        return ProjectResponse(
            error_message=self.latest_error_message(project),
            id=str(getattr(project, 'id', '')),
            name=str(getattr(project, 'name', '')),
            description=str(getattr(project, 'description', '')) if getattr(project, 'description', None) is not None else None,
            project_type=ProjectType(getattr(project, 'project_type').value) if hasattr(project, 'project_type') and getattr(project, 'project_type', None) is not None else ProjectType.DEFAULT,
            status=getattr(project, 'status', ProjectStatus.PtranslatedDING),
            source_url=project.project_metadata.get("source_url") if getattr(project, 'project_metadata', None) else None,
            source_file=str(getattr(project, 'video_path', '')) if getattr(project, 'video_path', None) is not None else None,
            video_path=str(getattr(project, 'video_path', '')) if getattr(project, 'video_path', None) is not None else None,  # addvideo_pathtranslatedfrontenduse
            thumbnail=getattr(project, 'thumbnail', None),  # fromdatabasefetchtranslated
            settings=getattr(project, 'processing_config', {}) or {},
            created_at=self._convert_utc_to_local(getattr(project, 'created_at', None)),
            updated_at=self._convert_utc_to_local(getattr(project, 'updated_at', None)),
            completed_at=self._convert_utc_to_local(getattr(project, 'completed_at', None)),
            total_clips=total_clips,
            total_collections=total_collections,
            total_tasks=total_tasks
        )
    
    def get_projects_paginated(
        self, 
        pagination: PaginationParams,
        filters: Optional[ProjectFilter] = None
    ) -> ProjectListResponse:
        """Get paginated projects with filtering."""
        # Convert filters to dict
        filter_dict = {}
        if filters:
            filter_data = filters.model_dump()
            filter_dict = {k: v for k, v in filter_data.items() if v is not None}
        
        items, pagination_response = self.get_paginated(pagination, filter_dict)
        
        # Convert to response schemas
        project_responses = []
        for project in items:
            # Get actual statistics for each project
            from ..models.clip import Clip
            from ..models.collection import Collection
            from ..models.task import Task
            
            project_id = str(project.id)
            total_clips = self.db.query(Clip).filter(Clip.project_id == project_id).count()
            total_collections = self.db.query(Collection).filter(Collection.project_id == project_id).count()
            total_tasks = self.db.query(Task).filter(Task.project_id == project_id).count()
            
            project_responses.append(ProjectResponse(
                error_message=self.latest_error_message(project),
                id=str(getattr(project, 'id', '')),
                name=str(getattr(project, 'name', '')),
                description=str(getattr(project, 'description', '')) if getattr(project, 'description', None) is not None else None,
                project_type=ProjectType(getattr(project, 'project_type').value) if hasattr(project, 'project_type') and hasattr(getattr(project, 'project_type'), 'value') else ProjectType.DEFAULT,
                status=ProjectStatus(getattr(project, 'status').value) if hasattr(project, 'status') and hasattr(getattr(project, 'status'), 'value') else ProjectStatus.PtranslatedDING,
                source_url=project.project_metadata.get("source_url") if getattr(project, 'project_metadata', None) else None,
                source_file=str(getattr(project, 'video_path', '')) if getattr(project, 'video_path', None) is not None else None,
                video_path=str(getattr(project, 'video_path', '')) if getattr(project, 'video_path', None) is not None else None,  # addvideo_pathtranslatedfrontenduse
                thumbnail=getattr(project, 'thumbnail', None),  # fromdatabasefetchtranslated
                settings=getattr(project, 'processing_config', {}) or {},
                created_at=self._convert_utc_to_local(getattr(project, 'created_at', None)),
                updated_at=self._convert_utc_to_local(getattr(project, 'updated_at', None)),
                completed_at=self._convert_utc_to_local(getattr(project, 'completed_at', None)),
                total_clips=total_clips,
                total_collections=total_collections,
                total_tasks=total_tasks
            ))
        
        return ProjectListResponse(
            items=project_responses,
            pagination=pagination_response
        )
    
    def start_project_processing(self, project_id: str) -> bool:
        """Start processing a project."""
        project = self.get(project_id)
        if not project or project.status != "pending":
            return False
        
        # Update status to processing
        self.update(project_id, status="processing")
        return True
    
    def complete_project(self, project_id: str) -> bool:
        """Mark project as completed."""
        project = self.get(project_id)
        if not project:
            return False
        
        # Update status and completion time
        from datetime import datetime
        self.update(project_id, status="completed", completed_at=datetime.utcnow())
        return True
    
    def fail_project(self, project_id: str, error_message: str = None) -> bool:
        """Mark project as failed."""
        project = self.get(project_id)
        if not project:
            return False
        
        # Update status and add error message to settings
        settings = project.settings or {}
        if error_message:
            settings["error_message"] = error_message
        
        self.update(project_id, status="failed", settings=settings)
        return True
    
    def update_project_status(self, project_id: str, status: str) -> bool:
        """Update project status."""
        project = self.get(project_id)
        if not project:
            return False
        
        # Update status
        self.update(project_id, status=status)
        return True
    
    def _convert_utc_to_local(self, dt):
        """translatedUTCtranslatedlocaltranslated（SQLitetranslatedinfo）"""
        if dt is None:
            return None
        
        from datetime import datetime, timezone
        import pytz
        
        # translatedSQLitetranslatedinfo，translatedthistranslatedIsUTCtranslated
        # translatedlocaltranslated
        local_tz = pytz.timezone('Asia/Shanghai')
        utc_time = dt.replace(tzinfo=timezone.utc)
        local_time = utc_time.astimezone(local_tz)
        
        return local_time
    
    def delete_project_with_files(self, project_id: str) -> bool:
        """
        deleteprojecttranslated
        
        Args:
            project_id: projectID
            
        Returns:
            Istranslateddeletesucceeded
        """
        try:
            # fetchprojectinfo
            project = self.get(project_id)
            if not project:
                logger.warning(f"project {project_id} not found")
                return False
            
            logger.info(f"translateddeleteproject {project_id}: {project.name}")
            
            # checkIstranslatedintranslated'stask（translatedstatus'sprojecttranslatedcheck）
            if project.status not in ["completed", "failed"]:
                running_tasks = self.db.query(Task).filter(
                    Task.project_id == project_id,
                    Task.status == TaskStatus.RUNNING
                ).count()
                
                if running_tasks > 0:
                    logger.warning(f"project {project_id} translated {running_tasks}  translatedintranslated'stask，translateddelete")
                    return False
            else:
                # translatedcompletedorfailed'sproject，translatedtaskstatustranslateddelete
                running_tasks = self.db.query(Task).filter(
                    Task.project_id == project_id,
                    Task.status == TaskStatus.RUNNING
                ).count()
                
                if running_tasks > 0:
                    logger.info(f"project {project_id} completed，translated {running_tasks}  translated'stask，translatedonetranslateddelete")
            
            # translated（iftranslated'stranslated）
            if not self.db.in_transaction():
                self.db.begin()
            
            try:
                # 1. deletetranslatedtask
                task_count = self.db.query(Task).filter(Task.project_id == project_id).count()
                if task_count > 0:
                    self.db.query(Task).filter(Task.project_id == project_id).delete()
                    logger.info(f"deleteproject {project_id} 's {task_count}  task")
                
                # 2. deletetranslatedclip
                clip_count = self.db.query(Clip).filter(Clip.project_id == project_id).count()
                if clip_count > 0:
                    self.db.query(Clip).filter(Clip.project_id == project_id).delete()
                    logger.info(f"deleteproject {project_id} 's {clip_count}  clip")
                
                # 3. deletetranslatedcollection
                collection_count = self.db.query(Collection).filter(Collection.project_id == project_id).count()
                if collection_count > 0:
                    self.db.query(Collection).filter(Collection.project_id == project_id).delete()
                    logger.info(f"deleteproject {project_id} 's {collection_count}  collection")
                
                # 4. deleteprojecttranslated
                self.db.query(Project).filter(Project.id == project_id).delete()
                logger.info(f"deleteproject {project_id} translated")
                
                # 5. translated
                self.db.commit()
                
                # 6. deleteprojectfile
                self._delete_project_files(project_id)
                
                # 7. cleanprogresstranslated
                self._cleanup_project_progress(project_id)
                
                logger.info(f"project {project_id} deletesucceeded")
                return True
                
            except Exception as e:
                self.db.rollback()
                logger.error(f"deleteproject {project_id} databasetranslatedfailed: {str(e)}")
                return False
            
        except Exception as e:
            logger.error(f"deleteproject {project_id} translatederror: {str(e)}")
            return False
    
    def _delete_project_files(self, project_id: str):
        """
        deleteprojecttranslated'sfile
        
        Args:
            project_id: projectID
        """
        try:
            # projectdirectorypath
            project_dir = Path(f"data/projects/{project_id}")
            
            if project_dir.exists():
                logger.info(f"deleteprojectdirectory: {project_dir}")
                shutil.rmtree(project_dir)
            else:
                logger.info(f"projectdirectorynot found: {project_dir}")
            
            # deletetranslateddirectorytranslated'stranslatedfile（iftranslatedin）
            # translated：translatedintranslateduseprojecttranslateddirectory，translateddirectory'scleantranslatedfile
            from ..core.path_utils import get_data_directory
            data_dir = get_data_directory()
            global_clips_dir = data_dir / "output" / "clips"
            global_collections_dir = data_dir / "output" / "collections"
            
            # deletetranslateddirectorytranslatedproject'sclipfile
            if global_clips_dir.exists():
                for clip_file in global_clips_dir.glob(f"*_{project_id}*"):
                    try:
                        clip_file.unlink()
                        logger.info(f"deletetranslatedclipfile: {clip_file}")
                    except Exception as e:
                        logger.warning(f"deletetranslatedclipfilefailed {clip_file}: {e}")
            
            # deletetranslateddirectorytranslatedproject'scollectionfile
            if global_collections_dir.exists():
                for collection_file in global_collections_dir.glob(f"*_{project_id}*"):
                    try:
                        collection_file.unlink()
                        logger.info(f"deletetranslatedcollectionfile: {collection_file}")
                    except Exception as e:
                        logger.warning(f"deletetranslatedcollectionfilefailed {collection_file}: {e}")
            
        except Exception as e:
            logger.error(f"deleteprojectfiletranslatederror: {str(e)}")
            # translated，translateddatabasedeletetranslated
    
    def _cleanup_project_progress(self, project_id: str):
        """
        cleanprojecttranslated'sprogresstranslated
        
        Args:
            project_id: projectID
        """
        try:
            # cleanRedistranslated'sprogresstranslated
            try:
                from ..services.simple_progress import clear_progress
                clear_progress(project_id)
                logger.info(f"cleanproject {project_id} 'sRedisprogresstranslated")
            except Exception as e:
                logger.warning(f"cleanRedisprogresstranslatedfailed: {e}")
            
            # cleantranslatedprogressservicetranslated'scache
            try:
                from ..services.enhanced_progress_service import progress_service
                if project_id in progress_service.progress_cache:
                    del progress_service.progress_cache[project_id]
                    logger.info(f"cleanproject {project_id} 'stranslatedprogresscache")
            except Exception as e:
                logger.warning(f"cleantranslatedprogresscachefailed: {e}")
            
        except Exception as e:
            logger.error(f"cleanprojectprogresstranslatedfailed: {str(e)}")
    
 