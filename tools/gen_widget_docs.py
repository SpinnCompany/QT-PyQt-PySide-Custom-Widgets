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
import time

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
    """A screenshot of an empty widget is worse than no screenshot.

    Counting distinct colours does not work: one antialiased hairline is
    enough to clear that bar, which is how a batch of pages ended up shipping
    plain grey rectangles. Judge by DOMINANCE instead — if the backdrop owns
    almost every pixel, there is nothing to look at.
    """
    counts = {}
    total = 0
    for y in range(0, image.height(), 2):
        for x in range(0, image.width(), 2):
            pixel = image.pixel(x, y)
            counts[pixel] = counts.get(pixel, 0) + 1
            total += 1
    if not total:
        return True
    # Applied to the widget's own rect, so this is close to "every pixel is the
    # same colour" — a real widget always breaks it with text or a border.
    return max(counts.values()) / float(total) >= 0.995


# --------------------------------------------------------------------------- #
# Demo content
#
# A container widget is empty until something is put in it, and an empty
# container photographs as a blank rectangle — which is exactly what a batch of
# these pages used to ship. WIDGET_DOM_XML defaults cover the simple painted
# widgets; everything below needs real data, so it gets real data.
#
# Keep the content plausible. These are the public documentation screenshots,
# and "Item 1 / Item 2 / Item 3" tells a reader nothing about what the widget
# is for.
# --------------------------------------------------------------------------- #
def _swatches(pairs):
    from qtpy.QtGui import QPixmap, QColor
    out = []
    for colour in pairs:
        pixmap = QPixmap(960, 600)
        pixmap.fill(QColor(colour))
        out.append(pixmap)
    return out


def _seedChatList(w):
    w.setConversations([
        {"name": "Ricky Smith", "preview": "YOU: Sending the file over now",
         "time": "1min ago", "online": True},
        {"name": "Lorri Warf", "preview": "Let's go on a date tomorrow",
         "time": "2min ago", "unread": 2, "online": True},
        {"name": "Judith Rodriguez", "preview": "See you on the call.",
         "time": "18min ago", "online": False},
        {"name": "Frances Swann", "preview": "Standup moved to 10:00",
         "time": "Jan 01", "muted": True, "online": False},
    ])
    w.setCurrentIndex(1)
    w.setMinimumSize(320, 320)


def _seedChatThread(w):
    # `side` is 'in'/'out'. Anything else silently renders as incoming.
    w.setSenderName("Ricky Smith")
    w.setMessages([
        {"kind": "date", "text": "YESTERDAY"},
        {"kind": "text", "side": "in", "text": "Hi! How are you?",
         "time": "11:00 AM", "reactions": [("Like", 2)]},
        {"kind": "text", "side": "out",
         "text": "Hey Ricky! Feeling great — how about you?",
         "time": "12:42 PM", "status": "read"},
        {"kind": "voice", "side": "in", "duration": "01:30", "time": "12:00 PM",
         "wave": "3,6,10,14,9,16,20,12,7,18,22,14,8,12,6,10,16,9,5,12"},
        {"kind": "text", "side": "out", "text": "That's a cool idea!",
         "time": "12:44 PM", "status": "delivered"},
    ])
    w.setMinimumSize(560, 460)


def _seedImageViewer(w):
    w.setImages(_swatches(("#f6a94b", "#7fc7f5", "#c58bf0")))
    w.setIndex(1)
    w.resize(720, 480)
    # __init__ hides it; the image rect is width-200 x height-150, so below
    # roughly 400x300 only the scrim and arrows draw and never the photo.
    w.show()


def _seedMediaGrid(w):
    w.columns = 3
    w.tileHeight = 84
    w.tileRadius = 14
    w.setPlaceholders([
        ("#f6a94b", "#b5541e"), ("#8fd66f", "#2f7d3e"), ("#7fc7f5", "#2b6fb0"),
        ("#c58bf0", "#6a34b0"), ("#f28b8b", "#b53b52"), ("#8ad9c8", "#2f8f86"),
    ])
    w.setMinimumSize(300, 200)


