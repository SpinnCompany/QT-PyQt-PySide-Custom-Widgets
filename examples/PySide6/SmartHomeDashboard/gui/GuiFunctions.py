"""My Home smart-home dashboard — GUI orchestration (the CORRECT Custom_Widgets way).

The window shell (ui/MainWindow.ui) hosts one QCustomComponentContainer per
region; each loads a granular component .ui (TopBar, HelloCard, GaugesCard,
DevicesCard, LightingCard, SecurityCard) exposed as ``container.component``.
This orchestrator fills every component with data + icons and paints the
gradient surfaces (header bar, active tile, ring gauges, brightness slider,
lock switch) from the token-driven ChartPalette in style.json, so they flip
when the theme switches (SmartHome Dark / Light).
"""

import os

from qtpy.QtCore import QObject, Qt, QByteArray, QThread, QTimer, QSize
from qtpy.QtGui import QColor, QPainter, QPixmap, QIcon, QBrush, QFont, QPainterPath
from qtpy.QtWidgets import QApplication, QLabel, QButtonGroup

import Custom_Widgets
from gui import theme as T
from gui import data as D
from gui.workers import AvatarWorker

_ICONS = os.path.join(os.path.dirname(Custom_Widgets.__file__), "Qss", "icons")
_FEATHER = os.path.join(_ICONS, "feather")
_MATERIAL = os.path.join(_ICONS, "material_design")
_PM = {}

try:
    from qtpy.QtSvg import QSvgRenderer
except Exception:
    QSvgRenderer = None


def _icon_path(name):
    """Resolve a feather name, else fall back to material_design."""
    p = os.path.join(_FEATHER, name + ".svg")
    if os.path.exists(p):
        return p
    return os.path.join(_MATERIAL, name + ".svg")


def icon_pixmap(name_or_path, color, size=22):
    """Recolour ANY svg (stroke- or fill-based) to `color` by tinting its alpha
    — works for both the feather and material icon sets."""
    path = name_or_path if os.path.isabs(name_or_path) else _icon_path(name_or_path)
    key = (path, str(color), size)
    if key in _PM:
        return _PM[key]
    pm = QPixmap(int(size * 2), int(size * 2))
    pm.fill(QColor(0, 0, 0, 0))
    if os.path.exists(path) and QSvgRenderer is not None:
        r = QSvgRenderer(path)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        r.render(p)
        p.setCompositionMode(QPainter.CompositionMode_SourceIn)
        p.fillRect(pm.rect(), QColor(color))
        p.end()
    pm.setDevicePixelRatio(2.0)
    _PM[key] = pm
    return pm


def icon(name, color, size=22):
    return QIcon(icon_pixmap(name, color, size))


