"""AURORA - Deck Pro
====================

A multi-page showcase for the QT-PyQt-PySide Custom Widgets design-token set.
Sidebar navigation with an animated active indicator, animated page transitions
(QCustomQStackedWidget), a scroll-reveal Widget Gallery, and ~25 widgets spread
across six pages -- all styled by a single applyDesignTokens call, with a live
light/dark toggle.

Run:
    python deck_pro.py                 # interactive
    python deck_pro.py --shots DIR     # render every page (both themes) to PNG
"""

import sys
import os
import math
import argparse

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QPoint, QTimer

from Custom_Widgets.JSonStyles.tokens import applyDesignTokens, DesignTokens

# token widgets ---------------------------------------------------------------
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget
from Custom_Widgets.QCustomStatCard import QCustomStatCard
from Custom_Widgets.QCustomCard import QCustomCard
from Custom_Widgets.QCustomKbd import QCustomKbd
from Custom_Widgets.QCustomSplitter import QCustomSplitter
from Custom_Widgets.QCustomCarousel import QCustomCarousel
from Custom_Widgets.QCustomChip import QCustomChipGroup
from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
from Custom_Widgets.QCustomBadge import QCustomBadge
from Custom_Widgets.QCustomRating import QCustomRating
from Custom_Widgets.QCustomSwitch import QCustomSwitch
from Custom_Widgets.QCustomAlert import QCustomAlert
from Custom_Widgets.QCustomTimeline import QCustomTimeline
from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
from Custom_Widgets.QCustomStepper import QCustomStepper
from Custom_Widgets.QCustomAccordion import QCustomAccordion
from Custom_Widgets.QCustomBreadcrumbs import QCustomBreadcrumbs
from Custom_Widgets.QCustomPagination import QCustomPagination
from Custom_Widgets.QCustomAvatarGroup import QCustomAvatarGroup
from Custom_Widgets.QCustomSkeleton import QCustomSkeleton
from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider
from Custom_Widgets.QCustomNumberInput import QCustomNumberInput
from Custom_Widgets.QCustomComboBox import QCustomComboBox
from Custom_Widgets.QCustomColorPicker import QCustomColorPicker
from Custom_Widgets.QCustomToast import QCustomToast


# --------------------------------------------------------------------------- #
# Fictional data
# --------------------------------------------------------------------------- #
STATIONS = [
    {"call": "Tromsø-1", "region": "Arctic", "kp": 6.2, "clouds": 12, "status": "LIVE"},
    {"call": "Fairbanks-A", "region": "Arctic", "kp": 5.8, "clouds": 40, "status": "LIVE"},
    {"call": "Reykjavík", "region": "Atlantic", "kp": 4.9, "clouds": 65, "status": "HAZY"},
    {"call": "Yellowknife", "region": "Arctic", "kp": 6.7, "clouds": 8, "status": "LIVE"},
    {"call": "Murmansk", "region": "Arctic", "kp": 5.1, "clouds": 30, "status": "LIVE"},
    {"call": "Dunedin", "region": "Antarctic", "kp": 3.4, "clouds": 78, "status": "DARK"},
    {"call": "Ushuaia", "region": "Antarctic", "kp": 4.2, "clouds": 55, "status": "HAZY"},
    {"call": "Kiruna", "region": "Arctic", "kp": 6.0, "clouds": 20, "status": "LIVE"},
    {"call": "Nuuk", "region": "Atlantic", "kp": 5.5, "clouds": 45, "status": "HAZY"},
    {"call": "Hobart", "region": "Antarctic", "kp": 3.9, "clouds": 70, "status": "DARK"},
    {"call": "Abisko", "region": "Arctic", "kp": 6.4, "clouds": 5, "status": "LIVE"},
    {"call": "Sodankylä", "region": "Arctic", "kp": 5.9, "clouds": 25, "status": "LIVE"},
]
FORECASTS = [
    ("Tonight", "Substorm onset expected 21:40 UTC. Kp climbing to 6+ across the "
                "Arctic belt — corona overhead at Tromsø and Abisko."),
    ("Tomorrow", "Coronal hole stream arrives. Sustained Kp 5–6 for 18h. "
                 "Atlantic stations clearing after midnight."),
    ("72 Hours", "Quieting trend. Kp settling to 3–4. Antarctic sites regain the "
                 "edge as the southern season deepens."),
]


