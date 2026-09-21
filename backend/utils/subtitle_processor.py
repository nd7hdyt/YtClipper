import logging
import re
import uuid
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pysrt
from pysrt import SubRipItem, SubRipTime

logger = logging.getLogger(__name__)

class SubtitleProcessor:
    """subtitlesprocessingEN - ENsubtitlesparseENprocessing"""
    
    def __init__(self):
        # EN：EN（，。！？；：“”‘’（）【】、）EN。
        # useEN，EN/EN，
        # meanwhileEN \s EN、EN SyntaxWarning。
        self.word_separators = r"[，。！？；：“”‘’（）【】、\s]+"
    
    def parse_srt_to_word_level(self, srt_path: Path) -> List[Dict]:
        """
        ENSRTsubtitlesparseEN
        
        Args:
            srt_path: SRTfilepath
            
        Returns:
            ENsubtitlesEN
        """
        if not srt_path.exists():
            logger.error(f"SRTfiledoes not exist: {srt_path}")
            return []
        
        try:
            subs = pysrt.open(str(srt_path), encoding='utf-8')
            word_level_data = []
            
            for sub in subs:
                segment_data = self._process_subtitle_segment(sub)
                word_level_data.append(segment_data)
            
            logger.info(f"succeededparseSRTfile，EN {len(word_level_data)} ENsubtitlesEN")
            return word_level_data
            
        except Exception as e:
            logger.error(f"parseSRTfilefailed: {e}")
            return []
    
    def _process_subtitle_segment(self, sub: SubRipItem) -> Dict:
        """
        processingENsubtitlesEN，EN
        
        Args:
            sub: pysrtsubtitlesEN
            
        Returns:
            ENsubtitlesEN
        """
        # ENtimeEN
        start_seconds = self._srt_time_to_seconds(sub.start)
        end_seconds = self._srt_time_to_seconds(sub.end)
        
        # EN
        words = self._split_text_to_words(sub.text, start_seconds, end_seconds)
        
        return {
            'id': str(uuid.uuid4()),
            'startTime': start_seconds,
            'endTime': end_seconds,
            'text': sub.text.strip(),
            'words': words,
            'index': sub.index
        }
    
    def _split_text_to_words(self, text: str, start_time: float, end_time: float) -> List[Dict]:
        """
        EN，ENtimeEN
        
        Args:
            text: subtitlesEN
            start_time: starttime（EN）
            end_time: endtime（EN）
            
        Returns:
            EN，eachENtimeEN
        """
        # EN
        clean_text = text.strip()
        if not clean_text:
            return []
        
        # EN
        word_parts = re.split(self.word_separators, clean_text)
        word_parts = [part.strip() for part in word_parts if part.strip()]
        
        if not word_parts:
            return []
        
        # ENeachENtimeEN
        total_duration = end_time - start_time
        words_count = len(word_parts)
        
        # ENtimeEN：EN
        word_duration = total_duration / words_count
        
        words = []
        for i, word_text in enumerate(word_parts):
            word_start = start_time + (i * word_duration)
            word_end = word_start + word_duration
            
            words.append({
                'id': str(uuid.uuid4()),
                'text': word_text,
                'startTime': word_start,
                'endTime': word_end
            })
        
        return words
    
    def _srt_time_to_seconds(self, srt_time: SubRipTime) -> float:
        """
        ENSRTtimeEN
        
        Args:
            srt_time: pysrttimeEN
            
        Returns:
            EN
        """
        return srt_time.hours * 3600 + srt_time.minutes * 60 + srt_time.seconds + srt_time.milliseconds / 1000
    
    def _seconds_to_srt_time_object(self, time_str: str) -> SubRipTime:
        """
        ENtimeENpysrttimeEN
        
        Args:
            time_str: timeEN (EN "00:01:25,140")
            
        Returns:
            pysrttimeEN
        """
        # processingEN
        time_str = time_str.replace(',', '.')
        
        # parsetime
        time_parts = time_str.split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        
        # processingEN
        seconds_part = time_parts[2]
        if '.' in seconds_part:
            seconds, milliseconds = seconds_part.split('.')
            seconds = int(seconds)
            milliseconds = int(milliseconds.ljust(3, '0')[:3])  # EN3EN
        else:
            seconds = int(seconds_part)
            milliseconds = 0
        
        return SubRipTime(hours, minutes, seconds, milliseconds)
    
    def create_edit_operations(self, deleted_segments: List[str], 
                             original_data: List[Dict]) -> List[Dict]:
        """
        ENdeleteENsubtitlesENcreateEN
        
        Args:
            deleted_segments: ENdeleteENsubtitlesENIDEN
            original_data: ENsubtitlesEN
            
        Returns:
            EN
        """
        operations = []
        
        for segment_id in deleted_segments:
            segment = next((s for s in original_data if s['id'] == segment_id), None)
            if segment:
                operation = {
                    'type': 'delete',
                    'segmentIds': [segment_id],
                    'timestamp': segment['startTime'],
                    'metadata': {
                        'originalText': segment['text'],
                        'timeRange': {
                            'start': segment['startTime'],
                            'end': segment['endTime']
                        }
                    }
                }
                operations.append(operation)
        
        return operations
    
    def generate_edited_video_timeline(self, original_data: List[Dict], 
                                     deleted_segments: List[str]) -> List[Tuple[float, float]]:
        """
        generateENvideotimeEN
        
        Args:
            original_data: ENsubtitlesEN
            deleted_segments: ENdeleteENsubtitlesENIDEN
            
        Returns:
            ENtimeEN [(start, end), ...]
        """
        deleted_ids = set(deleted_segments)
        timeline = []
        
        for segment in original_data:
            if segment['id'] not in deleted_ids:
                timeline.append((segment['startTime'], segment['endTime']))
        
        # ENtimeEN
        if timeline:
            merged_timeline = [timeline[0]]
            for current_start, current_end in timeline[1:]:
                last_start, last_end = merged_timeline[-1]
                
                # ifcurrentEN，thenEN
                if current_start <= last_end + 0.1:  # EN0.1EN
                    merged_timeline[-1] = (last_start, max(last_end, current_end))
                else:
                    merged_timeline.append((current_start, current_end))
            
            return merged_timeline
        
        return []
    
    def export_edited_srt(self, original_data: List[Dict], 
                         deleted_segments: List[str], 
                         output_path: Path) -> bool:
        """
        ENSRTfile
        
        Args:
            original_data: ENsubtitlesEN
            deleted_segments: ENdeleteENsubtitlesENIDEN
            output_path: ENfilepath
            
        Returns:
            ENsucceeded
        """
        try:
            deleted_ids = set(deleted_segments)
            edited_segments = []
            
            for segment in original_data:
                if segment['id'] not in deleted_ids:
                    edited_segments.append(segment)
            
            # EN
            for i, segment in enumerate(edited_segments, 1):
                segment['index'] = i
            
            # writeSRTfile
            with open(output_path, 'w', encoding='utf-8') as f:
                for segment in edited_segments:
                    start_time = self._seconds_to_srt_time(segment['startTime'])
                    end_time = self._seconds_to_srt_time(segment['endTime'])
                    
                    f.write(f"{segment['index']}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{segment['text']}\n\n")
            
            logger.info(f"ENSRTfileENsave: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"ENSRTfilefailed: {e}")
            return False
    
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """
        ENSRTtimeEN
        
        Args:
            seconds: EN
            
        Returns:
            SRTtimeEN
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    
    def get_subtitle_statistics(self, data: List[Dict]) -> Dict:
        """
        fetchsubtitlesEN
        
        Args:
            data: subtitlesEN
            
        Returns:
            EN
        """
        if not data:
            return {
                'totalDuration': 0,
                'wordCount': 0,
                'segmentCount': 0,
                'averageWordsPerSegment': 0
            }
        
        total_duration = max(seg['endTime'] for seg in data) - min(seg['startTime'] for seg in data)
        word_count = sum(len(seg['words']) for seg in data)
        segment_count = len(data)
        
        return {
            'totalDuration': total_duration,
            'wordCount': word_count,
            'segmentCount': segment_count,
            'averageWordsPerSegment': word_count / segment_count if segment_count > 0 else 0
        }
