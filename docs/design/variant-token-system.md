# Variant/size API + design tokens (pilot: QCustomQPushButton)

**Status:** Proposed / not started
**Owner:** TBD
**Created:** 2026-07-22
**Parent:** modernization-roadmap.md (Gap #2)

## Summary

Introduce a modern component API — `variant` + `size` props — driven by a new
**design-token** system, replacing per-instance QSS. Pilot on
`QCustomQPushButton`, then template across the widget catalog.

Decisions locked (see roadmap quiz):

- **Variant mechanism:** Qt **dynamic properties + QSS attribute selectors**
  (Designer-editable, runtime hot-swappable, no subclasses).
- **Token model:** **hybrid** — Tailwind-like primitive scales + a Material-3-like
  semantic role layer that references them.
- **Format:** **clean break** from the current flat theme JSON (no compat shim).
- **Catalog:** include **machine-readable catalog hooks** from day one for
  MCP/agent introspection.

## Current state (what we're replacing)

Theme JSON today is a flat 4-color model per theme
(`Background-color`, `Text-color`, `Accent-color`, `Icons-color`) under
`QSettings.ThemeSettings.CustomThemes[]` (see
`examples/svg_icons_demo/json-styles/style.json`). Buttons carry no `variant`/
`size` concept — styling is ad-hoc QSS + imperative helpers like
`setObjectTheme("1")` with hard-coded `QColor`s in `QCustomQPushButton.py`.
There is no semantic scale for spacing/radius/typography/elevation.

Problems: no consistency across widgets, no variants, theme = 4 colors only,
colors hard-coded in Python, nothing an agent can introspect.

## Token architecture (two layers)

### Layer 1 — primitives (raw values, theme-independent)
Tailwind-like scales. Example (illustrative):

```jsonc
"primitives": {
  "color": {
    "blue":   { "50": "#eff6ff", "500": "#3b82f6", "600": "#2563eb", "...": "" },
    "slate":  { "50": "#f8fafc", "900": "#0f172a", "...": "" }
  },
  "space":  { "1": 4, "2": 8, "3": 12, "4": 16, "6": 24 },   // px
  "radius": { "sm": 4, "md": 8, "lg": 12, "full": 9999 },
  "font":   { "size": { "sm": 13, "md": 14, "lg": 16 }, "weight": { "regular": 400, "medium": 500, "semibold": 600 } },
  "elevation": { "0": "none", "1": "0 1px 2px rgba(0,0,0,.12)", "2": "0 2px 6px rgba(0,0,0,.16)" }
}
```

### Layer 2 — semantic roles (reference primitives; swap per theme)
Material-3-like roles. Light/dark/accent are just different role bindings.

```jsonc
"semantic": {
  "surface":        "{color.slate.50}",
  "on-surface":     "{color.slate.900}",
  "surface-muted":  "{color.slate.100}",
  "primary":        "{color.blue.600}",
  "on-primary":     "#ffffff",
  "primary-hover":  "{color.blue.700}",
  "outline":        "{color.slate.300}",
  "destructive":    "{color.red.600}",
  "focus-ring":     "{color.blue.500}"
}
```

Components only ever reference **semantic** tokens, never primitives directly.
This is what makes theming composable and keeps variants theme-agnostic.

Resolution: `{color.blue.600}` references are resolved at compile time by the
SCSS engine into QSS values. Ties directly into `docs/design/scss-engine.md` —
tokens should be a first-class input to that engine, exposed as SCSS variables/
functions (e.g. `token('primary')`).

## Variant + size API

Props exposed as Qt dynamic properties on the widget:

| Prop      | Values                                                        | Default   |
|-----------|--------------------------------------------------------------|-----------|
| `variant` | `primary` \| `secondary` \| `outline` \| `ghost` \| `destructive` | `primary` |
| `size`    | `sm` \| `md` \| `lg`                                          | `md`      |

Set from Python, `.ui` XML, or Designer:

```python
btn.setProperty("variant", "ghost")
btn.setProperty("size", "sm")
```
```xml
<property name="variant"><string>ghost</string></property>
```

QSS is generated from tokens per variant×size. Example (generated, not
hand-written):

```css
QCustomQPushButton {                       /* base */
  border-radius: token(radius.md);
  font-weight: token(font.weight.medium);
}
QCustomQPushButton[size="sm"] { padding: token(space.1) token(space.2); font-size: token(font.size.sm); }
QCustomQPushButton[size="md"] { padding: token(space.2) token(space.3); font-size: token(font.size.md); }

QCustomQPushButton[variant="primary"]           { background: token(primary); color: token(on-primary); }
QCustomQPushButton[variant="primary"]:hover     { background: token(primary-hover); }
QCustomQPushButton[variant="ghost"]             { background: transparent; color: token(on-surface); }
QCustomQPushButton[variant="ghost"]:hover       { background: token(surface-muted); }
QCustomQPushButton[variant="outline"]           { background: transparent; border: 1px solid token(outline); color: token(on-surface); }
QCustomQPushButton[variant="destructive"]       { background: token(destructive); color: token(on-primary); }
QCustomQPushButton:focus                        { outline: 2px solid token(focus-ring); } /* a11y, roadmap #5 */
```

### Naming: `sizeVariant`, not `size` (implementation note)
`size` cannot be used as a property name on a `QWidget` subclass — it shadows
`QWidget.size()` and breaks it (`'str' object is not callable`). The size prop is
therefore named **`sizeVariant`** (QSS selector `[sizeVariant="sm"]`). `variant`
is safe (no such method on QWidget).

### Declared Q_PROPERTY + QSS (implementation note)
`variant`/`sizeVariant` are **declared** `@Property(str)`. Qt QSS attribute
selectors read declared properties **via their getter** — so the setter must
**not** call `self.setProperty("variant", ...)`: for a declared property that
re-enters the same setter and recurses infinitely. The setter only stores the
value and calls `_repolish()`. Verified end-to-end: a `variant="primary"` button
paints exactly the `primary` token colour.

### Runtime re-style gotcha (important)
Qt does **not** re-evaluate attribute-selector QSS when a dynamic property
changes. When `variant`/`size` is set after construction, the widget must
force a repolish. Add a helper on the widget:

```python
def _repolish(self):
    self.style().unpolish(self)
    self.style().polish(self)
    self.update()
```

Expose `variant`/`size` as **`Property(str, notify=...)`** setters that call
`_repolish()` in their bodies, so both code and Designer edits take effect live.
(We use `str` Qt properties, not `QEnum`, per the mechanism decision — but the
setter can validate against the allowed value set and warn on unknown values.)

## Machine-readable catalog hooks

So an agent (via MCP) can introspect the system without reading source. Each
widget declares its API in a class-level descriptor; a registry aggregates them.

```python
class QCustomQPushButton(QPushButton):
    __catalog__ = {
        "name": "QCustomQPushButton",
        "props": {
            "variant": {"type": "enum", "values": ["primary","secondary","outline","ghost","destructive"], "default": "primary"},
            "size":    {"type": "enum", "values": ["sm","md","lg"], "default": "md"},
        },
        "signals": ["clicked"],
        "tokens_used": ["primary","on-primary","primary-hover","surface-muted","outline","destructive","focus-ring"],
    }
```

A `Custom_Widgets/registrars/catalog.py` walks all widgets and emits JSON. Later
an MCP tool (`catalog_list` / `catalog_describe`) serves it to agents. This is
the dependency the roadmap's "component-catalog introspection" tool builds on.

## Pilot scope (QCustomQPushButton only)

1. Define token schema + loader (`Custom_Widgets/JSonStyles/tokens.py`) — parse
   primitives + semantic, resolve `{ref}` chains, expose to SCSS engine.
2. Add `variant`/`size` `Property` setters + `_repolish()` to
   `QCustomQPushButton`. Keep legacy `setObjectTheme`/animation intact for now
   (removed in a later clean-break pass, documented in the docs repo).
3. Generate button QSS from tokens for all variant×size combos.
4. Add `__catalog__` descriptor + minimal registry walker.
5. Example + visual check via the `run`/`verify` skills across variants×sizes×themes.

Out of scope for the pilot: other widgets, MCP catalog tool, binding layer, WASM.

## Open questions

- Token file: one `tokens.json` per project, or split primitives (shipped
  defaults) vs semantic (per-project override)?
- Do we keep `Accent-color` from old themes as a migration convenience mapping to
  `semantic.primary`, or require full re-authoring? (Clean-break bias says
  re-author + provide a one-shot migration script, not a runtime shim.)
- SCSS `token()` function vs plain SCSS variables — decide with scss-engine.md.
- Secondary variant definition (is it muted-surface or a second accent?).
