# modelproviderintegrate

## 🎯 overview

nowsupportAImodelprovider，canneedselectservicemodel，AIclip。

## 🏗️ 

### supportprovider

| provider |  | model | features |
|--------|----------|----------|------|
| `dashscope` | Alibaba Qwen | qwen-plus, qwen-max, qwen-turbo | access，Chinese |
| `openai` | OpenAI | gpt-3.5-turbo, gpt-4, gpt-4-turbo | ， |
| `gemini` | Google Gemini | gemini-2.5-flash, gemini-1.5-pro | support， |
| `siliconflow` |  | Qwen2.5, DeepSeek-V2.5 | ， |

### 

```
┌─────────────────────────────────────────────────────────────┐
│                    frontendSettings page                              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ providerselect  │  │ APIkey │  │  model selection   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   backendAPIservice                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ settingsAPI │  │ testAPI │  │ modelAPI │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   LLM                                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ provider  │  │ API    │  │ config    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   provider                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ DashScope   │  │   OpenAI    │  │   Gemini    │         │
│  │  Provider   │  │  Provider   │  │  Provider   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐                                           │
│  │SiliconFlow  │                                           │
│  │  Provider   │                                           │
│  └─────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 quick start

### 1. installdependencies

```bash
# dependenciesinstall
python install_llm_dependencies.py

# install
pip install openai>=1.0.0 google-generativeai>=0.3.0 requests>=2.25.0 dashscope>=1.10.0
```

### 2. start

```bash
# startbackendservice
python backend/main.py

# startfrontendservice
cd frontend && npm run dev
```

### 3. configAPIkey

1. accessSettings page
2. selectAImodelprovider
3. APIkey
4. selectmodel
5. test
6. config

## 📋 config notes

### Alibaba Qwen (DashScope)

**fetchAPIkey:**
1. access [](https://dashscope.console.aliyun.com/)
2. Qwenservice
3. createAPIkey

**supportmodel:**
- `qwen-plus`: QwenPlus (recommend)
- `qwen-max`: QwenMax ()
- `qwen-turbo`: QwenTurbo ()

### OpenAI

**fetchAPIkey:**
1. access [OpenAI Platform](https://platform.openai.com/)
2. account
3. createAPIkey

**supportmodel:**
- `gpt-3.5-turbo`: GPT-3.5 Turbo ()
- `gpt-4`: GPT-4 ()
- `gpt-4-turbo`: GPT-4 Turbo ()

### Google Gemini

**fetchAPIkey:**
1. access [Google AI Studio](https://ai.google.dev/)
2. sign inGoogleaccount
3. createAPIkey

**supportmodel:**
- `gemini-2.5-flash`: Gemini 2.5 Flash ()
- `gemini-1.5-pro`: Gemini 1.5 Pro ()
- `gemini-1.5-flash`: Gemini 1.5 Flash ()

### 

**fetchAPIkey:**
1. access [](https://cloud.siliconflow.cn/)
2. account
3. createAPIkey

**supportmodel:**
- `Qwen/Qwen2.5-7B-Instruct`: Qwen2.5-7B
- `Qwen/Qwen2.5-14B-Instruct`: Qwen2.5-14B
- `Qwen/Qwen2.5-32B-Instruct`: Qwen2.5-32B
- `deepseek-ai/DeepSeek-V2.5`: DeepSeek-V2.5

### Ollama / LM Studio（local，no need API key）

Settings page「modelprovider」「Ollama（local）」「LM Studio（local）」， OpenAI API +  `base_url`：

|  | default | defaultmodel |
|---|---|---|
| Ollama | `http://localhost:11434/v1` | `qwen2.5:7b`（`ollama pull qwen2.5:7b`） |
| LM Studio | `http://localhost:1234/v1` |  Local Server  |

serviceavailablemodel；。proxy（Clash ）impactlocal。
CLI available：`autoclip run video.mp4 --provider ollama`。 `docs/CLI_AND_MCP.md`  4 。

## 🔧 technical details

### 

#### 1. LLMProvider 

