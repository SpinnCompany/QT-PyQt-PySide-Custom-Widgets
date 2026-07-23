"""AURORA - Command Deck
=========================

A creative, self-contained showcase for the QT-PyQt-PySide Custom Widgets
design-token widget set. It stages a fictional aurora-forecasting network's
"command deck": live station telemetry, a rolling forecast carousel, region
filters and headline stats -- all styled purely through ``applyDesignTokens``
with a live light / dark toggle.

Run:
    python main.py               # normal, interactive
    python main.py --shots DIR   # render, write light+dark PNGs to DIR, keep open

No .ui file, no .qrc, no JSON -- everything is code + design tokens.
"""

import sys
import os
import argparse
from functools import partial

from PySide6 import QtWidgets, QtCore, QtGui

from Custom_Widgets.JSonStyles.tokens import applyDesignTokens, DesignTokens
from Custom_Widgets.QCustomKbd import QCustomKbd
from Custom_Widgets.QCustomSplitter import QCustomSplitter
from Custom_Widgets.QCustomCarousel import QCustomCarousel
from Custom_Widgets.QCustomChip import QCustomChipGroup
from Custom_Widgets.QCustomStatCard import QCustomStatCard
from Custom_Widgets.QCustomCard import QCustomCard
from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn


# --------------------------------------------------------------------------- #
# Fictional data model -- a network of aurora ground stations.
# --------------------------------------------------------------------------- #
STATIONS = [
    {"call": "Tromsø-1",   "region": "Arctic",    "kp": 6.2, "clouds": 12, "status": "LIVE"},
    {"call": "Fairbanks-A",     "region": "Arctic",    "kp": 5.8, "clouds": 40, "status": "LIVE"},
    {"call": "Reykjavík",  "region": "Atlantic",  "kp": 4.9, "clouds": 65, "status": "HAZY"},
    {"call": "Yellowknife",     "region": "Arctic",    "kp": 6.7, "clouds": 8,  "status": "LIVE"},
    {"call": "Murmansk",        "region": "Arctic",    "kp": 5.1, "clouds": 30, "status": "LIVE"},
    {"call": "Dunedin",         "region": "Antarctic", "kp": 3.4, "clouds": 78, "status": "DARK"},
    {"call": "Ushuaia",         "region": "Antarctic", "kp": 4.2, "clouds": 55, "status": "HAZY"},
    {"call": "Kiruna",          "region": "Arctic",    "kp": 6.0, "clouds": 20, "status": "LIVE"},
    {"call": "Nuuk",            "region": "Atlantic",  "kp": 5.5, "clouds": 45, "status": "HAZY"},
    {"call": "Hobart",          "region": "Antarctic", "kp": 3.9, "clouds": 70, "status": "DARK"},
    {"call": "Abisko",          "region": "Arctic",    "kp": 6.4, "clouds": 5,  "status": "LIVE"},
    {"call": "Sodankylä",  "region": "Arctic",    "kp": 5.9, "clouds": 25, "status": "LIVE"},
]

FORECASTS = [
    ("Tonight", "Substorm onset expected 21:40 UTC. Kp climbing to 6+ across the "
                "Arctic belt -- corona overhead at Tromsø and Abisko."),
    ("Tomorrow", "Coronal hole stream arrives. Sustained Kp 5-6 for 18h. "
                 "Atlantic stations clearing after midnight."),
    ("72 Hours", "Quieting trend. Kp settling to 3-4. Antarctic sites regain the "
                 "edge as the southern season deepens."),
]


def _region_of(call):
    for s in STATIONS:
        if s["call"] == call:
            return s["region"]
    return "Arctic"


