# 🎤 EN

## 📋 EN

AutoClipSupportEN，EN，EN。

## 🔧 SupportEN

### 1. ENWhisper（EN）

**EN：**
- ✅ EN，EN
- ✅ ENAPIEN
- ✅ EN
- ✅ SupportENLanguage
- ✅ EN

**EN：**

```bash
# EN1：ENpipEN
pip install openai-whisper

# EN2：ENcondaEN
conda install -c conda-forge openai-whisper

# EN3：EN
git clone https://github.com/openai/whisper.git
cd whisper
pip install -e .
```

**EN：**
```bash
whisper --help
```

**EN：**
- `tiny`: 39MB，EN，EN
- `base`: 74MB，EN，EN（EN）
- `small`: 244MB，EN，EN
- `medium`: 769MB，EN，EN
- `large`: 1550MB，EN，EN

### 2. OpenAI API（EN）

**EN：**
- ✅ EN
- ✅ SupportENLanguage
- ❌ ENAPIEN
- ❌ EN
- ❌ EN

**EN：**
```bash
# EN
export OPENAI_API_KEY="your-api-key-here"
```

### 3. EN（EN）

**EN：**
- ✅ EN
- ✅ EN
- ❌ EN，EN
- ❌ EN

## 🚀 EN

### EN（EN）

EN：

```python
from shared.utils.speech_recognizer import generate_subtitle_for_video

# EN
result = generate_subtitle_for_video(video_path, method="auto")
```

### EN

```python
# ENWhisper
result = generate_subtitle_for_video(video_path, method="whisper_local")

# ENOpenAI API
result = generate_subtitle_for_video(video_path, method="openai_api")

# EN
result = generate_subtitle_for_video(video_path, method="simple")
```

### EN

```python
from shared.utils.speech_recognizer import get_available_speech_recognition_methods

methods = get_available_speech_recognition_methods()
print(methods)
# EN：
# {
#     "whisper_local": True,
#     "openai_api": False,
#     "simple": True
# }
```

## 📝 EN

### ENWhisperEN

EN `shared/utils/speech_recognizer.py` ENWhisperEN：

```python
cmd = [
    'whisper',
    str(video_path),
    '--output_dir', str(output_path.parent),
    '--output_format', 'srt',
    '--language', 'zh',  # Language：zh(Chinese), en(English), auto(EN)
    '--model', 'base'    # EN：tiny, base, small, medium, large
]
```

### EN

- `--language`: ENLanguage，EN
- `--model`: EN，EN
- `--output_format`: EN，Supportsrt, vtt, txtEN
- `--task`: EN，transcribe(EN)ENtranslate(EN)

## 🔍 Troubleshooting

### WhisperEN

**EN：** `whisper: command not found`

**EN：**
```bash
# EN
pip list | grep whisper

# EN
pip uninstall openai-whisper
pip install openai-whisper

# ENPATH
which whisper
```

**EN：** EN

**EN：**
```bash
# EN（Ubuntu/Debian）
sudo apt update
sudo apt install ffmpeg

# EN（macOS）
brew install ffmpeg

# ENPythonEN
pip install torch torchvision torchaudio
```

### Performance

**EN：** WhisperEN

**EN：**
1. EN：`--model tiny`
2. ENGPUEN（EN）
3. EN

**EN：** EN

**EN：**
1. EN
2. EN
3. ENCPUEN

## 📊 EN

| EN | EN | EN | EN | EN | EN |
|------|------|--------|------|----------|----------|
| Whisper tiny | ⭐⭐⭐⭐⭐ | ⭐⭐ | EN | EN | EN |
| Whisper base | ⭐⭐⭐⭐ | ⭐⭐⭐ | EN | EN | EN |
| Whisper small | ⭐⭐⭐ | ⭐⭐⭐⭐ | EN | EN | EN |
| Whisper medium | ⭐⭐ | ⭐⭐⭐⭐⭐ | EN | EN | EN |
| OpenAI API | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | EN | EN | EN |
| EN | ⭐⭐⭐⭐⭐ | ⭐ | EN | EN | EN |

## 🎯 EN

### EN
```bash
# ENbaseEN（EN）
pip install openai-whisper
```

### EN
```bash
# ENsmallENmediumEN（EN）
pip install openai-whisper
# ENGPUEN
```

### EN
```bash
# EN，EN
# EN
```

## 📞 ENSupport

EN，EN：

1. EN
2. ENWhisperEN
3. ENSupport
4. EN

ENReference：
- [WhisperEN](https://github.com/openai/whisper)
- [OpenAI APIEN](https://platform.openai.com/docs/api-reference)
