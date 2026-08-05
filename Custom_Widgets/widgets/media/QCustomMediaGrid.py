########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomMediaGrid - a data-driven thumbnail gallery.
##
## The "Media, Files & Links" photo grid: a responsive grid of rounded
## thumbnails. Feed it images with setImages([...]) (QPixmap / path) or coloured
## placeholders with setPlaceholders([(top,bottom), …]); it lays them out in
## `columns` with rounded corners and emits `tileClicked(index)` so a manager
## can open a viewer. Layout, corner radius and spacing are Designer
## qproperties — the manager supplies DATA only, never builds tiles.
########################################################################
from qtpy.QtCore import Qt, Property, Signal, QSize
from qtpy.QtGui import QColor, QPixmap, QPainter, QPainterPath, QBrush, QLinearGradient
from qtpy.QtWidgets import QLabel, QWidget, QGridLayout, QSizePolicy


class _Tile(QLabel):
    clicked = Signal(int)

    def __init__(self, index, radius, parent=None):
        super().__init__(parent)
        self._index = index
        self._radius = radius
        self.setObjectName("mediaTile%d" % index)
        self.setScaledContents(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(10, 10)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def setRoundedPixmap(self, pm):
        self.setPixmap(_rounded(pm, self._radius))

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit(self._index)
        super().mousePressEvent(e)


def _rounded(pm, radius):
    if pm is None or pm.isNull():
        return QPixmap()
    out = QPixmap(pm.size())
    out.setDevicePixelRatio(pm.devicePixelRatio())
    out.fill(QColor(0, 0, 0, 0))
    p = QPainter(out)
    p.setRenderHint(QPainter.Antialiasing, True)
    path = QPainterPath()
    path.addRoundedRect(0, 0, pm.width(), pm.height(), radius, radius)
    p.setClipPath(path)
    p.drawPixmap(0, 0, pm)
    p.end()
    return out


def _gradient(top, bottom, w=220, h=150, radius=22):
    pm = QPixmap(w, h)
    pm.fill(QColor(0, 0, 0, 0))
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    g = QLinearGradient(0, 0, w, h)
    g.setColorAt(0.0, QColor(top))
    g.setColorAt(1.0, QColor(bottom))
    p.setPen(Qt.NoPen)
    p.setBrush(QBrush(g))
    p.drawRoundedRect(0, 0, w, h, radius, radius)
    p.end()
    return pm


class QCustomMediaGrid(QWidget):

    tileClicked = Signal(int)

    WIDGET_ICON = "components/icons/media_grid.png"
    WIDGET_TOOLTIP = "A data-driven thumbnail gallery"
    WIDGET_MODULE = "Custom_Widgets.QCustomMediaGrid"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomMediaGrid' name='customMediaGrid'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>280</width><height>200</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomMediaGrid",
        "props": {"columns": {"type": "int", "default": 3},
                  "spacing": {"type": "int", "default": 8},
                  "tileRadius": {"type": "int", "default": 12},
                  "tileHeight": {"type": "int", "default": 60}},
        "signals": ["tileClicked"],
        "tokens_used": [],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomMediaGrid")
        self._columns = 3
        self._spacing = 8
        self._radius = 12
        self._tile_h = 60
        self._pixmaps = []
        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setHorizontalSpacing(self._spacing)
        self._grid.setVerticalSpacing(self._spacing)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    # ------------------------------------------------------------------ #
    ## Data API — manager supplies DATA, the widget builds the tiles.
    # ------------------------------------------------------------------ #
    def setImages(self, images):
        self._pixmaps = [im if isinstance(im, QPixmap) else QPixmap(str(im)) for im in (images or [])]
        self._rebuild()

    def setPlaceholders(self, pairs):
        self._pixmaps = [_gradient(a, b) for (a, b) in (pairs or [])]
        self._rebuild()

    def setImageAt(self, index, pm):
        """Swap one tile's pixmap in place (e.g. a real photo arriving async).
        Also updates the stored pixmap so pixmaps() reflects the real image."""
        pm = pm if isinstance(pm, QPixmap) else QPixmap(str(pm))
        if 0 <= index < len(self._pixmaps):
            self._pixmaps[index] = pm
        if 0 <= index < len(self._tiles):
            self._tiles[index].setRoundedPixmap(pm)

    def count(self):
        return len(self._pixmaps)

    def pixmaps(self):
        """The current tile pixmaps (for feeding a lightbox / viewer)."""
        return list(self._pixmaps)

    _tiles = []

    def _rebuild(self):
        while self._grid.count():
            it = self._grid.takeAt(0)
            w = it.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        self._tiles = []
        for i, pm in enumerate(self._pixmaps):
            tile = _Tile(i, self._radius, self)
            tile.setFixedHeight(self._tile_h)
            tile.setRoundedPixmap(pm)
            tile.clicked.connect(self.tileClicked)
            self._grid.addWidget(tile, i // self._columns, i % self._columns)
            self._tiles.append(tile)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(int)
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, v):
        self._columns = max(1, int(v))
        self._rebuild()

    @Property(int)
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, v):
        self._spacing = max(0, int(v))
        self._grid.setHorizontalSpacing(self._spacing)
        self._grid.setVerticalSpacing(self._spacing)

    @Property(int)
    def tileRadius(self):
        return self._radius

    @tileRadius.setter
    def tileRadius(self, v):
        self._radius = max(0, int(v))
        self._rebuild()

    @Property(int)
    def tileHeight(self):
        return self._tile_h

    @tileHeight.setter
    def tileHeight(self, v):
        self._tile_h = max(20, int(v))
        for t in self._tiles:
            t.setFixedHeight(self._tile_h)
