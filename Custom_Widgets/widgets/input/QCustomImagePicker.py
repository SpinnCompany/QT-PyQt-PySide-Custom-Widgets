########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomImagePicker - a drop / browse image field with a live preview.
##
## The avatar-or-cover upload control: an empty dashed target that accepts a
## drag-and-drop or a click-to-browse, then shows the chosen image scaled to
## fit with a remove button.
##
## Validation is on the *bytes*, never the file extension - a .png that is not
## an image is rejected, which is the whole point of validating at all. Size
## and pixel-dimension caps guard against a decompression bomb being loaded
## into a preview.
##
## Emits imageSelected(str), imageCleared() and selectionRejected(str) - the
## last carrying a human-readable reason, so a caller can surface it rather
## than leaving the user with a target that silently ignores their file.
########################################################################
import os

from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QPixmap, QImageReader
from qtpy.QtWidgets import QWidget, QSizePolicy, QFileDialog


class QCustomImagePicker(QWidget):
    imageSelected = Signal(str)
    imageCleared = Signal()
    selectionRejected = Signal(str)

    WIDGET_ICON = "components/icons/add_photo_alternate.png"
    WIDGET_TOOLTIP = "An image picker with drag-drop, browse and preview"
    WIDGET_MODULE = "Custom_Widgets.QCustomImagePicker"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomImagePicker' name='customImagePicker'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>240</width><height>160</height></rect></property>
            <property name='placeholderText'><string>Drop an image or click to browse</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomImagePicker",
        "props": {"imagePath": {"type": "string", "default": ""},
                  "placeholderText": {"type": "string",
                                      "default": "Drop an image or click to browse"},
                  "shape": {"type": "enum", "values": ["rounded", "circle"],
                            "default": "rounded"},
                  "fitMode": {"type": "enum", "values": ["cover", "contain"],
                              "default": "cover"},
                  "maxBytes": {"type": "int", "default": 5242880},
                  "maxPixels": {"type": "int", "default": 8000},
                  "allowClear": {"type": "bool", "default": True},
                  "cornerRadius": {"type": "int", "default": 10},
                  "state": {"type": "enum", "values": ["default", "error"],
                            "default": "default"}},
        "signals": ["imageSelected", "imageCleared", "selectionRejected"],
        "tokens_used": ["surface", "on-surface", "outline", "accent",
                        "destructive"],
    }

    # Matches UploadService on the billing site: trust the decoder, not the name.
    ALLOWED_FORMATS = ("png", "jpg", "jpeg", "webp", "gif", "bmp")

    def __init__(self, parent=None, path="", placeholder="Drop an image or click to browse"):
        super().__init__(parent)
        self.setObjectName("QCustomImagePicker")
        self._path = ""
        self._pixmap = QPixmap()
        self._placeholder = str(placeholder)
        self._shape = "rounded"
        self._fitMode = "cover"
        self._maxBytes = 5 * 1024 * 1024
        self._maxPixels = 8000
        self._allowClear = True
        self._radius = 10
        self._state = "default"
        self._hovered = False
        self._dragActive = False
        self._clearRect = QRectF()

        self._borderColor = QColor("#cbd5e1")
        self._borderActiveColor = QColor("#2563eb")
        self._borderErrorColor = QColor("#dc2626")
        self._backgroundColor = QColor("#f8fafc")
        self._textColor = QColor("#64748b")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
        if path:
            self.setImagePath(path)

    # ------------------------------------------------------------------ #
    ## Validation
    # ------------------------------------------------------------------ #
    def validationError(self, path):
        """Reason this file cannot be used, or None if it is fine.

        Deliberately reads the header rather than the suffix: a .png that is
        not a PNG must be rejected, otherwise validating by name is theatre.
        """
        if not path or not os.path.isfile(path):
            return "File does not exist"
        try:
            size = os.path.getsize(path)
        except OSError:
            return "File is not readable"
        if self._maxBytes > 0 and size > self._maxBytes:
            return "Image exceeds the %.1f MB limit" % (self._maxBytes / 1048576.0)

        reader = QImageReader(path)
        reader.setDecideFormatFromContent(True)
        fmt = bytes(reader.format()).decode("ascii", "ignore").lower()
        if not fmt:
            return "File is not a readable image"
        if fmt not in self.ALLOWED_FORMATS:
            return "Unsupported image type: %s" % fmt
        size_hint = reader.size()
        if self._maxPixels > 0 and size_hint.isValid() and (
                size_hint.width() > self._maxPixels
                or size_hint.height() > self._maxPixels):
            return "Image dimensions exceed %dpx" % self._maxPixels
        return None

    def canAccept(self, path):
        return self.validationError(path) is None

    # ------------------------------------------------------------------ #
    ## Selection
    # ------------------------------------------------------------------ #
    def setImagePath(self, path):
        """Select an image. Rejects and emits selectionRejected on failure."""
        path = str(path or "")
        if not path:
            self.clearImage()
            return True
        reason = self.validationError(path)
        if reason is not None:
            self._state = "error"
            self.update()
            self.selectionRejected.emit(reason)
            return False
        pixmap = QPixmap(path)
        if pixmap.isNull():
            self._state = "error"
            self.update()
            self.selectionRejected.emit("Image could not be decoded")
            return False
        self._path = path
        self._pixmap = pixmap
        self._state = "default"
        self.update()
        self.imageSelected.emit(path)
        return True

    def pixmap(self):
        return self._pixmap

    def hasImage(self):
        return bool(self._path) and not self._pixmap.isNull()

    def clearImage(self):
        if not self._path and self._pixmap.isNull():
            return
        self._path = ""
        self._pixmap = QPixmap()
        self._state = "default"
        self.update()
        self.imageCleared.emit()

    def browse(self):
        """Open a file dialog. Returns True if an image was accepted."""
        patterns = " ".join("*.%s" % ext for ext in self.ALLOWED_FORMATS)
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose an image", "", "Images (%s)" % patterns)
        if not path:
            return False
        return self.setImagePath(path)

    # ------------------------------------------------------------------ #
    ## Geometry / painting
    # ------------------------------------------------------------------ #
    def sizeHint(self):
        return QSize(240, 160)

    def minimumSizeHint(self):
        return QSize(80, 60)

    def _radiusFor(self, rect):
        if self._shape == "circle":
            return min(rect.width(), rect.height()) / 2.0
        return float(self._radius)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        rect = QRectF(1, 1, self.width() - 2, self.height() - 2)
        radius = self._radiusFor(rect)

        if self._state == "error":
            border = self._borderErrorColor
        elif self._dragActive or self._hovered or self.hasFocus():
            border = self._borderActiveColor
        else:
            border = self._borderColor

        if self.hasImage():
            path_clip = self._clipPath(rect, radius)
            p.save()
            p.setClipPath(path_clip)
            # Fill first: in contain mode the letterbox bars would otherwise be
            # whatever happened to be in the buffer.
            p.fillRect(rect, QBrush(self._backgroundColor))
            p.drawPixmap(self._targetRect(rect), self._pixmap,
                         self._sourceRect(rect))
            p.restore()
            p.setPen(QPen(border, 2 if self._dragActive else 1))
            p.setBrush(Qt.NoBrush)
            p.drawRoundedRect(rect, radius, radius)
            if self._allowClear:
                self._paintClearButton(p, rect)
            else:
                self._clearRect = QRectF()
            return

        self._clearRect = QRectF()
        pen = QPen(border, 2)
        pen.setStyle(Qt.DashLine)          # empty target reads as "drop here"
        p.setPen(pen)
        p.setBrush(QBrush(self._backgroundColor))
        p.drawRoundedRect(rect, radius, radius)

        p.setPen(QPen(self._textColor))
        p.setFont(self.font())
        p.drawText(rect.adjusted(12, 12, -12, -12),
                   int(Qt.AlignCenter | Qt.TextWordWrap), self._placeholder)

    def _clipPath(self, rect, radius):
        from qtpy.QtGui import QPainterPath
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        return path

    def _targetRect(self, rect):
        """Where the pixmap is drawn.

        cover fills the whole field (the crop happens on the source side);
        contain letterboxes — the image is scaled down to fit entirely and
        centred, leaving background visible. Filling the field in contain mode
        would stretch the image, which is exactly what contain means to avoid.
        """
        pw, ph = self._pixmap.width(), self._pixmap.height()
        if self._fitMode != "contain" or pw <= 0 or ph <= 0:
            return rect
        scale = min(rect.width() / pw, rect.height() / ph)
        w, h = pw * scale, ph * scale
        return QRectF(rect.left() + (rect.width() - w) / 2.0,
                      rect.top() + (rect.height() - h) / 2.0, w, h)

    def _sourceRect(self, rect):
        """Which part of the pixmap is used. Never distorts the aspect ratio."""
        pw, ph = self._pixmap.width(), self._pixmap.height()
        if pw <= 0 or ph <= 0:
            return QRectF(0, 0, 0, 0)
        if self._fitMode == "contain":
            return QRectF(0, 0, pw, ph)       # all of it; _targetRect shrinks
        # cover: crop the long axis so the aspect ratio is preserved
        target_ratio = rect.width() / max(1.0, rect.height())
        source_ratio = pw / float(ph)
        if source_ratio > target_ratio:
            new_w = ph * target_ratio
            return QRectF((pw - new_w) / 2.0, 0, new_w, ph)
        new_h = pw / target_ratio
        return QRectF(0, (ph - new_h) / 2.0, pw, new_h)

    def _paintClearButton(self, p, rect):
        size = 22.0
        self._clearRect = QRectF(rect.right() - size - 6, rect.top() + 6, size, size)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(0, 0, 0, 140)))
        p.drawEllipse(self._clearRect)
        c = self._clearRect.center()
        p.setPen(QPen(QColor("#ffffff"), 1.8))
        p.drawLine(int(c.x() - 4), int(c.y() - 4), int(c.x() + 4), int(c.y() + 4))
        p.drawLine(int(c.x() + 4), int(c.y() - 4), int(c.x() - 4), int(c.y() + 4))

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def _firstLocalFile(self, mime):
        if not mime.hasUrls():
            return None
        for url in mime.urls():
            if url.isLocalFile():
                return url.toLocalFile()
        return None

    def dragEnterEvent(self, e):
        path = self._firstLocalFile(e.mimeData())
        if path and self.canAccept(path):
            self._dragActive = True
            self.update()
            e.acceptProposedAction()
        else:
            e.ignore()

    def dragLeaveEvent(self, e):
        self._dragActive = False
        self.update()
        super().dragLeaveEvent(e)

    def dropEvent(self, e):
        self._dragActive = False
        path = self._firstLocalFile(e.mimeData())
        if path and self.setImagePath(path):
            e.acceptProposedAction()
        else:
            e.ignore()
        self.update()

    def enterEvent(self, e):
        self._hovered = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hovered = False
        self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self._allowClear and self.hasImage() \
                    and self._clearRect.contains(e.pos()):
                self.clearImage()
                return
            self.browse()
        super().mouseReleaseEvent(e)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
            self.browse()
            return
        if e.key() in (Qt.Key_Delete, Qt.Key_Backspace) and self._allowClear:
            self.clearImage()
            return
        super().keyPressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def imagePath(self):
        return self._path

    @imagePath.setter
    def imagePath(self, path):
        self.setImagePath(path)

    @Property(str)
    def placeholderText(self):
        return self._placeholder

    @placeholderText.setter
    def placeholderText(self, text):
        self._placeholder = str(text); self.update()

    @Property(str)
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._shape = "circle" if str(value) == "circle" else "rounded"
        self.update()

    @Property(str)
    def fitMode(self):
        return self._fitMode

    @fitMode.setter
    def fitMode(self, value):
        self._fitMode = "contain" if str(value) == "contain" else "cover"
        self.update()

    @Property(int)
    def maxBytes(self):
        return self._maxBytes

    @maxBytes.setter
    def maxBytes(self, value):
        self._maxBytes = max(0, int(value))

    @Property(int)
    def maxPixels(self):
        return self._maxPixels

    @maxPixels.setter
    def maxPixels(self, value):
        self._maxPixels = max(0, int(value))

    @Property(bool)
    def allowClear(self):
        return self._allowClear

    @allowClear.setter
    def allowClear(self, value):
        self._allowClear = bool(value); self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, value):
        self._radius = max(0, int(value)); self.update()

    @Property(str)
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = "error" if str(value) == "error" else "default"
        self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def borderColor(self):
        return self._borderColor

    @borderColor.setter
    def borderColor(self, c):
        self._borderColor = QColor(c); self.update()

    @Property(QColor)
    def borderActiveColor(self):
        return self._borderActiveColor

    @borderActiveColor.setter
    def borderActiveColor(self, c):
        self._borderActiveColor = QColor(c); self.update()

    @Property(QColor)
    def borderErrorColor(self):
        return self._borderErrorColor

    @borderErrorColor.setter
    def borderErrorColor(self, c):
        self._borderErrorColor = QColor(c); self.update()

    @Property(QColor)
    def backgroundColor(self):
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, c):
        self._backgroundColor = QColor(c); self.update()

    @Property(QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, c):
        self._textColor = QColor(c); self.update()
