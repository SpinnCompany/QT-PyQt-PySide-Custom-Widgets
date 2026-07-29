# RhythmoTune — Session Report

Reproduced the "RhythmoTune" music-dashboard reference as a proper Custom_Widgets
forms-pipeline app, and hardened the library along the way. This report captures
what shipped, the rules established, and the one open issue.

## 1. New library widgets

| Widget | Purpose |
| ------ | ------- |
| `QCustomCoverFlow` | 3D cover-flow hero — active cover centred (scrim + title/artist + play), neighbours peek scaled/dimmed; click/drag/wheel/arrow, eased. Data-driven; loads item cover URLs itself. |
| `QCustomCoverCard` | Album/song tile — art + gradient scrim + title/artist + hover play. Hooks added: `textAlign`, `scrimColor` (per-slot accent band), `titleScale`. Loads cover URLs itself. |
| `QCustomPlayerBar` | Now-playing transport bar — cover, title/artist, prev/play/next, seek slider, favourite/shuffle/repeat/volume. All glyphs painted (no font icons). |
| `QCustomQLabel` | QLabel that recolours an SVG icon from a QSS `iconColor` property (`iconName`/`iconSize`). |

Extended existing widgets: `QCustomQPushButton` gained `iconName`/`iconColor`
(SVG recoloured from QSS, incl. `:checked`/`:hover` states); `QCustomAvatar`
gained `cornerRadius` (rounded-square) + `imageSource` (async URL loading).

## 2. New library infrastructure

- `Custom_Widgets/ImageLoader.py` — async URL/file image loading + disk cache;
  `load_image()`, `rounded_pixmap()`. Widgets fetch their own imagery.
- `Custom_Widgets/Utils.py` — `recolor_icon()`, `themed_icon()`,
  `resolve_icon_path()` (feather → material → font_awesome).
- `QCustomTheme` — `customColors()`, `themeColor(role)`, `toggleTheme(dark, light)`;
  and a **compile-cache fix** (key on theme NAME so a switch between two
  same-class themes recompiles `main.css` instead of reusing stale CSS).

## 3. Architecture rules established (see project memory)

1. **Forms pipeline** — granular `.ui` components → compiled `src/` +
   `json-styles/style.json` themes + `Qss/scss` tokens + a thin `GuiFunctions`.
2. **All styling from QSS/SCSS** — Python may only `setProperty`, `polish`,
   `unpolish` (+ content: `setText`/`setIcon`). No `setStyleSheet` anywhere.
   Region chrome uses objectName + token + state selectors in `chrome.scss`.
3. **Icons/pixmaps/sizes set in the `.ui`** (Designer). Dynamic aspects (colour)
   via a widget property in Python or QSS `qproperty-*`. Prefer the QSS-recolour
   icon widgets (`QCustomQPushButton`/`QCustomQLabel` `iconColor`).
4. **Per-theme brand colours** live in each theme's `Other-variables` → available
   as `$name` SCSS tokens AND via `themeEngine.customColors()`.
5. **Goal: eliminate/reduce user GUI code** — the framework does the work; the
   manager just feeds data + wires signals. RhythmoTune's `GuiFunctions` has zero
   icon/style/colour code.

## 4. Result

Faithful reproduction of the reference (logo, nav, expandable playlists, search,
Premium chip, cover-flow hero, category chips, coloured popular-song cards, player
bar) with real imagery. `GuiFunctions` is pure data + wiring.

## 5. OPEN ISSUE — live theme toggle

After moving **all** colours to QSS `qproperty-*`, the **live** dark/light toggle
stopped visually applying: on disk everything is correct and in sync (persisted
theme, `_variables.scss`, `main.css`), but the running app holds a stale
stylesheet. It worked before only because the old manager re-set colours in
Python on each theme change, masking two framework issues (plain-`QWidget` panels
need `WA_StyledBackground` to paint a global-QSS background; `qproperty` colours
aren't repolished on a live switch). Full diagnosis in memory
`qss-only-theming-live-apply-gap`.

**Resolution options (undecided):**
- (a) Keep painted-widget + icon **colours** as Python `setProperty` reapplied on
  `onThemeChangeComplete` (allowed by the QSS-only rule; proven to theme
  reliably) — icon *names/sizes* stay in the `.ui`, chrome in QSS.
- (b) Fix the theme engine to fully re-apply the compiled CSS + unpolish/polish
  the tree on switch, and give container panels `WA_StyledBackground`, so pure
  `qproperty` theming works live.
