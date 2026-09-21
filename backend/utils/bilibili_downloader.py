#!/usr/bin/env python3
"""
BENvideodownloadEN - ENyt-dlpENBENvideoENsubtitlesdownload
ENclipENprojectEN
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
    # ENrunEN
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from ..utils.error_handler import FileIOError, ValidationError, ProcessingError

logger = logging.getLogger(__name__)

class BilibiliVideoInfo:
    """BENvideoEN"""
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
        """EN"""
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
    """BENvideodownloadEN"""
    
    def __init__(self, download_dir: Optional[Path] = None, browser: Optional[str] = None):
        """
        initializedownloadEN
        
        Args:
            download_dir: downloaddirectory，ENcurrentdirectory
            browser: EN，ENfetchcookies
        """
        self.download_dir = download_dir or Path.cwd()
        self.browser = browser
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
    def validate_bilibili_url(self, url: str) -> bool:
        """
        validateBENvideoEN
        
        Args:
            url: videoEN
            
        Returns:
            ENBEN
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
        fetchvideoEN（ENdownload）
        
        Args:
            url: videoEN
            
        Returns:
            videoEN
        """
        if not self.validate_bilibili_url(url):
            raise ValidationError(f"ENBENvideoEN: {url}")
        
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
            raise ProcessingError(f"fetchvideoENfailed: {str(e)}")
    
    def _extract_info_sync(self, url: str, ydl_opts: Dict[str, Any]) -> Dict[str, Any]:
        """ENvideoEN"""
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    
    async def download_video_and_subtitle(
        self, 
        url: str, 
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> Dict[str, str]:
        """
        downloadvideoENsubtitlesfile
        
        Args:
            url: videoEN
            progress_callback: progressEN，parametersEN(statusEN, progressEN)
            
        Returns:
            ENvideo_pathENsubtitle_pathEN
        """
        if not self.validate_bilibili_url(url):
            raise ValidationError(f"ENBENvideoEN: {url}")
        
        # fetchvideoEN
        video_info = await self.get_video_info(url)
        
        # ENfileEN，EN
        safe_title = self._sanitize_filename(video_info.title)
        
        # settingsdownloadEN - ENsubtitlesdownloadEN
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'writesubtitles': True,
            'writeautomaticsub': True,  # meanwhileENdownloadENgeneratesubtitles
            'subtitleslangs': ['ai-zh', 'zh-Hans', 'zh', 'en'],  # ENsubtitlesEN
            'subtitlesformat': 'srt',  # ENSRTEN
            'outtmpl': str(self.download_dir / f'{safe_title}.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'progress': True,
            'no_warnings': False,  # ENwarningEN
        }
        
        if self.browser:
            ydl_opts['cookiesfrombrowser'] = (self.browser.lower(),)
        
        # ENprogressEN
        if progress_callback:
            ydl_opts['progress_hooks'] = [self._create_progress_hook(progress_callback)]
        
        try:
            if progress_callback:
                progress_callback("startdownloadvideoENsubtitles...", 0)
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._download_sync,
                url,
                ydl_opts
            )
            
            # ENdownloadENfile
            video_path = self._find_downloaded_video(safe_title)
            subtitle_path = self._find_downloaded_subtitle(safe_title)
            
            # ifENsubtitles，ENsubtitlesfetchEN
            if not subtitle_path:
                logger.info("ENsubtitlesdownloadfailed，EN...")
                subtitle_path = await self._try_alternative_subtitle_strategies(url, safe_title)
            
            if progress_callback:
                progress_callback("downloadEN", 100)
            
            result = {
                'video_path': str(video_path) if video_path else '',
                'subtitle_path': str(subtitle_path) if subtitle_path else '',
                'video_info': video_info.to_dict()
            }
            
            logger.info(f"downloadEN: {video_info.title}")
            return result
            
        except Exception as e:
            error_msg = f"downloadfailed: {str(e)}"
            if progress_callback:
                progress_callback(error_msg, 0)
            raise ProcessingError(error_msg)
    
    async def _try_alternative_subtitle_strategies(self, url: str, safe_title: str) -> Optional[Path]:
        """ENsubtitlesfetchEN"""
        strategies = [
            self._try_download_with_different_langs,
            self._try_download_without_cookies,
            self._try_extract_from_video_metadata
        ]
        
        for strategy in strategies:
            try:
                subtitle_path = await strategy(url, safe_title)
                if subtitle_path:
                    logger.info(f"ENsubtitlesENsucceeded: {strategy.__name__}")
                    return subtitle_path
            except Exception as e:
                logger.warning(f"ENsubtitlesENfailed {strategy.__name__}: {e}")
                continue
        
        logger.warning("allsubtitlesfetchENfailedEN")
        return None
    
    async def _try_download_with_different_langs(self, url: str, safe_title: str) -> Optional[Path]:
        """ENdownloadENsubtitles"""
        logger.info("ENdownloadENsubtitles...")
        
        # ENsubtitlesEN
        lang_combinations = [
            ['zh-Hans', 'zh'],  # EN
            ['en', 'en-US'],    # EN
            ['ai-zh'],          # AIENsubtitles
            ['auto']            # EN
        ]
        
        for langs in lang_combinations:
            try:
                ydl_opts = {
                    'skip_download': True,  # ENdownloadsubtitles，ENdownloadvideo
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
                
                # ENsubtitlesfile
                subtitle_path = self._find_downloaded_subtitle(safe_title + "_sub")
                if subtitle_path:
                    return subtitle_path
                    
            except Exception as e:
                logger.debug(f"EN {langs} failed: {e}")
                continue
        
        return None
    
    async def _try_download_without_cookies(self, url: str, safe_title: str) -> Optional[Path]:
        """ENusecookiesdownloadsubtitles（ENsubtitlesmayENneedlogin）"""
        logger.info("ENusecookiesdownloadsubtitles...")
        
        try:
            ydl_opts = {
                'skip_download': True,  # ENdownloadsubtitles，ENdownloadvideo
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
            logger.debug(f"ENusecookiesdownloadfailed: {e}")
            return None
    
    async def _try_extract_from_video_metadata(self, url: str, safe_title: str) -> Optional[Path]:
        """ENvideoENsubtitlesEN"""
        logger.info("ENvideoENsubtitlesEN...")
        
        try:
            # fetchvideoEN
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            if self.browser:
                ydl_opts['cookiesfrombrowser'] = (self.browser.lower(),)
            
            loop = asyncio.get_event_loop()
            info_dict = await loop.run_in_executor(None, self._extract_info_sync, url, ydl_opts)
            
            # checkENsubtitlesEN
            subtitles = info_dict.get('subtitles', {})
            auto_subtitles = info_dict.get('automatic_captions', {})
            
            if subtitles or auto_subtitles:
                logger.info(f"ENsubtitlesEN: {list(subtitles.keys()) + list(auto_subtitles.keys())}")
                # ENcanENprocessingsubtitlesEN
                return None  # ENreturnNone，ENcanEN
            
            return None
            
        except Exception as e:
            logger.debug(f"ENvideoENfailed: {e}")
            return None
    
    def _download_sync(self, url: str, ydl_opts: Dict[str, Any]):
        """ENdownload"""
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
    def _create_progress_hook(self, progress_callback: Callable[[str, float], None]):
        """createprogressEN"""
        def progress_hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d and d['total_bytes']:
                    progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                elif '_percent_str' in d:
                    # EN
                    percent_str = d['_percent_str'].strip().rstrip('%')
                    try:
                        progress = float(percent_str)
                    except ValueError:
                        progress = 0
                else:
                    progress = 0
                
                speed = d.get('_speed_str', '')
                eta = d.get('_eta_str', '')
                status = f"downloadEN... {speed} ETA: {eta}"
                progress_callback(status, progress)
            elif d['status'] == 'finished':
                progress_callback("downloadEN，currentlyprocessing...", 95)
        
        return progress_hook
    
    def _sanitize_filename(self, filename: str) -> str:
        """ENfileEN，EN"""
        # EN
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        
        # ENfileEN
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename.strip()
    
    def _find_downloaded_video(self, title: str) -> Optional[Path]:
        """ENdownloadENvideofile"""
        possible_extensions = ['.mp4', '.mkv', '.webm', '.flv']
        
        for ext in possible_extensions:
            video_path = self.download_dir / f"{title}{ext}"
            if video_path.exists():
                return video_path
        
        # ifENfailed，EN
        for file_path in self.download_dir.glob(f"{title}*"):
            if file_path.suffix.lower() in possible_extensions:
                return file_path
        
        return None
    
    def _find_downloaded_subtitle(self, title: str) -> Optional[Path]:
        """ENdownloadENsubtitlesfile - EN，ENAIsubtitles"""
        logger.info(f"currentlyENsubtitlesfile，title: {title}")
        
        # ENcheckAIsubtitlesfile
        ai_subtitle_path = self.download_dir / f"{title}.ai-zh.srt"
        if ai_subtitle_path.exists():
            # EN
            standard_path = self.download_dir / f"{title}.srt"
            if not standard_path.exists():
                ai_subtitle_path.rename(standard_path)
                logger.info(f"ENAIsubtitlesfile: {title}.ai-zh.srt -> {title}.srt")
                return standard_path
            return ai_subtitle_path
        
        # checkENalreadyEN
        standard_path = self.download_dir / f"{title}.srt"
        if standard_path.exists():
            logger.info(f"ENsubtitlesfile: {title}.srt")
            return standard_path
        
        # ENsubtitlesfile
        for file_path in self.download_dir.glob(f"{title}*.srt"):
            logger.info(f"ENsubtitlesfile: {file_path.name}")
            return file_path
        
        logger.warning(f"not foundsubtitlesfile，title: {title}")
        return None
    
    def _convert_vtt_to_srt(self, vtt_path: Path, srt_path: Path):
        """ENVTTsubtitlesfileENSRTEN"""
        try:
            with open(vtt_path, 'r', encoding='utf-8') as vtt_file:
                vtt_content = vtt_file.read()
            
            # ENVTTENSRTEN
            lines = vtt_content.split('\n')
            srt_lines = []
            subtitle_count = 1
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # ENVTTEN
                if line.startswith('WEBVTT') or line.startswith('NOTE') or not line:
                    i += 1
                    continue
                
                # ENtimeEN
                if '-->' in line:
                    # ENtimeEN (VTTuseEN，SRTuseEN)
                    time_line = line.replace('.', ',')
                    srt_lines.append(str(subtitle_count))
                    srt_lines.append(time_line)
                    
                    # fetchsubtitlesEN
                    i += 1
                    subtitle_text = []
                    while i < len(lines) and lines[i].strip():
                        subtitle_text.append(lines[i].strip())
                        i += 1
                    
                    srt_lines.extend(subtitle_text)
                    srt_lines.append('')  # EN
                    subtitle_count += 1
                
                i += 1
            
            # writeSRTfile
            with open(srt_path, 'w', encoding='utf-8') as srt_file:
                srt_file.write('\n'.join(srt_lines))
                
        except Exception as e:
            logger.error(f"VTTENSRTENfailed: {e}")
            raise
    
    def cleanup_temp_files(self, title: str):
        """ENfile"""
        try:
            # ENmayENfile
            for pattern in [f"{title}*.part", f"{title}*.tmp", f"{title}*.ytdl"]:
                for temp_file in self.download_dir.glob(pattern):
                    temp_file.unlink(missing_ok=True)
        except Exception as e:
            logger.warning(f"ENfilefailed: {e}")

# EN
async def download_bilibili_video(
    url: str, 
    download_dir: Optional[Path] = None,
    browser: Optional[str] = None,
    progress_callback: Optional[Callable[[str, float], None]] = None
) -> Dict[str, str]:
    """
    ENBENvideodownloadEN
    
    Args:
        url: BENvideoEN
        download_dir: downloaddirectory
        browser: EN
        progress_callback: progressEN
        
    Returns:
        ENvideo_pathENsubtitle_pathEN
    """
    downloader = BilibiliDownloader(download_dir, browser)
    return await downloader.download_video_and_subtitle(url, progress_callback)

async def get_bilibili_video_info(url: str, browser: Optional[str] = None) -> BilibiliVideoInfo:
    """
    ENBENvideoENfetchEN
    
    Args:
        url: BENvideoEN
        browser: EN
        
    Returns:
        videoEN
    """
    downloader = BilibiliDownloader(browser=browser)
    return await downloader.get_video_info(url)