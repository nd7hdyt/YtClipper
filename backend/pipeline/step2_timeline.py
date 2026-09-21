"""
Step 2: Timeline extraction - locate concrete time ranges for each outline topic
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
from ..core.shared_config import PROMPT_FILES, METADATA_DIR

logger = logging.getLogger(__name__)

class TimelineExtractor:
    """Extract precise timelines from the outline and SRT subtitles"""
    
    def __init__(self, metadata_dir: Path = None, prompt_files: Dict = None):
        self.llm_client = LLMClient()
        self.text_processor = TextProcessor()
        
        # Use the provided metadata_dir or the default
        if metadata_dir is None:
            metadata_dir = METADATA_DIR
        self.metadata_dir = metadata_dir
        
        # Load the prompt
        prompt_files_to_use = prompt_files if prompt_files is not None else PROMPT_FILES
        with open(prompt_files_to_use['timeline'], 'r', encoding='utf-8') as f:
            self.timeline_prompt = f.read()
            
        # SRT chunk directory
        self.srt_chunks_dir = self.metadata_dir / "step1_srt_chunks"
        self.timeline_chunks_dir = self.metadata_dir / "step2_timeline_chunks"
        self.llm_raw_output_dir = self.metadata_dir / "step2_llm_raw_output"

    def extract_timeline(self, outlines: List[Dict]) -> List[Dict]:
        """
        Extract topic time ranges.
        New in this version:
        - Based on pre-chunked SRT
        - Batched per chunk
        - Raw LLM responses cached to avoid repeated calls
        - Per-chunk results saved as intermediate files for robustness
        """
        logger.info("Extracting topic time ranges...")
        
        if not outlines:
            logger.warning("Outline data is empty, cannot extract timeline.")
            return []

        if not self.srt_chunks_dir.exists():
            logger.error(f"SRT chunk directory not found: {self.srt_chunks_dir}. Please run Step 1 first.")
            return []

        # 1. Create the directories needed for this step
        self.timeline_chunks_dir.mkdir(parents=True, exist_ok=True)
        self.llm_raw_output_dir.mkdir(parents=True, exist_ok=True)

        # Append the duration profile to the prompt (overrides the hardcoded
        # 90s / 3-6min rules written in the prompt file)
        from .quality import load_profile
        profile = load_profile(self.metadata_dir)
        timeline_prompt = self.timeline_prompt + (profile.prompt_hint() if profile else "")

        # 2. Group all outlines by chunk_index
        outlines_by_chunk = defaultdict(list)
        for outline in outlines:
            chunk_index = outline.get('chunk_index')
            if chunk_index is not None:
                outlines_by_chunk[chunk_index].append(outline)
            else:
                logger.warning(f"  > Topic '{outline.get('title', 'unknown')}' is missing chunk_index, skipping.")

        all_timeline_data = []
        # 3. Process each chunk in batch and save the result as a standalone JSON file
        for chunk_index, chunk_outlines in outlines_by_chunk.items():
            logger.info(f"Processing chunk {chunk_index} with {len(chunk_outlines)} topics...")
            
            # Always reprocess, never use the cache
            chunk_output_path = self.timeline_chunks_dir / f"chunk_{chunk_index}.json"

            try:
                # First load the matching SRT chunk file; needed with or without cache
                srt_chunk_path = self.srt_chunks_dir / f"chunk_{chunk_index}.json"
                if not srt_chunk_path.exists():
                    logger.warning(f"  > Matching SRT chunk file not found: {srt_chunk_path}, skipping the whole chunk.")
                    continue
                
                with open(srt_chunk_path, 'r', encoding='utf-8') as f:
                    srt_chunk_data = json.load(f)

                if not srt_chunk_data:
                    logger.warning(f"  > SRT chunk file is empty: {srt_chunk_path}, skipping the whole chunk.")
                    continue

                # Get the time range info
                chunk_start_time = srt_chunk_data[0]['start_time']
                chunk_end_time = srt_chunk_data[-1]['end_time']

                raw_response = ""
                llm_cache_path = self.llm_raw_output_dir / f"chunk_{chunk_index}.txt"

                if llm_cache_path.exists():
                    logger.info(f"  > Found cached raw LLM response for chunk {chunk_index}, reading it directly.")
                    with open(llm_cache_path, 'r', encoding='utf-8') as f:
                        raw_response = f.read()
                else:
                    logger.info(f"  > No LLM cache found, calling the API...")
                    
                    # Build the SRT text for the LLM
                    srt_text_for_prompt = ""
                    for sub in srt_chunk_data:
                        srt_text_for_prompt += f"{sub['index']}\\n{sub['start_time']} --> {sub['end_time']}\\n{sub['text']}\\n\\n"
                    
                    # Prepare a "clean" input for the LLM with only what it needs
                    llm_input_outlines = [
                        {"title": o.get("title"), "subtopics": o.get("subtopics")}
                        for o in chunk_outlines
                    ]

                    input_data = {
                        "outline": llm_input_outlines,  # use the clean data
                        "srt_text": srt_text_for_prompt
                    }
                    
                    # Call the LLM for the raw response, with retries
                    parsed_items = None
                    max_parse_retries = 2
                    
                    for retry_count in range(max_parse_retries + 1):
                        try:
                            raw_response = self.llm_client.call_with_retry(timeline_prompt, input_data)
                            
                            if not raw_response:
                                logger.warning(f"  > Chunk {chunk_index} got an empty LLM response, skipping")
                                break
                            
                            # Save the raw response to cache
                            cache_file = self.llm_raw_output_dir / f"chunk_{chunk_index}_attempt_{retry_count}.txt"
                            with open(cache_file, 'w', encoding='utf-8') as f:
                                f.write(raw_response)
                            
                            # Parse the raw LLM response
                            parsed_items = self._parse_and_validate_response(
                                raw_response, 
                                chunk_start_time, 
                                chunk_end_time,
                                chunk_index
                            )
                            
                            if parsed_items:
                                # Save the parsed result
                                with open(chunk_output_path, 'w', encoding='utf-8') as f:
                                    json.dump(parsed_items, f, ensure_ascii=False, indent=2)
                                
                                logger.info(f"  > Chunk {chunk_index} parsed {len(parsed_items)} segments")
                                break  # parsed successfully, leave the retry loop
                            else:
                                if retry_count < max_parse_retries:
                                    logger.warning(f"  > Chunk {chunk_index} failed to parse, retrying ({retry_count + 1}/{max_parse_retries + 1})")
                                    # On retry, strengthen the prompt with JSON format emphasis
                                    input_data['additional_instruction'] = "\n\n[IMPORTANT] Output requirements:\n1. Must start with [ and end with ]\n2. Use standard English double quotes, never locale-specific quotes\n3. Quotes inside strings must be escaped as \\\"\n4. Do not add any explanatory text or code-block markers\n5. Ensure the JSON is fully valid"
                                else:
                                    logger.error(f"  > Chunk {chunk_index} still failed to parse after {max_parse_retries + 1} attempts")
                                    # Save the last raw response for debugging
                                    self._save_debug_response(raw_response, chunk_index, "final_parse_failure")
                                    
                        except Exception as parse_error:
                            logger.error(f"  > Chunk {chunk_index} raised during parse attempt {retry_count + 1}: {parse_error}")
                            if retry_count == max_parse_retries:
                                # Save the raw response for debugging
                                self._save_debug_response(raw_response if 'raw_response' in locals() else "No response", chunk_index, "parse_exception")
                            continue
                    
                    if not parsed_items:
                          logger.warning(f"  > Chunk {chunk_index} failed to parse in the end, skipping")
                          continue

            except Exception as e:
                logger.error(f"  > Error processing chunk {chunk_index}: {str(e)}")
                continue
        
        # 4. Stitch the final result from all intermediate files
        logger.info("All chunks processed, stitching the final result from intermediate files...")
        all_timeline_data = []
        chunk_files = sorted(self.timeline_chunks_dir.glob("*.json"))
        for chunk_file in chunk_files:
            with open(chunk_file, 'r', encoding='utf-8') as f:
                chunk_data = json.load(f)
                all_timeline_data.extend(chunk_data)

        logger.info(f"Loaded {len(all_timeline_data)} topics from {len(chunk_files)} chunk files.")
        
        # Final sort: globally sort all results by start time before returning
        if all_timeline_data:
            logger.info("Sorting all topics by start time for the final pass...")
            try:
                # Use text_processor to convert time strings to seconds for correct sorting
                all_timeline_data.sort(key=lambda x: self.text_processor.time_to_seconds(x['start_time']))
                logger.info("Sorting done.")
                
                # Assign stable IDs to all segments in time order
                logger.info("Assigning stable IDs to all segments in time order...")
                for i, timeline_item in enumerate(all_timeline_data):
                    timeline_item['id'] = str(i + 1)
                logger.info(f"Assigned stable IDs to {len(all_timeline_data)} segments (1-{len(all_timeline_data)})")
                
            except Exception as e:
                logger.error(f"Error sorting the final result: {e}. Returning unsorted results.")

        # 5. Programmatic correction: snap to subtitle boundaries / duration
        # bounds / dedupe-and-merge (docs/QUALITY_AND_PUBLISH_PLAN.md section 1-B)
        if all_timeline_data:
            try:
                from .quality import load_srt_chunks, refine_timeline, save_report
                srt_entries = load_srt_chunks(self.metadata_dir)
                refined, report = refine_timeline(all_timeline_data, srt_entries, profile)
                save_report({"step2": report}, self.metadata_dir)
                logger.info(
                    f"Timeline refinement: {report['input']} → {report['output']} segments, "
                    f"merged {len(report['merged'])}, dropped {len(report['dropped'])}, "
                    f"extended {report['extended']}, trimmed {report['trimmed']}, "
                    f"snap offset p90={report.get('snap_offset_p90', 0)}s"
                )
                all_timeline_data = refined
            except Exception as e:  # noqa: BLE001
                logger.error(f"Timeline refinement failed, keeping the raw result: {e}")

        return all_timeline_data
        
    def _parse_and_validate_response(self, response: str, chunk_start: str, chunk_end: str, chunk_index: int) -> List[Dict]:
        """Parse the batched LLM response with extra validation and time adjustment"""
        validated_items = []
        
        # Save the raw response for debugging
        self._save_debug_response(response, chunk_index, "original_response")
        
        try:
            # Try parsing the JSON
            parsed_response = self.llm_client.parse_json_response(response)
            
            # Validate the JSON structure
            if not self.llm_client._validate_json_structure(parsed_response):
                logger.error(f"  > Chunk {chunk_index} failed JSON structure validation")
                self._save_debug_response(str(parsed_response), chunk_index, "invalid_structure")
                return []
            
            if not isinstance(parsed_response, list):
                logger.warning(f"  > Chunk {chunk_index} LLM did not return a list")
                self._save_debug_response(f"Type: {type(parsed_response)}, content: {parsed_response}", chunk_index, "not_list")
                return []
            
            for timeline_item in parsed_response:
                if 'outline' not in timeline_item or 'start_time' not in timeline_item or 'end_time' not in timeline_item:
                    logger.warning(f"  > A JSON object from the LLM has an invalid shape: {timeline_item}")
                    continue
                
                # Add chunk_index back onto the object for later steps
                timeline_item['chunk_index'] = chunk_index
                
                # Validate and adjust the time range
                try:
                    # Validate the time format
                    if not self._validate_time_format(timeline_item['start_time']):
                        logger.warning(f"  > Topic '{timeline_item['outline']}' has a bad start_time format: {timeline_item['start_time']}")
                        continue
                    
                    if not self._validate_time_format(timeline_item['end_time']):
                        logger.warning(f"  > Topic '{timeline_item['outline']}' has a bad end_time format: {timeline_item['end_time']}")
                        continue
                    
                    start_time = self._convert_time_format(timeline_item['start_time'])
                    end_time = self._convert_time_format(timeline_item['end_time'])
                    
                    start_sec = self.text_processor.time_to_seconds(start_time)
                    end_sec = self.text_processor.time_to_seconds(end_time)
                    chunk_start_sec = self.text_processor.time_to_seconds(chunk_start)
                    chunk_end_sec = self.text_processor.time_to_seconds(chunk_end)
                    
                    if start_sec < chunk_start_sec:
                        logger.warning(f"  > Clamping topic '{timeline_item['outline']}' start_time from {start_time} to {chunk_start}")
                        timeline_item['start_time'] = chunk_start
                    
                    if end_sec > chunk_end_sec:
                        logger.warning(f"  > Clamping topic '{timeline_item['outline']}' end_time from {end_time} to {chunk_end}")
                        timeline_item['end_time'] = chunk_end
                    
                    logger.info(f"  > Located: {timeline_item['outline']} ({timeline_item['start_time']} -> {timeline_item['end_time']})")
                    validated_items.append(timeline_item)
                except Exception as e:
                    logger.error(f"  > Error validating a single timestamp: {e} - item: {timeline_item}")
                    continue
            
            return validated_items

        except Exception as e:
            logger.error(f"  > Chunk {chunk_index} raised while parsing the LLM response: {e}")
            # Save the detailed error info
            error_info = {
                "error": str(e),
                "error_type": type(e).__name__,
                "response_length": len(response),
                "response_preview": response[:200],
                "chunk_index": chunk_index,
                "chunk_start": chunk_start,
                "chunk_end": chunk_end
            }
            import json
            self._save_debug_response(json.dumps(error_info, indent=2, ensure_ascii=False), chunk_index, "parse_error")
            return []

    def _validate_time_format(self, time_str: str) -> bool:
        """
        Check the time format (HH:MM:SS,mmm)
        """
        pattern = r'^\d{2}:\d{2}:\d{2},\d{3}$'
        return bool(re.match(pattern, time_str))
    
    def _convert_time_format(self, time_str: str) -> str:
        """
        Convert time format: SRT format -> FFmpeg format
        """
        if not time_str or time_str == "end":
            return time_str
        return time_str.replace(',', '.')

    def _save_debug_response(self, response: str, chunk_index: int, error_type: str) -> None:
        """Save a debug response to a file"""
        try:
            debug_dir = self.metadata_dir / "debug_responses"
            debug_dir.mkdir(parents=True, exist_ok=True)
            debug_file = debug_dir / f"chunk_{chunk_index}_{error_type}.txt"
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(response)
            logger.info(f"Debug response saved to: {debug_file}")
        except Exception as e:
            logger.error(f"Failed to save debug response: {e}")

    def save_timeline(self, timeline_data: List[Dict], output_path: Optional[Path] = None) -> Path:
        """
        Save the timeline data
        """
        if output_path is None:
            output_path = METADATA_DIR / "step2_timeline.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(timeline_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"Timeline data saved to: {output_path}")
        return output_path

    def load_timeline(self, input_path: Path) -> List[Dict]:
        """
        Load timeline data from a file
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)

def run_step2_timeline(outline_path: Path, metadata_dir: Path = None, output_path: Optional[Path] = None, prompt_files: Dict = None) -> List[Dict]:
    """
    Run Step 2: timeline extraction
    """
    if metadata_dir is None:
        metadata_dir = METADATA_DIR
        
    extractor = TimelineExtractor(metadata_dir, prompt_files)
    
    # Load the outline
    with open(outline_path, 'r', encoding='utf-8') as f:
        outlines = json.load(f)
        
    timeline_data = extractor.extract_timeline(outlines)
    
    # Save the result
    if output_path is None:
        output_path = metadata_dir / "step2_timeline.json"
        
    extractor.save_timeline(timeline_data, output_path)
    
    return timeline_data