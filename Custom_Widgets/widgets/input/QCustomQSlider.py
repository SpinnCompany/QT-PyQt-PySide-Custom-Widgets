########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## IMPORTS
########################################################################

########################################################################
## MODULE UPDATED TO USE QT.PY
########################################################################
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QSlider, QStyle, QStyleOptionSlider

########################################################################
## CUSTOM QSLIDER
########################################################################
class QCustomQSlider(QSlider):
    # Qt Designer contract. WIDGET_MODULE is the FLAT public path --
    # Custom_Widgets.QCustomQSlider is what .ui files carry in <header>, not the
    # subpackage this file now lives in.
    WIDGET_MODULE = "Custom_Widgets.QCustomQSlider"
    WIDGET_TOOLTIP = "A QSlider that jumps to the clicked position"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomQSlider' name='qCustomQSlider'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>200</width><height>24</height></rect></property>
        </widget>
    </ui>
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        super(QCustomQSlider, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)

    def pixelPosToRangeValue(self, pos):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)

        if self.orientation() == Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()
        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                               sliderMax - sliderMin, opt.upsideDown)