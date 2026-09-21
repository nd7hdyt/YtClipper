"""
Repositorytranslatedtest
verifytranslated'sfeature
"""

import sys, os
# addprojecttranslateddirectorytranslatedsys.path，ensuretranslatedbackendPackage
current_file = os.path.abspath(__file__)
backend_dir = os.path.dirname(os.path.dirname(current_file))  # backenddirectory
project_root = os.path.dirname(backend_dir)  # autocliptranslateddirectory

# translatedprojecttranslateddirectoryaddtranslatedsys.path，thistranslatedPythontranslatedbackendPackage
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
    """Repositorytranslatedtesttranslated"""
    
    @pytest.fixture(autouse=True)
    def setup_database(self):
        """settingstestdatabase"""
        # translateddatabase，ensuretesttranslated
        reset_database()
        # translateddatabase
        init_database()
        yield
        # testtranslatedcleandatabase
        reset_database()
    
    def test_project_repository_crud(self):
        """testprojectRepository'sCRUDtranslated"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        
        # createproject
        project_data = {
            "name": "testproject",
            "description": "thisIsone testproject",
            "project_type": ProjectType.KNOWLEDGE,
            "status": ProjectStatus.PtranslatedDING
        }
        
        project = project_repo.create(**project_data)
        assert project.id is not None
        assert project.name == "testproject"
        assert project.status == ProjectStatus.PtranslatedDING
        
        # translatedproject
        retrieved_project = project_repo.get_by_id(project.id)
        assert retrieved_project is not None
        assert retrieved_project.name == "testproject"
        
        # updateproject
        updated_project = project_repo.update(project.id, status=ProjectStatus.PROCESSING)
        assert updated_project.status == ProjectStatus.PROCESSING
        
        # deleteproject
        success = project_repo.delete(project.id)
        assert success is True
        
        # verifydelete
        deleted_project = project_repo.get_by_id(project.id)
        assert deleted_project is None
    
    def test_clip_repository_operations(self):
        """testclipRepository'stranslated"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        clip_repo = get_clip_repository(db)
        
        # createproject
        project = project_repo.create(
            name="testproject",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.PtranslatedDING
        )
        
        # createclip
        clip_data = {
            "project_id": project.id,
            "title": "testclip",
            "description": "thisIsone testclip",
            "start_time": 0,
            "end_time": 60,
            "duration": 60,
            "score": 0.8,
            "status": ClipStatus.COMPLETED
        }
        
        clip = clip_repo.create(**clip_data)
        assert clip.project_id == project.id
        assert clip.title == "testclip"
        
        # testbyprojecttranslatedclip
        project_clips = clip_repo.get_by_project(project.id)
        assert len(project_clips) == 1
        assert project_clips[0].id == clip.id
        
        # testbystatustranslatedclip
        completed_clips = clip_repo.get_by_status(ClipStatus.COMPLETED)
        assert len(completed_clips) == 1
        assert completed_clips[0].id == clip.id
        
        # testtranslatedcliptranslated
        high_score_clips = clip_repo.get_high_score_clips(project.id, min_score=0.7)
        assert len(high_score_clips) == 1
        assert high_score_clips[0].id == clip.id
    
    def test_collection_repository_operations(self):
        """testcollectionRepository'stranslated"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        collection_repo = get_collection_repository(db)
        
        # createproject
        project = project_repo.create(
            name="testproject",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.PtranslatedDING
        )
        
        # createcollection
        collection_data = {
            "project_id": project.id,
            "name": "testcollection",
            "description": "thisIsone testcollection",
            "theme": "testtranslated",
            "clips_count": 5,
            "total_duration": 300,
            "status": CollectionStatus.COMPLETED
        }
        
        collection = collection_repo.create(**collection_data)
        assert collection.project_id == project.id
        assert collection.name == "testcollection"
        
        # testbyprojecttranslatedcollection
        project_collections = collection_repo.get_by_project(project.id)
        assert len(project_collections) == 1
        assert project_collections[0].id == collection.id
        
        # testbytranslatedcollection
        theme_collections = collection_repo.get_by_theme(project.id, "testtranslated")
        assert len(theme_collections) == 1
        assert theme_collections[0].id == collection.id
    
    def test_task_repository_operations(self):
        """testtaskRepository'stranslated"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        task_repo = get_task_repository(db)
        
        # createproject
        project = project_repo.create(
            name="testproject",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.PtranslatedDING
        )
        
        # createtask
        task_data = {
            "project_id": project.id,
            "name": "testtask",
            "description": "thisIsone testtask",
            "task_type": TaskType.VIDEO_PROCESSING,
            "status": TaskStatus.PtranslatedDING,
            "priority": 1
        }
        
        task = task_repo.create(**task_data)
        assert task.project_id == project.id
        assert task.name == "testtask"
        assert task.status == TaskStatus.PtranslatedDING
        
        # testtaskstatusupdate
        task_repo.update_task_status(task.id, TaskStatus.RUNNING)
        updated_task = task_repo.get_by_id(task.id)
        assert updated_task.status == TaskStatus.RUNNING
        
        # testtasktranslated
        task_repo.update_task_status(task.id, TaskStatus.COMPLETED)
        completed_task = task_repo.get_by_id(task.id)
        assert completed_task.status == TaskStatus.COMPLETED
        
        # testbyprojecttranslatedtask
        project_tasks = task_repo.get_by_project(project.id)
        assert len(project_tasks) == 1
        assert project_tasks[0].id == task.id
    
    def test_repository_statistics(self):
        """testRepositorytranslatedfeature"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        clip_repo = get_clip_repository(db)
        collection_repo = get_collection_repository(db)
        task_repo = get_task_repository(db)
        
        # createproject
        project = project_repo.create(
            name="translatedtestproject",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.COMPLETED
        )
        
        # createmulti clip
        for i in range(5):
            clip_repo.create(
                project_id=project.id,
                title=f"clip{i+1}",
                start_time=i*60,
                end_time=(i+1)*60,
                duration=60,
                score=0.7 + i*0.1,
                status=ClipStatus.COMPLETED
            )
        
        # createmulti collection
        for i in range(3):
            collection_repo.create(
                project_id=project.id,
                name=f"collection{i+1}",
                theme=f"translated{i+1}",
                clips_count=2,
                total_duration=120,
                status=CollectionStatus.COMPLETED
            )
        
        # createmulti task
        for i in range(6):
            task_repo.create(
                project_id=project.id,
                name=f"task{i+1}",
                            task_type=TaskType.VIDEO_PROCESSING,
            status=TaskStatus.COMPLETED if i < 5 else TaskStatus.FAILED
            )
        
        # testprojecttranslated
        project_stats = project_repo.get_project_statistics()
        assert project_stats["total"] >= 1
        assert project_stats["completed"] >= 1
        
        # testcliptranslated
        clip_stats = clip_repo.get_clips_statistics(project.id)
        assert clip_stats["total"] == 5
        assert clip_stats["completed"] == 5
        assert clip_stats["avg_score"] > 0.7
        
        # testcollectiontranslated
        collection_stats = collection_repo.get_collections_statistics(project.id)
        assert collection_stats["total"] == 3
        assert collection_stats["completed"] == 3
        
        # testtasktranslated
        task_stats = task_repo.get_tasks_statistics(project.id)
        assert task_stats["total"] == 6
        assert task_stats["completed"] == 5
        assert task_stats["failed"] == 1
    
    def test_repository_search(self):
        """testRepositorytranslatedfeature"""
        db = next(get_db())
        project_repo = get_project_repository(db)
        clip_repo = get_clip_repository(db)
        
        # createproject
        project = project_repo.create(
            name="translatedtestproject",
            description="thisIsone usetranslatedtest'sproject",
            project_type=ProjectType.KNOWLEDGE,
            status=ProjectStatus.PtranslatedDING
        )
        
        # createclip
        clip_repo.create(
            project_id=project.id,
            title="Packageincludetranslated'sclip",
            description="this clipPackageincludetranslated'stranslated",
            start_time=0,
            end_time=60,
            duration=60,
            status=ClipStatus.COMPLETED
        )
        
        # testprojecttranslated
        search_results = project_repo.search_projects("translatedtest")
        assert len(search_results) == 1
        assert search_results[0].id == project.id
        
        # testcliptranslated
        clip_results = clip_repo.search_clips(project.id, "translated")
        assert len(clip_results) == 1
        assert "translated" in clip_results[0].title or "translated" in clip_results[0].description

if __name__ == "__main__":
    # translatedtest
    pytest.main([__file__, "-v"]) 
