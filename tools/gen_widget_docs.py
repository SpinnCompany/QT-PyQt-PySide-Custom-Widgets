#!/usr/bin/env python3
"""Generate Docusaurus reference pages + showcase screenshots per widget.

Docs for ~150 widgets cannot be hand-maintained: the moment a property is
added, every hand-written table is wrong and nobody notices. These pages are
derived from the things that cannot drift — the module docstring, `__catalog__`,
the live `metaObject` and the real constructor signature — so regenerating is
the fix for staleness rather than a chore.

Usage:
    python tools/gen_widget_docs.py                 # everything missing
    python tools/gen_widget_docs.py --all           # rewrite generated pages
    python tools/gen_widget_docs.py --only QCustomSwitch QCustomCard
    python tools/gen_widget_docs.py --no-shots      # skip screenshots

Hand-written pages are never touched unless --force is given: a page without
the generated marker is assumed to be better than anything this can produce.
"""
import argparse
import inspect
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Running `python tools/gen_widget_docs.py` puts tools/ on sys.path, not the
# repo root — without this the script silently imports an INSTALLED
# Custom_Widgets from site-packages instead of the working tree, and reports
# every widget as missing.
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
DOCS_REPO = os.path.join(os.path.dirname(ROOT), "Docs-QT-PyQt-PySide-Custom-Widgets")
WIDGET_DOCS = os.path.join(DOCS_REPO, "docs", "01-Widgets")
SHOTS = os.path.join(DOCS_REPO, "static", "img", "showcase")

MARKER = "<!-- generated:widget-reference -->"

#: Manifest entries that are not documentable widgets.
#: QCustomLoadingIndicators / QCustomProgressBars are re-export shims with no
#: class of their own; Ui_CustomMainWindow is a generated form.
SKIP = {"Canvas", "LoadForm", "QCustomLoadingIndicators", "QCustomProgressBars",
        "Ui_CustomMainWindow"}


# --------------------------------------------------------------------------- #
# Introspection
# --------------------------------------------------------------------------- #
def manifestRows():
    path = os.path.join(ROOT, "docs", "design", "tiering-manifest.json")
    data = json.load(open(path, encoding="utf-8"))
    rows = data if isinstance(data, list) else data.get("widgets", data.get("rows", []))
    return [r for r in rows if r.get("tier") in ("free", "pro-ext")
            and r.get("widget") not in SKIP]


def importWidget(name, module):
    """Import a widget class from its real module path."""
    dotted = os.path.splitext(module)[0].replace(os.sep, ".").replace("/", ".")
    mod = __import__(dotted, fromlist=[name])
    return getattr(mod, name, None)


def prose(cls, mod):
    """The human description: module banner comment, else the class docstring.

    The banner is preferred because that is where the *why* lives — the class
    docstring is usually one line.
    """
    source = ""
    try:
        source = inspect.getsource(sys.modules[cls.__module__])
    except Exception:
        pass
    lines = []
    for block in re.findall(r"^#{10,}\n((?:##.*\n)+)#{10,}", source, re.M):
        text = "\n".join(l[2:].strip() if l.startswith("##") else l
                         for l in block.strip().splitlines())
        if "SPINN DESIGN CODE" in text or "YOUTUBE" in text:
            continue
        lines.append(text)
    if lines:
        body = max(lines, key=len)
        # Drop the leading "QCustomX - summary." line; it becomes the intro.
        parts = body.split("\n", 1)
        summary = parts[0].strip()
        rest = parts[1].strip() if len(parts) > 1 else ""
        return summary, rest
    doc = inspect.getdoc(cls) or ""
    parts = doc.split("\n", 1)
    return parts[0].strip(), (parts[1].strip() if len(parts) > 1 else "")


def designerProperties(cls):
    """(name, type, default) from the live metaObject, minus QWidget's own."""
    from qtpy.QtWidgets import QWidget
    meta = getattr(cls, "staticMetaObject", None)
    if meta is None:
        return []
    first = QWidget.staticMetaObject.propertyCount()
    catalog = getattr(cls, "__catalog__", {}).get("props", {})
    out = []
    for i in range(first, meta.propertyCount()):
        prop = meta.property(i)
        name = prop.name()
        spec = catalog.get(name, {})
        kind = spec.get("type") or _friendlyType(prop.typeName())
        default = spec.get("default", "")
        if spec.get("values"):
            kind = "enum: " + " / ".join("`%s`" % v for v in spec["values"])
        out.append((name, kind, default))
    return out


def _friendlyType(typeName):
    return {"QString": "string", "bool": "bool", "int": "int",
            "double": "float", "float": "float",
            "QColor": "color"}.get(typeName, typeName)


def signalsOf(cls):
    from qtpy.QtCore import QMetaMethod
    meta = getattr(cls, "staticMetaObject", None)
    if meta is None:
        return []
    out = []
    for i in range(meta.methodOffset(), meta.methodCount()):
        method = meta.method(i)
        if method.methodType() == QMetaMethod.MethodType.Signal:
            out.append(bytes(method.methodSignature()).decode())
    return sorted(set(out))


