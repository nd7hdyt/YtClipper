"""
videotranslatedtool
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
    """videotranslated"""
    
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv']
    
    def generate_thumbnail(self, video_path: Path, output_path: Optional[Path] = None, 
                          time_offset: Optional[float] = None, width: int = 320, height: int = 180) -> Optional[Path]:
        """
        translatedvideotranslated - usetranslatedSelectselecttranslated
        
        Args:
            video_path: videofile path
            output_path: translatedpath，iftranslatedNonetranslated
            time_offset: translated（seconds），iftranslatedNonetranslatedSelectselecttranslated
            width: translated
            height: translated
            
        Returns:
            translated'stranslatedpath，failedreturnNone
        """
        try:
            if not video_path.exists():
                logger.error(f"videofile not found: {video_path}")
                return None
            
            # checkfileformat
            if video_path.suffix.lower() not in self.supported_formats:
                logger.error(f"translatedsupport'svideoformat: {video_path.suffix}")
                return None
            
            # translatedpath
            if output_path is None:
                output_path = video_path.parent / f"{video_path.stem}_thumbnail.jpg"
            
            # ensuretranslateddirectorytranslatedin
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # translatedSelectselecttranslated
            if time_offset is None:
                time_offset = self._get_optimal_thumbnail_time(video_path)
            
            # checkIstranslatedusevideotranslated
            if time_offset == -1.0:
                # usevideotranslated
                cover_path = video_path.parent / f"{video_path.stem}_cover.jpg"
                if cover_path.exists():
                    # translatedfiletranslated
                    ffmpeg_bin = get_ffmpeg_path()
                    cmd = [
                        ffmpeg_bin,
                        '-i', str(cover_path),
                        '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black',
                        '-q:v', '2',
                        '-y',
                        str(output_path)
                    ]
                    logger.info(f"usevideotranslated: {cover_path} -> {output_path}")
                else:
                    # translatednot found，translateddefaulttranslated
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
                    logger.info(f"translatednot found，translateddefaulttranslated: {time_offset}seconds")
            else:
                # usetranslated
                logger.info(f"translatedvideo {video_path.name} Selectselecttranslated: {time_offset}seconds")
                ffmpeg_bin = get_ffmpeg_path()
                cmd = [
                    ffmpeg_bin,
                    '-ss', str(time_offset),  # translated
                    '-i', str(video_path),    # translatedvideo
                    '-vframes', '1',          # translatedonetranslated
                    '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black',  # translated
                    '-q:v', '2',              # translated
                    '-y',                     # translatedfile
                    str(output_path)
                ]
            
            logger.info(f"translated: {video_path} -> {output_path}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"translatedsucceeded: {output_path}")
                return output_path
            else:
                logger.error(f"translatedfailed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"translated: {video_path}")
            return None
        except Exception as e:
            logger.error(f"translated: {e}")
            return None
    
    def _extract_video_cover(self, video_path: Path) -> Optional[Path]:
        """
        translatedvideo'stranslated
        
        Args:
            video_path: videofile path
            
        Returns:
            translatedpath，iftranslatednot foundtranslatedreturnNone
        """
        try:
            # checkIstranslated'stranslated
            ffmpeg_bin = get_ffmpeg_path()
            cmd = [
                ffmpeg_bin,
                '-i', str(video_path),
                '-an',  # translatedusetranslated
                '-vcodec', 'copy',  # translatedvideotranslated
                '-f', 'image2',
                '-vframes', '1',
                '-y',
                str(video_path.parent / f"{video_path.stem}_cover.jpg")
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                cover_path = video_path.parent / f"{video_path.stem}_cover.jpg"
                if cover_path.exists() and cover_path.stat().st_size > 0:
                    logger.info(f"succeededtranslatedvideotranslated: {cover_path}")
                    return cover_path
            
            return None
            
        except Exception as e:
            logger.debug(f"translatedvideotranslatedfailed: {e}")
            return None
    
    def _get_optimal_thumbnail_time(self, video_path: Path) -> float:
        """
        translatedSelectselecttranslated'stranslated
        
        translated：
        1. translatedvideotranslated（iftranslatedin）
        2. iftranslatedvideotranslated（<30seconds），Selectselecttranslated
        3. iftranslatedvideotranslatedetc.translated（30seconds-5minutes），Selectselect10%translated
        4. iftranslatedvideotranslated（>5minutes），Selectselect5%translated
        5. translatedSelectselecttranslatedAndtranslated，translatedthistranslatedIstranslatedortranslated
        
        Args:
            video_path: videofile path
            
        Returns:
            translated（seconds）
        """
        try:
            # translatedvideotranslated
            cover_path = self._extract_video_cover(video_path)
            if cover_path:
                logger.info(f"usevideotranslated: {cover_path}")
                # iftranslatedsucceededtranslated，returnone translatedusetranslated
                return -1.0  # translated，translatedusetranslated
            
            # fetchvideoinfo
            video_info = self.get_video_info(video_path)
            if not video_info:
                logger.warning(f"translatedfetchvideoinfo，usedefaulttranslated: {video_path}")
                return 1.0
            
            # fetchvideotranslated
            duration = float(video_info.get('format', {}).get('duration', 0))
            if duration <= 0:
                logger.warning(f"videotranslated0，usedefaulttranslated: {video_path}")
                return 1.0
            
            logger.info(f"videotranslated: {duration}seconds")
            
            # translatedSelectselecttranslated
            if duration < 30:
                # translatedvideo：Selectselecttranslated
                optimal_time = duration * 0.5
            elif duration < 300:  # 5minutes
                # translatedetc.translated：Selectselect10%translated，translatedcantranslated'stranslated
                optimal_time = duration * 0.1
            else:
                # translatedvideo：Selectselect5%translated
                optimal_time = duration * 0.05
            
            # ensuretranslated（translated1seconds，translatedmultitranslatedvideotranslated）
            optimal_time = max(1.0, min(optimal_time, duration - 1))
            
            logger.info(f"translatedvideo {video_path.name} Selectselecttranslated: {optimal_time}seconds (translated: {duration}seconds)")
            return optimal_time
            
        except Exception as e:
            logger.error(f"Selectselecttranslatedfailed: {e}")
            return 1.0
    
    def generate_thumbnail_base64(self, video_path: Path, time_offset: Optional[float] = None, 
                                 width: int = 320, height: int = 180) -> Optional[str]:
        """
        translatedreturnbase64translated
        
        Args:
            video_path: videofile path
            time_offset: translated（seconds），iftranslatedNonetranslatedSelectselecttranslated
            width: translated
            height: translated
            
        Returns:
            base64translated'stranslated，failedreturnNone
        """
        try:
            # translated
            temp_path = video_path.parent / f"temp_thumbnail_{video_path.stem}.jpg"
            thumbnail_path = self.generate_thumbnail(video_path, temp_path, time_offset, width, height)
            
            if thumbnail_path and thumbnail_path.exists():
                # translatedbase64
                with open(thumbnail_path, 'rb') as f:
                    image_data = f.read()
                    base64_data = base64.b64encode(image_data).decode('utf-8')
                
                # clean temp files
                try:
                    temp_path.unlink()
                except:
                    pass
                
                return f"data:image/jpeg;base64,{base64_data}"
            else:
                return None
                
        except Exception as e:
            logger.error(f"translatedbase64translatedfailed: {e}")
            return None
    
    def get_video_info(self, video_path: Path) -> Optional[dict]:
        """
        fetchvideoinfo
        
        Args:
            video_path: videofile path
            
        Returns:
            videoinfotranslated，failedreturnNone
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
                logger.error(f"fetchvideoinfofailed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"fetchvideoinfotranslated: {e}")
            return None

# translated
def generate_project_thumbnail(project_id: str, video_path: Path) -> Optional[str]:
    """
    translatedprojecttranslated
    
    Args:
        project_id: projectID
        video_path: videofile path
        
    Returns:
        base64translated'stranslated
    """
    generator = ThumbnailGenerator()
    return generator.generate_thumbnail_base64(video_path)

