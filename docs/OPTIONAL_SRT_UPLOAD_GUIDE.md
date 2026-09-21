# optionalSRTfile upload

## overview

AutoClipnowsupport：
1. ** + subtitlesfile**：SRTsubtitlesfile
2. **file**：file，usespeech recognitiongeneratesubtitles

## features

### ✅ 
- ****：subtitlesfile，prefersubtitles
- **AI**：，callspeech recognitiongeneratesubtitles
- **error handling**：speech recognition failed，error

### ✅ multi-language support
- support15speech recognition
- select：
  - business/：preferChinese
  - ：auto-detect
  - ：auto-detect

### ✅ speech recognition
- localWhisper（recommend）
- OpenAI API
- Azure Speech Services
- Google Speech-to-Text
- Alibaba speech recognition

## usage

### frontend

1. **update**
   - ：importsubtitlesfile(.srt)
   - ：optionalimportsubtitlesfile(.srt)useAIgenerate

2. ****
   - +subtitles：file
   - ："useAIspeech recognitiongeneratesubtitlesfile"

3. **button**
   - ：need+subtitles+project
   - now：need+project

### APIAPI

#### API `POST /api/v1/projects/upload`

**：**
```python
# ：srt_file
srt_file: UploadFile = File(...)

# now：srt_fileoptional
srt_file: Optional[UploadFile] = File(None)
```

**：**

1. **subtitles**
```python
files = {
    'video_file': ('video.mp4', video_content, 'video/mp4'),
    'srt_file': ('subtitle.srt', srt_content, 'application/x-subrip')
}
data = {
    'project_name': 'project',
    'video_category': 'knowledge'
}
```

2. ****
```python
files = {
    'video_file': ('video.mp4', video_content, 'video/mp4')
}
data = {
    'project_name': 'project',
    'video_category': 'knowledge'
}
```

**：**

succeeded，project：
```json
{
    "id": "project-id",
    "name": "project",
    "description": "Video: video.mp4 (Will generate subtitle using speech recognition)",
    "settings": {
        "auto_generate_subtitle": true,
        "video_category": "knowledge"
    }
}
```

**error handling：**

speech recognition failedreturn400error：
```json
{
    "detail": "speech recognition failed: availablespeech recognitionservice，installwhisperconfigAPIkey。subtitlesfilecheckspeech recognitionserviceconfig。"
}
```

## technical details

### backend

1. **verify**
   ```python
   # fileverify（）
   if not video_file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
       raise HTTPException(status_code=400, detail="Invalid video file format")
   
   # subtitlesfileverify（optional）
   if srt_file and not srt_file.filename.lower().endswith('.srt'):
       raise HTTPException(status_code=400, detail="Invalid subtitle file format")
   ```

2. **subtitles**
   ```python
   if srt_file:
       # subtitlesfile
       srt_path = save_user_subtitle(srt_file)
   else:
       # usespeech recognitiongeneratesubtitles
       srt_path = generate_subtitle_with_speech_recognition(video_path, language, model)
   ```

3. **select**
   ```python
   # 
   language = "auto"  # defaultauto-detect
   if video_category in ["business", "knowledge"]:
       language = "zh"  # Chinese
   elif video_category == "entertainment":
       language = "auto"  # 
   ```

### frontend

1. ****
   ```typescript
   // subtitlesfileverify
   if (!files.video) {
       message.error('selectfile')
       return
   }
   // if (!files.srt) {  // check
   //     message.error('importsubtitlesfile(.srt)')
   //     return
   // }
   ```

2. **UIupdate**
   ```typescript
   // 
   {files.video && !files.srt && (
       <div>useAIspeech recognitiongeneratesubtitlesfile</div>
   )}
   ```

3. **APIcall**
   ```typescript
   const formData = new FormData()
   formData.append('video_file', data.video_file)
   if (data.srt_file) {  // subtitlesfile
       formData.append('srt_file', data.srt_file)
   }
   ```

## config

### speech recognitionserviceconfig

usespeech recognition，needconfigspeech recognitionservice：

#### 1. localWhisper（recommend）
```bash
# installWhisper
pip install openai-whisper

# installFFmpeg
# macOS
brew install ffmpeg
# Ubuntu/Debian
sudo apt install ffmpeg
```

#### 2. OpenAI API
```bash
export OPENAI_API_KEY="your-api-key"
```

#### 3. Azure Speech Services
```bash
export AZURE_SPEECH_KEY="your-api-key"
export AZURE_SPEECH_REGION="your-region"
```

#### 4. Google Speech-to-Text
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

#### 5. Alibaba speech recognition
```bash
export ALIYUN_ACCESS_KEY_ID="your-access-key"
export ALIYUN_ACCESS_KEY_SECRET="your-secret-key"
export ALIYUN_SPEECH_APP_KEY="your-app-key"
```

### checkconfigstatus

canAPIcheckspeech recognitionservicestatus：

```bash
# checkavailablespeech recognitionmethod
GET /api/v1/speech-recognition/status

# 
{
    "available_methods": {
        "whisper_local": true,
        "openai_api": false,
        "azure_speech": false,
        "google_speech": false,
        "aliyun_speech": false
    },
    "supported_languages": ["zh", "en", "ja", "ko", "fr", "de", ...],
    "whisper_models": ["tiny", "base", "small", "medium", "large"],
    "default_config": {
        "method": "whisper_local",
        "language": "auto",
        "model": "base",
        "timeout": 300
    }
}
```

## best practices

### 1. 
- ****：subtitlesfileoptional
- ****：speech recognitionneed
- **error**：subtitles

### 2. 
- **model selection**：defaultuse`base`model
- ****：select
- **settings**：settingsspeech recognition（default5minutes）

### 3. error handling
- **servicecheck**：startcheckspeech recognitionserviceavailable
- ****：speech recognitionservice
- ****：errorsolve

## troubleshooting

### FAQ

1. **"availablespeech recognitionservice"**
   - checkinstallWhisper：`which whisper`
   - checkconfigAPIkey
   - viewservicestatus：`GET /api/v1/speech-recognition/status`

2. **"speech recognition"**
   - checkfile（<100MB）
   - settings
   - usemodel（tiny/base）

3. **"subtitlesfile"**
   - checkWhisperinstall
   - viewbackenderror
   - Whispertest

### step

1. **checkservicestatus**
   ```bash
   curl http://localhost:8000/api/v1/speech-recognition/status
   ```

2. **viewbackend**
   ```bash
   tail -f backend/backend.log
   ```

3. **testWhisperinstall**
   ```bash
   whisper --help
   ffmpeg -version
   ```

## changelog

### v1.0.0
- ✅ supportoptionalSRTfile upload
- ✅ integrationspeech recognitionservice
- ✅ select
- ✅ error handling
- ✅ 

---

## related docs

- [speech recognitiondocs](./SPEECH_RECOGNITION_REDESIGN.md)
- [speech recognitionsettings](./SPEECH_RECOGNITION_SETUP.md)
- [backenddocs](./BACKEND_ARCHITECTURE.md)

