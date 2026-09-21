# 🎤 speech recognitionsettings

## 📋 overview

AutoClipsupportspeech recognitiongeneratesubtitlesfile，subtitles，generatesubtitles。

## 🔧 supportspeech recognition

### 1. localWhisper（recommend）

**features：**
- ✅ local，no need
- ✅ no needAPIkey
- ✅ free use
- ✅ support
- ✅ 

**installmethod：**

```bash
# method1：usepipinstall
pip install openai-whisper

# method2：usecondainstall
conda install -c conda-forge openai-whisper

# method3：install
git clone https://github.com/openai/whisper.git
cd whisper
pip install -e .
```

**verifyinstall：**
```bash
whisper --help
```

**model selection：**
- `tiny`: 39MB，，
- `base`: 74MB，，medium（default）
- `small`: 244MB，medium，
- `medium`: 769MB，，
- `large`: 1550MB，，

### 2. OpenAI API（）

**features：**
- ✅ 
- ✅ support
- ❌ needAPIkey
- ❌ need
- ❌ usecost

**settingsmethod：**
```bash
# settingsenv var
export OPENAI_API_KEY="your-api-key-here"
```

### 3. testsubtitles（）

**features：**
- ✅ no needinstalldependencies
- ✅ available
- ❌ test，subtitles
- ❌ 

## 🚀 use

### （default）

selectavailablemethod：

```python
from shared.utils.speech_recognizer import generate_subtitle_for_video

# selectmethod
result = generate_subtitle_for_video(video_path, method="auto")
```

### method

```python
# uselocalWhisper
result = generate_subtitle_for_video(video_path, method="whisper_local")

# useOpenAI API
result = generate_subtitle_for_video(video_path, method="openai_api")

# usetestsubtitles
result = generate_subtitle_for_video(video_path, method="simple")
```

### checkavailablemethod

```python
from shared.utils.speech_recognizer import get_available_speech_recognition_methods

methods = get_available_speech_recognition_methods()
print(methods)
# ：
# {
#     "whisper_local": True,
#     "openai_api": False,
#     "simple": True
# }
```

## 📝 config

### Whisper

 `shared/utils/speech_recognizer.py` canWhisper：

```python
cmd = [
    'whisper',
    str(video_path),
    '--output_dir', str(output_path.parent),
    '--output_format', 'srt',
    '--language', 'zh',  # ：zh(Chinese), en(English), auto(auto-detect)
    '--model', 'base'    # model：tiny, base, small, medium, large
]
```

### notes

- `--language`: ，
- `--model`: selectmodel，impact
- `--output_format`: format，supportsrt, vtt, txt
- `--task`: ，transcribe()translate()

## 🔍 troubleshooting

### Whisperinstallissue

**issue：** `whisper: command not found`

**solution：**
```bash
# checkinstallsucceeded
pip list | grep whisper

# install
pip uninstall openai-whisper
pip install openai-whisper

# checkPATH
which whisper
```

**issue：** dependencies

**solution：**
```bash
# installdependencies（Ubuntu/Debian）
sudo apt update
sudo apt install ffmpeg

# installdependencies（macOS）
brew install ffmpeg

# installPythondependencies
pip install torch torchvision torchaudio
```

### performance

**issue：** Whisper

**solution：**
1. use a smaller model：`--model tiny`
2. useGPU（available）
3. 

**issue：** out of memory

**solution：**
1. use a smaller model
2. memory
3. useCPU

## 📊 

| method |  |  |  | dependencies | install |
|------|------|--------|------|----------|----------|
| Whisper tiny | ⭐⭐⭐⭐⭐ | ⭐⭐ | free |  |  |
| Whisper base | ⭐⭐⭐⭐ | ⭐⭐⭐ | free |  |  |
| Whisper small | ⭐⭐⭐ | ⭐⭐⭐⭐ | free |  |  |
| Whisper medium | ⭐⭐ | ⭐⭐⭐⭐⭐ | free |  |  |
| OpenAI API | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |  | need |  |
| testsubtitles | ⭐⭐⭐⭐⭐ | ⭐ | free |  | no needinstall |

## 🎯 recommended config

### dev environment
```bash
# installbasemodel（）
pip install openai-whisper
```

### production
```bash
# installsmallmediummodel（）
pip install openai-whisper
# useGPU
```

### test
```bash
# no needinstall，usetestsubtitles
# generatetestsubtitlesfile
```

## 📞 tech support

if you encounter issues，：

1. checkfileerror
2. verifyWhisperinstall
3. confirmfileformatsupport
4. view

：
- [Whisperdocs](https://github.com/openai/whisper)
- [OpenAI APIdocs](https://platform.openai.com/docs/api-reference)
