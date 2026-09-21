# AutoClip AnalyticsEN

> EN：**PostHog**（US EN，`https://us.i.posthog.com`）
> EN（EN `ROADMAP.md` Phase 0）：**EN · EN · EN**。EN PII、EN、EN、API key EN。

## 1. EN

| EN | EN | EN |
|------|------|---------|
| 🌟 EN | EN | `clips_exported` |
| EN | EN / EN | EN / `app_installed` |
| EN | EN→EN、EN | EN |
| EN | D1/D7/D30、EN | `app_opened`（PostHog EN） |
| EN | EN、EN | EN |
| EN | EN、EN key EN、EN | `api_key_configured` / `processing_failed` |

## 2. EN

```
EN .dmg → app_installed → video_imported → clips_exported(★EN) → EN(EN)
```

## 3. EN

EN：`EN_EN`，snake_case。EN `src/analytics/events.ts`，EN key EN no-op。

### EN（`src/analytics/lifecycle.ts`）
| EN | EN | EN |
|------|------|------|
| `app_installed` | EN | `version, os, arch` |
| `app_opened` | EN | `version, session_number` |
| `app_updated` | EN | `from_version, to_version` |

### EN
| EN | EN | EN |
|------|---------|------|
| `video_imported` | `api.ts` `uploadFiles` / `createDownloadTask` / `createYouTubeDownloadTask` | `source(upload/url), fileType, sizeBytes` |
| `clips_exported` ★ | `api.ts` `downloadVideo` | `clipCount, exportType(clip/collection/project)` |

### EN
| EN | EN | EN |
|------|---------|------|
| `api_key_configured` | `SettingsPage` EN | `provider, hasKey`（**EN**） |

### EN
| EN | EN | EN |
|------|---------|------|
| `processing_failed` | `api.ts` EN/EN catch | `stage(import/export/...), code, message` |

> EN/EN **Sentry**（Phase 0 EN），PostHog EN。

## 4. EN（Super Properties）

EN，EN `lifecycle.ts` EN `trackLaunch()` EN：
`app_version`（Tauri `getVersion()`）· `os` · `arch` · `app_locale`。

## 5. EN

- EN：EN ID（PostHog EN，`localStorage` EN）。
- Phase 1 AccountEN：EN `identifyUser(userId)`、EN `resetUser()`（`src/analytics/posthog.ts` EN）。

## 6. EN（App EN）

App EN `app_installed` EN。EN，EN PostHog EN snippet EN `download_clicked`，EN"EN→EN→EN"EN。

## 7. EN / EN

- EN → EN → **EN** EN（`setAnalyticsEnabled`），EN，EN。
- EN、EN PII、key EN `hasKey`。
- EN**EN**（《EN》EN）。

## 8. EN

EN（`frontend/.env.local`，EN gitignore）：
```
VITE_PUBLIC_POSTHOG_KEY=phc_xxx
VITE_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com
```
ENAnalyticsEN no-op。EN `frontend/.env.example`。

## 9. EN

1. EN `events.ts` EN `AnalyticsEvent` EN + EN。
2. EN import EN（EN `services/api.ts` EN）。
3. EN。