# --------------------------------------------------------------------------- #
# Base chrome -- the surrounding window styling, derived from the same tokens
# so it tracks the light/dark toggle. Everything else is styled by
# applyDesignTokens automatically.
# --------------------------------------------------------------------------- #
def base_chrome(tokens):
    surface = tokens.role("surface")
    muted = tokens.role("surface-muted")
    on_surface = tokens.role("on-surface")
    outline = tokens.role("outline")
    primary = tokens.role("primary")
    return """
        QWidget#deckRoot {{ background: {muted}; }}
        QWidget {{ color: {on_surface}; font-family: 'Segoe UI', 'Inter', sans-serif; }}

        QFrame#hero {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {primary}, stop:1 {muted});
            border: 1px solid {outline};
            border-radius: 16px;
        }}
        QLabel#heroTitle {{ font-size: 26px; font-weight: 800; letter-spacing: 1px; }}
        QLabel#heroSub   {{ font-size: 13px; color: {on_surface}; opacity: 0.85; }}
        QLabel#sectionTitle {{ font-size: 12px; font-weight: 700;
                               letter-spacing: 2px; color: {primary}; }}

        QLineEdit {{
            background: {surface}; color: {on_surface};
            border: 1px solid {outline}; border-radius: 8px;
            padding: 6px 10px; selection-background-color: {primary};
        }}
        QLineEdit:focus {{ border: 1px solid {primary}; }}

        QFrame#panel {{
            background: {surface}; border: 1px solid {outline}; border-radius: 14px;
        }}
        QLabel#forecastWhen {{ font-size: 18px; font-weight: 700; color: {primary}; }}
        QLabel#forecastBody {{ font-size: 13px; line-height: 1.5; }}
        QLabel#footNote {{ font-size: 11px; color: {on_surface}; opacity: 0.6; }}
    """.format(surface=surface, muted=muted, on_surface=on_surface,
               outline=outline, primary=primary)


def apply_theme(app, theme):
    tokens = DesignTokens(theme=theme)
    app.setStyleSheet(base_chrome(tokens))     # base chrome first ...
    applyDesignTokens(app, tokens=tokens)      # ... tokens append their marked block
    return tokens


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #
def section_label(text):
    lbl = QtWidgets.QLabel(text)
    lbl.setObjectName("sectionTitle")
    return lbl


def forecast_slide(when, body):
    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)
    lay.setContentsMargins(18, 16, 18, 16)
    lay.setSpacing(8)
    t = QtWidgets.QLabel(when)
    t.setObjectName("forecastWhen")
    b = QtWidgets.QLabel(body)
    b.setObjectName("forecastBody")
    b.setWordWrap(True)
    lay.addWidget(t)
    lay.addWidget(b)
    lay.addStretch(1)
    return w


