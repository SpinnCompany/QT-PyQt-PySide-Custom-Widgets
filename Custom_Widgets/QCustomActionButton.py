########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomActionButton - a round icon button with a caption beneath it.
##
## The "quick action" tile seen on profile panels and toolbars (Profile / Mute /
## Search, Call / Video, …): a circular icon button over a small caption label.
## The icon is a normal Qt icon so it can be set in Designer OR from QSS
## (`#objectName { qproperty-icon: url(theme-icons:…) }`) and recolours with the
## theme; colours are qproperties. Emits `clicked`. Designer-droppable, so a
## row of these is assembled in the form, not hand-built in Python.
########################################################################
from qtpy.QtCore import Qt, Property, Signal, QSize
from qtpy.QtGui import QColor, QIcon
from qtpy.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, QSizePolicy)


class QCustomActionButton(QFrame):

    clicked = Signal()

    WIDGET_ICON = "components/icons/action_button.png"
    WIDGET_TOOLTIP = "A round icon button with a caption"
    WIDGET_MODULE = "Custom_Widgets.QCustomActionButton"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomActionButton' name='customActionButton'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>72</width><height>72</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomActionButton",
        "props": {"caption": {"type": "string", "default": "Profile"},
                  "buttonSize": {"type": "int", "default": 46},
                  "iconSize": {"type": "int", "default": 19},
                  "bgColor": {"type": "color", "default": "#f0f2f6"},
                  "hoverColor": {"type": "color", "default": "#1b74e4"},
                  "captionColor": {"type": "color", "default": "#8a93a6"}},
        "signals": ["clicked"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, caption="", icon=None):
        super().__init__(parent)
        self.setObjectName("QCustomActionButton")
        self._bg = QColor("#f0f2f6")
        self._hover = QColor("#1b74e4")
        self._caption_color = QColor("#8a93a6")
        self._btn_size = 46
        self._icon_size = 19

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(7)
        lay.setAlignment(Qt.AlignHCenter)

        self._btn = QPushButton(self)
        self._btn.setObjectName("actionButtonBtn")
        self._btn.setCursor(Qt.PointingHandCursor)
        self._btn.setFixedSize(self._btn_size, self._btn_size)
        self._btn.setIconSize(QSize(self._icon_size, self._icon_size))
        if icon is not None:
            self._btn.setIcon(icon if isinstance(icon, QIcon) else QIcon(icon))
        self._btn.clicked.connect(self.clicked)

        self._caption = QLabel(caption, self)
        self._caption.setObjectName("actionButtonCaption")
        self._caption.setAlignment(Qt.AlignHCenter)

        lay.addWidget(self._btn, 0, Qt.AlignHCenter)
        lay.addWidget(self._caption, 0, Qt.AlignHCenter)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._restyle()

    def _restyle(self):
        # No per-widget stylesheet — the app QSS styles #actionButtonBtn and
        # #actionButtonCaption (and their icons); we only re-polish so the theme
        # engine re-evaluates on a theme change.
        for w in (self, self._btn, self._caption):
            w.style().unpolish(w)
            w.style().polish(w)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def caption(self):
        return self._caption.text()

    @caption.setter
    def caption(self, v):
        self._caption.setText(str(v))

    @Property(QIcon)
    def icon(self):
        return self._btn.icon()

    @icon.setter
    def icon(self, ic):
        self._btn.setIcon(ic)

    @Property(int)
    def buttonSize(self):
        return self._btn_size

    @buttonSize.setter
    def buttonSize(self, v):
        self._btn_size = max(24, int(v))
        self._btn.setFixedSize(self._btn_size, self._btn_size)
        self._restyle()

    @Property(int)
    def iconSize(self):
        return self._icon_size

    @iconSize.setter
    def iconSize(self, v):
        self._icon_size = max(10, int(v))
        self._btn.setIconSize(QSize(self._icon_size, self._icon_size))

    @Property(QColor)
    def bgColor(self):
        return self._bg

    @bgColor.setter
    def bgColor(self, c):
        self._bg = QColor(c)
        self._restyle()

    @Property(QColor)
    def hoverColor(self):
        return self._hover

    @hoverColor.setter
    def hoverColor(self, c):
        self._hover = QColor(c)
        self._restyle()

    @Property(QColor)
    def captionColor(self):
        return self._caption_color

    @captionColor.setter
    def captionColor(self, c):
        self._caption_color = QColor(c)
        self._restyle()
