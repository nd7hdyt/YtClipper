import React, { useState, useEffect, useMemo } from 'react'
import { Form, Input, Select, Switch, message } from 'antd'
import { useLocation } from 'react-router-dom'
import { settingsApi } from '../services/api'
import SpeechRecognitionConfig from '../components/SpeechRecognitionConfig'
import FeedbackDialog from '../components/FeedbackDialog'
import { isDesktopMode } from '../utils/desktopMode'
import { openExternalLink } from '../utils/externalLinks'
import { trackApiKeyConfigured } from '../analytics/events'
import { isAnalyticsEnabled, setAnalyticsEnabled } from '../analytics/posthog'
import { getRuntimeInfo } from '../analytics/lifecycle'
import { FEEDBACK_FORM_URL, FEEDBACK_ISSUES_URL } from '../analytics/feedback'
import { useTheme } from '../context/ThemeContext'
import { Btn, Icon, Row, Section, Segmented, StatusDot } from '../ui'

const normalizeBaseUrl = (value: unknown): string =>
  typeof value === 'string' ? value.trim().replace(/\/+$/, '') : ''

// The model Select uses mode="tags"; manual input yields an array, but the backend only accepts a string
const normalizeModelName = (value: unknown): string => {
  if (Array.isArray(value)) return String(value[value.length - 1] ?? '').trim()
  return typeof value === 'string' ? value.trim() : ''
}
const toNumber = (v: unknown, fallback: number): number => {
  const n = typeof v === 'number' ? v : parseFloat(String(v ?? ''))
  return Number.isFinite(n) ? n : fallback
}

type ProviderKey = 'dashscope' | 'openai' | 'gemini' | 'siliconflow' | 'ollama' | 'lmstudio'
type LocalPreset = { baseUrl: string; defaultModel: string; docsUrl: string; app: string }
const PROVIDERS: Record<ProviderKey, { name: string; short: string; hint: string; apiKeyField: string; placeholder: string; keyUrl: string; local?: LocalPreset }> = {
  dashscope: { name: 'Alibaba Qwen', short: 'Qwen', hint: 'Alibaba Cloud DashScope. Direct connection in China; qwen-plus is the best value.', apiKeyField: 'dashscope_api_key', placeholder: 'sk-...', keyUrl: 'https://dashscope.console.aliyun.com/apiKey' },
  openai: { name: 'OpenAI / Compatible API', short: 'OpenAI Compatible', hint: 'OpenAI, or any compatible API: Zhipu, DeepSeek, OpenRouter, vLLM.', apiKeyField: 'openai_api_key', placeholder: 'sk-... (leave empty for self-hosted)', keyUrl: 'https://platform.openai.com/api-keys' },
  gemini: { name: 'Google Gemini', short: 'Gemini', hint: 'Gemini family from Google AI Studio.', apiKeyField: 'gemini_api_key', placeholder: 'AIza...', keyUrl: 'https://aistudio.google.com/apikey' },
  siliconflow: { name: 'SiliconFlow', short: 'SiliconFlow', hint: 'SiliconFlow hub with open models like DeepSeek / Qwen.', apiKeyField: 'siliconflow_api_key', placeholder: 'sk-...', keyUrl: 'https://cloud.siliconflow.cn/account/ak' },
  // Local presets: OpenAI-compatible + base_url under the hood, resolved by backend core/local_presets.py; no key, free, offline
  ollama: { name: 'Ollama', short: 'Ollama', hint: 'Local Ollama, free and offline. Recommended: ollama pull qwen2.5:7b.', apiKeyField: 'openai_api_key', placeholder: '', keyUrl: 'https://ollama.com/download', local: { baseUrl: 'http://localhost:11434/v1', defaultModel: 'qwen2.5:7b', docsUrl: 'https://ollama.com/download', app: 'Ollama' } },
  lmstudio: { name: 'LM Studio', short: 'LM Studio', hint: 'Local LM Studio server, free and offline. Load a model and start the server in LM Studio.', apiKeyField: 'openai_api_key', placeholder: '', keyUrl: 'https://lmstudio.ai', local: { baseUrl: 'http://localhost:1234/v1', defaultModel: '', docsUrl: 'https://lmstudio.ai', app: 'LM Studio' } },
}
const isLocalProvider = (p: ProviderKey) => !!PROVIDERS[p]?.local

