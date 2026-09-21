import React, { useEffect, useMemo, useState } from 'react'
import { message } from 'antd'
import { Btn, Dialog, Icon, Segmented } from '../ui'
import {
  FEEDBACK_FORM_URL,
  FEEDBACK_ISSUES_URL,
  FeedbackCategory,
  FeedbackContext,
  collectLlmContext,
  resolveFeedbackSurvey,
  submitFeedback,
  trackFeedbackDismissed,
  trackFeedbackOpened,
} from '../analytics/feedback'
import { isAnalyticsEnabled } from '../analytics/posthog'
import { getRuntimeInfo } from '../analytics/lifecycle'
import { openExternalLink as openExternal } from '../utils/externalLinks'

interface FeedbackDialogProps {
  open: boolean
  onClose: () => void
  context: FeedbackContext
}

/**
 * In-app feedback - shared by Settings "Feedback" and the project failure state.
 * Version / OS / arch / LLM provider & model / failure stage & error are attached automatically; the user only writes one sentence.
 */
const FeedbackDialog: React.FC<FeedbackDialogProps> = ({ open, onClose, context }) => {
  const [category, setCategory] = useState<FeedbackCategory>(context.source === 'failure' ? 'bug' : 'idea')
  const [text, setText] = useState('')
  const [contact, setContact] = useState('')
  const [sending, setSending] = useState(false)
  const [llm, setLlm] = useState<Pick<FeedbackContext, 'llm_provider' | 'llm_model' | 'llm_base_url'>>({})
  const [surveyReady, setSurveyReady] = useState<boolean | null>(null)
  const runtime = useMemo(() => getRuntimeInfo(), [])
  const analyticsOn = isAnalyticsEnabled()

  const fullContext: FeedbackContext = useMemo(() => ({ ...llm, ...context }), [llm, context])

  useEffect(() => {
    if (!open) return
    setText('')
    setContact('')
    setCategory(context.source === 'failure' ? 'bug' : 'idea')
    collectLlmContext().then(setLlm)
    resolveFeedbackSurvey().then((s) => {
      setSurveyReady(!!s)
      trackFeedbackOpened(context, s)
    })
  }, [open, context])

  const handleClose = () => {
    resolveFeedbackSurvey().then((s) => trackFeedbackDismissed(context, s))
    onClose()
  }

  const handleSend = async () => {
    if (text.trim().length < 4) {
      message.warning('Please add a few more words so we can locate the issue')
      return
    }
    setSending(true)
    try {
      const ok = await submitFeedback({ category, text: text.trim(), contact: contact.trim() || undefined, context: fullContext })
      if (ok) {
        message.success('Received, thanks for the feedback')
        onClose()
      } else {
        message.info('Anonymous stats are off, please use the form instead')
        void openExternal(FEEDBACK_FORM_URL)
      }
    } finally {
      setSending(false)
    }
  }

  const ctxChips: string[] = [
    runtime.version !== 'unknown' ? `v${runtime.version}` : 'dev',
    `${runtime.os}/${runtime.arch}`,
  ]
  if (fullContext.llm_provider) ctxChips.push(`${fullContext.llm_provider}${fullContext.llm_model ? ` · ${fullContext.llm_model}` : ''}`)
  if (fullContext.stage) ctxChips.push(`stage: ${fullContext.stage}`)

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      title={context.source === 'failure' ? 'No output this time? Tell us what went wrong' : 'Feedback'}
      description={
        context.source === 'failure'
          ? 'Error details and environment are attached automatically; just add what happened.'
          : 'One sentence is enough. Environment is attached automatically; no video content or API keys.'
      }
      footer={
        <>
          <div style={{ display: 'flex', gap: 4 }}>
            <Btn variant="text" size="sm" onClick={() => openExternal(FEEDBACK_FORM_URL)}>Form <Icon.External size={12} /></Btn>
            <Btn variant="text" size="sm" onClick={() => openExternal(FEEDBACK_ISSUES_URL)}>GitHub <Icon.External size={12} /></Btn>
          </div>
          <div className="right">
            <Btn size="sm" onClick={handleClose}>Cancel</Btn>
            <Btn variant="cta" size="sm" style={{ height: 32, fontSize: 13, padding: '0 16px' }} loading={sending} onClick={handleSend}>
              Send
            </Btn>
          </div>
        </>
      }
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
        <Segmented
          size="sm"
          ariaLabel="Feedback type"
          value={category}
          onChange={setCategory}
          options={[
            { value: 'bug', label: 'Bug' },
            { value: 'idea', label: 'Feature request' },
            { value: 'other', label: 'Other' },
          ]}
        />
        <textarea
          className="ac-input ac-textarea"
          autoFocus
          placeholder={
            category === 'bug'
              ? 'What happened? What did you do, what did you expect, what did you see?'
              : category === 'idea'
                ? 'What do you want AutoClip to do for you?'
                : 'Anything you want to say.'
          }
          value={text}
          onChange={(e) => setText(e.target.value)}
          maxLength={2000}
        />
        {fullContext.error_message && (
          <div className="ac-input ac-input--mono" style={{ height: 'auto', padding: '8px 12px', color: 'var(--ac-sub)', background: 'var(--ac-line-2)', whiteSpace: 'pre-wrap', wordBreak: 'break-all', maxHeight: 88, overflow: 'auto', fontSize: 11.5 }}>
            {fullContext.error_message}
          </div>
        )}
        <input
          className="ac-input"
          placeholder="Contact (optional, email / Lark / WeChat)"
          value={contact}
          onChange={(e) => setContact(e.target.value)}
        />
        <div className="ac-context" title="Context sent with feedback">
          {ctxChips.map((c) => <span key={c}>{c}</span>)}
          {!analyticsOn && <span style={{ color: 'var(--ac-warn)' }}>Anonymous stats off · will use form instead</span>}
          {analyticsOn && surveyReady === false && <span>· direct report</span>}
        </div>
      </div>
    </Dialog>
  )
}

export default FeedbackDialog
