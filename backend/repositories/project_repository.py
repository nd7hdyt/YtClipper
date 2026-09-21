"""
projectRepository
Providesprojecttranslated'stranslated
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from pathlib import Path
from .base import BaseRepository
from ..models.project import Project, ProjectStatus, ProjectType

class ProjectRepository(BaseRepository[Project]):
    """projectRepositorytranslated"""
    
    def __init__(self, db: Session):
        super().__init__(Project, db)
    
    def get_by_status(self, status: ProjectStatus) -> List[Project]:
        """
        translatedstatusfetchprojectlist
        
        Args:
            status: projectstatus
            
        Returns:
            projectlist
        """
        return self.find_by(status=status)
    
    def get_by_category(self, category: ProjectType) -> List[Project]:
        """
        translatedprojecttranslatedfetchprojectlist
        
        Args:
            category: projecttranslated
            
        Returns:
            projectlist
        """
        return self.find_by(project_type=category)
    
    def get_recent_projects(self, limit: int = 10) -> List[Project]:
        """
        fetchtranslatedcreate'sproject
        
        Args:
            limit: returntranslated
            
        Returns:
            translated'sprojectlist
        """
        return self.db.query(self.model).order_by(
            desc(self.model.created_at)
        ).limit(limit).all()
    
    def create_project(self, project_data: Dict[str, Any]) -> Project:
        """createprojecttranslated（translated）"""
        from ..services.storage_service import StorageService
        import uuid
        
        # translatedprojectID（iftranslatedProvides）
        if "id" not in project_data:
            project_data["id"] = str(uuid.uuid4())
        
        # translatedservice
        storage_service = StorageService(project_data["id"])
        
        # createprojecttranslated
        project = Project(
            id=project_data["id"],
            name=project_data["name"],
            description=project_data.get("description"),
            project_type=project_data.get("project_type", ProjectType.DEFAULT),
            status=project_data.get("status", ProjectStatus.PtranslatedDING),
            processing_config=project_data.get("processing_config", {}),
            project_metadata={
                'project_id': project_data["id"],
                'created_at': project_data.get("created_at"),
                'storage_service_initialized': True
            }
        )
        
        self.db.add(project)
        self.db.commit()
        return project
    
    def get_project_file_paths(self, project_id: str) -> Dict[str, Optional[Path]]:
        """fetchprojectfile path"""
        project = self.get_by_id(project_id)
        if not project:
            return {}
        
        return {
            "video_path": Path(project.video_path) if project.video_path else None,
            "subtitle_path": Path(project.subtitle_path) if project.subtitle_path else None
        }
    
    def update_project_file_path(self, project_id: str, file_type: str, file_path: str) -> bool:
        """updateprojectfile path"""
        project = self.get_by_id(project_id)
        if not project:
            return False
        
        if file_type == "video":
            project.video_path = file_path
        elif file_type == "subtitle":
            project.subtitle_path = file_path
        else:
            return False
        
        self.db.commit()
        return True
    
    def get_project_storage_info(self, project_id: str) -> Dict[str, Any]:
        """fetchprojecttranslatedinfo"""
        from ..services.storage_service import StorageService
        
        project = self.get_by_id(project_id)
        if not project:
            return {}
        
        storage_service = StorageService(project_id)
        storage_info = storage_service.get_project_storage_info()
        
        return {
            "project_id": project_id,
            "storage_info": storage_info,
            "file_paths": {
                "video_path": project.video_path,
                "subtitle_path": project.subtitle_path
            }
        }
    
    def get_processing_projects(self) -> List[Project]:
        """
        fetchtranslatedinprocess'sproject
        
        Returns:
            translatedinprocess'sprojectlist
        """
        return self.find_by(status=ProjectStatus.PROCESSING)
    
    def get_completed_projects(self) -> List[Project]:
        """
        fetchcompleted'sproject
        
        Returns:
            completed'sprojectlist
        """
        return self.find_by(status=ProjectStatus.COMPLETED)
    
    def get_error_projects(self) -> List[Project]:
        """
        fetchtranslated'sproject
        
        Returns:
            translated'sprojectlist
        """
        return self.find_by(status=ProjectStatus.FAILED)
    
    def search_projects(self, keyword: str) -> List[Project]:
        """
        translatedproject
        
        Args:
            keyword: translated
            
        Returns:
            translated'sprojectlist
        """
        return self.db.query(self.model).filter(
            self.model.name.contains(keyword) | 
            self.model.description.contains(keyword)
        ).all()
    
    def get_projects_with_clips_count(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        fetchprojectlist，Packageincludecliptranslated
        
        Args:
            skip: skip'stranslated
            limit: return'stranslated
            
        Returns:
            projectlist
        """
        return self.db.query(self.model).options(
            # thistranslatedcantranslatedaddtranslatedSelecttranslated，translatedN+1translatedissue
        ).offset(skip).limit(limit).all()
    
    def get_project_with_details(self, project_id: str) -> Optional[Project]:
        """
        fetchprojecttranslated，Packageincludetranslated'sclipAndcollection
        
        Args:
            project_id: projectID
            
        Returns:
            projecttranslatedorNone
        """
        return self.db.query(self.model).filter(
            self.model.id == project_id
        ).first()
    
    def update_project_status(self, project_id: str, status: ProjectStatus) -> Optional[Project]:
        """
        updateprojectstatus
        
        Args:
            project_id: projectID
            status: translatedstatus
            
        Returns:
            updatetranslated'sprojecttranslatedorNone
        """
        return self.update(project_id, status=status)
    
    def get_projects_by_date_range(self, start_date, end_date) -> List[Project]:
        """
        translatedfetchproject
        
        Args:
            start_date: translated
            end_date: translated
            
        Returns:
            projectlist
        """
        return self.db.query(self.model).filter(
            self.model.created_at >= start_date,
            self.model.created_at <= end_date
        ).order_by(desc(self.model.created_at)).all()
    
    def get_project_statistics(self) -> dict:
        """
        fetchprojecttranslatedinfo
        
        Returns:
            translatedinfotranslated
        """
        total_projects = self.count()
        processing_projects = len(self.get_processing_projects())
        completed_projects = len(self.get_completed_projects())
        error_projects = len(self.get_error_projects())
        
        return {
            "total": total_projects,
            "processing": processing_projects,
            "completed": completed_projects,
            "error": error_projects,
            "success_rate": (completed_projects / total_projects * 100) if total_projects > 0 else 0
        }