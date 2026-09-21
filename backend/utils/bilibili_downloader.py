#!/usr/bin/env python3
"""
Bsitevideodownloadtranslated - Based onyt-dlptranslatedBsitevideoAndsubtitlesdownload
translatedAuto Clippingtoolprojecttranslated
"""

import os
import re
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import yt_dlp

try:
    from .error_handler import FileIOError, ValidationError, ProcessingError
except ImportError:
    # translatedRuntime'simport
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from ..utils.error_handler import FileIOError, ValidationError, ProcessingError

logger = logging.getLogger(__name__)

class BilibiliVideoInfo:
    """Bsitevideoinfotranslated"""
    def __init__(self, info_dict: Dict[str, Any]):
        self.bvid = info_dict.get('id', '')
        self.title = info_dict.get('title', 'unknown_video')
        self.duration = info_dict.get('duration', 0)
        self.uploader = info_dict.get('uploader', 'unknown')
        self.description = info_dict.get('description', '')
        self.thumbnail_url = info_dict.get('thumbnail', '')
        self.view_count = info_dict.get('view_count', 0)
        self.upload_date = info_dict.get('upload_date', '')
        self.webpage_url = info_dict.get('webpage_url', '')
    
    def to_dict(self) -> Dict[str, Any]:
        """translatedformat"""
        return {
            'bvid': self.bvid,
            'title': self.title,
            'duration': self.duration,
            'uploader': self.uploader,
            'description': self.description,
            'thumbnail_url': self.thumbnail_url,
            'view_count': self.view_count,
            'upload_date': self.upload_date,
            'webpage_url': self.webpage_url
        }

