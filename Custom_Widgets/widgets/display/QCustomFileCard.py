########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomFileCard - a file / attachment row.
##
## The row seen under the "Files" tab: a painted rounded badge with the file
## extension ("PDF", "ZIP", …) coloured by type, the file name (elided) and a
## meta line (size · date), plus a painted download button. Feed it data with
## setFile(name, size, ext=None, date=None) or the Designer qproperties; the
## badge colour is auto-picked from the extension unless badgeColor is set.
## Emits downloadClicked() and clicked(). The card panel + text colours are
## driven from the app QSS (objectName selectors) so they flip with the theme.
########################################################################
import os

from qtpy.QtCore import Qt, Property, Signal, QRectF
from qtpy.QtGui import QColor, QPainter, QBrush, QPen, QPolygonF, QFont
from qtpy.QtCore import QPointF
from qtpy.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy


_EXT_COLORS = {
    "pdf": "#f0524b", "doc": "#2b7cff", "docx": "#2b7cff", "txt": "#7b8494",
    "xls": "#1f9d55", "xlsx": "#1f9d55", "csv": "#1f9d55",
    "ppt": "#e8703a", "pptx": "#e8703a",
    "zip": "#b06fd6", "rar": "#b06fd6", "7z": "#b06fd6",
    "png": "#12b5b0", "jpg": "#12b5b0", "jpeg": "#12b5b0", "gif": "#12b5b0", "svg": "#12b5b0",
    "mp3": "#e5497d", "wav": "#e5497d", "mp4": "#8a63d2", "mov": "#8a63d2",
}


class _Badge(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ext = "FILE"
        self._color = QColor("#2b7cff")
        self._radius = 12
        self.setFixedSize(46, 46)

    def setExt(self, ext, color):
        self._ext = (ext or "FILE").upper()[:4]
        self._color = QColor(color)
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._color))
        p.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), self._radius, self._radius)
        f = QFont(self.font())
        f.setPointSizeF(8.5 if len(self._ext) > 3 else 9.5)
        f.setWeight(QFont.Black)
        p.setFont(f)
        p.setPen(QPen(QColor("#ffffff")))
        p.drawText(self.rect(), Qt.AlignCenter, self._ext)
        p.end()


class _DownloadButton(QWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._fg = QColor("#7b8494")
        self._hover = False
        self.setFixedSize(34, 34)
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover, True)

    def setColor(self, c):
        self._fg = QColor(c)
        self.update()

    def enterEvent(self, e):
        self._hover = True
        self.update()

    def leaveEvent(self, e):
        self._hover = False
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        c = self.rect().center()
        col = QColor(self._fg)
        if self._hover:
            col = col.lighter(125)
        pen = QPen(col, 2.0)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        cx, cy = c.x() + 0.5, c.y() + 0.5
        p.drawLine(QPointF(cx, cy - 7), QPointF(cx, cy + 4))
        p.drawPolyline(QPolygonF([QPointF(cx - 4, cy), QPointF(cx, cy + 4), QPointF(cx + 4, cy)]))
        p.drawLine(QPointF(cx - 6, cy + 8), QPointF(cx + 6, cy + 8))
        p.end()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
        e.accept()


class QCustomFileCard(QWidget):

    clicked = Signal()
    downloadClicked = Signal()

    WIDGET_ICON = "components/icons/description.png"
    WIDGET_TOOLTIP = "A file / attachment row"
    WIDGET_MODULE = "Custom_Widgets.QCustomFileCard"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomFileCard' name='customFileCard'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>260</width><height>64</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomFileCard",
        "props": {
            "fileName": {"type": "string", "default": "Document.pdf"},
            "fileSize": {"type": "string", "default": "1.2 MB"},
            "fileExt": {"type": "string", "default": ""},
            "fileDate": {"type": "string", "default": ""},
            "badgeColor": {"type": "color", "default": "#00000000"},
            "iconColor": {"type": "color", "default": "#7b8494"},
        },
        "signals": ["clicked", "downloadClicked"],
        "tokens_used": [],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomFileCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._ext_override = ""
        self._badge_override = QColor(0, 0, 0, 0)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(12)

        self._badge = _Badge(self)
        mid = QVBoxLayout()
        mid.setContentsMargins(0, 0, 0, 0)
        mid.setSpacing(2)
        self._name = QLabel("Document.pdf")
        self._name.setObjectName("fileCardName")
        self._meta = QLabel("1.2 MB")
        self._meta.setObjectName("fileCardMeta")
        mid.addWidget(self._name)
        mid.addWidget(self._meta)

        self._dl = _DownloadButton(self)
        self._dl.clicked.connect(self.downloadClicked)

        lay.addWidget(self._badge, 0)
        lay.addLayout(mid, 1)
        lay.addWidget(self._dl, 0)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        self._apply_badge()

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setFile(self, name, size="", ext=None, date=None):
        self._name.setText(str(name))
        meta = str(size)
        if date:
            meta = "%s  ·  %s" % (meta, date) if meta else str(date)
        self._meta.setText(meta)
        if ext is not None:
            self._ext_override = str(ext)
        self._apply_badge()

    def _resolved_ext(self):
        if self._ext_override:
            return self._ext_override
        base = self._name.text()
        _, dot, tail = base.rpartition(".")
        return tail if dot else "file"

    def _apply_badge(self):
        ext = self._resolved_ext().lower()
        if self._badge_override.alpha() > 0:
            color = self._badge_override
        else:
            color = QColor(_EXT_COLORS.get(ext, "#5a6478"))
        self._badge.setExt(ext, color)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def fileName(self):
        return self._name.text()

    @fileName.setter
    def fileName(self, v):
        self._name.setText(str(v))
        self._apply_badge()

    @Property(str)
    def fileSize(self):
        return self._meta.text()

    @fileSize.setter
    def fileSize(self, v):
        self._meta.setText(str(v))

    @Property(str)
    def fileExt(self):
        return self._ext_override

    @fileExt.setter
    def fileExt(self, v):
        self._ext_override = str(v)
        self._apply_badge()

    @Property(str)
    def fileDate(self):
        return ""

    @fileDate.setter
    def fileDate(self, v):
        if v:
            base = self._meta.text().split("  ·  ")[0]
            self._meta.setText("%s  ·  %s" % (base, v))

    @Property(QColor)
    def badgeColor(self):
        return self._badge_override

    @badgeColor.setter
    def badgeColor(self, c):
        self._badge_override = QColor(c)
        self._apply_badge()

    @Property(QColor)
    def iconColor(self):
        return self._dl._fg

    @iconColor.setter
    def iconColor(self, c):
        self._dl.setColor(QColor(c))