# --------------------------------------------------------------------------- #
# Chrome — derived from token roles so it flips with the theme
# --------------------------------------------------------------------------- #
def base_chrome(t):
    r = t.role
    return """
        QWidget#root {{ background:{muted}; }}
        QWidget {{ color:{on}; font-family:'Segoe UI','Inter',sans-serif; }}

        QWidget#sidebar {{ background:{surface}; border-right:1px solid {outline}; }}
        QLabel#brand {{ font-size:19px; font-weight:800; letter-spacing:1px; }}
        QLabel#brandSub {{ font-size:11px; color:{on}; }}

        QPushButton#navBtn {{ background:transparent; border:none; text-align:left;
            padding:11px 14px; border-radius:10px; font-size:14px; color:{on}; }}
        QPushButton#navBtn:hover {{ background:{muted}; }}
        QPushButton#navBtn:checked {{ color:{onp}; font-weight:600; }}
        QFrame#navIndicator {{ background:{primary}; border-radius:10px; }}

        QFrame#hero {{ border:1px solid {outline}; border-radius:16px;
            background:qlineargradient(x1:0,y1:0,x2:1,y2:1,
                       stop:0 {primary}, stop:1 {muted}); }}
        QLabel#heroTitle {{ font-size:24px; font-weight:800; letter-spacing:.5px; }}
        QLabel#heroSub {{ font-size:13px; color:{on}; }}

        QLabel#pageTitle {{ font-size:22px; font-weight:800; }}
        QLabel#pageKicker {{ font-family:monospace; font-size:11px; letter-spacing:3px;
            text-transform:uppercase; color:{primary}; }}
        QLabel#sectionTitle {{ font-size:12px; font-weight:700; letter-spacing:2px;
            color:{primary}; }}
        QLabel#muted {{ color:{on}; font-size:13px; }}

        QFrame#panel {{ background:{surface}; border:1px solid {outline};
            border-radius:14px; }}

        QLineEdit, QComboBox {{ background:{surface}; color:{on};
            border:1px solid {outline}; border-radius:8px; padding:6px 10px;
            selection-background-color:{primary}; }}
        QLineEdit:focus, QComboBox:focus {{ border:1px solid {primary}; }}

        QScrollArea {{ border:none; background:transparent; }}
        QScrollBar:vertical {{ background:transparent; width:10px; margin:2px; }}
        QScrollBar::handle:vertical {{ background:{outline}; border-radius:5px;
            min-height:30px; }}
        QScrollBar::handle:vertical:hover {{ background:{primary}; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}

        QLabel#forecastWhen {{ font-size:18px; font-weight:700; color:{primary}; }}
        QLabel#forecastBody {{ font-size:13px; }}
        QLabel#footNote {{ font-size:11px; color:{on}; }}
    """.format(surface=r("surface"), muted=r("surface-muted"), on=r("on-surface"),
               outline=r("outline"), primary=r("primary"), onp=r("on-primary"))


def apply_theme(app, theme):
    tokens = DesignTokens(theme=theme)
    app.setStyleSheet(base_chrome(tokens))
    applyDesignTokens(app, tokens=tokens)
    return tokens


# --------------------------------------------------------------------------- #
# Small reusable pieces
# --------------------------------------------------------------------------- #
def kicker(text):
    l = QtWidgets.QLabel(text)
    l.setObjectName("pageKicker")
    return l


def page_header(kick, title, subtitle=None):
    w = QtWidgets.QWidget()
    v = QtWidgets.QVBoxLayout(w)
    v.setContentsMargins(0, 0, 0, 0)
    v.setSpacing(2)
    v.addWidget(kicker(kick))
    t = QtWidgets.QLabel(title)
    t.setObjectName("pageTitle")
    v.addWidget(t)
    if subtitle:
        s = QtWidgets.QLabel(subtitle)
        s.setObjectName("muted")
        v.addWidget(s)
    return w


def section(text):
    l = QtWidgets.QLabel(text)
    l.setObjectName("sectionTitle")
    return l


