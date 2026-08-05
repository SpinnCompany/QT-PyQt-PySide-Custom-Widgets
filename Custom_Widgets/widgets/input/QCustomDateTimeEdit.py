########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomDateEdit / QCustomTimeEdit / QCustomDateRangeEdit
##
## Tokenized date & time inputs built on Qt's date/time editors (correct
## calendar popup, keyboard entry and validation) plus a two-field date
## range picker that keeps start <= end. Styled from design tokens; the
## calendar popup is scoped via the object name "customCalendar".
########################################################################
from qtpy.QtCore import Qt, QDate, Property, Signal
from qtpy.QtWidgets import QDateEdit, QTimeEdit, QWidget, QHBoxLayout, QLabel


class _VariantMixin(object):
    """variant / sizeVariant declared properties (QSS reads them via the
    getter; never call setProperty(name) in the setter - that recurses)."""

    def _initVariant(self):
        self._variant = "outline"
        self._sizeVariant = "md"

    def _repolish(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value):
        self._variant = str(value)
        self._repolish()

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self._repolish()


class QCustomDateEdit(_VariantMixin, QDateEdit):
    WIDGET_ICON = "components/icons/calendar.png"
    WIDGET_TOOLTIP = "A date input with a calendar popup"
    WIDGET_MODULE = "Custom_Widgets.QCustomDateTimeEdit"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomDateEdit' name='customDateEdit'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>160</width><height>32</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomDateEdit",
        "props": {"variant": {"type": "enum",
                              "values": ["primary", "secondary", "outline", "ghost"],
                              "default": "outline"},
                  "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                                  "default": "md"}},
        "signals": ["dateChanged"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "accent", "on-primary", "focus-ring"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initVariant()
        self.setObjectName("QCustomDateEdit")
        self.setCalendarPopup(True)
        self.setDisplayFormat("yyyy-MM-dd")
        self.setDate(QDate.currentDate())
        cal = self.calendarWidget()
        if cal is not None:
            cal.setObjectName("customCalendar")
            cal.setGridVisible(False)


class QCustomTimeEdit(_VariantMixin, QTimeEdit):
    WIDGET_ICON = "components/icons/clock.png"
    WIDGET_TOOLTIP = "A time input"
    WIDGET_MODULE = "Custom_Widgets.QCustomDateTimeEdit"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomTimeEdit' name='customTimeEdit'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>120</width><height>32</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomTimeEdit",
        "props": {"variant": {"type": "enum",
                              "values": ["primary", "secondary", "outline", "ghost"],
                              "default": "outline"},
                  "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                                  "default": "md"}},
        "signals": ["timeChanged"],
        "tokens_used": ["surface", "on-surface", "outline", "accent", "focus-ring"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initVariant()
        self.setObjectName("QCustomTimeEdit")
        self.setDisplayFormat("HH:mm")


class QCustomDateRangeEdit(QWidget):
    """A start/end date range picker. Keeps start <= end automatically (via the
    child editors' min/max dates)."""

    rangeChanged = Signal(object, object)   # (QDate start, QDate end)

    WIDGET_ICON = "components/icons/calendar.png"
    WIDGET_TOOLTIP = "A start/end date range picker"
    WIDGET_MODULE = "Custom_Widgets.QCustomDateTimeEdit"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomDateRangeEdit' name='customDateRangeEdit'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>32</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomDateRangeEdit",
        "props": {},
        "signals": ["rangeChanged"],
        "tokens_used": ["surface", "on-surface", "outline", "accent"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomDateRangeEdit")
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        self._start = QCustomDateEdit(self)
        self._end = QCustomDateEdit(self)
        self._sep = QLabel("to", self)
        self._sep.setObjectName("dateRangeSep")
        row.addWidget(self._start, 1)
        row.addWidget(self._sep, 0, Qt.AlignCenter)
        row.addWidget(self._end, 1)

        # keep start <= end: the end can't go before the start, and moving the
        # start past the end drags the end forward (end.minimumDate = start).
        self._start.dateChanged.connect(self._end.setMinimumDate)
        self._start.dateChanged.connect(self._emit)
        self._end.dateChanged.connect(self._emit)

    def _emit(self, *args):
        self.rangeChanged.emit(self._start.date(), self._end.date())

    # -- API --
    def startDate(self):
        return self._start.date()

    def endDate(self):
        return self._end.date()

    def dateRange(self):
        return self._start.date(), self._end.date()

    def setDateRange(self, start, end):
        self._start.setDate(start)
        self._end.setDate(end)

    def startEdit(self):
        return self._start

    def endEdit(self):
        return self._end