# --------------------------------------------------------------------------- #
# Main window
# --------------------------------------------------------------------------- #
class CommandDeck(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.theme = "dark"
        self.setWindowTitle("AURORA · Command Deck")

        root = QtWidgets.QWidget()
        root.setObjectName("deckRoot")
        self.setCentralWidget(root)
        outer = QtWidgets.QVBoxLayout(root)
        outer.setContentsMargins(20, 20, 20, 16)
        outer.setSpacing(16)

        outer.addWidget(self._build_hero())
        outer.addWidget(self._build_stats())
        outer.addWidget(self._build_body(), 1)
        outer.addWidget(self._build_footer())

        # Live pulse: nudge the Kp readings + rings so the deck feels alive.
        self._tick = 0
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._pulse)
        self._timer.start(1200)

        self.resize(1180, 760)

    # -- hero -------------------------------------------------------------- #
    def _build_hero(self):
        hero = QtWidgets.QFrame()
        hero.setObjectName("hero")
        lay = QtWidgets.QHBoxLayout(hero)
        lay.setContentsMargins(24, 18, 24, 18)
        lay.setSpacing(16)

        left = QtWidgets.QVBoxLayout()
        left.setSpacing(4)
        title = QtWidgets.QLabel("✦  AURORA COMMAND DECK")
        title.setObjectName("heroTitle")
        sub = QtWidgets.QLabel("Real-time geomagnetic forecast network  ·  "
                               "12 ground stations  ·  built with Custom Widgets")
        sub.setObjectName("heroSub")
        left.addWidget(title)
        left.addWidget(sub)
        lay.addLayout(left)
        lay.addStretch(1)

        hint = QtWidgets.QHBoxLayout()
        hint.setSpacing(8)
        hint.addWidget(QtWidgets.QLabel("Command palette"))
        hint.addWidget(QCustomKbd(keys="Ctrl+K"))
        lay.addLayout(hint)

        self.themeBtn = QCustomQPushButton("☾  Dark")
        self.themeBtn.variant = "outline"
        self.themeBtn.sizeVariant = "sm"
        self.themeBtn.clicked.connect(self.toggle_theme)
        lay.addWidget(self.themeBtn)
        return hero

    # -- stat row ---------------------------------------------------------- #
    def _build_stats(self):
        wrap = QtWidgets.QWidget()
        row = QtWidgets.QHBoxLayout(wrap)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(14)

        self.statLive = QCustomStatCard(label="STATIONS LIVE", value="8 / 12",
                                        delta="+2 tonight", trend="up",
                                        caption="Arctic belt active")
        self.statKp = QCustomStatCard(label="PLANETARY Kp", value="6.2",
                                      delta="+0.8 / 3h", trend="up",
                                      caption="G2 storm watch")
        self.statProb = QCustomStatCard(label="AURORA PROBABILITY", value="87%",
                                        delta="+15%", trend="up",
                                        caption="65°N and above")
        self.statClear = QCustomStatCard(label="CLEAR SKIES", value="5 sites",
                                         delta="-1", trend="down",
                                         caption="Cloud moving in")
        for c in (self.statLive, self.statKp, self.statProb, self.statClear):
            row.addWidget(c, 1)
        return wrap

    # -- main body: splitter (table | forecast panel) ---------------------- #
    def _build_body(self):
        split = QCustomSplitter(QtCore.Qt.Horizontal)
        split.addWidget(self._build_stations_panel())
        split.addWidget(self._build_forecast_panel())
        split.setSizes([680, 480])
        return split

    def _build_stations_panel(self):
        panel = QtWidgets.QFrame()
        panel.setObjectName("panel")
        lay = QtWidgets.QVBoxLayout(panel)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(12)

        head = QtWidgets.QHBoxLayout()
        head.addWidget(section_label("GROUND STATIONS"))
        head.addStretch(1)
        self.filterBox = QtWidgets.QLineEdit()
        self.filterBox.setPlaceholderText("Filter stations…")
        self.filterBox.setFixedWidth(180)
        self.filterBox.textChanged.connect(self._on_filter)
        head.addWidget(self.filterBox)
        lay.addLayout(head)

        # region filter chips
        self.chips = QCustomChipGroup(selectable=True, exclusive=True)
        self.chips.addChip("All", data="All")
        self.chips.addChip("Arctic", data="Arctic")
        self.chips.addChip("Atlantic", data="Atlantic")
        self.chips.addChip("Antarctic", data="Antarctic")
        self.chips.selectionChanged.connect(self._on_region)
        lay.addWidget(self.chips)

        # the data table
        self.table = QCustomDataTable()
        self.table.setColumns([
            DataTableColumn("call", "Station", width=130),
            DataTableColumn("region", "Region", width=110),
            DataTableColumn("kp", "Kp", type="number", width=70,
                            formatter=lambda v: "%.1f" % v),
            DataTableColumn("clouds", "Cloud %", type="number", width=90,
                            formatter=lambda v: "%d%%" % v),
            DataTableColumn("status", "Status", width=90),
        ])
        self.table.setData([dict(s) for s in STATIONS])
        try:
            self.table.pageSize = 8
        except Exception:
            pass
        self.table.rowSelected.connect(self._on_row)
        lay.addWidget(self.table, 1)
        return panel

    def _build_forecast_panel(self):
        panel = QtWidgets.QFrame()
        panel.setObjectName("panel")
        lay = QtWidgets.QVBoxLayout(panel)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(12)

        lay.addWidget(section_label("FORECAST"))
        self.carousel = QCustomCarousel(wrap=True)
        for when, body in FORECASTS:
            self.carousel.addSlide(forecast_slide(when, body))
        self.carousel.setAutoAdvance(4000)
        self.carousel.setMinimumHeight(150)
        lay.addWidget(self.carousel)

        # progress rings row inside a card
        card = QCustomCard(title="Tonight's window", subtitle="Odds by latitude band")
        rings = QtWidgets.QHBoxLayout()
        rings.setSpacing(18)
        self.rings = []
        for name, val in (("65°N", 87), ("60°N", 62), ("55°N", 34)):
            col = QtWidgets.QVBoxLayout()
            col.setSpacing(6)
            ring = QCustomProgressRing(value=val)
            ring.setFixedSize(96, 96)
            self.rings.append(ring)
            cap = QtWidgets.QLabel(name)
            cap.setAlignment(QtCore.Qt.AlignCenter)
            col.addWidget(ring, 0, QtCore.Qt.AlignCenter)
            col.addWidget(cap)
            rings.addLayout(col)
        card.addLayout(rings)
        lay.addWidget(card)
        lay.addStretch(1)
        return panel

    # -- footer buttons ---------------------------------------------------- #
    def _build_footer(self):
        wrap = QtWidgets.QWidget()
        row = QtWidgets.QHBoxLayout(wrap)
        row.setContentsMargins(2, 0, 2, 0)
        row.setSpacing(10)

        self.statusLbl = QtWidgets.QLabel("Ready · select a station for details")
        self.statusLbl.setObjectName("footNote")
        row.addWidget(self.statusLbl)
        row.addStretch(1)

        for text, variant in (("Export CSV", "ghost"), ("Refresh", "secondary"),
                              ("Broadcast Alert", "primary")):
            b = QCustomQPushButton(text)
            b.variant = variant
            b.sizeVariant = "md"
            b.clicked.connect(partial(self._on_action, text))
            row.addWidget(b)
        return wrap

    # -- behaviour --------------------------------------------------------- #
    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        apply_theme(self.app, self.theme)
        self.themeBtn.setText("☀  Light" if self.theme == "light" else "☾  Dark")

    def _on_filter(self, text):
        self.table.setFilterText(text)

    def _on_region(self, selected):
        region = selected[0] if selected else "All"
        self.table.setFilterText("" if region == "All" else region)
        self.statusLbl.setText("Filtering region: %s" % region)

    def _on_row(self, row):
        if 0 <= row < len(STATIONS):
            s = STATIONS[row]
            self.statusLbl.setText("%s (%s) · Kp %.1f · %d%% cloud · %s"
                                   % (s["call"], s["region"], s["kp"],
                                      s["clouds"], s["status"]))

    def _on_action(self, name):
        self.statusLbl.setText("Action: %s — dispatched at tick %d"
                               % (name, self._tick))

    def _pulse(self):
        import math
        self._tick += 1
        kp = 6.2 + 0.4 * math.sin(self._tick / 3.0)
        self.statKp.setValue("%.1f" % kp)
        self.statKp.setDelta("%+.1f / 3h" % (0.4 * math.cos(self._tick / 3.0)),
                             trend="up" if math.cos(self._tick / 3.0) >= 0 else "down")
        for i, ring in enumerate(self.rings):
            base = (87, 62, 34)[i]
            ring.setValue(int(max(0, min(100, base + 6 * math.sin(self._tick / 2.0 + i)))))


# --------------------------------------------------------------------------- #
# Screenshot driver (for "share results" without a human at the keyboard).
# --------------------------------------------------------------------------- #
def _shoot(win, app, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    dark_path = os.path.join(out_dir, "aurora_dark.png")
    light_path = os.path.join(out_dir, "aurora_light.png")

    def grab(path):
        app.processEvents()
        win.grab().save(path)
        print("[shot] wrote", path, flush=True)

    # dark first (default), then flip to light
    QtCore.QTimer.singleShot(900, lambda: grab(dark_path))
    QtCore.QTimer.singleShot(1400, win.toggle_theme)
    QtCore.QTimer.singleShot(2000, lambda: grab(light_path))
    QtCore.QTimer.singleShot(2400, lambda: win.toggle_theme())  # back to dark for viewing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", metavar="DIR", default=None,
                        help="render, save light+dark screenshots to DIR, keep running")
    parser.add_argument("--exit-after", type=float, default=0,
                        help="seconds to auto-quit (0 = stay open)")
    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    win = CommandDeck(app)
    apply_theme(app, "dark")
    win.show()

    if args.shots:
        _shoot(win, app, args.shots)
    if args.exit_after:
        QtCore.QTimer.singleShot(int(args.exit_after * 1000), app.quit)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