def _seedMiniBarChart(w):
    w.setData([42, 58, 35, 72, 66, 88, 54, 61, 79, 95, 48, 70], None,
              ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    w.highlightIndex(9)
    w.setMinimumSize(360, 180)


def _seedSparkline(w):
    w.setValues([12, 15, 13, 18, 16, 22, 20, 24, 21, 27, 25, 31])
    w.fillEnabled = True
    w.setMinimumSize(240, 72)


def _seedTimeline(w):
    w.setItems([
        {"title": "Order placed", "time": "09:12",
         "description": "Payment confirmed via Visa 4242"},
        {"title": "Packed at warehouse", "time": "11:40"},
        {"title": "Out for delivery", "time": "15:05", "color": "#f59e0b"},
        {"title": "Delivered", "time": "17:26",
         "description": "Left with the front desk"},
    ])
    w.setMinimumSize(320, 260)


def _seedEmptyState(w):
    w.setTitle("No invoices yet")
    w.setDescription("Create your first invoice and it will show up here.")
    w.setActionText("New invoice")
    w.setMinimumSize(320, 240)


def _seedCarousel(w):
    from qtpy.QtCore import Qt
    from qtpy.QtWidgets import QLabel
    for text in ("Welcome to Aurora", "Design faster with tokens",
                 "Ship with confidence"):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        w.addSlide(label)
    w.setCurrentIndex(1)
    w.setMinimumSize(360, 220)


def _seedWallpaper(w):
    from qtpy.QtGui import QColor
    # No public QPixmap setter — only a path or URL. The built-in three-stop
    # gradient fallback is the one thing that paints with zero assets.
    w.fallbackTop = QColor("#2b3550")
    w.fallbackMid = QColor("#4c4668")
    w.fallbackBottom = QColor("#1a1e30")
    w.setMinimumSize(400, 300)


def _chartPresentation(w, theme, title, xTitle, yTitle):
    """Presentation goes on LAST, and that ordering is load-bearing.

    Applying data re-runs the chart's theme manager, which resets the theme to
    "App Theme" and the axis titles to "X Axis"/"Y Axis" — so anything set
    before the data is silently thrown away. That is also why these shipped
    black: App Theme takes its colours from QCustomTheme, a different system
    from the design tokens, and it is dark when no theme JSON is loaded.
    """
    w.animationEnabled = False                   # else grab() catches an empty plot
    w.showToolbar = False
    w.showFooter = False
    w.chartTitle = title
    if xTitle:
        w.xAxisTitle = xTitle
    if yTitle:
        w.yAxisTitle = yTitle
    # theme goes ABSOLUTELY LAST. Setting a title re-runs the theme manager,
    # which resets to "App Theme" — so a theme set any earlier is discarded.
    # This is invisible in dark (App Theme is dark anyway) and is exactly why
    # the light shots stayed black while the dark ones looked right.
    w.theme = 2 if theme == "dark" else 1        # 0 = App Theme, 1 = Light


def _seedQtChart(w, theme):
    w.categoriesCsv = "Jan,Feb,Mar,Apr,May,Jun"
    w.seriesCsv = "Revenue=12,19,15,24,22,30;Costs=8,11,9,14,13,17"
    _chartPresentation(w, theme, "Revenue vs costs", "Month", "$k")
    # The host sizes itself from sizeHint, and with the toolbar hidden that
    # collapses to 68px — a plot area with nowhere to draw, which photographs
    # as a black sliver. Give it a real minimum instead.
    w.setMinimumSize(560, 320)


def _seedPieChart(w, theme):
    w.categoriesCsv = "Direct,Search,Social,Referral"
    w.seriesCsv = "Sessions=42,28,18,12"
    _chartPresentation(w, theme, "Traffic by source", None, None)
    w.setMinimumSize(460, 320)


#: seed(widget, theme) -> None. Theme matters wherever a widget has its own
#: notion of light/dark that the design tokens do not drive.
SEEDS = {
    "QCustomChatList": lambda w, t: _seedChatList(w),
    "QCustomChatThread": lambda w, t: _seedChatThread(w),
    "QCustomImageViewer": lambda w, t: _seedImageViewer(w),
    "QCustomMediaGrid": lambda w, t: _seedMediaGrid(w),
    "QCustomMiniBarChart": lambda w, t: _seedMiniBarChart(w),
    "QCustomSparkline": lambda w, t: _seedSparkline(w),
    "QCustomStepper": lambda w, t: (
        w.setSteps(["Account", "Profile", "Payment", "Confirm"]),
        w.setCurrentStep(2), w.setMinimumSize(440, 80)),
    "QCustomTimeline": lambda w, t: _seedTimeline(w),
    "QCustomWallpaper": lambda w, t: _seedWallpaper(w),
    "QCustomEmptyState": lambda w, t: _seedEmptyState(w),
    "QCustomCarousel": lambda w, t: _seedCarousel(w),
    "QCustomPagination": lambda w, t: (
        w.setPageCount(12), w.setCurrentPage(5), w.setMinimumSize(360, 40)),

    "QCustomLineChart": _seedQtChart,
    "QCustomAreaChart": _seedQtChart,
    "QCustomBarChart": _seedQtChart,
    "QCustomPieChart": _seedPieChart,

    # A widget whose whole job is to display a value photographs as a lie at
    # its default of 0 — an empty rating, a 0% ring, a counter reading "0".
    "QCustomRating": lambda w, t: setattr(w, "value", 4),
    "QCustomProgressRing": lambda w, t: w.setValue(68),
    "QCustomRoundProgressBar": lambda w, t: w.setValue(72),
    "QCustomNumberCounter": lambda w, t: w.reset(1250),
    "QCustomRadialGauge": lambda w, t: w.setValue(64),
    "QCustomTypewriterText": lambda w, t: w.skip(),
}

def _reassertChartTheme(w, theme):
    """Paint the chart from design tokens directly, after everything else.

    Going through the `theme` property does not survive: the chart's theme
    manager re-applies "App Theme" (which reads QCustomTheme, dark by default,
    not the design tokens) in response to broadcasts from other widgets alive
    in the process, and the property setter short-circuits on an unchanged
    value so it cannot even be re-asserted. Setting the QChart's brushes is
    the one thing nothing else overwrites.
    """
    from qtpy.QtGui import QBrush, QColor
    from Custom_Widgets.JSonStyles.tokens import DesignTokens

    # `w.chart` is a lazily-populated public attribute and is still None here;
    # the live QChart hangs off the QChartView child.
    from qtpy.QtCharts import QChartView
    chart = getattr(w, "_chart", None)
    if chart is None:
        views = w.findChildren(QChartView)
        chart = views[0].chart() if views else None
    if chart is None:
        print("  post-seed: no QChart found on %s" % type(w).__name__)
        return
    tokens = DesignTokens(theme=theme)
    surface = QColor(tokens.role("surface"))
    onSurface = QColor(tokens.role("on-surface"))
    grid = QColor(tokens.role("outline"))

    chart.setBackgroundBrush(QBrush(surface))
    chart.setPlotAreaBackgroundBrush(QBrush(surface))
    chart.setPlotAreaBackgroundVisible(True)
    chart.setTitleBrush(QBrush(onSurface))
    for axis in chart.axes():
        axis.setLabelsColor(onSurface)
        axis.setTitleBrush(QBrush(onSurface))
        axis.setGridLineColor(grid)
        axis.setLinePenColor(grid)
    legend = chart.legend()
    if legend is not None:
        legend.setLabelColor(onSurface)


#: post(widget, theme), applied after show + settle, immediately before the
#: grab. The QtCharts theme manager re-applies "App Theme" (dark) in response
#: to theme broadcasts from OTHER widgets alive in the same process — which is
#: why a chart shot in isolation came out light and the same chart in a full
#: run came out black. Re-asserting last is the only thing that survives.
POST_SEEDS = {
    "QCustomLineChart": _reassertChartTheme,
    "QCustomAreaChart": _reassertChartTheme,
    "QCustomBarChart": _reassertChartTheme,
    "QCustomPieChart": _reassertChartTheme,
}

#: Widgets that need wall-clock time before they have anything to show.
#: processEvents() alone does not advance an animation — no time passes.
SETTLE = {
    "QCustomLineChart": 1.2, "QCustomAreaChart": 1.2, "QCustomBarChart": 1.2,
    "QCustomPieChart": 1.2, "QCustomSpinner": 0.35, "QCustomArcLoader": 0.35,
    "QCustomPerlinLoader": 0.35, "QCustom3CirclesLoader": 0.35,
    "QCustomProgressIndicator": 0.35, "QCustomQProgressBar": 0.30,
}


def _backdrop(theme):
    """Card colour behind the widget: one step off `surface`, so a widget that
    paints its own surface still reads as a card rather than dissolving."""
    from Custom_Widgets.JSonStyles.tokens import DesignTokens
    return DesignTokens(theme=theme).role("surface-muted")


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

    seed = SEEDS.get(cls.__name__)
    if seed is not None:
        try:
            seed(widget, theme)
        except Exception as exc:
            print("  seed failed for %s: %s" % (cls.__name__, exc))

    host = QWidget()
    # The backdrop must follow the theme. A plain QWidget keeps the platform
    # palette's light window colour, so every "-dark" shot used to be a dark
    # widget on a light card — white legend text on #eee, invisible.
    host.setObjectName("shotHost")
    host.setStyleSheet("QWidget#shotHost { background: %s; }"
                       % _backdrop(theme))
    box = QVBoxLayout(host)
    box.setContentsMargins(16, 16, 16, 16)
    box.addWidget(widget)
    hint = widget.sizeHint()
    host.resize(max(180, hint.width() + 32), max(90, hint.height() + 32))
    host.show()
    host.ensurePolished()
    widget.ensurePolished()
    settle = SETTLE.get(cls.__name__, 0.0)
    if settle:
        deadline = time.time() + settle
        while time.time() < deadline:
            app.processEvents()
            time.sleep(0.01)
    post = POST_SEEDS.get(cls.__name__)
    if post is not None:
        try:
            post(widget, theme)
        except Exception as exc:
            print("  post-seed failed for %s: %s" % (cls.__name__, exc))
    for _ in range(4):
        app.processEvents()

    pixmap = host.grab()
    image = pixmap.toImage()
    # Judge emptiness on the WIDGET's own pixels, never the host's. A badge
    # legitimately occupies 3% of a padded card, so measuring the whole canvas
    # condemns every small widget as blank while passing a big empty one.
    own = widget.grab().toImage()
    if image.isNull() or own.isNull() or _isBlank(own):
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
    parser.add_argument("--reshoot", action="store_true",
                        help="re-capture screenshots that already exist")
    parser.add_argument("--force", action="store_true",
                        help="overwrite hand-written pages too (dangerous)")
    args = parser.parse_args()

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from qtpy.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    os.makedirs(WIDGET_DOCS, exist_ok=True)
    written, skipped, failed, stale, shot = [], [], [], [], 0

    for row in manifestRows():
        name = row["widget"]
        if args.only and name not in args.only:
            continue
        path = os.path.join(WIDGET_DOCS, name + ".md")
        # A hand-written page keeps its prose but still shows a screenshot, so
        # "skip" means skip the WRITE, not the shot — otherwise a reshoot
        # leaves those images stale forever, which is how the dark variants
        # stayed on a light backdrop.
        writePage = True
        # Docusaurus derives the doc id from the basename, so a generated .md
        # beside a hand-written .mdx is an id collision that fails the build.
        if os.path.exists(path[:-3] + ".mdx"):
            writePage = False
        elif os.path.exists(path):
            existing = open(path, encoding="utf-8").read()
            handwritten = MARKER not in existing
            if handwritten and not args.force:
                writePage = False
            elif not args.all and not args.only and not handwritten:
                writePage = False
        if not writePage:
            skipped.append(name)
            if not args.reshoot:
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
                if not args.reshoot and os.path.isfile(
                        os.path.join(SHOTS, existingShot)):
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
                elif os.path.isfile(os.path.join(SHOTS, existingShot)):
                    # Nothing rendered, but an old file is still on disk and
                    # pages will keep pointing at it. Never silently keep it.
                    stale.append(existingShot)
                    shots[key] = existingShot

        if not writePage:
            continue
        try:
            open(path, "w", encoding="utf-8").write(renderPage(cls, row, shots))
            written.append(name)
        except Exception as exc:
            failed.append("%s (render: %s)" % (name, exc))

    if stale:
        print("STALE (nothing rendered, old image kept) %d:" % len(stale))
        for item in sorted(set(stale)):
            print("    %s" % item)
    print("written %d, skipped %d (hand-written or current), screenshots %d"
          % (len(written), len(skipped), shot))
    if failed:
        print("FAILED %d:" % len(failed))
        for item in failed:
            print("   ", item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
