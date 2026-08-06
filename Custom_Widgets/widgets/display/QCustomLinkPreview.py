########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomLinkPreview - a shared-link preview card.
##
## The row seen under the "Links" tab: a rounded thumbnail (a real favicon /
## image via setThumbnail, or a painted gradient with the site initial as a
## fallback), the link title (bold, elided), the domain (muted) and an optional
## one-line description. Feed it with setLink(title, url, description=None,
## thumbnail=None) or the Designer qproperties. Clicking emits clicked(url).
## The card panel + text colours are driven from the app QSS (objectName
## selectors) so they flip with the theme.
########################################################################
from qtpy.QtCore import Qt, Property, Signal, QRectF
from qtpy.QtGui import (QColor, QPainter, QBrush, QFont, QPixmap, QLinearGradient,
                        QPainterPath, QFontMetrics)
from qtpy.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy


def _domain_of(url):
    u = str(url or "")
    for pre in ("https://", "http://"):
        if u.startswith(pre):
            u = u[len(pre):]
            break
    if u.startswith("www."):
        u = u[4:]
    return u.split("/")[0] or u


class _Thumb(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pm = QPixmap()
        self._initial = "#"
        self._c1 = QColor("#4b6cff")
        self._c2 = QColor("#8a5cf6")
        self._radius = 12
        self.setFixedSize(56, 56)

    def setSeed(self, text):
        t = (text or "#").strip()
        self._initial = (t[:1] or "#").upper()
        h = 0
        for ch in t:
            h = (h * 131 + ord(ch)) & 0xFFFFFF
        hue1 = h % 360
        hue2 = (hue1 + 40) % 360
        self._c1 = QColor.fromHsv(hue1, 150, 220)
        self._c2 = QColor.fromHsv(hue2, 170, 180)
        self.update()

    def setPixmap(self, pm):
        self._pm = pm if isinstance(pm, QPixmap) else QPixmap(str(pm))
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        rect = QRectF(0, 0, self.width(), self.height())
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)
        p.setClipPath(path)
        if not self._pm.isNull():
            scaled = self._pm.size().scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding)
            x = (self.width() - scaled.width()) / 2.0
            y = (self.height() - scaled.height()) / 2.0
            p.drawPixmap(QRectF(x, y, scaled.width(), scaled.height()).toRect(), self._pm)
        else:
            g = QLinearGradient(0, 0, self.width(), self.height())
            g.setColorAt(0.0, self._c1)
            g.setColorAt(1.0, self._c2)
            p.fillRect(rect, QBrush(g))
            f = QFont(self.font())
            f.setPointSizeF(18)
            f.setWeight(QFont.Black)
            p.setFont(f)
            p.setPen(QColor("#ffffff"))
            p.drawText(rect, Qt.AlignCenter, self._initial)
        p.end()


class QCustomLinkPreview(QWidget):

    clicked = Signal(str)

    WIDGET_ICON = "components/icons/link.png"
    WIDGET_TOOLTIP = "A shared-link preview card"
    WIDGET_MODULE = "Custom_Widgets.QCustomLinkPreview"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomLinkPreview' name='customLinkPreview'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>260</width><height>76</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomLinkPreview",
        "props": {
            "title": {"type": "string", "default": "Shared link"},
            "url": {"type": "string", "default": "example.com"},
            "description": {"type": "string", "default": ""},
        },
        "signals": ["clicked"],
        "tokens_used": [],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomLinkPreview")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._url = "example.com"

        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(12)

        self._thumb = _Thumb(self)
        mid = QVBoxLayout()
        mid.setContentsMargins(0, 0, 0, 0)
        mid.setSpacing(2)
        self._title = QLabel("Shared link")
        self._title.setObjectName("linkPreviewTitle")
        self._domain = QLabel("example.com")
        self._domain.setObjectName("linkPreviewDomain")
        self._desc = QLabel("")
        self._desc.setObjectName("linkPreviewDesc")
        self._desc.setVisible(False)
        mid.addWidget(self._title)
        mid.addWidget(self._domain)
        mid.addWidget(self._desc)

        lay.addWidget(self._thumb, 0, Qt.AlignTop)
        lay.addLayout(mid, 1)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        self._full_title = "Shared link"
        self._thumb.setSeed(_domain_of(self._url))

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setLink(self, title, url, description=None, thumbnail=None):
        self._full_title = str(title)
        self._url = str(url)
        self._domain.setText(_domain_of(url))
        if description:
            self._desc.setText(str(description))
            self._desc.setVisible(True)
        else:
            self._desc.setVisible(False)
        if thumbnail is not None:
            self._thumb.setPixmap(thumbnail)
        else:
            self._thumb.setSeed(_domain_of(url))
        self._relayout_title()

    def setThumbnail(self, pm):
        self._thumb.setPixmap(pm)

    def _relayout_title(self):
        fm = QFontMetrics(self._title.font())
        avail = max(60, self._title.width())
        self._title.setText(fm.elidedText(self._full_title, Qt.ElideRight, avail))

    def resizeEvent(self, e):
        self._relayout_title()
        super().resizeEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit(self._url)
        super().mousePressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def title(self):
        return self._full_title

    @title.setter
    def title(self, v):
        self._full_title = str(v)
        self._relayout_title()

    @Property(str)
    def url(self):
        return self._url

    @url.setter
    def url(self, v):
        self._url = str(v)
        self._domain.setText(_domain_of(v))
        self._thumb.setSeed(_domain_of(v))

    @Property(str)
    def description(self):
        return self._desc.text()

    @description.setter
    def description(self, v):
        self._desc.setText(str(v))
        self._desc.setVisible(bool(v))
