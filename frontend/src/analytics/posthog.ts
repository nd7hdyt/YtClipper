/**
 * PostHog product analytics / instrumentation
 *
 * Design goals (see ROADMAP.md Phase 0): anonymous, opt-out, local buffering.
 * - Anonymous: no PII by default, anonymous device ID before sign-in; person profiles only after identify.
 * - Opt-out: user can disable in Settings; status persists in localStorage across restarts.
 * - Local buffering: posthog-js buffers events in memory; core flow not lost on offline/proxy exit.
 *
 * Without VITE_PUBLIC_POSTHOG_KEY, this module is entirely no-op,
 * so dev (no key) won't pollute prod data.
 */
import posthog from 'posthog-js'

const POSTHOG_KEY = import.meta.env.VITE_PUBLIC_POSTHOG_KEY as string | undefined
const POSTHOG_HOST =
  (import.meta.env.VITE_PUBLIC_POSTHOG_HOST as string | undefined) ??
  'https://us.i.posthog.com'

/** Storage key for analytics opt-out (true = disabled). */
const OPT_OUT_STORAGE_KEY = 'autoclip.analytics.optOut'

let initialized = false

/** Whether analytics is enabled (key configured and not opt-out). */
export function isAnalyticsEnabled(): boolean {
  if (!POSTHOG_KEY) return false
  try {
    return localStorage.getItem(OPT_OUT_STORAGE_KEY) !== 'true'
  } catch {
    return true
  }
}

/**
 * Initialize PostHog. Call once at app startup.
 * Return immediately without key; no network request.
 */
export function initAnalytics(): void {
  if (initialized) return
  if (!POSTHOG_KEY) {
    if (import.meta.env.DEV) {
      console.info('[analytics] VITE_PUBLIC_POSTHOG_KEY not configured, analytics disabled')
    }
    return
  }

  posthog.init(POSTHOG_KEY, {
    api_host: POSTHOG_HOST,
    // Desktop loads via file:// / custom protocol; cookies unreliable, so persist anonymous ID in localStorage
    persistence: 'localStorage',
    // No person profile before sign-in, stay anonymous; associate via identify after sign-in (see ROADMAP Phase 1)
    person_profiles: 'identified_only',
    // Auto-capture page clicks/inputs, plus manual key events for funnels
    autocapture: true,
    // Privacy-first: no session recording by default (needs enabling on PostHog side)
    disable_session_recording: true,
    // Manually report pageview under HashRouter (see trackPageview)
    capture_pageview: false,
    capture_pageleave: true,
    // Respect user's local opt-out preference
    opt_out_capturing_by_default: !isAnalyticsEnabled(),
    loaded: (ph) => {
      if (import.meta.env.DEV) ph.debug()
    },
  })

  initialized = true
}

/**
 * Enable/disable analytics (Settings toggle). Persists to localStorage.
 */
export function setAnalyticsEnabled(enabled: boolean): void {
  try {
    localStorage.setItem(OPT_OUT_STORAGE_KEY, enabled ? 'false' : 'true')
  } catch {
    /* Ignore when localStorage unavailable */
  }
  if (!initialized) return
  if (enabled) posthog.opt_in_capturing()
  else posthog.opt_out_capturing()
}

/** Report a pageview (on route change). */
export function trackPageview(path: string): void {
  if (!initialized) return
  posthog.capture('$pageview', { $current_url: path })
}

/** Associate identity after sign-in (Phase 1). */
export function identifyUser(
  distinctId: string,
  properties?: Record<string, unknown>,
): void {
  if (!initialized) return
  posthog.identify(distinctId, properties)
}

/** Reset anonymous identity on sign-out. */
export function resetUser(): void {
  if (!initialized) return
  posthog.reset()
}

export { posthog }