class RevealCard(QtWidgets.QFrame):
    """A panel that fades + slides up into place on demand (scroll reveal)."""

    def __init__(self, title=None, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._lay = QtWidgets.QVBoxLayout(self)
        self._base = 16
        self._slidePx = 26.0
        self._lay.setContentsMargins(16, int(self._base + self._slidePx), 16, 16)
        self._lay.setSpacing(10)
        if title:
            self._lay.addWidget(section(title))
        self._eff = QtWidgets.QGraphicsOpacityEffect(self)
        self._eff.setOpacity(0.0)
        self.setGraphicsEffect(self._eff)
        self._revealed = False
        self._anims = []

    def add(self, w):
        if isinstance(w, QtWidgets.QLayout):
            self._lay.addLayout(w)
        else:
            self._lay.addWidget(w)
        return w

    def getSlide(self):
        return self._slidePx

    def setSlide(self, v):
        self._slidePx = v
        self._lay.setContentsMargins(16, int(self._base + v), 16, 16)

    slide = Property(float, getSlide, setSlide)

    def reveal(self):
        if self._revealed:
            return
        self._revealed = True
        ao = QPropertyAnimation(self._eff, b"opacity", self)
        ao.setDuration(540)
        ao.setStartValue(0.0)
        ao.setEndValue(1.0)
        ao.setEasingCurve(QEasingCurve.OutCubic)
        aslide = QPropertyAnimation(self, b"slide", self)
        aslide.setDuration(540)
        aslide.setStartValue(self._slidePx)
        aslide.setEndValue(0.0)
        aslide.setEasingCurve(QEasingCurve.OutCubic)
        ao.start()
        aslide.start()
        self._anims = [ao, aslide]


# --------------------------------------------------------------------------- #
# Sidebar with an animated active indicator
# --------------------------------------------------------------------------- #
class NavBar(QtWidgets.QWidget):
    currentChanged = QtCore.Signal(int)

    def __init__(self, items, parent=None):
        super().__init__(parent)
        self._indicator = QtWidgets.QFrame(self)
        self._indicator.setObjectName("navIndicator")
        self._buttons = []

        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        for i, (glyph, label) in enumerate(items):
            b = QtWidgets.QPushButton("   %s   %s" % (glyph, label))
            b.setObjectName("navBtn")
            b.setCheckable(True)
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _=False, idx=i: self.setCurrent(idx))
            lay.addWidget(b)
            self._buttons.append(b)
        lay.addStretch(1)
        self._current = 0
        self._buttons[0].setChecked(True)
        self._anim = None
        QTimer.singleShot(0, lambda: self._place(animate=False))

    def _targetRect(self, idx):
        g = self._buttons[idx].geometry()
        return QtCore.QRect(g.x(), g.y(), g.width(), g.height())

    def _place(self, animate=True):
        self._indicator.lower()
        target = self._targetRect(self._current)
        if not animate:
            self._indicator.setGeometry(target)
            return
        self._anim = QPropertyAnimation(self._indicator, b"geometry", self)
        self._anim.setDuration(340)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.setStartValue(self._indicator.geometry())
        self._anim.setEndValue(target)
        self._anim.start()

    def setCurrent(self, idx):
        if idx == self._current:
            self._buttons[idx].setChecked(True)
            return
        self._current = idx
        for i, b in enumerate(self._buttons):
            b.setChecked(i == idx)
        self._place(animate=True)
        self.currentChanged.emit(idx)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._place(animate=False)


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
def _forecast_slide(when, body):
    w = QtWidgets.QWidget()
    v = QtWidgets.QVBoxLayout(w)
    v.setContentsMargins(18, 16, 18, 16)
    v.setSpacing(8)
    t = QtWidgets.QLabel(when)
    t.setObjectName("forecastWhen")
    b = QtWidgets.QLabel(body)
    b.setObjectName("forecastBody")
    b.setWordWrap(True)
    v.addWidget(t)
    v.addWidget(b)
    v.addStretch(1)
    return w


