# 🎤 speech recognition

## 📋 overview

，speech recognition，improve：

1. **testsubtitles** - failedfailed，usemock
2. **support** - supportChinese、English、Japanese、
3. **supportAPIintegrate** - supportlocalWhisper、OpenAI API、Azure Speech Services

## 🔧 improve

### 1. testsubtitles

**issue：**
- speech recognition failed，generatetestsubtitlesfile
- testsubtitles，impact
- succeeded

**nowimprove：**
- testsubtitlesgenerate
- speech recognition failed
- production

```python
# ：returnNonetestsubtitles
result = generate_subtitle_for_video(video_path)
if result is None:
    # generatetestsubtitles...

# now：failed
try:
    result = generate_subtitle_for_video(video_path)
except SpeechRecognitionError as e:
    # speech recognition failed
    logger.error(f"speech recognition failed: {e}")
    raise
```

### 2. support

**support：**
- Chinese（/）
- English（/）
- Japanese
- 
- 
- 
- 
- 
- 
- 
- 
- auto-detect

**use：**
```python
from shared.utils.speech_recognizer import generate_subtitle_for_video, LanguageCode

# 
result = generate_subtitle_for_video(
    video_path, 
    language=LanguageCode.CHINESE_SIMPLIFIED
)

# auto-detect
result = generate_subtitle_for_video(
    video_path, 
    language=LanguageCode.AUTO
)
```

### 3. speech recognitionservice

**supportservice：**

| service | features | config |
|------|------|----------|
| localWhisper | free、、 | installwhisperffmpeg |
| OpenAI API | 、support | OpenAI APIkey |
| Azure Speech | 、 | AzureAPIkey |
| Google Speech | 、support | Google Cloud |
|  | Chinese | APIkey |

**select：**
1. localWhisper（recommend）
2. OpenAI API
3. Azure Speech Services
4. Google Speech-to-Text
5. Alibaba speech recognition

## 🚀 APIAPI

### speech recognitionstatus

```bash
GET /api/v1/speech-recognition/status
```

return：
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

### configtest

```bash
POST /api/v1/speech-recognition/test
```

：
```json
{
  "method": "whisper_local",
  "language": "zh",
  "model": "base",
  "timeout": 300
}
```

### install

```bash
GET /api/v1/speech-recognition/install-guide?method=whisper_local
```

## 📝 config

### env varconfig

```bash
# speech recognitionmethod
export SPEECH_RECOGNITION_METHOD="whisper_local"

# settings
export SPEECH_RECOGNITION_LANGUAGE="zh"

# Whispermodel
export SPEECH_RECOGNITION_MODEL="base"

# 
export SPEECH_RECOGNITION_TIMEOUT="300"

# APIkey（selectservice）
export OPENAI_API_KEY="your-openai-key"
export AZURE_SPEECH_KEY="your-azure-key"
export AZURE_SPEECH_REGION="your-region"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
export ALIYUN_ACCESS_KEY_ID="your-access-key"
export ALIYUN_ACCESS_KEY_SECRET="your-secret-key"
export ALIYUN_SPEECH_APP_KEY="your-app-key"
```

### configfile

 `data/settings.json` canconfig：

```json
{
  "speech_recognition_method": "whisper_local",
  "speech_recognition_language": "zh",
  "speech_recognition_model": "base",
  "speech_recognition_timeout": 300
}
```

## 🔍 error handling

### 

```python
from shared.utils.speech_recognizer import SpeechRecognitionError

try:
    result = generate_subtitle_for_video(video_path)
except SpeechRecognitionError as e:
    # speech recognitionerror
    logger.error(f"speech recognition failed: {e}")
    # canselectusemethod
```

### error

1. **serviceavailable** - speech recognitionservicenot installedconfig
2. **file** - fileaccess
3. **** - speech recognition
4. **failed** - speech recognitionservicefailed
5. **configerror** - config

## 📊 performance

### Whispermodel selection

| model |  |  |  | use cases |
|------|------|------|--------|----------|
| tiny | 39MB | ⭐⭐⭐⭐⭐ | ⭐⭐ | test |
| base | 74MB | ⭐⭐⭐⭐ | ⭐⭐⭐ | daily use |
| small | 244MB | ⭐⭐⭐ | ⭐⭐⭐⭐ |  |
| medium | 769MB | ⭐⭐ | ⭐⭐⭐⭐⭐ |  |
| large | 1550MB | ⭐ | ⭐⭐⭐⭐⭐ |  |

### settings

- （<5minutes）：60
- medium（5-30minutes）：300
- （>30minutes）：600

## 🛠️ install

### localWhisperinstall

```bash
# installPythondependencies
pip install openai-whisper

# installdependencies
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# downloadffmpegPATH

# verifyinstall
whisper --help
```

### APIserviceconfig

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

#### Alibaba speech recognition
```bash
export ALIYUN_ACCESS_KEY_ID="your-access-key"
export ALIYUN_ACCESS_KEY_SECRET="your-secret-key"
export ALIYUN_SPEECH_APP_KEY="your-app-key"
```

## 🔄 

### version

1. **updateimport**
```python
# version
from shared.utils.speech_recognizer import generate_subtitle_for_video

# version
from shared.utils.speech_recognizer import (
    generate_subtitle_for_video, 
    SpeechRecognitionError,
    LanguageCode
)
```

2. **updateerror handling**
```python
# version
result = generate_subtitle_for_video(video_path)
if result is None:
    # failed

# version
try:
    result = generate_subtitle_for_video(video_path)
except SpeechRecognitionError as e:
    # failed
```

3. **testsubtitles**
```python
# 
if method == "simple":
    return recognizer.generate_subtitle_simple(video_path, output_path)
```

## 📈 monitor

### 

```python
import logging
logger = logging.getLogger(__name__)

# speech recognition
logger.info(f"speech recognition: {video_path}")

# speech recognitionsucceeded
logger.info(f"speech recognitionsucceeded: {output_path}")

# speech recognition failed
logger.error(f"speech recognition failed: {error}")
```

### perf monitor

monitor：
- speech recognitionsucceeded
- 
- error
- serviceuse

## 🎯 best practices

1. **production**
   - use `small`  `medium` model
   - settings
   - configerror

2. ****
   - prefer
   - ，
   - usespeech recognitionservice

3. **error handling**
   - error handling
   - error
   - 

4. **performance**
   - selectmodel
   - useGPU（available）
   - 

## 🔮 

1. **APIservice**
   - speech recognition
   - speech recognition
   - speech recognition

2. ****
   - 
   - 
   - 

3. **performance**
   - 
   - cache
   - 

## 📞 tech support

if you encounter issues，：

1. checkfileerror
2. verifyspeech recognitionserviceinstall
3. confirmconfigfile
4. viewAPIdocsinstall

：
- [Whisperdocs](https://github.com/openai/whisper)
- [OpenAI APIdocs](https://platform.openai.com/docs/api-reference)
- [Azure Speech Servicesdocs](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [Google Speech-to-Textdocs](https://cloud.google.com/speech-to-text/docs)
- [Alibaba speech recognitiondocs](https://help.aliyun.com/product/30413.html)

