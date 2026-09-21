# Design System — AutoClip

> AutoClip EN。EN UI/VisualDecisionsEN。
> EN：**Restrained Professional / Calm Premium**（Reference Dia Browser）。Quiet、EN、Ample Whitespace、EN，
> Only one restrained blue for emphasis。EN"EN"EN，EN、EN。

## Product Context
- **EN**：Based on AI EN。EN BEN/YouTube EN → EN。
- **EN**：EN / EN。
- **EN**：macOS EN（Tauri + React + TypeScript）。EN Ant Design，EN。
- **EN**：EN、EN、EN——EN"EN"。

## Aesthetic Direction
- **EN**：Calm Premium / EN。
- **EN**：minimal（EN，EN）。
- **EN**：Quiet、EN、EN、EN。EN、EN、EN。
- **Reference**：Dia Browser (diabrowser.com) —— sans+serif EN、Near-Monochrome、EN。
- **ENDo not**：Toy-like Contrasting Colors、Colorful chip、Purple Gradient、Neon、3 EN、EN、Pure Black `#000`。

## Color

EN（EN，EN）。EN**EN**：EN、EN、EN；EN。

### EN（EN）
```css
--bg:        #F6F5F3;  /* EN，EN */
--card:      #FFFFFF;
--ink:       #1A1A19;  /* EN，EN */
--sub:       #6E6B66;  /* EN */
--muted:     #A8A59F;  /* EN/EN */
--line:      #EBE9E4;  /* EN */
--line-2:    #F0EEEA;  /* EN */
--accent:    #2D6BFF;  /* EN，EN */
--thumb:     #EEECE8;  /* EN */
--cta-bg:    #1A1A19;  /* EN：EN */
--cta-fg:    #FFFFFF;
```

### EN
```css
--bg:        #19181A;  /* EN，EN */
--card:      #211F22;
--ink:       #ECEAE6;  /* EN */
--sub:       #A6A29B;
--muted:     #76726C;
--line:      #2C2A2D;
--line-2:    #232124;
--accent:    #5A8BFF;  /* EN */
--thumb:     #262428;
--cta-bg:    #ECEAE6;  /* EN：EN */
--cta-fg:    #19181A;
```

### EN（EN，EN）
```css
--ok:    #5BB36A;  /* EN（EN） */
--warn:  #E6B23C;
--error: #E66A5C;  /* EN */
--info:  var(--accent);
```
- **EN**：EN，EN；EN 10–15% EN。

## Typography

sans + serif EN：EN**EN**（wordmark、EN），ChineseEN UI EN。

- **EN/EN（EN）**：`Instrument Serif`（EN italic）。EN `AutoClip` wordmark、ENEnglishEN。
- **Chinese**：`PingFang SC`（mac EN、EN）EN，EN `Noto Sans SC`。
- **UI / EN（EN）**：`Geist`（400/500/600）。**EN Inter/Roboto**。
- **EN / EN / EN**：`Geist Mono`（tabular）。
- **TypographyEN**：
  ```css
  --font-sans: "Geist", "PingFang SC", "Noto Sans SC", system-ui, sans-serif;
  --font-serif: "Instrument Serif", Georgia, serif;   /* EN */
  --font-mono: "Geist Mono", ui-monospace, monospace;
  ```
- **EN**（rem，16px EN）：
  | EN | EN | EN | EN |
  |------|------|------|------|
  | wordmark（serif）| 28px | 400 | 1.1 |
  | EN h2 | 16px | 600 | 1.3 |
  | EN | 15px | 500 | 1.45 |
  | EN | 14–15px | 400 | 1.5 |
  | EN/EN | 12.5–13px | 400/500 | 1.4 |
  | EN/uppercase | 11px / letter-spacing .8px | 500 | — |

## Spacing
- **EN**：4px。
- **EN**：spacious（Ample Whitespace、EN）。
- **EN**：`2(2) xs(4) sm(8) md(16) lg(24) xl(32) 2xl(40) 3xl(56)`。
- **EN**：EN 56px；ENSpacing 56px；EN gap 24px；EN 20–22px；EN。

## Layout
- **EN**：grid-disciplined（EN），EN。
- **EN**：3 EN（ENSpacing、EN），EN 2/1 EN。
- **EN**：EN，EN 56px EN。
- **Border Radius**：EN/EN/EN `16px`；EN `10px`；EN/EN/EN `999px`（EN）。
- **EN**：EN `1px solid var(--line)`，EN。

## Components
- **EN**：EN（EN=EN/EN=EN），EN 14.5px/500，EN ~14×26px。
- **EN**：EN，EN `--sub`。
- **EN**（EN/EN）：EN `--line-2` EN，EN `--card` EN + EN。
- **State Expression（EN）**：EN + EN（`EN`/`EN`=accent、`EN`=ok、`EN`=error）。EN 4px EN（accent），EN mono。
- **EN**：EN mono EN + EN，EN `7 EN · 1 EN · 8 EN`，**ENColorful chip**。
- **EN**：EN。`0 1px 2px rgba(0,0,0,.03), 0 8px 24px rgba(0,0,0,.04)`（EN）。