def publicMethods(cls):
    """Methods defined on the class itself, skipping Qt overrides."""
    overrides = {"paintEvent", "resizeEvent", "mousePressEvent", "showEvent",
                 "mouseMoveEvent", "mouseReleaseEvent", "mouseDoubleClickEvent",
                 "keyPressEvent", "enterEvent", "leaveEvent", "hideEvent",
                 "focusInEvent", "focusOutEvent", "sizeHint", "minimumSizeHint",
                 "dragEnterEvent", "dragLeaveEvent", "dropEvent", "wheelEvent"}
    out = []
    for name, value in vars(cls).items():
        if name.startswith("_") or name in overrides:
            continue
        if not callable(value) or isinstance(value, type):
            continue
        try:
            signature = str(inspect.signature(value)).replace("(self, ", "(")
            signature = signature.replace("(self)", "()")
        except (TypeError, ValueError):
            signature = "(...)"
        doc = (inspect.getdoc(value) or "").split("\n")[0].strip()
        out.append((name + signature, doc))
    return sorted(out)


def constructorSignature(cls):
    try:
        signature = str(inspect.signature(cls.__init__)).replace("(self, ", "(")
        return cls.__name__ + signature.replace("(self)", "()")
    except (TypeError, ValueError):
        return cls.__name__ + "(parent=None)"


def exampleFor(name):
    rel = os.path.join("examples", "PySide6", name, "main.py")
    return rel if os.path.isfile(os.path.join(ROOT, rel)) else None


# --------------------------------------------------------------------------- #
# Screenshots
# --------------------------------------------------------------------------- #
def _domDefaults(cls):
    """Property defaults declared in WIDGET_DOM_XML, so a screenshot shows the
    widget as Qt Designer would drop it in rather than empty."""
    xml = getattr(cls, "WIDGET_DOM_XML", "") or ""
    out = {}
    for name, value in re.findall(
            r"<property name='([^']+)'>\s*<(?:string|number|double|bool)>"
            r"([^<]*)</(?:string|number|double|bool)>", xml):
        if name == "geometry":
            continue
        out[name] = value
    return out


def _isBlank(image):
    """A screenshot with one colour is worse than no screenshot."""
    colors = {image.pixel(x, y)
              for y in range(0, image.height(), 4)
              for x in range(0, image.width(), 4)}
    return len(colors) <= 1


def shoot(cls, slug, theme):
    """Render one widget to static/img/showcase/. Returns the filename or None."""
    from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout
    from Custom_Widgets.JSonStyles.tokens import applyDesignTokens

    app = QApplication.instance()
    applyDesignTokens(app, theme=theme)
    # Not everything the manifest lists is a QWidget — generated Ui_* form
    # classes turn up too, and QBoxLayout.addWidget rejects them outright.
    if not (isinstance(cls, type) and issubclass(cls, QWidget)):
        return None
    try:
        widget = cls()
    except Exception:
        return None
    for name, value in _domDefaults(cls).items():
        try:
            widget.setProperty(name, value)
        except Exception:
            pass

    host = QWidget()
    box = QVBoxLayout(host)
    box.setContentsMargins(16, 16, 16, 16)
    box.addWidget(widget)
    hint = widget.sizeHint()
    host.resize(max(180, hint.width() + 32), max(90, hint.height() + 32))
    host.ensurePolished()
    widget.ensurePolished()
    app.processEvents()

    pixmap = host.grab()
    image = pixmap.toImage()
    if image.isNull() or _isBlank(image):
        return None
    name = "%s%s.png" % (slug, "-dark" if theme == "dark" else "")
    os.makedirs(SHOTS, exist_ok=True)
    pixmap.save(os.path.join(SHOTS, name))
    return name


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def slugFor(name):
    return re.sub(r"^QCustom|^Q", "", name).lower()


