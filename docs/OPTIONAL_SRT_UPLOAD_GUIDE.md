# ENSRTENUploadEN

## EN

AutoClipENSupportENUploadEN：
1. **EN + EN**：ENUploadENSRTEN
2. **EN**：ENUploadEN，EN

## EN

### ✅ ENUploadEN
- **EN**：ENProvidesEN，EN
- **AIEN**：ENUploadEN，EN
- **EN**：EN，EN

### ✅ ENLanguageSupport
- Support15ENLanguageEN
- ENLanguage：
  - EN/EN：ENChineseEN
  - EN：ENLanguage
  - EN：ENLanguage

### ✅ EN
- ENWhisper（EN）
- OpenAI API
- Azure Speech Services
- Google Speech-to-Text
- EN

## EN

### ENInterfaceEN

1. **UploadEN**
   - EN：EN(.srt)
   - EN：EN(.srt)ENAIEN

2. **EN**
   - UploadEN+EN：EN
   - ENUploadEN：EN"ENAIEN"

3. **UploadEN**
   - EN：EN+EN+EN
   - EN：EN+EN

### APIEN

#### UploadEN `POST /api/v1/projects/upload`

**EN：**
```python
# EN：srt_fileEN
srt_file: UploadFile = File(...)

# EN：srt_fileEN
srt_file: Optional[UploadFile] = File(None)
```

**EN：**

1. **ENUploadEN**
```python
files = {
    'video_file': ('video.mp4', video_content, 'video/mp4'),
    'srt_file': ('subtitle.srt', srt_content, 'application/x-subrip')
}
data = {
    'project_name': 'EN',
    'video_category': 'knowledge'
}
```

2. **ENUploadEN**
```python
files = {
    'video_file': ('video.mp4', video_content, 'video/mp4')
}
data = {
    'project_name': 'EN',
    'video_category': 'knowledge'
}
```

**EN：**

EN，EN：
```json
{
    "id": "project-id",
    "name": "EN",
    "description": "Video: video.mp4 (Will generate subtitle using speech recognition)",
    "settings": {
        "auto_generate_subtitle": true,
        "video_category": "knowledge"
    }
}
```

**EN：**

EN400EN：
```json
{
    "detail": "EN: EN，ENwhisperENAPIEN。ENUploadEN。"
}
```

## EN

### EN

1. **EN**
   ```python
   # EN（EN）
   if not video_file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
       raise HTTPException(status_code=400, detail="Invalid video file format")
   
   # EN（EN）
   if srt_file and not srt_file.filename.lower().endswith('.srt'):
       raise HTTPException(status_code=400, detail="Invalid subtitle file format")
   ```

2. **EN**
   ```python
   if srt_file:
       # ENProvidesEN
       srt_path = save_user_subtitle(srt_file)
   else:
       # EN
       srt_path = generate_subtitle_with_speech_recognition(video_path, language, model)
   ```

3. **LanguageEN**
   ```python
   # ENLanguage
   language = "auto"  # EN
   if video_category in ["business", "knowledge"]:
       language = "zh"  # ChineseEN
   elif video_category == "entertainment":
       language = "auto"  # ENLanguage
   ```

### EN

1. **UploadEN**
   ```typescript
   // EN
   if (!files.video) {
       message.error('EN')
       return
   }
   // if (!files.srt) {  // EN
   //     message.error('EN(.srt)')
   //     return
   // }
   ```

2. **UIEN**
   ```typescript
   // EN
   {files.video && !files.srt && (
       <div>ENAIEN</div>
   )}
   ```

3. **APIEN**
   ```typescript
   const formData = new FormData()
   formData.append('video_file', data.video_file)
   if (data.srt_file) {  // EN
       formData.append('srt_file', data.srt_file)
   }
   ```

## EN

### EN

EN，EN：

#### 1. ENWhisper（EN）
```bash
# ENWhisper
pip install openai-whisper

# ENFFmpeg
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

#### 5. EN
```bash
export ALIYUN_ACCESS_KEY_ID="your-access-key"
export ALIYUN_ACCESS_KEY_SECRET="your-secret-key"
export ALIYUN_SPEECH_APP_KEY="your-app-key"
```

### EN

ENAPIEN：

```bash
# EN
GET /api/v1/speech-recognition/status

# EN
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

## EN

### 1. EN
- **EN**：EN
- **EN**：EN
- **EN**：ProvidesENUploadEN

### 2. EN
- **EN**：EN`base`EN
- **LanguageEN**：ENLanguage
- **EN**：EN（EN5EN）

### 3. EN
- **EN**：EN
- **EN**：EN
- **EN**：ProvidesEN

## Troubleshooting

### FAQ

1. **"EN"**
   - ENWhisper：`which whisper`
   - ENAPIEN
   - EN：`GET /api/v1/speech-recognition/status`

2. **"EN"**
   - EN（EN<100MB）
   - EN
   - EN（tiny/base）

3. **"EN"**
   - ENWhisperEN
   - EN
   - ENWhisperEN

### EN

1. **EN**
   ```bash
   curl http://localhost:8000/api/v1/speech-recognition/status
   ```

2. **EN**
   ```bash
   tail -f backend/backend.log
   ```

3. **ENWhisperEN**
   ```bash
   whisper --help
   ffmpeg -version
   ```

## EN

### v1.0.0
- ✅ SupportENSRTENUpload
- ✅ EN
- ✅ ENLanguageEN
- ✅ EN
- ✅ ENInterfaceEN

---

## EN

- [EN](./SPEECH_RECOGNITION_REDESIGN.md)
- [EN](./SPEECH_RECOGNITION_SETUP.md)
- [EN](./BACKEND_ARCHITECTURE.md)

