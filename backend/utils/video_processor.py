"""
videoprocessingEN
"""
import subprocess
import json
import logging
import re
from typing import List, Dict, Optional
from pathlib import Path
from .ffmpeg_utils import get_ffmpeg_path, get_ffprobe_path

# EN
try:
    from ..core.shared_config import CLIPS_DIR, COLLECTIONS_DIR
except ImportError:
    # ifENfailed，EN
    import sys
    from pathlib import Path
    backend_path = Path(__file__).parent.parent
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    from ..core.shared_config import CLIPS_DIR, COLLECTIONS_DIR

logger = logging.getLogger(__name__)

class VideoProcessor:
    """videoprocessingEN"""
    
    def __init__(self, clips_dir: Optional[str] = None, collections_dir: Optional[str] = None):
        # ENuseENprojectENpath，ENuseENpathEN
        if not clips_dir:
            raise ValueError("clips_dir parametersEN，ENuseENpath")
        if not collections_dir:
            raise ValueError("collections_dir parametersEN，ENuseENpath")
        
        self.clips_dir = Path(clips_dir)
        self.collections_dir = Path(collections_dir)
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        ENfileEN，EN
        
        Args:
            filename: ENfileEN
            
        Returns:
            ENfileEN
        """
        # EN
        # WindowsENUnixsystemEN: < > : " | ? * \ /
        # EN
        sanitized = re.sub(r'[<>:"|?*\\/]', '_', filename)
        
        # EN
        sanitized = sanitized.strip(' .')
        
        # EN，ENfileEN
        if len(sanitized) > 100:
            sanitized = sanitized[:100]
        
        # ENfileEN
        if not sanitized:
            sanitized = "untitled"
            
        return sanitized
    
    @staticmethod
    def convert_srt_time_to_ffmpeg_time(srt_time: str) -> str:
        """
        ENSRTtimeENFFmpegtimeEN
        
        Args:
            srt_time: SRTtimeEN (EN "00:00:06,140" EN "00:00:06.140")
            
        Returns:
            FFmpegtimeEN (EN "00:00:06.140")
        """
        # EN
        return srt_time.replace(',', '.')
    
    @staticmethod
    def convert_seconds_to_ffmpeg_time(seconds: float) -> str:
        """
        ENFFmpegtimeEN
        
        Args:
            seconds: EN
            
        Returns:
            FFmpegtimeEN (EN "00:00:06.140")
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"
    
    @staticmethod
    def convert_ffmpeg_time_to_seconds(time_str: str) -> float:
        """
        ENFFmpegtimeEN
        
        Args:
            time_str: FFmpegtimeEN (EN "00:00:06.140")
            
        Returns:
            EN
        """
        try:
            # processingEN
            if '.' in time_str:
                time_part, ms_part = time_str.split('.')
                milliseconds = int(ms_part)
            else:
                time_part = time_str
                milliseconds = 0
            
            # parseEN
            h, m, s = map(int, time_part.split(':'))
            
            return h * 3600 + m * 60 + s + milliseconds / 1000
        except Exception as e:
            logger.error(f"timeENfailed: {time_str}, error: {e}")
            return 0.0
    
    @staticmethod
    def extract_clip(input_video: Path, output_path: Path, 
                    start_time: str, end_time: str) -> bool:
        """
        ENvideoENtimeEN
        
        Args:
            input_video: ENvideopath
            output_path: ENvideopath
            start_time: starttime (EN: "00:01:25,140")
            end_time: endtime (EN: "00:02:53,500")
            
        Returns:
            ENsucceeded
        """
        try:
            # ENdirectoryEN
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # ENtimeEN：ENSRTENFFmpegEN
            ffmpeg_start_time = VideoProcessor.convert_srt_time_to_ffmpeg_time(start_time)
            ffmpeg_end_time = VideoProcessor.convert_srt_time_to_ffmpeg_time(end_time)
            
            # ENtime
            start_seconds = VideoProcessor.convert_ffmpeg_time_to_seconds(ffmpeg_start_time)
            end_seconds = VideoProcessor.convert_ffmpeg_time_to_seconds(ffmpeg_end_time)
            duration = end_seconds - start_seconds
            
            # ENFFmpegEN
            # use -ss EN，use -t ENtime
            ffmpeg_bin = get_ffmpeg_path()
            cmd = [
                ffmpeg_bin,
                '-ss', ffmpeg_start_time,  # EN，EN
                '-i', str(input_video),
                '-t', str(duration),  # useENtimeENendtime
                '-c:v', 'copy',  # ENvideoEN
                '-c:a', 'copy',  # EN
                '-avoid_negative_ts', 'make_zero',
                '-y',  # ENfile
                str(output_path)
            ]
            
            # executeEN
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            if result.returncode == 0:
                logger.info(f"succeededENvideoEN: {output_path} ({ffmpeg_start_time} -> {ffmpeg_end_time}, duration: {duration:.2f}EN)")
                return True
            else:
                logger.error(f"ENvideoENfailed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"videoprocessingexception: {str(e)}")
            return False
    
    @staticmethod
    def create_collection(clips_list: List[Path], output_path: Path) -> bool:
        """
        ENvideoENcollection
        
        Args:
            clips_list: videoENpathEN
            output_path: ENcollectionpath
            
        Returns:
            ENsucceeded
        """
        try:
            # validateENparameters
            if not clips_list:
                logger.error("clips_listEN，cannotcreatecollection")
                return False
            
            # validateallvideofileEN
            valid_clips = []
            for clip_path in clips_list:
                if not clip_path.exists():
                    logger.warning(f"videofiledoes not exist，EN: {clip_path}")
                    continue
                valid_clips.append(clip_path)
            
            if not valid_clips:
                logger.error("ENvideofile，cannotcreatecollection")
                return False
            
            # ENdirectoryEN
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # createconcatfile
            concat_file = output_path.parent / "concat_list.txt"
            
            with open(concat_file, 'w', encoding='utf-8') as f:
                for clip_path in valid_clips:
                    # useENpathEN
                    abs_path = clip_path.absolute()
                    escaped_path = str(abs_path).replace("'", "'\"'\"'")
                    f.write(f"file '{escaped_path}'\n")
            
            # validateconcatfileEN
            if concat_file.stat().st_size == 0:
                logger.error("concatfileEN，cannotcreatecollection")
                concat_file.unlink(missing_ok=True)
                return False
            
            # ENFFmpegEN - useH.264EN
            ffmpeg_bin = get_ffmpeg_path()
            cmd = [
                ffmpeg_bin,
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-c:v', 'libx264',  # useH.264videoEN
                '-preset', 'ultrafast',  # useEN
                '-crf', '28',  # EN
                '-c:a', 'aac',  # useAACEN
                '-b:a', '128k',  # EN
                '-movflags', '+faststart',  # EN
                '-y',
                str(output_path)
            ]
            
            logger.info(f"executeFFmpegEN: {' '.join(cmd)}")
            
            # executeEN
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            # ENfile
            concat_file.unlink(missing_ok=True)
            
            if result.returncode == 0:
                logger.info(f"succeededcreatecollection: {output_path}")
                return True
            else:
                logger.error(f"createcollectionfailed: {result.stderr}")
                logger.error(f"FFmpeg stdout: {result.stdout}")
                return False
                
        except Exception as e:
            logger.error(f"videoENexception: {str(e)}")
            return False
    
    @staticmethod
    def extract_thumbnail(video_path: Path, output_path: Path, time_offset: int = 5) -> bool:
        """
        ENvideoEN
        
        Args:
            video_path: videofilepath
            output_path: ENpath
            time_offset: ENtimeEN（EN）
            
        Returns:
            ENsucceeded
        """
        try:
            # ENdirectoryEN
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # ENFFmpegEN
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-ss', str(time_offset),
                '-vframes', '1',
                '-q:v', '2',  # EN
                '-y',  # ENfile
                str(output_path)
            ]
            
            # executeEN
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            if result.returncode == 0 and output_path.exists():
                logger.info(f"succeededEN: {output_path}")
                return True
            else:
                logger.error(f"ENfailed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"ENexception: {str(e)}")
            return False
    
    @staticmethod
    def get_video_info(video_path: Path) -> Dict:
        """
        fetchvideoEN
        
        Args:
            video_path: videofilepath
            
        Returns:
            videoEN
        """
        try:
            ffprobe_bin = get_ffprobe_path()
            cmd = [
                ffprobe_bin,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(video_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            if result.returncode == 0:
                info = json.loads(result.stdout)
                return {
                    'duration': float(info['format']['duration']),
                    'size': int(info['format']['size']),
                    'bitrate': int(info['format']['bit_rate']),
                    'streams': info['streams']
                }
            else:
                logger.error(f"fetchvideoENfailed: {result.stderr}")
                return {}
                
        except Exception as e:
            logger.error(f"fetchvideoENexception: {str(e)}")
            return {}
    
    def batch_extract_clips(self, input_video: Path, clips_data: List[Dict]) -> List[Path]:
        """
        ENvideoEN
        
        Args:
            input_video: ENvideopath
            clips_data: EN，eachENid、title、start_time、end_time
            
        Returns:
            succeededENpathEN
        """
        successful_clips = []
        
        for clip_data in clips_data:
            clip_id = clip_data['id']
            title = clip_data.get('title', f"EN_{clip_id}")
            start_time = clip_data['start_time']
            end_time = clip_data['end_time']
            
            # processingtimeEN - ifEN，ENSRTEN
            if isinstance(start_time, (int, float)):
                start_time = VideoProcessor.convert_seconds_to_ffmpeg_time(start_time)
            if isinstance(end_time, (int, float)):
                end_time = VideoProcessor.convert_seconds_to_ffmpeg_time(end_time)
            
            # usetitleENfileEN，EN
            # ENfileENclip_id，ENcollectionEN
            safe_title = VideoProcessor.sanitize_filename(title)
            output_path = self.clips_dir / f"{clip_id}_{safe_title}.mp4"
            
            logger.info(f"ENclip {clip_id}: {start_time} -> {end_time}, EN: {output_path}")
            
            if VideoProcessor.extract_clip(input_video, output_path, start_time, end_time):
                successful_clips.append(output_path)
                logger.info(f"clip {clip_id} ENsucceeded")
            else:
                logger.error(f"clip {clip_id} ENfailed")
        
        return successful_clips
    
    def create_collections_from_metadata(self, collections_data: List[Dict]) -> List[Dict]:
        """
        ENcreatecollection
        
        Args:
            collections_data: collectionEN
            
        Returns:
            succeededcreateENcollectionEN，ENvideopathENpath
        """
        successful_collections = []
        
        for collection_data in collections_data:
            collection_id = collection_data['id']
            collection_title = collection_data.get('collection_title', f'collection_{collection_id}')
            clip_ids = collection_data['clip_ids']
            
            # ENpathEN
            clips_list = []
            for clip_id in clip_ids:
                # ENclipfile
                # ENfileEN: {clip_id}_{title}.mp4
                clip_path = self.clips_dir / f"{clip_id}_*.mp4"
                found_clips = list(self.clips_dir.glob(f"{clip_id}_*.mp4"))
                
                if found_clips:
                    found_clip = found_clips[0]  # ENfile
                    clips_list.append(found_clip)
                    logger.info(f"ENcollection {collection_id} ENclip: {found_clip.name}")
                else:
                    logger.warning(f"not foundcollection {collection_id} ENclip {clip_id}")
            
            if clips_list:
                # usecollection_titleENfileEN，EN
                safe_title = VideoProcessor.sanitize_filename(collection_title)
                output_path = self.collections_dir / f"{safe_title}.mp4"
                
                if VideoProcessor.create_collection(clips_list, output_path):
                    # generatecollectionEN
                    thumbnail_path = None
                    try:
                        thumbnail_filename = f"{collection_id}_{safe_title}_thumbnail.jpg"
                        thumbnail_path = self.collections_dir / thumbnail_filename
                        
                        # ENvideoEN（EN2EN）
                        thumbnail_success = VideoProcessor.extract_thumbnail(output_path, thumbnail_path, time_offset=2)
                        if thumbnail_success:
                            logger.info(f"collection {collection_id} ENgeneratesucceeded: {thumbnail_path}")
                        else:
                            logger.warning(f"collection {collection_id} ENgeneratefailed")
                            thumbnail_path = None
                    except Exception as e:
                        logger.error(f"generatecollection {collection_id} EN: {e}")
                        thumbnail_path = None
                    
                    # returnENvideopathENpathEN
                    collection_info = {
                        'collection_id': collection_id,
                        'video_path': str(output_path),
                        'thumbnail_path': str(thumbnail_path) if thumbnail_path else None,
                        'title': collection_title
                    }
                    successful_collections.append(collection_info)
                    logger.info(f"succeededcreatecollection {collection_id}: {output_path}")
            else:
                logger.warning(f"collection {collection_id} ENclipfile")
        
        return successful_collections