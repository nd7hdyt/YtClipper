# Design System — AutoClip

> AutoClip 。 UI/。
> ：** / Calm Premium**（ Dia Browser）。、、、，
>  。""，Is、Is。

## Product Context
- **Is**： AI 。 B/YouTube  → 。
- ****： / 。
- ****：macOS （Tauri + React + TypeScript）。 Ant Design，System。
- ****：、、——"Is"。

## Aesthetic Direction
- ****：Calm Premium / 。
- ****：minimal（，）。
- ****：、、From、。、、。
- ****：Dia Browser (diabrowser.com) —— sans+serif 、、。
- ****：、 chip、、、3 、、 `#000`。

## Color

（，）。****：、、；。

### （）
```css
--bg:        #F6F5F3;  /* ， */
--card:      #FFFFFF;
--ink:       #1A1A19;  /* ， */
--sub:       #6E6B66;  /*  */
--muted:     #A8A59F;  /* / */
--line:      #EBE9E4;  /*  */
--line-2:    #F0EEEA;  /*  */
--accent:    #2D6BFF;  /* ， */
--thumb:     #EEECE8;  /*  */
--cta-bg:    #1A1A19;  /* ： */
--cta-fg:    #FFFFFF;
```

### 
```css
--bg:        #19181A;  /* ， */
--card:      #211F22;
--ink:       #ECEAE6;  /*  */
--sub:       #A6A29B;
--muted:     #76726C;
--line:      #2C2A2D;
--line-2:    #232124;
--accent:    #5A8BFF;  /*  */
--thumb:     #262428;
--cta-bg:    #ECEAE6;  /* ： */
--cta-fg:    #19181A;
```

### （，）
```css
--ok:    #5BB36A;  /* Completed（） */
--warn:  #E6B23C;
--error: #E66A5C;  /*  */
--info:  var(--accent);
```
- ****：Is ，Is； 10–15% 。

## Typography

sans + serif Is：****（wordmark、）， UI 。

- **/（Only）**：`Instrument Serif`（ italic）。 `AutoClip` wordmark、。
- ****：`PingFang SC`（mac 、）， `Noto Sans SC`。
- **UI / （）**：`Geist`（400/500/600）。** Inter/Roboto**。
- ** /  / **：`Geist Mono`（tabular）。
- ****：
  ```css
  --font-sans: "Geist", "PingFang SC", "Noto Sans SC", system-ui, sans-serif;
  --font-serif: "Instrument Serif", Georgia, serif;   /* Only */
  --font-mono: "Geist Mono", ui-monospace, monospace;
  ```
- ****（rem，16px ）：
  |  |  |  |  |
  |------|------|------|------|
  | wordmark（serif）| 28px | 400 | 1.1 |
  |  h2 | 16px | 600 | 1.3 |
  |  | 15px | 500 | 1.45 |
  |  | 14–15px | 400 | 1.5 |
  | / | 12.5–13px | 400/500 | 1.4 |
  | /uppercase | 11px / letter-spacing .8px | 500 | — |

## Spacing
- ****：4px。
- ****：spacious（、）。
- ****：`2(2) xs(4) sm(8) md(16) lg(24) xl(32) 2xl(40) 3xl(56)`。
- ****： 56px； 56px； gap 24px； 20–22px；。

## Layout
- ****：grid-disciplined（），。
- ****：3 （、），To 2/1 。
- ****：， 56px 。
- ****：// `16px`； `10px`；// `999px`（）。
- ****： `1px solid var(--line)`，。

## Components
- ****：（=/=）， 14.5px/500， ~14×26px。
- ****：， `--sub`。
- ****（/）： `--line-2` ，Select `--card`  + 。
- **（）**： + （`Download`/``=accent、`Completed`=ok、``=error）。Progress 4px （accent）， mono。
- **Completed**： mono  + ， `7  · 1  · 8  `，** chip**。
- ****：。`0 1px 2px rgba(0,0,0,.03), 0 8px 24px rgba(0,0,0,.04)`（）。

## App Layer（，2026-09-07）
 UI  `frontend/src/ui/`（`index.tsx` + `ac.css`），AntD （Select / Form  / message）。、**** AntD `Card` / `Tag` / `Tabs` / `Alert` / `Button` 。

|  |  |  |
|------|------|------|
| `ac-page` / `ac-back` / `ac-title` / `ac-meta` |  |  22px/600； 12.5px `--muted`， mono， `.dot` ；Is `‹ `，Is |
| `Section` |  |  15px/600 + mono （`--muted`）+ ；   |
| `Row` |  | +、，（macOS System）； `.ac-unit`  |
| `Segmented` | /Select | ；Select `--card`  + ； Tabs |
| `Btn` |  | `cta`（）/ （）/ `text`（）/ `danger`（Only，）； `text`  hover  |
| `StatusDot` |  | 6px  + ：`--accent`  / `--ok`  / `--error` ；** chip** |
| `ProgressLine` | Progress | 4px  +  mono  |
| `ac-card` + `ac-card-thumb` + `ac-tag` | （ /  / ） | 16:9 ； mono （ /  / ）； 14px ； mono |
| `Dialog` |  | portal To body；520px； +  +  + ；Esc /  |
| `ac-empty` |  /  | ，`b`  + ； mono ， Alert |
| `Icon.*` |  |  SVG、1.5px ； emoji、 icon  |

- ****： emoji + （ `getCategoryInfo` ）， chip 。
- ****：「」 + （ ` · `、 ``、 0 ）。 / OS /  / ，。

## Motion
- ****：minimal-functional +   intentional。，。
- ****： `ease-out`、 `ease-in`、 `ease-in-out`。
- ****：micro 80–120ms、short 150–250ms。
- ****： hover  2px + ；Progress。
- ** **：「」 （、），""。

## Web / Marketing Layer（ autoclip_intro）
 token（：`--ac-*`， `autoclip_intro/tokens.css`），""。：**Is，Is **。

- **Display **（web ，）：
  |  |  |  |  |
  |------|------|------|------|
  | hero h1 | `clamp(40px, 1.6rem+3vw, 60px)` | 500 |  1.12，letter-spacing −.02em；  serif italic ， |
  | hero wordmark | 28–40px serif | 400 |  h1 ， logo  |
  | section h2 | `clamp(28px, 1.3rem+1.5vw, 36px)` | 500 |  11px uppercase eyebrow（`--muted`） |
  | lede | 17px | 400 | `--sub`， 56ch |
  |  | 16px | 400 |  14–15px |
- ****： 1120px； `clamp(72px, 6vw+40px, 128px)`；，。
- **（Product Frame）**：hero  HTML/CSS （ `--line` ，），（、、3 、、4px Progress）。Is，Is UI ——。****。
- ****：（5:7）， UI （ /  / ），、。
- ** / FAQ**： + mono  + ；FAQ  `details`， `+ / –` mono 。
- **Download**：（macOS / Windows），mono  + ，； CTA  UA 。
- ****：（ / EN /  / 한），。
- ****：System `prefers-color-scheme`，；。

## Decisions Log
|  |  |  |
|------|------|------|
| 2026-05-31 | System | /design-consultation 。（→→） Dia 「」，/，、、。 |
| 2026-09-06 | System； Web  |  2025  Tailwind （、 icon 、），。，Is  token To、 display ；hero ，， UI 。 `index.html` + `tokens.css`（GitHub Pages ）。 |
| 2026-09-07 | （ /  / ）； App Layer  | Is AntD 「 AI 」： Tag、、/、emoji 。 Granola / Raycast / Dia 「、、、System」， 、、 /  /  `frontend/src/ui/` ；AntD  Select / Form / message。。 |
