# AutoClip 

> tool：**PostHog**（US ，`https://us.i.posthog.com`）
> （ `ROADMAP.md` Phase 0）：** ·  · local**。 PII、、subtitles、API key 。

## 1. 

|  |  |  |
|------|------|---------|
| 🌟  | succeeded | `clips_exported` |
| fetch | download / install | download / `app_installed` |
|  | import→、 | event |
|  | D1/D7/D30、 | `app_opened`（PostHog ） |
|  | 、 | event |
|  | model、 key 、failed | `api_key_configured` / `processing_failed` |

## 2. 

```
download .dmg → app_installed → video_imported → clips_exported(★) → ()
```

## 3. event

：`_`，snake_case。 `src/analytics/events.ts`，config key  no-op。

### （`src/analytics/lifecycle.ts`）
| event |  |  |
|------|------|------|
| `app_installed` | start | `version, os, arch` |
| `app_opened` | start | `version, session_number` |
| `app_updated` | version | `from_version, to_version` |

### 
| event | location |  |
|------|---------|------|
| `video_imported` | `api.ts` `uploadFiles` / `createDownloadTask` / `createYouTubeDownloadTask` | `source(upload/url), fileType, sizeBytes` |
| `clips_exported` ★ | `api.ts` `downloadVideo` | `clipCount, exportType(clip/collection/project)` |

### config
| event | location |  |
|------|---------|------|
| `api_key_configured` | `SettingsPage` succeeded | `provider, hasKey`（****） |

### error
| event | location |  |
|------|---------|------|
| `processing_failed` | `api.ts` import/export catch | `stage(import/export/...), code, message` |

> / **Sentry**（Phase 0 ），PostHog failed。

## 4. （Super Properties）

event， `lifecycle.ts`  `trackLaunch()` ：
`app_version`（Tauri `getVersion()`）· `os` · `arch` · `app_locale`。

## 5. model

- now： ID（PostHog ，`localStorage` ）。
- Phase 1 account：sign in `identifyUser(userId)`、 `resetUser()`（`src/analytics/posthog.ts` ）。

## 6. download（App ）

App  `app_installed` 。official site， PostHog  snippet  `download_clicked`，"→download→install"。

## 7.  / 

- Settings page → settings → **** （`setAnalyticsEnabled`），status，。
- default、 PII、key  `hasKey`。
- ****（《Personal Info Protection Law》）。

## 8. config

env var（`frontend/.env.local`， gitignore）：
```
VITE_PUBLIC_POSTHOG_KEY=phc_xxx
VITE_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com
```
 no-op。 `frontend/.env.example`。

## 9. eventstep

1.  `events.ts`  `AnalyticsEvent`  + 。
2. call import call（ `services/api.ts` ）。
3. updatefileevent。
