# ENProvidesEN

## 🎯 EN

ENSupportENAIENProvidesEN，EN，ENAIAuto ClippingEN。

## 🏗️ EN

### SupportENProvidesEN

| ProvidesEN | EN | EN | EN |
|--------|----------|----------|------|
| `dashscope` | EN | qwen-plus, qwen-max, qwen-turbo | EN，ChineseEN |
| `openai` | OpenAI | gpt-3.5-turbo, gpt-4, gpt-4-turbo | EN，EN |
| `gemini` | Google Gemini | gemini-2.5-flash, gemini-1.5-pro | ENSupport，EN |
| `siliconflow` | EN | Qwen2.5EN, DeepSeek-V2.5 | EN，EN |

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EN                              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ ProvidesEN  │  │ APIEN │  │  EN   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   ENAPIEN                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ ENAPI │  │ ENAPI │  │ ENAPI │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   LLMEN                                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ ProvidesEN  │  │ EN    │  │ EN    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   ENProvidesEN                            │
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

## 🚀 Quick Start

### 1. EN

```bash
# EN
python install_llm_dependencies.py

# ENManual Installation
pip install openai>=1.0.0 google-generativeai>=0.3.0 requests>=2.25.0 dashscope>=1.10.0
```

### 2. EN

```bash
# EN
python backend/main.py

# EN
cd frontend && npm run dev
```

### 3. ENAPIEN

1. EN
2. ENAIENProvidesEN
3. ENAPIEN
4. EN
5. EN
6. EN

## 📋 ENConfiguration

### EN (DashScope)

**ENAPIEN:**
1. EN [EN](https://dashscope.console.aliyun.com/)
2. EN
3. ENAPIEN

**SupportEN:**
- `qwen-plus`: ENPlus (EN)
- `qwen-max`: ENMax (EN)
- `qwen-turbo`: ENTurbo (EN)

### OpenAI

**ENAPIEN:**
1. EN [OpenAI Platform](https://platform.openai.com/)
2. ENAccountEN
3. ENAPIEN

**SupportEN:**
- `gpt-3.5-turbo`: GPT-3.5 Turbo (EN)
- `gpt-4`: GPT-4 (EN)
- `gpt-4-turbo`: GPT-4 Turbo (EN)

### Google Gemini

**ENAPIEN:**
1. EN [Google AI Studio](https://ai.google.dev/)
2. ENGoogleAccount
3. ENAPIEN

**SupportEN:**
- `gemini-2.5-flash`: Gemini 2.5 Flash (EN)
- `gemini-1.5-pro`: Gemini 1.5 Pro (EN)
- `gemini-1.5-flash`: Gemini 1.5 Flash (EN)

### EN

**ENAPIEN:**
1. EN [EN](https://cloud.siliconflow.cn/)
2. ENAccount
3. ENAPIEN

**SupportEN:**
- `Qwen/Qwen2.5-7B-Instruct`: Qwen2.5-7B
- `Qwen/Qwen2.5-14B-Instruct`: Qwen2.5-14B
- `Qwen/Qwen2.5-32B-Instruct`: Qwen2.5-32B
- `deepseek-ai/DeepSeek-V2.5`: DeepSeek-V2.5

### Ollama / LM Studio（EN，EN API EN）

EN「ENProvidesEN」EN「Ollama（EN）」EN「LM Studio（EN）」，EN OpenAI EN + EN `base_url`：

| EN | EN | EN |
|---|---|---|
| Ollama | `http://localhost:11434/v1` | `qwen2.5:7b`（`ollama pull qwen2.5:7b`） |
| LM Studio | `http://localhost:1234/v1` | EN Local Server ENAs Standard |

EN；EN。EN（Clash EN）EN。
CLI EN：`autoclip run video.mp4 --provider ollama`。EN `docs/CLI_AND_MCP.md` EN 4 EN。

## 🔧 EN

### EN

#### 1. LLMProvider EN

```python
class LLMProvider(ABC):
    @abstractmethod
    def call(self, prompt: str, input_data: Any = None, **kwargs) -> LLMResponse:
        """ENAPI"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """ENAPIEN"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[ModelInfo]:
        """EN"""
        pass
```

#### 2. ProvidesEN

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
        """ENProvidesEN"""
        pass
```

#### 3. LLMEN

```python
class LLMManager:
    def __init__(self, settings_file: Optional[Path] = None):
        """EN"""
        pass
    
    def set_provider(self, provider_type: ProviderType, api_key: str, model_name: str):
        """ENProvidesEN"""
        pass
    
    def call(self, prompt: str, input_data: Any = None, **kwargs) -> str:
        """ENLLM"""
        pass
```

### APIEN

#### EN

```http
GET /api/v1/settings
POST /api/v1/settings
```

#### EN

```http
POST /api/v1/settings/test-api-key
```

#### EN

```http
GET /api/v1/settings/available-models
GET /api/v1/settings/current-provider
```

## 🎨 ENInterface

### EN

1. **ProvidesEN**: ENAIENProvidesEN
2. **APIEN**: ENProvidesEN
3. **EN**: ENProvidesEN
4. **EN**: ENAPIEN
5. **EN**: ENProvidesEN

### InterfaceEN

- Responsive Design，SupportEN
- EN，EN
- EN，EN
- EN

## 🔍 Troubleshooting

### FAQ

#### 1. APIEN

**EN**: EN，EN"API KeyEN"

**EN**:
- ENAPIEN
- ENAPIEN
- EN

#### 2. EN

**EN**: EN

**EN**:
- EN
- EN
- EN（EN）

#### 3. EN

**EN**: EN

**EN**:
- EN
- EN
- EN

#### 4. EN

**EN**: EN

**EN**:
```bash
# EN
python install_llm_dependencies.py

# ENManual Installation
pip install --upgrade openai google-generativeai requests dashscope
```

### EN

EN：

- EN: `logs/backend.log`
- EN: EN

## 🚀 EN

### ENProvidesEN

1. **ENProvidesEN**:
```python
class NewProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str, **kwargs):
        super().__init__(api_key, model_name, **kwargs)
    
    def call(self, prompt: str, input_data: Any = None, **kwargs) -> LLMResponse:
        # ENAPIEN
        pass
    
    def test_connection(self) -> bool:
        # EN
        pass
    
    def get_available_models(self) -> List[ModelInfo]:
        # EN
        pass
```

2. **EN**:
```python
# EN llm_providers.py EN
class LLMProviderFactory:
    _providers = {
        # ... ENProvidesEN
        ProviderType.NEW_PROVIDER: NewProvider,
    }
```

3. **EN**:
```typescript
// EN SettingsPage.tsx EN
const providerConfig = {
  // ... EN
  new_provider: {
    name: 'ENProvidesEN',
    icon: <RobotOutlined />,
    color: '#ff4d4f',
    description: 'ENProvidesEN',
    apiKeyField: 'new_provider_api_key',
    placeholder: 'ENProvidesENAPIEN'
  }
}
```

## 📊 EN

| ProvidesEN | EN | ChineseEN | EN | EN | EN |
|--------|----------|----------|------|--------|----------|
| EN | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ChineseEN |
| OpenAI | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | EN |
| Google Gemini | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | EN |
| EN | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | EN |

## 🎯 EN

1. **ENProvidesEN**: ENProvidesEN
2. **EN**: ENAPIEN
3. **EN**: EN
4. **EN**: ENAPIEN
5. **EN**: Do notENAPIEN

## 📞 ENSupport

EN，EN：

1. EN
2. ENAPIProvidesEN
3. ContactENSupportEN

---

**EN**: ENAPIEN，Do notEN。ENAPIEN。
