# ⚡ AutoClip Desktop 

## 🚀 quick start

### use
1. start → config → settingsAPIkey → use

### 
```
 →  → viewclip → create collection → export
```

## 📋 

|  |  | notes |
|------|--------|------|
| new project | `Ctrl/Cmd + N` | createproject |
| openproject | `Ctrl/Cmd + O` | openproject |
| project | `Ctrl/Cmd + S` | project |
| refresh page | `F5` | page |
| opensettings | `Ctrl/Cmd + ,` | openSettings page |
|  | `Ctrl/Cmd + Q` |  |

## 📁 supportfileformat

### format
- **MP4** ✅ (recommend)
- **AVI** ✅
- **MOV** ✅
- **MKV** ✅
- **WEBM** ✅
- **FLV** ✅
- **WMV** ✅

### subtitlesformat
- **SRT** ✅ (recommend)
- **VTT** ✅
- **ASS** ✅
- **SSA** ✅

## ⚙️ config

### speech recognitionconfig

#### localWhispermodel
```yaml
model selection:
  - base:  (recommend)
  - small: 
  - medium: 
  - large: 

settings:
  - auto: auto-detect
  - zh: Chinese
  - en: English
  - ja: Japanese
```

#### cloudAPIservice
```yaml
OpenAI Whisper:
  - pros: 、
  - cons: need

Azure Speech:
  - pros: service
  - cons: config

Google Cloud:
  - pros: free
  - cons: needGoogleaccount
```

### AImodelconfig

#### recommended config
```yaml
Alibaba Qwen:
  - model: qwen-plus
  - pros: Chinesesupport
  - applicable: Chinese

OpenAI GPT:
  - model: gpt-4
  - pros: 
  - applicable: 

Google Gemini:
  - model: gemini-pro
  - pros: free
  - applicable: daily use
```

## 🎯 settings

### 

| settings |  | medium |  |
|------|--------|----------|--------|
| filelimit | 512MB | 2GB | 5GB |
|  | 1 | 2 | 4 |
| memoryuse | 2GB | 4GB | 8GB |
|  |  | medium |  |
| use cases |  | daily use |  |

### recommended config

#### 
```yaml
: medium
speech recognition: localWhisper (basemodel)
AImodel: Alibaba Qwen
: 2
```

#### 
```yaml
: 
speech recognition: cloudAPI
AImodel: OpenAI GPT-4
: 4
```

## 🔧 

### project management

#### createproject
1. click "new project"
2. selectfile
3. project
4. click ""

#### project status
- 🔄 **processing**: 
- ✅ **completed**: canview
- ❌ **failed**: need
- ⏸️ ****: 

### clip

#### clip
- **90-100**: ，recommend
- **80-89**: ，recommended
- **70-79**: ，canuse
- **60-69**: ，use
- **60**: recommended

#### clip
- ****: clickclip
- **edit**: clickeditbutton
- ****: clickbutton
- ****: selectclick"create collection"

### 

#### 
- **AIrecommend**: recommend
- **create**: select
- ****: 
- ****: 

#### 
- **view**: click
- **edit**: 
- ****: 
- **export**: generate

## 🚨 troubleshooting

### FAQ

#### start
```bash
checkproject:
1. 
2. install
3. checksettings
4. viewerror
```

#### failed
```bash
reason:
- fileformatsupport
- file
- network issue
- 

solution:
1. checkfileformat
2. check network connection
3. 
4. 
```

#### 
```bash
:
1. settings
2. 
3. usecloudAPI
4. selectmodel
```

#### APIconnection failed
```bash
checkstep:
1. verifyAPIkey
2. check network connection
3. confirmservicestatus
4. check
```

### error

|  | issue | solve |
|------|------|------|
| ERR_001 | fileformatsupport | useMP4format |
| ERR_002 | file | file |
| ERR_003 | APIkey | updateAPIkey |
| ERR_004 | connection failed | checksettings |
| ERR_005 |  |  |
| ERR_006 | out of memory | settings |

## 📊 best practices

### 
```yaml
:
  - : 1080p+
  - : 30fps+
  - : 

:
  - 
  - 
  - 
  - 
```

### clip
```yaml
:
  - 
  - 
  - 30

:
  - 
  - 
  - 
```

### 
```yaml
:
  - 
  - 
  - 

:
  - 
  - 
  - update
```

## 🔄 update

### auto-update
- checkupdate
- click"update"installversion
- restart app

### manual update
1. accessGitHub Releasespage
2. downloadinstall
3. install

### 
```yaml
:
  - project
  - configfile
  - settings

location:
  - macOS: ~/Library/Application Support/AutoClip
  - Windows: %APPDATA%/AutoClip
  - Linux: ~/.config/AutoClip
```

## 📞 get help

### 
- ****: usenotes
- ****: 
- **FAQ**: FAQsolution

### tech support
- **GitHub Issues**: issue
- ****: 
- **support**: tech support

### 
- ****: 
- **use**: 
- **issue**: issue

---

## 💡 

1. **use**：
2. **performance**：configselect
3. **APIconfig**：configAPIservice
4. ****：needprojectcachefile
5. ****：project

🎉 **use！**
