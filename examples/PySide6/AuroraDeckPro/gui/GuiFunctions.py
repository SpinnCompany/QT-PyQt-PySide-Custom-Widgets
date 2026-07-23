"""Aurora Deck Pro — GUI orchestration.

A single GuiFunctions orchestrator holds one Manager per page. navigateTo(name)
switches the animated pageStack by *widget* (never by index), marks the active
sidebar button, and lazy-inits the page's manager. Each manager reaches its
embedded component via ``container.component`` and wires child widgets by
objectName. Runtime data + interactions live here, never in the .ui.
"""

import math

from qtpy.QtCore import QObject, QTimer, Qt
from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsOpacityEffect
from qtpy.QtCore import QPropertyAnimation, QEasingCurve

from Custom_Widgets.QCustomDataTable import DataTableColumn
from Custom_Widgets.QCustomToast import QCustomToast


# --------------------------------------------------------------------------- #
# Fictional data (aurora-monitoring theme)
# --------------------------------------------------------------------------- #
STATIONS = [
    {"call": "Tromso-1", "region": "Arctic", "kp": 6.2, "clouds": 12, "status": "LIVE"},
    {"call": "Fairbanks-A", "region": "Arctic", "kp": 5.8, "clouds": 40, "status": "LIVE"},
    {"call": "Reykjavik", "region": "Atlantic", "kp": 4.9, "clouds": 65, "status": "HAZY"},
    {"call": "Yellowknife", "region": "Arctic", "kp": 6.7, "clouds": 8, "status": "LIVE"},
    {"call": "Murmansk", "region": "Arctic", "kp": 5.1, "clouds": 30, "status": "LIVE"},
    {"call": "Dunedin", "region": "Antarctic", "kp": 3.4, "clouds": 78, "status": "DARK"},
    {"call": "Ushuaia", "region": "Antarctic", "kp": 4.2, "clouds": 55, "status": "HAZY"},
    {"call": "Kiruna", "region": "Arctic", "kp": 6.0, "clouds": 20, "status": "LIVE"},
    {"call": "Nuuk", "region": "Atlantic", "kp": 5.5, "clouds": 45, "status": "HAZY"},
    {"call": "Hobart", "region": "Antarctic", "kp": 3.9, "clouds": 70, "status": "DARK"},
    {"call": "Abisko", "region": "Arctic", "kp": 6.4, "clouds": 5, "status": "LIVE"},
    {"call": "Sodankyla", "region": "Arctic", "kp": 5.9, "clouds": 25, "status": "LIVE"},
]

FORECASTS = [
    ("Tonight", "Substorm onset expected 21:40 UTC. Kp climbing to 6+ across the "
                "Arctic belt - corona overhead at Tromso and Abisko."),
    ("Tomorrow", "Coronal hole stream arrives. Sustained Kp 5-6 for 18h. "
                 "Atlantic stations clearing after midnight."),
    ("72 Hours", "Quieting trend. Kp settling to 3-4. Antarctic sites regain the "
                 "edge as the southern season deepens."),
]


# --------------------------------------------------------------------------- #
# Base manager
# --------------------------------------------------------------------------- #
class PageManager(QObject):
    def __init__(self, win, container):
        super().__init__(win)
        self.win = win
        self.container = container
        self._loaded = False

    @property
    def component(self):
        return getattr(self.container, "component", None)

    def onShown(self):
        if self._loaded:
            return
        comp = self.component
        if comp is None:
            # Component not embedded yet — retry shortly (container loads async
            # on first show for non-default pages).
            QTimer.singleShot(80, self.onShown)
            return
        try:
            self.setup(comp)
            self._loaded = True
        except Exception as e:  # never let one page break navigation
            print("[deck-pro] %s setup failed: %s" % (type(self).__name__, e))

    def setup(self, comp):
        raise NotImplementedError


