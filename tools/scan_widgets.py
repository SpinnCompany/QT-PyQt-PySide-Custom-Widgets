#!/usr/bin/env python3
"""Widget tiering & hardening scanner.

Mechanically inventories every user-facing widget in Custom_Widgets and its
coverage signals (test / example / __catalog__ / Designer-registration / .pyi),
proposes a free/Pro tier, and writes docs/design/tiering-manifest.md.

This is the launch-gate artifact: the free/Pro SKU split is not locked until
every user-facing widget is tested, stable, secure, and tier-classified. The
presence signals here are objective; the Tier / Stable / Secure judgments are
human and refined during the hardening pass.

Usage:  python tools/scan_widgets.py
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CW = os.path.join(ROOT, "Custom_Widgets")
DATE = "2026-07-31"  # bump when regenerating

# Rendered into the Markdown table. Built via chr() so this .py stays glyph-free
# for the design linter; the generated .md still shows a real check mark / dash.
CHECK = chr(0x2705)   # white heavy check mark
DASH = chr(0x2014)    # em dash

# Chart-subsystem engine + shared helpers: shipped as free library internals,
# not standalone widgets, so they carry no separate tier.
INTERNAL = re.compile(r'(ChartBase|ChartView|ChartDataManager|ChartExporter|'
                      r'ChartProps|ChartThemeManager|ChartToolbar|ChartTooltip|'
                      r'LegendManager|QLineSeries|BarSeries|BarChartBase|'
                      r'ChartConstants|ChartEnums)')

# --- Ratified tiers (2026-07-24) ------------------------------------------
# Decision: everything is FREE except the 5 anchors below; no Pro "watchlist"
# earmarks (mini data-viz, editors, tree, timeline all stay free for now).

# Free base classes that already have (or anchor) a separate compiled Pro widget.
PRO_EXT = {
    "QCustomDataTable": "DataTable Pro (SKU-1, LOCKED - built)",
    "QCustomAreaChart": "Charts Pro (SKU-2, candidate)",
    "QCustomLineChart": "Charts Pro (SKU-2, candidate)",
    "QCustomBarChart": "Charts Pro (SKU-2, candidate)",
    "QCustomPieChart": "Charts Pro (SKU-2, candidate)",
}

# Library infrastructure, not standalone catalog widgets. Still free/open-source;
# just not sellable/tierable widgets, so they carry no free/Pro tier.
INFRA = {
    "QCustomComponent", "QCustomComponentContainer", "QCustomComponentLoader",
    "QCustomTheme", "QCustomThemeList",
}

# Display-name fixups where the scanned primary class isn't the public widget.
WIDGET_OVERRIDE = {
    "Custom_Widgets/QCustomAnnotationWidget.py": "QCustomAnnotationWidget",
    "Custom_Widgets/QCustomModals.py": "QCustomModals",
}

CLASS_RE = re.compile(r'^class\s+([A-Z]\w+)\s*\(([^)]*)\)', re.M)
WIDGET_BASE = re.compile(
    r'QWidget|QFrame|QLabel|QPushButton|QDialog|QAbstractButton|QTableView|'
    r'QTableWidget|QTreeWidget|QStackedWidget|QScrollArea|QSlider|QComboBox|'
    r'QLineEdit|QPlainTextEdit|QTextEdit|QMainWindow|QGraphicsView|QToolButton|'
    r'QCheckBox|QCustom|ChartBase|GaugeWidget')


def _read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def scan():
    tests_text = "\n".join(_read(p) for p in
                           glob.glob(os.path.join(ROOT, "tests", "**", "*.py"), recursive=True))
    examples_text = "\n".join(_read(p) for p in
                              glob.glob(os.path.join(ROOT, "examples", "**", "*.py"), recursive=True))
    example_dirs = set(os.listdir(os.path.join(ROOT, "examples", "PySide6")))
    register_text = _read(os.path.join(CW, "Plugins", "register.py"))

    mods = []
    # Recursive: widgets live under Custom_Widgets/widgets/<group>/ since the
    # 2026-07-31 regrouping, and a non-recursive glob silently dropped every
    # module that had moved — the manifest is the launch gate, so a widget
    # going missing from it must not be possible.
    mods += glob.glob(os.path.join(CW, "**", "QCustom*.py"), recursive=True)
    # Two widgets that do not match the QCustom* prefix. Globbed rather than
    # hardcoded at the package root, because they moved with the regrouping and
    # a fixed path silently dropped them from the launch gate.
    for _stray in ("AnalogGaugeWidget.py", "QFlowProgressBar.py"):
        mods += glob.glob(os.path.join(CW, "**", _stray), recursive=True)
    # QCustomMapView lives behind a facade in the optional [map] subpackage, so
    # neither the QCustom* glob nor the stray list above finds it. Its row was
    # added to the manifest by hand (commit 8ffdcb82f) and every regeneration
    # then silently deleted it again — precisely the "a widget going missing
    # must not be possible" failure the comment above warns about. The class is
    # QCustomMapView(QWidget), so name resolution needs no override.
    mods += glob.glob(os.path.join(CW, "map", "facade.py"))
    mods = sorted({m for m in mods
                   if os.path.isfile(m)
                   and not m.endswith(".pyi")
                   and "__pycache__" not in m})

    rows = []
    for m in mods:
        src = _read(m)
        stem = os.path.splitext(os.path.basename(m))[0]
        classes = CLASS_RE.findall(src)
        widget_classes = [c for c, base in classes
                          if WIDGET_BASE.search(base) or WIDGET_BASE.search(c)]
        primary = (stem if any(c == stem for c, _ in classes)
                   else (widget_classes[0] if widget_classes
                         else (classes[0][0] if classes else stem)))
        rel = os.path.relpath(m, ROOT)
        names = {primary, stem} | set(widget_classes)
        primary = WIDGET_OVERRIDE.get(rel, primary)   # public-widget display name

        def hit(corpus):
            return any(re.search(r'\b%s\b' % re.escape(nm), corpus) for nm in names)

        rows.append({
            "module": os.path.relpath(m, ROOT),
            "widget": primary,
            "loc": src.count("\n") + 1,
            # Stubs live at the PUBLIC path, not beside a module that has moved
            # into a subpackage — that is what users import and the only thing
            # type checkers resolve. That is usually flat
            # (Custom_Widgets/QCustomX.pyi) but nested for the charts
            # (Custom_Widgets/QCustomCharts/QCustomLineChart.pyi), so search
            # rather than guess a single location.
            "pyi": bool(glob.glob(os.path.join(CW, "**",
                                               os.path.splitext(os.path.basename(m))[0] + ".pyi"),
                                  recursive=True)),
            "catalog": "__catalog__" in src,
            "test": hit(tests_text),
            "example": hit(examples_text) or primary in example_dirs or stem in example_dirs,
            "designer": hit(register_text),
        })
    return rows


def tier(r):
    if INTERNAL.search(r["module"]) or r["widget"] in INFRA:
        return "internal"
    if r["widget"] in PRO_EXT:
        return "pro-ext"
    return "free"


def render(rows):
    for r in rows:
        r["tier"] = tier(r)

    def y(b):
        return CHECK if b else DASH

    order = {"pro-ext": 0, "free": 1, "internal": 2}
    rows.sort(key=lambda r: (order[r["tier"]], r["widget"].lower()))

    def table(subset):
        out = ["| Widget | Test | Example | Catalog | Designer | .pyi | LOC | Module |",
               "|---|:--:|:--:|:--:|:--:|:--:|--:|---|"]
        for r in subset:
            out.append("| `%s` | %s | %s | %s | %s | %s | %d | %s |" % (
                r["widget"], y(r["test"]), y(r["example"]), y(r["catalog"]),
                y(r["designer"]), y(r["pyi"]), r["loc"], r["module"]))
        return "\n".join(out)

    pro = [r for r in rows if r["tier"] == "pro-ext"]
    free = [r for r in rows if r["tier"] == "free"]
    internal = [r for r in rows if r["tier"] == "internal"]
    n = len(rows)

    def pc(k):
        return "%d/%d (%d%%)" % (sum(r[k] for r in rows), n,
                                 round(100 * sum(r[k] for r in rows) / n))

    nl = "\n"
    untested = [r for r in rows if r["tier"] != "internal" and not r["test"]]
    uncataloged = [r for r in rows if r["tier"] != "internal" and not r["catalog"]]
    no_example = [r for r in rows if r["tier"] != "internal" and not r["example"]]

    return f"""# Widget Tiering & Hardening Manifest

