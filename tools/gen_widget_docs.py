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
    # Left on App Theme (0) deliberately: it now reads the design tokens, so
    # this shoots the charts exactly as a token-themed app renders them.


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


def _iconPath(name):
    from Custom_Widgets._resources import packageDir
    return os.path.join(packageDir(), "components", "icons", name)


def _seedQSlider(w, theme):
    from qtpy.QtCore import Qt
    w.setOrientation(Qt.Horizontal)
    w.setRange(0, 100)
    w.setValue(64)
    w.setMinimumWidth(260)


def _seedStatCard(w, theme):
    w.setLabel("Monthly recurring revenue")
    w.setValue("$48,320")
    w.setDelta("12.4%", "up")
    w.setCaption("vs last month")
    w.setMinimumSize(220, 110)


def _seedDataTable(w, theme):
    w.setColumns([
        {"key": "name", "title": "Customer", "renderer": "twoline",
         "subtitleKey": "email"},
        {"key": "plan", "title": "Plan"},
        {"key": "status", "title": "Status", "renderer": "status",
         "colorMap": {"Active": "#22c55e", "Trialing": "#f59e0b",
                      "Churned": "#ef4444"}},
        {"key": "mrr", "title": "MRR", "type": "number", "renderer": "currency"},
    ])
    w.setData([
        {"name": "Acme Corp", "email": "billing@acme.io", "plan": "Enterprise",
         "status": "Active", "mrr": 1290},
        {"name": "Globex", "email": "ops@globex.com", "plan": "Pro",
         "status": "Trialing", "mrr": 240},
        {"name": "Initech", "email": "admin@initech.co", "plan": "Starter",
         "status": "Churned", "mrr": 0},
        {"name": "Umbrella Ltd", "email": "ap@umbrella.co.uk", "plan": "Pro",
         "status": "Active", "mrr": 480},
    ])
    w.setSelectable(True)
    w.setMinimumSize(640, 260)


def _seedChipGroup(w, theme):
    w.setChips(["Design", "Engineering", "Marketing", "Support"])
    w.setMinimumSize(360, 40)


def _seedTagEdit(w, theme):
    w.setTagSuggestions(["python", "qt", "pyside6", "pyqt5", "widgets"])
    w.setTags(["python", "qt", "pyside6", "widgets"])
    w.setMinimumSize(320, 60)


def _seedTrendChip(w, theme):
    w.setVariant("soft")
    # setValue LAST: it derives the direction from the sign of the number and
    # overwrites anything setDirection() did.
    w.setValue(12.4, "+12.4%")
    w.setMinimumSize(96, 30)


def _seedFeaturedIcon(w, theme):
    from qtpy.QtGui import QIcon
    w.setIcon(QIcon(_iconPath("rocket.png")))
    w.variant = "tinted"
    w.shape = "rounded"
    w.sizeVariant = "lg"


def _seedActionButton(w, theme):
    from qtpy.QtGui import QIcon
    w.icon = QIcon(_iconPath("paid.png"))
    w.caption = "Transfer"


def _seedListRow(w, theme):
    w.setIconText("AM")
    w.setTitle("Amara Mensah")
    w.setSubtitle("Product designer")
    w.setValue("$1,290")
    w.setMeta("2 min ago")
    w.setMinimumSize(380, 56)


def _seedTabWidget(w, theme):
    from qtpy.QtWidgets import QLabel
    w.addTab(QLabel("  Revenue is up 12.4% this quarter."), "Overview")
    w.addTab(QLabel("  4,182 weekly active users."), "Analytics")
    w.addTab(QLabel("  Workspace preferences."), "Settings")
    w.tabStyle = "underline"
    w.setMinimumSize(420, 220)


def _seedTreeWidget(w, theme):
    w.setItems([
        {"text": "src", "expanded": True, "children": [
            {"text": "main.py"},
            {"text": "widgets", "expanded": True, "children": [
                {"text": "button.py"}, {"text": "card.py"}]}]},
        {"text": "tests", "children": [{"text": "test_button.py"}]},
        {"text": "README.md"},
    ])
    w.setMinimumSize(300, 220)


