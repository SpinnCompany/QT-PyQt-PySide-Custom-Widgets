########################################################################
## WIDGET CATALOG — the single source for what widgets exist.
##
## The MCP server (`widgets_catalog` / `customwidgets://catalog` resource),
## the type-stub generator and the launch-gate manifest all need the same
## inventory of widgets and their `__catalog__` metadata. It used to be
## re-implemented (differently) in server.py and stubgen.py; this module is
## the one implementation they all import.
##
## Everything here is pure stdlib + AST — no widget is imported or
## instantiated, so it is safe in the headless server and in standalone tools.
########################################################################
import ast
import functools
import glob
import os


def widgets_package_dir():
    """Absolute path of the Custom_Widgets package.

    Derived from this module's location rather than `import Custom_Widgets`,
    so catalog consumers stay import-light (no qtpy pull) and never trigger a
    Qt bootstrap.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _ast_literal(node):
    try:
        return ast.literal_eval(node)
    except (ValueError, SyntaxError):
        return None


def class_catalog(node, stem):
    """Extract a widget's catalog entry from its ClassDef, or None if the class
    declares no `__catalog__`."""
    catalog = None
    attrs = {}
    for stmt in node.body:
        if not isinstance(stmt, ast.Assign):
            continue
        for tgt in stmt.targets:
            if not isinstance(tgt, ast.Name):
                continue
            if tgt.id == "__catalog__":
                catalog = _ast_literal(stmt.value)
            elif tgt.id in ("WIDGET_MODULE", "WIDGET_TOOLTIP", "WIDGET_DOM_XML"):
                attrs[tgt.id] = _ast_literal(stmt.value)
    if not isinstance(catalog, dict):
        return None
    doc = ast.get_docstring(node)
    summary = (doc.strip().splitlines()[0] if doc
               else (attrs.get("WIDGET_TOOLTIP") or ""))
    return {
        "name": catalog.get("name") or node.name,
        "class": node.name,
        "module": attrs.get("WIDGET_MODULE") or "Custom_Widgets.%s" % stem,
        "summary": summary,
        "props": catalog.get("props", {}),
        "signals": catalog.get("signals", []),
        "tokens_used": catalog.get("tokens_used", []),
        "droppable": "WIDGET_DOM_XML" in attrs,
    }


@functools.lru_cache(maxsize=1)
def discover_widgets():
    """Scan the Custom_Widgets package for widgets declaring `__catalog__` and
    return {name: entry}. Parsed via AST — nothing is imported or instantiated,
    so it's safe and fast in the headless server process."""
    out = {}
    # Recursive: widgets live under Custom_Widgets/widgets/<group>/ since the
    # 2026-07-31 regrouping. A top-level-only glob silently dropped every
    # module that had moved, emptying them out of the MCP catalog and out of
    # stub generation with no error to show for it.
    _paths = glob.glob(os.path.join(widgets_package_dir(), "**", "QCustom*.py"),
                       recursive=True)
    for path in sorted(p for p in _paths if "__pycache__" not in p):
        stem = os.path.splitext(os.path.basename(path))[0]
        try:
            with open(path, encoding="utf-8") as fh:
                tree = ast.parse(fh.read(), filename=path)
        except (OSError, SyntaxError):
            continue
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                entry = class_catalog(node, stem)
                if entry:
                    out[entry["name"]] = entry
    return out


def find_widget(name):
    """Catalog entry for `name` (catalog name or class name, case-insensitive),
    or None if no widget matches."""
    widgets = discover_widgets()
    info = widgets.get(name)
    if info is None:
        needle = name.lower()
        info = next((w for w in widgets.values()
                     if w["name"].lower() == needle or w["class"].lower() == needle),
                    None)
    return info