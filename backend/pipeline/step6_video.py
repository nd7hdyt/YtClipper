"""
Step 6: videogenerate - ENresultgenerateENvideoclip
"""
import json
import logging
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

# EN
from ..utils.video_processor import VideoProcessor
from ..core.shared_config import METADATA_DIR, CLIPS_DIR, COLLECTIONS_DIR

logger = logging.getLogger(__name__)

class VideoGenerator:
    """videogenerateEN"""
    
    def __init__(self, clips_dir: Optional[str] = None, collections_dir: Optional[str] = None, metadata_dir: Optional[str] = None):
        # ENuseprojectENdirectory，ENuseENdirectoryEN
        if not clips_dir:
            raise ValueError("clips_dir parametersEN，ENuseENpath")
        if not collections_dir:
            raise ValueError("collections_dir parametersEN，ENuseENpath")
        
        self.clips_dir = Path(clips_dir)
        self.collections_dir = Path(collections_dir)
        self.metadata_dir = Path(metadata_dir) if metadata_dir else METADATA_DIR
        
        # ENdirectoryEN
        self.clips_dir.mkdir(parents=True, exist_ok=True)
        self.collections_dir.mkdir(parents=True, exist_ok=True)
        
        # createVideoProcessorEN，ENuseprojectENpath
        self.video_processor = VideoProcessor(clips_dir=str(self.clips_dir), collections_dir=str(self.collections_dir))
    
    def generate_clips(self, clips_with_titles: List[Dict], input_video: Path) -> List[Path]:
        """
        generateclipvideo
        
        Args:
            clips_with_titles: ENtitleEN
            input_video: ENvideopath
            
        Returns:
            generateENclipvideopathEN
        """
        logger.info("startgenerateclipvideo...")
        
        # ENclipEN
        clips_data = []
        for clip in clips_with_titles:
            clips_data.append({
                'id': clip['id'],
                'title': clip.get('generated_title', f"EN_{clip['id']}"),
                'start_time': clip['start_time'],
                'end_time': clip['end_time']
            })
        
        # ENgenerateclip
        successful_clips = self.video_processor.batch_extract_clips(input_video, clips_data)
        
        logger.info(f"clipvideogenerateEN，EN{len(successful_clips)}ENclip")
        return successful_clips
    
    def generate_collections(self, collections_data: List[Dict]) -> List[Dict]:
        """
        generatecollectionvideo
        
        Args:
            collections_data: collectionEN
            
        Returns:
            generateENcollectionEN，ENvideopathENpath
        """
        logger.info("startgeneratecollectionvideo...")
        
        # generatecollectionvideoEN
        successful_collections = self.video_processor.create_collections_from_metadata(collections_data)
        
        logger.info(f"collectionvideogenerateEN，EN{len(successful_collections)}ENcollection")
        return successful_collections
    
    def save_clip_metadata(self, clips_with_titles: List[Dict], output_path: Optional[Path] = None) -> Path:
        """
        saveENclipENclips_metadata.json
        
        Args:
            clips_with_titles: ENtitleEN（ENstep4）
            output_path: ENpath，ENclips_metadata.json
            
        Returns:
            saveENfilepath
            
        Note:
            ENsaveENclipEN，ENvideogenerateEN。
            ENstep4ENstep4_titles.jsonEN，ENsaveEN。
        """
        if output_path is None:
            output_path = self.metadata_dir / "clips_metadata.json"
        
        # ENdirectoryEN
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # saveEN
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clips_with_titles, f, ensure_ascii=False, indent=2)
        
        logger.info(f"clipENsaveEN: {output_path}")
        return output_path
    
    def save_collection_metadata(self, collections_data: List[Dict], output_path: Optional[Path] = None) -> Path:
        """
        savecollectionEN
        
        Args:
            collections_data: collectionEN
            output_path: ENpath
            
        Returns:
            saveENfilepath
        """
        if output_path is None:
            output_path = self.metadata_dir / "collections_metadata.json"
        
        # ENdirectoryEN
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # saveEN
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(collections_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"collectionENsaveEN: {output_path}")
        return output_path

def run_step6_video(clips_with_titles_path: Path, collections_path: Path, 
                   input_video: Path, output_dir: Optional[Path] = None, 
                   clips_dir: Optional[str] = None, collections_dir: Optional[str] = None, 
                   metadata_dir: Optional[str] = None) -> Dict:
    """
    runStep 6: videoEN
    
    Args:
        clips_with_titles_path: ENtitleENfilepath
        collections_path: collectionfilepath
        input_video: ENvideopath
        output_dir: ENdirectory
        
    Returns:
        generateresultEN
    """
    # loadEN
    with open(clips_with_titles_path, 'r', encoding='utf-8') as f:
        clips_with_titles = json.load(f)
    
    with open(collections_path, 'r', encoding='utf-8') as f:
        collections_data = json.load(f)
    
    # createvideogenerateEN
    generator = VideoGenerator(clips_dir=clips_dir, collections_dir=collections_dir, metadata_dir=metadata_dir)
    
    # generateclipvideo
    successful_clips = generator.generate_clips(clips_with_titles, input_video)
    
    # generatecollectionvideo
    successful_collections = generator.generate_collections(collections_data)
    
    # saveENprojectdirectory
    # EN：clips_metadata.jsonENsave，ENclipEN（ENvideopathEN）
    # ENstep4ENstep4_titles.jsonEN，step4ENsaveENtitleEN
    if metadata_dir:
        project_metadata_dir = Path(metadata_dir)
        generator.save_clip_metadata(clips_with_titles, project_metadata_dir / "clips_metadata.json")
        generator.save_collection_metadata(collections_data, project_metadata_dir / "collections_metadata.json")
    else:
        generator.save_clip_metadata(clips_with_titles)
        generator.save_collection_metadata(collections_data)
    
    # returnresultEN
    result = {
        'clips_generated': len(successful_clips),
        'collections_generated': len(successful_collections),
        'clip_paths': [str(path) for path in successful_clips],
        'collection_paths': [collection['video_path'] for collection in successful_collections],
        'collection_thumbnails': [collection['thumbnail_path'] for collection in successful_collections if collection['thumbnail_path']],
        'collections_info': successful_collections  # ENcollectionEN
    }
    
    logger.info(f"videogenerateEN: {result['clips_generated']}ENclip, {result['collections_generated']}ENcollection")
    
    # saveresultENfile
    if output_dir is not None:
        output_path = output_dir / "step6_video_output.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"EN6resultENsaveEN: {output_path}")
    
    return result