# --------------------------------------------------------------------------- #
# Overview
# --------------------------------------------------------------------------- #
class OverviewManager(PageManager):
    def setup(self, comp):
        comp.activityTimeline.setItems([
            {"title": "Substorm onset detected", "time": "21:40", "color": "#4fe3a6"},
            {"title": "Kiruna came online", "time": "20:12"},
            {"title": "Kp forecast raised to 6", "time": "18:30", "color": "#f6c65a"},
            {"title": "Coronal hole flagged", "time": "14:05"},
        ])
        comp.shiftAvatars.setAvatars(["Ada L", "Kai R", "Mira S", "Tom V", "Nia B", "Jun P"])

        # Live Kp pulse.
        self._tick = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._pulse)
        self._timer.start(1200)

    def _pulse(self):
        comp = self.component
        if comp is None:
            return
        self._tick += 1
        kp = 6.2 + 0.4 * math.sin(self._tick / 3.0)
        try:
            comp.statKp.setValue("%.1f" % kp)
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# Stations
# --------------------------------------------------------------------------- #
class StationsManager(PageManager):
    def setup(self, comp):
        self.comp = comp
        comp.regionCombo.setItems(["All regions", "Arctic", "Atlantic", "Antarctic"])
        comp.stationsTable.setColumns([
            DataTableColumn("call", "Station", width=150),
            DataTableColumn("region", "Region", width=120),
            DataTableColumn("kp", "Kp", type="number", width=70,
                            formatter=lambda x: "%.1f" % x),
            DataTableColumn("clouds", "Cloud %", type="number", width=90,
                            formatter=lambda x: "%d%%" % x),
            DataTableColumn("status", "Status", width=90),
        ])
        comp.regionCombo.currentIndexChanged.connect(lambda *_: self.refilter())
        comp.minKp.valueChanged.connect(lambda *_: self.refilter())
        comp.liveOnly.toggled.connect(lambda *_: self.refilter())
        comp.cloudRange.valuesChanged.connect(lambda *_: self.refilter())
        comp.searchBox.textChanged.connect(lambda *_: self.refilter())
        self.refilter()

    def refilter(self):
        comp = self.comp
        reg = comp.regionCombo.currentText()
        try:
            minkp = float(comp.minKp.value() or 0)
        except Exception:
            minkp = 0.0
        try:
            lo, hi = int(comp.cloudRange.lowerValue), int(comp.cloudRange.upperValue)
        except Exception:
            lo, hi = 0, 100
        try:
            live = comp.liveOnly.isChecked()
        except Exception:
            live = False
        q = comp.searchBox.text().strip().lower()
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
        comp.stationsTable.setData(rows)
        comp.stationsStatus.setText("%d of %d stations match" % (len(rows), len(STATIONS)))


# --------------------------------------------------------------------------- #
# Forecast
# --------------------------------------------------------------------------- #
def _forecast_slide(when, body):
    w = QWidget()
    v = QVBoxLayout(w)
    v.setContentsMargins(18, 16, 18, 16)
    v.setSpacing(8)
    t = QLabel(when)
    t.setProperty("role", "h2")
    b = QLabel(body)
    b.setProperty("role", "muted")
    b.setWordWrap(True)
    v.addWidget(t)
    v.addWidget(b)
    v.addStretch(1)
    return w


class ForecastManager(PageManager):
    def setup(self, comp):
        for when, body in FORECASTS:
            comp.forecastCarousel.addSlide(_forecast_slide(when, body))
        comp.forecastCarousel.setAutoAdvance(4200)

        comp.phaseStepper.setSteps(["Standby", "Watch", "Capture", "Wrap-up"])
        comp.phaseStepper.setCurrentStep(1)

        comp.briefingAccordion.addSection(
            "What is the Kp index?",
            "A 0-9 scale of global geomagnetic activity. 5+ means a storm; higher "
            "pushes the aurora oval toward the equator.")
        comp.briefingAccordion.addSection(
            "Best viewing window",
            "Local midnight +/- 2h, away from city light, with clear skies and a low "
            "northern (or southern) horizon.")
        comp.briefingAccordion.addSection(
            "Camera settings",
            "Wide lens, f/2.8, ISO 1600-3200, 5-10s exposure, manual focus on a "
            "bright star.")


# --------------------------------------------------------------------------- #
# Analytics
# --------------------------------------------------------------------------- #
class AnalyticsManager(PageManager):
    def setup(self, comp):
        data = [(i, 4.0 + 2.2 * math.sin(i / 2.4) + 0.4 * math.cos(i)) for i in range(24)]
        comp.kpChart.addSeries("Kp", data)
        for setter, arg in (("setXAxisTitle", "hour"), ("setYAxisTitle", "Kp"),
                            ("setChartTitle", "24-hour Kp")):
            getattr(comp.kpChart, setter, lambda *a: None)(arg)

        counts = {}
        for s in STATIONS:
            counts[s["region"]] = counts.get(s["region"], 0) + 1
        comp.regionPie.addSeries("Regions", list(counts.items()))
        getattr(comp.regionPie, "setShowPercentages", lambda *a: None)(True)


