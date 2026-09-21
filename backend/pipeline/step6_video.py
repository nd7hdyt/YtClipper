"""
Step 6: videotranslated - translatedvideoclip
"""
import json
import logging
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

# importdependencies
from ..utils.video_processor import VideoProcessor
from ..core.shared_config import METADATA_DIR, CLIPS_DIR, COLLECTIONS_DIR

logger = logging.getLogger(__name__)

class VideoGenerator:
    """videotranslated"""
    
    def __init__(self, clips_dir: Optional[str] = None, collections_dir: Optional[str] = None, metadata_dir: Optional[str] = None):
        # translateduseprojecttranslateddirectory，translatedusetranslateddirectorytranslated
        if not clips_dir:
            raise ValueError("clips_dir translatedIstranslated's，translatedusetranslatedpath")
        if not collections_dir:
            raise ValueError("collections_dir translatedIstranslated's，translatedusetranslatedpath")
        
        self.clips_dir = Path(clips_dir)
        self.collections_dir = Path(collections_dir)
        self.metadata_dir = Path(metadata_dir) if metadata_dir else METADATA_DIR
        
        # ensuredirectorytranslatedin
        self.clips_dir.mkdir(parents=True, exist_ok=True)
        self.collections_dir.mkdir(parents=True, exist_ok=True)
        
        # createVideoProcessortranslated，translateduseprojecttranslatedpath
        self.video_processor = VideoProcessor(clips_dir=str(self.clips_dir), collections_dir=str(self.collections_dir))
    
    def generate_clips(self, clips_with_titles: List[Dict], input_video: Path) -> List[Path]:
        """
        translatedclipvideo
        
        Args:
            clips_with_titles: translated'stranslated
            input_video: translatedvideopath
            
        Returns:
            translated'sclipvideopathlist
        """
        logger.info("translatedclipvideo...")
        
        # translatedcliptranslated
        clips_data = []
        for clip in clips_with_titles:
            clips_data.append({
                'id': clip['id'],
                'title': clip.get('generated_title', f"translated_{clip['id']}"),
                'start_time': clip['start_time'],
                'end_time': clip['end_time']
            })
        
        # translatedclip
        successful_clips = self.video_processor.batch_extract_clips(input_video, clips_data)
        
        logger.info(f"clipvideotranslated，translated{len(successful_clips)} clip")
        return successful_clips
    
    def generate_collections(self, collections_data: List[Dict]) -> List[Dict]:
        """
        translatedcollectionvideo
        
        Args:
            collections_data: collectiontranslated
            
        Returns:
            translated'scollectioninfolist，PackageincludevideopathAndtranslatedpath
        """
        logger.info("translatedcollectionvideo...")
        
        # translatedcollectionvideoAndtranslated
        successful_collections = self.video_processor.create_collections_from_metadata(collections_data)
        
        logger.info(f"collectionvideotranslated，translated{len(successful_collections)} collection")
        return successful_collections
    
    def save_clip_metadata(self, clips_with_titles: List[Dict], output_path: Optional[Path] = None) -> Path:
        """
        translated'scliptranslatedclips_metadata.json
        
        Args:
            clips_with_titles: translated'stranslated（translatedstep4）
            output_path: translatedpath，defaulttranslatedclips_metadata.json
            
        Returns:
            translated'sfile path
            
        Note:
            translated'sIstranslated'scliptranslated，Packageincludevideotranslated'stranslatedinfo。
            andstep4'sstep4_titles.jsontranslated，thistranslated'sIsusetranslatedfrontendtranslated'stranslated。
        """
        if output_path is None:
            output_path = self.metadata_dir / "clips_metadata.json"
        
        # ensuredirectorytranslatedin
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # translated
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clips_with_titles, f, ensure_ascii=False, indent=2)
        
        logger.info(f"cliptranslated: {output_path}")
        return output_path
    
    def save_collection_metadata(self, collections_data: List[Dict], output_path: Optional[Path] = None) -> Path:
        """
        translatedcollectiontranslated
        
        Args:
            collections_data: collectiontranslated
            output_path: translatedpath
            
        Returns:
            translated'sfile path
        """
        if output_path is None:
            output_path = self.metadata_dir / "collections_metadata.json"
        
        # ensuredirectorytranslatedin
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # translated
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(collections_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"collectiontranslated: {output_path}")
        return output_path

def run_step6_video(clips_with_titles_path: Path, collections_path: Path, 
                   input_video: Path, output_dir: Optional[Path] = None, 
                   clips_dir: Optional[str] = None, collections_dir: Optional[str] = None, 
                   metadata_dir: Optional[str] = None) -> Dict:
    """
    translatedStep 6: videotranslated
    
    Args:
        clips_with_titles_path: translated'stranslatedfile path
        collections_path: collectionfile path
        input_video: translatedvideopath
        output_dir: translateddirectory
        
    Returns:
        translatedinfo
    """
    # translated
    with open(clips_with_titles_path, 'r', encoding='utf-8') as f:
        clips_with_titles = json.load(f)
    
    with open(collections_path, 'r', encoding='utf-8') as f:
        collections_data = json.load(f)
    
    # createvideotranslated
    generator = VideoGenerator(clips_dir=clips_dir, collections_dir=collections_dir, metadata_dir=metadata_dir)
    
    # translatedclipvideo
    successful_clips = generator.generate_clips(clips_with_titles, input_video)
    
    # translatedcollectionvideo
    successful_collections = generator.generate_collections(collections_data)
    
    # translatedprojectdirectory
    # translated：clips_metadata.jsoninthistranslated，Packageincludetranslated'scliptranslated（Packageincludevideopathetc.info）
    # thisandstep4'sstep4_titles.jsontranslated，step4translated'stranslated
    if metadata_dir:
        project_metadata_dir = Path(metadata_dir)
        generator.save_clip_metadata(clips_with_titles, project_metadata_dir / "clips_metadata.json")
        generator.save_collection_metadata(collections_data, project_metadata_dir / "collections_metadata.json")
    else:
        generator.save_clip_metadata(clips_with_titles)
        generator.save_collection_metadata(collections_data)
    
    # returntranslatedinfo
    result = {
        'clips_generated': len(successful_clips),
        'collections_generated': len(successful_collections),
        'clip_paths': [str(path) for path in successful_clips],
        'collection_paths': [collection['video_path'] for collection in successful_collections],
        'collection_thumbnails': [collection['thumbnail_path'] for collection in successful_collections if collection['thumbnail_path']],
        'collections_info': successful_collections  # Packageincludetranslated'scollectioninfo
    }
    
    logger.info(f"videotranslated: {result['clips_generated']} clip, {result['collections_generated']} collection")
    
    # translatedfile
    if output_dir is not None:
        output_path = output_dir / "step6_video_output.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"step6translated: {output_path}")
    
    return result