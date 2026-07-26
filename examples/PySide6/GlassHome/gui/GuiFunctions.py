"""GlassHome — GUI orchestration (the CORRECT Custom_Widgets way).

After pushing the chrome work into the library, managers here are ONLY demo
CONTENT + signal wiring. The framework handles the rest declaratively:
wallpaper photo + themed fallback (QCustomWallpaper, glass frames auto-resample
when it loads), the rounded lamp photo (QCustomQLabel imageSource), the clock
(QCustomClockLabel), the theme flip (QCustomThemeDarkLightToggle darkTheme/
lightTheme), chart selection (QCustomMiniBarChart selectOnClick), player time
maths (QCustomPlayerBar elapsedSeconds/durationSeconds), theme-switch
re-polish (the theme engine), and container translucency (the loader).
"""

import os

from qtpy.QtCore import QObject, QTimer
from qtpy.QtWidgets import QButtonGroup

import Custom_Widgets
from Custom_Widgets import set_state

from gui import data as D

_ICONS = os.path.join(os.path.dirname(Custom_Widgets.__file__), "Qss", "icons")
_FEATHER = os.path.join(_ICONS, "feather")


def _feather(name):
    return os.path.join(_FEATHER, name + ".svg")


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
            set_state(tile.tileGlass, "active", on)
            tile.tileSwitch.toggled.connect(
                lambda checked, t=tile: set_state(t.tileGlass, "active", checked))


class ThermostatManager(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def initialize(self):
        panel = self.window.ui.thermoContainer.component
        panel.thermoMinus.clicked.connect(panel.thermoGauge.stepDown)
        panel.thermoPlus.clicked.connect(panel.thermoGauge.stepUp)
        panel.thermoSwitch.toggled.connect(panel.thermoGauge.setEnabled)


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
    """Simulated playback: tick elapsed seconds — the bar formats the time and
    derives the seek position itself."""

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)

    def initialize(self):
        player = self._player()
        player.playToggled.connect(
            lambda playing: self._timer.start() if playing else self._timer.stop())
        self._timer.start()

    def _player(self):
        return self.window.ui.playerContainer.component.player

    def _tick(self):
        player = self._player()
        player.elapsedSeconds = (player.elapsedSeconds + 1) % max(1.0, player.durationSeconds)


class RoomsManager(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def initialize(self):
        tabs = self.window.ui.roomTabsContainer.component
        tabs.roomDots.bindTo(tabs.roomSegments)


class GuiFunctions(QObject):
    """Orchestrator: one manager per panel — content + wiring only."""

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.managers = [
            StatsManager(window),
            TilesManager(window),
            ThermostatManager(window),
            ModeManager(window),
            PlayerManager(window),
            RoomsManager(window),
        ]

    def initialize(self):
        for manager in self.managers:
            manager.initialize()