**Generated mechanically {DATE}** by `tools/scan_widgets.py` (test / example /
`__catalog__` / Designer-registration / `.pyi` coverage per widget). This is the
launch gate artifact: no free/pro SKU split is locked until every user-facing row
below is **tested, stable, secure, and tier-classified**, then the whole product
ships at once.

> **Tiers RATIFIED {DATE}:** everything is **free** except the 5 anchors
> (`free -> Pro`); DataTable Pro is locked, Charts Pro is a candidate. No Pro
> "watchlist" earmarks - mini data-viz, editors, tree and timeline all stay free
> for now. `internal` = engine + infrastructure (still open-source, not a
> sellable widget). Remaining gate work: the per-widget **Stable/Secure** review.

> Regenerate: `python tools/scan_widgets.py`. Presence signals are objective; the
> tier decisions above are ratified; Stable/Secure remain a human review pass.

## Coverage summary ({n} widget modules)

| Signal | Coverage |
|---|---|
| Has a test | {pc('test')} |
| Has an example | {pc('example')} |
| In `__catalog__` | {pc('catalog')} |
| Designer-registered | {pc('designer')} |
| `.pyi` type stub | {pc('pyi')} |

Breakdown: **{len(pro)}** free-base-with-Pro-extension, **{len(free)}** free
standalone, **{len(internal)}** internal/engine (not shipped as standalone).

