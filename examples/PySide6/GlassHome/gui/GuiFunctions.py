"""GlassHome — GUI orchestration (the CORRECT Custom_Widgets way).

The window shell (ui/MainWindow.ui) is a full-bleed ``wallpaper`` QLabel with a
glass overlay: every panel is a QCustomGlassFrame sampling that label
(backdropSource="wallpaper").  ALL chrome colours come from Qss/scss via theme
tokens; managers here only feed CONTENT (texts, images, values, wiring) and
re-assert the glass after async events (photo arrival, theme switch).
"""

import os

from qtpy.QtCore import QObject, Qt, QTime, QTimer, QRectF
from qtpy.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPixmap
from qtpy.QtWidgets import QButtonGroup

import Custom_Widgets
from Custom_Widgets.ImageLoader import load_image
from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame

from gui import data as D
from gui import theme as T

_ICONS = os.path.join(os.path.dirname(Custom_Widgets.__file__), "Qss", "icons")
_FEATHER = os.path.join(_ICONS, "feather")


def _feather(name):
    return os.path.join(_FEATHER, name + ".svg")


def _repolish(widget):
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def _rounded(pixmap, w, h, radius):
    """Scale-crop ``pixmap`` to w×h with rounded corners (2x for crispness)."""
    out = QPixmap(w * 2, h * 2)
    out.fill(QColor(0, 0, 0, 0))
    p = QPainter(out)
    p.setRenderHint(QPainter.Antialiasing, True)
    path = QPainterPath()
    path.addRoundedRect(QRectF(0, 0, w * 2, h * 2), radius * 2, radius * 2)
    p.setClipPath(path)
    scaled = pixmap.scaled(w * 2, h * 2, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    p.drawPixmap((w * 2 - scaled.width()) // 2, (h * 2 - scaled.height()) // 2, scaled)
    p.end()
    out.setDevicePixelRatio(2.0)
    return out


class WallpaperManager(QObject):
    """Full-bleed dusk photo behind the glass; themed gradient fallback while
    (or if) the download never lands. Every arrival refreshes ALL glass."""

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self._have_photo = False

    def initialize(self):
        self._paint_fallback()
        load_image(D.WALLPAPER_URL, self._on_photo)

    def _wallpaper(self):
        return self.window.ui.wallpaper

    def _paint_fallback(self):
        pal = T.palette(self.window)
        pm = QPixmap(1600, 1000)
        g = QLinearGradient(0, 0, 400, 1000)
        g.setColorAt(0.0, QColor(pal.get("wallTop", "#2b3550")))
        g.setColorAt(0.5, QColor(pal.get("wallMid", "#4c4668")))
        g.setColorAt(1.0, QColor(pal.get("wallBottom", "#1a1e30")))
        p = QPainter(pm)
        p.fillRect(pm.rect(), g)
        p.end()
        self._wallpaper().setPixmap(pm)
        self.refresh_glass()

    def _on_photo(self, pm):
        if pm is None or pm.isNull():
            return
        self._have_photo = True
        self._wallpaper().setPixmap(pm)
        self.refresh_glass()

    def on_theme_changed(self):
        if not self._have_photo:
            self._paint_fallback()
        else:
            self.refresh_glass()

    def refresh_glass(self):
        for glass in self.window.findChildren(QCustomGlassFrame):
            glass.refreshBackdrop()


class HeroManager(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def initialize(self):
        hero = self.window.ui.heroContainer.component
        load_image(D.LAMP_URL, lambda pm: self._set_lamp(pm))

    def _set_lamp(self, pm):
        if pm is None or pm.isNull():
            return
        hero = self.window.ui.heroContainer.component
        hero.lampImage.setPixmap(_rounded(pm, 128, 216, 18))


class StatsManager(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def initialize(self):
        for container_name, label, value in D.STATS:
            card = getattr(self.window.ui, container_name).component
            card.statLabel.setText(label)
            card.statValue.setText(value)


class TilesManager(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def initialize(self):
        for container_name, vendor, name, on in D.TILES:
            tile = getattr(self.window.ui, container_name).component
            tile.tileVendor.setText(vendor)
            tile.tileName.setText(name)
            tile.tileSwitch.setChecked(on)
            self._apply_active(tile, on)
            tile.tileSwitch.toggled.connect(
                lambda checked, t=tile: self._apply_active(t, checked))

    @staticmethod
    def _apply_active(tile, on):
        tile.tileGlass.setProperty("active", "true" if on else "false")
        _repolish(tile.tileGlass)
        for label in (tile.tileVendor, tile.tileName, tile.tileApps):
            _repolish(label)


class ThermostatManager(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick_clock)

    def initialize(self):
        panel = self.window.ui.thermoContainer.component
        panel.thermoMinus.clicked.connect(lambda: self._nudge(-1))
        panel.thermoPlus.clicked.connect(lambda: self._nudge(+1))
        panel.thermoSwitch.toggled.connect(self._on_switch)
        self._tick_clock()
        self._timer.start()

    def _panel(self):
        return self.window.ui.thermoContainer.component

    def _tick_clock(self):
        self._panel().clockLabel.setText(QTime.currentTime().toString("h:mm AP"))

    def _nudge(self, delta):
        gauge = self._panel().thermoGauge
        value = max(gauge.minimum, min(gauge.maximum, float(gauge.value) + delta))
        gauge.setValue(value)
        gauge.centerText = "%d" % round(value)

    def _on_switch(self, on):
        gauge = self._panel().thermoGauge
        gauge.setEnabled(on)


class ModeManager(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)

    def initialize(self):
        row = self.window.ui.modeContainer.component
        for name, icon in D.MODE_ICONS.items():
            btn = getattr(row, name)
            btn.setIconPath(_feather(icon))
            self._group.addButton(btn)


class PlayerManager(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self._elapsed = D.TRACK_START
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)

    def initialize(self):
        player = self._player()
        player.setCoverSource(D.COVER_URL)
        player.playToggled.connect(self._on_play_toggled)
        self._apply()
        self._timer.start()

    def _player(self):
        return self.window.ui.playerContainer.component.player

    def _on_play_toggled(self, playing):
        self._timer.start() if playing else self._timer.stop()

    def _tick(self):
        self._elapsed = (self._elapsed + 1) % D.TRACK_SECONDS
        self._apply()

    def _apply(self):
        player = self._player()
        player.elapsedText = "%d:%02d" % divmod(self._elapsed, 60)
        player.position = self._elapsed / float(D.TRACK_SECONDS)


class RoomsManager(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def initialize(self):
        tabs = self.window.ui.roomTabsContainer.component
        tabs.roomSegments.currentChanged.connect(
            lambda i: tabs.roomDots.setActiveIndex(i))
        tabs.roomDots.pageChanged.connect(
            lambda i: tabs.roomSegments.setCurrentIndex(i))


class NavManager(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def initialize(self):
        rail = self.window.ui.navRailContainer.component
        rail.navAvatar.setImageSource(D.AVATAR_URL)
        # Avatar click flips Glass Dusk <-> Glass Day — always BY NAME
        # (the generic Light/Dark toggle can't match a custom theme).
        rail.navAvatar.clicked.connect(self._toggle_theme)

    def _toggle_theme(self):
        engine = getattr(self.window, "themeEngine", None)
        if engine is None:
            return
        current = T.current_theme_name(self.window)
        engine.setTheme("Glass Day" if current == "Glass Dusk" else "Glass Dusk")


class GuiFunctions(QObject):
    """Orchestrator: one manager per panel + theme-switch re-assertion."""

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.wallpaper = WallpaperManager(window)
        self.managers = [
            self.wallpaper,
            HeroManager(window),
            StatsManager(window),
            TilesManager(window),
            ThermostatManager(window),
            ModeManager(window),
            PlayerManager(window),
            RoomsManager(window),
            NavManager(window),
        ]

    def initialize(self):
        self._make_containers_translucent()
        for manager in self.managers:
            manager.initialize()
        engine = getattr(self.window, "themeEngine", None)
        if engine is not None and hasattr(engine, "onThemeChangeComplete"):
            engine.onThemeChangeComplete.connect(self._on_theme_changed)

    def _make_containers_translucent(self):
        """Component containers sit ON glass — a native holder painting the
        palette would black the panel out (known native-container gotcha).
        NB: container.component is the Ui_ OBJECT, not a widget — walk the
        container's real child widgets instead."""
        from qtpy.QtWidgets import QWidget
        ui = self.window.ui
        for name in ("thermoContainer", "modeContainer", "playerContainer",
                     "navRailContainer", "roomTabsContainer"):
            container = getattr(ui, name, None)
            if container is None:
                continue
            container.setAttribute(Qt.WA_TranslucentBackground, True)
            for child in container.children():
                if isinstance(child, QWidget):
                    child.setAttribute(Qt.WA_TranslucentBackground, True)

    def _on_theme_changed(self):
        # qproperty-* colours don't reliably re-apply on a live switch — force a
        # full repolish so the compiled sheet re-lands, then re-sample the glass.
        for widget in self.window.findChildren(QObject):
            if hasattr(widget, "style") and callable(getattr(widget, "style", None)):
                try:
                    _repolish(widget)
                except Exception:
                    pass
        self.wallpaper.on_theme_changed()
