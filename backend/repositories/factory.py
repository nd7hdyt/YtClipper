"""
RepositoryEN
ENRepositoryEN
"""

from typing import Dict, Type
from sqlalchemy.orm import Session
from ..repositories.base import BaseRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.clip_repository import ClipRepository
from ..repositories.collection_repository import CollectionRepository
from ..repositories.task_repository import TaskRepository

class RepositoryFactory:
    """RepositoryEN"""
    
    def __init__(self, db: Session):
        """
        initializeRepositoryEN
        
        Args:
            db: databaseEN
        """
        self.db = db
        self._repositories: Dict[str, BaseRepository] = {}
    
    def get_project_repository(self) -> ProjectRepository:
        """fetchprojectRepository"""
        if "project" not in self._repositories:
            self._repositories["project"] = ProjectRepository(self.db)
        return self._repositories["project"]
    
    def get_clip_repository(self) -> ClipRepository:
        """fetchclipRepository"""
        if "clip" not in self._repositories:
            self._repositories["clip"] = ClipRepository(self.db)
        return self._repositories["clip"]
    
    def get_collection_repository(self) -> CollectionRepository:
        """fetchcollectionRepository"""
        if "collection" not in self._repositories:
            self._repositories["collection"] = CollectionRepository(self.db)
        return self._repositories["collection"]
    
    def get_task_repository(self) -> TaskRepository:
        """fetchtaskRepository"""
        if "task" not in self._repositories:
            self._repositories["task"] = TaskRepository(self.db)
        return self._repositories["task"]
    
    def get_repository(self, repository_type: str) -> BaseRepository:
        """
        ENfetchRepository
        
        Args:
            repository_type: RepositoryEN
            
        Returns:
            RepositoryEN
        """
        repository_map = {
            "project": self.get_project_repository,
            "clip": self.get_clip_repository,
            "collection": self.get_collection_repository,
            "task": self.get_task_repository
        }
        
        if repository_type not in repository_map:
            raise ValueError(f"Unknown repository type: {repository_type}")
        
        return repository_map[repository_type]()
    
    def clear_cache(self):
        """ENRepositorycache"""
        self._repositories.clear()
    
    def __enter__(self):
        """EN"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """EN"""
        self.clear_cache()

# ENRepositoryEN
_repository_factory: RepositoryFactory = None

def get_repository_factory(db: Session) -> RepositoryFactory:
    """
    fetchRepositoryEN
    
    Args:
        db: databaseEN
        
    Returns:
        RepositoryEN
    """
    global _repository_factory
    if _repository_factory is None or _repository_factory.db != db:
        _repository_factory = RepositoryFactory(db)
    return _repository_factory

def get_project_repository(db: Session) -> ProjectRepository:
    """
    fetchprojectRepository
    
    Args:
        db: databaseEN
        
    Returns:
        projectRepositoryEN
    """
    return get_repository_factory(db).get_project_repository()

def get_clip_repository(db: Session) -> ClipRepository:
    """
    fetchclipRepository
    
    Args:
        db: databaseEN
        
    Returns:
        clipRepositoryEN
    """
    return get_repository_factory(db).get_clip_repository()

def get_collection_repository(db: Session) -> CollectionRepository:
    """
    fetchcollectionRepository
    
    Args:
        db: databaseEN
        
    Returns:
        collectionRepositoryEN
    """
    return get_repository_factory(db).get_collection_repository()

def get_task_repository(db: Session) -> TaskRepository:
    """
    fetchtaskRepository
    
    Args:
        db: databaseEN
        
    Returns:
        taskRepositoryEN
    """
    return get_repository_factory(db).get_task_repository() 