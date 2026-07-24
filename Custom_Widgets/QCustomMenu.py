########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomMenu - a modern popup action menu.
##
## A frameless, rounded, elevated popup for the "..." / more buttons: a column
## of icon + label action rows with hover states, optional separators and a
## right-aligned hint. Open it anchored under a button with popupAt(button).
## Emits triggered(key) when an item is picked. Theme it from code with
## applyColors(...) so it flips with the app theme (it is a top-level popup, so
## the app stylesheet does not cascade in automatically).
########################################################################
from qtpy.QtCore import Qt, Signal, QPoint
from qtpy.QtGui import QColor
from qtpy.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QGraphicsDropShadowEffect, QSizePolicy)


class QCustomMenu(QWidget):

    WIDGET_ICON = "components/icons/menu.png"
    WIDGET_TOOLTIP = "A modern popup action menu for '...' / more buttons"
    WIDGET_MODULE = "Custom_Widgets.QCustomMenu"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomMenu' name='customMenu'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>200</width><height>160</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomMenu",
        "props": {"itemHeight": {"type": "int", "default": 38},
                  "cornerRadius": {"type": "int", "default": 14},
                  "minWidth": {"type": "int", "default": 200}},
        "signals": ["triggered(QString)"],
        "tokens_used": ["accent", "background", "text"],
    }

    triggered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setObjectName("QCustomMenu")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._item_height = 38
        self._corner_radius = 14
        self._min_width = 200

        self._margin = 16       # room for the shadow
        outer = QVBoxLayout(self)
        outer.setContentsMargins(self._margin, self._margin, self._margin, self._margin)
        self._panel = QFrame(self)
        self._panel.setObjectName("menuPanel")
        outer.addWidget(self._panel)
        self._vbox = QVBoxLayout(self._panel)
        self._vbox.setContentsMargins(8, 8, 8, 8)
        self._vbox.setSpacing(2)

        shadow = QGraphicsDropShadowEffect(self)   # allow-shadow: a floating menu needs real elevation
        shadow.setBlurRadius(34)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 55))
        self._panel.setGraphicsEffect(shadow)

        # theme colours (override via applyColors)
        self._c_bg = "#ffffff"
        self._c_text = "#0f1b18"
        self._c_muted = "#8b93a1"
        self._c_hover = "#f1f3f5"
        self._c_border = "#e6e9ec"
        self._c_accent = "#16a34a"
        self._c_danger = "#e5484d"
        self._restyle()
        self._seed_defaults()

    def _seed_defaults(self):
        """Demo items so the menu previews in Designer / render_widget
        (call clear() then re-add your real actions)."""
        self.addAction("Edit", "edit")
        self.addAction("Duplicate", "duplicate")
        self.addSeparator()
        self.addAction("Delete", "delete", danger=True)

    # ------------------------------------------------------------------ #
    ## Build the menu
    # ------------------------------------------------------------------ #
    def addAction(self, text, key=None, icon=None, hint="", danger=False):
        """Add an action row. `icon` may be a QIcon or QPixmap. Returns the key."""
        key = key if key is not None else text
        btn = QPushButton(text, self._panel)
        btn.setObjectName("menuDanger" if danger else "menuItem")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(self._item_height)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if icon is not None:
            from qtpy.QtGui import QIcon, QPixmap
            btn.setIcon(icon if isinstance(icon, QIcon) else QIcon(icon))
            from qtpy.QtCore import QSize
            btn.setIconSize(QSize(17, 17))
        if hint:
            btn.setText("%s\t%s" % (text, hint))
        btn.clicked.connect(lambda _=False, k=key: self._pick(k))
        self._vbox.addWidget(btn)
        return key

    def addSeparator(self):
        line = QFrame(self._panel)
        line.setObjectName("menuSep")
        line.setFrameShape(QFrame.HLine)
        line.setFixedHeight(1)
        self._vbox.addWidget(line)

    def clear(self):
        while self._vbox.count():
            it = self._vbox.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
                w.deleteLater()

    def _pick(self, key):
        self.close()
        self.triggered.emit(key)

    # ------------------------------------------------------------------ #
    ## Theming
    # ------------------------------------------------------------------ #
    def applyColors(self, bg=None, text=None, muted=None, hover=None,
                    border=None, accent=None, danger=None):
        if bg is not None: self._c_bg = QColor(bg).name()
        if text is not None: self._c_text = QColor(text).name()
        if muted is not None: self._c_muted = QColor(muted).name()
        if hover is not None: self._c_hover = QColor(hover).name()
        if border is not None: self._c_border = QColor(border).name()
        if accent is not None: self._c_accent = QColor(accent).name()
        if danger is not None: self._c_danger = QColor(danger).name()
        self._restyle()

    def _restyle(self):
        self._panel.setStyleSheet("""
            QFrame#menuPanel { background: %(bg)s; border: 1px solid %(border)s; border-radius: %(r)dpx; }
            QPushButton#menuItem, QPushButton#menuDanger {
                text-align: left; padding: 0 12px; border: 0; border-radius: 9px;
                background: transparent; color: %(text)s; font-size: 13px; font-weight: 600;
            }
            QPushButton#menuDanger { color: %(danger)s; }
            QPushButton#menuItem:hover { background: %(hover)s; }
            QPushButton#menuDanger:hover { background: %(hover)s; }
            QFrame#menuSep { background: %(border)s; border: 0; margin: 4px 6px; }
        """ % {"bg": self._c_bg, "border": self._c_border, "text": self._c_text,
               "danger": self._c_danger, "hover": self._c_hover, "r": self._corner_radius})

    # ------------------------------------------------------------------ #
    ## Show anchored to a widget
    # ------------------------------------------------------------------ #
    def popupAt(self, anchor, align="right", gap=4):
        """Show the menu just below `anchor`, right- or left-aligned to it."""
        self._panel.setMinimumWidth(self._min_width)
        self.adjustSize()
        if align == "right":
            corner = anchor.mapToGlobal(anchor.rect().bottomRight())
            x = corner.x() - self.width() + self._margin
        else:
            corner = anchor.mapToGlobal(anchor.rect().bottomLeft())
            x = corner.x() - self._margin
        y = anchor.mapToGlobal(anchor.rect().bottomLeft()).y() - self._margin + gap
        self.move(QPoint(int(x), int(y)))
        self.show()

    def popupAtPos(self, global_pos):
        self._panel.setMinimumWidth(self._min_width)
        self.adjustSize()
        self.move(global_pos - QPoint(self._margin, self._margin))
        self.show()
