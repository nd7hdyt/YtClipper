# 🎬 subtitlesdownloadtroubleshooting

## 📋 overview

solveBYouTubesubtitlesdownloadfailedissue。subtitlesdownloadfailedissue，：

1. **Bsubtitlesneedsign in**
2. **YouTubesubtitlesformat**
3. **speech recognitionconfigissue**
4. **issue**

## 🔍 issue

### usetool

toolissue：

```bash
# checkspeech recognitionsettings
python scripts/debug_subtitle_download.py --check-speech

# Bsubtitlesdownload
python scripts/debug_subtitle_download.py https://www.bilibili.com/video/BV1xx411c7mu chrome

# YouTubesubtitlesdownload
python scripts/debug_subtitle_download.py https://www.youtube.com/watch?v=dQw4w9WgXcQ chrome
```

### error

#### Berror

1. **"Subtitles are only available when logged in"**
   - **reason**: Bsubtitles（AIsubtitles）needsign indownload
   - **solution**: 
     - sign inBsite account
     - select（Chrome、Firefox、Safari）
     - Bsign instatus

2. **"subtitlesfile"**
   - **reason**: subtitlessubtitlesdownloadfailed
   - **solution**: 
     - checksubtitles（Bview）
     - subtitles
     - usespeech recognitiongeneratesubtitles

#### YouTubeerror

1. **"No subtitles available"**
   - **reason**: subtitlesgeneratesubtitles
   - **solution**: 
     - checksubtitles
     - downloadgeneratesubtitles
     - usespeech recognitiongeneratesubtitles

2. **"VTT format not supported"**
   - **reason**: YouTubedownloadVTTformatsubtitles，needSRT
   - **solution**: ，failedcheckfile

#### speech recognitionerror

1. **"whisper: command not found"**
   - **reason**: not installedWhisperspeech recognitiontool
   - **solution**: 
     ```bash
     pip install openai-whisper
     ```

2. **"ffmpeg: command not found"**
   - **reason**: not installedffmpeg
   - **solution**: 
     ```bash
     # macOS
     brew install ffmpeg
     
     # Ubuntu/Debian
     sudo apt update && sudo apt install ffmpeg
     
     # Windows
     # downloadffmpegPATHenv var
     ```

3. **"speech recognition"**
   - **reason**: 
   - **solution**: 
     - useWhispermodel（tiny、base）
     - 
     - checkmemoryCPUuse

## 🛠️ solution

### 1. Bsubtitlesdownload

#### sign inconfig
```python
# sign inB
# select
browser = "chrome"  #  "firefox", "safari"
```

#### subtitles
：
1. **AIsubtitles**: downloadAIgenerateChinesesubtitles
2. ****: Chinese、English
3. **cookies**: usecookiesdownloadsubtitles

#### config
```python
# downloadsubtitles
ydl_opts = {
    'subtitleslangs': ['ai-zh', 'zh-Hans', 'zh', 'en'],
    'writeautomaticsub': True,
    'cookiesfrombrowser': ('chrome',)
}
```

### 2. YouTubesubtitlesdownload

#### subtitlesformatsupport
```python
# supportsubtitlesformat
formats = ['srt', 'vtt', 'json3']
languages = ['en', 'zh-Hans', 'zh', 'ja', 'ko']
```

#### format
VTTformatSRTformat：
```python
# VTTSRT
async def _convert_vtt_to_srt(vtt_path: str, srt_path: str):
    # formatsubtitles
```

### 3. speech recognition

#### installWhisper
```bash
# installWhisper
pip install openai-whisper

# verifyinstall
whisper --help
```

#### model selection
```python
# selectmodel
models = {
    "tiny": "39MB, ，",
    "base": "74MB, ，medium（recommend）",
    "small": "244MB, medium，",
    "medium": "769MB, ，",
    "large": "1550MB, ，"
}
```

#### config
```python
# 
languages = {
    "zh": "Chinese",
    "en": "English",
    "ja": "Japanese",
    "ko": "",
    "auto": "auto-detect"
}
```

## 📊 performance

### 1. 
- use
- download
- useproxyVPN

### 2. 
- 
- 
- useSSDI/O

### 3. config
```python
# downloadconfig
ydl_opts = {
    'format': 'best[ext=mp4]/best',  # select
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['ai-zh', 'zh-Hans', 'en'],
    'subtitlesformat': 'srt',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': False,  # 
}
```

## 🔧 troubleshooting

### 1. checkyt-dlpversion
```bash
# updateversion
pip install --upgrade yt-dlp

# checkversion
yt-dlp --version
```

### 2. checkcookies
```bash
# cookies
# accessB/YouTubesign in
# checkcookies
```

### 3. test
```bash
# test
ping www.bilibili.com
ping www.youtube.com

# testDNS
nslookup www.bilibili.com
nslookup www.youtube.com
```

### 4. checkfile
```bash
# checkdownload
ls -la /path/to/download/directory

# 
chmod 755 /path/to/download/directory
```

## 📞 get help

### 1. view
```bash
# view
tail -f backend.log

# viewerror
grep "ERROR" backend.log
```

### 2. usetool
```bash
# 
python scripts/debug_subtitle_download.py <url> <browser>

# checkspeech recognition
python scripts/debug_subtitle_download.py --check-speech
```

### 3. FAQFAQ

**Q: Bsubtitlesdownloadfailed？**
A: Bsubtitlesneedsign indownload，sign inBsite accountselect。

**Q: YouTubesubtitlesdownloadfailed？**
A: step：
1. checksubtitles
2. subtitles
3. usespeech recognitiongeneratesubtitles

**Q: speech recognition？**
A: can：
1. use a smaller model（tinybase）
2. 
3. check

**Q: subtitlesdownloadsucceeded？**
A: ：
1. 
2. useversionyt-dlp
3. configcookies
4. installWhisper

## 🎯 best practices

### 1. daily use
- preferB/YouTubesubtitles
- configspeech recognition
- updateyt-dlpWhisper
- sign instatus

### 2. 
- 
- monitoruse
- settings
- 

### 3. error handling
- error
- usetoolissue
- solution
- issue

---

，solvesubtitlesdownloadissue。issue，usetoolgenerate，tech support。

