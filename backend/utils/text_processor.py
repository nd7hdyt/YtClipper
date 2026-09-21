"""
ENprocessingEN
"""
import json
import logging
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

# EN
try:
    from ..core.shared_config import CHUNK_SIZE
except ImportError:
    # ifENfailed，EN
    import sys
    from pathlib import Path
    backend_path = Path(__file__).parent.parent
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    from core.shared_config import CHUNK_SIZE

import pysrt

logger = logging.getLogger(__name__)

class TextProcessor:
    """ENprocessingEN"""
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> List[str]:
        """
        EN
        
        Args:
            text: EN
            chunk_size: EN
            
        Returns:
            EN
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # EN
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            # ifcurrentEN，thenEN
            if len(current_chunk) + len(paragraph) + 1 <= chunk_size:
                current_chunk += paragraph + '\n'
            else:
                # ifcurrentEN，saveEN
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                # ifEN，needEN
                if len(paragraph) > chunk_size:
                    # EN
                    sentences = re.split(r'[。！？]', paragraph)
                    temp_chunk = ""
                    for sentence in sentences:
                        if len(temp_chunk) + len(sentence) + 1 <= chunk_size:
                            temp_chunk += sentence + "。"
                        else:
                            if temp_chunk:
                                chunks.append(temp_chunk.strip())
                            temp_chunk = sentence + "。"
                    current_chunk = temp_chunk
                else:
                    current_chunk = paragraph + '\n'
        
        # EN
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def chunk_srt_data(self, srt_data: List[Dict], interval_minutes: int = 30, pause_threshold_ms: int = 1000) -> List[Dict]:
        """
        ENtime，ENSRTENtimeEN。
        ENcanENdisconnect。

        Args:
            srt_data: SRTEN
            interval_minutes: eachENtimeEN（EN）
            pause_threshold_ms: EN

        Returns:
            EN，amongEN srt_entries ENprocessingEN。
        """
        if not srt_data:
            return []

        # createEN，EN
        srt_data_with_seconds = []
        for sub in srt_data:
            entry = sub.copy()
            entry['start_seconds'] = self.time_to_seconds(sub['start_time'])
            entry['end_seconds'] = self.time_to_seconds(sub['end_time'])
            srt_data_with_seconds.append(entry)

        interval_seconds = interval_minutes * 60
        chunks = []
        current_chunk_start_index = 0
        chunk_index = 0
        
        last_cut_time = 0
        
        while current_chunk_start_index < len(srt_data_with_seconds):
            target_cut_time = last_cut_time + interval_seconds
            
            # ENtimeEN
            best_cut_index = -1
            
            # ENcurrentENstartEN 90% EN 110% ENtimeEN
            search_start_index = current_chunk_start_index
            while search_start_index < len(srt_data_with_seconds) and srt_data_with_seconds[search_start_index]['start_seconds'] < target_cut_time * 0.9:
                search_start_index += 1

            # ENstartEN
            for i in range(search_start_index, len(srt_data_with_seconds) - 1):
                current_sub = srt_data_with_seconds[i]
                next_sub = srt_data_with_seconds[i+1]
                
                # ifwealreadyENtimeEN110%，ENstopEN
                if current_sub['start_seconds'] > target_cut_time * 1.1:
                    break
                
                # ENsubtitlesENtime
                pause = next_sub['start_seconds'] - current_sub['end_seconds']
                if pause * 1000 >= pause_threshold_ms:
                    best_cut_index = i + 1  # EN
                    break
            
            # ifEN，ENtimeEN
            if best_cut_index == -1:
                # ENtimeENsubtitlesEN
                i = current_chunk_start_index
                while i < len(srt_data_with_seconds) and srt_data_with_seconds[i]['start_seconds'] < target_cut_time:
                    i += 1
                best_cut_index = i if i < len(srt_data_with_seconds) else len(srt_data_with_seconds)

            # ifEN，thenENallEN
            if best_cut_index <= current_chunk_start_index:
                 best_cut_index = len(srt_data_with_seconds)

            # createEN
            chunk_entries_with_seconds = srt_data_with_seconds[current_chunk_start_index:best_cut_index]
            if not chunk_entries_with_seconds:
                break

            # EN，ENsrt_entries
            chunk_entries = []
            for entry in chunk_entries_with_seconds:
                clean_entry = entry.copy()
                del clean_entry['start_seconds']
                del clean_entry['end_seconds']
                chunk_entries.append(clean_entry)
            
            start_time = chunk_entries[0]['start_time']
            end_time = chunk_entries[-1]['end_time']
            text = " ".join([entry['text'] for entry in chunk_entries])
            
            chunks.append({
                "chunk_index": chunk_index,
                "text": text,
                "start_time": start_time,
                "end_time": end_time,
                "srt_entries": chunk_entries
            })
            
            chunk_index += 1
            last_cut_time = chunk_entries_with_seconds[-1]['end_seconds']
            current_chunk_start_index = best_cut_index
            
        return chunks

    @staticmethod
    def parse_srt(srt_path: Path) -> List[Dict]:
        """
        parseSRTsubtitlesfile
        
        Args:
            srt_path: SRTfilepath
            
        Returns:
            subtitlesEN，eachENtimeEN
        """
        if not srt_path.exists():
            logger.error(f"SRTfiledoes not exist: {srt_path}")
            return []
        
        if srt_path.stat().st_size == 0:
            logger.warning(f"SRTfileEN: {srt_path}")
            return []

        try:
            try:
                subs = pysrt.open(str(srt_path), encoding='utf-8')
            except UnicodeDecodeError:
                logger.warning("UTF-8ENfailed，ENuse utf-8-sig...")
                subs = pysrt.open(str(srt_path), encoding='utf-8-sig')

            subtitles = []
            for sub in subs:
                subtitles.append({
                    'start_time': str(sub.start),
                    'end_time': str(sub.end),
                    'text': sub.text.strip(),
                    'index': sub.index
                })

            if not subtitles:
                logger.warning(f"succeededENSRTfileENparseENsubtitlesEN: {srt_path}")
            
            return subtitles
        except Exception as e:
            logger.error(f"usepysrtparseSRTfile'{srt_path}'ENUnknown error: {e}", exc_info=True)
            return []
    
    @staticmethod
    def extract_text_by_time_range(text: str, srt_data: List[Dict], 
                                  start_time: str, end_time: str) -> str:
        """
        ENtimeEN
        
        Args:
            text: EN
            srt_data: SRTsubtitlesEN
            start_time: starttime (EN: "00:01:25")
            end_time: endtime (EN: "00:02:53")
            
        Returns:
            ENtimeEN
        """
        # ENtimeENsubtitles
        target_subtitles = []
        
        for sub in srt_data:
            sub_start = sub['start_time']
            sub_end = sub['end_time']
            
            # checktimeEN
            if (sub_start <= end_time and sub_end >= start_time):
                target_subtitles.append(sub)
        
        # EN
        extracted_text = ""
        for sub in target_subtitles:
            extracted_text += sub['text'] + " "
        
        return extracted_text.strip()
    
    @staticmethod
    def time_to_seconds(time_str: str) -> float:
        """
        ENSRTtimeEN（HH:MM:SS,mmm）EN
        
        Args:
            time_str: timeEN
            
        Returns:
            EN
        """
        time_str = time_str.replace(',', '.')
        parts = time_str.split(':')
        
        if len(parts) == 3:
            h = int(parts[0])
            m = int(parts[1])
            s_parts = parts[2].split('.')
            s = int(s_parts[0])
            ms = int(s_parts[1]) if len(s_parts) > 1 else 0
            return h * 3600 + m * 60 + s + ms / 1000.0
        
        raise ValueError(f"ENtimeEN: {time_str}")
    
    @staticmethod
    def seconds_to_time(seconds: float) -> str:
        """
        ENtimeEN
        
        Args:
            seconds: EN
            
        Returns:
            timeEN (EN: "00:01:25")
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}" 