########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomAvatar - a single circular avatar with an optional status dot.
##
## Shows either initials (text) or an image, clipped to a circle, over a solid
## fill. An optional status / notification dot sits in a corner with a ring that
## separates it from whatever is behind the avatar (set statusBorderColor to the
## surface colour). An optional outer ring frames the whole avatar. Everything is
## painted with QPainter so it stays crisp at any size and needs no children.
## Emits `clicked` so it can act as a profile button.
##
## (QCustomAvatarGroup already exists for a row of overlapping avatars; this is
## the single, status-aware building block.)
########################################################################
from qtpy.QtCore import Qt, Property, Signal, QRectF
from qtpy.QtGui import QColor, QPainter, QBrush, QPen, QPixmap, QPainterPath, QFont
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomAvatar(QWidget):

    clicked = Signal()

    WIDGET_ICON = "components/icons/account_circle.png"
    WIDGET_TOOLTIP = "A circular avatar with an optional status dot"
    WIDGET_MODULE = "Custom_Widgets.QCustomAvatar"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomAvatar' name='customAvatar'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>48</width><height>48</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomAvatar",
        "props": {"text": {"type": "string", "default": "M"},
                  "bgColor": {"type": "color", "default": "#3355e8"},
                  "textColor": {"type": "color", "default": "#ffffff"},
                  "showStatus": {"type": "bool", "default": True},
                  "statusColor": {"type": "color", "default": "#f2704e"},
                  "statusPosition": {"type": "enum",
                                     "values": ["top-right", "bottom-right", "top-left", "bottom-left"],
                                     "default": "top-right"},
                  "statusBorderColor": {"type": "color", "default": "#ffffff"},
                  "ringColor": {"type": "color", "default": "#00000000"},
                  "ringWidth": {"type": "int", "default": 0},
                  "cornerRadius": {"type": "int", "default": -1},
                  "imageSource": {"type": "string", "default": ""}},
        "signals": ["clicked"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, text="M", image=None):
        super().__init__(parent)
        self.setObjectName("QCustomAvatar")
        self._text = str(text)
        self._pixmap = None
        self._img_source = ""
        self._bg = QColor("#3355e8")
        self._text_color = QColor("#ffffff")
        self._show_status = True
        self._status_color = QColor("#f2704e")
        self._status_pos = "top-right"
        self._status_border = QColor("#ffffff")
        self._status_ratio = 0.28       # dot diameter as fraction of avatar
        self._ring_color = QColor(0, 0, 0, 0)
        self._ring_width = 0
        self._font_ratio = 0.42
        self._corner_radius = -1        # -1 = circle; >=0 = rounded-square radius
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMinimumSize(24, 24)
        self.setCursor(Qt.PointingHandCursor)
        if image is not None:
            self.setImage(image)

    # ------------------------------------------------------------------ #
    ## Content API
    # ------------------------------------------------------------------ #
    def setText(self, text):
        self._text = str(text)
        self._pixmap = None
        self.update()

    def setImage(self, image):
        if isinstance(image, str):
            image = QPixmap(image)
        self._pixmap = image if isinstance(image, QPixmap) and not image.isNull() else None
        self.update()

    def setImageSource(self, source):
        """Set the avatar image from a local PATH or an http(s) URL — the URL is
        downloaded + disk-cached asynchronously (see Custom_Widgets.ImageLoader)
        and the circular crop is handled by paintEvent. Falls back to the
        initials until the image lands."""
        self._img_source = str(source or "")
        if not self._img_source:
            self._pixmap = None
            self.update()
            return
        from Custom_Widgets.ImageLoader import load_image
        load_image(self._img_source, self.setImage)

    def setBgColor(self, c):
        self._bg = QColor(c)
        self.update()

    def setStatus(self, visible, color=None):
        self._show_status = bool(visible)
        if color is not None:
            self._status_color = QColor(color)
        self.update()

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        side = min(self.width(), self.height())
        cx = (self.width() - side) / 2.0
        cy = (self.height() - side) / 2.0
        inset = self._ring_width + 1 if self._ring_width > 0 else 0
        rounded = self._corner_radius is not None and self._corner_radius >= 0

        # outer ring
        if self._ring_width > 0 and self._ring_color.alpha() > 0:
            pen = QPen(self._ring_color, self._ring_width)
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            r = QRectF(cx + self._ring_width / 2.0, cy + self._ring_width / 2.0,
                       side - self._ring_width, side - self._ring_width)
            if rounded:
                p.drawRoundedRect(r, self._corner_radius, self._corner_radius)
            else:
                p.drawEllipse(r)

        face = QRectF(cx + inset, cy + inset, side - 2 * inset, side - 2 * inset)

        if self._pixmap is not None:
            path = QPainterPath()
            if rounded:
                path.addRoundedRect(face, self._corner_radius, self._corner_radius)
            else:
                path.addEllipse(face)
            p.setClipPath(path)
            scaled = self._pixmap.scaled(int(face.width()), int(face.height()),
                                         Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            ox = face.x() - (scaled.width() - face.width()) / 2.0
            oy = face.y() - (scaled.height() - face.height()) / 2.0
            p.drawPixmap(int(ox), int(oy), scaled)
            p.setClipping(False)
        else:
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._bg))
            if rounded:
                p.drawRoundedRect(face, self._corner_radius, self._corner_radius)
            else:
                p.drawEllipse(face)
            f = QFont(self.font())
            f.setPixelSize(max(8, int(face.height() * self._font_ratio)))
            f.setBold(True)
            p.setFont(f)
            p.setPen(QPen(self._text_color))
            p.drawText(face, Qt.AlignCenter, self._text)

        # status dot
        if self._show_status:
            d = max(6.0, side * self._status_ratio)
            ring = max(1.5, d * 0.22)
            if "right" in self._status_pos:
                dx = cx + side - d
            else:
                dx = cx
            if "top" in self._status_pos:
                dy = cy
            else:
                dy = cy + side - d
            # border ring (separates dot from the surface behind)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._status_border))
            p.drawEllipse(QRectF(dx - ring, dy - ring, d + 2 * ring, d + 2 * ring))
            p.setBrush(QBrush(self._status_color))
            p.drawEllipse(QRectF(dx, dy, d, d))
        p.end()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def text(self):
        return self._text

    @text.setter
    def text(self, v):
        self.setText(v)

    @Property(str)
    def imageSource(self):
        return self._img_source

    @imageSource.setter
    def imageSource(self, v):
        self.setImageSource(v)

    @Property(int)
    def cornerRadius(self):
        return self._corner_radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._corner_radius = int(v)     # -1 = circle; >=0 = rounded-square radius
        self.update()

    @Property(QColor)
    def bgColor(self):
        return self._bg

    @bgColor.setter
    def bgColor(self, c):
        self._bg = QColor(c)
        self.update()

    @Property(QColor)
    def textColor(self):
        return self._text_color

    @textColor.setter
    def textColor(self, c):
        self._text_color = QColor(c)
        self.update()

    @Property(bool)
    def showStatus(self):
        return self._show_status

    @showStatus.setter
    def showStatus(self, v):
        self._show_status = bool(v)
        self.update()

    @Property(QColor)
    def statusColor(self):
        return self._status_color

    @statusColor.setter
    def statusColor(self, c):
        self._status_color = QColor(c)
        self.update()

    @Property(str)
    def statusPosition(self):
        return self._status_pos

    @statusPosition.setter
    def statusPosition(self, v):
        v = str(v)
        if v in ("top-right", "bottom-right", "top-left", "bottom-left"):
            self._status_pos = v
            self.update()

    @Property(QColor)
    def statusBorderColor(self):
        return self._status_border

    @statusBorderColor.setter
    def statusBorderColor(self, c):
        self._status_border = QColor(c)
        self.update()

    @Property(QColor)
    def ringColor(self):
        return self._ring_color

    @ringColor.setter
    def ringColor(self, c):
        self._ring_color = QColor(c)
        self.update()

    @Property(int)
    def ringWidth(self):
        return self._ring_width

    @ringWidth.setter
    def ringWidth(self, v):
        self._ring_width = max(0, int(v))
        self.update()
