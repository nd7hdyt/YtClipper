import React, { useCallback, useEffect, useRef, useState } from 'react'
import { Popconfirm, message } from 'antd'
import { speechApi, WhisperRuntimeStatus, WhisperModel } from '../services/api'
import { Btn, ProgressLine, Row, StatusDot } from '../ui'

interface SpeechRecognitionConfigProps {
  config?: Record<string, unknown>
  onConfigChange?: (config: Record<string, unknown>) => void
}

// Whisper Runtime + modeltranslated — Calm Premium translated（translated DESIGN.md）
const SpeechRecognitionConfig: React.FC<SpeechRecognitionConfigProps> = () => {
  const [runtime, setRuntime] = useState<WhisperRuntimeStatus | null>(null)
  const [models, setModels] = useState<WhisperModel[]>([])
  const [loading, setLoading] = useState(true)
  const timer = useRef<number | null>(null)

  const refresh = useCallback(async () => {
    try {
      const [rt, ms] = await Promise.all([speechApi.getRuntimeStatus(), speechApi.getModels()])
      setRuntime(rt)
      setModels(Array.isArray(ms) ? ms : [])
    } catch {
      // backendcantranslated，translated
    } finally {
      setLoading(false)
    }
  }, [])

  // installtranslatedortranslatedmodeldownloadtranslated，translated
  const needsFastPoll = (rt: WhisperRuntimeStatus | null, ms: WhisperModel[]) =>
    rt?.status === 'installing' || ms.some((m) => m.status === 'downloading')

  useEffect(() => {
    refresh()
    return () => { if (timer.current) window.clearInterval(timer.current) }
  }, [refresh])

  useEffect(() => {
    if (timer.current) window.clearInterval(timer.current)
    timer.current = window.setInterval(refresh, needsFastPoll(runtime, models) ? 2000 : 15000)
    return () => { if (timer.current) window.clearInterval(timer.current) }
  }, [runtime, models, refresh])

  const handleInstall = async () => {
    try {
      const r = await speechApi.installRuntime()
      message.info(r.message || 'translatedinstall')
      setRuntime((p) => (p ? { ...p, status: 'installing', progress: 5 } : p))
      refresh()
    } catch (e: any) {
      message.error(e?.response?.data?.detail || 'installfailed')
    }
  }

  const handleUninstall = async () => {
    try {
      const r = await speechApi.uninstallRuntime()
      message.success(r.message || 'translated')
      refresh()
    } catch {
      message.error('translatedfailed')
    }
  }

  const handleDownload = async (model: string) => {
    try {
      await speechApi.downloadModel(model)
      message.info(`translateddownload ${model}`)
      setModels((prev) => prev.map((m) => (m.name === model ? { ...m, status: 'downloading' } : m)))
      refresh()
    } catch (e: any) {
      message.error(e?.response?.data?.detail || 'downloadfailed')
    }
  }

  const handleDelete = async (model: string) => {
    try {
      await speechApi.deleteModel(model)
      message.success(`translateddelete ${model}`)
      refresh()
    } catch {
      message.error('deletefailed')
    }
  }

  if (loading) return <div className="ac-hint">translated Whisper status…</div>

  const installed = runtime?.status === 'installed'
  const installing = runtime?.status === 'installing'
  const supported = runtime?.platform_supported !== false

  return (
    <>
      <div className="ac-rows">
        <Row
          top
          label="Whisper Runtime"
          hint={
            !supported ? 'translatedsupportlocaltranslated。'
              : installed ? `faster-whisper translatedinstall${runtime?.packages?.length ? `（${runtime.packages.join(', ')}）` : ''}。`
              : installing ? (runtime?.message || 'translatedininstall…')
              : runtime?.status === 'error' ? `installtranslated：${runtime?.message || ''}`
              : 'bytranslatedinstall，translated 200–400 MB（translatedinclude PyTorch）。translatedSelectone modeldownloadtranslatedcan。'
          }
        >
          {installed && (
            <>
              <StatusDot tone="ok" label="translatedinstall" />
              <Popconfirm title="translated Whisper Runtime？translateddownload'smodeltranslateddelete。" onConfirm={handleUninstall} okText="translated" cancelText="cancel">
                <Btn variant="danger" size="sm">translated</Btn>
              </Popconfirm>
            </>
          )}
          {installing && (
            <div style={{ width: 220 }}>
              <ProgressLine percent={runtime?.progress ?? 5} />
              <div className="ac-hint" style={{ textAlign: 'right', fontFamily: 'var(--ac-font-mono)' }}>{Math.round(runtime?.progress ?? 5)}%</div>
            </div>
          )}
          {runtime?.status === 'not_installed' && (
            <Btn variant="cta" size="sm" style={{ height: 32, fontSize: 13, padding: '0 16px' }} onClick={handleInstall} disabled={!supported}>install</Btn>
          )}
          {runtime?.status === 'error' && (
            <Btn size="sm" onClick={handleInstall} disabled={!supported}>translatedinstall</Btn>
          )}
        </Row>
      </div>

      {installing && runtime?.log_tail && (
        <pre className="ac-input ac-input--mono" style={{ height: 'auto', maxHeight: 120, overflow: 'auto', padding: '8px 12px', margin: '12px 0 0', color: 'var(--ac-sub)', background: 'var(--ac-line-2)', fontSize: 11, whiteSpace: 'pre-wrap' }}>
          {runtime.log_tail}
        </pre>
      )}

      <div className="ac-eyebrow" style={{ marginTop: 40, marginBottom: 12 }}>model</div>
      {!installed ? (
        <div className="ac-hint">translatedinstallRuntime，translatedinthistranslateddownloadmodel。</div>
      ) : (
        <div className="ac-rows">
          {models.map((m) => {
            const downloaded = m.status === 'downloaded'
            const downloading = m.status === 'downloading'
            return (
              <Row
                key={m.name}
                label={
                  <span style={{ display: 'inline-flex', alignItems: 'baseline', gap: 10 }}>
                    <span className="ac-mono">{m.name}</span>
                    <span className="ac-mono" style={{ fontSize: 12, color: 'var(--ac-muted)', fontWeight: 400 }}>{m.size}</span>
                    {downloaded && <StatusDot tone="ok" label="translateddownload" />}
                  </span>
                }
                hint={
                  <>
                    {m.description} · translated{m.accuracy} · translated{m.speed}
                    {m.status === 'error' && m.errorMessage && <span style={{ color: 'var(--ac-error)' }}> · {m.errorMessage}</span>}
                  </>
                }
              >
                {downloaded ? (
                  <Popconfirm title={`deletemodel ${m.name}？`} onConfirm={() => handleDelete(m.name)} okText="delete" cancelText="cancel">
                    <Btn variant="danger" size="sm">delete</Btn>
                  </Popconfirm>
                ) : downloading ? (
                  <div style={{ width: 160 }}>
                    <ProgressLine percent={m.downloadProgress ?? 0} />
                    <div className="ac-hint" style={{ textAlign: 'right', fontFamily: 'var(--ac-font-mono)' }}>
                      {m.downloadProgress != null ? `${Math.round(m.downloadProgress)}%` : 'downloadtranslated'}
                    </div>
                  </div>
                ) : (
                  <Btn size="sm" onClick={() => handleDownload(m.name)}>download</Btn>
                )}
              </Row>
            )
          })}
        </div>
      )}
    </>
  )
}

export default SpeechRecognitionConfig
