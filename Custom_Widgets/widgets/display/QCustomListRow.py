########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomListRow - a leading-icon list item.
##
## The universal "row" for transaction feeds, activity lists, leaderboards and
## notifications: a rounded icon/avatar chip, a title + subtitle stacked in the
## middle, and an optional trailing value + meta on the right. Composed from a
## layout + QLabels (not painted) so the text uses real fonts and can be themed
## by objectName/role QSS, while sensible inline defaults make it look right
## standalone. The leading chip takes either a QPixmap/QIcon (setIcon) or a
## letter/emoji (iconText). Set content in code or via the Designer properties.
########################################################################
from qtpy.QtCore import Qt, Property, QSize, QPointF
from qtpy.QtGui import QColor, QPixmap, QIcon, QPainter
from qtpy.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout,
                            QWidget, QSizePolicy)


class _DragHandle(QWidget):
    """A painted 2x3 dot grip — the opt-in reorder affordance for a list row."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._color = QColor(150, 155, 170)
        self.setFixedWidth(18)
        self.setCursor(Qt.OpenHandCursor)

    def setColor(self, c):
        self._color = QColor(c)
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(self._color)
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        r = 1.6
        for gx in (cx - 3, cx + 3):
            for gy in (cy - 6, cy, cy + 6):
                p.drawEllipse(QPointF(gx, gy), r, r)
        p.end()


class QCustomListRow(QFrame):

    WIDGET_ICON = "components/icons/table_rows.png"
    WIDGET_TOOLTIP = "A leading-icon list item (transaction / activity row)"
    WIDGET_MODULE = "Custom_Widgets.QCustomListRow"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomListRow' name='customListRow'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>60</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomListRow",
        "props": {"title": {"type": "string", "default": "Starbucks"},
                  "subtitle": {"type": "string", "default": "Shopping"},
                  "value": {"type": "string", "default": "- $120.00"},
                  "meta": {"type": "string", "default": "31 Mar 2019"},
                  "iconText": {"type": "string", "default": ""},
                  "chipColor": {"type": "color", "default": "#f1f3f8"},
                  "chipTextColor": {"type": "color", "default": "#3355e8"},
                  "valueColor": {"type": "color", "default": ""},
                  "subtitleColor": {"type": "color", "default": "#3355e8"},
                  "chipSize": {"type": "int", "default": 44},
                  "chipRadius": {"type": "int", "default": 13},
                  "showDragHandle": {"type": "bool", "default": False},
                  "dragHandleColor": {"type": "color", "default": "#969baa"}},
        "signals": [],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, title="", subtitle="", value="", meta="", icon=None):
        super().__init__(parent)
        self.setObjectName("QCustomListRow")
        self._chip_size = 44
        self._chip_radius = 13
        self._chip_color = QColor("#f1f3f8")
        self._chip_text_color = QColor("#3355e8")
        self._subtitle_color = QColor("#3355e8")
        self._value_color = QColor()          # invalid -> inherit / default
        self._icon_text = ""

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        self._chip = QLabel()
        self._chip.setAlignment(Qt.AlignCenter)
        self._chip.setFixedSize(self._chip_size, self._chip_size)
        lay.addWidget(self._chip, 0)

        mid = QVBoxLayout()
        mid.setSpacing(3)
        mid.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel(title)
        self._title.setProperty("role", "listRowTitle")
        self._subtitle = QLabel(subtitle)
        self._subtitle.setProperty("role", "listRowSubtitle")
        mid.addWidget(self._title)
        mid.addWidget(self._subtitle)
        midw = QWidget()
        midw.setLayout(mid)
        lay.addWidget(midw, 1)

        right = QVBoxLayout()
        right.setSpacing(3)
        right.setContentsMargins(0, 0, 0, 0)
        self._value = QLabel(value)
        self._value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._value.setProperty("role", "listRowValue")
        self._meta = QLabel(meta)
        self._meta.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._meta.setProperty("role", "listRowMeta")
        right.addWidget(self._value)
        right.addWidget(self._meta)
        rightw = QWidget()
        rightw.setLayout(right)
        lay.addWidget(rightw, 0)

        # opt-in trailing reorder grip (hidden by default -> existing rows are
        # unchanged)
        self._grip = _DragHandle()
        self._grip.hide()
        lay.addWidget(self._grip, 0)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        if icon is not None:
            self.setIcon(icon)
        self._applyStyles()

    # ------------------------------------------------------------------ #
    ## Content API
    # ------------------------------------------------------------------ #
    def setTitle(self, text):
        self._title.setText(str(text))

    def setSubtitle(self, text):
        self._subtitle.setText(str(text))

    def setValue(self, text):
        self._value.setText(str(text))
        self._value.setVisible(bool(str(text)))

    def setMeta(self, text):
        self._meta.setText(str(text))
        self._meta.setVisible(bool(str(text)))

    def setIcon(self, icon):
        """Leading chip image: a QPixmap or QIcon. Clears any iconText."""
        pm = None
        if isinstance(icon, QIcon):
            pm = icon.pixmap(QSize(int(self._chip_size * 0.5), int(self._chip_size * 0.5)))
        elif isinstance(icon, QPixmap):
            pm = icon
        if pm is not None:
            self._icon_text = ""
            self._chip.setPixmap(pm)

    def setIconText(self, text):
        """Leading chip glyph/letter (e.g. an initial). Clears any pixmap."""
        self._icon_text = str(text)
        self._chip.setPixmap(QPixmap())
        self._chip.setText(self._icon_text)
        self._applyStyles()

    # ------------------------------------------------------------------ #
    ## Styling
    # ------------------------------------------------------------------ #
    def _applyStyles(self):
        self._chip.setStyleSheet(
            "background:%s; color:%s; border-radius:%dpx; font-weight:800; font-size:15px;"
            % (self._chip_color.name(), self._chip_text_color.name(), self._chip_radius))
        self._subtitle.setStyleSheet(
            "color:%s; background:transparent; font-size:12px; font-weight:600;"
            % self._subtitle_color.name())
        self._title.setStyleSheet(
            "background:transparent; font-size:14px; font-weight:700;")
        if self._value_color.isValid():
            self._value.setStyleSheet(
                "color:%s; background:transparent; font-size:14px; font-weight:800;"
                % self._value_color.name())
        else:
            self._value.setStyleSheet(
                "background:transparent; font-size:14px; font-weight:800;")
        self._meta.setStyleSheet(
            "background:transparent; font-size:12px;")

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def title(self):
        return self._title.text()

    @title.setter
    def title(self, v):
        self.setTitle(v)

    @Property(str)
    def subtitle(self):
        return self._subtitle.text()

    @subtitle.setter
    def subtitle(self, v):
        self.setSubtitle(v)

    @Property(str)
    def value(self):
        return self._value.text()

    @value.setter
    def value(self, v):
        self.setValue(v)

    @Property(str)
    def meta(self):
        return self._meta.text()

    @meta.setter
    def meta(self, v):
        self.setMeta(v)

    @Property(str)
    def iconText(self):
        return self._icon_text

    @iconText.setter
    def iconText(self, v):
        self.setIconText(v)

    @Property(QColor)
    def chipColor(self):
        return self._chip_color

    @chipColor.setter
    def chipColor(self, c):
        self._chip_color = QColor(c)
        self._applyStyles()

    @Property(QColor)
    def chipTextColor(self):
        return self._chip_text_color

    @chipTextColor.setter
    def chipTextColor(self, c):
        self._chip_text_color = QColor(c)
        self._applyStyles()

    @Property(QColor)
    def subtitleColor(self):
        return self._subtitle_color

    @subtitleColor.setter
    def subtitleColor(self, c):
        self._subtitle_color = QColor(c)
        self._applyStyles()

    @Property(QColor)
    def valueColor(self):
        return self._value_color

    @valueColor.setter
    def valueColor(self, c):
        self._value_color = QColor(c)
        self._applyStyles()

    @Property(int)
    def chipSize(self):
        return self._chip_size

    @chipSize.setter
    def chipSize(self, v):
        self._chip_size = max(16, int(v))
        self._chip.setFixedSize(self._chip_size, self._chip_size)
        self._applyStyles()

    @Property(int)
    def chipRadius(self):
        return self._chip_radius

    @chipRadius.setter
    def chipRadius(self, v):
        self._chip_radius = max(0, int(v))
        self._applyStyles()

    @Property(bool)
    def showDragHandle(self):
        return self._grip.isVisible()

    @showDragHandle.setter
    def showDragHandle(self, v):
        self._grip.setVisible(bool(v))

    @Property(QColor)
    def dragHandleColor(self):
        return self._grip._color

    @dragHandleColor.setter
    def dragHandleColor(self, c):
        self._grip.setColor(c)
