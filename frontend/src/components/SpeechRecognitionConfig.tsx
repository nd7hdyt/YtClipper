import React, { useCallback, useEffect, useRef, useState } from 'react'
import { Popconfirm, message } from 'antd'
import { speechApi, WhisperRuntimeStatus, WhisperModel } from '../services/api'
import { Btn, ProgressLine, Row, StatusDot } from '../ui'

interface SpeechRecognitionConfigProps {
  config?: Record<string, unknown>
  onConfigChange?: (config: Record<string, unknown>) => void
}

// Whisper EN + ModelEN — Calm Premium EN（EN DESIGN.md）
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
      // EN，ENRetry
    } finally {
      setLoading(false)
    }
  }, [])

  // installENModeldownloadEN，EN
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
      message.info(r.message || 'ENinstall')
      setRuntime((p) => (p ? { ...p, status: 'installing', progress: 5 } : p))
      refresh()
    } catch (e: any) {
      message.error(e?.response?.data?.detail || 'installFailed')
    }
  }

  const handleUninstall = async () => {
    try {
      const r = await speechApi.uninstallRuntime()
      message.success(r.message || 'ENuninstall')
      refresh()
    } catch {
      message.error('uninstallFailed')
    }
  }

  const handleDownload = async (model: string) => {
    try {
      await speechApi.downloadModel(model)
      message.info(`ENdownload ${model}`)
      setModels((prev) => prev.map((m) => (m.name === model ? { ...m, status: 'downloading' } : m)))
      refresh()
    } catch (e: any) {
      message.error(e?.response?.data?.detail || 'Download failed')
    }
  }

  const handleDelete = async (model: string) => {
    try {
      await speechApi.deleteModel(model)
      message.success(`ENDelete ${model}`)
      refresh()
    } catch {
      message.error('Delete failed')
    }
  }

  if (loading) return <div className="ac-hint">EN Whisper Status…</div>

  const installed = runtime?.status === 'installed'
  const installing = runtime?.status === 'installing'
  const supported = runtime?.platform_supported !== false

  return (
    <>
      <div className="ac-rows">
        <Row
          top
          label="Whisper EN"
          hint={
            !supported ? 'EN。'
              : installed ? `faster-whisper Installed${runtime?.packages?.length ? `（${runtime.packages.join(', ')}）` : ''}。`
              : installing ? (runtime?.message || 'ENinstall…')
              : runtime?.status === 'error' ? `installEN：${runtime?.message || ''}`
              : 'ENinstall，EN 200–400 MB（EN PyTorch）。ENModeldownloadEN。'
          }
        >
          {installed && (
            <>
              <StatusDot tone="ok" label="Installed" />
              <Popconfirm title="uninstall Whisper EN？ENdownloadENModelENDelete。" onConfirm={handleUninstall} okText="uninstall" cancelText="Cancel">
                <Btn variant="danger" size="sm">uninstall</Btn>
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
            <Btn size="sm" onClick={handleInstall} disabled={!supported}>Retryinstall</Btn>
          )}
        </Row>
      </div>

      {installing && runtime?.log_tail && (
        <pre className="ac-input ac-input--mono" style={{ height: 'auto', maxHeight: 120, overflow: 'auto', padding: '8px 12px', margin: '12px 0 0', color: 'var(--ac-sub)', background: 'var(--ac-line-2)', fontSize: 11, whiteSpace: 'pre-wrap' }}>
          {runtime.log_tail}
        </pre>
      )}

      <div className="ac-eyebrow" style={{ marginTop: 40, marginBottom: 12 }}>Model</div>
      {!installed ? (
        <div className="ac-hint">ENinstallEN，ENdownloadModel。</div>
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
                    {downloaded && <StatusDot tone="ok" label="ENdownload" />}
                  </span>
                }
                hint={
                  <>
                    {m.description} · EN{m.accuracy} · EN{m.speed}
                    {m.status === 'error' && m.errorMessage && <span style={{ color: 'var(--ac-error)' }}> · {m.errorMessage}</span>}
                  </>
                }
              >
                {downloaded ? (
                  <Popconfirm title={`DeleteModel ${m.name}？`} onConfirm={() => handleDelete(m.name)} okText="Delete" cancelText="Cancel">
                    <Btn variant="danger" size="sm">Delete</Btn>
                  </Popconfirm>
                ) : downloading ? (
                  <div style={{ width: 160 }}>
                    <ProgressLine percent={m.downloadProgress ?? 0} />
                    <div className="ac-hint" style={{ textAlign: 'right', fontFamily: 'var(--ac-font-mono)' }}>
                      {m.downloadProgress != null ? `${Math.round(m.downloadProgress)}%` : 'downloadEN'}
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