class OverviewPage(QtWidgets.QWidget):
    def __init__(self, win):
        super().__init__()
        self.win = win
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(26, 24, 26, 24)
        v.setSpacing(16)

        hero = QtWidgets.QFrame()
        hero.setObjectName("hero")
        hl = QtWidgets.QHBoxLayout(hero)
        hl.setContentsMargins(24, 20, 24, 20)
        col = QtWidgets.QVBoxLayout()
        col.setSpacing(4)
        tt = QtWidgets.QLabel("✦  Good evening, Operator")
        tt.setObjectName("heroTitle")
        st = QtWidgets.QLabel("G2 storm watch is active. 8 of 12 stations reporting live.")
        st.setObjectName("heroSub")
        col.addWidget(tt)
        col.addWidget(st)
        hl.addLayout(col)
        hl.addStretch(1)
        hint = QtWidgets.QHBoxLayout()
        hint.setSpacing(8)
        hint.addWidget(QtWidgets.QLabel("Command palette"))
        hint.addWidget(QCustomKbd(keys="Ctrl+K"))
        hl.addLayout(hint)
        v.addWidget(hero)

        # stats
        stats = QtWidgets.QHBoxLayout()
        stats.setSpacing(14)
        self.statKp = QCustomStatCard(label="PLANETARY Kp", value="6.2",
                                      delta="+0.8 / 3h", trend="up", caption="G2 watch")
        for c in (QCustomStatCard(label="STATIONS LIVE", value="8 / 12",
                                  delta="+2", trend="up", caption="Arctic belt"),
                  self.statKp,
                  QCustomStatCard(label="AURORA ODDS", value="87%", delta="+15%",
                                  trend="up", caption="≥65°N"),
                  QCustomStatCard(label="CLEAR SKIES", value="5", delta="-1",
                                  trend="down", caption="cloud moving in")):
            stats.addWidget(c, 1)
        v.addLayout(stats)

        alert = QCustomAlert(
            title="Geomagnetic storm in progress",
            text="Kp has crossed 6. Aurora may be visible down to 60°N tonight.",
            variant="warning")
        v.addWidget(alert)

        row = QtWidgets.QHBoxLayout()
        row.setSpacing(14)

        events = QCustomCard(title="Activity", subtitle="Last few hours")
        tl = QCustomTimeline()
        tl.setItems([
            {"title": "Substorm onset detected", "time": "21:40", "color": "#4fe3a6"},
            {"title": "Kiruna came online", "time": "20:12"},
            {"title": "Kp forecast raised to 6", "time": "18:30", "color": "#f6c65a"},
            {"title": "Coronal hole flagged", "time": "14:05"},
        ])
        events.addWidget(tl)
        row.addWidget(events, 1)

        team = QCustomCard(title="On shift", subtitle="Night watch team")
        avatars = QCustomAvatarGroup(maxVisible=5, size=36)
        avatars.setAvatars(["Ada L", "Kai R", "Mira S", "Tom V", "Nia B", "Jun P"])
        team.addWidget(avatars)
        badges = QtWidgets.QHBoxLayout()
        badges.setSpacing(8)
        for txt, var in (("LIVE", "success"), ("G2", "warning"), ("3 alerts", "danger")):
            badges.addWidget(QCustomBadge(txt, variant=var))
        badges.addStretch(1)
        team.addLayout(badges)
        row.addWidget(team, 1)
        v.addLayout(row)
        v.addStretch(1)


class StationsPage(QtWidgets.QWidget):
    def __init__(self, win):
        super().__init__()
        self.win = win
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(26, 24, 26, 24)
        v.setSpacing(14)
        v.addWidget(page_header("Network", "Ground Stations",
                                "Filter the array by region, activity and sky."))

        panel = QtWidgets.QFrame()
        panel.setObjectName("panel")
        pl = QtWidgets.QVBoxLayout(panel)
        pl.setContentsMargins(18, 16, 18, 16)
        pl.setSpacing(12)

        # toolbar of inputs
        bar = QtWidgets.QHBoxLayout()
        bar.setSpacing(14)
        self.region = QCustomComboBox(editable=False)
        self.region.setItems(["All regions", "Arctic", "Atlantic", "Antarctic"])
        self.region.currentIndexChanged.connect(lambda *_: self.refilter())
        bar.addWidget(self.region)

        minkpBox = QtWidgets.QHBoxLayout()
        minkpBox.setSpacing(6)
        minkpBox.addWidget(QtWidgets.QLabel("Min Kp"))
        self.minKp = QCustomNumberInput(minimum=0, maximum=9, value=0, step=1)
        self.minKp.valueChanged.connect(lambda *_: self.refilter())
        minkpBox.addWidget(self.minKp)
        bar.addLayout(minkpBox)

        self.liveOnly = QCustomSwitch(checked=False)
        self.liveOnly.toggled.connect(lambda *_: self.refilter())
        liveBox = QtWidgets.QHBoxLayout()
        liveBox.setSpacing(6)
        liveBox.addWidget(QtWidgets.QLabel("Live only"))
        liveBox.addWidget(self.liveOnly)
        bar.addLayout(liveBox)
        bar.addStretch(1)

        self.filterBox = QtWidgets.QLineEdit()
        self.filterBox.setPlaceholderText("Search…")
        self.filterBox.setFixedWidth(160)
        self.filterBox.textChanged.connect(lambda *_: self.refilter())
        bar.addWidget(self.filterBox)
        pl.addLayout(bar)

        # cloud range
        cloud = QtWidgets.QHBoxLayout()
        cloud.setSpacing(10)
        cloud.addWidget(QtWidgets.QLabel("Cloud cover %"))
        self.cloud = QCustomRangeSlider(minimum=0, maximum=100)
        self.cloud.setValues(0, 100)
        self.cloud.valuesChanged.connect(lambda *_: self.refilter())
        cloud.addWidget(self.cloud, 1)
        pl.addLayout(cloud)

        self.table = QCustomDataTable()
        self.table.setColumns([
            DataTableColumn("call", "Station", width=140),
            DataTableColumn("region", "Region", width=120),
            DataTableColumn("kp", "Kp", type="number", width=70,
                            formatter=lambda x: "%.1f" % x),
            DataTableColumn("clouds", "Cloud %", type="number", width=90,
                            formatter=lambda x: "%d%%" % x),
            DataTableColumn("status", "Status", width=90),
        ])
        try:
            self.table.pageSize = 8
        except Exception:
            pass
        self.table.rowSelected.connect(self._on_row)
        pl.addWidget(self.table, 1)

        self.status = QtWidgets.QLabel("")
        self.status.setObjectName("footNote")
        pl.addWidget(self.status)

        v.addWidget(panel, 1)
        self.refilter()

    def refilter(self):
        reg = self.region.currentText()
        minkp = float(self.minKp.value() or 0)
        try:
            lo, hi = int(self.cloud.lowerValue), int(self.cloud.upperValue)
        except Exception:
            lo, hi = 0, 100
        live = self._live_only()
        q = self.filterBox.text().strip().lower()
        rows = []
        for s in STATIONS:
            if reg != "All regions" and s["region"] != reg:
                continue
            if s["kp"] < minkp:
                continue
            if not (lo <= s["clouds"] <= hi):
                continue
            if live and s["status"] != "LIVE":
                continue
            if q and q not in (s["call"] + s["region"] + s["status"]).lower():
                continue
            rows.append(dict(s))
        self.table.setData(rows)
        self.status.setText("%d of %d stations match" % (len(rows), len(STATIONS)))

    def _live_only(self):
        try:
            return self.liveOnly.isChecked()
        except Exception:
            return False

    def _on_row(self, row):
        if 0 <= row < len(STATIONS):
            s = STATIONS[row]
            self.status.setText("%s (%s) · Kp %.1f · %d%% cloud · %s"
                                % (s["call"], s["region"], s["kp"], s["clouds"], s["status"]))