def renderPage(cls, row, shots):
    name = cls.__name__
    summary, detail = prose(cls, row["module"])
    catalog = getattr(cls, "__catalog__", {})
    tooltip = getattr(cls, "WIDGET_TOOLTIP", "")
    module = getattr(cls, "WIDGET_MODULE", "Custom_Widgets." + name)

    # `format: md` parses the page as CommonMark instead of MDX. Docstrings are
    # prose written for Python, and prose like "setItems([{label, value}])"
    # is a JSX expression to MDX — it fails the build rather than rendering.
    out = ["---", "mdx:", "  format: md", "---", "", MARKER, "# %s" % name, ""]
    if shots.get("light"):
        out += ["![%s screenshot](/img/showcase/%s)" % (name, shots["light"]), ""]

    intro = summary
    if intro.lower().startswith(name.lower()):
        intro = intro[len(name):].lstrip(" -–—")
    out += ["`%s` — %s" % (name, intro or tooltip or "a Custom Widget."), ""]
    if detail:
        out += [detail, ""]
    out += ["---", ""]

    out += ["## Import", "", "```python", "from %s import %s" % (module, name),
            "```", ""]

    if getattr(cls, "WIDGET_DOM_XML", None):
        out += ["Also available from the **Qt Designer** palette — every property "
                "below is settable in Designer and saved into the `.ui` file.", ""]

    out += ["## Constructor", "", "```python", constructorSignature(cls),
            "```", ""]

    props = designerProperties(cls)
    if props:
        out += ["## Properties", "",
                "| Property | Type | Default |", "|---|---|---|"]
        for prop, kind, default in props:
            shown = "`%s`" % default if default not in ("", None) else "—"
            # Backticks are mandatory, not cosmetic: bare `Qt::TextFormat` is a
            # CommonMark autolink with a bad port, and `QFlags<Qt::…>` is a raw
            # HTML tag. Either one fails the Docusaurus build.
            out.append("| `%s` | `%s` | %s |" % (prop, kind, shown))
        out.append("")

    methods = publicMethods(cls)
    if methods:
        out += ["## Methods", "", "| Method | Description |", "|---|---|"]
        for signature, doc in methods:
            out.append("| `%s` | %s |" % (signature, doc or ""))
        out.append("")

    sigs = signalsOf(cls)
    if sigs:
        out += ["## Signals", "", "| Signal | Description |", "|---|---|"]
        described = {s.split("(")[0]: "" for s in sigs}
        for signature in sigs:
            out.append("| `%s` | %s |" % (signature,
                                          described.get(signature.split("(")[0], "")))
        out.append("")

    tokens = catalog.get("tokens_used") or []
    if tokens:
        out += ["## Theming", "",
                "Colours come from the design tokens, so they follow the active "
                "theme. Roles used: " + ", ".join("`%s`" % t for t in tokens) + ".",
                "", "See [Design tokens](../02-Theming/DesignTokens.md).", ""]

    if shots.get("dark"):
        out += ["### Dark theme", "",
                "![%s dark](/img/showcase/%s)" % (name, shots["dark"]), ""]

    example = exampleFor(name)
    if example:
        out += ["## Example", "",
                "A runnable demo ships with the library:", "",
                "```bash", "python %s" % example, "```", ""]

    out += ["---", "",
            "<!-- Generated by tools/gen_widget_docs.py from the widget's "
            "__catalog__, metaObject and module docstring. Edit the widget, "
            "then regenerate — hand edits here are overwritten. Remove the "
            "marker at the top of this file to take it over by hand. -->", ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true",
                        help="rewrite every generated page, not just missing ones")
    parser.add_argument("--only", nargs="*", default=None)
    parser.add_argument("--no-shots", action="store_true")
    parser.add_argument("--force", action="store_true",
                        help="overwrite hand-written pages too (dangerous)")
    args = parser.parse_args()

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from qtpy.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    os.makedirs(WIDGET_DOCS, exist_ok=True)
    written, skipped, failed, shot = [], [], [], 0

    for row in manifestRows():
        name = row["widget"]
        if args.only and name not in args.only:
            continue
        path = os.path.join(WIDGET_DOCS, name + ".md")
        # Docusaurus derives the doc id from the basename, so a generated .md
        # beside a hand-written .mdx is an id collision that fails the build.
        if os.path.exists(path[:-3] + ".mdx"):
            skipped.append(name)
            continue
        if os.path.exists(path):
            existing = open(path, encoding="utf-8").read()
            handwritten = MARKER not in existing
            if handwritten and not args.force:
                skipped.append(name)
                continue
            if not args.all and not args.only and not handwritten:
                skipped.append(name)
                continue

        try:
            cls = importWidget(name, row["module"])
        except Exception as exc:
            failed.append("%s (import: %s)" % (name, exc))
            continue
        if cls is None:
            failed.append("%s (class not found)" % name)
            continue

        from qtpy.QtWidgets import QWidget
        if not (isinstance(cls, type) and issubclass(cls, QWidget)):
            failed.append("%s (not a QWidget)" % name)
            continue

        shots = {}
        if not args.no_shots:
            slug = slugFor(name)
            for theme, key in (("light", "light"), ("dark", "dark")):
                existingShot = "%s%s.png" % (slug, "-dark" if theme == "dark" else "")
                if os.path.isfile(os.path.join(SHOTS, existingShot)):
                    shots[key] = existingShot
                    continue
                try:
                    produced = shoot(cls, slug, theme)
                except Exception as exc:
                    # One unrenderable widget must not abort a 120-page run.
                    failed.append("%s (shot %s: %s)" % (name, theme, exc))
                    produced = None
                if produced:
                    shots[key] = produced
                    shot += 1

        try:
            open(path, "w", encoding="utf-8").write(renderPage(cls, row, shots))
            written.append(name)
        except Exception as exc:
            failed.append("%s (render: %s)" % (name, exc))

    print("written %d, skipped %d (hand-written or current), screenshots %d"
          % (len(written), len(skipped), shot))
    if failed:
        print("FAILED %d:" % len(failed))
        for item in failed:
            print("   ", item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
