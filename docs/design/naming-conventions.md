# Naming conventions

**Ratified 2026-07-31.** Enforced by the `camelcase-api` rule in
`Custom_Widgets.lint`.

---

## The rule

**Public API in `Custom_Widgets` is camelCase, not PEP 8 snake_case.**

```python
# yes
def setChecked(self, checked): ...
def isComplete(self): ...
def currentIndex(self): ...
sizeVariant = Property(str, ...)

# no
def set_checked(self, checked): ...
def is_complete(self): ...
def current_index(self): ...
```

This covers **public methods on classes** and **Qt properties**. It does not
cover:

- module-level functions — plain Python helpers, not part of the widget API
- `_private` and `__dunder` names — internal, style is the author's call
- local variables and module constants — ordinary Python style applies

## Why

These widgets are called in the same expression as Qt's own API:

```python
field.setSizeVariant("lg")      # ours
field.setMinimumHeight(48)      # Qt's
```

A snake_case method in that surface reads as foreign and forces the caller to
remember which convention applies to which call — a per-call cognitive tax that
buys nothing. Qt has been camelCase for thirty years and every Qt binding
(PySide, PyQt) follows it; a Qt-facing widget library that half-follows PEP 8
is the worst of both.

It is also what the codebase already does: at the time the rule was written it
was **3507 camelCase methods to 72 snake_case** — about 98%. This ratifies
existing practice rather than introducing a new one.

## Enforcement

`camelcase-api` is a **warning**, not an error, and the 69 pre-existing
violations are recorded in `.custom_widgets_lint_baseline.json`. So:

- existing code keeps working and is not mass-renamed
- **new** snake_case public methods are flagged immediately

```
python -m Custom_Widgets.lint Custom_Widgets/
```

Deliberate exceptions carry a trailing justification:

```python
def setup_method(self):     # allow-snake-case: pytest collection hook
    ...
```

## Renaming an existing method

Do **not** bulk-rename. Every public method is API that user code and generated
`.ui` files may reference. When a snake_case method genuinely needs to become
camelCase:

1. add the camelCase name as the real implementation
2. keep the snake_case name as a thin forwarding alias
3. remove the fingerprint from the lint baseline
4. drop the alias only at a major version, with a note in the changelog

Related: [tiering-manifest.md](tiering-manifest.md) tracks per-widget API
coverage (`__catalog__`, `.pyi`, Designer registration), which is where a
renamed method will show up if a stub goes stale.
