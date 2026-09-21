/**
 * EN + Global properties（super properties）。
 *
 * - Global properties：app_version / os / arch / locale，EN，
 *   EN"version / system / arch"ClipEN（EN"ENversionENsystemFailedENHigh"EN）。
 * - EN：
 *   - app_installed：EN（= EN）
 *   - app_opened：On each startup（PostHog EN DAU / EN）
 *   - app_updated：versionENChange
 */
import { getVersion } from '@tauri-apps/api/app'
import { posthog } from './posthog'

const INSTALL_FLAG_KEY = 'autoclip.analytics.installed'
const LAST_VERSION_KEY = 'autoclip.analytics.lastVersion'
const SESSION_COUNT_KEY = 'autoclip.analytics.sessionCount'

/** EN webview EN UA Rough parseActionssystem，EN Rust EN plugin-os EN。 */
function detectOS(): string {
  const ua = navigator.userAgent
  if (/Mac/i.test(ua)) return 'macos'
  if (/Win/i.test(ua)) return 'windows'
  if (/Linux/i.test(ua)) return 'linux'
  return 'unknown'
}

/** Rough parse CPU arch（EN Intel / Apple Silicon EN）。 */
function detectArch(): string {
  const ua = navigator.userAgent
  if (/arm64|aarch64/i.test(ua)) return 'arm64'
  if (/x86_64|x64|Win64|WOW64|Intel/i.test(ua)) return 'x64'
  return 'unknown'
}

async function getAppVersion(): Promise<string> {
  try {
    return await getVersion()
  } catch {
    // EN Tauri EN（EN vite dev）ENtoversion
    return 'unknown'
  }
}

function readInt(key: string): number {
  try {
    return parseInt(localStorage.getItem(key) || '0', 10) || 0
  } catch {
    return 0
  }
}

function safeSet(key: string, value: string): void {
  try {
    localStorage.setItem(key, value)
  } catch {
    /* ignore */
  }
}

export interface RuntimeInfo { version: string; os: string; arch: string; locale: string }
let runtimeInfo: RuntimeInfo = { version: 'unknown', os: detectOS(), arch: detectArch(), locale: typeof navigator !== 'undefined' ? navigator.language : '' }

/** EN（version / system / arch），EN；EN。 */
export function getRuntimeInfo(): RuntimeInfo {
  return runtimeInfo
}

/**
 * ENGlobal propertiesEN。
 * EN initAnalytics() ENonce。posthog EN。
 */
export async function trackLaunch(): Promise<void> {
  const version = await getAppVersion()
  const os = detectOS()
  const arch = detectArch()
  const locale = navigator.language
  runtimeInfo = { version, os, arch, locale }

  if (typeof posthog?.register !== 'function') return

  // Global properties：EN
  posthog.register({
    app_version: version,
    os,
    arch,
    app_locale: locale,
  })

  // EN
  const sessionCount = readInt(SESSION_COUNT_KEY) + 1
  safeSet(SESSION_COUNT_KEY, String(sessionCount))

  // ENinstall
  let isInstalled = false
  try {
    isInstalled = localStorage.getItem(INSTALL_FLAG_KEY) === 'true'
  } catch {
    /* ignore */
  }
  if (!isInstalled) {
    posthog.capture('app_installed', { version, os, arch })
    safeSet(INSTALL_FLAG_KEY, 'true')
  }

  // versionupdate
  let lastVersion: string | null = null
  try {
    lastVersion = localStorage.getItem(LAST_VERSION_KEY)
  } catch {
    /* ignore */
  }
  if (lastVersion && lastVersion !== version) {
    posthog.capture('app_updated', { from_version: lastVersion, to_version: version })
  }
  safeSet(LAST_VERSION_KEY, version)

  // On each startup
  posthog.capture('app_opened', { version, session_number: sessionCount })
}