## Legend
- **Test / Example / Catalog / Designer / .pyi** -- objective presence signals.
- **Tier** -- proposed classification: `free` (ships free, standalone),
  `free -> Pro` (free base kept in core, a compiled Pro widget extends it),
  `internal` (engine/helper, not a standalone shipped widget).
- **Stable / Secure** -- filled during the hardening pass (not mechanical).

---

## Tier: free base -> Pro extension ({len(pro)})

Stay free in the core; the Pro package extends them (never bundles them).

{table(pro)}

Pro mapping:
{nl.join("- `%s` -> %s" % (w, PRO_EXT[w]) for w in PRO_EXT if any(r['widget'] == w for r in pro))}

## Tier: free -- standalone ({len(free)})

{table(free)}

## Internal / engine -- not standalone widgets ({len(internal)})

Chart-subsystem engine + shared helpers. Ship as free library internals; no
separate tier. (Most surface through the public chart types above.)

{table(internal)}

---

## Hardening backlog (drives the gate)

### Untested user-facing widgets ({len(untested)}) -- highest priority
{nl.join("- `%s` (%s)" % (r['widget'], os.path.basename(r['module'])) for r in sorted(untested, key=lambda r: r['widget'].lower()))}

### Missing `__catalog__` entry ({len(uncataloged)})
{nl.join("- `%s`" % r['widget'] for r in sorted(uncataloged, key=lambda r: r['widget'].lower()))}

### Missing example ({len(no_example)})
{nl.join("- `%s`" % r['widget'] for r in sorted(no_example, key=lambda r: r['widget'].lower())) or "- (none)"}

## Per-widget hardening checklist (fill during the pass)

Before a tier is locked, each user-facing widget needs:
- [ ] Test present & passing (headless)
- [ ] Example present & runs
- [ ] `__catalog__` entry (name, group, capabilities, edition)
- [ ] `.pyi` stub for IDE/Designer typing
- [ ] Stability: no crash on empty/huge/edge inputs; theme-switch safe
- [ ] Security: no eval/exec/network/file-write on untrusted input; QSS-injection safe
- [ ] Tier ratified (free / free-to-Pro / internal)
"""


def main():
    rows = scan()
    doc = render(rows)
    path = os.path.join(ROOT, "docs", "design", "tiering-manifest.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(doc)
    # machine-readable sidecar for downstream tooling
    with open(os.path.join(ROOT, "docs", "design", "tiering-manifest.json"), "w") as fh:
        json.dump(rows, fh, indent=2)
    print("wrote", os.path.relpath(path, ROOT), "(%d widget modules)" % len(rows))


if __name__ == "__main__":
    main()
