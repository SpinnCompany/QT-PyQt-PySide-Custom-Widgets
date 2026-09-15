#!/usr/bin/env python3
"""Print the authoritative widget count.

Four different numbers were live at once on 2026-09-15 — the marketing site said
89 on one page and 117 on another, the docs said 164, and a crude `^class Q`
grep gave 193. They disagreed because nothing derived from anything: each had
been typed by hand at a different moment.

`Custom_Widgets.mcp.catalog` is the source that wins, for three reasons:

  * 2.4.0 introduced it explicitly as "the single source for what widgets
    exist", and the MCP server, the stub generator and the launch-gate manifest
    already import it rather than re-counting;
  * it is pure AST over the package, so it needs no Qt binding, imports
    nothing, and cannot drift from the code it describes;
  * the alternatives are gone or stale. `docs/design/tiering-manifest.json`
    — which `gen_widget_docs.py` reads and the docs' 164 derives from — was
    stripped from this repo when its history was rewritten, and survives only
    on `archive/tiering-manifest-internal`. The 193 figure counted helper and
    internal classes that were never widgets.

A "widget" is a class declaring `__catalog__`. That is the same definition the
MCP catalog, the type stubs and Qt Designer registration already use, so this
number and those surfaces cannot disagree.

Usage:
    python tools/widget_count.py           # 118
    python tools/widget_count.py --json    # {"widgets": 118, "droppable": 116}
"""
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Custom_Widgets.mcp import catalog  # noqa: E402


def uncatalogued():
    """Widget classes that ship but never declared `__catalog__`.

    The catalog is the right definition but it is not currently COMPLETE. This
    returns every class under QCustom*.py without `__catalog__`, which includes
    internal helpers as well as real widgets — treat it as an upper bound on the
    gap, not a widget count.

    Cross-referenced against the docs on 2026-09-15, **37 of them are real,
    documented, shipping widgets** (QCustomCheckBox, QCustomChip,
    QCustomCodeEditor, QCustomArcLoader …) and **33 of those declare
    WIDGET_DOM_XML**, so they are droppable in Qt Designer. They are missing
    from the MCP catalog, the generated type stubs and the launch-gate manifest,
    silently.

    Reporting the gap rather than hiding it is the point: publishing the
    catalogued figure alone understates the product, which is exactly how 118
    briefly reached a pricing page that should have said 155.
    """
    import glob
    import re

    catalogued = set(catalog.discover_widgets())
    root = catalog.widgets_package_dir()
    found = set()
    for path in glob.glob(os.path.join(root, "**", "QCustom*.py"), recursive=True):
        if "__pycache__" in path:
            continue
        with open(path, encoding="utf-8", errors="ignore") as fh:
            src = fh.read()
        for m in re.finditer(r"^class (Q[A-Za-z0-9_]+)\s*\(", src, re.M):
            found.add(m.group(1))
    return sorted(found - catalogued)


def counts():
    widgets = catalog.discover_widgets()
    missing = uncatalogued()
    return {
        "widgets": len(widgets),
        # Droppable = declares WIDGET_DOM_XML, i.e. can be placed in Qt Designer.
        "droppable": sum(1 for w in widgets.values() if w["droppable"]),
        # Classes that ship without __catalog__ — the catalog's blind spot.
        "uncatalogued": len(missing),
    }


if __name__ == "__main__":
    data = counts()
    if "--json" in sys.argv:
        print(json.dumps(data))
    else:
        print(data["widgets"])