class ForecastPage(QtWidgets.QWidget):
    def __init__(self, win):
        super().__init__()
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(26, 24, 26, 24)
        v.setSpacing(14)
        v.addWidget(page_header("Outlook", "Forecast",
                                "Three-day geomagnetic outlook and mission phases."))

        split = QCustomSplitter(Qt.Horizontal)

        left = QtWidgets.QFrame()
        left.setObjectName("panel")
        ll = QtWidgets.QVBoxLayout(left)
        ll.setContentsMargins(18, 16, 18, 16)
        ll.setSpacing(12)
        ll.addWidget(section("ROLLING FORECAST"))
        car = QCustomCarousel(wrap=True)
        for when, body in FORECASTS:
            car.addSlide(_forecast_slide(when, body))
        car.setAutoAdvance(4200)
        car.setMinimumHeight(150)
        ll.addWidget(car)

        rings = QtWidgets.QHBoxLayout()
        rings.setSpacing(16)
        for name, val in (("65°N", 87), ("60°N", 62), ("55°N", 34)):
            c = QtWidgets.QVBoxLayout()
            c.setSpacing(6)
            ring = QCustomProgressRing(value=val)
            ring.setFixedSize(92, 92)
            cap = QtWidgets.QLabel(name)
            cap.setAlignment(Qt.AlignCenter)
            c.addWidget(ring, 0, Qt.AlignCenter)
            c.addWidget(cap)
            rings.addLayout(c)
        ll.addLayout(rings)
        ll.addStretch(1)
        split.addWidget(left)

        right = QtWidgets.QFrame()
        right.setObjectName("panel")
        rl = QtWidgets.QVBoxLayout(right)
        rl.setContentsMargins(18, 16, 18, 16)
        rl.setSpacing(14)
        rl.addWidget(section("MISSION PHASES"))
        stepper = QCustomStepper(orientation=Qt.Horizontal)
        stepper.setSteps(["Standby", "Watch", "Capture", "Wrap-up"])
        stepper.setCurrentStep(1)
        rl.addWidget(stepper)

        rl.addWidget(section("BRIEFING"))
        acc = QCustomAccordion(exclusive=True)
        acc.addSection("What is the Kp index?",
                       "A 0–9 scale of global geomagnetic activity. 5+ means a storm; "
                       "higher pushes the aurora oval toward the equator.")
        acc.addSection("Best viewing window",
                       "Local midnight ± 2h, away from city light, with clear skies "
                       "and a low northern (or southern) horizon.")
        acc.addSection("Camera settings",
                       "Wide lens, f/2.8, ISO 1600–3200, 5–10s exposure, manual focus "
                       "on a bright star.")
        rl.addWidget(acc)
        rl.addStretch(1)
        split.addWidget(right)
        split.setSizes([520, 520])
        v.addWidget(split, 1)


