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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomForm import QCustomForm
from Custom_Widgets.QCustomHeatmap import QCustomHeatmap
from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker
from Custom_Widgets.QCustomWaveform import QCustomWaveform
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1300, 860)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(14)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.headerLabel = QLabel(self.centralwidget)
        self.headerLabel.setObjectName(u"headerLabel")

        self.verticalLayout.addWidget(self.headerLabel)

        self.splitRow = QHBoxLayout()
        self.splitRow.setSpacing(16)
        self.splitRow.setObjectName(u"splitRow")
        self.leftScroll = QScrollArea(self.centralwidget)
        self.leftScroll.setObjectName(u"leftScroll")
        self.leftScroll.setWidgetResizable(True)
        self.leftScroll.setFrameShape(QFrame.NoFrame)
        self.leftContent = QWidget()
        self.leftContent.setObjectName(u"leftContent")
        self.leftContent.setGeometry(QRect(0, 0, 610, 720))
        self.leftLayout = QVBoxLayout(self.leftContent)
        self.leftLayout.setSpacing(12)
        self.leftLayout.setObjectName(u"leftLayout")
        self.formTitle = QLabel(self.leftContent)
        self.formTitle.setObjectName(u"formTitle")

        self.leftLayout.addWidget(self.formTitle)

        self.formCard = QFrame(self.leftContent)
        self.formCard.setObjectName(u"formCard")
        self.formCard.setFrameShape(QFrame.StyledPanel)
        self.formCardLayout = QVBoxLayout(self.formCard)
        self.formCardLayout.setObjectName(u"formCardLayout")
        self.showcaseForm = QCustomForm(self.formCard)
        self.showcaseForm.setObjectName(u"showcaseForm")

        self.formCardLayout.addWidget(self.showcaseForm)


        self.leftLayout.addWidget(self.formCard)

        self.groupsTitle = QLabel(self.leftContent)
        self.groupsTitle.setObjectName(u"groupsTitle")

        self.leftLayout.addWidget(self.groupsTitle)

        self.groupsCard = QFrame(self.leftContent)
        self.groupsCard.setObjectName(u"groupsCard")
        self.groupsCard.setFrameShape(QFrame.StyledPanel)
        self.groupsHostLayout = QVBoxLayout(self.groupsCard)
        self.groupsHostLayout.setSpacing(8)
        self.groupsHostLayout.setObjectName(u"groupsHostLayout")

        self.leftLayout.addWidget(self.groupsCard)

        self.leftSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.leftLayout.addItem(self.leftSpacer)

        self.leftScroll.setWidget(self.leftContent)

        self.splitRow.addWidget(self.leftScroll)

        self.rightScroll = QScrollArea(self.centralwidget)
        self.rightScroll.setObjectName(u"rightScroll")
        self.rightScroll.setWidgetResizable(True)
        self.rightScroll.setFrameShape(QFrame.NoFrame)
        self.rightContent = QWidget()
        self.rightContent.setObjectName(u"rightContent")
        self.rightContent.setGeometry(QRect(0, 0, 610, 720))
        self.rightLayout = QVBoxLayout(self.rightContent)
        self.rightLayout.setSpacing(12)
        self.rightLayout.setObjectName(u"rightLayout")
        self.vizTitle = QLabel(self.rightContent)
        self.vizTitle.setObjectName(u"vizTitle")

        self.rightLayout.addWidget(self.vizTitle)

        self.gaugeSectionLabel = QLabel(self.rightContent)
        self.gaugeSectionLabel.setObjectName(u"gaugeSectionLabel")

        self.rightLayout.addWidget(self.gaugeSectionLabel)

        self.gaugeGrid = QGridLayout()
        self.gaugeGrid.setSpacing(8)
        self.gaugeGrid.setObjectName(u"gaugeGrid")
        self.radialCaption = QLabel(self.rightContent)
        self.radialCaption.setObjectName(u"radialCaption")

        self.gaugeGrid.addWidget(self.radialCaption, 0, 0, 1, 1)

        self.liquidCaption = QLabel(self.rightContent)
        self.liquidCaption.setObjectName(u"liquidCaption")

        self.gaugeGrid.addWidget(self.liquidCaption, 0, 1, 1, 1)

        self.radialGauge = QCustomRadialGauge(self.rightContent)
        self.radialGauge.setObjectName(u"radialGauge")
        self.radialGauge.setMaximumSize(QSize(16777215, 180))
        self.radialGauge.setProperty(u"value", 65.000000000000000)

        self.gaugeGrid.addWidget(self.radialGauge, 1, 0, 1, 1)

        self.liquidGauge = QCustomLiquidGauge(self.rightContent)
        self.liquidGauge.setObjectName(u"liquidGauge")
        self.liquidGauge.setMaximumSize(QSize(16777215, 180))
        self.liquidGauge.setProperty(u"value", 72.000000000000000)

        self.gaugeGrid.addWidget(self.liquidGauge, 1, 1, 1, 1)


        self.rightLayout.addLayout(self.gaugeGrid)

        self.rulerCaption = QLabel(self.rightContent)
        self.rulerCaption.setObjectName(u"rulerCaption")

        self.rightLayout.addWidget(self.rulerCaption)

        self.rulerPicker = QCustomRulerPicker(self.rightContent)
        self.rulerPicker.setObjectName(u"rulerPicker")
        self.rulerPicker.setMaximumSize(QSize(16777215, 80))
        self.rulerPicker.setProperty(u"value", 50.000000000000000)

        self.rightLayout.addWidget(self.rulerPicker)

        self.waveformCaption = QLabel(self.rightContent)
        self.waveformCaption.setObjectName(u"waveformCaption")

        self.rightLayout.addWidget(self.waveformCaption)

        self.waveform = QCustomWaveform(self.rightContent)
        self.waveform.setObjectName(u"waveform")
        self.waveform.setMaximumSize(QSize(16777215, 100))
        self.waveform.setProperty(u"animated", True)

        self.rightLayout.addWidget(self.waveform)

        self.heatmapCaption = QLabel(self.rightContent)
        self.heatmapCaption.setObjectName(u"heatmapCaption")

        self.rightLayout.addWidget(self.heatmapCaption)

        self.heatmap = QCustomHeatmap(self.rightContent)
        self.heatmap.setObjectName(u"heatmap")
        self.heatmap.setMaximumSize(QSize(16777215, 120))

        self.rightLayout.addWidget(self.heatmap)

        self.rightSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightLayout.addItem(self.rightSpacer)

        self.rightScroll.setWidget(self.rightContent)

        self.splitRow.addWidget(self.rightScroll)


        self.verticalLayout.addLayout(self.splitRow)

        self.actionBar = QHBoxLayout()
        self.actionBar.setObjectName(u"actionBar")
        self.actionSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.actionBar.addItem(self.actionSpacer)

        self.submitBtn = QCustomQPushButton(self.centralwidget)
        self.submitBtn.setObjectName(u"submitBtn")

        self.actionBar.addWidget(self.submitBtn)


        self.verticalLayout.addLayout(self.actionBar)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"New Widgets Release \u2014 Input Layer + Data Viz", None))
        self.headerLabel.setText(QCoreApplication.translate("MainWindow", u"Release Ready: New Widgets Showcase", None))
        self.formTitle.setText(QCoreApplication.translate("MainWindow", u"Form Input Layer", None))
        self.groupsTitle.setText(QCoreApplication.translate("MainWindow", u"Selection Buttons (Variants)", None))
        self.vizTitle.setText(QCoreApplication.translate("MainWindow", u"Data Visualization Widgets", None))
        self.gaugeSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Gauges", None))
        self.radialCaption.setText(QCoreApplication.translate("MainWindow", u"Radial Gauge", None))
        self.liquidCaption.setText(QCoreApplication.translate("MainWindow", u"Liquid Gauge", None))
        self.rulerCaption.setText(QCoreApplication.translate("MainWindow", u"Ruler Picker", None))
        self.waveformCaption.setText(QCoreApplication.translate("MainWindow", u"Waveform", None))
        self.waveform.setProperty(u"mode", QCoreApplication.translate("MainWindow", u"bars", None))
        self.heatmapCaption.setText(QCoreApplication.translate("MainWindow", u"Heatmap (Activity Grid)", None))
        self.submitBtn.setText(QCoreApplication.translate("MainWindow", u"Submit Form", None))
        self.submitBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
        self.submitBtn.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
    # retranslateUi

