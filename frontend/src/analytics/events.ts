/**
 * translated（translated ROADMAP.md Phase 0：import / translated / failed / settings key）。
 *
 * translatedoneinthistranslatedandtranslated，translated。
 * translated capture translated trackEvent，translated / translated no-op。
 */
import { posthog } from './posthog'

export const AnalyticsEvent = {
  /** importtranslated（Upload/Selectselectvideotranslatedone project） */
  VideoImported: 'video_imported',
  /** translated：succeededtranslatedclip */
  ClipsExported: 'clips_exported',
  /** translatedfailed（import/translated/clip/exporttranslatedonetranslated） */
  ProcessingFailed: 'processing_failed',
  /** settings/update LLM API key */
  ApiKeyConfigured: 'api_key_configured',
} as const

export type AnalyticsEventName =
  (typeof AnalyticsEvent)[keyof typeof AnalyticsEvent]

/** translateduseAnalyticstranslated。posthog translatedortranslated opt-out translated no-op（translatedprocess）。 */
function trackEvent(
  name: AnalyticsEventName,
  properties?: Record<string, unknown>,
): void {
  // posthog.capture intranslated init translated；translated
  if (typeof posthog?.capture !== 'function') return
  posthog.capture(name, properties)
}

export function trackVideoImported(props?: {
  source?: 'upload' | 'url' | 'local'
  fileType?: string
  durationSec?: number
  sizeBytes?: number
}): void {
  trackEvent(AnalyticsEvent.VideoImported, props)
}

export function trackClipsExported(props?: {
  clipCount?: number
  durationSec?: number
  withSubtitles?: boolean
  exportType?: 'clip' | 'collection' | 'project'
}): void {
  trackEvent(AnalyticsEvent.ClipsExported, props)
}

export function trackProcessingFailed(props: {
  stage: 'import' | 'transcribe' | 'analyze' | 'clip' | 'export' | 'other'
  message?: string
  code?: string | number
}): void {
  trackEvent(AnalyticsEvent.ProcessingFailed, props)
}

export function trackApiKeyConfigured(props: {
  provider: string
  /** Do nottranslated key translated，OnlytranslatedIstranslated */
  hasKey: boolean
}): void {
  trackEvent(AnalyticsEvent.ApiKeyConfigured, props)
}
