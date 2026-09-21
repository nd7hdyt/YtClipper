"""
videoENgenerateEN
"""
import subprocess
import logging
from pathlib import Path
from typing import Optional
import base64
from PIL import Image
import io
from .ffmpeg_utils import get_ffmpeg_path, get_ffprobe_path

logger = logging.getLogger(__name__)

class ThumbnailGenerator:
    """videoENgenerateEN"""
    
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv']
    
    def generate_thumbnail(self, video_path: Path, output_path: Optional[Path] = None, 
                          time_offset: Optional[float] = None, width: int = 320, height: int = 180) -> Optional[Path]:
        """
        generatevideoEN - useEN
        
        Args:
            video_path: videofilepath
            output_path: ENpath，ifENNonethenENgenerate
            time_offset: ENtimeEN（EN），ifENNonethenENtimeEN
            width: EN
            height: EN
            
        Returns:
            generateENpath，failedreturnNone
        """
        try:
            if not video_path.exists():
                logger.error(f"videofiledoes not exist: {video_path}")
                return None
            
            # checkfileEN
            if video_path.suffix.lower() not in self.supported_formats:
                logger.error(f"ENvideoEN: {video_path.suffix}")
                return None
            
            # generateENpath
            if output_path is None:
                output_path = video_path.parent / f"{video_path.stem}_thumbnail.jpg"
            
            # ENdirectoryEN
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # ENtimeEN
            if time_offset is None:
                time_offset = self._get_optimal_thumbnail_time(video_path)
            
            # checkENusevideoEN
            if time_offset == -1.0:
                # usevideoEN
                cover_path = video_path.parent / f"{video_path.stem}_cover.jpg"
                if cover_path.exists():
                    # ENfileEN
                    ffmpeg_bin = get_ffmpeg_path()
                    cmd = [
                        ffmpeg_bin,
                        '-i', str(cover_path),
                        '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black',
                        '-q:v', '2',
                        '-y',
                        str(output_path)
                    ]
                    logger.info(f"usevideoENgenerateEN: {cover_path} -> {output_path}")
                else:
                    # ENdoes not exist，ENtimeEN
                    time_offset = 1.0
                    cmd = [
                        'ffmpeg',
                        '-ss', str(time_offset),
                        '-i', str(video_path),
                        '-vframes', '1',
                        '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black',
                        '-q:v', '2',
                        '-y',
                        str(output_path)
                    ]
                    logger.info(f"ENdoes not exist，ENtimeEN: {time_offset}EN")
            else:
                # useENtimeEN
                logger.info(f"ENvideo {video_path.name} ENtimeEN: {time_offset}EN")
                ffmpeg_bin = get_ffmpeg_path()
                cmd = [
                    ffmpeg_bin,
                    '-ss', str(time_offset),  # ENtime
                    '-i', str(video_path),    # ENvideo
                    '-vframes', '1',          # EN
                    '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black',  # EN
                    '-q:v', '2',              # EN
                    '-y',                     # ENfile
                    str(output_path)
                ]
            
            logger.info(f"generateEN: {video_path} -> {output_path}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"ENgeneratesucceeded: {output_path}")
                return output_path
            else:
                logger.error(f"ENgeneratefailed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"ENgeneratetimeout: {video_path}")
            return None
        except Exception as e:
            logger.error(f"ENgenerateexception: {e}")
            return None
    
    def _extract_video_cover(self, video_path: Path) -> Optional[Path]:
        """
        ENvideoEN
        
        Args:
            video_path: videofilepath
            
        Returns:
            ENpath，ifdoes not existthenreturnNone
        """
        try:
            # checkEN
            ffmpeg_bin = get_ffmpeg_path()
            cmd = [
                ffmpeg_bin,
                '-i', str(video_path),
                '-an',  # EN
                '-vcodec', 'copy',  # ENvideoEN
                '-f', 'image2',
                '-vframes', '1',
                '-y',
                str(video_path.parent / f"{video_path.stem}_cover.jpg")
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                cover_path = video_path.parent / f"{video_path.stem}_cover.jpg"
                if cover_path.exists() and cover_path.stat().st_size > 0:
                    logger.info(f"succeededENvideoEN: {cover_path}")
                    return cover_path
            
            return None
            
        except Exception as e:
            logger.debug(f"ENvideoENfailed: {e}")
            return None
    
    def _get_optimal_thumbnail_time(self, video_path: Path) -> float:
        """
        ENtimeEN
        
        EN：
        1. ENvideoEN（ifEN）
        2. ifvideoEN（<30EN），EN
        3. ifvideoEN（30EN-5EN），EN10%EN
        4. ifvideoEN（>5EN），EN5%EN
        5. EN，becausetheseEN
        
        Args:
            video_path: videofilepath
            
        Returns:
            ENtimeEN（EN）
        """
        try:
            # ENvideoEN
            cover_path = self._extract_video_cover(video_path)
            if cover_path:
                logger.info(f"usevideoEN: {cover_path}")
                # ifsucceededEN，returnENuseEN
                return -1.0  # EN，ENuseEN
            
            # fetchvideoEN
            video_info = self.get_video_info(video_path)
            if not video_info:
                logger.warning(f"cannotfetchvideoEN，useENtimeEN: {video_path}")
                return 1.0
            
            # fetchvideoduration
            duration = float(video_info.get('format', {}).get('duration', 0))
            if duration <= 0:
                logger.warning(f"videodurationEN0，useENtimeEN: {video_path}")
                return 1.0
            
            logger.info(f"videoduration: {duration}EN")
            
            # ENtimeEN
            if duration < 30:
                # ENvideo：EN
                optimal_time = duration * 0.5
            elif duration < 300:  # 5EN
                # EN：EN10%EN，ENmayEN
                optimal_time = duration * 0.1
            else:
                # ENvideo：EN5%EN
                optimal_time = duration * 0.05
            
            # ENtimeEN（EN1EN，ENvideoEN）
            optimal_time = max(1.0, min(optimal_time, duration - 1))
            
            logger.info(f"ENvideo {video_path.name} ENtimeEN: {optimal_time}EN (ENduration: {duration}EN)")
            return optimal_time
            
        except Exception as e:
            logger.error(f"ENtimeENfailed: {e}")
            return 1.0
    
    def generate_thumbnail_base64(self, video_path: Path, time_offset: Optional[float] = None, 
                                 width: int = 320, height: int = 180) -> Optional[str]:
        """
        generateENreturnbase64EN
        
        Args:
            video_path: videofilepath
            time_offset: ENtimeEN（EN），ifENNonethenENtimeEN
            width: EN
            height: EN
            
        Returns:
            base64EN，failedreturnNone
        """
        try:
            # generateEN
            temp_path = video_path.parent / f"temp_thumbnail_{video_path.stem}.jpg"
            thumbnail_path = self.generate_thumbnail(video_path, temp_path, time_offset, width, height)
            
            if thumbnail_path and thumbnail_path.exists():
                # readENbase64
                with open(thumbnail_path, 'rb') as f:
                    image_data = f.read()
                    base64_data = base64.b64encode(image_data).decode('utf-8')
                
                # ENfile
                try:
                    temp_path.unlink()
                except:
                    pass
                
                return f"data:image/jpeg;base64,{base64_data}"
            else:
                return None
                
        except Exception as e:
            logger.error(f"generatebase64ENfailed: {e}")
            return None
    
    def get_video_info(self, video_path: Path) -> Optional[dict]:
        """
        fetchvideoEN
        
        Args:
            video_path: videofilepath
            
        Returns:
            videoEN，failedreturnNone
        """
        try:
            if not video_path.exists():
                return None
            
            ffprobe_bin = get_ffprobe_path()
            cmd = [
                ffprobe_bin,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(video_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                import json
                return json.loads(result.stdout)
            else:
                logger.error(f"fetchvideoENfailed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"fetchvideoENexception: {e}")
            return None

# EN
def generate_project_thumbnail(project_id: str, video_path: Path) -> Optional[str]:
    """
    ENprojectgenerateEN
    
    Args:
        project_id: projectID
        video_path: videofilepath
        
    Returns:
        base64EN
    """
    generator = ThumbnailGenerator()
    return generator.generate_thumbnail_base64(video_path)

