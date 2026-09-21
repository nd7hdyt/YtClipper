"""
Step 4: titlegenerate - ENgenerateENtitle
"""
import json
import logging
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from collections import defaultdict

# EN
from ..utils.llm_client import LLMClient
from ..utils.text_processor import TextProcessor
from ..core.shared_config import PROMPT_FILES, METADATA_DIR

logger = logging.getLogger(__name__)

class TitleGenerator:
    """titlegenerateEN"""
    
    def __init__(self, metadata_dir: Optional[Path] = None, prompt_files: Dict = None):
        self.llm_client = LLMClient()
        self.text_processor = TextProcessor()
        
        # loadhintEN
        prompt_files_to_use = prompt_files if prompt_files is not None else PROMPT_FILES
        with open(prompt_files_to_use['title'], 'r', encoding='utf-8') as f:
            self.title_prompt = f.read()
        
        # useENmetadata_dirEN
        if metadata_dir is None:
            metadata_dir = METADATA_DIR
        self.metadata_dir = metadata_dir
        self.llm_raw_output_dir = self.metadata_dir / "step4_llm_raw_output"
    
    def generate_titles(self, high_score_clips: List[Dict]) -> List[Dict]:
        """
        ENclipgeneratetitle (EN：ENprocessing，ENcache)
        """
        if not high_score_clips:
            return []
            
        logger.info(f"startEN {len(high_score_clips)} ENtitlegenerate...")
        
        self.llm_raw_output_dir.mkdir(parents=True, exist_ok=True)
        
        clips_by_chunk = defaultdict(list)
        for clip in high_score_clips:
            clips_by_chunk[clip.get('chunk_index', 0)].append(clip)
            
        all_clips_with_titles = []
        for chunk_index, chunk_clips in clips_by_chunk.items():
            logger.info(f"processingEN {chunk_index}，amongEN {len(chunk_clips)} EN...")
            
            try:
                logger.info(f"  > startcallAPIgeneratetitle...")
                input_for_llm = [
                    {
                        "id": clip.get('id'),
                        "title": clip.get('outline'),  # useoutlineENtitle
                        "content": clip.get('content'),
                        "recommend_reason": clip.get('recommend_reason')
                    } for clip in chunk_clips
                ]
                
                raw_response = self.llm_client.call_with_retry(self.title_prompt, input_for_llm)
                
                if raw_response:
                    # saveLLMENresponseEN（ENcache）
                    llm_cache_path = self.llm_raw_output_dir / f"chunk_{chunk_index}.txt"
                    with open(llm_cache_path, 'w', encoding='utf-8') as f:
                        f.write(raw_response)
                    logger.info(f"  > LLMENresponseENsaveEN {llm_cache_path}")
                    titles_map = self.llm_client.parse_json_response(raw_response)
                else:
                    titles_map = {}
                
                if not isinstance(titles_map, dict):
                    logger.warning(f"  > LLMreturnENtitleEN: {titles_map}，EN。")
                    # ENfailed，EN，EN
                    all_clips_with_titles.extend(chunk_clips)
                    continue

                for clip in chunk_clips:
                    clip_id = clip.get('id')
                    generated_title = titles_map.get(clip_id)
                    if generated_title and isinstance(generated_title, str):
                        clip['generated_title'] = generated_title
                        # ENfetchoutlinetitleENlogEN
                        outline = clip.get('outline', {})
                        if isinstance(outline, dict):
                            title = outline.get('title', 'ENtitle')
                        else:
                            title = str(outline)
                        logger.info(f"  > EN {clip_id} ('{title[:20]}...') generatetitle: {generated_title}")
                    else:
                        clip['generated_title'] = clip.get('outline', f"EN_{clip_id}")  # useoutlineENfallback
                        logger.warning(f"  > EN {clip_id} ENparsetitle，useENoutline")
                
                all_clips_with_titles.extend(chunk_clips)

            except Exception as e:
                logger.error(f"  > EN {chunk_index} generatetitleEN: {e}")
                # EN，EN
                all_clips_with_titles.extend(chunk_clips)
                continue
                
        logger.info("allENtitlegenerateEN")
        return all_clips_with_titles
        
    def save_clips_with_titles(self, clips_with_titles: List[Dict], output_path: Path):
        """saveENtitleEN"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clips_with_titles, f, ensure_ascii=False, indent=2)
        logger.info(f"ENtitleENsaveEN: {output_path}")

def run_step4_title(high_score_clips_path: Path, output_path: Optional[Path] = None, metadata_dir: Optional[str] = None, prompt_files: Dict = None) -> List[Dict]:
    """
    runStep 4: titlegenerate
    
    Args:
        high_score_clips_path: ENclipfilepath
        output_path: ENfilepath，ENstep4_titles.json
        metadata_dir: ENdirectorypath
        prompt_files: ENhintENfile
        
    Returns:
        ENtitleENclipEN
        
    Note:
        ENsavestep4_titles.jsonfile，ENtitleEN。
        clips_metadata.jsonfileENstep6ENsave，ENsave。
    """
    # loadEN
    with open(high_score_clips_path, 'r', encoding='utf-8') as f:
        high_score_clips = json.load(f)
        
    # createtitlegenerateEN
    if metadata_dir is None:
        metadata_dir = METADATA_DIR
    title_generator = TitleGenerator(metadata_dir=Path(metadata_dir), prompt_files=prompt_files)
    
    # generatetitle
    clips_with_titles = title_generator.generate_titles(high_score_clips)
    
    # ENpath
    if metadata_dir is None:
        metadata_dir = METADATA_DIR
    
    if output_path is None:
        output_path = Path(metadata_dir) / "step4_titles.json"
        
    # saveENtitleENstep4_titles.json
    title_generator.save_clips_with_titles(clips_with_titles, output_path)
    
    # EN：clips_metadata.jsonENstep6ENsave，ENsave
    # ENcanENsaveEN
    
    return clips_with_titles