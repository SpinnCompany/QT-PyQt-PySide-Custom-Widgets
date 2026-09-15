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


def counts():
    widgets = catalog.discover_widgets()
    return {
        "widgets": len(widgets),
        # Droppable = declares WIDGET_DOM_XML, i.e. can be placed in Qt Designer.
        "droppable": sum(1 for w in widgets.values() if w["droppable"]),
    }


if __name__ == "__main__":
    data = counts()
    if "--json" in sys.argv:
        print(json.dumps(data))
    else:
        print(data["widgets"])