// Qwen international endpoint (keys from alibabacloud.com only work here, #45); backend picks compat mode from base_url
const DASHSCOPE_INTL_BASE_URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'
type DashscopeRegion = 'cn' | 'intl'

const MODEL_GROUPS: Array<{ label: string; models: string[] }> = [
  { label: 'Qwen', models: ['qwen-plus', 'qwen-turbo', 'qwen-max', 'qwen-long'] },
  { label: 'OpenAI', models: ['gpt-4o', 'gpt-4o-mini', 'gpt-4.1', 'gpt-4.1-mini'] },
  { label: 'Gemini', models: ['gemini-2.5-pro', 'gemini-2.5-flash', 'gemini-1.5-pro', 'gemini-1.5-flash'] },
  { label: 'SiliconFlow / Open', models: ['deepseek-ai/DeepSeek-V3', 'deepseek-chat', 'Qwen/Qwen2.5-72B-Instruct'] },
]

const CLOUD_DEFAULT_MODEL: Partial<Record<ProviderKey, string>> = {
  dashscope: 'qwen-plus', openai: 'gpt-4o-mini', gemini: 'gemini-2.5-flash', siliconflow: 'deepseek-ai/DeepSeek-V3',
}

type SectionKey = 'model' | 'speech' | 'app' | 'feedback'
const NAV: Array<{ key: SectionKey; label: string }> = [
  { key: 'model', label: 'Model' },
  { key: 'speech', label: 'Transcription' },
  { key: 'app', label: 'App' },
  { key: 'feedback', label: 'Feedback' },
]