def _seedNodeGraph(w, theme):
    # `rows` entries must be dicts — a tuple crashes inside paintEvent.
    w.setGraph({"nodes": [
        {"nid": "load", "title": "Load CSV", "x": 30, "y": 40, "w": 190,
         "h": 110, "accent": "#38bdf8", "outputs": ["data"],
         "rows": [{"label": "rows", "value": "12,480"},
                  {"label": "columns", "value": "9"}]},
        {"nid": "clean", "title": "Clean", "x": 290, "y": 40, "w": 190,
         "h": 110, "accent": "#f2a63b", "inputs": ["in"], "outputs": ["out"],
         "rows": [{"label": "dropped", "value": "126"},
                  {"label": "nulls", "value": "0"}]},
        {"nid": "train", "title": "Train model", "x": 550, "y": 40, "w": 190,
         "h": 110, "accent": "#a78bfa", "inputs": ["x"],
         "rows": [{"label": "accuracy", "value": "0.94", "dot": "#22c55e"}]},
    ], "edges": [
        {"src": "load", "srcPort": 0, "dst": "clean", "dstPort": 0},
        {"src": "clean", "srcPort": 0, "dst": "train", "dstPort": 0},
    ]})
    w.setMinimumSize(780, 220)


def _seedBreadcrumbs(w, theme):
    w.setItems([("Home", "/"), ("Projects", "/projects"),
                ("Atlas", "/projects/atlas"),
                ("Settings", "/projects/atlas/settings")])
    w.setMinimumSize(360, 28)


def _seedAccordion(w, theme):
    from qtpy.QtWidgets import QLabel
    w.addSection("Shipping address", QLabel("221B Baker Street, London NW1 6XE"))
    w.addSection("Payment method", QLabel("Visa ending 4242, expires 08/28"))
    w.addSection("Delivery notes", QLabel("Leave with the concierge."))
    w.setExpanded(0, True, animate=False)   # no-op unless the section exists
    w.setMinimumSize(380, 180)


def _seedAvatarGroup(w, theme):
    w.setAvatars(["Amara Mensah", "Ben Ortiz", "Chidi Okafor", "Dana Levy",
                  "Eli Novak", "Farah Aziz"])
    w.setMinimumSize(190, 40)


def _seedButtonGroup(w, theme):
    w.setButtons([("Day", 0), ("Week", 1), ("Month", 2)])
    # setButtons rebuilds the internal QButtonGroup, so a selection set before
    # it is silently discarded.
    w.setSelectedId(1)
    w.setMinimumSize(140, 120)


def _seedSplitter(w, theme):
    from qtpy.QtWidgets import QLabel
    w.addWidget(QLabel("  Navigator"))
    w.addWidget(QLabel("  Editor"))
    w.setSizes([130, 210])
    w.setMinimumSize(340, 160)


def _seedReactionBar(w, theme):
    w.setReactions([("\U0001f44d", 12), ("\U0001f525", 4), ("\U0001f389", 2)])
    w.setMinimumSize(220, 34)


