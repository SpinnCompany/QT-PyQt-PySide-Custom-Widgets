# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomScatterChart import QCustomScatterChart
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(720, 640)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(14)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(20, 20, 20, 20)
        self.chart = QCustomScatterChart(self.centralwidget)
        self.chart.setObjectName(u"chart")
        self.chart.setMinimumSize(QSize(0, 280))

        self.rootLayout.addWidget(self.chart)

        self.bubbles = QCustomScatterChart(self.centralwidget)
        self.bubbles.setObjectName(u"bubbles")
        self.bubbles.setMinimumSize(QSize(0, 200))
        self.bubbles.setProperty(u"markerOpacity", 0.550000000000000)

        self.rootLayout.addWidget(self.bubbles)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(8)
        self.controlsRow.setObjectName(u"controlsRow")
        self.markerLabel = QLabel(self.centralwidget)
        self.markerLabel.setObjectName(u"markerLabel")

        self.controlsRow.addWidget(self.markerLabel)

        self.shapeCombo = QComboBox(self.centralwidget)
        self.shapeCombo.addItem("")
        self.shapeCombo.addItem("")
        self.shapeCombo.addItem("")
        self.shapeCombo.addItem("")
        self.shapeCombo.setObjectName(u"shapeCombo")

        self.controlsRow.addWidget(self.shapeCombo)

        self.sizeLabel = QLabel(self.centralwidget)
        self.sizeLabel.setObjectName(u"sizeLabel")

        self.controlsRow.addWidget(self.sizeLabel)

        self.sizeSlider = QSlider(self.centralwidget)
        self.sizeSlider.setObjectName(u"sizeSlider")
        self.sizeSlider.setMinimum(3)
        self.sizeSlider.setMaximum(24)
        self.sizeSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.sizeSlider)

        self.ticksLabel = QLabel(self.centralwidget)
        self.ticksLabel.setObjectName(u"ticksLabel")

        self.controlsRow.addWidget(self.ticksLabel)

        self.tickSpin = QSpinBox(self.centralwidget)
        self.tickSpin.setObjectName(u"tickSpin")
        self.tickSpin.setMinimum(2)
        self.tickSpin.setMaximum(12)

        self.controlsRow.addWidget(self.tickSpin)

        self.gridBtn = QPushButton(self.centralwidget)
        self.gridBtn.setObjectName(u"gridBtn")

        self.controlsRow.addWidget(self.gridBtn)

        self.legendBtn = QPushButton(self.centralwidget)
        self.legendBtn.setObjectName(u"legendBtn")

        self.controlsRow.addWidget(self.legendBtn)

        self.themeBtn = QPushButton(self.centralwidget)
        self.themeBtn.setObjectName(u"themeBtn")

        self.controlsRow.addWidget(self.themeBtn)

        self.controlsSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.rootLayout.addLayout(self.controlsRow)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.rootLayout.addWidget(self.statusLabel)

        self.rootLayout.setStretch(0, 2)
        self.rootLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomScatterChart Showcase", None))
        self.chart.setProperty(u"xAxisTitle", QCoreApplication.translate("MainWindow", u"Session", None))
        self.chart.setProperty(u"yAxisTitle", QCoreApplication.translate("MainWindow", u"Score", None))
        self.bubbles.setProperty(u"xAxisTitle", QCoreApplication.translate("MainWindow", u"Quarter", None))
        self.bubbles.setProperty(u"yAxisTitle", QCoreApplication.translate("MainWindow", u"Revenue", None))
        self.markerLabel.setText(QCoreApplication.translate("MainWindow", u"Marker", None))
        self.shapeCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"circle", None))
        self.shapeCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"square", None))
        self.shapeCombo.setItemText(2, QCoreApplication.translate("MainWindow", u"diamond", None))
        self.shapeCombo.setItemText(3, QCoreApplication.translate("MainWindow", u"triangle", None))

        self.sizeLabel.setText(QCoreApplication.translate("MainWindow", u"Size", None))
        self.ticksLabel.setText(QCoreApplication.translate("MainWindow", u"Ticks", None))
        self.gridBtn.setText(QCoreApplication.translate("MainWindow", u"Grid", None))
        self.legendBtn.setText(QCoreApplication.translate("MainWindow", u"Legend", None))
        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Hover a marker for its coordinates", None))
    # retranslateUi

