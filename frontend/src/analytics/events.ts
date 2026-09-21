/**
 * EN（EN ROADMAP.md Phase 0：Import / Export / Failed / settings key）。
 *
 * EN，EN。
 * All capture EN trackEvent，EN / ENCloseEN no-op。
 */
import { posthog } from './posthog'

export const AnalyticsEvent = {
  /** ImportEN（Upload/ENvideoENproject） */
  VideoImported: 'video_imported',
  /** Export：SucceededgenerateClip */
  ClipsExported: 'clips_exported',
  /** ENFailed（Import/EN/Clip/EN） */
  ProcessingFailed: 'processing_failed',
  /** settings/update LLM API key */
  ApiKeyConfigured: 'api_key_configured',
} as const

export type AnalyticsEventName =
  (typeof AnalyticsEvent)[keyof typeof AnalyticsEvent]

/** EN。posthog EN opt-out EN no-op（EN）。 */
function trackEvent(
  name: AnalyticsEventName,
  properties?: Record<string, unknown>,
): void {
  // posthog.capture EN init EN；EN
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
  /** EN key EN，EN */
  hasKey: boolean
}): void {
  trackEvent(AnalyticsEvent.ApiKeyConfigured, props)
}
