#!/usr/bin/env python3
"""
testtranslatedimportprojecttranslatedfeature
"""

import sys
import asyncio
from pathlib import Path

# addprojecttranslateddirectorytranslatedPythonpath
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.utils.bilibili_downloader import BilibiliDownloader
import requests
import base64

async def test_bilibili_thumbnail_extraction():
    """testBsitetranslatedfeature"""
    print("🧪 testBsitetranslatedfeature...")
    
    # useone translated'sBsitevideotranslatedtest
    test_url = "https://www.bilibili.com/video/BV1LSegzbEp9/"
    
    try:
        # createdownloadtranslated
        downloader = BilibiliDownloader()
        
        # fetchvideoinfo
        video_info = await downloader.get_video_info(test_url)
        
        print(f"✅ videoinfofetchsucceeded:")
        print(f"   translated: {video_info.title}")
        print(f"   Uploadtranslated: {video_info.uploader}")
        print(f"   translatedURL: {video_info.thumbnail_url}")
        
        # testtranslateddownload
        if video_info.thumbnail_url:
            print("🖼️  testtranslateddownload...")
            response = requests.get(video_info.thumbnail_url, timeout=10)
            if response.status_code == 200:
                # translatedbase64
                thumbnail_base64 = base64.b64encode(response.content).decode('utf-8')
                thumbnail_data = f"data:image/jpeg;base64,{thumbnail_base64}"
                
                print(f"✅ translateddownloadsucceeded，translated: {len(response.content)} bytes")
                print(f"   Base64translated: {len(thumbnail_base64)} translated")
                print(f"   translatedURItranslated: {thumbnail_data[:50]}...")
                
                return True
            else:
                print(f"❌ translateddownloadfailed: HTTP {response.status_code}")
                return False
        else:
            print("⚠️  translatedURL")
            return False
            
    except Exception as e:
        print(f"❌ testfailed: {e}")
        return False

async def test_youtube_thumbnail_extraction():
    """testYouTubetranslatedfeature"""
    print("\n🧪 testYouTubetranslatedfeature...")
    
    # useone translated'sYouTubevideotranslatedtest
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
        
        print(f"✅ videoinfofetchsucceeded:")
        print(f"   translated: {video_info.get('title', 'Unknown')}")
        print(f"   Uploadtranslated: {video_info.get('uploader', 'Unknown')}")
        print(f"   translatedURL: {video_info.get('thumbnail', '')}")
        
        # testtranslateddownload
        thumbnail_url = video_info.get('thumbnail', '')
        if thumbnail_url:
            print("🖼️  testtranslateddownload...")
            response = requests.get(thumbnail_url, timeout=10)
            if response.status_code == 200:
                # translatedbase64
                thumbnail_base64 = base64.b64encode(response.content).decode('utf-8')
                thumbnail_data = f"data:image/jpeg;base64,{thumbnail_base64}"
                
                print(f"✅ translateddownloadsucceeded，translated: {len(response.content)} bytes")
                print(f"   Base64translated: {len(thumbnail_base64)} translated")
                print(f"   translatedURItranslated: {thumbnail_data[:50]}...")
                
                return True
            else:
                print(f"❌ translateddownloadfailed: HTTP {response.status_code}")
                return False
        else:
            print("⚠️  translatedURL")
            return False
            
    except Exception as e:
        print(f"❌ testfailed: {e}")
        return False

async def main():
    """translated"""
    print("🚀 translatedtesttranslatedimportprojecttranslatedfeature...\n")
    
    # testBsitetranslated
    bilibili_success = await test_bilibili_thumbnail_extraction()
    
    # testYouTubetranslated
    youtube_success = await test_youtube_thumbnail_extraction()
    
    print(f"\n📊 testtranslated:")
    print(f"   Bsitetranslated: {'✅ succeeded' if bilibili_success else '❌ failed'}")
    print(f"   YouTubetranslated: {'✅ succeeded' if youtube_success else '❌ failed'}")
    
    if bilibili_success and youtube_success:
        print("\n🎉 translatedtesttranslated！translatedimportprojecttranslatedfeaturetranslated")
        return True
    else:
        print("\n⚠️  translatedtestfailed，translatedchecktranslatedfeature")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
