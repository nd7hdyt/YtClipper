# 🎬 ENTroubleshootingEN

## 📋 EN

ENBENYouTubeEN。EN，EN：

1. **BEN**
2. **YouTubeEN**
3. **EN**
4. **EN**

## 🔍 EN

### EN

ENProvidesEN：

```bash
# EN
python scripts/debug_subtitle_download.py --check-speech

# ENBEN
python scripts/debug_subtitle_download.py https://www.bilibili.com/video/BV1xx411c7mu chrome

# ENYouTubeEN
python scripts/debug_subtitle_download.py https://www.youtube.com/watch?v=dQw4w9WgXcQ chrome
```

### EN

#### BEN

1. **"Subtitles are only available when logged in"**
   - **EN**: BEN（ENAIEN）EN
   - **EN**: 
     - ENBENAccount
     - EN（Chrome、Firefox、SafariEN）
     - ENBEN

2. **"EN"**
   - **EN**: EN
   - **EN**: 
     - EN（ENBEN）
     - ENLanguage
     - EN

#### YouTubeEN

1. **"No subtitles available"**
   - **EN**: EN
   - **EN**: 
     - EN
     - EN
     - EN

2. **"VTT format not supported"**
   - **EN**: YouTubeENVTTEN，ENSRT
   - **EN**: EN，EN

#### EN

1. **"whisper: command not found"**
   - **EN**: ENWhisperEN
   - **EN**: 
     ```bash
     pip install openai-whisper
     ```

2. **"ffmpeg: command not found"**
   - **EN**: ENffmpeg
   - **EN**: 
     ```bash
     # macOS
     brew install ffmpeg
     
     # Ubuntu/Debian
     sudo apt update && sudo apt install ffmpeg
     
     # Windows
     # ENffmpegENPATHEN
     ```

3. **"EN"**
   - **EN**: EN
   - **EN**: 
     - ENWhisperEN（tiny、base）
     - EN
     - ENCPUEN

## 🛠️ EN

### 1. BEN

#### EN
```python
# ENBEN
# EN
browser = "chrome"  # EN "firefox", "safari"
```

#### EN
EN：
1. **AIEN**: ENAIENChineseEN
2. **ENLanguageEN**: ENChinese、EnglishENLanguage
3. **ENcookiesEN**: ENcookiesEN

#### EN
```python
# ENLanguage
ydl_opts = {
    'subtitleslangs': ['ai-zh', 'zh-Hans', 'zh', 'en'],
    'writeautomaticsub': True,
    'cookiesfrombrowser': ('chrome',)
}
```

### 2. YouTubeEN

#### ENSupport
```python
# SupportEN
formats = ['srt', 'vtt', 'json3']
languages = ['en', 'zh-Hans', 'zh', 'ja', 'ko']
```

#### EN
ENVTTENSRTEN：
```python
# VTTENSRTEN
async def _convert_vtt_to_srt(vtt_path: str, srt_path: str):
    # EN
```

### 3. EN

#### ENWhisper
```bash
# ENWhisper
pip install openai-whisper

# EN
whisper --help
```

#### EN
```python
# EN
models = {
    "tiny": "39MB, EN，EN",
    "base": "74MB, EN，EN（EN）",
    "small": "244MB, EN，EN",
    "medium": "769MB, EN，EN",
    "large": "1550MB, EN，EN"
}
```

#### LanguageEN
```python
# ENLanguageEN
languages = {
    "zh": "Chinese",
    "en": "English",
    "ja": "EN",
    "ko": "EN",
    "auto": "EN"
}
```

## 📊 PerformanceEN

### 1. EN
- EN
- EN
- ENVPN

### 2. EN
- EN
- EN
- ENSSDENI/OEN

### 3. EN
```python
# EN
ydl_opts = {
    'format': 'best[ext=mp4]/best',  # EN
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['ai-zh', 'zh-Hans', 'en'],
    'subtitlesformat': 'srt',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': False,  # EN
}
```

## 🔧 ENTroubleshooting

### 1. ENyt-dlpEN
```bash
# EN
pip install --upgrade yt-dlp

# EN
yt-dlp --version
```

### 2. ENcookies
```bash
# ENcookies
# ENBEN/YouTubeEN
# ENcookiesEN
```

### 3. EN
```bash
# EN
ping www.bilibili.com
ping www.youtube.com

# ENDNSEN
nslookup www.bilibili.com
nslookup www.youtube.com
```

### 4. EN
```bash
# EN
ls -la /path/to/download/directory

# EN
chmod 755 /path/to/download/directory
```

## 📞 EN

### 1. EN
```bash
# EN
tail -f backend.log

# EN
grep "ERROR" backend.log
```

### 2. EN
```bash
# EN
python scripts/debug_subtitle_download.py <url> <browser>

# EN
python scripts/debug_subtitle_download.py --check-speech
```

### 3. FAQFAQ

**Q: ENBEN？**
A: BEN，ENBENAccountEN。

**Q: YouTubeEN？**
A: EN：
1. EN
2. ENLanguage
3. EN

**Q: EN？**
A: EN：
1. EN（tinyENbase）
2. EN
3. EN

**Q: EN？**
A: EN：
1. EN
2. ENyt-dlp
3. ENcookies
4. ENWhisperEN

## 🎯 EN

### 1. EN
- ENBEN/YouTubeEN
- EN
- ENyt-dlpENWhisper
- EN

### 2. EN
- EN
- EN
- EN
- EN

### 3. EN
- EN
- EN
- EN
- EN

---

EN，EN。EN，EN，ENContactENSupportEN。

