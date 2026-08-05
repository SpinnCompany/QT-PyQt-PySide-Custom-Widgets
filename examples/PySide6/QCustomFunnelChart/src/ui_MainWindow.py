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
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomFunnelChart import QCustomFunnelChart
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(620, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(14)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.funnelChart = QCustomFunnelChart(self.centralwidget)
        self.funnelChart.setObjectName(u"funnelChart")
        self.funnelChart.setMinimumSize(QSize(0, 300))
        self.funnelChart.setProperty(u"showPercent", True)

        self.mainLayout.addWidget(self.funnelChart)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(8)
        self.controlsRow.setObjectName(u"controlsRow")
        self.shapeCaption = QLabel(self.centralwidget)
        self.shapeCaption.setObjectName(u"shapeCaption")

        self.controlsRow.addWidget(self.shapeCaption)

        self.shapeCombo = QComboBox(self.centralwidget)
        self.shapeCombo.addItem("")
        self.shapeCombo.addItem("")
        self.shapeCombo.setObjectName(u"shapeCombo")

        self.controlsRow.addWidget(self.shapeCombo)

        self.orientCaption = QLabel(self.centralwidget)
        self.orientCaption.setObjectName(u"orientCaption")

        self.controlsRow.addWidget(self.orientCaption)

        self.orientCombo = QComboBox(self.centralwidget)
        self.orientCombo.addItem("")
        self.orientCombo.addItem("")
        self.orientCombo.setObjectName(u"orientCombo")

        self.controlsRow.addWidget(self.orientCombo)

        self.basisCaption = QLabel(self.centralwidget)
        self.basisCaption.setObjectName(u"basisCaption")

        self.controlsRow.addWidget(self.basisCaption)

        self.basisCombo = QComboBox(self.centralwidget)
        self.basisCombo.addItem("")
        self.basisCombo.addItem("")
        self.basisCombo.setObjectName(u"basisCombo")

        self.controlsRow.addWidget(self.basisCombo)

        self.neckCaption = QLabel(self.centralwidget)
        self.neckCaption.setObjectName(u"neckCaption")

        self.controlsRow.addWidget(self.neckCaption)

        self.neckSlider = QSlider(self.centralwidget)
        self.neckSlider.setObjectName(u"neckSlider")
        self.neckSlider.setMaximum(80)
        self.neckSlider.setOrientation(Qt.Horizontal)

        self.controlsRow.addWidget(self.neckSlider)

        self.themeBtn = QPushButton(self.centralwidget)
        self.themeBtn.setObjectName(u"themeBtn")

        self.controlsRow.addWidget(self.themeBtn)

        self.controlsRow.setStretch(7, 1)

        self.mainLayout.addLayout(self.controlsRow)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.mainLayout.addWidget(self.statusLabel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomFunnelChart", None))
        self.shapeCaption.setText(QCoreApplication.translate("MainWindow", u"Shape", None))
        self.shapeCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"funnel", None))
        self.shapeCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"pyramid", None))

        self.orientCaption.setText(QCoreApplication.translate("MainWindow", u"Orientation", None))
        self.orientCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"vertical", None))
        self.orientCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"horizontal", None))

        self.basisCaption.setText(QCoreApplication.translate("MainWindow", u"% of", None))
        self.basisCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"first", None))
        self.basisCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"previous", None))

        self.neckCaption.setText(QCoreApplication.translate("MainWindow", u"Neck", None))
        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Hover a stage for its conversion", None))
    # retranslateUi