// Calm Premium settings — left nav + setting rows (see DESIGN.md → App Layer)
const SettingsPage: React.FC = () => {
  const [form] = Form.useForm()
  const location = useLocation()
  const initialSection = useMemo<SectionKey>(() => {
    const s = new URLSearchParams(location.search).get('section')
    return (NAV.find((n) => n.key === s)?.key as SectionKey) || 'model'
  }, [location.search])
  const [active, setActive] = useState<SectionKey>(initialSection)
  const [loading, setLoading] = useState(false)
  const [testing, setTesting] = useState(false)
  const [currentProvider, setCurrentProvider] = useState<any>({})
  const [selectedProvider, setSelectedProvider] = useState<ProviderKey>('dashscope')
  // Local preset model probing: { reachable, models } — pick from dropdown instead of typing qwen2.5:7b
  const [localModels, setLocalModels] = useState<{ loading: boolean; reachable: boolean | null; models: string[] }>({ loading: false, reachable: null, models: [] })
  const [dashscopeRegion, setDashscopeRegion] = useState<DashscopeRegion>('cn')
  const [analyticsOn, setAnalyticsOn] = useState(isAnalyticsEnabled())
  const [feedbackOpen, setFeedbackOpen] = useState(false)
  const runtime = getRuntimeInfo()

  useEffect(() => { loadData() }, [])
  useEffect(() => { setActive(initialSection) }, [initialSection])

  // Desktop / Docker / local script all use the same /settings API: settings.json lives in the backend data dir,
  // API process and worker hot-reload by mtime. Docker users previously could only edit .env (#100).
  const loadData = async () => {
    try {
      const [settings, provider] = await Promise.allSettled([
        settingsApi.getSettings(),
        settingsApi.getCurrentProvider()
      ])
      if (settings.status === 'rejected') console.warn('Failed to load settings:', settings.reason)
      const settingsData = settings.status === 'fulfilled' ? settings.value : {}
      const providerData = provider.status === 'fulfilled'
        ? provider.value
        : { available: false, provider: 'dashscope', display_name: 'Alibaba Qwen', model: 'qwen-plus' }
      // The provider saved in settings.json wins; fall back to the backend-reported provider for legacy configs
      const providerName = (settingsData.api?.api_provider || providerData.provider || 'dashscope') as ProviderKey
      setCurrentProvider(providerData)
      const savedBaseUrl = settingsData.api?.api_base_url || ''
      const localPreset = PROVIDERS[providerName]?.local
      setDashscopeRegion(providerName === 'dashscope' && normalizeBaseUrl(savedBaseUrl) === DASHSCOPE_INTL_BASE_URL ? 'intl' : 'cn')
      form.setFieldsValue({
        llm_provider: providerName,
        dashscope_api_key: settingsData.api?.api_keys?.dashscope || '',
        openai_api_key: settingsData.api?.api_keys?.openai || '',
        openai_base_url: localPreset || providerName === 'dashscope' ? '' : savedBaseUrl,
        // Only fill the local preset address into the form when it differs from the default
        local_base_url: localPreset && savedBaseUrl && savedBaseUrl !== localPreset.baseUrl ? savedBaseUrl : '',
        gemini_api_key: settingsData.api?.api_keys?.gemini || '',
        siliconflow_api_key: settingsData.api?.api_keys?.siliconflow || '',
        jimeng_access_key: settingsData.api?.api_keys?.jimeng_access || '',
        jimeng_secret_key: settingsData.api?.api_keys?.jimeng_secret || '',
        model_name: settingsData.api?.api_model || 'qwen-plus',
        chunk_size: settingsData.processing?.processing_chunk_size || 5000,
        min_score_threshold: settingsData.processing?.processing_min_score || 0.7,
        max_clips_per_collection: settingsData.processing?.processing_max_clips || 5
      })
      setSelectedProvider(PROVIDERS[providerName] ? providerName : 'dashscope')
    } catch (err) {
      console.error('Failed to load data:', err)
    }
  }

  const handleSave = async (values: any) => {
    try {
      setLoading(true)
      // Read existing config first so we don't wipe keys saved for other providers
      let existing: any = null
      try { existing = await settingsApi.getSettings() } catch (err) { console.warn('Failed to fetch existing config:', err) }
      const keys = existing?.api?.api_keys || {}
      const provider = (values.llm_provider || selectedProvider) as ProviderKey

      await settingsApi.updateSettings({
        basic: { app_name: 'AutoClip Desktop', app_version: runtime.version !== 'unknown' ? runtime.version : '1.0.0', debug_mode: false, auto_start: true },
        service: { host: '127.0.0.1', port: 8000, max_memory_usage: 2048 },
        api: {
          api_keys: {
            dashscope: values.dashscope_api_key || keys.dashscope || '',
            openai: values.openai_api_key || keys.openai || '',
            gemini: values.gemini_api_key || keys.gemini || '',
            siliconflow: values.siliconflow_api_key || keys.siliconflow || '',
            jimeng_access: values.jimeng_access_key || keys.jimeng_access || '',
            jimeng_secret: values.jimeng_secret_key || keys.jimeng_secret || ''
          },
          api_provider: provider,
          api_base_url: provider === 'openai'
            ? normalizeBaseUrl(values.openai_base_url)
            : isLocalProvider(provider) ? normalizeBaseUrl(values.local_base_url)
            : provider === 'dashscope' && dashscopeRegion === 'intl' ? DASHSCOPE_INTL_BASE_URL : '',
          api_model: normalizeModelName(values.model_name) || 'qwen-plus',
          api_max_tokens: 4096,
          api_timeout: 30
        },
        processing: {
          processing_chunk_size: toNumber(values.chunk_size, 5000),
          processing_min_score: toNumber(values.min_score_threshold, 0.7),
          processing_max_clips: toNumber(values.max_clips_per_collection, 5),
          processing_max_retries: 3
        },
        logs: { log_level: 'INFO', log_retention_days: 7 }
        // paths are decided by the backend data dir; the frontend does not send them
      })
      message.success('Saved')
      trackApiKeyConfigured({ provider, hasKey: isLocalProvider(provider) || !!values[PROVIDERS[provider].apiKeyField] })
      await loadData()
    } catch (err: any) {
      message.error('Save failed: ' + (err.message || 'Unknown error'))
    } finally {
      setLoading(false)
    }
  }

  const handleTest = async () => {
    const cfg = PROVIDERS[selectedProvider]
    const local = isLocalProvider(selectedProvider)
    const apiKey: string = local ? '' : (form.getFieldValue(cfg.apiKeyField) || '')
    const baseUrl = selectedProvider === 'openai'
      ? normalizeBaseUrl(form.getFieldValue('openai_base_url'))
      : local ? (normalizeBaseUrl(form.getFieldValue('local_base_url')) || cfg.local!.baseUrl)
      : selectedProvider === 'dashscope' && dashscopeRegion === 'intl' ? DASHSCOPE_INTL_BASE_URL : ''
    const modelName = normalizeModelName(form.getFieldValue('model_name'))
    if (local && !modelName) {
      message.error('Please select a model first')
      return
    }
    // Self-hosted compatible services (Ollama / vLLM etc.) usually need no key; an address is enough to test
    if (!apiKey.trim() && !baseUrl) {
      message.error('Please enter an API key first')
      return
    }
    try {
      setTesting(true)
      const r = await settingsApi.testApiKey(selectedProvider, apiKey, { baseUrl: baseUrl || undefined, model: modelName || undefined })
      if (r.success) message.success('Connection OK')
      else message.error('Connection failed: ' + (r.error || 'Unknown error'))
    } catch (err: any) {
      message.error('Test failed: ' + (err.message || 'Unknown error'))
    } finally {
      setTesting(false)
    }
  }

  const detectLocalModels = async (p: ProviderKey, baseUrl?: string) => {
    const preset = PROVIDERS[p]?.local
    if (!preset) return
    setLocalModels((s) => ({ ...s, loading: true }))
    try {
      const r = await settingsApi.listCompatibleModels({ provider: p, baseUrl: normalizeBaseUrl(baseUrl) || undefined })
      setLocalModels({ loading: false, reachable: r.reachable, models: r.models || [] })
      // If models are detected and nothing is selected (or selection is stale), pick one (preset default first)
      const current = normalizeModelName(form.getFieldValue('model_name'))
      if (r.reachable && r.models.length && (!current || !r.models.includes(current))) {
        form.setFieldsValue({ model_name: r.models.includes(preset.defaultModel) ? preset.defaultModel : r.models[0] })
      }
    } catch {
      setLocalModels({ loading: false, reachable: false, models: [] })
    }
  }

  const handleProviderChange = (p: ProviderKey) => {
    const prev = selectedProvider
    setSelectedProvider(p)
    form.setFieldsValue({ llm_provider: p })
    const preset = PROVIDERS[p]?.local
    const current = normalizeModelName(form.getFieldValue('model_name'))
    if (preset) {
      // Switching cloud -> local: cloud names like qwen-plus mean nothing locally
      if (!current || MODEL_GROUPS.some((g) => g.models.includes(current))) {
        form.setFieldsValue({ model_name: preset.defaultModel || undefined })
      }
      void detectLocalModels(p, form.getFieldValue('local_base_url'))
    } else if (isLocalProvider(prev) || !current) {
      // Switching local -> cloud: local names like qwen2.5:7b mean nothing in the cloud, use a common default
      form.setFieldsValue({ model_name: CLOUD_DEFAULT_MODEL[p] })
    }
  }

  // Probe once when opening Settings on a local preset
  useEffect(() => {
    if (isLocalProvider(selectedProvider)) void detectLocalModels(selectedProvider, form.getFieldValue('local_base_url'))
  }, [selectedProvider])

  const openaiBaseUrl = Form.useWatch('openai_base_url', form)
  const usingCustomEndpoint = selectedProvider === 'openai' && !!normalizeBaseUrl(openaiBaseUrl)
  const cfg = PROVIDERS[selectedProvider]
  const localCfg = cfg.local
  const keyUrl = selectedProvider === 'dashscope' && dashscopeRegion === 'intl'
    ? 'https://bailian.console.alibabacloud.com/?tab=model#/api-key'
    : cfg.keyUrl

  return (
    <div className="ac-page">
      <header>
        <h1 className="ac-title" style={{ marginTop: 0 }}>Settings</h1>
        <div className="ac-meta">
          <span className="ac-mono">{runtime.version !== 'unknown' ? `v${runtime.version}` : 'dev'}</span>
          <span className="dot" />
          <span className="ac-mono">{runtime.os}/{runtime.arch}</span>
          {currentProvider?.available && (
            <>
              <span className="dot" />
              <span>Current model <span className="ac-mono">{currentProvider.provider} · {currentProvider.model}</span></span>
            </>
          )}
        </div>
      </header>

      <div className="ac-settings" style={{ marginTop: 36 }}>
        <nav className="ac-settings-nav" aria-label="Settings sections">
          {NAV.map((n) => (
            <button key={n.key} aria-current={active === n.key} onClick={() => setActive(n.key)}>{n.label}</button>
          ))}
        </nav>

        <div className="ac-settings-body">
          {/* ---------------- Model ---------------- */}
          {active === 'model' && (
            <Section title="Model" description="Which LLM analyzes your clips. Keys stay on this machine and are never uploaded.">
              <Form
                form={form}
                layout="vertical"
                onFinish={handleSave}
                requiredMark={false}
                initialValues={{ llm_provider: 'dashscope', model_name: 'qwen-plus', chunk_size: 5000, min_score_threshold: 0.7, max_clips_per_collection: 5 }}
              >
                <Form.Item name="llm_provider" hidden><Input /></Form.Item>
                <div className="ac-rows">
                  <Row label="Provider" hint={cfg.hint} stack>
                    <Segmented
                      size="sm"
                      ariaLabel="Provider"
                      value={selectedProvider}
                      onChange={handleProviderChange}
                      options={(Object.keys(PROVIDERS) as ProviderKey[]).map((k) => ({ value: k, label: PROVIDERS[k].short }))}
                    />
                  </Row>

                  {localCfg && (
                    <Row
                      wide
                      label="Server address"
                      hint={<>Default <span className="ac-mono">{localCfg.baseUrl}</span>; only change it if you customized the port. If not installed, download it from the <a href={localCfg.docsUrl} onClick={(e) => { e.preventDefault(); openExternalLink(localCfg.docsUrl) }} style={{ color: 'var(--ac-accent)' }}>{localCfg.app} website</a>.</>}
                    >
                      <Form.Item
                        name="local_base_url"
                        style={{ width: '100%' }}
                        rules={[{
                          validator: (_, value) => {
                            const url = normalizeBaseUrl(value)
                            if (!url || /^https?:\/\/\S+$/.test(url)) return Promise.resolve()
                            return Promise.reject(new Error('Enter an address starting with http:// or https://'))
                          },
                        }]}
                      >
                        <Input
                          placeholder={localCfg.baseUrl}
                          allowClear
                          className="ac-mono"
                          onBlur={(e) => void detectLocalModels(selectedProvider, e.target.value)}
                        />
                      </Form.Item>
                    </Row>
                  )}

                  {selectedProvider === 'dashscope' && (
                    <Row
                      label="Region"
                      hint={dashscopeRegion === 'intl'
                        ? <>Keys from the international site (alibabacloud.com) go to <span className="ac-mono">dashscope-intl.aliyuncs.com</span>.</>
                        : 'Pick this for keys from Alibaba Cloud China (aliyun.com); overseas accounts pick International.'}
                    >
                      <Segmented
                        size="sm"
                        ariaLabel="Qwen region"
                        value={dashscopeRegion}
                        onChange={setDashscopeRegion}
                        options={[{ value: 'cn', label: 'China' }, { value: 'intl', label: 'International' }]}
                      />
                    </Row>
                  )}

                  {selectedProvider === 'openai' && (
                    <Row
                      wide
                      label="API base URL"
                      hint={<>Leave empty for the official OpenAI endpoint. For compatible services use your own, e.g. <span className="ac-mono">https://api.deepseek.com/v1</span>, <span className="ac-mono">http://localhost:11434/v1</span> (Ollama).</>}
                    >
                      <Form.Item
                        name="openai_base_url"
                        style={{ width: '100%' }}
                        rules={[{
                          validator: (_, value) => {
                            const url = normalizeBaseUrl(value)
                            if (!url || /^https?:\/\/\S+$/.test(url)) return Promise.resolve()
                            return Promise.reject(new Error('Enter an address starting with http:// or https://'))
                          },
                        }]}
                      >
                        <Input placeholder="https://api.openai.com/v1" allowClear className="ac-mono" />
                      </Form.Item>
                    </Row>
                  )}

                  {!localCfg && <Row
                    wide
                    label="API Key"
                    hint={usingCustomEndpoint
                      ? 'Can be left empty for self-hosted / local services that skip key validation.'
                      : <>Get it from the <a href={keyUrl} onClick={(e) => { e.preventDefault(); openExternalLink(keyUrl) }} style={{ color: 'var(--ac-accent)' }}>{cfg.name}{selectedProvider === 'dashscope' && dashscopeRegion === 'intl' ? ' International' : ''} console</a>.</>}
                  >
                    <Form.Item
                      name={cfg.apiKeyField}
                      style={{ width: '100%' }}
                      rules={usingCustomEndpoint ? [] : [
                        { required: true, message: 'Please enter an API key' },
                        { min: 10, message: 'API key must be at least 10 characters' }
                      ]}
                    >
                      <Input.Password placeholder={cfg.placeholder} className="ac-mono" />
                    </Form.Item>
                  </Row>}

                  <Row
                    wide
                    label="Model"
                    hint={localCfg
                      ? (localModels.loading
                          ? 'Detecting local service…'
                          : localModels.reachable
                            ? <>Connected, found {localModels.models.length} models. <a onClick={() => void detectLocalModels(selectedProvider, form.getFieldValue('local_base_url'))} style={{ color: 'var(--ac-accent)', cursor: 'pointer' }}>Refresh</a></>
                            : localModels.reachable === false
                              ? <>{localCfg.app} is unreachable. Start it first{localCfg.defaultModel ? <> and run <span className="ac-mono">ollama pull {localCfg.defaultModel}</span></> : ''}, then <a onClick={() => void detectLocalModels(selectedProvider, form.getFieldValue('local_base_url'))} style={{ color: 'var(--ac-accent)', cursor: 'pointer' }}>retry detection</a>. You can also type a model name directly.</>
                              : 'Choose from models loaded in the local service.')
                      : usingCustomEndpoint
                        ? 'Enter the exact model name served there (e.g. glm-4-flash, deepseek-chat, qwen2.5:7b), press Enter to confirm.'
                        : 'You can type a model name directly, press Enter to confirm.'}
                  >
                    <Form.Item name="model_name" style={{ width: '100%' }} rules={[{ required: true, message: 'Please enter or select a model' }]}>
                      <Select
                        placeholder={localCfg ? (localCfg.defaultModel || 'Select or type a model name') : 'qwen-plus'}
                        showSearch
                        allowClear
                        mode="tags"
                        maxCount={1}
                        loading={localCfg ? localModels.loading : false}
                        className="ac-mono"
                        options={(localCfg
                          ? localModels.models.map((m) => ({ value: m, label: m }))
                          : MODEL_GROUPS.map((g) => ({ label: g.label, options: g.models.map((m) => ({ value: m, label: m })) }))) as any}
                      />
                    </Form.Item>
                  </Row>

                  <Row label="Connection test" hint={localCfg ? 'Test the local service and model before saving.' : 'Test the key and model before saving.'}>
                    <Btn size="sm" loading={testing} onClick={handleTest}>Test connection</Btn>
                  </Row>
                </div>

                <div className="ac-eyebrow" style={{ marginTop: 40, marginBottom: 12 }}>Clipping parameters</div>
                <div className="ac-rows">
                  <Row label="Text chunk size" hint="Subtitle length sent to the model per call. Larger is more coherent but slower; 5000 recommended.">
                    <Form.Item name="chunk_size">
                      <input className="ac-input ac-input--mono" type="number" min={1000} step={500} style={{ width: 120, textAlign: 'right' }} />
                    </Form.Item>
                    <span className="ac-unit">chars</span>
                  </Row>
                  <Row label="Minimum score" hint="Clips below this score are dropped. Lower it if you get zero clips.">
                    <Form.Item name="min_score_threshold">
                      <input className="ac-input ac-input--mono" type="number" min={0} max={1} step={0.05} style={{ width: 120, textAlign: 'right' }} />
                    </Form.Item>
                    <span className="ac-unit" />
                  </Row>
                  <Row label="Max clips per collection" hint="How many clips one topic strings together in AI-recommended collections.">
                    <Form.Item name="max_clips_per_collection">
                      <input className="ac-input ac-input--mono" type="number" min={1} max={20} style={{ width: 120, textAlign: 'right' }} />
                    </Form.Item>
                    <span className="ac-unit">clips</span>
                  </Row>
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: 12, marginTop: 28 }}>
                  {currentProvider?.available && (
                    <StatusDot tone="ok" label={<>Configured <span className="ac-mono">{currentProvider.display_name} · {currentProvider.model}</span></>} />
                  )}
                  <Btn variant="cta" loading={loading} onClick={() => form.submit()}>Save</Btn>
                </div>
              </Form>
            </Section>
          )}

          {/* ---------------- Transcription ---------------- */}
          {active === 'speech' && (
            <Section
              title="Transcription"
              description="When a video has no subtitles, generate them locally with Whisper before analysis. Videos with built-in subtitles (e.g. Bilibili) don't need this; installing and which model is up to you."
            >
              <SpeechRecognitionConfig />
            </Section>
          )}

          {/* ---------------- App ---------------- */}
          {active === 'app' && (
            <AppSection analyticsOn={analyticsOn} onAnalyticsChange={(on) => { setAnalyticsEnabled(on); setAnalyticsOn(on) }} />
          )}

          {/* ---------------- Feedback ---------------- */}
          {active === 'feedback' && (
            <Section title="Feedback" description="Tell us what's wrong or what you want. Runtime info is attached automatically; no video content or API keys.">
              <div className="ac-rows">
                <Row label="Send feedback" hint="One sentence in the app is enough; we review weekly.">
                  <Btn variant="cta" size="sm" style={{ height: 32, fontSize: 13, padding: '0 16px' }} onClick={() => setFeedbackOpen(true)}>
                    <Icon.Chat size={13} /> Write feedback
                  </Btn>
                </Row>
                <Row label="Feedback form" hint="Use when you prefer not to write in-app, or want to attach screenshots / logs.">
                  <Btn size="sm" onClick={() => openExternalLink(FEEDBACK_FORM_URL)}>Open form <Icon.External size={12} /></Btn>
                </Row>
                <Row label="GitHub" hint="Developers can file an issue (templated) or discuss in Discussions.">
                  <Btn size="sm" onClick={() => openExternalLink(FEEDBACK_ISSUES_URL)}>New issue <Icon.External size={12} /></Btn>
                </Row>
                <Row label="Status & known issues" hint="Release cadence, known bugs and workarounds live in this pinned issue.">
                  <Btn variant="text" size="sm" onClick={() => openExternalLink('https://github.com/nd7hdyt/YtClipper/issues/96')}>#96 <Icon.External size={12} /></Btn>
                </Row>
              </div>
            </Section>
          )}
        </div>
      </div>

      <FeedbackDialog open={feedbackOpen} onClose={() => setFeedbackOpen(false)} context={{ source: 'settings' }} />
    </div>
  )
}

