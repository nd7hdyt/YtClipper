"""
Step 4: translated - translated'stranslated
"""
import json
import logging
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from collections import defaultdict

# importdependencies
from ..utils.llm_client import LLMClient
from ..utils.text_processor import TextProcessor
from ..core.shared_config import PROMPT_FILES, METADATA_DIR

logger = logging.getLogger(__name__)

class TitleGenerator:
    """translated"""
    
    def __init__(self, metadata_dir: Optional[Path] = None, prompt_files: Dict = None):
        self.llm_client = LLMClient()
        self.text_processor = TextProcessor()
        
        # translated
        prompt_files_to_use = prompt_files if prompt_files is not None else PROMPT_FILES
        with open(prompt_files_to_use['title'], 'r', encoding='utf-8') as f:
            self.title_prompt = f.read()
        
        # usetranslated'smetadata_dirordefaulttranslated
        if metadata_dir is None:
            metadata_dir = METADATA_DIR
        self.metadata_dir = metadata_dir
        self.llm_raw_output_dir = self.metadata_dir / "step4_llm_raw_output"
    
    def generate_titles(self, high_score_clips: List[Dict]) -> List[Dict]:
        """
        translatedcliptranslated (translated：bytranslatedprocess，translatedcache)
        """
        if not high_score_clips:
            return []
            
        logger.info(f"translated {len(high_score_clips)}  translated...")
        
        self.llm_raw_output_dir.mkdir(parents=True, exist_ok=True)
        
        clips_by_chunk = defaultdict(list)
        for clip in high_score_clips:
            clips_by_chunk[clip.get('chunk_index', 0)].append(clip)
            
        all_clips_with_titles = []
        for chunk_index, chunk_clips in clips_by_chunk.items():
            logger.info(f"processtranslated {chunk_index}，translatedPackageinclude {len(chunk_clips)}  translated...")
            
            try:
                logger.info(f"  > translatedcallAPItranslated...")
                input_for_llm = [
                    {
                        "id": clip.get('id'),
                        "title": clip.get('outline'),  # useoutlinetranslatedtitle
                        "content": clip.get('content'),
                        "recommend_reason": clip.get('recommend_reason')
                    } for clip in chunk_clips
                ]
                
                raw_response = self.llm_client.call_with_retry(self.title_prompt, input_for_llm)
                
                if raw_response:
                    # translatedLLMtranslatedusetranslated（translatedusetranslatedcache）
                    llm_cache_path = self.llm_raw_output_dir / f"chunk_{chunk_index}.txt"
                    with open(llm_cache_path, 'w', encoding='utf-8') as f:
                        f.write(raw_response)
                    logger.info(f"  > LLMtranslated {llm_cache_path}")
                    titles_map = self.llm_client.parse_json_response(raw_response)
                else:
                    titles_map = {}
                
                if not isinstance(titles_map, dict):
                    logger.warning(f"  > LLMreturn'stranslatedIsone translated: {titles_map}，skiptranslated。")
                    # translatedfailed，translated translated，translated
                    all_clips_with_titles.extend(chunk_clips)
                    continue

                for clip in chunk_clips:
                    clip_id = clip.get('id')
                    generated_title = titles_map.get(clip_id)
                    if generated_title and isinstance(generated_title, str):
                        clip['generated_title'] = generated_title
                        # translatedfetchoutlinetranslatedusetranslatedlogstranslated
                        outline = clip.get('outline', {})
                        if isinstance(outline, dict):
                            title = outline.get('title', 'translated')
                        else:
                            title = str(outline)
                        logger.info(f"  > translated {clip_id} ('{title[:20]}...') translated: {generated_title}")
                    else:
                        clip['generated_title'] = clip.get('outline', f"translated_{clip_id}")  # useoutlinetranslatedfallback
                        logger.warning(f"  > translated {clip_id} translatedortranslated，usetranslatedoutline")
                
                all_clips_with_titles.extend(chunk_clips)

            except Exception as e:
                logger.error(f"  > translated {chunk_index} translated: {e}")
                # translated，translatedaddtranslated
                all_clips_with_titles.extend(chunk_clips)
                continue
                
        logger.info("translated")
        return all_clips_with_titles
        
    def save_clips_with_titles(self, clips_with_titles: List[Dict], output_path: Path):
        """translated'stranslated"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clips_with_titles, f, ensure_ascii=False, indent=2)
        logger.info(f"translated'stranslated: {output_path}")

def run_step4_title(high_score_clips_path: Path, output_path: Optional[Path] = None, metadata_dir: Optional[str] = None, prompt_files: Dict = None) -> List[Dict]:
    """
    translatedStep 4: translated
    
    Args:
        high_score_clips_path: translatedclipfile path
        output_path: translatedfile path，defaulttranslatedstep4_titles.json
        metadata_dir: translateddirectorypath
        prompt_files: translatedfile
        
    Returns:
        translated'scliplist
        
    Note:
        translatedsteptranslatedstep4_titles.jsonfile，Packageincludetranslated'stranslated。
        clips_metadata.jsonfiletranslatedinstep6translatedonetranslated，translated。
    """
    # translated
    with open(high_score_clips_path, 'r', encoding='utf-8') as f:
        high_score_clips = json.load(f)
        
    # createtranslated
    if metadata_dir is None:
        metadata_dir = METADATA_DIR
    title_generator = TitleGenerator(metadata_dir=Path(metadata_dir), prompt_files=prompt_files)
    
    # translated
    clips_with_titles = title_generator.generate_titles(high_score_clips)
    
    # translatedpath
    if metadata_dir is None:
        metadata_dir = METADATA_DIR
    
    if output_path is None:
        output_path = Path(metadata_dir) / "step4_titles.json"
        
    # translated'stranslatedstep4_titles.json
    title_generator.save_clips_with_titles(clips_with_titles, output_path)
    
    # translated：clips_metadata.jsontranslatedinstep6translated，thistranslated
    # thistranslatedcantranslatedAndtranslated
    
    return clips_with_titles