# RhythmoTune — Music Dashboard

A music-player dashboard built the **correct Custom_Widgets way** — the forms
pipeline, granular component `.ui` forms, a token-driven JSON theme, and a
`GuiFunctions` orchestrator. Reproduces the "RhythmoTune" reference: a cover-flow
hero, category chips, a popular-songs row and a now-playing transport bar, in a
dark (and matching light) theme with real cover/avatar imagery.

## Three widgets this example added to the library

| Widget | What it is |
| ------ | ---------- |
| **`QCustomCoverFlow`** | 3D cover-flow carousel — active cover centred with a scrim + title/artist + play badge, neighbours peek scaled & dimmed; click / drag / wheel / arrows to rotate, eased animation. Data-driven (`setItems`). |
| **`QCustomCoverCard`** | Album/song cover card — rounded art + gradient scrim + title + artist + hover play. Used for every "Popular songs" tile. |
| **`QCustomPlayerBar`** | Now-playing transport bar — cover, title/artist, prev / play-pause / next, a click-drag seek slider with times, and favourite / shuffle / repeat / volume. Every glyph is painted (no font icons) so it recolours on a theme switch. |

## Architecture

```
ui/*.ui  ->  src/ui_*.py            (Custom_Widgets --convert-ui)
json-styles/style.json              (RhythmoTune Dark / Light + ChartPalette)
Qss/scss/*.scss                     ($TOKENS, no hard-coded hex in chrome)
gui/GuiFunctions.py                 (orchestrator: per-region builders + ImageWorker)
```

- **MainWindow.ui** is the shell: a sidebar + right column (top bar over a
  scroll area with the hero, categories and popular rows) with the player bar
  pinned full-width at the bottom. Every region is a
  `QCustomComponentContainer` pointing at a granular component form.
- **Components:** `Sidebar`, `TopBar`, `HeroCard` (coverflow), `CategoriesRow`
  (`QCustomChipGroup`), `PopularSongs` (six `QCustomCoverCard`), `PlayerBar`
  (`QCustomPlayerBar`).
- **Theming:** each theme's brand/chart colours live in its `Other-variables`
  in `json-styles/style.json`; `GuiFunctions` reads them with
  `themeEngine.customColors()` (no style.json parsing in app code) and re-applies
  on `onThemeChangeComplete`, so the whole UI flips on a theme switch. The gear
  icon calls `themeEngine.toggleTheme("RhythmoTune Dark", "RhythmoTune Light")`.
- **Imagery:** the widgets fetch their OWN cover/avatar images — pass a URL to
  `QCustomAvatar.setImageSource`, `QCustomCoverCard.setData(coverPath=…)`,
  `QCustomCoverFlow.setItems([{coverPath: url}])` or `QCustomPlayerBar.setTrack(
  coverPath=…)` and the shared `Custom_Widgets.ImageLoader` downloads + disk-caches
  it asynchronously (accent-gradient fallback until it lands).
- **Icons** are set in the `.ui` (`QCustomQPushButton`/`QCustomQLabel` `iconName`
  + `iconSize`) and recoloured from QSS (`qproperty-iconColor`, incl. `:checked`
  accent nav) — `GuiFunctions` has no icon code at all. (`Custom_Widgets`
  `recolor_icon`/`themed_icon` remain available for one-off Python use.)

> **Status:** see [SESSION_REPORT.md](SESSION_REPORT.md) for the full build log,
> the rules established, and one open issue (the live dark/light toggle needs the
> theme engine to re-apply + repolish on switch — colours currently come 100%
> from QSS, which the framework doesn't yet re-apply live).

### The library did the heavy lifting

This build deliberately pushed reusable capability INTO the framework rather than
into the app, so `GuiFunctions` stays thin (region binding only):

| Was hand-rolled in the app | Now a library capability |
| -------------------------- | ------------------------ |
| `icon_pixmap` SVG tinting  | `Custom_Widgets.recolor_icon` / `themed_icon` |
| `round_pixmap` + `ImageWorker` + `_onImage` | `Custom_Widgets.ImageLoader` + `QCustom*` image sources; `QCustomAvatar.imageSource` |
| `gui/theme.py` reading `ChartPalette` | `themeEngine.customColors()` / `themeColor(role)` (per-theme `Other-variables`) |
| computing the dark/light target | `themeEngine.toggleTheme(dark, light)` |

## Run

Build the compiled forms, then run:

```
Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src
python main.py
```
