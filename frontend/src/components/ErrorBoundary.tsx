/**
 * React error boundary
 * Catches JS errors in children, logs them, and shows a fallback UI (per DESIGN.md: monochrome, no gradients)
 */

import { Component, ErrorInfo, ReactNode } from 'react'
import { errorHandler } from '../utils/errorHandler'
import { isDomDisplacementError, isPageTranslated } from '../utils/domTranslationGuard'
import { Btn } from '../ui'

interface Props {
  children: ReactNode
  fallback?: ReactNode
  onError?: (error: Error, errorInfo: ErrorInfo) => void
  showDetails?: boolean
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
  errorId: string
}

const ISSUE_URL = 'https://github.com/nd7hdyt/YtClipper/issues/new/choose'

const preStyle: React.CSSProperties = {
  margin: 0,
  padding: 12,
  fontFamily: 'var(--ac-font-mono)',
  fontSize: 11.5,
  lineHeight: 1.5,
  color: 'var(--ac-sub)',
  background: 'var(--ac-line-2)',
  border: '1px solid var(--ac-line)',
  borderRadius: 10,
  overflow: 'auto',
  maxHeight: 220,
  whiteSpace: 'pre-wrap',
  wordBreak: 'break-word',
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
      errorId: ''
    }
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    // Show the fallback UI on the next render
    return {
      hasError: true,
      error,
      errorId: `error_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({ errorInfo })
    errorHandler.handleError(error, 'ReactErrorBoundary')
    if (this.props.onError) {
      this.props.onError(error, errorInfo)
    }
    console.group('React Error Boundary')
    console.error('Error:', error)
    console.error('Error Info:', errorInfo)
    console.error('Error ID:', this.state.errorId)
    console.groupEnd()
  }

  handleReload = () => {
    this.setState({ hasError: false, error: null, errorInfo: null, errorId: '' })
    window.location.reload()
  }

  handleGoHome = () => {
    this.setState({ hasError: false, error: null, errorInfo: null, errorId: '' })
    // HashRouter: home is #/; assigning href would keep the hash and reload in place
    window.location.hash = '#/'
    window.location.reload()
  }

  handleReportError = () => {
    const { error, errorInfo, errorId } = this.state
    if (!error) return
    const errorReport = {
      id: errorId,
      message: error.message,
      stack: error.stack,
      componentStack: errorInfo?.componentStack,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href,
      translated: isPageTranslated(),
    }
    console.log('Error Report:', errorReport)
    window.open(ISSUE_URL, '_blank', 'noopener')
  }

  render() {
    if (!this.state.hasError) {
      return this.props.children
    }
    if (this.props.fallback) {
      return this.props.fallback
    }

    const { error, errorInfo, errorId } = this.state
    // Browser "Translate this page" moves DOM nodes and breaks React updates (#100); show a self-serve hint
    const translationSuspected = isDomDisplacementError(error) || isPageTranslated()

    return (
      <div
        translate="no"
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: 24,
          background: 'var(--ac-bg)',
          color: 'var(--ac-ink)',
          fontFamily: 'var(--ac-font-sans)',
        }}
      >
        <div
          style={{
            width: 'min(560px, 100%)',
            background: 'var(--ac-card)',
            border: '1px solid var(--ac-line)',
            borderRadius: 16,
            padding: '32px 32px 28px',
          }}
        >
          <div className="ac-eyebrow">Page error</div>
          <h1 style={{ margin: '10px 0 0', fontSize: 20, fontWeight: 600, lineHeight: 1.3, letterSpacing: '-0.01em' }}>
            {translationSuspected ? 'Browser translation broke rendering' : 'This page hit an unexpected error'}
          </h1>
          <p style={{ margin: '8px 0 0', fontSize: 13.5, color: 'var(--ac-sub)', lineHeight: 1.6, maxWidth: '60ch' }}>
            {translationSuspected ? (
              <>
                This page is being translated by the browser (Chrome / Edge “Translate this page”). Translation rewrites the page structure and can crash the UI when switching options.
                Turn translation off in the address bar, show the original, then reload.
                <span style={{ display: 'block', marginTop: 6 }}>
                  Page translation (Chrome / Edge “Translate this page”) rewrites the DOM and breaks the UI.
                  Please turn translation off, show the original page, then reload.
                </span>
              </>
            ) : (
              'The issue is logged locally. Try reloading; if it persists, file a GitHub issue with the error details below.'
            )}
          </p>

          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 24, flexWrap: 'wrap' }}>
            <Btn variant="cta" onClick={this.handleReload}>Reload page</Btn>
            <Btn onClick={this.handleGoHome}>Go home</Btn>
            <Btn variant="text" onClick={this.handleReportError}>Report issue</Btn>
          </div>

          {error && (
            <details style={{ marginTop: 24 }} open={!!this.props.showDetails}>
              <summary style={{ cursor: 'pointer', fontSize: 12.5, color: 'var(--ac-muted)', userSelect: 'none' }}>
                Error details <span className="ac-mono" style={{ fontFamily: 'var(--ac-font-mono)' }}>{errorId}</span>
              </summary>
              <div style={{ display: 'grid', gap: 10, marginTop: 12 }}>
                <pre style={preStyle}>{error.message}</pre>
                {this.props.showDetails && error.stack && <pre style={preStyle}>{error.stack}</pre>}
                {this.props.showDetails && errorInfo?.componentStack && <pre style={preStyle}>{errorInfo.componentStack}</pre>}
              </div>
            </details>
          )}
        </div>
      </div>
    )
  }
}

export default ErrorBoundary