class AnalyticsPage(QtWidgets.QWidget):
    def __init__(self, win):
        super().__init__()
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(26, 24, 26, 24)
        v.setSpacing(14)
        v.addWidget(page_header("Signals", "Analytics",
                                "Kp trend and station distribution."))
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(14)
        row.addWidget(self._line_panel(), 3)
        row.addWidget(self._pie_panel(), 2)
        v.addLayout(row, 1)

    def _wrap(self, title, inner):
        p = QtWidgets.QFrame()
        p.setObjectName("panel")
        l = QtWidgets.QVBoxLayout(p)
        l.setContentsMargins(18, 16, 18, 16)
        l.setSpacing(10)
        l.addWidget(section(title))
        l.addWidget(inner, 1)
        return p

    def _line_panel(self):
        try:
            from Custom_Widgets.QCustomCharts.QCustomLineChart import QCustomLineChart
            ch = QCustomLineChart()
            data = [(i, 4.0 + 2.2 * math.sin(i / 2.4) + 0.4 * math.cos(i))
                    for i in range(24)]
            ch.addSeries("Kp", data)
            for setter, arg in (("setXAxisTitle", "hour"), ("setYAxisTitle", "Kp"),
                                ("setChartTitle", "24-hour Kp")):
                getattr(ch, setter, lambda *a: None)(arg)
            return self._wrap("KP TREND", ch)
        except Exception as e:
            return self._wrap("KP TREND", self._empty("Chart unavailable", str(e)))

    def _pie_panel(self):
        try:
            from Custom_Widgets.QCustomCharts.QCustomPieChart import QCustomPieChart
            ch = QCustomPieChart()
            counts = {}
            for s in STATIONS:
                counts[s["region"]] = counts.get(s["region"], 0) + 1
            ch.addSeries("Regions", list(counts.items()))
            getattr(ch, "setShowPercentages", lambda *a: None)(True)
            return self._wrap("BY REGION", ch)
        except Exception as e:
            return self._wrap("BY REGION", self._empty("Chart unavailable", str(e)))

    def _empty(self, title, desc):
        es = QCustomEmptyState(icon="📊", title=title)
        try:
            es.setDescription(desc[:120])
        except Exception:
            pass
        return es


