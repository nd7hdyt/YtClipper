"""
Step 3: Highlight scoring - score each topic for quality and keep the high-quality clips
"""
import json
import logging
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from collections import defaultdict

# Import dependencies
from ..utils.llm_client import LLMClient
from ..utils.text_processor import TextProcessor
from ..core.shared_config import PROMPT_FILES, METADATA_DIR, MIN_SCORE_THRESHOLD

logger = logging.getLogger(__name__)

# Explicit CLI `--min-score` style override: highest priority. None = use the value
# saved on the settings page, falling back to MIN_SCORE_THRESHOLD
MIN_SCORE_OVERRIDE: Optional[float] = None


def resolve_min_score_threshold() -> float:
    """Explicit override > settings-page "minimum score threshold" (settings.json,
    hot-reloaded) > code default 0.7. The settings-page value used to only tweak
    the API process memory and was never read by the pipeline."""
    if MIN_SCORE_OVERRIDE is not None:
        return float(MIN_SCORE_OVERRIDE)
    try:
        from ..core.llm_manager import get_llm_manager
        value = get_llm_manager().get_processing_setting("min_score_threshold")
        if value is not None:
            value = float(value)
            if 0.0 < value <= 1.0:
                return value
            logger.warning(f"Settings-page min score threshold {value} is outside (0, 1], using default {MIN_SCORE_THRESHOLD}")
    except Exception as e:  # noqa: BLE001
        logger.debug(f"Failed to read the settings-page score threshold, using default: {e}")
    return float(MIN_SCORE_THRESHOLD)

class ClipScorer:
    """Highlight scorer"""
    
    def __init__(self, prompt_files: Dict = None, metadata_dir: Path = None):
        self.llm_client = LLMClient()
        self.text_processor = TextProcessor()
        self.metadata_dir = Path(metadata_dir) if metadata_dir else None
        
        # Load the prompt
        prompt_files_to_use = prompt_files if prompt_files is not None else PROMPT_FILES
        with open(prompt_files_to_use['recommendation'], 'r', encoding='utf-8') as f:
            self.recommendation_prompt = f.read()

        from .quality import load_srt_chunks
        self._srt_entries = load_srt_chunks(self.metadata_dir) if self.metadata_dir else []
    
    def score_clips(self, timeline_data: List[Dict]) -> List[Dict]:
        """
        Score the clips (new version: batched per chunk with LLM-based holistic scoring)
        """
        if not timeline_data:
            logger.warning("Timeline data is empty, nothing to score")
            return []
            
        logger.info(f"Batch-scoring {len(timeline_data)} clips...")
        
        # 1. Group all timeline items by chunk_index
        timeline_by_chunk = defaultdict(list)
        for item in timeline_data:
            chunk_index = item.get('chunk_index')
            if chunk_index is not None:
                timeline_by_chunk[chunk_index].append(item)
            else:
                logger.warning(f"  > Topic '{item.get('outline', 'unknown')}' is missing chunk_index, skipping.")
        
        all_scored_clips = []
        # 2. Process the topics of each chunk in batch
        for chunk_index, chunk_items in timeline_by_chunk.items():
            logger.info(f"Processing chunk {chunk_index} with {len(chunk_items)} topics...")
            try:
                # 3. Batched scoring via the LLM
                scored_chunk_items = self._get_llm_evaluation(chunk_items)
                
                if scored_chunk_items:
                    all_scored_clips.extend(scored_chunk_items)
                else:
                    logger.warning(f"Chunk {chunk_index} LLM evaluation came back empty, skipping.")

            except Exception as e:
                logger.error(f"  > Error scoring chunk {chunk_index}: {str(e)}")
                continue

        # 4. Sort all results by final score
        if all_scored_clips:
            all_scored_clips.sort(key=lambda x: x.get('final_score', 0), reverse=True)
            # Keep the stable IDs assigned in Step 2, do not reassign
            logger.info("Sorted by score, keeping the original stable IDs")
            
            # Sort by ID last to restore time order
            all_scored_clips.sort(key=lambda x: int(x.get('id', 0)))
            logger.info("Sorted by ID, time order preserved")
                
        logger.info("All clips scored")
        return all_scored_clips
    
    def _excerpt(self, clip: Dict) -> str:
        if not self._srt_entries:
            return ""
        from .quality import excerpt_between, to_seconds
        try:
            return excerpt_between(self._srt_entries, to_seconds(clip["start_time"]), to_seconds(clip["end_time"]))
        except (KeyError, ValueError, TypeError):
            return ""

    def _get_llm_evaluation(self, clips: List[Dict]) -> List[Dict]:
        """
        Batched scoring via the LLM, adding final_score and recommend_reason to each clip.
        When counts mismatch, align by outline instead of dropping the whole chunk (#11).
        """
        from .quality import align_scores

        try:
            input_for_llm = [
                {
                    "outline": clip.get('outline'),
                    "content": clip.get('content'),
                    "start_time": clip.get('start_time'),
                    "end_time": clip.get('end_time'),
                    "transcript": self._excerpt(clip),
                } for clip in clips
            ]

            response = self.llm_client.call_with_retry(self.recommendation_prompt, input_for_llm)
            parsed_list = self.llm_client.parse_json_response(response)
            scored, stats = align_scores(clips, parsed_list)
            logger.info(f"  > Score alignment: {stats['matched']} matched, {stats['fallback']} fallback")
            return scored

        except Exception as e:
            logger.error(f"Batched LLM evaluation failed: {e}")
            scored, _ = align_scores(clips, [])
            return scored

    def save_scores(self, scored_clips: List[Dict], output_path: Path):
        """Save the scoring results"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(scored_clips, f, ensure_ascii=False, indent=2)
        logger.info(f"Scoring results saved to: {output_path}")

def run_step3_scoring(timeline_path: Path, metadata_dir: Path = None, output_path: Optional[Path] = None, prompt_files: Dict = None) -> List[Dict]:
    """
    Run Step 3: highlight scoring and filtering
    
    Args:
        timeline_path: path to the timeline file
        output_path: output file path
        prompt_files: custom prompt files
        
    Returns:
        list of high-scoring clips
    """
    # Load the timeline data
    with open(timeline_path, 'r', encoding='utf-8') as f:
        timeline_data = json.load(f)
    
    if metadata_dir is None:
        metadata_dir = METADATA_DIR

    from .quality import load_profile, select_clips, save_report

    scorer = ClipScorer(prompt_files, metadata_dir=metadata_dir)
    scored_clips = scorer.score_clips(timeline_data)

    profile = load_profile(metadata_dir)
    threshold = resolve_min_score_threshold()
    high_score_clips, select_info = select_clips(scored_clips, threshold, profile)
    select_info["threshold"] = threshold
    save_report({"step3": select_info}, metadata_dir)
    logger.info(
        f"Score filtering: {select_info['candidates']} candidates → {select_info['selected']} kept"
        f" (threshold {threshold}, fallback top-up {select_info['fallback_selected']})"
    )

    all_scored_path = metadata_dir / "step3_all_scored.json"
    scorer.save_scores(scored_clips, all_scored_path)

    if output_path is None:
        output_path = metadata_dir / "step3_high_score_clips.json"
    scorer.save_scores(high_score_clips, output_path)

    return high_score_clips