# --------------------------------------------------------------------------- #
# Gallery (scroll-reveal showcase)
# --------------------------------------------------------------------------- #
class GalleryManager(PageManager):
    CARDS = ["cardRating", "cardBadges", "cardSwitches", "cardSegmented", "cardRange",
             "cardNumber", "cardKbd", "cardPagination", "cardColor", "cardRings",
             "cardChips", "cardCombo", "cardAvatars", "cardSkeleton", "cardBreadcrumbs",
             "cardToasts"]

    def setup(self, comp):
        comp.gSegmented.setSegments(["Day", "Night", "Auto"])
        comp.gSegmented.setCurrentIndex(1)
        comp.gCombo.setItems(["Arctic", "Atlantic", "Antarctic"])
        comp.gChips.setChips(["Arctic", "Atlantic", "Antarctic", "Live", "G2 watch"])
        comp.gBreadcrumbs.setItems(["Home", "Network", "Arctic", "Tromso-1"])
        comp.gAvatars.setAvatars(["Ada", "Kai", "Mira", "Tom", "Nia", "Jun", "Lee"])
        try:
            comp.gColorPicker.setColor("#4fe3a6")
        except Exception:
            pass

        for name, variant in (("gToastInfo", "info"), ("gToastSuccess", "success"),
                              ("gToastWarning", "warning")):
            btn = getattr(comp, name, None)
            if btn is not None:
                btn.clicked.connect(lambda _=False, v=variant: self._toast(v))

        self._reveal(comp)

    def _toast(self, variant):
        fn = getattr(QCustomToast, variant, None)
        try:
            if fn:
                fn(self.win, "%s: aurora conditions updated" % variant.capitalize())
            else:
                QCustomToast.show_toast(self.win, "Aurora conditions updated", variant=variant)
        except Exception:
            pass

    def _reveal(self, comp):
        """Staggered fade-in of the gallery cards on first show."""
        self._anims = []
        for i, name in enumerate(self.CARDS):
            card = getattr(comp, name, None)
            if card is None:
                continue
            eff = QGraphicsOpacityEffect(card)
            eff.setOpacity(0.0)
            card.setGraphicsEffect(eff)
            anim = QPropertyAnimation(eff, b"opacity", self)
            anim.setDuration(420)
            anim.setStartValue(0.0)
            anim.setEndValue(1.0)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            self._anims.append(anim)
            QTimer.singleShot(45 * i, anim.start)


# --------------------------------------------------------------------------- #
# Settings
# --------------------------------------------------------------------------- #
class SettingsManager(PageManager):
    def setup(self, comp):
        comp.themeSeg.setSegments(["Light", "Dark"])
        comp.themeSeg.setCurrentIndex(1)
        try:
            comp.accentPicker.setColor("#4fe3a6")
        except Exception:
            pass
        comp.saveBtn.clicked.connect(self._save)

    def _save(self):
        try:
            QCustomToast.success(self.win, "Preferences saved")
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# Orchestrator
# --------------------------------------------------------------------------- #
class GuiFunctions:
    def __init__(self, win):
        self.win = win
        self.ui = win.ui

    def initialize(self):
        ui = self.ui
        self.pages = {
            "overview": ui.overviewContainer,
            "stations": ui.stationsContainer,
            "forecast": ui.forecastContainer,
            "analytics": ui.analyticsContainer,
            "gallery": ui.galleryContainer,
            "settings": ui.settingsContainer,
        }
        self.navButtons = {
            "overview": ui.navOverview,
            "stations": ui.navStations,
            "forecast": ui.navForecast,
            "analytics": ui.navAnalytics,
            "gallery": ui.navGallery,
            "settings": ui.navSettings,
        }
        self.managers = {
            "overview": OverviewManager(self.win, ui.overviewContainer),
            "stations": StationsManager(self.win, ui.stationsContainer),
            "forecast": ForecastManager(self.win, ui.forecastContainer),
            "analytics": AnalyticsManager(self.win, ui.analyticsContainer),
            "gallery": GalleryManager(self.win, ui.galleryContainer),
            "settings": SettingsManager(self.win, ui.settingsContainer),
        }

        for name, btn in self.navButtons.items():
            btn.clicked.connect(lambda _=False, n=name: self.navigateTo(n))

        # Start on Overview.
        self.navigateTo("overview")

    def navigateTo(self, name):
        page = self.pages.get(name)
        if page is None:
            return
        # Switch by widget, never by index.
        self.ui.pageStack.setCurrentWidget(page)
        for n, btn in self.navButtons.items():
            active = (n == name)
            btn.setChecked(active)
            btn.setProperty("active", "true" if active else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        mgr = self.managers.get(name)
        if mgr is not None:
            mgr.onShown()
