"""
Step 1: Outline extraction - extract a structural outline from transcript text
"""
import json
import logging
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

# Import dependencies
from ..utils.llm_client import LLMClient
from ..utils.text_processor import TextProcessor
from ..core.shared_config import PROMPT_FILES, METADATA_DIR
from .failures import PipelineFailure, HINT_CHECK_LLM, HINT_SUBTITLE

logger = logging.getLogger(__name__)

class OutlineExtractor:
    """Outline extractor (refactored version)"""
    
    def __init__(self, metadata_dir: Path = None, prompt_files: Dict = None):
        self.llm_client = LLMClient()
        self.text_processor = TextProcessor()
        
        # Use the provided metadata_dir or the default
        if metadata_dir is None:
            metadata_dir = METADATA_DIR
        self.metadata_dir = metadata_dir
        
        # Use the provided prompt_files or the defaults
        if prompt_files is None:
            prompt_files = PROMPT_FILES
        
        # Load the prompt
        with open(prompt_files['outline'], 'r', encoding='utf-8') as f:
            self.outline_prompt = f.read()
            
        # Directory for intermediate text chunks
        self.chunks_dir = self.metadata_dir / "step1_chunks"
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
        # Directory for intermediate SRT chunks
        self.srt_chunks_dir = self.metadata_dir / "step1_srt_chunks"
        self.srt_chunks_dir.mkdir(parents=True, exist_ok=True)

    def extract_outline(self, srt_path: Path) -> List[Dict]:
        """
        Extract the video outline from an SRT file
        
        Args:
            srt_path: path to the SRT file
            
        Returns:
            list of video outline topics
        """
        logger.info("Extracting video outline...")
        
        # 1. Parse the SRT file. Empty subtitles / parse failure must fail the
        # pipeline, never silently return [] and let later steps run into 0 clips
        try:
            srt_data = self.text_processor.parse_srt(srt_path)
        except Exception as e:
            logger.error(f"Failed to parse SRT file: {e}")
            raise PipelineFailure("SUBTITLE", f"Subtitle file could not be parsed: {e}", HINT_SUBTITLE) from e
        if not srt_data:
            logger.warning("SRT file is empty or failed to parse")
            raise PipelineFailure("SUBTITLE", "Subtitle file is empty; there is no text to analyze.", HINT_SUBTITLE)
            
        # 1.5 Duration profile: short videos must not reuse podcast parameters (#59).
        # Persist to disk for step2 / step3 reuse
        from .quality import profile_from_srt, save_profile
        profile = profile_from_srt(srt_data)
        save_profile(profile, self.metadata_dir)
        outline_prompt = self.outline_prompt + profile.prompt_hint()
        logger.info(f"Duration profile: {profile.tier}, total {profile.total_sec:.0f}s, suggested topics {profile.topics_hint}")

        # 2. Time-based smart chunking (short/medium videos as a single chunk,
        # long videos ~30 minutes per chunk)
        interval = 30 if profile.tier == "long" else max(1, int(profile.total_sec // 60) + 1)
        chunks = self.text_processor.chunk_srt_data(srt_data, interval_minutes=interval)
        logger.info(f"Text split into ~{interval} min/chunk, {len(chunks)} chunks total")
        
        # 3. Save text chunks and SRT chunks to intermediate files
        chunk_files = self._save_chunks_to_files(chunks)
        self._save_srt_chunks(chunks)
        
        all_outlines = []
        failed_chunks = 0
        last_error: Optional[BaseException] = None
        
        # 4. Process each text-chunk file one by one
        for i, chunk_file in enumerate(chunk_files):
            logger.info(f"Processing chunk {i+1}/{len(chunks)}: {chunk_file.name}")
            try:
                # Read the chunk content
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunk_text = f.read()
                
                # Call the LLM for each chunk
                input_data = {"text": chunk_text}
                response = self.llm_client.call_with_retry(outline_prompt, input_data)
                
                if response:
                    # Parse the response and attach the chunk index
                    # Note: chunk_index uses i directly, matching the file name and original chunk
                    parsed_outlines = self._parse_outline_response(response, i)
                    all_outlines.extend(parsed_outlines)
                else:
                    logger.warning(f"Chunk {i+1} returned an empty response")
            except Exception as e:
                # A single-chunk failure is tolerable (an occasional timeout on one
                # chunk of a long video should not kill the whole run), but count it:
                # all chunks failing = wrong provider / key / model, which must raise
                # instead of handing downstream an empty outline
                failed_chunks += 1
                last_error = e
                logger.error(f"Failed to process chunk {i+1}: {e}")
                continue

        total_chunks = len(chunk_files)
        if total_chunks and failed_chunks == total_chunks:
            raise PipelineFailure(
                "ANALYZE",
                f"Outline extraction failed: model calls failed for {failed_chunks}/{total_chunks} text chunks. Last error: {last_error}",
                HINT_CHECK_LLM,
            ) from last_error
        if failed_chunks:
            logger.warning(f"{failed_chunks}/{total_chunks} chunks failed, continuing with the rest. Last error: {last_error}")
        
        # 5. Merge and deduplicate
        final_outlines = self._merge_outlines(all_outlines)
        if not final_outlines:
            raise PipelineFailure(
                "ANALYZE",
                f"Model output could not be parsed into an outline (no valid topics from any of the {total_chunks} text chunks).",
                "Retry with a stronger or more stable model (e.g. qwen-plus / gpt-4o-mini); for a local model, make sure it handles long Chinese text.",
            )
        
        logger.info(f"Outline extraction done, {len(final_outlines)} topics total")
        return final_outlines

    def _save_chunks_to_files(self, chunks: List[Dict]) -> List[Path]:
        """Save text chunks as individual .txt files"""
        chunk_files = []
        for chunk in chunks:
            chunk_index = chunk['chunk_index']
            text_content = chunk['text']
            file_path = self.chunks_dir / f"chunk_{chunk_index}.txt"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
            chunk_files.append(file_path)
        
        logger.info(f"All text chunks saved to: {self.chunks_dir}")
        return chunk_files

    def _save_srt_chunks(self, chunks: List[Dict]):
        """Save SRT data chunks as individual .json files"""
        for chunk in chunks:
            chunk_index = chunk['chunk_index']
            srt_entries = chunk['srt_entries']
            file_path = self.srt_chunks_dir / f"chunk_{chunk_index}.json"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(srt_entries, f, ensure_ascii=False, indent=2)
        
        logger.info(f"All SRT chunks saved to: {self.srt_chunks_dir}")

    def _parse_outline_response(self, response: str, chunk_index: int) -> List[Dict]:
        """
        Parse the outline response from the LLM (same as the previous version, no quality checks)
        
        Args:
            response: LLM response
            chunk_index: index of the chunk being processed
            
        Returns:
            parsed outline structure
        """
        outlines = []
        lines = response.split('\n')
        current_outline = None
        
        for line in lines:
            line = line.strip()
            
            if re.match(r'^\d+\.\s*\*\*', line):
                if current_outline:
                    outlines.append(current_outline)
                
                topic_name = line.split('**')[1] if '**' in line else line.split('.', 1)[1].strip()
                current_outline = {
                    'title': topic_name,
                    'subtopics': [],
                    'chunk_index': chunk_index
                }
            
            elif line.startswith('-') and current_outline:
                subtopic = line[1:].strip()
                if subtopic and len(subtopic) <= 200:
                    current_outline['subtopics'].append(subtopic)
        
        if current_outline:
            outlines.append(current_outline)
        
        return outlines
    
    def _merge_outlines(self, outlines: List[Dict]) -> List[Dict]:
        """
        Merge and deduplicate outlines, keeping the first occurrence of each title
        """
        unique_outlines = {}
        for outline in outlines:
            title = outline['title']
            if title not in unique_outlines:
                unique_outlines[title] = outline
        return list(unique_outlines.values())
    
    def save_outline(self, outlines: List[Dict], output_path: Optional[Path] = None) -> Path:
        """
        Save the outline to a file
        """
        if output_path is None:
            output_path = self.metadata_dir / "step1_outline.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(outlines, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Outline saved to: {output_path}")
        return output_path
    
    def load_outline(self, input_path: Path) -> List[Dict]:
        """
        Load the outline from a file
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)

def run_step1_outline(srt_path: Path, metadata_dir: Path = None, output_path: Optional[Path] = None, prompt_files: Dict = None) -> List[Dict]:
    """
    Run Step 1: outline extraction
    """
    if metadata_dir is None:
        metadata_dir = METADATA_DIR
        
    extractor = OutlineExtractor(metadata_dir, prompt_files)
    outlines = extractor.extract_outline(srt_path)
    
    if output_path is None:
        output_path = metadata_dir / "step1_outline.json"
        
    extractor.save_outline(outlines, output_path)
    
    return outlines