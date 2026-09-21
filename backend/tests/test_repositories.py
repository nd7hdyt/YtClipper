"""
RepositoryEN
EN
"""

import sys, os
# ENsys.path，ENbackendEN
current_file = os.path.abspath(__file__)
backend_dir = os.path.dirname(os.path.dirname(current_file))  # backendEN
project_root = os.path.dirname(backend_dir)  # autoclipEN

# ENsys.path，ENPythonENbackendEN
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.repositories.factory import (
    get_project_repository,
    get_clip_repository,
    get_collection_repository,
    get_task_repository
)
from backend.core.database import get_db, init_database, reset_database
from backend.models.project import ProjectStatus, ProjectType
from backend.models.clip import ClipStatus
from backend.models.collection import CollectionStatus
from backend.models.task import TaskStatus, TaskType

class TestRepositoryPattern:
    """RepositoryEN"""
    
    @pytest.fixture(autouse=True)
    def setup_database(self):
        """EN"""
        # EN，EN
        reset_database()
        # EN
        init_database()
        yield
        # EN
        reset_database()
    
    def test_project_repository_crud(self):
        """ENRepositoryENCRUDEN"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        
        # EN
        project_data = {
            "name": "EN",
            "description": "EN",
            "project_type": ProjectType.KNOWLEDGE,
            "status": ProjectStatus.PENDING
        }
        
        project = project_repo.create(**project_data)
        assert project.id is not None
        assert project.name == "EN"
        assert project.status == ProjectStatus.PENDING
        
        # EN
        retrieved_project = project_repo.get_by_id(project.id)
        assert retrieved_project is not None
        assert retrieved_project.name == "EN"
        
        # EN
        updated_project = project_repo.update(project.id, status=ProjectStatus.PROCESSING)
        assert updated_project.status == ProjectStatus.PROCESSING
        
        # EN
        success = project_repo.delete(project.id)
        assert success is True
        
        # EN
        deleted_project = project_repo.get_by_id(project.id)
        assert deleted_project is None
    
    def test_clip_repository_operations(self):
        """ENRepositoryEN"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        clip_repo = get_clip_repository(db)
        
        # EN
        project = project_repo.create(
            name="EN",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.PENDING
        )
        
        # EN
        clip_data = {
            "project_id": project.id,
            "title": "EN",
            "description": "EN",
            "start_time": 0,
            "end_time": 60,
            "duration": 60,
            "score": 0.8,
            "status": ClipStatus.COMPLETED
        }
        
        clip = clip_repo.create(**clip_data)
        assert clip.project_id == project.id
        assert clip.title == "EN"
        
        # EN
        project_clips = clip_repo.get_by_project(project.id)
        assert len(project_clips) == 1
        assert project_clips[0].id == clip.id
        
        # EN
        completed_clips = clip_repo.get_by_status(ClipStatus.COMPLETED)
        assert len(completed_clips) == 1
        assert completed_clips[0].id == clip.id
        
        # EN
        high_score_clips = clip_repo.get_high_score_clips(project.id, min_score=0.7)
        assert len(high_score_clips) == 1
        assert high_score_clips[0].id == clip.id
    
    def test_collection_repository_operations(self):
        """ENRepositoryEN"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        collection_repo = get_collection_repository(db)
        
        # EN
        project = project_repo.create(
            name="EN",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.PENDING
        )
        
        # EN
        collection_data = {
            "project_id": project.id,
            "name": "EN",
            "description": "EN",
            "theme": "EN",
            "clips_count": 5,
            "total_duration": 300,
            "status": CollectionStatus.COMPLETED
        }
        
        collection = collection_repo.create(**collection_data)
        assert collection.project_id == project.id
        assert collection.name == "EN"
        
        # EN
        project_collections = collection_repo.get_by_project(project.id)
        assert len(project_collections) == 1
        assert project_collections[0].id == collection.id
        
        # EN
        theme_collections = collection_repo.get_by_theme(project.id, "EN")
        assert len(theme_collections) == 1
        assert theme_collections[0].id == collection.id
    
    def test_task_repository_operations(self):
        """ENRepositoryEN"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        task_repo = get_task_repository(db)
        
        # EN
        project = project_repo.create(
            name="EN",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.PENDING
        )
        
        # EN
        task_data = {
            "project_id": project.id,
            "name": "EN",
            "description": "EN",
            "task_type": TaskType.VIDEO_PROCESSING,
            "status": TaskStatus.PENDING,
            "priority": 1
        }
        
        task = task_repo.create(**task_data)
        assert task.project_id == project.id
        assert task.name == "EN"
        assert task.status == TaskStatus.PENDING
        
        # EN
        task_repo.update_task_status(task.id, TaskStatus.RUNNING)
        updated_task = task_repo.get_by_id(task.id)
        assert updated_task.status == TaskStatus.RUNNING
        
        # EN
        task_repo.update_task_status(task.id, TaskStatus.COMPLETED)
        completed_task = task_repo.get_by_id(task.id)
        assert completed_task.status == TaskStatus.COMPLETED
        
        # EN
        project_tasks = task_repo.get_by_project(project.id)
        assert len(project_tasks) == 1
        assert project_tasks[0].id == task.id
    
    def test_repository_statistics(self):
        """ENRepositoryEN"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        clip_repo = get_clip_repository(db)
        collection_repo = get_collection_repository(db)
        task_repo = get_task_repository(db)
        
        # EN
        project = project_repo.create(
            name="EN",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.COMPLETED
        )
        
        # EN
        for i in range(5):
            clip_repo.create(
                project_id=project.id,
                title=f"EN{i+1}",
                start_time=i*60,
                end_time=(i+1)*60,
                duration=60,
                score=0.7 + i*0.1,
                status=ClipStatus.COMPLETED
            )
        
        # EN
        for i in range(3):
            collection_repo.create(
                project_id=project.id,
                name=f"EN{i+1}",
                theme=f"EN{i+1}",
                clips_count=2,
                total_duration=120,
                status=CollectionStatus.COMPLETED
            )
        
        # EN
        for i in range(6):
            task_repo.create(
                project_id=project.id,
                name=f"EN{i+1}",
                            task_type=TaskType.VIDEO_PROCESSING,
            status=TaskStatus.COMPLETED if i < 5 else TaskStatus.FAILED
            )
        
        # EN
        project_stats = project_repo.get_project_statistics()
        assert project_stats["total"] >= 1
        assert project_stats["completed"] >= 1
        
        # EN
        clip_stats = clip_repo.get_clips_statistics(project.id)
        assert clip_stats["total"] == 5
        assert clip_stats["completed"] == 5
        assert clip_stats["avg_score"] > 0.7
        
        # EN
        collection_stats = collection_repo.get_collections_statistics(project.id)
        assert collection_stats["total"] == 3
        assert collection_stats["completed"] == 3
        
        # EN
        task_stats = task_repo.get_tasks_statistics(project.id)
        assert task_stats["total"] == 6
        assert task_stats["completed"] == 5
        assert task_stats["failed"] == 1
    
    def test_repository_search(self):
        """ENRepositoryEN"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        clip_repo = get_clip_repository(db)
        
        # EN
        project = project_repo.create(
            name="EN",
            description="EN",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.PENDING
        )
        
        # EN
        clip_repo.create(
            project_id=project.id,
            title="EN",
            description="EN",
            start_time=0,
            end_time=60,
            duration=60,
            status=ClipStatus.COMPLETED
        )
        
        # EN
        search_results = project_repo.search_projects("EN")
        assert len(search_results) == 1
        assert search_results[0].id == project.id
        
        # EN
        clip_results = clip_repo.search_clips(project.id, "EN")
        assert len(clip_results) == 1
        assert "EN" in clip_results[0].title or "EN" in clip_results[0].description

if __name__ == "__main__":
    # EN
    pytest.main([__file__, "-v"]) 