```python
class LLMProvider(ABC):
    @abstractmethod
    def call(self, prompt: str, input_data: Any = None, **kwargs) -> LLMResponse:
        """callmodelAPI"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """testAPI"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[ModelInfo]:
        """fetchavailablemodel"""
        pass
```

#### 2. provider

```python
class LLMProviderFactory:
    _providers = {
        ProviderType.DASHSCOPE: DashScopeProvider,
        ProviderType.OPENAI: OpenAIProvider,
        ProviderType.GEMINI: GeminiProvider,
        ProviderType.SILICONFLOW: SiliconFlowProvider,
    }
    
    @classmethod
    def create_provider(cls, provider_type: ProviderType, api_key: str, model_name: str, **kwargs) -> LLMProvider:
        """createprovider"""
        pass
```

#### 3. LLM

```python
class LLMManager:
    def __init__(self, settings_file: Optional[Path] = None):
        """"""
        pass
    
    def set_provider(self, provider_type: ProviderType, api_key: str, model_name: str):
        """settingsprovider"""
        pass
    
    def call(self, prompt: str, input_data: Any = None, **kwargs) -> str:
        """callLLM"""
        pass
```

### APIAPI

#### settings

```http
GET /api/v1/settings
POST /api/v1/settings
```

#### test

```http
POST /api/v1/settings/test-api-key
```

#### model

```http
GET /api/v1/settings/available-models
GET /api/v1/settings/current-provider
```

## 🎨 frontend

### Settings page

1. **providerselect**: selectAImodelprovider
2. **APIkey**: providerkey
3. **model selection**: selectprovideravailablemodel
4. **test**: testAPIkeymodelavailable
5. **status**: useprovidermodel

### features

- responsive design，support
- ，
- status，
- usenotes

## 🔍 troubleshooting

### FAQ

#### 1. APIkey

**symptom**: testconnection failed，"API Key"

**solution**:
- checkAPIkey
- confirmAPIkey
- check

#### 2. network issue

**symptom**: error

**solution**:
- check network connection
- confirmsettings
- useproxy（need）

#### 3. modelavailable

**symptom**: selectmodeluse

**solution**:
- checkmodel
- confirmusemodel
- availablemodel

#### 4. dependenciesissue

**symptom**: importerror

**solution**:
```bash
# installdependencies
python install_llm_dependencies.py

# install
pip install --upgrade openai google-generativeai requests dashscope
```

### view

location：

- backend: `logs/backend.log`
- frontend: tool

## 🚀 

### provider

1. **createprovider**:
```python
class NewProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str, **kwargs):
        super().__init__(api_key, model_name, **kwargs)
    
    def call(self, prompt: str, input_data: Any = None, **kwargs) -> LLMResponse:
        # APIcall
        pass
    
    def test_connection(self) -> bool:
        # test
        pass
    
    def get_available_models(self) -> List[ModelInfo]:
        # returnavailablemodel
        pass
```

2. ****:
```python
#  llm_providers.py 
class LLMProviderFactory:
    _providers = {
        # ... provider
        ProviderType.NEW_PROVIDER: NewProvider,
    }
```

3. **updatefrontendconfig**:
```typescript
//  SettingsPage.tsx 
const providerConfig = {
  // ... config
  new_provider: {
    name: 'provider',
    icon: <RobotOutlined />,
    color: '#ff4d4f',
    description: 'provider',
    apiKeyField: 'new_provider_api_key',
    placeholder: 'providerAPIkey'
  }
}
```

## 📊 

| provider |  | Chinese |  |  | recommend |
|--------|----------|----------|------|--------|----------|
| Alibaba Qwen | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Chinese |
| OpenAI | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |  |
| Google Gemini | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |  |
|  | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |  |

## 🎯 best practices

1. **selectprovider**: selectprovider
2. **test**: APIkeymodelavailable
3. **monitoruse**: limit
4. **config**: APIkeyconfig
5. **security**: APIkey

## 📞 tech support

useissue，canget help：

1. viewfile
2. checkAPIproviderdocs
3. tech support

---

****: APIkey，security。APIkeysecurity。
