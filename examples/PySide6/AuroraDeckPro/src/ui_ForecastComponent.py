# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_ForecastComponent.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomAccordion import QCustomAccordion
from Custom_Widgets.QCustomCarousel import QCustomCarousel
from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
from Custom_Widgets.QCustomSplitter import QCustomSplitter
from Custom_Widgets.QCustomStepper import QCustomStepper
class Ui_ForecastComponent(object):
    def setupUi(self, ForecastComponent):
        if not ForecastComponent.objectName():
            ForecastComponent.setObjectName(u"ForecastComponent")
        ForecastComponent.resize(940, 680)
        self.forecastRoot = QVBoxLayout(ForecastComponent)
        self.forecastRoot.setSpacing(14)
        self.forecastRoot.setObjectName(u"forecastRoot")
        self.forecastRoot.setContentsMargins(24, 24, 24, 24)
        self.forecastHeader = QVBoxLayout()
        self.forecastHeader.setSpacing(2)
        self.forecastHeader.setObjectName(u"forecastHeader")
        self.forecastKicker = QLabel(ForecastComponent)
        self.forecastKicker.setObjectName(u"forecastKicker")

        self.forecastHeader.addWidget(self.forecastKicker)

        self.forecastTitle = QLabel(ForecastComponent)
        self.forecastTitle.setObjectName(u"forecastTitle")

        self.forecastHeader.addWidget(self.forecastTitle)

        self.forecastSub = QLabel(ForecastComponent)
        self.forecastSub.setObjectName(u"forecastSub")

        self.forecastHeader.addWidget(self.forecastSub)


        self.forecastRoot.addLayout(self.forecastHeader)

        self.forecastSplitter = QCustomSplitter(ForecastComponent)
        self.forecastSplitter.setObjectName(u"forecastSplitter")
        self.forecastLeft = QFrame(self.forecastSplitter)
        self.forecastLeft.setObjectName(u"forecastLeft")
        self.forecastLeftLayout = QVBoxLayout(self.forecastLeft)
        self.forecastLeftLayout.setSpacing(12)
        self.forecastLeftLayout.setObjectName(u"forecastLeftLayout")
        self.forecastLeftLayout.setContentsMargins(18, 16, 18, 16)
        self.rollingLabel = QLabel(self.forecastLeft)
        self.rollingLabel.setObjectName(u"rollingLabel")

        self.forecastLeftLayout.addWidget(self.rollingLabel)

        self.forecastCarousel = QCustomCarousel(self.forecastLeft)
        self.forecastCarousel.setObjectName(u"forecastCarousel")
        self.forecastCarousel.setMinimumSize(QSize(0, 150))
        self.forecastCarousel.setProperty(u"wrap", True)

        self.forecastLeftLayout.addWidget(self.forecastCarousel)

        self.ringsRow = QHBoxLayout()
        self.ringsRow.setSpacing(16)
        self.ringsRow.setObjectName(u"ringsRow")
        self.ring65Col = QVBoxLayout()
        self.ring65Col.setSpacing(6)
        self.ring65Col.setObjectName(u"ring65Col")
        self.ring65 = QCustomProgressRing(self.forecastLeft)
        self.ring65.setObjectName(u"ring65")
        self.ring65.setMinimumSize(QSize(92, 92))
        self.ring65.setMaximumSize(QSize(92, 92))
        self.ring65.setProperty(u"value", 87)
        self.ring65.setProperty(u"showText", True)

        self.ring65Col.addWidget(self.ring65)

        self.ring65Cap = QLabel(self.forecastLeft)
        self.ring65Cap.setObjectName(u"ring65Cap")
        self.ring65Cap.setAlignment(Qt.AlignCenter)

        self.ring65Col.addWidget(self.ring65Cap)


        self.ringsRow.addLayout(self.ring65Col)

        self.ring60Col = QVBoxLayout()
        self.ring60Col.setSpacing(6)
        self.ring60Col.setObjectName(u"ring60Col")
        self.ring60 = QCustomProgressRing(self.forecastLeft)
        self.ring60.setObjectName(u"ring60")
        self.ring60.setMinimumSize(QSize(92, 92))
        self.ring60.setMaximumSize(QSize(92, 92))
        self.ring60.setProperty(u"value", 62)
        self.ring60.setProperty(u"showText", True)

        self.ring60Col.addWidget(self.ring60)

        self.ring60Cap = QLabel(self.forecastLeft)
        self.ring60Cap.setObjectName(u"ring60Cap")
        self.ring60Cap.setAlignment(Qt.AlignCenter)

        self.ring60Col.addWidget(self.ring60Cap)


        self.ringsRow.addLayout(self.ring60Col)

        self.ring55Col = QVBoxLayout()
        self.ring55Col.setSpacing(6)
        self.ring55Col.setObjectName(u"ring55Col")
        self.ring55 = QCustomProgressRing(self.forecastLeft)
        self.ring55.setObjectName(u"ring55")
        self.ring55.setMinimumSize(QSize(92, 92))
        self.ring55.setMaximumSize(QSize(92, 92))
        self.ring55.setProperty(u"value", 34)
        self.ring55.setProperty(u"showText", True)

        self.ring55Col.addWidget(self.ring55)

        self.ring55Cap = QLabel(self.forecastLeft)
        self.ring55Cap.setObjectName(u"ring55Cap")
        self.ring55Cap.setAlignment(Qt.AlignCenter)

        self.ring55Col.addWidget(self.ring55Cap)


        self.ringsRow.addLayout(self.ring55Col)

        self.ringsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ringsRow.addItem(self.ringsSpacer)


        self.forecastLeftLayout.addLayout(self.ringsRow)

        self.forecastLeftSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.forecastLeftLayout.addItem(self.forecastLeftSpacer)

        self.forecastSplitter.addWidget(self.forecastLeft)
        self.forecastRight = QFrame(self.forecastSplitter)
        self.forecastRight.setObjectName(u"forecastRight")
        self.forecastRightLayout = QVBoxLayout(self.forecastRight)
        self.forecastRightLayout.setSpacing(14)
        self.forecastRightLayout.setObjectName(u"forecastRightLayout")
        self.forecastRightLayout.setContentsMargins(18, 16, 18, 16)
        self.phasesLabel = QLabel(self.forecastRight)
        self.phasesLabel.setObjectName(u"phasesLabel")

        self.forecastRightLayout.addWidget(self.phasesLabel)

        self.phaseStepper = QCustomStepper(self.forecastRight)
        self.phaseStepper.setObjectName(u"phaseStepper")
        self.phaseStepper.setProperty(u"currentStep", 1)

        self.forecastRightLayout.addWidget(self.phaseStepper)

        self.briefingLabel = QLabel(self.forecastRight)
        self.briefingLabel.setObjectName(u"briefingLabel")

        self.forecastRightLayout.addWidget(self.briefingLabel)

        self.briefingAccordion = QCustomAccordion(self.forecastRight)
        self.briefingAccordion.setObjectName(u"briefingAccordion")
        self.briefingAccordion.setProperty(u"exclusive", True)

        self.forecastRightLayout.addWidget(self.briefingAccordion)

        self.forecastRightSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.forecastRightLayout.addItem(self.forecastRightSpacer)

        self.forecastSplitter.addWidget(self.forecastRight)

        self.forecastRoot.addWidget(self.forecastSplitter)


        self.retranslateUi(ForecastComponent)

        QMetaObject.connectSlotsByName(ForecastComponent)
    # setupUi

    def retranslateUi(self, ForecastComponent):
        self.forecastKicker.setProperty(u"role", QCoreApplication.translate("ForecastComponent", u"kicker", None))
        self.forecastKicker.setText(QCoreApplication.translate("ForecastComponent", u"OUTLOOK", None))
        self.forecastTitle.setProperty(u"role", QCoreApplication.translate("ForecastComponent", u"h1", None))
        self.forecastTitle.setText(QCoreApplication.translate("ForecastComponent", u"Forecast", None))
        self.forecastSub.setProperty(u"role", QCoreApplication.translate("ForecastComponent", u"muted", None))
        self.forecastSub.setText(QCoreApplication.translate("ForecastComponent", u"Three-day geomagnetic outlook and mission phases.", None))
        self.forecastSplitter.setProperty(u"orientation", QCoreApplication.translate("ForecastComponent", u"horizontal", None))
        self.forecastLeft.setProperty(u"role", QCoreApplication.translate("ForecastComponent", u"panel", None))
        self.rollingLabel.setProperty(u"role", QCoreApplication.translate("ForecastComponent", u"kicker", None))
        self.rollingLabel.setText(QCoreApplication.translate("ForecastComponent", u"ROLLING FORECAST", None))
        self.ring65Cap.setProperty(u"role", QCoreApplication.translate("ForecastComponent", u"muted", None))
        self.ring65Cap.setText(QCoreApplication.translate("ForecastComponent", u"65\u00b0N", None))
        self.ring60Cap.setProperty(u"role", QCoreApplication.translate("ForecastComponent", u"muted", None))
        self.ring60Cap.setText(QCoreApplication.translate("ForecastComponent", u"60\u00b0N", None))
        self.ring55Cap.setProperty(u"role", QCoreApplication.translate("ForecastComponent", u"muted", None))
        self.ring55Cap.setText(QCoreApplication.translate("ForecastComponent", u"55\u00b0N", None))
        self.forecastRight.setProperty(u"role", QCoreApplication.translate("ForecastComponent", u"panel", None))
        self.phasesLabel.setProperty(u"role", QCoreApplication.translate("ForecastComponent", u"kicker", None))
        self.phasesLabel.setText(QCoreApplication.translate("ForecastComponent", u"MISSION PHASES", None))
        self.briefingLabel.setProperty(u"role", QCoreApplication.translate("ForecastComponent", u"kicker", None))
        self.briefingLabel.setText(QCoreApplication.translate("ForecastComponent", u"BRIEFING", None))
        pass
    # retranslateUi

