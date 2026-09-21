/**
 * In-app feedback (PostHog Surveys).
 *
 * Goal: users can report issues/requests without leaving the app or signing up for GitHub,
 * and automatically include triage context (version / OS / arch / LLM provider & model / failed stage & error).
 *
 * Implementation notes:
 * - Feedback enters PostHog as `feedback_submitted` (always sent, even without a Survey).
 * - If a Survey named FEEDBACK_SURVEY_NAME (or env-specified ID) exists in PostHog (API-type / no UI),
 *   also send `survey shown` / `survey sent` / `survey dismissed` per PostHog convention,
 *   so results appear in PostHog → Surveys and are readable in the weekly report.
 * - Version / OS / arch are auto-carried via super properties registered in lifecycle.ts; also written explicitly here
 *   to avoid losing context when Surveys panel only shows `$survey_response*`.
 * - When analytics is disabled, nothing is sent to PostHog; fall back to the Feishu form (FEEDBACK_FORM_URL).
 */
import { posthog, isAnalyticsEnabled } from './posthog'
import { settingsApi } from '../services/api'

export const FEEDBACK_SURVEY_NAME = 'AutoClip In-App Feedback'
export const FEEDBACK_FORM_URL = 'https://my.feishu.cn/share/base/shrcn8hKUG2icIJLpNry6uWVNJe'
export const FEEDBACK_ISSUES_URL = 'https://github.com/nd7hdyt/YtClipper/issues/new/choose'

const SURVEY_ID_ENV = import.meta.env.VITE_PUBLIC_POSTHOG_FEEDBACK_SURVEY_ID as string | undefined

export type FeedbackCategory = 'bug' | 'idea' | 'other'
export type FeedbackSource = 'settings' | 'failure' | 'detail'

export interface FeedbackContext {
  source: FeedbackSource
  /** Carried in failed state */
  stage?: string
  error_message?: string
  project_id?: string
  /** Settings page / failed state will try to fill */
  llm_provider?: string
  llm_model?: string
  llm_base_url?: string
}

interface SurveyLike {
  id: string
  name: string
  type?: string
  questions?: Array<{ id?: string; type?: string; question?: string }>
}

let cachedSurvey: SurveyLike | null | undefined

/** Find the Survey for feedback; return null if not found (doesn't affect feedback_submitted). */
export function resolveFeedbackSurvey(): Promise<SurveyLike | null> {
  if (cachedSurvey !== undefined) return Promise.resolve(cachedSurvey)
  return new Promise((resolve) => {
    if (typeof posthog?.getSurveys !== 'function' || !isAnalyticsEnabled()) {
      cachedSurvey = null
      return resolve(null)
    }
    try {
      posthog.getSurveys((surveys: unknown) => {
        const list = (Array.isArray(surveys) ? surveys : []) as SurveyLike[]
        const found =
          list.find((s) => SURVEY_ID_ENV && s.id === SURVEY_ID_ENV) ||
          list.find((s) => s.name === FEEDBACK_SURVEY_NAME) ||
          null
        cachedSurvey = found
        resolve(found)
      }, false)
    } catch {
      cachedSurvey = null
      resolve(null)
    }
  })
}

/** Read current LLM provider / model into feedback context; silently ignore if backend unreachable. */
export async function collectLlmContext(): Promise<Pick<FeedbackContext, 'llm_provider' | 'llm_model' | 'llm_base_url'>> {
  try {
    const p = await settingsApi.getCurrentProvider()
    return {
      llm_provider: p?.provider,
      llm_model: p?.model,
      llm_base_url: p?.base_url || undefined,
    }
  } catch {
    return {}
  }
}

export function trackFeedbackOpened(ctx: FeedbackContext, survey: SurveyLike | null): void {
  if (typeof posthog?.capture !== 'function') return
  posthog.capture('feedback_opened', { source: ctx.source, stage: ctx.stage })
  if (survey) posthog.capture('survey shown', { $survey_id: survey.id, $survey_name: survey.name })
}

export function trackFeedbackDismissed(ctx: FeedbackContext, survey: SurveyLike | null): void {
  if (typeof posthog?.capture !== 'function') return
  posthog.capture('feedback_dismissed', { source: ctx.source })
  if (survey) posthog.capture('survey dismissed', { $survey_id: survey.id, $survey_name: survey.name })
}

export interface FeedbackPayload {
  category: FeedbackCategory
  text: string
  contact?: string
  context: FeedbackContext
}

/**
 * Submit feedback. Returns true if sent via PostHog; false if analytics disabled / not initialized,
 * caller should guide user to the Feishu form.
 */
export async function submitFeedback(payload: FeedbackPayload): Promise<boolean> {
  if (typeof posthog?.capture !== 'function' || !isAnalyticsEnabled()) return false

  const survey = await resolveFeedbackSurvey()
  const props: Record<string, unknown> = {
    category: payload.category,
    text: payload.text,
    contact: payload.contact || undefined,
    ...payload.context,
  }
  posthog.capture('feedback_submitted', props)

  if (survey) {
    const qs = survey.questions || []
    const responses: Record<string, unknown> = {
      $survey_id: survey.id,
      $survey_name: survey.name,
      $survey_questions: qs.map((q) => ({ id: q.id, question: q.question })),
      // Q1: free text
      $survey_response: payload.text,
      ...props,
    }
    // Compat question-id keys: Q1 = text, subsequent single_choice = category
    qs.forEach((q, i) => {
      const key = q.id ? `$survey_response_${q.id}` : `$survey_response_${i}`
      if (i === 0) responses[key] = payload.text
      else if (q.type === 'single_choice' || q.type === 'multiple_choice') responses[key] = payload.category
      else if (/EN|contact|email/i.test(q.question || '')) responses[key] = payload.contact || ''
    })
    posthog.capture('survey sent', responses)
  }
  return true
}
