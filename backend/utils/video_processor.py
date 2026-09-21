"""
videoprocesstool
"""
import subprocess
import json
import logging
import re
from typing import List, Dict, Optional
from pathlib import Path
from .ffmpeg_utils import get_ffmpeg_path, get_ffprobe_path

# fixedimportissue
try:
    from ..core.shared_config import CLIPS_DIR, COLLECTIONS_DIR
except ImportError:
    # iftranslatedimportfailed，translatedimport
    import sys
    from pathlib import Path
    backend_path = Path(__file__).parent.parent
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    from ..core.shared_config import CLIPS_DIR, COLLECTIONS_DIR

logger = logging.getLogger(__name__)

class VideoProcessor:
    """videoprocesstooltranslated"""
    
    def __init__(self, clips_dir: Optional[str] = None, collections_dir: Optional[str] = None):
        # translatedusetranslated'sprojecttranslatedpath，translatedusetranslatedpathtranslated
        if not clips_dir:
            raise ValueError("clips_dir translatedIstranslated's，translatedusetranslatedpath")
        if not collections_dir:
            raise ValueError("collections_dir translatedIstranslated's，translatedusetranslatedpath")
        
        self.clips_dir = Path(clips_dir)
        self.collections_dir = Path(collections_dir)
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        cleanfiletranslated，translatedortranslated'stranslated
        
        Args:
            filename: translatedfiletranslated
            
        Returns:
            cleantranslated'sfiletranslated
        """
        # translatedortranslated'stranslated
        # WindowsAndUnixSystemtranslated'stranslated: < > : " | ? * \ /
        # translated
        sanitized = re.sub(r'[<>:"|?*\\/]', '_', filename)
        
        # translatedAndtranslated
        sanitized = sanitized.strip(' .')
        
        # translated，translatedfiletranslated
        if len(sanitized) > 100:
            sanitized = sanitized[:100]
        
        # ensurefiletranslated
        if not sanitized:
            sanitized = "untitled"
            
        return sanitized
    
    @staticmethod
    def convert_srt_time_to_ffmpeg_time(srt_time: str) -> str:
        """
        translatedSRTtranslatedformattranslatedFFmpegtranslatedformat
        
        Args:
            srt_time: SRTtranslatedformat (if "00:00:06,140" or "00:00:06.140")
            
        Returns:
            FFmpegtranslatedformat (if "00:00:06.140")
        """
        # translated
        return srt_time.replace(',', '.')
    
    @staticmethod
    def convert_seconds_to_ffmpeg_time(seconds: float) -> str:
        """
        translatedsecondstranslatedFFmpegtranslatedformat
        
        Args:
            seconds: secondstranslated
            
        Returns:
            FFmpegtranslatedformat (if "00:00:06.140")
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"
    
    @staticmethod
    def convert_ffmpeg_time_to_seconds(time_str: str) -> float:
        """
        translatedFFmpegtranslatedformattranslatedsecondstranslated
        
        Args:
            time_str: FFmpegtranslatedformat (if "00:00:06.140")
            
        Returns:
            secondstranslated
        """
        try:
            # processtranslatedsecondstranslated
            if '.' in time_str:
                time_part, ms_part = time_str.split('.')
                milliseconds = int(ms_part)
            else:
                time_part = time_str
                milliseconds = 0
            
            # translatedseconds
            h, m, s = map(int, time_part.split(':'))
            
            return h * 3600 + m * 60 + s + milliseconds / 1000
        except Exception as e:
            logger.error(f"translatedformattranslatedfailed: {time_str}, error: {e}")
            return 0.0
    
    @staticmethod
    def extract_clip(input_video: Path, output_path: Path, 
                    start_time: str, end_time: str) -> bool:
        """
        fromvideotranslated'stranslated
        
        Args:
            input_video: translatedvideopath
            output_path: translatedvideopath
            start_time: translated (format: "00:01:25,140")
            end_time: translated (format: "00:02:53,500")
            
        Returns:
            Istranslatedsucceeded
        """
        try:
            # ensuretranslateddirectorytranslatedin
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # translatedformat：fromSRTformattranslatedFFmpegformat
            ffmpeg_start_time = VideoProcessor.convert_srt_time_to_ffmpeg_time(start_time)
            ffmpeg_end_time = VideoProcessor.convert_srt_time_to_ffmpeg_time(end_time)
            
            # translated
            start_seconds = VideoProcessor.convert_ffmpeg_time_to_seconds(ffmpeg_start_time)
            end_seconds = VideoProcessor.convert_ffmpeg_time_to_seconds(ffmpeg_end_time)
            duration = end_seconds - start_seconds
            
            # translated'sFFmpegtranslated
            # use -ss intranslated，use -t translated
            ffmpeg_bin = get_ffmpeg_path()
            cmd = [
                ffmpeg_bin,
                '-ss', ffmpeg_start_time,  # intranslated，translated
                '-i', str(input_video),
                '-t', str(duration),  # usetranslatedIstranslated
                '-c:v', 'copy',  # translatedvideotranslated
                '-c:a', 'copy',  # translated
                '-avoid_negative_ts', 'make_zero',
                '-y',  # translatedfile
                str(output_path)
            ]
            
            # translated
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            if result.returncode == 0:
                logger.info(f"succeededtranslatedvideotranslated: {output_path} ({ffmpeg_start_time} -> {ffmpeg_end_time}, translated: {duration:.2f}seconds)")
                return True
            else:
                logger.error(f"translatedvideotranslatedfailed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"videoprocesstranslated: {str(e)}")
            return False
    
    @staticmethod
    def create_collection(clips_list: List[Path], output_path: Path) -> bool:
        """
        translatedmulti videotranslatedcollection
        
        Args:
            clips_list: videotranslatedpathlist
            output_path: translatedcollectionpath
            
        Returns:
            Istranslatedsucceeded
        """
        try:
            # verifytranslated
            if not clips_list:
                logger.error("clips_listtranslated，translatedcreatecollection")
                return False
            
            # verifytranslatedvideofileIstranslatedin
            valid_clips = []
            for clip_path in clips_list:
                if not clip_path.exists():
                    logger.warning(f"videofile not found，skip: {clip_path}")
                    continue
                valid_clips.append(clip_path)
            
            if not valid_clips:
                logger.error("translated'svideofile，translatedcreatecollection")
                return False
            
            # ensuretranslateddirectorytranslatedin
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # createconcatfile
            concat_file = output_path.parent / "concat_list.txt"
            
            with open(concat_file, 'w', encoding='utf-8') as f:
                for clip_path in valid_clips:
                    # usetranslatedpathtranslated
                    abs_path = clip_path.absolute()
                    escaped_path = str(abs_path).replace("'", "'\"'\"'")
                    f.write(f"file '{escaped_path}'\n")
            
            # verifyconcatfiletranslated
            if concat_file.stat().st_size == 0:
                logger.error("concatfiletranslated，translatedcreatecollection")
                concat_file.unlink(missing_ok=True)
                return False
            
            # translatedFFmpegtranslated - useH.264translatedensuretranslated
            ffmpeg_bin = get_ffmpeg_path()
            cmd = [
                ffmpeg_bin,
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-c:v', 'libx264',  # useH.264videotranslated
                '-preset', 'ultrafast',  # usetranslated'stranslated
                '-crf', '28',  # translated
                '-c:a', 'aac',  # useAACtranslated
                '-b:a', '128k',  # translated
                '-movflags', '+faststart',  # translated
                '-y',
                str(output_path)
            ]
            
            logger.info(f"translatedFFmpegtranslated: {' '.join(cmd)}")
            
            # translated
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            # clean temp files
            concat_file.unlink(missing_ok=True)
            
            if result.returncode == 0:
                logger.info(f"succeededcreatecollection: {output_path}")
                return True
            else:
                logger.error(f"createcollectionfailed: {result.stderr}")
                logger.error(f"FFmpeg stdout: {result.stdout}")
                return False
                
        except Exception as e:
            logger.error(f"videotranslated: {str(e)}")
            return False
    
    @staticmethod
    def extract_thumbnail(video_path: Path, output_path: Path, time_offset: int = 5) -> bool:
        """
        fromvideotranslated
        
        Args:
            video_path: videofile path
            output_path: translatedpath
            time_offset: translated（seconds）
            
        Returns:
            Istranslatedsucceeded
        """
        try:
            # ensuretranslateddirectorytranslatedin
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # translatedFFmpegtranslated
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-ss', str(time_offset),
                '-vframes', '1',
                '-q:v', '2',  # translated
                '-y',  # translatedfile
                str(output_path)
            ]
            
            # translated
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            if result.returncode == 0 and output_path.exists():
                logger.info(f"succeededtranslated: {output_path}")
                return True
            else:
                logger.error(f"translatedfailed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"translated: {str(e)}")
            return False
    
    @staticmethod
    def get_video_info(video_path: Path) -> Dict:
        """
        fetchvideoinfo
        
        Args:
            video_path: videofile path
            
        Returns:
            videoinfotranslated
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
                logger.error(f"fetchvideoinfofailed: {result.stderr}")
                return {}
                
        except Exception as e:
            logger.error(f"fetchvideoinfotranslated: {str(e)}")
            return {}
    
    def batch_extract_clips(self, input_video: Path, clips_data: List[Dict]) -> List[Path]:
        """
        translatedvideotranslated
        
        Args:
            input_video: translatedvideopath
            clips_data: translatedlist，per translatedPackageincludeid、title、start_time、end_time
            
        Returns:
            succeededtranslated'stranslatedpathlist
        """
        successful_clips = []
        
        for clip_data in clips_data:
            clip_id = clip_data['id']
            title = clip_data.get('title', f"translated_{clip_id}")
            start_time = clip_data['start_time']
            end_time = clip_data['end_time']
            
            # processtranslatedformat - iftranslatedIssecondstranslated，translatedSRTformat
            if isinstance(start_time, (int, float)):
                start_time = VideoProcessor.convert_seconds_to_ffmpeg_time(start_time)
            if isinstance(end_time, (int, float)):
                end_time = VideoProcessor.convert_seconds_to_ffmpeg_time(end_time)
            
            # usetranslatedfiletranslated，translatedcleantranslated'stranslated
            # infiletranslatedPackageincludeclip_id，translatedcollectiontranslated
            safe_title = VideoProcessor.sanitize_filename(title)
            output_path = self.clips_dir / f"{clip_id}_{safe_title}.mp4"
            
            logger.info(f"translatedclip {clip_id}: {start_time} -> {end_time}, translated: {output_path}")
            
            if VideoProcessor.extract_clip(input_video, output_path, start_time, end_time):
                successful_clips.append(output_path)
                logger.info(f"clip {clip_id} translatedsucceeded")
            else:
                logger.error(f"clip {clip_id} translatedfailed")
        
        return successful_clips
    
    def create_collections_from_metadata(self, collections_data: List[Dict]) -> List[Dict]:
        """
        translatedcreatecollection
        
        Args:
            collections_data: collectiontranslatedlist
            
        Returns:
            succeededcreate'scollectioninfolist，PackageincludevideopathAndtranslatedpath
        """
        successful_collections = []
        
        for collection_data in collections_data:
            collection_id = collection_data['id']
            collection_title = collection_data.get('collection_title', f'collection_{collection_id}')
            clip_ids = collection_data['clip_ids']
            
            # translatedpathlist
            clips_list = []
            for clip_id in clip_ids:
                # translated'sclipfile
                # translated'sfiletranslatedformatIs: {clip_id}_{title}.mp4
                clip_path = self.clips_dir / f"{clip_id}_*.mp4"
                found_clips = list(self.clips_dir.glob(f"{clip_id}_*.mp4"))
                
                if found_clips:
                    found_clip = found_clips[0]  # translatedNo.one translated'sfile
                    clips_list.append(found_clip)
                    logger.info(f"translatedcollection {collection_id} 'sclip: {found_clip.name}")
                else:
                    logger.warning(f"translatedcollection {collection_id} 'sclip {clip_id}")
            
            if clips_list:
                # usecollection_titletranslatedfiletranslated，translatedcleantranslated'stranslated
                safe_title = VideoProcessor.sanitize_filename(collection_title)
                output_path = self.collections_dir / f"{safe_title}.mp4"
                
                if VideoProcessor.create_collection(clips_list, output_path):
                    # translatedcollectiontranslated
                    thumbnail_path = None
                    try:
                        thumbnail_filename = f"{collection_id}_{safe_title}_thumbnail.jpg"
                        thumbnail_path = self.collections_dir / thumbnail_filename
                        
                        # fromvideotranslated（No.2seconds'stranslated）
                        thumbnail_success = VideoProcessor.extract_thumbnail(output_path, thumbnail_path, time_offset=2)
                        if thumbnail_success:
                            logger.info(f"collection {collection_id} translatedsucceeded: {thumbnail_path}")
                        else:
                            logger.warning(f"collection {collection_id} translatedfailed")
                            thumbnail_path = None
                    except Exception as e:
                        logger.error(f"translatedcollection {collection_id} translated: {e}")
                        thumbnail_path = None
                    
                    # returnPackageincludevideopathAndtranslatedpath'sinfo
                    collection_info = {
                        'collection_id': collection_id,
                        'video_path': str(output_path),
                        'thumbnail_path': str(thumbnail_path) if thumbnail_path else None,
                        'title': collection_title
                    }
                    successful_collections.append(collection_info)
                    logger.info(f"succeededcreatecollection {collection_id}: {output_path}")
            else:
                logger.warning(f"collection {collection_id} translated'sclipfile")
        
        return successful_collections