class GalleryPage(QtWidgets.QWidget):
    """The scroll-reveal showcase: cards fade + slide up as they enter view."""

    def __init__(self, win):
        super().__init__()
        self.win = win
        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(26, 24, 26, 8)
        outer.setSpacing(12)
        outer.addWidget(page_header("Everything", "Widget Gallery",
                                    "Scroll — each card animates into view."))

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.verticalScrollBar().valueChanged.connect(self._check)
        inner = QtWidgets.QWidget()
        self.grid = QtWidgets.QGridLayout(inner)
        self.grid.setContentsMargins(2, 6, 12, 26)
        self.grid.setHorizontalSpacing(16)
        self.grid.setVerticalSpacing(16)
        self.scroll.setWidget(inner)
        outer.addWidget(self.scroll, 1)

        self.cards = []
        self._build_cards()
        for i, c in enumerate(self.cards):
            self.grid.addWidget(c, i // 2, i % 2)

    # -- gallery card builders ------------------------------------------- #
    def _card(self, title):
        c = RevealCard(title)
        self.cards.append(c)
        return c

    def _build_cards(self):
        c = self._card("Rating")
        c.add(QCustomRating(maximum=5)).setValue(4)

        c = self._card("Switches")
        rowsw = QtWidgets.QHBoxLayout()
        rowsw.setSpacing(14)
        for lab, on in (("Alerts", True), ("Auto-capture", False), ("Dark mode", True)):
            box = QtWidgets.QHBoxLayout()
            box.setSpacing(6)
            box.addWidget(QtWidgets.QLabel(lab))
            box.addWidget(QCustomSwitch(checked=on))
            rowsw.addLayout(box)
        rowsw.addStretch(1)
        c.add(rowsw)

        c = self._card("Badges")
        rowb = QtWidgets.QHBoxLayout()
        rowb.setSpacing(8)
        for t, var in (("Default", "default"), ("Success", "success"),
                       ("Warning", "warning"), ("Danger", "danger")):
            rowb.addWidget(QCustomBadge(t, variant=var))
        rowb.addStretch(1)
        c.add(rowb)

        c = self._card("Segmented control")
        seg = QCustomSegmentedControl()
        seg.setSegments(["Day", "Night", "Auto"])
        seg.setCurrentIndex(1)
        c.add(seg)

        c = self._card("Range slider")
        rs = QCustomRangeSlider(minimum=0, maximum=100)
        rs.setValues(20, 80)
        c.add(rs)

        c = self._card("Number input")
        c.add(QCustomNumberInput(minimum=0, maximum=9, value=6, step=1))

        c = self._card("Keyboard shortcuts")
        rowk = QtWidgets.QHBoxLayout()
        rowk.setSpacing(10)
        for keys in ("Ctrl+K", "Ctrl+Shift+P", "⌘+S"):
            rowk.addWidget(QCustomKbd(keys=keys))
        rowk.addStretch(1)
        c.add(rowk)

        c = self._card("Breadcrumbs")
        bc = QCustomBreadcrumbs()
        bc.setItems(["Home", "Network", "Arctic", "Tromsø-1"])
        c.add(bc)

        c = self._card("Pagination")
        pg = QCustomPagination(pageCount=8)
        pg.setCurrentPage(3)
        c.add(pg)

        c = self._card("Color picker")
        c.add(QCustomColorPicker(color="#4fe3a6"))

        c = self._card("Progress rings")
        rowr = QtWidgets.QHBoxLayout()
        rowr.setSpacing(14)
        for v in (34, 62, 87):
            r = QCustomProgressRing(value=v)
            r.setFixedSize(72, 72)
            rowr.addWidget(r)
        rowr.addStretch(1)
        c.add(rowr)

        c = self._card("Loading skeleton")
        for shape in ("line", "line", "line"):
            sk = QCustomSkeleton(shape=shape)
            sk.setMinimumHeight(14)
            c.add(sk)

        c = self._card("Combo box")
        cb = QCustomComboBox(editable=False)
        cb.setItems(["Arctic", "Atlantic", "Antarctic"])
        c.add(cb)

        c = self._card("Avatar group")
        ag = QCustomAvatarGroup(maxVisible=5, size=34)
        ag.setAvatars(["Ada", "Kai", "Mira", "Tom", "Nia", "Jun", "Lee"])
        c.add(ag)

        c = self._card("Toasts")
        rowt = QtWidgets.QHBoxLayout()
        rowt.setSpacing(8)
        for label, var in (("Info", "info"), ("Success", "success"), ("Warning", "warning")):
            b = QCustomQPushButton("%s toast" % label)
            b.variant = "outline"
            b.sizeVariant = "sm"
            b.clicked.connect(lambda _=False, v=var, l=label: self._toast(v, l))
            rowt.addWidget(b)
        rowt.addStretch(1)
        c.add(rowt)

        c = self._card("Empty state")
        es = QCustomEmptyState(icon="🛰️", title="No passes scheduled")
        try:
            es.setDescription("Add a target to begin tracking.")
            es.setActionText("Add target")
        except Exception:
            pass
        c.add(es)

    def _toast(self, variant, label):
        try:
            fn = getattr(QCustomToast, variant, None)
            if fn:
                fn(self.window(), "%s: aurora conditions updated" % label)
            else:
                QCustomToast.show_toast(self.window(), label, variant=variant)
        except Exception:
            pass

    def _check(self, *_):
        vp = self.scroll.viewport()
        h = vp.height()
        for c in self.cards:
            if c._revealed:
                continue
            top = c.mapTo(vp, QPoint(0, 0)).y()
            if -c.height() < top < h - 30:
                c.reveal()

    def showEvent(self, e):
        super().showEvent(e)
        QTimer.singleShot(60, self._check)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._check()

    def on_shown(self):
        # called when the page becomes current in the stack
        for stagger, c in enumerate(self.cards):
            if not c._revealed:
                QTimer.singleShot(40 * stagger, self._check)
                break
        QTimer.singleShot(80, self._check)


class SettingsPage(QtWidgets.QWidget):
    def __init__(self, win):
        super().__init__()
        self.win = win
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(26, 24, 26, 24)
        v.setSpacing(14)
        v.addWidget(page_header("Preferences", "Settings",
                                "Tune the deck to your watch."))

        appearance = QCustomCard(title="Appearance", subtitle="Theme and accent")
        seg = QCustomSegmentedControl()
        seg.setSegments(["Light", "Dark"])
        seg.setCurrentIndex(1)
        seg.currentChanged.connect(lambda i: win.set_theme("light" if i == 0 else "dark"))
        appearance.addWidget(seg)
        appearance.addWidget(QCustomColorPicker(color="#4fe3a6"))
        v.addWidget(appearance)

        prefs = QCustomCard(title="Notifications", subtitle="What wakes you up")
        for lab, on in (("Storm alerts (Kp ≥ 6)", True),
                        ("Station offline", True),
                        ("Clear-sky windows", False)):
            r = QtWidgets.QHBoxLayout()
            l = QtWidgets.QLabel(lab)
            l.setObjectName("muted")
            r.addWidget(l)
            r.addStretch(1)
            r.addWidget(QCustomSwitch(checked=on))
            prefs.addLayout(r)
        v.addWidget(prefs)

        save = QCustomQPushButton("Save preferences")
        save.variant = "primary"
        save.clicked.connect(self._save)
        v.addWidget(save, 0, Qt.AlignLeft)
        v.addStretch(1)

    def _save(self):
        try:
            QCustomToast.success(self.window(), "Preferences saved")
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# Main window
# --------------------------------------------------------------------------- #
class DeckPro(QtWidgets.QMainWindow):
    NAV = [("◉", "Overview"), ("▤", "Stations"), ("◈", "Forecast"),
           ("▚", "Analytics"), ("⬢", "Gallery"), ("⚙", "Settings")]

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.theme = "dark"
        self.setWindowTitle("AURORA · Deck Pro")

        root = QtWidgets.QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        h = QtWidgets.QHBoxLayout(root)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)

        # sidebar
        side = QtWidgets.QWidget()
        side.setObjectName("sidebar")
        side.setFixedWidth(216)
        sv = QtWidgets.QVBoxLayout(side)
        sv.setContentsMargins(18, 22, 18, 18)
        sv.setSpacing(16)
        brand = QtWidgets.QVBoxLayout()
        brand.setSpacing(2)
        b1 = QtWidgets.QLabel("✦ AURORA")
        b1.setObjectName("brand")
        b2 = QtWidgets.QLabel("deck pro")
        b2.setObjectName("brandSub")
        brand.addWidget(b1)
        brand.addWidget(b2)
        sv.addLayout(brand)

        self.nav = NavBar(self.NAV)
        self.nav.currentChanged.connect(self.go)
        sv.addWidget(self.nav)
        sv.addStretch(1)

        themeSeg = QCustomSegmentedControl()
        themeSeg.setSegments(["☀", "☾"])
        themeSeg.setCurrentIndex(1)
        themeSeg.currentChanged.connect(lambda i: self.set_theme("light" if i == 0 else "dark"))
        self.themeSeg = themeSeg
        sv.addWidget(themeSeg)
        h.addWidget(side)

        # animated page stack
        self.stack = QCustomQStackedWidget()
        try:
            self.stack.fadeTransition = True
            self.stack.slideTransition = True
            self.stack.transitionDirection = "horizontal"
            self.stack.transitionTime = 420
            self.stack.fadeTime = 320
        except Exception:
            pass
        h.addWidget(self.stack, 1)

        self.pages = [
            OverviewPage(self), StationsPage(self), ForecastPage(self),
            AnalyticsPage(self), GalleryPage(self), SettingsPage(self),
        ]
        for p in self.pages:
            self.stack.addWidget(p)

        # live pulse for the Kp stat
        self._tick = 0
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._pulse)
        self._timer.start(1200)

        self.resize(1200, 800)

    def go(self, idx):
        try:
            self.stack.setCurrentIndex(idx)
        except Exception:
            QtWidgets.QStackedWidget.setCurrentIndex(self.stack, idx)
        page = self.pages[idx]
        if hasattr(page, "on_shown"):
            page.on_shown()

    def set_theme(self, theme):
        if theme == self.theme:
            return
        self.theme = theme
        apply_theme(self.app, theme)
        # keep the two theme controls in sync
        idx = 0 if theme == "light" else 1
        for seg in (self.themeSeg,):
            try:
                seg.blockSignals(True)
                seg.setCurrentIndex(idx)
                seg.blockSignals(False)
            except Exception:
                pass

    def _pulse(self):
        self._tick += 1
        kp = 6.2 + 0.4 * math.sin(self._tick / 3.0)
        ov = self.pages[0]
        if hasattr(ov, "statKp"):
            ov.statKp.setValue("%.1f" % kp)


# --------------------------------------------------------------------------- #
# Screenshot driver
# --------------------------------------------------------------------------- #
def _shoot(win, app, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    names = ["overview", "stations", "forecast", "analytics", "gallery", "settings"]
    plan = []
    t = 500
    for theme in ("dark", "light"):
        plan.append((t, lambda th=theme: win.set_theme(th)))
        t += 250
        for i, nm in enumerate(names):
            plan.append((t, lambda idx=i: win.go(idx)))
            t += 350
            plan.append((t, lambda th=theme, nm=nm: _grab(win, app, out_dir, "%s_%s" % (nm, th))))
            t += 250
    plan.append((t + 200, app.quit))
    for when, fn in plan:
        QtCore.QTimer.singleShot(when, fn)


def _grab(win, app, out_dir, name):
    app.processEvents()
    path = os.path.join(out_dir, "deck_%s.png" % name)
    win.grab().save(path)
    print("[shot]", path, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", metavar="DIR", default=None)
    args = ap.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    win = DeckPro(app)
    apply_theme(app, "dark")
    win.show()
    if args.shots:
        _shoot(win, app, args.shots)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
