#!/usr/bin/env python3
"""
ENprojectEN
"""

import sys
import asyncio
from pathlib import Path

# ENprojectENdirectoryENPythonpath
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.utils.bilibili_downloader import BilibiliDownloader
import requests
import base64

async def test_bilibili_thumbnail_extraction():
    """ENBEN"""
    print("🧪 ENBEN...")
    
    # useENBENvideoEN
    test_url = "https://www.bilibili.com/video/BV1LSegzbEp9/"
    
    try:
        # createdownloadEN
        downloader = BilibiliDownloader()
        
        # fetchvideoEN
        video_info = await downloader.get_video_info(test_url)
        
        print(f"✅ videoENfetchsucceeded:")
        print(f"   title: {video_info.title}")
        print(f"   uploadEN: {video_info.uploader}")
        print(f"   ENURL: {video_info.thumbnail_url}")
        
        # ENdownload
        if video_info.thumbnail_url:
            print("🖼️  ENdownload...")
            response = requests.get(video_info.thumbnail_url, timeout=10)
            if response.status_code == 200:
                # ENbase64
                thumbnail_base64 = base64.b64encode(response.content).decode('utf-8')
                thumbnail_data = f"data:image/jpeg;base64,{thumbnail_base64}"
                
                print(f"✅ ENdownloadsucceeded，EN: {len(response.content)} bytes")
                print(f"   Base64EN: {len(thumbnail_base64)} EN")
                print(f"   ENURIEN: {thumbnail_data[:50]}...")
                
                return True
            else:
                print(f"❌ ENdownloadfailed: HTTP {response.status_code}")
                return False
        else:
            print("⚠️  ENURL")
            return False
            
    except Exception as e:
        print(f"❌ ENfailed: {e}")
        return False

async def test_youtube_thumbnail_extraction():
    """ENYouTubeEN"""
    print("\n🧪 ENYouTubeEN...")
    
    # useENYouTubevideoEN
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        import yt_dlp
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        def extract_info_sync(url, ydl_opts):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)
        
        loop = asyncio.get_event_loop()
        video_info = await loop.run_in_executor(None, extract_info_sync, test_url, ydl_opts)
        
        print(f"✅ videoENfetchsucceeded:")
        print(f"   title: {video_info.get('title', 'Unknown')}")
        print(f"   uploadEN: {video_info.get('uploader', 'Unknown')}")
        print(f"   ENURL: {video_info.get('thumbnail', '')}")
        
        # ENdownload
        thumbnail_url = video_info.get('thumbnail', '')
        if thumbnail_url:
            print("🖼️  ENdownload...")
            response = requests.get(thumbnail_url, timeout=10)
            if response.status_code == 200:
                # ENbase64
                thumbnail_base64 = base64.b64encode(response.content).decode('utf-8')
                thumbnail_data = f"data:image/jpeg;base64,{thumbnail_base64}"
                
                print(f"✅ ENdownloadsucceeded，EN: {len(response.content)} bytes")
                print(f"   Base64EN: {len(thumbnail_base64)} EN")
                print(f"   ENURIEN: {thumbnail_data[:50]}...")
                
                return True
            else:
                print(f"❌ ENdownloadfailed: HTTP {response.status_code}")
                return False
        else:
            print("⚠️  ENURL")
            return False
            
    except Exception as e:
        print(f"❌ ENfailed: {e}")
        return False

async def main():
    """EN"""
    print("🚀 startENprojectEN...\n")
    
    # ENBEN
    bilibili_success = await test_bilibili_thumbnail_extraction()
    
    # ENYouTubeEN
    youtube_success = await test_youtube_thumbnail_extraction()
    
    print(f"\n📊 ENresult:")
    print(f"   BEN: {'✅ succeeded' if bilibili_success else '❌ failed'}")
    print(f"   YouTubeEN: {'✅ succeeded' if youtube_success else '❌ failed'}")
    
    if bilibili_success and youtube_success:
        print("\n🎉 allENthrough！ENprojectEN")
        return True
    else:
        print("\n⚠️  ENfailed，pleasecheckEN")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
