"""
translatedservice - translatedprocesstranslateddatabase
"""

import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from sqlalchemy.orm import Session
from backend.models.clip import Clip, ClipStatus
from backend.models.collection import Collection, CollectionStatus
from backend.models.project import Project, ProjectStatus, ProjectType
from backend.models.task import Task, TaskStatus, TaskType
from datetime import datetime

logger = logging.getLogger(__name__)


class DataSyncService:
    """translatedservice"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def sync_all_projects_from_filesystem(self, data_dir: Path) -> Dict[str, Any]:
        """fromfileSystemtranslatedprojecttranslateddatabase"""
        try:
            logger.info(f"translatedfromfileSystemtranslatedproject: {data_dir}")
            
            projects_dir = data_dir / "projects"
            if not projects_dir.exists():
                logger.warning(f"projectdirectorynot found: {projects_dir}")
                return {"success": False, "error": "projectdirectorynot found"}
            
            synced_projects = []
            failed_projects = []
            
            # translatedprojectdirectory
            for project_dir in projects_dir.iterdir():
                if project_dir.is_dir() and not project_dir.name.startswith('.'):
                    project_id = project_dir.name
                    try:
                        result = self.sync_project_from_filesystem(project_id, project_dir)
                        if result["success"]:
                            synced_projects.append(project_id)
                        else:
                            failed_projects.append({"project_id": project_id, "error": result.get("error")})
                    except Exception as e:
                        logger.error(f"translatedproject {project_id} failed: {str(e)}")
                        failed_projects.append({"project_id": project_id, "error": str(e)})
            
            logger.info(f"translated: succeeded {len(synced_projects)}  , failed {len(failed_projects)}  ")
            
            return {
                "success": True,
                "synced_projects": synced_projects,
                "failed_projects": failed_projects,
                "total_synced": len(synced_projects),
                "total_failed": len(failed_projects)
            }
            
        except Exception as e:
            logger.error(f"translatedprojectfailed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def sync_project_from_filesystem(self, project_id: str, project_dir: Path) -> Dict[str, Any]:
        """fromfileSystemtranslated projecttranslateddatabase"""
        try:
            logger.info(f"translatedproject: {project_id}")
            
            # checkprojectIstranslatedintranslateddatabase
            existing_project = self.db.query(Project).filter(Project.id == project_id).first()
            if existing_project:
                logger.info(f"project {project_id} translatedintranslateddatabase，translatedcliptranslated")
            else:
                # translatedprojecttranslated
                project_metadata = self._read_project_metadata(project_dir)
                if not project_metadata:
                    logger.warning(f"project {project_id} translatedfile，createtranslatedprojecttranslated")
                    project_metadata = {
                        "project_name": f"project_{project_id[:8]}",
                        "created_at": datetime.now().isoformat(),
                        "status": "pending"
                    }
                
                # createprojecttranslated
                project = Project(
                    id=project_id,
                    name=project_metadata.get("project_name", f"project_{project_id[:8]}"),
                    description=project_metadata.get("description", ""),
                    project_type=ProjectType.KNOWLEDGE,  # defaulttranslated
                    status=ProjectStatus.PtranslatedDING,
                    processing_config=project_metadata.get("processing_config", {}),
                    project_metadata=project_metadata
                )
                
                self.db.add(project)
                self.db.commit()
                self.db.refresh(project)
                
                logger.info(f"project {project_id} translateddatabasesucceeded")
            

            
            # translatedcliptranslated
            clips_count = self._sync_clips_from_filesystem(project_id, project_dir)
            
            # translatedcollectiontranslated
            logger.info(f"translatedproject {project_id} 'scollectiontranslated")
            collections_count = self._sync_collections_from_filesystem(project_id, project_dir)
            logger.info(f"project {project_id} collectiontranslated，translated {collections_count}  collection")
            
            # checkprojectIstranslatedcompletedprocess，updateprojectstatus
            self._update_project_status_if_completed(project_id, project_dir)
            
            return {
                "success": True,
                "project_id": project_id,
                "clips_synced": clips_count,
                "collections_synced": collections_count
            }
            
        except Exception as e:
            logger.error(f"translatedproject {project_id} failed: {str(e)}")
            self.db.rollback()
            return {"success": False, "error": str(e)}
    
    def _read_project_metadata(self, project_dir: Path) -> Optional[Dict[str, Any]]:
        """translatedprojecttranslated"""
        metadata_files = [
            project_dir / "project.json",
            project_dir / "metadata.json",
            project_dir / "info.json"
        ]
        
        for metadata_file in metadata_files:
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as e:
                    logger.warning(f"translatedfilefailed {metadata_file}: {e}")
        
        return None
    
    def _sync_clips_from_filesystem(self, project_id: str, project_dir: Path) -> int:
        """fromfileSystemtranslatedcliptranslated"""
        try:
            # translatedcliptranslatedfile
            clips_files = [
                project_dir / "step6_video" / "clips_metadata.json",  # translated'stranslated
                project_dir / "step3_all_scored.json",  # translatedusetranslated'stranslated
                project_dir / "step4_title" / "step4_title.json",
                project_dir / "step4_titles.json",
                project_dir / "clips_metadata.json",
                project_dir / "metadata" / "clips_metadata.json"
            ]
            
            clips_data = None
            for clips_file in clips_files:
                logger.info(f"checkclipfile: {clips_file}")
                if clips_file.exists():
                    try:
                        with open(clips_file, 'r', encoding='utf-8') as f:
                            clips_data = json.load(f)
                        logger.info(f"succeededtranslatedclipfile: {clips_file}, translated: {len(clips_data) if isinstance(clips_data, list) else 'not list'}")
                        break
                    except Exception as e:
                        logger.warning(f"translatedclipfilefailed {clips_file}: {e}")
                else:
                    logger.info(f"clipfile not found: {clips_file}")
            
            if not clips_data:
                logger.info(f"project {project_id} translatedcliptranslated")
                return 0
            
            # ensureclips_dataIslist
            if isinstance(clips_data, dict) and "clips" in clips_data:
                clips_data = clips_data["clips"]
            elif not isinstance(clips_data, list):
                logger.warning(f"project {project_id} cliptranslatedformattranslated")
                return 0
            
            synced_count = 0
            updated_count = 0
            for clip_data in clips_data:
                try:
                    # checkclipIstranslatedin
                    existing_clip = self.db.query(Clip).filter(
                        Clip.project_id == project_id,
                        Clip.title == clip_data.get("generated_title", clip_data.get("title", ""))
                    ).first()
                    
                    if existing_clip:
                        # updatetranslatedclip'svideo_pathAndtags，translateduseprojecttranslateddirectory
                        clip_id = clip_data.get('id', str(synced_count + 1))
                        safe_title = clip_data.get('generated_title', clip_data.get('title', clip_data.get('outline', '')))
                        # cleanfiletranslated，translated
                        safe_title = "".join(c for c in safe_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        safe_title = safe_title.replace(' ', '_')
                        
                        # translateduseprojecttranslatedpath
                        from ..core.path_utils import get_project_directory
                        project_dir = get_project_directory(project_id)
                        project_clips_dir = project_dir / "output" / "clips"
                        project_clips_dir.mkdir(parents=True, exist_ok=True)
                        project_video_path = project_clips_dir / f"{clip_id}_{safe_title}.mp4"
                        
                        # translated'stranslateddirectory，iftranslatedintranslatedprojectdirectory
                        from ..core.path_utils import get_data_directory
                        legacy_video_path = get_data_directory() / "output" / "clips" / f"{clip_id}_{safe_title}.mp4"
                        try:
                            if legacy_video_path.exists() and not project_video_path.exists():
                                import shutil
                                shutil.copy2(legacy_video_path, project_video_path)
                                logger.info(f"translatedclipfiletranslatedprojectdirectory: {legacy_video_path} -> {project_video_path}")
                        except Exception as _e:
                            logger.warning(f"translatedclipfilefailed: {legacy_video_path} -> {project_video_path}: {_e}")
                        
                        # translateduseprojecttranslatedpath
                        video_path = str(project_video_path)
                        logger.info(f"updateclip {existing_clip.id} 'svideo_path: {video_path}")
                        existing_clip.video_path = video_path
                        if existing_clip.tags is None:
                            existing_clip.tags = []  # ensuretagsIstranslatedlisttranslatedIsnull
                        updated_count += 1
                        continue
                    
                    # translatedformat
                    start_time = self._convert_time_to_seconds(clip_data.get('start_time', '00:00:00'))
                    end_time = self._convert_time_to_seconds(clip_data.get('end_time', '00:00:00'))
                    duration = end_time - start_time
                    
                    # translatedvideofile path，translateduseprojecttranslateddirectory
                    clip_id = clip_data.get('id', str(synced_count + 1))
                    title = clip_data.get('generated_title', clip_data.get('title', clip_data.get('outline', '')))
                    
                    # translateduseprojecttranslatedpath
                    from ..core.path_utils import get_project_directory, get_data_directory
                    project_dir = get_project_directory(project_id)
                    project_clips_dir = project_dir / "output" / "clips"
                    project_clips_dir.mkdir(parents=True, exist_ok=True)
                    
                    # translated'sfiletranslated（translated）
                    actual_filename = None
                    for file_path in project_clips_dir.glob(f"{clip_id}_*.mp4"):
                        actual_filename = file_path.name
                        break
                    
                    if actual_filename:
                        project_video_path = project_clips_dir / actual_filename
                    else:
                        # iftranslatedfile，usecleantranslated'sfiletranslated
                        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        safe_title = safe_title.replace(' ', '_')
                        project_video_path = project_clips_dir / f"{clip_id}_{safe_title}.mp4"
                    
                    # translated'stranslateddirectory，iftranslatedintranslatedprojectdirectory
                    global_clips_dir = get_data_directory() / "output" / "clips"
                    if actual_filename:
                        global_video_path = global_clips_dir / actual_filename
                    else:
                        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        safe_title = safe_title.replace(' ', '_')
                        global_video_path = global_clips_dir / f"{clip_id}_{safe_title}.mp4"
                    
                    if global_video_path.exists() and not project_video_path.exists():
                        import shutil
                        shutil.copy2(global_video_path, project_video_path)
                        logger.info(f"translatedclipfilefromtranslateddirectorytranslatedprojectdirectory: {global_video_path} -> {project_video_path}")
                    
                    # translateduseprojecttranslatedpath
                    video_path = str(project_video_path)
                    
                    # createcliptranslated
                    clip = Clip(
                        project_id=project_id,
                        title=clip_data.get('generated_title', clip_data.get('title', clip_data.get('outline', ''))),
                        description=clip_data.get('recommend_reason', ''),
                        start_time=start_time,
                        end_time=end_time,
                        duration=duration,
                        score=clip_data.get('final_score', 0.0),
                        video_path=video_path,
                        tags=[],  # ensuretagsIstranslatedlisttranslatedIsnull
                        clip_metadata=clip_data,
                        status=ClipStatus.COMPLETED
                    )
                    
                    self.db.add(clip)
                    synced_count += 1
                    
                except Exception as e:
                    logger.error(f"translatedclipfailed: {e}")
                    continue
            
            self.db.commit()
            logger.info(f"project {project_id} translated {synced_count}  clip，updatetranslated {updated_count}  clip")
            return synced_count
            
        except Exception as e:
            logger.error(f"translatedcliptranslatedfailed: {str(e)}")
            return 0
    
    def _sync_collections_from_filesystem(self, project_id: str, project_dir: Path) -> int:
        """fromfileSystemtranslatedcollectiontranslated"""
        try:
            # translatedcollectionsdirectorypath
            collections_dir = project_dir / "output" / "collections"
            
            # translatedcollectiontranslatedfile
            collections_files = [
                project_dir / "step6_video" / "collections_metadata.json",  # translated'stranslated
                project_dir / "step5_clustering" / "step5_clustering.json",
                project_dir / "metadata" / "step5_collections.json",  # addstep5_collections.json
                project_dir / "collections_metadata.json",
                project_dir / "metadata" / "collections_metadata.json"
            ]
            
            collections_data = None
            for collections_file in collections_files:
                logger.info(f"checkcollectionfile: {collections_file}")
                if collections_file.exists():
                    try:
                        with open(collections_file, 'r', encoding='utf-8') as f:
                            collections_data = json.load(f)
                        logger.info(f"succeededtranslatedcollectionfile: {collections_file}, translated: {len(collections_data) if isinstance(collections_data, list) else 'not list'}")
                        break
                    except Exception as e:
                        logger.warning(f"translatedcollectionfilefailed {collections_file}: {e}")
                else:
                    logger.info(f"collectionfile not found: {collections_file}")
            
            if not collections_data:
                logger.info(f"project {project_id} translatedcollectiontranslated")
                return 0
            
            # ensurecollections_dataIslist
            if isinstance(collections_data, dict) and "collections" in collections_data:
                collections_data = collections_data["collections"]
            elif not isinstance(collections_data, list):
                logger.warning(f"project {project_id} collectiontranslatedformattranslated")
                return 0
            
            # translateddeletetranslatedfile
            deleted_collections_file = project_dir / "deleted_collections.json"
            deleted_collections = set()
            if deleted_collections_file.exists():
                try:
                    with open(deleted_collections_file, 'r', encoding='utf-8') as f:
                        deleted_data = json.load(f)
                        deleted_collections = set(deleted_data.get('deleted_collection_ids', []))
                except Exception as e:
                    logger.warning(f"translateddeletetranslatedfailed: {e}")
            
            synced_count = 0
            for collection_data in collections_data:
                try:
                    collection_id = collection_data.get("id", "")
                    collection_title = collection_data.get("collection_title", "")
                    
                    # checkIstranslateddelete
                    if collection_id in deleted_collections:
                        logger.info(f"collection {collection_id} translateddelete，skiptranslated")
                        continue
                    
                    # checkcollectionIstranslatedin
                    existing_collection = self.db.query(Collection).filter(
                        Collection.project_id == project_id,
                        Collection.name == collection_title
                    ).first()
                    
                    if existing_collection:
                        # collectiontranslatedin，checkIstranslated
                        collection = existing_collection
                        logger.info(f"collection {collection_title} translatedin，checktranslated")
                    else:
                        # createtranslatedcollection
                        collection = None
                    
                    # translatedcollectionvideofile path，translateduseprojecttranslateddirectory
                    # translatedmultitranslatedcantranslated'sfiletranslatedformat
                    possible_filenames = [
                        f"{collection_id}_{collection_title}.mp4",
                        f"{collection_title}.mp4",
                        f"collection_{collection_id}.mp4"
                    ]
                    
                    from ..core.path_utils import get_project_directory, get_data_directory
                    project_dir = get_project_directory(project_id)
                    project_collections_dir = project_dir / "output" / "collections"
                    project_collections_dir.mkdir(parents=True, exist_ok=True)
                    
                    video_path = None
                    # translatedinprojectdirectorytranslated
                    for filename in possible_filenames:
                        project_video_path = project_collections_dir / filename
                        if project_video_path.exists():
                            video_path = str(project_video_path)
                            break
                    
                    # iftranslatedprojectdirectorytranslated，translateddirectorytranslated
                    if not video_path:
                        for filename in possible_filenames:
                            legacy_video_path = get_data_directory() / "output" / "collections" / filename
                            if legacy_video_path.exists():
                                # translatedprojectdirectory
                                project_video_path = project_collections_dir / filename
                                import shutil
                                shutil.copy2(legacy_video_path, project_video_path)
                                video_path = str(project_video_path)
                                logger.info(f"translatedcollectionfilefromtranslateddirectorytranslatedprojectdirectory: {legacy_video_path} -> {project_video_path}")
                                break
                    
                    # iftranslatedIstranslated，useprojecttranslatedpath（filecantranslated）
                    if not video_path:
                        video_path = str(project_collections_dir / possible_filenames[0])
                    
                    # translatedformat'sclip_idstranslatedUUIDformat
                    original_clip_ids = collection_data.get('clip_ids', [])
                    uuid_clip_ids = []
                    
                    # fetchprojecttranslatedclip'stranslated（translatedID -> UUID）
                    clips = self.db.query(Clip).filter(Clip.project_id == project_id).all()
                    clip_id_mapping = {}
                    for clip in clips:
                        # fromclip_metadatatranslatedfetchtranslatedID
                        if clip.clip_metadata and 'id' in clip.clip_metadata:
                            original_id = str(clip.clip_metadata['id'])
                            clip_id_mapping[original_id] = clip.id
                    
                    # translatedclip_ids
                    for original_id in original_clip_ids:
                        if str(original_id) in clip_id_mapping:
                            uuid_clip_ids.append(clip_id_mapping[str(original_id)])
                        else:
                            logger.warning(f"translatedclipID {original_id} translated'sUUID")
                    
                    # translatedpath
                    thumbnail_filename = f"{collection_id}_{collection_title}_thumbnail.jpg"
                    thumbnail_path = collections_dir / thumbnail_filename
                    
                    # iftranslatedcollectionnot found，createtranslatedcollection
                    if not collection:
                        collection = Collection(
                            project_id=project_id,
                            name=collection_title,
                            description=collection_data.get('collection_summary', ''),
                            video_path=video_path,
                            export_path=video_path,  # settingsexport_path
                            thumbnail_path=str(thumbnail_path) if thumbnail_path.exists() else None,
                            collection_metadata={
                                'clip_ids': uuid_clip_ids,  # useUUIDformat'sclip_ids
                                'original_clip_ids': original_clip_ids,  # translatedID
                                'collection_type': 'ai_recommended',
                                'original_id': collection_id
                            },
                            status=CollectionStatus.COMPLETED
                        )
                        
                        self.db.add(collection)
                        self.db.flush()  # ensurecollectiontranslatedID
                        logger.info(f"createtranslatedcollection: {collection.id}")
                    else:
                        # updatetranslatedcollection'stranslated
                        if not collection.collection_metadata:
                            collection.collection_metadata = {}
                        collection.collection_metadata.update({
                            'clip_ids': uuid_clip_ids,
                            'original_clip_ids': original_clip_ids,
                            'collection_type': 'ai_recommended',
                            'original_id': collection_id
                        })
                        collection.video_path = video_path
                        collection.export_path = video_path  # settingsexport_path
                        logger.info(f"updatetranslatedcollection: {collection.id}")
                    
                    # translatedcollectionAndclip'stranslated
                    for i, clip_id in enumerate(uuid_clip_ids):
                        try:
                            # checkclipIstranslatedin
                            clip = self.db.query(Clip).filter(Clip.id == clip_id).first()
                            if clip:
                                # checktranslatedIstranslatedin
                                from ..models.collection import clip_collection
                                existing_relation = self.db.execute(
                                    clip_collection.select().where(
                                        clip_collection.c.clip_id == clip_id,
                                        clip_collection.c.collection_id == collection.id
                                    )
                                ).first()
                                
                                if not existing_relation:
                                    # usetranslated
                                    stmt = clip_collection.insert().values(
                                        clip_id=clip_id,
                                        collection_id=collection.id,
                                        order_index=i
                                    )
                                    self.db.execute(stmt)
                                    logger.info(f"translatedcollection {collection.id} Andclip {clip_id} 'stranslated")
                                else:
                                    logger.info(f"collection {collection.id} Andclip {clip_id} 'stranslatedin")
                            else:
                                logger.warning(f"clip {clip_id} not found，skiptranslated")
                        except Exception as e:
                            logger.error(f"translatedcollectionAndcliptranslatedfailed: {e}")
                    
                    synced_count += 1
                    
                except Exception as e:
                    logger.error(f"translatedcollectionfailed: {e}")
                    continue
            
            self.db.commit()
            logger.info(f"project {project_id} translated {synced_count}  collection")
            return synced_count
            
        except Exception as e:
            logger.error(f"translatedcollectiontranslatedfailed: {str(e)}")
            return 0
    
    def sync_project_data(self, project_id: str, project_dir: Path) -> Dict[str, Any]:
        """translatedprojecttranslateddatabase"""
        try:
            logger.info(f"translatedprojecttranslated: {project_id}")
            
            # translatedclipstranslated
            clips_count = self._sync_clips(project_id, project_dir)
            
            # translatedcollectionstranslated
            collections_count = self._sync_collections(project_id, project_dir)
            
            # updateprojecttranslatedinfo
            self._update_project_stats(project_id, clips_count, collections_count)
            
            logger.info(f"projecttranslated: {project_id}, clips: {clips_count}, collections: {collections_count}")
            
            return {
                "success": True,
                "clips_synced": clips_count,
                "collections_synced": collections_count
            }
            
        except Exception as e:
            logger.error(f"translatedprojecttranslatedfailed: {str(e)}")
            raise
    
    def _sync_clips(self, project_id: str, project_dir: Path) -> int:
        """translatedclipstranslated"""
        clips_file = project_dir / "step4_titles.json"
        if not clips_file.exists():
            logger.warning(f"Clipsfile not found: {clips_file}")
            return 0
        
        try:
            with open(clips_file, 'r', encoding='utf-8') as f:
                clips_data = json.load(f)
            
            clips_count = 0
            for clip_data in clips_data:
                # checkIstranslatedin
                existing_clip = self.db.query(Clip).filter(
                    Clip.project_id == project_id,
                    Clip.title == clip_data.get("generated_title")
                ).first()
                
                if existing_clip:
                    logger.info(f"Cliptranslatedin，skip: {clip_data.get('generated_title')}")
                    continue
                
                # createtranslated'scliptranslated
                clip = Clip(
                    project_id=project_id,
                    title=clip_data.get("generated_title", ""),
                    description=clip_data.get("outline", ""),
                    start_time=self._parse_time(clip_data.get("start_time", "00:00:00")),
                    end_time=self._parse_time(clip_data.get("end_time", "00:00:00")),
                    duration=self._calculate_duration(
                        clip_data.get("start_time", "00:00:00"),
                        clip_data.get("end_time", "00:00:00")
                    ),
                    score=clip_data.get("final_score", 0.0),
                    status=ClipStatus.COMPLETED,
                    tags=[],
                    clip_metadata={
                        "outline": clip_data.get("outline"),
                        "content": clip_data.get("content", []),
                        "recommend_reason": clip_data.get("recommend_reason"),
                        "chunk_index": clip_data.get("chunk_index"),
                        "original_id": clip_data.get("id")
                    }
                )
                
                self.db.add(clip)
                clips_count += 1
                logger.info(f"createclip: {clip.title}")
            
            self.db.commit()
            logger.info(f"translated {clips_count}  clips")
            return clips_count
            
        except Exception as e:
            logger.error(f"translatedclipsfailed: {str(e)}")
            self.db.rollback()
            raise
    
    def _sync_collections(self, project_id: str, project_dir: Path) -> int:
        """translatedcollectionstranslateddatabase"""
        collections_file = project_dir / "step5_collections.json"
        if not collections_file.exists():
            logger.warning(f"Collectionsfile not found: {collections_file}")
            return 0
        
        try:
            # translatedcollectionsdirectorypath
            collections_dir = project_dir / "output" / "collections"
            
            with open(collections_file, 'r', encoding='utf-8') as f:
                collections_data = json.load(f)
            
            collections_count = 0
            for collection_data in collections_data:
                # checkIstranslatedin
                existing_collection = self.db.query(Collection).filter(
                    Collection.project_id == project_id,
                    Collection.name == collection_data.get("collection_title")
                ).first()
                
                if existing_collection:
                    logger.info(f"Collectiontranslatedin，skip: {collection_data.get('collection_title')}")
                    continue
                
                # translatedpath
                collection_id = collection_data.get("id", "")
                collection_title = collection_data.get("collection_title", "")
                thumbnail_filename = f"{collection_id}_{collection_title}_thumbnail.jpg"
                thumbnail_path = collections_dir / thumbnail_filename
                
                # createtranslated'scollectiontranslated
                collection = Collection(
                    project_id=project_id,
                    name=collection_data.get("collection_title", ""),
                    description=collection_data.get("collection_summary", ""),
                    theme="default",
                    status=CollectionStatus.COMPLETED,
                    tags=[],
                    thumbnail_path=str(thumbnail_path) if thumbnail_path.exists() else None,
                    collection_metadata={
                        "clip_ids": collection_data.get("clip_ids", []),
                        "original_id": collection_data.get("id"),
                        "collection_type": "ai_recommended"  # translatedAIrecommend
                    }
                )
                
                self.db.add(collection)
                collections_count += 1
                logger.info(f"createcollection: {collection.name}")
            
            self.db.commit()
            logger.info(f"translated {collections_count}  collections")
            return collections_count
            
        except Exception as e:
            logger.error(f"translatedcollectionsfailed: {str(e)}")
            self.db.rollback()
            raise
    
    def _update_project_stats(self, project_id: str, clips_count: int, collections_count: int):
        """updateprojecttranslatedinfo"""
        try:
            project = self.db.query(Project).filter(Project.id == project_id).first()
            if project:
                project.total_clips = clips_count
                project.total_collections = collections_count
                self.db.commit()
                logger.info(f"updateprojecttranslated: clips={clips_count}, collections={collections_count}")
        except Exception as e:
            logger.error(f"updateprojecttranslatedfailed: {str(e)}")
    
    def _parse_time(self, time_str: str) -> float:
        """translatedsecondstranslated"""
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
        except Exception:
            return 0.0
    
    def _calculate_duration(self, start_time: str, end_time: str) -> float:
        """translated"""
        start_seconds = self._parse_time(start_time)
        end_seconds = self._parse_time(end_time)
        return end_seconds - start_seconds

    def _convert_time_to_seconds(self, time_str: str) -> int:
        """translatedsecondstranslated"""
        try:
            # processformat "00:00:00,120" or "00:00:00.120"
            time_str = time_str.replace(',', '.')
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds_parts = parts[2].split('.')
            seconds = int(seconds_parts[0])
            milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
            
            total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
            return int(total_seconds)
        except Exception as e:
            logger.error(f"translatedfailed: {time_str}, error: {e}")
            return 0
    
    def _update_project_status_if_completed(self, project_id: str, project_dir: Path):
        """checkprojectIstranslatedcompletedprocess，iftranslatedIstranslatedupdatestatustranslatedcompleted"""
        try:
            # checkIstranslatedstep6_video_output.jsonfile，thisIsprocessing completed'stranslated
            step6_output_file = project_dir / "output" / "step6_video_output.json"
            
            if step6_output_file.exists():
                # fetchprojecttranslated
                project = self.db.query(Project).filter(Project.id == project_id).first()
                if project and project.status != ProjectStatus.COMPLETED:
                    # translatedstep6translatedfilefetchtranslatedinfo
                    try:
                        with open(step6_output_file, 'r', encoding='utf-8') as f:
                            step6_output = json.load(f)
                        
                        # updateprojectstatusAndtranslatedinfo
                        project.status = ProjectStatus.COMPLETED
                        project.total_clips = step6_output.get("clips_count", 0)
                        project.total_collections = step6_output.get("collections_count", 0)
                        project.completed_at = datetime.now()
                        
                        self.db.commit()
                        logger.info(f"project {project_id} statustranslatedupdatetranslatedcompleted，cliptranslated: {project.total_clips}, collectiontranslated: {project.total_collections}")
                        
                    except Exception as e:
                        logger.error(f"translatedstep6translatedfilefailed: {e}")
                        # translatedfailed，translatedcompleted
                        project.status = ProjectStatus.COMPLETED
                        project.completed_at = datetime.now()
                        self.db.commit()
                        logger.info(f"project {project_id} statustranslatedupdatetranslatedcompleted（translatedinfo）")
                        
        except Exception as e:
            logger.error(f"updateprojectstatusfailed: {e}")
