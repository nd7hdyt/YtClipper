# 🎤 EN

## 📋 EN

EN，EN，EN：

1. **EN** - EN，ENmockEN
2. **SupportEN** - SupportChinese、English、EN、ENLanguage
3. **SupportENAPIEN** - SupportENWhisper、OpenAI API、Azure Speech ServicesEN

## 🔧 EN

### 1. EN

**EN：**
- EN，EN
- EN，EN
- EN

**EN：**
- EN
- EN
- EN

```python
# EN：ENNoneEN
result = generate_subtitle_for_video(video_path)
if result is None:
    # EN...

# EN：EN
try:
    result = generate_subtitle_for_video(video_path)
except SpeechRecognitionError as e:
    # EN
    logger.error(f"EN: {e}")
    raise
```

### 2. ENSupport

**SupportENLanguage：**
- Chinese（EN/EN）
- English（EN/EN）
- EN
- EN
- EN
- EN
- EN
- EN
- EN
- EN
- EN
- EN

**EN：**
```python
from shared.utils.speech_recognizer import generate_subtitle_for_video, LanguageCode

# ENLanguage
result = generate_subtitle_for_video(
    video_path, 
    language=LanguageCode.CHINESE_SIMPLIFIED
)

# ENLanguage
result = generate_subtitle_for_video(
    video_path, 
    language=LanguageCode.AUTO
)
```

### 3. EN

**SupportEN：**

| EN | EN | EN |
|------|------|----------|
| ENWhisper | EN、EN、EN | ENwhisperENffmpeg |
| OpenAI API | EN、SupportENLanguage | OpenAI APIEN |
| Azure Speech | EN、EN | AzureENAPIEN |
| Google Speech | EN、SupportEN | Google CloudEN |
| EN | ChineseEN | ENAPIEN |

**EN：**
1. ENWhisper（EN）
2. OpenAI API
3. Azure Speech Services
4. Google Speech-to-Text
5. EN

## 🚀 ENAPIEN

### EN

```bash
GET /api/v1/speech-recognition/status
```

EN：
```json
{
  "available_methods": {
    "whisper_local": true,
    "openai_api": false,
    "azure_speech": false,
    "google_speech": false,
    "aliyun_speech": false
  },
  "supported_languages": ["zh", "en", "ja", "ko", "auto"],
  "whisper_models": ["tiny", "base", "small", "medium", "large"],
  "default_config": {
    "method": "whisper_local",
    "language": "auto",
    "model": "base",
    "timeout": 300
  }
}
```

### EN

```bash
POST /api/v1/speech-recognition/test
```

EN：
```json
{
  "method": "whisper_local",
  "language": "zh",
  "model": "base",
  "timeout": 300
}
```

### EN

```bash
GET /api/v1/speech-recognition/install-guide?method=whisper_local
```

## 📝 EN

### EN

```bash
# EN
export SPEECH_RECOGNITION_METHOD="whisper_local"

# LanguageEN
export SPEECH_RECOGNITION_LANGUAGE="zh"

# WhisperEN
export SPEECH_RECOGNITION_MODEL="base"

# EN
export SPEECH_RECOGNITION_TIMEOUT="300"

# APIEN（EN）
export OPENAI_API_KEY="your-openai-key"
export AZURE_SPEECH_KEY="your-azure-key"
export AZURE_SPEECH_REGION="your-region"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
export ALIYUN_ACCESS_KEY_ID="your-access-key"
export ALIYUN_ACCESS_KEY_SECRET="your-secret-key"
export ALIYUN_SPEECH_APP_KEY="your-app-key"
```

### EN

EN `data/settings.json` EN：

```json
{
  "speech_recognition_method": "whisper_local",
  "speech_recognition_language": "zh",
  "speech_recognition_model": "base",
  "speech_recognition_timeout": 300
}
```

## 🔍 EN

### EN

```python
from shared.utils.speech_recognizer import SpeechRecognitionError

try:
    result = generate_subtitle_for_video(video_path)
except SpeechRecognitionError as e:
    # EN
    logger.error(f"EN: {e}")
    # EN
```

### EN

1. **EN** - EN
2. **EN** - EN
3. **EN** - EN
4. **EN** - EN
5. **EN** - EN

## 📊 Performance

### WhisperEN

| EN | EN | EN | EN | EN |
|------|------|------|--------|----------|
| tiny | 39MB | ⭐⭐⭐⭐⭐ | ⭐⭐ | EN |
| base | 74MB | ⭐⭐⭐⭐ | ⭐⭐⭐ | EN |
| small | 244MB | ⭐⭐⭐ | ⭐⭐⭐⭐ | EN |
| medium | 769MB | ⭐⭐ | ⭐⭐⭐⭐⭐ | EN |
| large | 1550MB | ⭐ | ⭐⭐⭐⭐⭐ | EN |

### EN

- EN（<5EN）：60EN
- EN（5-30EN）：300EN
- EN（>30EN）：600EN

## 🛠️ EN

### ENWhisperEN

```bash
# ENPythonEN
pip install openai-whisper

# EN
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# ENffmpegENPATH

# EN
whisper --help
```

### APIEN

#### OpenAI API
```bash
export OPENAI_API_KEY="your-api-key"
```

#### Azure Speech Services
```bash
export AZURE_SPEECH_KEY="your-api-key"
export AZURE_SPEECH_REGION="your-region"
```

#### Google Speech-to-Text
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

#### EN
```bash
export ALIYUN_ACCESS_KEY_ID="your-access-key"
export ALIYUN_ACCESS_KEY_SECRET="your-secret-key"
export ALIYUN_SPEECH_APP_KEY="your-app-key"
```

## 🔄 EN

### EN

1. **EN**
```python
# EN
from shared.utils.speech_recognizer import generate_subtitle_for_video

# EN
from shared.utils.speech_recognizer import (
    generate_subtitle_for_video, 
    SpeechRecognitionError,
    LanguageCode
)
```

2. **EN**
```python
# EN
result = generate_subtitle_for_video(video_path)
if result is None:
    # EN

# EN
try:
    result = generate_subtitle_for_video(video_path)
except SpeechRecognitionError as e:
    # EN
```

3. **EN**
```python
# EN
if method == "simple":
    return recognizer.generate_subtitle_simple(video_path, output_path)
```

## 📈 EN

### EN

```python
import logging
logger = logging.getLogger(__name__)

# EN
logger.info(f"EN: {video_path}")

# EN
logger.info(f"EN: {output_path}")

# EN
logger.error(f"EN: {error}")
```

### EN

EN：
- EN
- EN
- EN
- EN

## 🎯 EN

1. **EN**
   - EN `small` EN `medium` EN
   - EN
   - EN

2. **ENLanguageEN**
   - ENLanguageEN
   - ENLanguageEN，ENLanguageEN
   - EN

3. **EN**
   - EN
   - ProvidesEN
   - EN

4. **Performance**
   - EN
   - ENGPUEN（EN）
   - EN

## 🔮 EN

1. **ENAPIEN**
   - EN
   - EN
   - EN

2. **EN**
   - EN
   - EN
   - EN

3. **Performance**
   - EN
   - EN
   - EN

## 📞 ENSupport

EN，EN：

1. EN
2. EN
3. EN
4. ENAPIEN

ENReference：
- [WhisperEN](https://github.com/openai/whisper)
- [OpenAI APIEN](https://platform.openai.com/docs/api-reference)
- [Azure Speech ServicesEN](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [Google Speech-to-TextEN](https://cloud.google.com/speech-to-text/docs)
- [EN](https://help.aliyun.com/product/30413.html)

