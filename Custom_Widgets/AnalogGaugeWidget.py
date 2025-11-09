#!/usr/bin/env python

###
# Author: Stefan Holstein
# inspired by: https://github.com/Werkov/PyQt4/blob/master/examples/widgets/analogclock.py
# Thanks to https://stackoverflow.com/

# Updated by 

## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
# GitHub : https://github.com/KhamisiKibet


## IMPORTS
import os
import math
import json

from qtpy.QtWidgets import QWidget 
from qtpy.QtGui import QPolygon, QPolygonF, QColor, QPen, QFont, QPainter, QFontMetrics, QConicalGradient, QRadialGradient, QFontDatabase
from qtpy.QtCore import Qt, QTimer, QPoint, QPointF, QRect, QSize, QObject, Signal, Property

from Custom_Widgets.Log import *

# AnalogGaugeWidget CLASS
class AnalogGaugeWidget(QWidget):
    # Icon path for the widget
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/watch.png")
    
    # Tooltip for the widget
    WIDGET_TOOLTIP = "An analog gauge widget"
    
    # XML string for the widget
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='AnalogGaugeWidget' name='analogGaugeWidget'>
            <property name='geometry'>
                <rect>
                    <x>0</x>
                    <y>0</y>
                    <width>200</width>
                    <height>200</height>
                </rect>
            </property>
        </widget>
    </ui>
    """
    WIDGET_MODULE="Custom_Widgets.AnalogGaugeWidget"

    valueChanged = Signal(int)

    def __init__(self, parent=None, min_value: int = 0, max_value: int = 1000, 
                 needle_color: QColor = QColor(0, 0, 0, 255), 
                 needle_color_drag: QColor = QColor(255, 0, 0, 255), 
                 scale_value_color: QColor = QColor(0, 0, 0, 255), 
                 display_value_color: QColor = QColor(0, 0, 0, 255),
                 center_point_color: QColor = QColor(0, 0, 0, 255)):
        super(AnalogGaugeWidget, self).__init__(parent)

        self._needle_color = needle_color
        self._needle_color_drag = needle_color_drag
        self._scale_value_color = scale_value_color
        self._display_value_color = display_value_color
        self._center_point_color = center_point_color
        self._value_needle_count = 1
        self._min_value = min_value
        self._max_value = max_value
        self._value = self._min_value
        self._value_offset = 0
        self._value_needle_snapzone = 0.05
        self._last_value = 0
        self._gauge_color_outer_radius_factor = 1
        self._gauge_color_inner_radius_factor = 0.9
        self._center_horizontal_value = 0
        self._center_vertical_value = 0
        self._scale_angle_start_value = 135
        self._scale_angle_size = 270
        self._angle_offset = 0
        self._scala_count = 10
        self._scala_subdiv_count = 5
        self._pen = QPen(QColor(0, 0, 0))
        self._scale_polygon_colors = []
        self._big_scale_marker = Qt.black
        self._fine_scale_color = Qt.black
        self._enable_scale_text = True
        self._scale_fontname = "Orbitron"
        self._initial_scale_fontsize = 14
        self._scale_fontsize = self._initial_scale_fontsize
        self._enable_value_text = True
        self._value_fontname = "Orbitron"
        self._initial_value_fontsize = 40
        self._value_fontsize = self._initial_value_fontsize
        self._text_radius_factor = 0.5
        self._enable_bar_graph = True
        self._enable_filled_polygon = True
        self._enable_center_point = True
        self._enable_fine_scaled_marker = True
        self._enable_big_scaled_marker = True
        self._needle_scale_factor = 0.8
        self._enable_needle_polygon = True
        self._units = "℃"
        self._themeNumber = 1

        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf'))
        
        self.update()
        self.setGaugeTheme(0)
        self.rescale_method()

    # Properties with getters and setters
    @Property(int)
    def themeNumber(self):
        return self._themeNumber
    
    @themeNumber.setter
    def themeNumber(self, value):
        self._themeNumber = value
        self.setGaugeTheme(value)
    
    @Property(str)
    def units(self):
        return self._units

    @units.setter
    def units(self, value: str):
        self._units = value
        self.update()

    def setUnits(self, value: str):
        self.units = value

    @Property(QColor)
    def needleColor(self):
        return self._needle_color

    @needleColor.setter
    def needleColor(self, color: QColor):
        self._needle_color = color
        print(color)
        self.update()

    def setNeedleColor(self, color: QColor):
        self.needleColor = color

    @Property(QColor)
    def needleColorOnDrag(self):
        return self._needle_color_drag

    @needleColorOnDrag.setter
    def needleColorOnDrag(self, color: QColor):
        self._needle_color_drag = color
        self.update()

    def setNeedleColorOnDrag(self, color: QColor):
        self.needleColorOnDrag=color

    @Property(QColor)
    def scaleValueColor(self):
        return self._scale_value_color

    @scaleValueColor.setter
    def scaleValueColor(self, color: QColor):
        self._scale_value_color = color
        self.update()

    def setScaleValueColor(self, color: QColor):
        self.scaleValueColor=color

    @Property(QColor)
    def fineScaleColor(self):
        return self._fine_scale_color

    @fineScaleColor.setter
    def fineScaleColor(self, color: QColor):
        self._fine_scale_color = color
        self.update()

    # SET FINE SCALE COLOR
    def setFineScaleColor(self, color: QColor):
        self.fineScaleColor = color

    @Property(QColor)
    def displayValueColor(self):
        return self._display_value_color

    @displayValueColor.setter
    def displayValueColor(self, color: QColor):
        self._display_value_color = color
        self.update()

    def setDisplayValueColor(self, color: QColor):
        self.displayValueColor=color

    @Property(QColor)
    def centerPointColor(self):
        return self._center_point_color

    @centerPointColor.setter
    def centerPointColor(self, color: QColor):
        self._center_point_color = color
        self.update()

    def setCenterPointColor(self, color: QColor):
        self.centerPointColor=color

    @Property(int)
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = value

        self.update()

    def setValue(self, value: int):
        self.value=value

    @Property(int)
    def minValue(self):
        return self._min_value

    @minValue.setter
    def minValue(self, value: int):
        if self._value < value:
            self._value = value
        if value >= self._max_value:
            self._min_value = self._max_value - 1
        else:
            self._min_value = value

        self.update()

    def setMinValue(self, value: int):
        self.minValue=value

    @Property(int)
    def maxValue(self):
        return self._max_value

    @maxValue.setter
    def maxValue(self, value: int):
        if self._value > value:
            self._value = value
        if value <= self._min_value:
            self._max_value = self._min_value + 1
        else:
            self._max_value = value

        self.update()

    def setMaxValue(self, value: int):
        self.maxValue=value

    @Property(QFont)
    def scaleFontFamily(self):
        return self._scale_fontname

    @scaleFontFamily.setter
    def scaleFontFamily(self, font: QFont | str):
        self._scale_fontname = font

        self.update()

    def setScaleFontFamily(self, font: QFont | str):
        self.scaleFontFamily=font

    @Property(QFont)
    def valueFontFamily(self):
        return self._value_fontname

    @valueFontFamily.setter
    def valueFontFamily(self, font: QFont | str):
        self._value_fontname = font

        self.update()

    def setValueFontFamily(self, font: QFont | str):
        self.valueFontFamily=font

    @Property(QColor)
    def bigScaleColor(self):
        return self._big_scale_marker

    @bigScaleColor.setter
    def bigScaleColor(self, color: QColor):
        self._big_scale_marker = color

        self.update()

    def setBigScaleColor(self, color: QColor):
        self._big_scale_marker = color       

    @Property(bool)
    def enableNeedlePolygon(self):
        return self._enable_needle_polygon

    @enableNeedlePolygon.setter
    def enableNeedlePolygon(self, enable: bool):
        self._enable_needle_polygon = enable

        self.update()

    def setEnableNeedlePolygon(self, enable: bool = True):
        self.enableNeedlePolygon = enable

    @Property(bool)
    def enableScaleText(self):
        return self._enable_scale_text

    @enableScaleText.setter
    def enableScaleText(self, enable: bool = True):
        self._enable_scale_text = enable

        self.update()

    def setEnableScaleText(self, enable=True):
        self.enableScaleText = enable

    @Property(bool)
    def enableBarGraph(self):
        return self._enable_bar_graph

    @enableBarGraph.setter
    def enableBarGraph(self, enable: bool = True):
        self._enable_bar_graph = enable

        self.update()

    def setEnableBarGraph(self, enable=True):
        self.enableBarGraph = enable

    @Property(bool)
    def enableValueText(self):
        return self._enable_value_text

    @enableValueText.setter
    def enableValueText(self, enable: bool = True):
        self._enable_value_text = enable

        self.update()

    def setEnableValueText(self, enable=True):
        self.enableValueText = enable

    @Property(bool)
    def enableCenterPoint(self):
        return self._enable_center_point

    @enableCenterPoint.setter
    def enableCenterPoint(self, enable: bool = True):
        self._enable_center_point = enable

        self.update()

    def setEnableCenterPoint(self, enable=True):
        self.enableCenterPoint = enable

    @Property(bool)
    def enableScalePolygon(self):
        return self._enable_filled_polygon

    @enableScalePolygon.setter
    def enableScalePolygon(self, enable: bool = True):
        self._enable_filled_polygon = enable

        self.update()

    def setEnableScalePolygon(self, enable=True):
        self.enableScalePolygon = enable

    @Property(bool)
    def enableBigScaleGrid(self):
        return self._enable_big_scaled_marker

    @enableBigScaleGrid.setter
    def enableBigScaleGrid(self, enable: bool = True):
        self._enable_big_scaled_marker = enable

        self.update()

    def setEnableBigScaleGrid(self, enable=True):
        self.enableBigScaleGrid = enable

    @Property(bool)
    def enableFineScaleGrid(self):
        return self._enable_fine_scaled_marker

    @enableFineScaleGrid.setter
    def enableFineScaleGrid(self, enable: bool = True):
        self._enable_fine_scaled_marker = enable

        self.update()

    def setEnableFineScaleGrid(self, enable=True):
        self.enableFineScaleGrid = enable

    @Property(int)
    def scalaCount(self):
        return self._scala_count

    @scalaCount.setter
    def scalaCount(self, count: int):
        if count < 1:
            count = 1
        self._scala_count = count

        self.update()

    def setScalaCount(self, count):
        self.scalaCount = count

    @Property(float)
    def scaleStartAngle(self):
        return self._scale_angle_start_value

    @scaleStartAngle.setter
    def scaleStartAngle(self, value: float):
        self._scale_angle_start_value = value

        self.update()

    def setScaleStartAngle(self, value):
        self.scaleStartAngle = value

    @Property(float)
    def totalScaleAngleSize(self):
        return self._scale_angle_size

    @totalScaleAngleSize.setter
    def totalScaleAngleSize(self, value: float):
        self._scale_angle_size = value

        self.update()

    def setTotalScaleAngleSize(self, value: float):
        self.totalScaleAngleSize = value

    @Property(float)
    def angleOffset(self):
        return self._angle_offset

    @angleOffset.setter
    def angleOffset(self, value: float):
        self._angle_offset = value

        self.update()

    def setAngleOffset(self, offset: float):
        self.angleOffset = offset

    @Property(float)
    def gaugeColorOuterRadiusFactor(self):
        return self._gauge_color_outer_radius_factor

    @gaugeColorOuterRadiusFactor.setter
    def gaugeColorOuterRadiusFactor(self, value: float):
        self._gauge_color_outer_radius_factor = float(value) / 1000

        self.update()

    def setGaugeColorOuterRadiusFactor(self, value):
        self.gaugeColorOuterRadiusFactor = value

    @Property(float)
    def gaugeColorInnerRadiusFactor(self):
        return self._gauge_color_inner_radius_factor

    @gaugeColorInnerRadiusFactor.setter
    def gaugeColorInnerRadiusFactor(self, value: float):
        self._gauge_color_inner_radius_factor = float(value) / 1000

        self.update()

    def setGaugeColorInnerRadiusFactor(self, value):
        self.gaugeColorInnerRadiusFactor = value


    def setGaugeTheme(self, Theme=0):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        theme_file = os.path.join(script_dir, "components/json/QAnalogGaugeThemes.json")
        with open(theme_file, 'r') as file:
            themes_data = json.load(file)

        if Theme < len(themes_data["themes"]):
            theme = themes_data["themes"][Theme]

            if "scale_polygon_colors" in theme:
                self.scale_polygon_colors = [
                    [scale[0], QColor(scale[1])] for scale in theme["scale_polygon_colors"]
                ]

            if "needle_center_bg" in theme:
                self.needle_center_bg = [
                    [bg[0], QColor(bg[1])] for bg in theme["needle_center_bg"]
                ]

            if "outer_circle_bg" in theme:
                self.outer_circle_bg = [
                    [bg[0], QColor(bg[1])] for bg in theme["outer_circle_bg"]
                ]

            if "bigScaleMarker" in theme:
                self._big_scale_marker = QColor(theme["bigScaleMarker"])
            if "fineScaleColor" in theme:
                self._fine_scale_color = QColor(theme["fineScaleColor"])

            if "customTheme" in theme:
                custom_theme = theme["customTheme"]
                self.setCustomGaugeTheme(custom_theme)

            self.update()
        else:
            self._themeNumber = 0
            self.setGaugeTheme(0)
    
    # SET CUSTOM GAUGE THEME
    def setCustomGaugeTheme(self, custom_theme: list):
        scale_polygon_colors = []
        needle_center_bg = []
        outer_circle_bg = []

        for x, color in enumerate(custom_theme):
            scale_polygon_colors.append([float(color[0]), QColor(color[1])])
            needle_center_bg.append([float(color[0]), QColor(color[1])])
            outer_circle_bg.append([float(color[0]), QColor(color[1])])

        self.scale_polygon_colors = scale_polygon_colors
        self.needle_center_bg = needle_center_bg
        self.outer_circle_bg = outer_circle_bg

    
    def setScalePolygonColor(self, **color_positions):
        if color_positions:
            scale_polygon_colors = []

            for position, color in color_positions.items():
                scale_polygon_colors.append([float(position), QColor(str(color))])

            self.scale_polygon_colors = scale_polygon_colors
        else:
            logInfo("Custom Gauge Theme: No colors defined")

    def setNeedleCenterColor(self, **color_positions):
        if color_positions:
            needle_center_bg = []

            for position, color in color_positions.items():
                needle_center_bg.append([float(position), QColor(str(color))])

            self.needle_center_bg = needle_center_bg
        else:
            logInfo("Custom Gauge Theme: No colors defined")

    def setOuterCircleColor(self, **color_positions):
        if color_positions:
            outer_circle_bg = []

            for position, color in color_positions.items():
                outer_circle_bg.append([float(position), QColor(str(color))])

            self.outer_circle_bg = outer_circle_bg
        else:
            logInfo("Custom Gauge Theme: No colors defined")

    # RESCALE
    def rescale_method(self):
        # SET WIDTH AND HEIGHT
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()

        
        # SET NEEDLE SIZE
        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, - self.widget_diameter / 2 * self._needle_scale_factor),
            QPoint(0, - self.widget_diameter / 2 * self._needle_scale_factor - 6),
            QPoint(2, - self.widget_diameter / 2 * self._needle_scale_factor)
        ])])

        # SET FONT SIZE
        self.scale_fontsize = self._initial_scale_fontsize * self.widget_diameter / 400
        self.value_fontsize = self._initial_value_fontsize * self.widget_diameter / 400


    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)

    def center_horizontal(self, value):
        self.center_horizontal_value = value

    def center_vertical(self, value):
        self.center_vertical_value = value


    # CREATE PIE
    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph = True):
        polygon_pie = QPolygonF()
    
        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        # todo enable/disable bar graf here
        if not self._enable_bar_graph and bar_graph:
            # float_value = ((lenght / (self._max_value - self._min_value)) * (self._value - self._min_value))
            lenght = int(round((lenght / (self._max_value - self._min_value)) * (self._value - self._min_value)))

        for i in range(lenght+1):                                              # add the points of polygon
            t = w * i + start - self._angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        for i in range(lenght+1):                                              # add the points of polygon
            t = w * (lenght - i) + start - self._angle_offset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        if not self.scale_polygon_colors == None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            # Koordinatenursprung in die Mitte der Flaeche legen
            painter_filled_polygon.translate(self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self._pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self._pen)

            colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self._pen.width() / 2)) * self._gauge_color_outer_radius_factor,
                (((self.widget_diameter / 2) - (self._pen.width() / 2)) * self._gauge_color_inner_radius_factor),
                self._scale_angle_start_value, self._scale_angle_size)

            gauge_rect = QRect(QPoint(0, 0), QSize(self.widget_diameter / 2 - 1, self.widget_diameter - 1))
            if isinstance(self.scale_polygon_colors, list):
                grad = QConicalGradient(QPointF(0, 0), - self._scale_angle_size - self._scale_angle_start_value +
                                    self._angle_offset - 1)
            else:
                grad = self.scale_polygon_colors

            # todo definition scale color as array here
            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])

            painter_filled_polygon.setBrush(grad)
            painter_filled_polygon.drawPolygon(colored_scale_polygon)

    def draw_icon_image(self):
        pass

    #######################
    # BIG SCALE MARKERS
    #######################
    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        # my_painter.setPen(Qt.NoPen)
        self._pen = QPen(self._big_scale_marker)
        self._pen.setWidth(2)
        # # if outline_pen_with > 0:
        my_painter.setPen(self._pen)

        my_painter.rotate(self._scale_angle_start_value - self._angle_offset)
        steps_size = (float(self._scale_angle_size) / float(self._scala_count))
        scale_line_outer_start = self.widget_diameter/2
        scale_line_lenght = (self.widget_diameter / 2) - (self.widget_diameter / 20)
        for i in range(self._scala_count+1):
            my_painter.drawLine(scale_line_lenght, 0, scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        if not isinstance(self._value_fontname, QFont):
            font = QFont(self._scale_fontname, self.scale_fontsize, QFont.Bold)
        else:
            font = self._scale_fontname

        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self._scale_value_color)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter/2 * text_radius_factor

        scale_per_div = int((self._max_value - self._min_value) / self._scala_count)

        angle_distance = (float(self._scale_angle_size) / float(self._scala_count))
        for i in range(self._scala_count + 1):
            # text = str(int((self._max_value - self._min_value) / self._scala_count * i))
            text = str(int(self._min_value + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(font)
            angle = angle_distance * i + float(self._scale_angle_start_value - self._angle_offset)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))

            text = [x - int(w/2), y - int(h/2), int(w), int(h), Qt.AlignCenter, text]
            painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])
    
    # FINE SCALE MARKERS
    def create_fine_scaled_marker(self):
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self._fine_scale_color)
        my_painter.rotate(self._scale_angle_start_value - self._angle_offset)
        steps_size = (float(self._scale_angle_size) / float(self._scala_count * self._scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter/2
        scale_line_lenght = (self.widget_diameter / 2) - (self.widget_diameter / 40)
        for i in range((self._scala_count * self._scala_subdiv_count)+1):
            my_painter.drawLine(scale_line_lenght, 0, scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    
    # VALUE TEXT
    def create_values_text(self):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.HighQualityAntialiasing)
        except AttributeError:
            try:
                painter.setRenderHint(QPainter.Antialiasing)
            except AttributeError:
                # Neither hint is available; you can handle this case as needed
                pass

        painter.translate(self.width() / 2, self.height() / 2)
        if not isinstance(self._value_fontname, QFont):
            font = QFont(self._value_fontname, self.value_fontsize, QFont.Bold)
        else:
            font = self._value_fontname
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self._display_value_color)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self._text_radius_factor

        # angle_distance = (float(self._scale_angle_size) / float(self._scala_count))
        text = str(int(self._value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(font)

        angle_end = float(self._scale_angle_start_value + self._scale_angle_size - 360)
        angle = (angle_end - self._scale_angle_start_value) / 2 + self._scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        text = [x - int(w/2), y - int(h/2), int(w), int(h), Qt.AlignCenter, text]
        painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])

    # UNITS TEXT
    def create_units_text(self):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.HighQualityAntialiasing)
        except AttributeError:
            try:
                painter.setRenderHint(QPainter.Antialiasing)
            except AttributeError:
                # Neither hint is available; you can handle this case as needed
                pass

        painter.translate(self.width() / 2, self.height() / 2)

        if not isinstance(self._value_fontname, QFont):
            font = QFont(self._value_fontname, int(self.value_fontsize / 2.5), QFont.Bold)
        else:
            font = self._value_fontname
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self._display_value_color)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self._text_radius_factor

        text = str(self._units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(font)

      
        angle_end = float(self._scale_angle_start_value + self._scale_angle_size + 180)
        angle = (angle_end - self._scale_angle_start_value) / 2 + self._scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        text = [x - int(w/2), y - int(h/2), int(w), int(h), Qt.AlignCenter, text]
        painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])
    
    # CENTER POINTER
    def draw_big_needle_center_point(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)

        # create_polygon_pie(self, outer_radius, inner_raduis, start, lenght)
        colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 8) - (self._pen.width() / 2)),
                0,
                self._scale_angle_start_value, 360, False)

        grad = QConicalGradient(QPointF(0, 0), 0)

        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(grad)
        painter.drawPolygon(colored_scale_polygon)
    
    # CREATE OUTER COVER
    def draw_outer_circle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self._pen.width())),
                (self.widget_diameter / 6),
                self._scale_angle_start_value / 10, 360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)
        painter.drawPolygon(colored_scale_polygon)

    # NEEDLE POINTER
    def draw_needle(self):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._needle_color)
        painter.rotate(((self._value - self._value_offset - self._min_value) * self._scale_angle_size /
                        (self._max_value - self._min_value)) + 90 + self._scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    # ON WINDOW RESIZE
    def resizeEvent(self, event):
        self.rescale_method()

    
    # ON PAINT EVENT
    def paintEvent(self, event):
        self.draw_outer_circle()
        self.draw_icon_image()
        # colored pie area
        if self._enable_filled_polygon:
            self.draw_filled_polygon()

        # draw scale marker lines
        if self._enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self._enable_big_scaled_marker:
            self.draw_big_scaled_marker()

        # draw scale marker value text
        if self._enable_scale_text:
            self.create_scale_marker_values_text()

        # Display Value
        if self._enable_value_text:
            self.create_values_text()
            self.create_units_text()

        # draw needle 1
        if self._enable_needle_polygon:
            self.draw_needle()

        # Draw Center Point
        if self._enable_center_point:
            self.draw_big_needle_center_point(diameter=(self.widget_diameter / 6))

    # MOUSE EVENTS
    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseReleaseEvent(self, QMouseEvent):
        self._needle_color = self._needle_color
        self.update()

    
    ## MOUSE LEAVE EVENT
    def leaveEvent(self, event):
        self._needle_color = self._needle_color
        self.update() 

    def mouseMoveEvent(self, event):
        x, y = event.x() - (self.width() / 2), event.y() - (self.height() / 2)
        if not x == 0: 
            angle = math.atan2(y, x) / math.pi * 180
            value = (float(math.fmod(angle - self._scale_angle_start_value + 720, 360)) / \
                     (float(self._scale_angle_size) / float(self._max_value - self._min_value))) + self._min_value
            temp = value
            fmod = float(math.fmod(angle - self._scale_angle_start_value + 720, 360))
            state = 0
            if (self._value - (self._max_value - self._min_value) * self._value_needle_snapzone) <= \
                    value <= \
                    (self._value + (self._max_value - self._min_value) * self._value_needle_snapzone):
                self._needle_color = self._needle_color_drag
                # todo: evtl ueberpruefen
                #
                state = 9
                if value >= self._max_value and self.last_value < (self._max_value - self._min_value) / 2:
                    state = 1
                    value = self._max_value
                    self.last_value = self._min_value
                    self.valueChanged.emit(int(value))

                elif value >= self._max_value >= self.last_value:
                    state = 2
                    value = self._max_value
                    self.last_value = self._max_value
                    self.valueChanged.emit(int(value))


                else:
                    state = 3
                    self.last_value = value
                    self.valueChanged.emit(int(value))

                self.setValue(value)   

        self.update()         