def _seedHeatmap(w, theme):
    w.setMode("grid")
    w.setValues([[2, 5, 9, 7, 4, 1, 0], [3, 8, 6, 9, 5, 2, 1],
                 [1, 4, 7, 8, 9, 3, 2], [0, 2, 5, 6, 7, 4, 1],
                 [4, 6, 9, 9, 8, 5, 2], [1, 3, 4, 6, 5, 2, 0]])
    w.setLabels(row_labels=["9am", "11am", "1pm", "3pm", "5pm", "7pm"],
                col_labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    # The heatmap paints its own palette rather than reading the tokens, so the
    # theme has to be pushed in by hand or the dark shot duplicates the light.
    if theme == "dark":
        w.setColors("#1e3a8a", "#60a5fa", "#1e293b")
    else:
        w.setColors("#dbeafe", "#1d4ed8", "#f1f5f9")
    w.setMinimumSize(360, 220)


def _seedRulerPicker(w, theme):
    w.setRange(40.0, 120.0)
    w.setUnit("kg")
    w.setValue(72.5)                      # clamps to the range, so set it after
    w.setMinimumSize(360, 120)


def _seedRadialLines(w, theme):
    w.setLabels(["Speed", "Power", "Range", "Comfort", "Safety", "Price"])
    w.setSeries([("Model A", [8, 6, 7, 9, 5, 6]),
                 ("Model B", [5, 9, 6, 4, 8, 7])])
    w.setMinimumSize(320, 300)


def _seedCodeEditor(w, theme):
    w.setLang("python")
    # Its own theme set, independent of the design tokens.
    w.setTheme("one-dark" if theme == "dark" else "one-light")
    w.editor.setPlainText(
        'def greet(name):\n'
        '    # a friendly hello\n'
        '    return f"Hello, {name}!"\n\n\n'
        'print(greet("World"))')
    w.setMinimumSize(440, 200)


def _seedChatBubble(w, theme):
    w.setSender("Amara Mensah")
    w.setText("Shipped the new dashboard - can you review the charts "
              "before standup?")
    w.setTime("09:41")
    w.setMinimumSize(340, 90)


def _seedChatInput(w, theme):
    w.placeholder = "Write a message..."
    w.setText("Sounds good - shipping it today")
    w.setMinimumSize(520, 64)


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

    # Legacy widgets whose defaults photograph badly: a vertical unstyled
    # slider, and a bar sitting at zero.
    "QCustomQSlider": _seedQSlider,
    "QCustomQProgressBar": lambda w, t: w.setFixedWidth(260),

    "QCustomStatCard": _seedStatCard,
    "QCustomDataTable": _seedDataTable,
    "QTagEdit": _seedTagEdit,
    "QCustomTrendChip": _seedTrendChip,
    "QCustomFeaturedIcon": _seedFeaturedIcon,
    "QCustomActionButton": _seedActionButton,
    "QCustomListRow": _seedListRow,
    "QCustomTabWidget": _seedTabWidget,
    "QCustomTreeWidget": _seedTreeWidget,
    "QCustomNodeGraph": _seedNodeGraph,
    "QCustomSkeleton": lambda w, t: (setattr(w, "shape", "rect"),
                                     w.setMinimumSize(240, 64)),
    "QCustomBreadcrumbs": _seedBreadcrumbs,
    "QCustomAccordion": _seedAccordion,
    "QCustomAvatarGroup": _seedAvatarGroup,
    "QCustomButtonGroup": _seedButtonGroup,
    "QCustomSegmentedControl": lambda w, t: (
        w.setSegments(["Day", "Week", "Month", "Year"]),
        w.setCurrentIndex(1), w.setMinimumSize(320, 34)),
    "QCustomSplitter": _seedSplitter,
    "QCustomChatDivider": lambda w, t: (setattr(w, "variant", "pill"),
                                        setattr(w, "text", "YESTERDAY"),
                                        w.setMinimumSize(420, 28)),
    "QCustomPageDots": lambda w, t: (w.setCount(5), w.setActiveIndex(2),
                                     w.setMinimumSize(120, 20)),
    "QCustomReactionBar": _seedReactionBar,
    "QCustomHeatmap": _seedHeatmap,
    "QCustomRulerPicker": _seedRulerPicker,
    "QCustomRadialLines": _seedRadialLines,
    "QCustomCodeEditor": _seedCodeEditor,
    "QCustomChatBubble": _seedChatBubble,
    "QCustomChatInput": _seedChatInput,
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
POST_SEEDS = {}

#: Widgets whose __init__ takes required arguments. Without an entry here the
#: bare `cls()` raises, shoot() returns None and the widget silently has no
#: screenshot at all — which is how QCustomChip went undocumented.
def _hostedParent(width=420, height=260):
    """A shown parent for widgets that position themselves against one.

    Kept alive on the function so the C++ object outlives the call; several of
    these dereference parent().mapToGlobal() during construction or showEvent.
    """
    from qtpy.QtWidgets import QWidget
    parent = QWidget()
    parent.resize(width, height)
    parent.show()
    _hostedParent.keep = getattr(_hostedParent, "keep", [])
    _hostedParent.keep.append(parent)
    return parent


CONSTRUCTORS = {
    "QCustomChip": lambda cls: cls("Design", closable=True, selectable=True),
    "QCustomCommandPalette": lambda cls: cls(_hostedParent()),
    "QCustomDrawer": lambda cls: cls(_hostedParent()),
    "QCustomEmbeddedWindow": lambda cls: cls(_hostedParent()),
    # Both take a `target` they anchor to, and dereference it during
    # construction — parent alone is not enough.
    "QCustomEmojiPicker": lambda cls: (lambda p: cls(p, target=p))(_hostedParent()),
    "QCustomQToolTip": lambda cls: (lambda p: cls("Saved to your workspace",
                                                  parent=p, target=p))(_hostedParent()),
    "QCustomToast": lambda cls: cls(_hostedParent(), "Invoice #10428 was paid"),
}

#: Widgets that need wall-clock time before they have anything to show.
#: processEvents() alone does not advance an animation — no time passes.
SETTLE = {
    "QCustomLineChart": 1.2, "QCustomAreaChart": 1.2, "QCustomBarChart": 1.2,
    "QCustomPieChart": 1.2, "QCustomSpinner": 0.35, "QCustomArcLoader": 0.35,
    "QCustomPerlinLoader": 0.35, "QCustom3CirclesLoader": 0.35,
    "QCustomProgressIndicator": 0.35, "QCustomQProgressBar": 0.30,
    # QCustomFlowLayout debounces its reflow on a 10ms timer, so without real
    # time passing every child keeps its default 640x480 geometry and paints
    # on top of everything else.
    # The reflow is also ANIMATED, so it needs long enough to land, not
    # just long enough to start.
    "QTagEdit": 0.70, "QCustomChip": 0.70, "QCustomChipGroup": 0.70,
}


# --------------------------------------------------------------------------- #
# Popups
#
# A drawer, toast, tooltip, command palette, modal or embedded window renders
# NOTHING inside a QVBoxLayout: it positions itself over a parent window and
# animates in. Dropped into the normal harness they photographed as blank
# rectangles, so they simply had no screenshot at all.
#
# These are shot differently: build a themed parent that stands in for an app
# window, show the popup over it, let the entry animation finish in real time,
# then grab the PARENT — except the tooltip, which is a genuine top-level
# window (Qt.Popup|Qt.Tool) and is not inside its parent's grab at all.
# --------------------------------------------------------------------------- #
def _popupLabels(theme, texts):
    """Labels styled for the popup surface.

    Only the panel itself gets a token colour rule; children do not inherit it,
    so plain QLabels come out near-invisible pale grey on white.
    """
    from qtpy.QtWidgets import QLabel
    from Custom_Widgets.JSonStyles.tokens import DesignTokens
    colour = DesignTokens(theme=theme).role("on-surface")
    out = []
    for text in texts:
        label = QLabel(text)
        label.setStyleSheet("color: %s;" % colour)
        out.append(label)
    return out


def _popupDrawer(cls, parent, theme):
    widget = cls(parent, side="left", size=260)
    for label in _popupLabels(theme, ("Dashboard", "Projects", "Team members",
                                      "Billing & plans", "Settings")):
        widget.addWidget(label)
    widget.contentLayout().addStretch(1)
    widget.open()                      # the method is open(), not openDrawer()
    return widget


def _popupToast(cls, parent, theme):
    # duration=0 disables the dismiss timer. With the default 4000 the toast is
    # gone before the grab and the parent photographs completely empty.
    widget = cls(parent, "Invoice #10428 was paid.", variant="success",
                 title="Payment received", duration=0, position="top-right")
    widget.showToast()
    return widget


def _popupToolTip(cls, parent, theme):
    from qtpy.QtWidgets import QPushButton
    button = QPushButton("Export", parent)
    button.move(24, 24)
    button.show()
    # duration must be NEGATIVE: the guard is `if duration >= 0`, so 0 still
    # arms the auto-close timer. target is required, not optional.
    widget = cls("Exports the last 30 days as CSV", parent=parent,
                 target=button, duration=-1, tailPosition="top-center")
    widget.show()
    return widget


def _popupCommandPalette(cls, parent, theme):
    widget = cls(parent)
    widget.setCommands([                       # must precede open()
        {"id": "new", "title": "New Project",
         "subtitle": "Create an empty workspace", "shortcut": "Ctrl+N"},
        {"id": "open", "title": "Open Recent...", "shortcut": "Ctrl+O"},
        {"id": "theme", "title": "Toggle Dark Theme"},
        {"id": "export", "title": "Export as PDF"},
        {"id": "settings", "title": "Open Settings", "shortcut": "Ctrl+,"},
    ])
    widget.open()
    return widget


def _popupEmbeddedWindow(cls, parent, theme):
    from Custom_Widgets.JSonStyles.tokens import DesignTokens
    tokens = DesignTokens(theme=theme)
    # pos= is mandatory: pos=None picks random.randint(0, parent.width()-285)
    # and raises outright on a parent narrower than 285.
    widget = cls(parent, pos=(16, 16), title="Render Queue", headerHeight=28,
                 animationDuration=400)
    # No token QSS exists for this widget, so untouched it paints transparent.
    widget.setStyleSheet(
        "QCustomEmbeddedWindow { background-color: %s; border: 1px solid %s;"
        " border-radius: 10px; }"
        " #header { background-color: %s; }"
        " QLabel { color: %s; }"
        % (tokens.role("surface"), tokens.role("outline"),
           tokens.role("surface-muted"), tokens.role("on-surface")))
    for label in _popupLabels(theme, ("3 jobs queued\nEstimated time 4m 12s",)):
        widget.addWidget(label)
    widget.show()
    return widget


def _popupContainerModal(cls, parent, theme):
    """QCustomModal — a dialog hosted inside its parent, not the notification
    namespace. Different class, different API: setTitle/addContent/showModal."""
    widget = cls(parent)
    widget.setTitle("Delete this project?")
    widget.clearContent()          # else the shipped placeholder text shows too
    for label in _popupLabels(theme, (
            "Everything in aurora-deck will be removed.\nThis cannot be undone.",)):
        label.setWordWrap(True)
        widget.addContent(label)
    widget.showModal()
    return widget


def _popupModal(cls, parent, theme):
    """QCustomModal / QCustomModals — position= is mandatory.

    With position=None showEvent never registers with the manager, so nothing
    is placed and nothing animates. Duration is left unset on purpose: any
    positive value arms the auto-close timer and the grab catches an empty
    parent.
    """
    factory = getattr(cls, "SuccessModal", cls)
    widget = factory(title="Deployment complete",
                     description="aurora-deck v2.4.1 is live on production.",
                     parent=parent, position="center-center", isClosable=True)
    widget.show()
    return widget


def _anchorButton(parent, text="Export"):
    from qtpy.QtWidgets import QPushButton
    button = QPushButton(text, parent)
    button.move(24, 24)
    button.show()
    return button


def _popupTipOverlay(cls, parent, theme):
    # duration must be NEGATIVE; the guard is `>= 0`, so 0 still auto-closes.
    widget = cls(title="Keyboard shortcuts",
                 description="Press Ctrl+K to open the command palette.",
                 target=_anchorButton(parent, "Help"), parent=parent,
                 isClosable=True, duration=-1, tailPosition="top-center")
    widget.show()
    return widget


def _popupEmojiPicker(cls, parent, theme):
    widget = cls(parent, target=_anchorButton(parent, "React"))
    widget.show()
    return widget


def _popupQDialog(cls, parent, theme):
    widget = cls(parent, title="Discard changes?",
                 description="Your edits to aurora-deck have not been saved.",
                 yesButtonText="Discard", cancelButtonText="Keep editing",
                 animationDuration=200, position="center")
    widget.show()
    return widget


#: name -> (build(cls, parent, theme), parentSize, settle, grabTarget)
POPUPS = {
    "QCustomDrawer": (_popupDrawer, (520, 360), 0.45, "parent"),
    "QCustomToast": (_popupToast, (420, 220), 0.35, "parent"),
    "QCustomQToolTip": (_popupToolTip, (420, 220), 0.75, "widget"),
    "QCustomCommandPalette": (_popupCommandPalette, (700, 460), 0.40, "parent"),
    "QCustomEmbeddedWindow": (_popupEmbeddedWindow, (360, 220), 0.65, "parent"),
    "QCustomModal": (_popupContainerModal, (560, 360), 0.55, "parent"),
    "QCustomModals": (_popupModal, (560, 360), 0.55, "parent"),
    "QCustomTipOverlay": (_popupTipOverlay, (420, 220), 0.75, "widget"),
    "QCustomEmojiPicker": (_popupEmojiPicker, (460, 460), 0.75, "widget"),
    # Top-level like the tooltip: the parent grab catches only its blur.
    "QCustomQDialog": (_popupQDialog, (560, 360), 0.55, "widget"),
}


def shootPopup(cls, slug, theme):
    """Render an overlay widget over a stand-in app window."""
    from qtpy.QtWidgets import QApplication, QWidget
    from Custom_Widgets.JSonStyles.tokens import applyDesignTokens

    app = QApplication.instance()
    # Chrome FIRST: setStyleSheet replaces the whole sheet, and
    # applyDesignTokens appends its marked block to whatever is already there.
    app.setStyleSheet(_chromeQss(theme))
    applyDesignTokens(app, theme=theme)
    build, size, settle, grabTarget = POPUPS[cls.__name__]

    parent = QWidget()
    parent.setObjectName("popupHost")
    parent.setStyleSheet("QWidget#popupHost { background: %s; }"
                         % _backdrop(theme))
    parent.resize(*size)
    parent.show()
    try:
        widget = build(cls, parent, theme)
    except Exception as exc:
        print("  popup build failed for %s: %s" % (cls.__name__, exc))
        return None

    _polishDeep(parent)
    _polishDeep(widget)
    deadline = time.time() + settle
    while time.time() < deadline:
        app.processEvents()
        time.sleep(0.01)

    subject = widget if grabTarget == "widget" else parent
    pixmap = subject.grab()
    image = pixmap.toImage()
    if image.isNull() or _isBlank(image):
        return None
    name = "%s%s.png" % (slug, "-dark" if theme == "dark" else "")
    os.makedirs(SHOTS, exist_ok=True)
    pixmap.save(os.path.join(SHOTS, name))
    parent.hide()
    return name


#: Hand-written pages reference these older filenames. Writing the current
#: image under both names keeps those pages current instead of leaving them
#: pointing at a screenshot nothing regenerates.
LEGACY_SLUGS = {"qslider": "slider", "qprogressbar": "progressbar"}


def _saveAliases(pixmap, slug, theme):
    alias = LEGACY_SLUGS.get(slug)
    if not alias:
        return
    pixmap.save(os.path.join(
        SHOTS, "%s%s.png" % (alias, "-dark" if theme == "dark" else "")))


def _chromeQss(theme):
    """Theme the STANDARD Qt controls these widgets embed.

    The token QSS styles the library's own widgets. Anything built out of a
    plain QScrollArea, QLabel, QPushButton or QLineEdit falls back to the
    platform style, so a themed widget photographed on a themed page still had
    raw Fusion grey inside it — and looked identical in light and dark.

    Deliberately NOT a blanket `QWidget { ... }` rule: that strips native
    styling off every input and turns a bare QLineEdit into an invisible black
    box. Each control is named explicitly.
    """
    from Custom_Widgets.JSonStyles.tokens import DesignTokens
    t = DesignTokens(theme=theme)
    r = t.role
    return """
        QScrollArea, QAbstractScrollArea {
            background: %(surface)s; border: none;
        }
        QScrollArea > QWidget > QWidget { background: %(surface)s; }
        QLabel { background: transparent; color: %(on_surface)s; }
        QPushButton {
            background: %(secondary)s; color: %(on_secondary)s;
            border: 1px solid %(outline)s; border-radius: 6px;
            padding: 5px 12px;
        }
        QPushButton:hover { background: %(secondary_hover)s; }
        QLineEdit, QPlainTextEdit, QTextEdit, QSpinBox, QComboBox {
            background: %(surface)s; color: %(on_surface)s;
            border: 1px solid %(outline)s; border-radius: 6px;
            padding: 4px 8px;
            selection-background-color: %(primary)s;
            selection-color: %(on_primary)s;
        }
        QDialog { background: %(surface)s; color: %(on_surface)s; }
        /* Direct children only: a QDialog's title bar and button row are plain
           QWidgets that otherwise keep the platform window colour. Scoped to
           `>` so it cannot reach the inputs styled by type above. */
        QDialog > QWidget { background: %(surface)s; }
        QHeaderView::section {
            background: %(surface_muted)s; color: %(on_surface)s;
            border: none; padding: 6px;
        }
        QScrollBar:vertical, QScrollBar:horizontal {
            background: transparent; width: 8px; height: 8px;
        }
        QScrollBar::handle {
            background: %(outline)s; border-radius: 4px; min-height: 24px;
        }
        QScrollBar::add-line, QScrollBar::sub-line { height: 0; width: 0; }
        QToolTip {
            background: %(surface)s; color: %(on_surface)s;
            border: 1px solid %(outline)s;
        }
    """ % {"surface": r("surface"), "surface_muted": r("surface-muted"),
           "on_surface": r("on-surface"), "outline": r("outline"),
           "secondary": r("secondary"), "secondary_hover": r("secondary-hover"),
           "on_secondary": r("on-secondary"), "primary": r("primary"),
           "on_primary": r("on-primary")}


def _polishDeep(widget):
    """Polish the whole tree. ensurePolished() on the parent does not descend,
    so children keep the platform style until they are polished themselves."""
    from qtpy.QtWidgets import QWidget
    widget.ensurePolished()
    for child in widget.findChildren(QWidget):
        child.ensurePolished()


def _backdrop(theme):
    """Card colour behind the widget: one step off `surface`, so a widget that
    paints its own surface still reads as a card rather than dissolving."""
    from Custom_Widgets.JSonStyles.tokens import DesignTokens
    return DesignTokens(theme=theme).role("surface-muted")


def shoot(cls, slug, theme):
    """Render one widget to static/img/showcase/. Returns the filename or None."""
    from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout
    from Custom_Widgets.JSonStyles.tokens import applyDesignTokens

    if cls.__name__ in POPUPS:
        return shootPopup(cls, slug, theme)

    app = QApplication.instance()
    app.setStyleSheet(_chromeQss(theme))     # before the tokens; see shootPopup
    applyDesignTokens(app, theme=theme)
    # Not everything the manifest lists is a QWidget — generated Ui_* form
    # classes turn up too, and QBoxLayout.addWidget rejects them outright.
    if not (isinstance(cls, type) and issubclass(cls, QWidget)):
        return None
    build = CONSTRUCTORS.get(cls.__name__)
    try:
        widget = build(cls) if build else cls()
    except Exception as exc:
        print("  cannot construct %s: %s" % (cls.__name__, exc))
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
    _polishDeep(host)
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
    _saveAliases(pixmap, slug, theme)
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