class GuiFunctions:
    def __init__(self, win):
        self.win = win
        self.ui = win.ui
        self._built = False

    # -- lifecycle -------------------------------------------------------- #
    def initialize(self):
        self.themeEngine = getattr(self.win, "themeEngine", None)
        if self.themeEngine is not None:
            try:
                self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
            except Exception:
                pass
        self._populateWhenReady()
        self._watchSources()

    def _watchSources(self):
        try:
            from qtpy.QtCore import QFileSystemWatcher
            src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
            self._srcDir = src
            self._w = QFileSystemWatcher(self.win)
            if os.path.isdir(src):
                self._w.addPath(src)
                for f in os.listdir(src):
                    if f.endswith(".py"):
                        self._w.addPath(os.path.join(src, f))
            self._rt = QTimer(self.win); self._rt.setSingleShot(True)
            self._rt.timeout.connect(self._reapply)
            self._w.directoryChanged.connect(lambda _p: self._rt.start(800))
            self._w.fileChanged.connect(lambda _p: self._rt.start(800))
        except Exception:
            pass

    def _reapply(self):
        try:
            src = getattr(self, "_srcDir", None)
            if src and os.path.isdir(src):
                have = set(self._w.files())
                for f in os.listdir(src):
                    p = os.path.join(src, f)
                    if f.endswith(".py") and p not in have:
                        self._w.addPath(p)
        except Exception:
            pass
        self._populateWhenReady()

    _NEED = ["topBarContainer", "helloContainer", "gaugesContainer",
             "devicesContainer", "lightingContainer", "securityContainer"]

    def _c(self, name):
        cont = getattr(self.ui, name, None)
        if cont is None:
            return None
        live = getattr(getattr(cont, "form", None), "ui", None)
        return live if live is not None else getattr(cont, "component", None)

    def _components_ready(self):
        return all(self._c(n) is not None for n in self._NEED)

    def _populateWhenReady(self, tries=0):
        if not self._components_ready():
            if tries < 40:
                QTimer.singleShot(60, lambda: self._populateWhenReady(tries + 1))
            return
        self._buildAll()

    def _theme(self):
        return str(getattr(self.themeEngine, "theme", "") or T.THEME_DARK)

    def _pal(self):
        return T.chart_palette(self._theme())

    # -- build ------------------------------------------------------------ #
    def _buildAll(self):
        pal = self._pal()
        jobs = [("topBarContainer", self._topbar), ("helloContainer", self._hello),
                ("gaugesContainer", self._gauges), ("devicesContainer", self._devices),
                ("lightingContainer", self._lighting), ("securityContainer", self._security)]
        stale = False
        for name, fn in jobs:
            try:
                fn(self._c(name), pal)
            except RuntimeError:
                stale = True
            except Exception:
                import traceback
                traceback.print_exc()
        if stale:
            QTimer.singleShot(250, self._populateWhenReady)
        if not self._built:
            self._built = True
            self._loadAvatar()

    def _onThemeReady(self):
        try:
            self._buildAll()
        except Exception:
            import traceback
            traceback.print_exc()

    # -- top bar ---------------------------------------------------------- #
    def _topbar(self, c, pal):
        c.topBarFrame.setStyleSheet(
            "QFrame#topBarFrame{ background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            " stop:0 %s, stop:1 %s); }" % (pal["gradStart"], pal["gradEnd"]))
        c.headerTitle.setText(D.USER["name"])
        c.headerTitle.setStyleSheet("background:transparent; color:%s; font-size:20px; font-weight:800;" % pal["headerText"])
        c.headerSub.setText(D.USER["members"])
        c.headerSub.setStyleSheet("background:transparent; color:%s; font-size:11px; font-weight:700; letter-spacing:1px;" % pal["headerSub"])
        c.memberChevron.setStyleSheet("background: transparent;")
        c.memberChevron.setPixmap(icon_pixmap("chevron-down", pal["headerSub"], 14))
        c.memberChevron.setScaledContents(True)
        for i, name in enumerate(D.NAV):
            b = getattr(c, "navBtn%d" % i)
            b.setIcon(icon(name, pal["headerIcon"], 21)); b.setIconSize(QSize(21, 21))
        if not getattr(self, "_navWired", False):
            self._navWired = True
            c.navBtn6.clicked.connect(self._toggleTheme)   # settings icon -> theme
        # avatar (fallback until the async photo lands)
        self._avatarFallback(c, pal)

    def _avatarFallback(self, c, pal):
        s = 52 * 2
        pm = QPixmap(s, s); pm.fill(QColor(0, 0, 0, 0))
        p = QPainter(pm); p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen); p.setBrush(QBrush(QColor("#ffffff")))
        p.drawEllipse(0, 0, s, s)
        p.setBrush(QBrush(QColor(pal["gradEnd"])))
        p.drawEllipse(int(s * 0.30), int(s * 0.22), int(s * 0.40), int(s * 0.40))
        p.setBrush(QBrush(QColor(pal["gradEnd"])))
        p.drawEllipse(int(s * 0.18), int(s * 0.62), int(s * 0.64), int(s * 0.5))
        p.end(); pm.setDevicePixelRatio(2.0)
        c.avatar.setPixmap(pm); c.avatar.setScaledContents(True)

    # -- hello card ------------------------------------------------------- #
    def _hello(self, c, pal):
        c.welcome.setText(D.WELCOME)
        c.helloMenu.setIcon(icon("more-horizontal", pal["muted"], 18)); c.helloMenu.setIconSize(QSize(18, 18))
        for i, (ic, val, lab) in enumerate(D.WEATHER):
            col = pal["muted"] if i == 3 else pal["gradEnd"]
            getattr(c, "wIcon%d" % i).setPixmap(icon_pixmap(ic, col, 42))
            getattr(c, "wIcon%d" % i).setScaledContents(True)
            getattr(c, "wValue%d" % i).setText(val)
            getattr(c, "wLabel%d" % i).setText(lab)

    # -- gauges ----------------------------------------------------------- #
    def _gauges(self, c, pal):
        specs = [(c.tempGauge, D.GAUGES[0], "temp"), (c.powerGauge, D.GAUGES[1], "power")]
        for g, d, _k in specs:
            g.setRange(d["min"], d["max"]); g.value = d["value"]
            g.zonesCsv = ""                         # use the gradient, not zones
            g.showNeedle = False; g.showGuide = False; g.showScaleLabels = False
            g.showHandle = True; g.roundedCaps = True
            g.showTicks = True; g.tickCount = 40      # outer scale ring
            g.scaleColor = QColor(pal["gaugeTrack"])
            g.startAngle = 232.0; g.spanAngle = -284.0; g.arcWidth = 14
            g.glow = True; g.glowStrength = 0.4          # optional soft painted halo
            g.setGradient(pal[d["grad"] + "Start"], pal[d["grad"] + "End"])
            g.trackColor = QColor(pal["gaugeTrack"])
            g.innerColor = QColor(pal["gaugeInner"])
            g.centerTextColor = QColor(pal["gaugeText"])
            g.handleColor = QColor(pal["gaugeInner"])
            g.centerText = d["text"]; g.centerSuffix = d["suffix"]; g.statusText = ""
            g.centerIcon = _icon_path(d["icon"]); g.iconColor = QColor(pal["gaugeIcon"])
        c.tempTitle.setStyleSheet("background:transparent; color:%s; font-size:15px; font-weight:700;" % pal["text"])
        c.powerTitle.setStyleSheet("background:transparent; color:%s; font-size:15px; font-weight:700;" % pal["text"])
        c.gaugesMenu.setIcon(icon("more-horizontal", pal["muted"], 18)); c.gaugesMenu.setIconSize(QSize(18, 18))
        self._status(c.tempStatus, D.GAUGES[0], pal)
        self._status(c.powerStatus, D.GAUGES[1], pal)

    def _status(self, holder, d, pal):
        holder.setStyleSheet("background: transparent;")
        lay = holder.layout()
        while lay.count():
            it = lay.takeAt(0)
            w = it.widget()
            if w is not None:
                w.setParent(None); w.deleteLater()
        lay.addStretch(1)
        ic = QLabel(); ic.setFixedSize(15, 15); ic.setScaledContents(True)
        ic.setStyleSheet("background: transparent;")
        ic.setPixmap(icon_pixmap(d["sicon"], pal["muted"], 15))
        tx = QLabel(d["status"]); tx.setStyleSheet("background:transparent; color:%s; font-size:12px;" % pal["muted"])
        lay.addWidget(ic); lay.addWidget(tx); lay.addStretch(1)

    # -- devices ---------------------------------------------------------- #
    def _devices(self, c, pal):
        if not hasattr(self, "_devGroup"):
            self._devGroup = QButtonGroup(self.win); self._devGroup.setExclusive(True)
            self._devGrouped = False
        for i, (ic, cap) in enumerate(D.DEVICES):
            t = getattr(c, "tile%d" % i)
            t.setCaption(cap)
            t.setGradient(pal["gradStart"], pal["gradEnd"])
            t.bgColor = QColor(pal["tileBg"]); t.iconColor = QColor(pal["tileIcon"])
            t.activeColor = QColor(pal["onGrad"]); t.cornerRadius = 16; t.iconSize = 48
            t.setIconPath(_icon_path(ic))
            t.setChecked(i == D.DEVICE_ACTIVE)
            if not self._devGrouped and self._devGroup.id(t) < 0:
                self._devGroup.addButton(t, i)
        self._devGrouped = True

    # -- lighting --------------------------------------------------------- #
    def _lighting(self, c, pal):
        c.lightingTitle  # role-styled
        c.lightingMenu.setIcon(icon("more-horizontal", pal["muted"], 18)); c.lightingMenu.setIconSize(QSize(18, 18))
        c.bulbIcon.setPixmap(icon_pixmap("lightbulb", pal["gradEnd"], 88)); c.bulbIcon.setScaledContents(True)
        c.sunLow.setPixmap(icon_pixmap("sun", pal["muted"], 16)); c.sunLow.setScaledContents(True)
        c.sunHigh.setPixmap(icon_pixmap("sun", pal["gradEnd"], 20)); c.sunHigh.setScaledContents(True)
        c.brightness.setValue(D.LIGHTING["brightness"])
        c.brightness.setStyleSheet(
            "QSlider::groove:horizontal{ height:6px; border-radius:3px; background:%s; }"
            "QSlider::sub-page:horizontal{ height:6px; border-radius:3px;"
            " background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 %s, stop:1 %s); }"
            "QSlider::handle:horizontal{ width:16px; height:16px; margin:-6px 0;"
            " border-radius:8px; background:#ffffff; }" % (
                pal["sliderTrack"], pal["gradStart"], pal["gradEnd"]))
        c.roomLabel.setText(D.LIGHTING["room"])
        c.prevRoom.setIcon(icon("chevron-left", pal["muted"], 16)); c.prevRoom.setIconSize(QSize(16, 16))
        c.nextRoom.setIcon(icon("chevron-right", pal["muted"], 16)); c.nextRoom.setIconSize(QSize(16, 16))

    # -- security --------------------------------------------------------- #
    def _security(self, c, pal):
        c.securityMenu.setIcon(icon("more-horizontal", pal["muted"], 18)); c.securityMenu.setIconSize(QSize(18, 18))
        c.shieldIcon.setPixmap(icon_pixmap("shield", pal["gradEnd"], 88)); c.shieldIcon.setScaledContents(True)
        sw = c.lockSwitch
        try:
            sw.trackOnColor = QColor(pal["gradEnd"])
            sw.trackOffColor = QColor(pal["switchTrack"])
            sw.thumbColor = QColor("#ffffff")
        except Exception:
            pass
        sw.setChecked(bool(D.SECURITY["locked"]))
        c.lockLabel.setText("Locked" if sw.isChecked() else "Unlocked")
        if not getattr(self, "_lockWired", False):
            self._lockWired = True
            sw.toggled.connect(lambda v: c.lockLabel.setText("Locked" if v else "Unlocked"))
        c.doorLabel.setText(D.SECURITY["door"])
        c.prevDoor.setIcon(icon("chevron-left", pal["muted"], 16)); c.prevDoor.setIconSize(QSize(16, 16))
        c.nextDoor.setIcon(icon("chevron-right", pal["muted"], 16)); c.nextDoor.setIconSize(QSize(16, 16))

    # -- avatar (real photo, async) --------------------------------------- #
    def _loadAvatar(self):
        try:
            self._avT = QThread(self.win)
            self._avW = AvatarWorker("https://i.pravatar.cc/104?img=47")
            self._avW.moveToThread(self._avT)
            self._avT.started.connect(self._avW.run)
            self._avW.loaded.connect(self._onAvatar)
            self._avT.start()
        except Exception:
            pass

    def _onAvatar(self, raw):
        try:
            pm = QPixmap()
            if not pm.loadFromData(raw):
                return
            s = 52 * 2
            out = QPixmap(s, s); out.fill(QColor(0, 0, 0, 0))
            p = QPainter(out); p.setRenderHint(QPainter.Antialiasing, True)
            path = QPainterPath(); path.addEllipse(0, 0, s, s); p.setClipPath(path)
            sc = pm.scaled(s, s, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            p.drawPixmap(0, 0, sc); p.end(); out.setDevicePixelRatio(2.0)
            av = self._c("topBarContainer").avatar
            av.setPixmap(out); av.setScaledContents(True)
        except Exception:
            pass
        finally:
            try:
                self._avT.quit()
            except Exception:
                pass

    # -- theme ------------------------------------------------------------ #
    def _toggleTheme(self):
        if self.themeEngine is None:
            return
        target = T.THEME_LIGHT if T.is_dark(self._theme()) else T.THEME_DARK
        self.themeEngine.setTheme(target)
