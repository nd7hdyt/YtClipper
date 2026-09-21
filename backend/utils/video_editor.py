import logging
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from .video_processor import VideoProcessor
from .subtitle_processor import SubtitleProcessor
from .ffmpeg_utils import get_ffmpeg_path, get_ffprobe_path

logger = logging.getLogger(__name__)

class VideoEditor:
    """videoEN - ENsubtitlesdeleteENvideoEN"""
    
    def __init__(self, clips_dir: Optional[str] = None, collections_dir: Optional[str] = None):
        # VideoEditor ENneedENpathparameters，ENuseENpath
        if clips_dir is None or collections_dir is None:
            # ifENpath，useENdirectory（EN）
            from ..core.shared_config import CLIPS_DIR, COLLECTIONS_DIR
            clips_dir = str(CLIPS_DIR) if clips_dir is None else clips_dir
            collections_dir = str(COLLECTIONS_DIR) if collections_dir is None else collections_dir
        
        self.video_processor = VideoProcessor(clips_dir=clips_dir, collections_dir=collections_dir)
        self.subtitle_processor = SubtitleProcessor()
    
    def edit_video_by_subtitle_deletion(self, 
                                      video_path: Path,
                                      subtitle_data: List[Dict],
                                      deleted_segments: List[str],
                                      output_path: Path) -> Dict:
        """
        ENsubtitlesdeleteENvideo
        
        Args:
            video_path: ENvideopath
            subtitle_data: subtitlesEN
            deleted_segments: ENdeleteENsubtitlesENIDEN
            output_path: ENvideopath
            
        Returns:
            ENresultEN
        """
        try:
            logger.info(f"startENsubtitlesdeleteENvideo: {video_path}")
            
            # generateENtimeEN
            timeline = self.subtitle_processor.generate_edited_video_timeline(
                subtitle_data, deleted_segments
            )
            
            if not timeline:
                logger.warning("ENtimeEN，cannotgeneratevideo")
                return {
                    'success': False,
                    'error': 'ENtimeEN'
                }
            
            # ENdeleteENduration
            total_deleted_duration = self._calculate_deleted_duration(
                subtitle_data, deleted_segments
            )
            
            # executevideoEN
            success = self._concatenate_video_segments(
                video_path, timeline, output_path
            )
            
            if success:
                # fetchENvideoduration
                final_duration = self._get_video_duration(output_path)
                
                result = {
                    'success': True,
                    'originalVideoPath': str(video_path),
                    'editedVideoPath': str(output_path),
                    'totalDeletedDuration': total_deleted_duration,
                    'finalDuration': final_duration,
                    'timeline': timeline,
                    'deletedSegments': deleted_segments
                }
                
                logger.info(f"videoEN: deleteduration {total_deleted_duration:.2f}EN，"
                          f"ENduration {final_duration:.2f}EN")
                return result
            else:
                return {
                    'success': False,
                    'error': 'videoENfailed'
                }
                
        except Exception as e:
            logger.error(f"videoENfailed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_deleted_duration(self, subtitle_data: List[Dict], 
                                  deleted_segments: List[str]) -> float:
        """
        ENdeleteENduration
        
        Args:
            subtitle_data: subtitlesEN
            deleted_segments: deleteENsubtitlesENIDEN
            
        Returns:
            deleteENduration（EN）
        """
        deleted_ids = set(deleted_segments)
        total_duration = 0.0
        
        for segment in subtitle_data:
            if segment['id'] in deleted_ids:
                duration = segment['endTime'] - segment['startTime']
                total_duration += duration
        
        return total_duration
    
    def _concatenate_video_segments(self, video_path: Path, 
                                  timeline: List[Tuple[float, float]], 
                                  output_path: Path) -> bool:
        """
        ENvideoEN
        
        Args:
            video_path: ENvideopath
            timeline: timeEN [(start, end), ...]
            output_path: ENpath
            
        Returns:
            ENsucceeded
        """
        try:
            # ENdirectoryEN
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if len(timeline) == 1:
                # EN，EN
                start_time, end_time = timeline[0]
                return self._extract_single_segment(
                    video_path, start_time, end_time, output_path
                )
            else:
                # EN，needEN
                return self._concatenate_multiple_segments(
                    video_path, timeline, output_path
                )
                
        except Exception as e:
            logger.error(f"ENvideoENfailed: {e}")
            return False
    
    def _extract_single_segment(self, video_path: Path, 
                              start_time: float, end_time: float, 
                              output_path: Path) -> bool:
        """
        ENvideoEN
        
        Args:
            video_path: ENvideopath
            start_time: starttime（EN）
            end_time: endtime（EN）
            output_path: ENpath
            
        Returns:
            ENsucceeded
        """
        try:
            duration = end_time - start_time
            
            ffmpeg_bin = get_ffmpeg_path()
            cmd = [
                ffmpeg_bin,
                '-ss', str(start_time),
                '-i', str(video_path),
                '-t', str(duration),
                '-c:v', 'copy',
                '-c:a', 'copy',
                '-avoid_negative_ts', 'make_zero',
                '-y',
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"succeededENvideoEN: {start_time:.2f}s - {end_time:.2f}s")
                return True
            else:
                logger.error(f"ENvideoENfailed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"ENvideoENexception: {e}")
            return False
    
    def _concatenate_multiple_segments(self, video_path: Path, 
                                     timeline: List[Tuple[float, float]], 
                                     output_path: Path) -> bool:
        """
        ENvideoEN
        
        Args:
            video_path: ENvideopath
            timeline: timeEN [(start, end), ...]
            output_path: ENpath
            
        Returns:
            ENsucceeded
        """
        try:
            # createENdirectory
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # ENallEN
                segment_files = []
                for i, (start_time, end_time) in enumerate(timeline):
                    segment_file = temp_path / f"segment_{i:03d}.mp4"
                    
                    success = self._extract_single_segment(
                        video_path, start_time, end_time, segment_file
                    )
                    
                    if success:
                        segment_files.append(segment_file)
                    else:
                        logger.error(f"EN {i} failed")
                        return False
                
                # createfileEN
                file_list_path = temp_path / "file_list.txt"
                with open(file_list_path, 'w', encoding='utf-8') as f:
                    for segment_file in segment_files:
                        f.write(f"file '{segment_file}'\n")
                
                # ENallEN
                ffmpeg_bin = get_ffmpeg_path()
                cmd = [
                    ffmpeg_bin,
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', str(file_list_path),
                    '-c', 'copy',
                    '-y',
                    str(output_path)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"succeededEN {len(segment_files)} ENvideoEN")
                    return True
                else:
                    logger.error(f"ENvideoENfailed: {result.stderr}")
                    return False
                    
        except Exception as e:
            logger.error(f"ENvideoENexception: {e}")
            return False
    
    def _get_video_duration(self, video_path: Path) -> float:
        """
        fetchvideoduration
        
        Args:
            video_path: videopath
            
        Returns:
            videoduration（EN）
        """
        try:
            ffprobe_bin = get_ffprobe_path()
            cmd = [
                ffprobe_bin,
                '-v', 'quiet',
                '-show_entries', 'format=duration',
                '-of', 'csv=p=0',
                str(video_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration
            else:
                logger.warning(f"fetchvideodurationfailed: {result.stderr}")
                return 0.0
                
        except Exception as e:
            logger.error(f"fetchvideodurationexception: {e}")
            return 0.0
    
    def create_preview_clips(self, video_path: Path, 
                           subtitle_data: List[Dict],
                           deleted_segments: List[str],
                           output_dir: Path) -> List[Path]:
        """
        createEN，EN
        
        Args:
            video_path: ENvideopath
            subtitle_data: subtitlesEN
            deleted_segments: ENdeleteENsubtitlesENIDEN
            output_dir: ENdirectory
            
        Returns:
            ENfilepathEN
        """
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            preview_files = []
            
            # ENeachENdeleteENcreateEN
            for segment_id in deleted_segments:
                segment = next((s for s in subtitle_data if s['id'] == segment_id), None)
                if segment:
                    preview_file = output_dir / f"preview_{segment_id}.mp4"
                    
                    success = self._extract_single_segment(
                        video_path,
                        segment['startTime'],
                        segment['endTime'],
                        preview_file
                    )
                    
                    if success:
                        preview_files.append(preview_file)
            
            logger.info(f"createEN {len(preview_files)} EN")
            return preview_files
            
        except Exception as e:
            logger.error(f"createENfailed: {e}")
            return []
    
    def validate_edit_operations(self, subtitle_data: List[Dict], 
                               deleted_segments: List[str]) -> Dict:
        """
        validateEN
        
        Args:
            subtitle_data: subtitlesEN
            deleted_segments: ENdeleteENsubtitlesENIDEN
            
        Returns:
            validateresult
        """
        try:
            # checkdeleteENsubtitlesEN
            existing_ids = {seg['id'] for seg in subtitle_data}
            deleted_ids = set(deleted_segments)
            
            invalid_ids = deleted_ids - existing_ids
            if invalid_ids:
                return {
                    'valid': False,
                    'error': f'ENsubtitlesENID: {list(invalid_ids)}'
                }
            
            # checkdeleteEN
            remaining_segments = [seg for seg in subtitle_data if seg['id'] not in deleted_ids]
            
            if not remaining_segments:
                return {
                    'valid': False,
                    'error': 'deleteallsubtitlesEN'
                }
            
            # ENdeleteENduration
            total_deleted_duration = self._calculate_deleted_duration(
                subtitle_data, deleted_segments
            )
            
            # ENduration
            total_duration = max(seg['endTime'] for seg in subtitle_data) - min(seg['startTime'] for seg in subtitle_data)
            
            return {
                'valid': True,
                'totalDuration': total_duration,
                'deletedDuration': total_deleted_duration,
                'remainingDuration': total_duration - total_deleted_duration,
                'deletedSegments': len(deleted_segments),
                'remainingSegments': len(remaining_segments)
            }
            
        except Exception as e:
            logger.error(f"validateENfailed: {e}")
            return {
                'valid': False,
                'error': str(e)
            }