## App Layer（EN，2026-09-07）
EN UI EN `frontend/src/ui/`（`index.tsx` + `ac.css`）EN，AntD EN（Select / Form EN / message）。EN、EN**Do not**EN AntD `Card` / `Tag` / `Tabs` / `Alert` / `Button` EN。

| EN | EN | EN |
|------|------|------|
| `ac-page` / `ac-back` / `ac-title` / `ac-meta` | EN | EN 22px/600；EN 12.5px `--muted`，EN mono，EN `.dot` EN；EN `‹ EN`，EN |
| `Section` | EN | EN 15px/600 + mono EN（`--muted`）+ EN；EN |
| `Row` | EN | EN+EN、EN，EN（macOS EN）；EN `.ac-unit` EN |
| `Segmented` | EN/EN | EN；EN `--card` EN + EN；EN Tabs |
| `Btn` | EN | `cta`（EN）/ EN（EN）/ `text`（QuietEN）/ `danger`（EN，EN）；EN `text` EN hover EN |
| `StatusDot` | EN | 6px EN + EN：`--accent` EN / `--ok` EN / `--error` EN；**ENColorful chip** |
| `ProgressLine` | EN | 4px EN + EN mono EN |
| `ac-card` + `ac-card-thumb` + `ac-tag` | EN（EN / EN / EN） | 16:9 EN；EN mono EN（EN / EN / EN）；EN 14px EN；EN mono |
| `Dialog` | EN | portal EN body；520px；EN + EN + EN + EN；Esc / EN |
| `ac-empty` | EN / EN | EN，`b` EN + EN；EN mono EN，EN Alert |
| `Icon.*` | EN | EN SVG、1.5px EN；EN emoji、EN icon Typography |

- **EN**：EN emoji + Colorful（EN `getCategoryInfo` EN），EN chip EN。
- **EN**：EN「EN」EN + EN（EN `EN · EN`、EN `EN`、EN 0 EN）。EN / OS / EN / EN，EN。

## Motion
- **EN**：minimal-functional + EN intentional。EN，EN。
- **EN**：EN `ease-out`、EN `ease-in`、EN `ease-in-out`。
- **EN**：micro 80–120ms、short 150–250ms。
- **EN**：EN hover EN 2px + EN；EN。
- **EN**：「EN」EN（EN、EN），EN"EN"。

## Web / Marketing Layer（EN autoclip_intro）
EN token（EN：`--ac-*`，EN `autoclip_intro/tokens.css`），EN"EN"EN。EN：**EN，EN**。

- **Display EN**（web EN，EN）：
  | EN | EN | EN | EN |
  |------|------|------|------|
  | hero h1 | `clamp(40px, 1.6rem+3vw, 60px)` | 500 | EN 1.12，letter-spacing −.02em；EnglishEN serif italic EN，ChineseEN |
  | hero wordmark | 28–40px serif | 400 | EN h1 EN，EN logo EN |
  | section h2 | `clamp(28px, 1.3rem+1.5vw, 36px)` | 500 | EN 11px uppercase eyebrow（`--muted`） |
  | lede | 17px | 400 | `--sub`，EN 56ch |
  | EN | 16px | 400 | EN 14–15px |
- **EN**：EN 1120px；ENSpacing `clamp(72px, 6vw+40px, 128px)`；EN，EN。
- **EN（Product Frame）**：hero EN HTML/CSS EN（EN `--line` EN，EN），EN（EN、EN、3 EN、EN、4px EN）。ENVisual，EN UI EN——EN。**EN**。
- **EN**：EN（5:7），EN UI EN（EN / EN / EN），EN、EN。
- **EN / FAQ**：EN + mono EN + EN；FAQ EN `details`，EN `+ / –` mono EN。
- **EN**：EN（macOS / Windows），mono EN + EN，EN；EN CTA EN UA EN。
- **LanguageEN**：EN（EN / EN / EN / 한），EN。
- **EN**：EN `prefers-color-scheme`，ENProvidesEN；EN。

## Decisions Log
| EN | Decisions | EN |
|------|------|------|
| 2026-05-31 | ENDesign System | /design-consultation EN。EN（EN→EN→EN）EN Dia EN「Restrained Professional」，EN/EN，EN、EN、EN。 |
| 2026-09-06 | EN；EN Web EN | EN 2025 EN Tailwind EN（EN、Colorful icon EN、EN），EN。ENVisual，EN token EN、EN display EN；hero EN，EN，EN UI EN。EN `index.html` + `tokens.css`（GitHub Pages EN）。 |
| 2026-09-07 | EN（EN / EN / EN）；EN App Layer EN | EN AntD EN「EN AI EN」EN：Colorful Tag、EN、EN/EN、emoji EN。EN Granola / Raycast / Dia EN「Quiet、EN、EN、EN」EN，EN、EN、EN / EN / EN `frontend/src/ui/` EN；AntD EN Select / Form / message。EN。 |