/* ---------------- App ---------------- */
const AppSection: React.FC<{ analyticsOn: boolean; onAnalyticsChange: (on: boolean) => void }> = ({ analyticsOn, onAnalyticsChange }) => {
  const { theme, setTheme } = useTheme()
  const [autostart, setAutostart] = useState(false)
  const [busy, setBusy] = useState(false)
  const [desktop, setDesktop] = useState(false)

  useEffect(() => {
    (async () => {
      try {
        const isDesktop = await isDesktopMode()
        setDesktop(isDesktop)
        if (isDesktop) {
          const { invoke } = await import('@tauri-apps/api/core')
          setAutostart(Boolean(await invoke('is_autostart_enabled')))
        }
      } catch (err) {
        console.error('Failed to check autostart status:', err)
      }
    })()
  }, [])

  const toggleAutostart = async (enabled: boolean) => {
    if (!desktop) { message.error('Available in the desktop app only'); return }
    setBusy(true)
    try {
      const { invoke } = await import('@tauri-apps/api/core')
      await invoke(enabled ? 'enable_autostart' : 'disable_autostart')
      setAutostart(enabled)
    } catch (err) {
      console.error('Failed to toggle autostart:', err)
      message.error(`Operation failed: ${err}`)
    } finally {
      setBusy(false)
    }
  }

  return (
    <Section title="App" description="Appearance, startup & privacy.">
      <div className="ac-rows">
        <Row label="Appearance" hint="Follows the system on first launch.">
          <Segmented size="sm" ariaLabel="Appearance" value={theme} onChange={setTheme} options={[{ value: 'light', label: 'Light' }, { value: 'dark', label: 'Dark' }]} />
        </Row>
        <Row label="Launch at login" hint="Starts with the system; open from the tray. Desktop app only.">
          <Switch checked={autostart} onChange={toggleAutostart} loading={busy} disabled={!desktop} />
        </Row>
        <Row label="Anonymous usage stats" hint="Only anonymous events (feature use, export success / failure). No video content, subtitles, or API keys. In-app feedback falls back to the form when off.">
          <Switch checked={analyticsOn} onChange={onAnalyticsChange} />
        </Row>
        <Row label="Bilibili accounts" hint="Multi-account management and one-click publishing, in development.">
          <span className="ac-hint" style={{ margin: 0 }}>Coming soon</span>
        </Row>
      </div>
    </Section>
  )
}

export default SettingsPage
