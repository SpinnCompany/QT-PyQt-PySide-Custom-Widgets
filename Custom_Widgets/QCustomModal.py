########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomModal - a modern centered modal dialog with a dim backdrop.
##
## Overlays its parent window with a translucent scrim and a centered rounded
## card (title + close, a content slot, and action buttons). Click the scrim or
## the close button, or press Esc, to dismiss. Show it with showModal(); it
## animates in. Emits triggered(key) for action buttons and closed() on
## dismiss. Theme from code with applyColors(...).
##
##   m = QCustomModal(mainWindow)
##   m.setTitle("Send money"); m.addContent(myForm)
##   m.addAction("Cancel", "cancel"); m.addAction("Send", "send", primary=True)
##   m.triggered.connect(handler); m.showModal()
########################################################################
from qtpy.QtCore import Qt, Signal, QEvent, QPropertyAnimation, QEasingCurve, QRect
from qtpy.QtGui import QColor, QPainter, QBrush, QPen
from qtpy.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QGraphicsDropShadowEffect, QSizePolicy)


class _ModalCloseButton(QPushButton):
    """A close affordance that PAINTS an X (no unicode glyph, so it recolours
    with the theme and passes the glyph-icons design rule)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._x_color = QColor("#8b93a1")

    def setXColor(self, c):
        self._x_color = QColor(c)
        self.update()

    def paintEvent(self, e):
        super().paintEvent(e)   # let the stylesheet paint the round background
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen(self._x_color, 2.0)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        m = 10
        r = self.rect()
        p.drawLine(r.left() + m, r.top() + m, r.right() - m, r.bottom() - m)
        p.drawLine(r.right() - m, r.top() + m, r.left() + m, r.bottom() - m)
        p.end()


class QCustomModal(QWidget):

    WIDGET_ICON = "components/icons/modal.png"
    WIDGET_TOOLTIP = "A modern centered modal dialog with a dim backdrop"
    WIDGET_MODULE = "Custom_Widgets.QCustomModal"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomModal' name='customModal'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>420</width><height>300</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomModal",
        "props": {"title": {"type": "string", "default": "Modal title"},
                  "subtitle": {"type": "string", "default": ""},
                  "cornerRadius": {"type": "int", "default": 20},
                  "panelWidth": {"type": "int", "default": 420},
                  "scrimAlpha": {"type": "int", "default": 120},
                  "closeOnScrim": {"type": "bool", "default": True}},
        "signals": ["triggered(QString)", "closed()"],
        "tokens_used": ["accent", "background", "text"],
    }

    triggered = Signal(str)
    closed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomModal")
        self._scrim_alpha = 120
        self._corner_radius = 20
        self._panel_width = 420
        self._close_on_scrim = True
        self._anim = None

        # theme colours
        self._c_bg = "#ffffff"
        self._c_text = "#0f1b18"
        self._c_muted = "#8b93a1"
        self._c_border = "#e6e9ec"
        self._c_accent = "#16a34a"
        self._c_accent_text = "#ffffff"
        self._c_hover = "#f1f3f5"

        # centered card
        self._panel = QFrame(self)
        self._panel.setObjectName("modalPanel")
        self._panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        pv = QVBoxLayout(self._panel)
        pv.setContentsMargins(24, 22, 24, 22)
        pv.setSpacing(14)

        head = QHBoxLayout(); head.setSpacing(10)
        titleCol = QVBoxLayout(); titleCol.setSpacing(2)
        self._title = QLabel("Modal title", self._panel); self._title.setObjectName("modalTitle")
        self._subtitle = QLabel("", self._panel); self._subtitle.setObjectName("modalSub")
        self._subtitle.hide()
        titleCol.addWidget(self._title); titleCol.addWidget(self._subtitle)
        head.addLayout(titleCol); head.addStretch(1)
        self._closeBtn = _ModalCloseButton(self._panel)   # paints an X (no glyph)
        self._closeBtn.setObjectName("modalClose")
        self._closeBtn.setFixedSize(30, 30)
        self._closeBtn.setCursor(Qt.PointingHandCursor)
        self._closeBtn.clicked.connect(self.closeModal)
        head.addWidget(self._closeBtn, 0, Qt.AlignTop)
        pv.addLayout(head)

        self._body = QVBoxLayout(); self._body.setSpacing(10)
        pv.addLayout(self._body)

        self._actions = QHBoxLayout(); self._actions.setSpacing(10)
        self._actions.addStretch(1)
        pv.addLayout(self._actions)

        shadow = QGraphicsDropShadowEffect(self)   # allow-shadow: a modal card needs elevation over the scrim
        shadow.setBlurRadius(48); shadow.setXOffset(0); shadow.setYOffset(18)
        shadow.setColor(QColor(0, 0, 0, 90))
        self._panel.setGraphicsEffect(shadow)

        self.hide()
        self._restyle()
        self._seed_defaults()
        if parent is not None:
            parent.installEventFilter(self)

    def _seed_defaults(self):
        """Demo content so the modal previews in Designer / render_widget
        (call clearContent()/clearActions() then add your own)."""
        self.setSubtitle("A modern modal dialog")
        lbl = QLabel("Put any content widget here.", self._panel)
        lbl.setStyleSheet("background:transparent; color:%s; font-size:13px;" % self._c_muted)
        self.addContent(lbl)
        self.addAction("Cancel", "cancel")
        self.addAction("Confirm", "confirm", primary=True)

    def clearContent(self):
        while self._body.count():
            it = self._body.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
                w.deleteLater()

    def clearActions(self):
        while self._actions.count():
            it = self._actions.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
                w.deleteLater()
        self._actions.addStretch(1)

    # ------------------------------------------------------------------ #
    ## Content API
    # ------------------------------------------------------------------ #
    def setTitle(self, text):
        self._title.setText(str(text))

    def setSubtitle(self, text):
        self._subtitle.setText(str(text))
        self._subtitle.setVisible(bool(text))

    def addContent(self, widget):
        self._body.addWidget(widget)

    def addAction(self, text, key=None, primary=False, danger=False):
        key = key if key is not None else text
        btn = QPushButton(text, self._panel)
        btn.setObjectName("modalPrimary" if primary else ("modalDanger" if danger else "modalGhost"))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.clicked.connect(lambda _=False, k=key: self._pick(k))
        self._actions.addWidget(btn)
        self._restyle()
        return key

    def _pick(self, key):
        self.triggered.emit(key)
        self.closeModal()

    # ------------------------------------------------------------------ #
    ## Show / hide
    # ------------------------------------------------------------------ #
    def showModal(self):
        if self.parentWidget() is not None:
            self.setGeometry(self.parentWidget().rect())
        self._center_panel()
        self.raise_()
        self.show()
        # fade + rise animation on the panel
        self._panel.show()
        start = self._panel.geometry()
        self._anim = QPropertyAnimation(self._panel, b"geometry", self)
        self._anim.setDuration(180)
        self._anim.setStartValue(QRect(start.x(), start.y() + 18, start.width(), start.height()))
        self._anim.setEndValue(start)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.start()

    def closeModal(self):
        self.hide()
        self.closed.emit()

    def _center_panel(self):
        self._panel.setFixedWidth(self._panel_width)
        self._panel.adjustSize()
        pw, ph = self._panel.width(), self._panel.height()
        self._panel.move((self.width() - pw) // 2, (self.height() - ph) // 2)

    # ------------------------------------------------------------------ #
    ## Backdrop paint + interaction
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.fillRect(self.rect(), QBrush(QColor(0, 0, 0, self._scrim_alpha)))
        p.end()

    def mousePressEvent(self, e):
        # click outside the panel dismisses (if enabled)
        if self._close_on_scrim and not self._panel.geometry().contains(e.pos()):
            self.closeModal()
        super().mousePressEvent(e)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.closeModal()
        else:
            super().keyPressEvent(e)

    def resizeEvent(self, e):
        self._center_panel()
        super().resizeEvent(e)

    def eventFilter(self, obj, ev):
        if obj is self.parentWidget() and ev.type() == QEvent.Resize and self.isVisible():
            self.setGeometry(self.parentWidget().rect())
        return super().eventFilter(obj, ev)

    # ------------------------------------------------------------------ #
    ## Theming
    # ------------------------------------------------------------------ #
    def applyColors(self, bg=None, text=None, muted=None, border=None,
                    accent=None, accentText=None, hover=None):
        if bg is not None: self._c_bg = QColor(bg).name()
        if text is not None: self._c_text = QColor(text).name()
        if muted is not None: self._c_muted = QColor(muted).name()
        if border is not None: self._c_border = QColor(border).name()
        if accent is not None: self._c_accent = QColor(accent).name()
        if accentText is not None: self._c_accent_text = QColor(accentText).name()
        if hover is not None: self._c_hover = QColor(hover).name()
        self._restyle()

    def _restyle(self):
        self._closeBtn.setXColor(self._c_muted)
        self._panel.setStyleSheet("""
            QFrame#modalPanel { background: %(bg)s; border: 1px solid %(border)s; border-radius: %(r)dpx; }
            QLabel#modalTitle { background: transparent; color: %(text)s; font-size: 18px; font-weight: 800; }
            QLabel#modalSub   { background: transparent; color: %(muted)s; font-size: 13px; }
            QPushButton#modalClose {
                background: %(hover)s; border: 0; border-radius: 15px;
            }
            QPushButton#modalPrimary {
                background: %(accent)s; color: %(accentText)s; border: 0; border-radius: 12px;
                padding: 0 20px; font-size: 14px; font-weight: 700;
            }
            QPushButton#modalGhost {
                background: transparent; color: %(text)s; border: 1px solid %(border)s;
                border-radius: 12px; padding: 0 20px; font-size: 14px; font-weight: 700;
            }
            QPushButton#modalGhost:hover { border-color: %(accent)s; color: %(accent)s; }
        """ % {"bg": self._c_bg, "border": self._c_border, "text": self._c_text,
               "muted": self._c_muted, "accent": self._c_accent,
               "accentText": self._c_accent_text, "hover": self._c_hover,
               "r": self._corner_radius})
