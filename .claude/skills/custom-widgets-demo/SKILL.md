---
name: custom-widgets-demo
description: Build a runnable, screenshot-verified demo app with the design-token widget set (QCustomStatCard, DataTable, Splitter, Carousel, ChipGroup, ProgressRing, Kbd, Card, QCustomQPushButton). Use when creating an example/showcase, a new examples/PySide6/* folder, or any from-scratch app that should be styled with applyDesignTokens. Covers the theming pattern, the gotchas, and the self-screenshot driver for headless verification.
---

# Building a Custom Widgets demo

## ⛔ RULE #1 — MCP first (do this before anything below)

Before ANY custom-widgets task: **mount the `customwidgets` MCP server, then read its
shipped agent knowledge (AGENT_GUIDE / instructions) and its skills.** Only then start.
Build and run apps **through the MCP** (runApp / app-control / Designer + QSS bridge) —
**never** via ad-hoc `python`/Bash. If the MCP is not connected in your session, STOP
and ask the user to connect it; do not silently fall back to a shell. This rule ships
with the product and applies to every agent that touches this repo.

## ⭐ RULE #2 — don't ship a BORING GUI (hard-won, 2026-07-23)

Clean chrome is not the goal; a **rich, dense, widget-heavy** screen is. Repeated
user feedback on a "competent but boring" build:

1. **USE the custom widgets — densely.** The library is the point. A page of
   label-in-card + empty space is a failure. Fill screens with real data-viz:
   charts (`QCustomLineChart/AreaChart/BarChart/PieChart` — gradient/glow fills),
   `QCustomProgressRing` (show REAL values, not 0%), progress bars/meters,
   `QCustomStepper`, `QCustomCarousel`, `QCustomTabWidget`, `QCustomBadge`,
   `QCustomAvatarGroup`, `QCustomTimeline`, sparklines, colour-blocked/active
   cards. Run `widgets_catalog` and actually place many of them.
2. **Exploit QSS + CustomTheme freedom.** Gradients (`qlineargradient`),
   `qproperty-icon`, per-role/per-objectName styling, oversized bold numbers,
   bold accent COLOUR-BLOCK panels. Reach for the boldest option, not the safest.
3. **Depth = borderless fill + big radius (~22px). NO drop shadows unless truly
   necessary** (`QGraphicsDropShadowEffect` was explicitly rejected). Hairline
   borders read as technical/boring.
4. **Design to a real modern reference** (Dribbble/product dashboards), matching
   its DENSITY and colour energy — not just tidy spacing.

See memory `modern-ui-design-bar` + `custom-widgets-theme-icon-pipeline`
(switch custom themes BY NAME via `setTheme`, never the generic dark/light
toggle; study `examples/svg_icons_demo` rather than hacking the theme engine).

## The demo pattern

The token widgets need **no `.ui`, no `.qrc`, no JSON** — instantiate widgets in
plain layouts and style the whole app with one call. This is the preferred path
for any new `examples/PySide6/*` showcase. Reference implementation:
`examples/PySide6/AuroraCommandDeck/main.py`.

## The theming pattern

```python
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens, DesignTokens

def apply_theme(app, theme):            # theme = "light" | "dark"
    tokens = DesignTokens(theme=theme)
    app.setStyleSheet(base_chrome(tokens))   # 1. your window shell FIRST
    applyDesignTokens(app, tokens=tokens)    # 2. widgets append their marked block
    return tokens
```

`applyDesignTokens` wraps its QSS in markers and replaces only that block, so
`setStyleSheet(chrome)` (which wipes the whole sheet) must come **first**, then
the token call re-adds the widget styles. A live theme toggle is just
`apply_theme(app, other_theme)` again.

Derive your own chrome from token roles so it flips with the theme — never
hard-code colours:

```python
def base_chrome(tokens):
    return "QWidget#root {{ background:{muted}; }} ...".format(
        surface=tokens.role("surface"), muted=tokens.role("surface-muted"),
        on_surface=tokens.role("on-surface"), outline=tokens.role("outline"),
        primary=tokens.role("primary"))
```

Roles available: `surface`, `surface-muted`, `on-surface`, `primary`,
`on-primary`, `primary-hover`, `secondary`, `outline`, `destructive`,
`focus-ring` (see `Custom_Widgets/JSonStyles/tokens.py`).

## Widget quick-reference (verified signatures)

| Widget | Construct / key API |
| --- | --- |
| `QCustomQPushButton` | `b = QCustomQPushButton("Save"); b.variant = "primary"` (primary/secondary/outline/ghost/destructive); `b.sizeVariant = "sm|md|lg"` |
| `QCustomStatCard` | `QCustomStatCard(label=, value=, delta=, trend="up|down|flat", caption=)`; `.setValue()`, `.setDelta(text, trend=)` |
| `QCustomDataTable` | `.setColumns([DataTableColumn(key, title, type="text|number|bool", width=, formatter=lambda v:...)])`; `.setData(list[dict])`; `.pageSize = 8`; `.setFilterText(s)`; signal `rowSelected(int)` — **index is the source row**, not the visible one |
| `QCustomChipGroup` | `QCustomChipGroup(selectable=True, exclusive=True)`; `.addChip(text, data=)`; signal `selectionChanged(list)` (list of `data`) |
| `QCustomCarousel` | `QCustomCarousel(wrap=True)`; `.addSlide(widget)`; `.setAutoAdvance(ms)`; `.next()/.previous()` |
| `QCustomSplitter` | `QCustomSplitter(Qt.Horizontal)`; then normal QSplitter API + `.setSizes([...])` |
| `QCustomProgressRing` | `QCustomProgressRing(value=87)`; `.setValue(int)`; give it a fixed size |
| `QCustomCard` | `QCustomCard(title=, subtitle=)`; `.addWidget()`, `.addLayout()` |
| `QCustomKbd` | `QCustomKbd(keys="Ctrl+K")` |

## Gotchas (learned the hard way)

- **App-wide `QWidget { ... }` QSS strips native styling from plain Qt inputs.**
  A bare `QLineEdit` then renders as a black box (invisible in light mode). If
  your chrome touches `QWidget`, explicitly style `QLineEdit`/`QComboBox`/etc.
  from token roles too.
- Set `b.variant` / `b.sizeVariant` as **attributes**, not `setProperty` — and
  never `setProperty(sameName)` inside a declared `@Property` setter (infinite
  recursion). Use `sizeVariant`, not `size` (shadows `QWidget.size`).
- Call `applyDesignTokens(app, ...)` once up front; re-call only to switch theme.

## Verify before declaring done

The environment has a real display (`DISPLAY=:1`) and `.venv` with PySide6.
Give the demo a screenshot driver so you can *see* the result and share it:

```python
# python main.py --shots DIR   -> writes light+dark PNGs, keeps running
QtCore.QTimer.singleShot(900,  lambda: win.grab().save(f"{d}/dark.png"))
QtCore.QTimer.singleShot(1400, win.toggle_theme)
QtCore.QTimer.singleShot(2000, lambda: win.grab().save(f"{d}/light.png"))
```

Then run headless functional checks (`QT_QPA_PLATFORM=offscreen`) driving the
real signals — filter, chip selection, `rowSelected`, theme round-trip — before
calling it done. Read the PNGs back to catch visual bugs a test can't.