class BilibiliDownloader:
    """Bsitevideodownloadtranslated"""
    
    def __init__(self, download_dir: Optional[Path] = None, browser: Optional[str] = None):
        """
        translateddownloadtranslated
        
        Args:
            download_dir: downloaddirectory，defaulttranslateddirectory
            browser: translated，usetranslatedfetchcookies
        """
        self.download_dir = download_dir or Path.cwd()
        self.browser = browser
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
    def validate_bilibili_url(self, url: str) -> bool:
        """
        verifyBsitevideotranslatedformat
        
        Args:
            url: videotranslated
            
        Returns:
            Istranslated'sBsitetranslated
        """
        bilibili_patterns = [
            r'https?://www\.bilibili\.com/video/[Bb][Vv][0-9A-Za-z]+',
            r'https?://bilibili\.com/video/[Bb][Vv][0-9A-Za-z]+',
            r'https?://b23\.tv/[0-9A-Za-z]+',
            r'https?://www\.bilibili\.com/video/av\d+',
            r'https?://bilibili\.com/video/av\d+'
        ]
        
        return any(re.match(pattern, url) for pattern in bilibili_patterns)
    
    async def get_video_info(self, url: str) -> BilibiliVideoInfo:
        """
        fetchvideoinfo（translateddownload）
        
        Args:
            url: videotranslated
            
        Returns:
            videoinfotranslated
        """
        if not self.validate_bilibili_url(url):
            raise ValidationError(f"translated'sBsitevideotranslated: {url}")
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        if self.browser:
            ydl_opts['cookiesfrombrowser'] = (self.browser.lower(),)
        
        try:
            loop = asyncio.get_event_loop()
            info_dict = await loop.run_in_executor(
                None, 
                self._extract_info_sync, 
                url, 
                ydl_opts
            )
            return BilibiliVideoInfo(info_dict)
        except Exception as e:
            raise ProcessingError(f"fetchvideoinfofailed: {str(e)}")
    
    def _extract_info_sync(self, url: str, ydl_opts: Dict[str, Any]) -> Dict[str, Any]:
        """translatedvideoinfo"""
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    
    async def download_video_and_subtitle(
        self, 
        url: str, 
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> Dict[str, str]:
        """
        downloadvideoAndsubtitlesfile
        
        Args:
            url: videotranslated
            progress_callback: progresstranslated，translated(statusinfo, progresstranslated)
            
        Returns:
            Packageincludevideo_pathAndsubtitle_path'stranslated
        """
        if not self.validate_bilibili_url(url):
            raise ValidationError(f"translated'sBsitevideotranslated: {url}")
        
        # fetchvideoinfo
        video_info = await self.get_video_info(url)
        
        # cleanfiletranslated，translated
        safe_title = self._sanitize_filename(video_info.title)
        
        # settingsdownloadSelecttranslated - translatedsubtitlesdownloadtranslated
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'writesubtitles': True,
            'writeautomaticsub': True,  # translateddownloadtranslatedgenerate subtitles
            'subtitleslangs': ['ai-zh', 'zh-Hans', 'zh', 'en'],  # multitranslatedsubtitlesLanguage
            'subtitlesformat': 'srt',  # translatedSRTformat
            'outtmpl': str(self.download_dir / f'{safe_title}.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'progress': True,
            'no_warnings': False,  # translatedinfotranslated
        }
        
        if self.browser:
            ydl_opts['cookiesfrombrowser'] = (self.browser.lower(),)
        
        # translatedAdd totranslated
        if progress_callback:
            ydl_opts['progress_hooks'] = [self._create_progress_hook(progress_callback)]
        
        try:
            if progress_callback:
                progress_callback("translateddownloadvideoAndsubtitles...", 0)
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._download_sync,
                url,
                ydl_opts
            )
            
            # translateddownload'sfile
            video_path = self._find_downloaded_video(safe_title)
            subtitle_path = self._find_downloaded_subtitle(safe_title)
            
            # iftranslatedNo.onetranslatedsubtitles，translated'ssubtitlesfetchtranslated
            if not subtitle_path:
                logger.info("No.onetranslatedsubtitlesdownloadfailed，translatedusetranslated...")
                subtitle_path = await self._try_alternative_subtitle_strategies(url, safe_title)
            
            if progress_callback:
                progress_callback("downloadtranslated", 100)
            
            result = {
                'video_path': str(video_path) if video_path else '',
                'subtitle_path': str(subtitle_path) if subtitle_path else '',
                'video_info': video_info.to_dict()
            }
            
            logger.info(f"downloadtranslated: {video_info.title}")
            return result
            
        except Exception as e:
            error_msg = f"downloadfailed: {str(e)}"
            if progress_callback:
                progress_callback(error_msg, 0)
            raise ProcessingError(error_msg)
    
    async def _try_alternative_subtitle_strategies(self, url: str, safe_title: str) -> Optional[Path]:
        """translatedmultitranslatedsubtitlesfetchtranslated"""
        strategies = [
            self._try_download_with_different_langs,
            self._try_download_without_cookies,
            self._try_extract_from_video_metadata
        ]
        
        for strategy in strategies:
            try:
                subtitle_path = await strategy(url, safe_title)
                if subtitle_path:
                    logger.info(f"translatedusesubtitlestranslatedsucceeded: {strategy.__name__}")
                    return subtitle_path
            except Exception as e:
                logger.warning(f"translatedusesubtitlestranslatedfailed {strategy.__name__}: {e}")
                continue
        
        logger.warning("translatedsubtitlesfetchtranslatedfailedtranslated")
        return None
    
    async def _try_download_with_different_langs(self, url: str, safe_title: str) -> Optional[Path]:
        """translateddownloadtranslatedLanguage'ssubtitles"""
        logger.info("translateddownloadtranslatedLanguage'ssubtitles...")
        
        # translated'ssubtitlesLanguagetranslated
        lang_combinations = [
            ['zh-Hans', 'zh'],  # translated
            ['en', 'en-US'],    # translated
            ['ai-zh'],          # AItranslatedsubtitles
            ['auto']            # translated
        ]
        
        for langs in lang_combinations:
            try:
                ydl_opts = {
                    'skip_download': True,  # translateddownloadsubtitles，translateddownloadvideo
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': langs,
                    'subtitlesformat': 'srt',
                    'outtmpl': str(self.download_dir / f'{safe_title}_sub.%(ext)s'),
                    'noplaylist': True,
                    'quiet': True,
                }
                
                if self.browser:
                    ydl_opts['cookiesfrombrowser'] = (self.browser.lower(),)
                
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self._download_sync, url, ydl_opts)
                
                # translatedsubtitlesfile
                subtitle_path = self._find_downloaded_subtitle(safe_title + "_sub")
                if subtitle_path:
                    return subtitle_path
                    
            except Exception as e:
                logger.debug(f"translatedLanguage {langs} failed: {e}")
                continue
        
        return None
    
    async def _try_download_without_cookies(self, url: str, safe_title: str) -> Optional[Path]:
        """translatedusecookiesdownloadsubtitles（translatedsubtitlescantranslatedNo needtranslated）"""
        logger.info("translatedusecookiesdownloadsubtitles...")
        
        try:
            ydl_opts = {
                'skip_download': True,  # translateddownloadsubtitles，translateddownloadvideo
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['zh-Hans', 'zh', 'en'],
                'subtitlesformat': 'srt',
                'outtmpl': str(self.download_dir / f'{safe_title}_nocookie.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
            }
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._download_sync, url, ydl_opts)
            
            subtitle_path = self._find_downloaded_subtitle(safe_title + "_nocookie")
            return subtitle_path
            
        except Exception as e:
            logger.debug(f"translatedusecookiesdownloadfailed: {e}")
            return None
    
    async def _try_extract_from_video_metadata(self, url: str, safe_title: str) -> Optional[Path]:
        """translatedfromvideotranslatedsubtitlesinfo"""
        logger.info("translatedfromvideotranslatedsubtitlesinfo...")
        
        try:
            # fetchvideotranslatedinfo
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            if self.browser:
                ydl_opts['cookiesfrombrowser'] = (self.browser.lower(),)
            
            loop = asyncio.get_event_loop()
            info_dict = await loop.run_in_executor(None, self._extract_info_sync, url, ydl_opts)
            
            # checkIstranslatedsubtitlesinfo
            subtitles = info_dict.get('subtitles', {})
            auto_subtitles = info_dict.get('automatic_captions', {})
            
            if subtitles or auto_subtitles:
                logger.info(f"translatedsubtitlesinfo: {list(subtitles.keys()) + list(auto_subtitles.keys())}")
                # thistranslatedcantranslatedonetranslatedprocesssubtitlesinfo
                return None  # translatedreturnNone，translatedcantranslated
            
            return None
            
        except Exception as e:
            logger.debug(f"translatedvideotranslatedfailed: {e}")
            return None
    
    def _download_sync(self, url: str, ydl_opts: Dict[str, Any]):
        """translateddownload"""
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
    def _create_progress_hook(self, progress_callback: Callable[[str, float], None]):
        """createprogresstranslated"""
        def progress_hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d and d['total_bytes']:
                    progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                elif '_percent_str' in d:
                    # fromtranslated
                    percent_str = d['_percent_str'].strip().rstrip('%')
                    try:
                        progress = float(percent_str)
                    except ValueError:
                        progress = 0
                else:
                    progress = 0
                
                speed = d.get('_speed_str', '')
                eta = d.get('_eta_str', '')
                status = f"downloadtranslated... {speed} ETA: {eta}"
                progress_callback(status, progress)
            elif d['status'] == 'finished':
                progress_callback("downloadtranslated，translatedinprocess...", 95)
        
        return progress_hook
    
    def _sanitize_filename(self, filename: str) -> str:
        """cleanfiletranslated，translated"""
        # translatedortranslated'stranslated
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        
        # translatedfiletranslated
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename.strip()
    
    def _find_downloaded_video(self, title: str) -> Optional[Path]:
        """translateddownload'svideofile"""
        possible_extensions = ['.mp4', '.mkv', '.webm', '.flv']
        
        for ext in possible_extensions:
            video_path = self.download_dir / f"{title}{ext}"
            if video_path.exists():
                return video_path
        
        # iftranslatedfailed，translated
        for file_path in self.download_dir.glob(f"{title}*"):
            if file_path.suffix.lower() in possible_extensions:
                return file_path
        
        return None
    
    def _find_downloaded_subtitle(self, title: str) -> Optional[Path]:
        """translateddownload'ssubtitlesfile - translatedversion，translatedAIsubtitles"""
        logger.info(f"translatedintranslatedsubtitlesfile，translated: {title}")
        
        # translatedcheckAIsubtitlesfile
        ai_subtitle_path = self.download_dir / f"{title}.ai-zh.srt"
        if ai_subtitle_path.exists():
            # translatedformat
            standard_path = self.download_dir / f"{title}.srt"
            if not standard_path.exists():
                ai_subtitle_path.rename(standard_path)
                logger.info(f"translatedAIsubtitlesfile: {title}.ai-zh.srt -> {title}.srt")
                return standard_path
            return ai_subtitle_path
        
        # checkIstranslatedIstranslatedformat
        standard_path = self.download_dir / f"{title}.srt"
        if standard_path.exists():
            logger.info(f"translatedsubtitlesfile: {title}.srt")
            return standard_path
        
        # translatedsubtitlesfile
        for file_path in self.download_dir.glob(f"{title}*.srt"):
            logger.info(f"translatedsubtitlesfile: {file_path.name}")
            return file_path
        
        logger.warning(f"translatedsubtitlesfile，translated: {title}")
        return None
    
    def _convert_vtt_to_srt(self, vtt_path: Path, srt_path: Path):
        """translatedVTTsubtitlesfiletranslatedSRTformat"""
        try:
            with open(vtt_path, 'r', encoding='utf-8') as vtt_file:
                vtt_content = vtt_file.read()
            
            # translated'sVTTtranslatedSRTtranslated
            lines = vtt_content.split('\n')
            srt_lines = []
            subtitle_count = 1
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # skipVTTtranslatedinfo
                if line.startswith('WEBVTT') or line.startswith('NOTE') or not line:
                    i += 1
                    continue
                
                # translated
                if '-->' in line:
                    # translatedformat (VTTusetranslated，SRTusetranslated)
                    time_line = line.replace('.', ',')
                    srt_lines.append(str(subtitle_count))
                    srt_lines.append(time_line)
                    
                    # fetchsubtitlestranslated
                    i += 1
                    subtitle_text = []
                    while i < len(lines) and lines[i].strip():
                        subtitle_text.append(lines[i].strip())
                        i += 1
                    
                    srt_lines.extend(subtitle_text)
                    srt_lines.append('')  # translated
                    subtitle_count += 1
                
                i += 1
            
            # translatedSRTfile
            with open(srt_path, 'w', encoding='utf-8') as srt_file:
                srt_file.write('\n'.join(srt_lines))
                
        except Exception as e:
            logger.error(f"VTTtranslatedSRTtranslatedfailed: {e}")
            raise
    
    def cleanup_temp_files(self, title: str):
        """clean temp files"""
        try:
            # cleancantranslated'stranslatedfile
            for pattern in [f"{title}*.part", f"{title}*.tmp", f"{title}*.ytdl"]:
                for temp_file in self.download_dir.glob(pattern):
                    temp_file.unlink(missing_ok=True)
        except Exception as e:
            logger.warning(f"clean temp filesfailed: {e}")

# translated
async def download_bilibili_video(
    url: str, 
    download_dir: Optional[Path] = None,
    browser: Optional[str] = None,
    progress_callback: Optional[Callable[[str, float], None]] = None
) -> Dict[str, str]:
    """
    translated'sBsitevideodownloadtranslated
    
    Args:
        url: Bsitevideotranslated
        download_dir: downloaddirectory
        browser: translated
        progress_callback: progresstranslated
        
    Returns:
        Packageincludevideo_pathAndsubtitle_path'stranslated
    """
    downloader = BilibiliDownloader(download_dir, browser)
    return await downloader.download_video_and_subtitle(url, progress_callback)

async def get_bilibili_video_info(url: str, browser: Optional[str] = None) -> BilibiliVideoInfo:
    """
    translated'sBsitevideoinfofetchtranslated
    
    Args:
        url: Bsitevideotranslated
        browser: translated
        
    Returns:
        videoinfotranslated
    """
    downloader = BilibiliDownloader(browser=browser)
    return await downloader.get_video_info(url)