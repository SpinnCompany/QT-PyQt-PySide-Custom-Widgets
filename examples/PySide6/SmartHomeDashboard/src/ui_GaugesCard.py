# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_GaugesCard.ui'
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
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
class Ui_GaugesCard(object):
    def setupUi(self, GaugesCard):
        if not GaugesCard.objectName():
            GaugesCard.setObjectName(u"GaugesCard")
        GaugesCard.resize(560, 280)
        self.gaugesRoot = QVBoxLayout(GaugesCard)
        self.gaugesRoot.setSpacing(0)
        self.gaugesRoot.setObjectName(u"gaugesRoot")
        self.gaugesRoot.setContentsMargins(0, 0, 0, 0)
        self.gaugesCard = QFrame(GaugesCard)
        self.gaugesCard.setObjectName(u"gaugesCard")
        self.gaugesCard.setFrameShape(QFrame.StyledPanel)
        self.gaugesLayout = QVBoxLayout(self.gaugesCard)
        self.gaugesLayout.setSpacing(6)
        self.gaugesLayout.setObjectName(u"gaugesLayout")
        self.gaugesLayout.setContentsMargins(28, 26, 28, 24)
        self.gaugesHeader = QHBoxLayout()
        self.gaugesHeader.setObjectName(u"gaugesHeader")
        self.tempTitle = QLabel(self.gaugesCard)
        self.tempTitle.setObjectName(u"tempTitle")
        self.tempTitle.setAlignment(Qt.AlignCenter)

        self.gaugesHeader.addWidget(self.tempTitle)

        self.powerTitle = QLabel(self.gaugesCard)
        self.powerTitle.setObjectName(u"powerTitle")
        self.powerTitle.setAlignment(Qt.AlignCenter)

        self.gaugesHeader.addWidget(self.powerTitle)

        self.gaugesMenu = QPushButton(self.gaugesCard)
        self.gaugesMenu.setObjectName(u"gaugesMenu")
        self.gaugesMenu.setMinimumSize(QSize(30, 26))
        self.gaugesMenu.setMaximumSize(QSize(30, 26))

        self.gaugesHeader.addWidget(self.gaugesMenu)


        self.gaugesLayout.addLayout(self.gaugesHeader)

        self.gaugesRow = QHBoxLayout()
        self.gaugesRow.setSpacing(16)
        self.gaugesRow.setObjectName(u"gaugesRow")
        self.tempGauge = QCustomRadialGauge(self.gaugesCard)
        self.tempGauge.setObjectName(u"tempGauge")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tempGauge.sizePolicy().hasHeightForWidth())
        self.tempGauge.setSizePolicy(sizePolicy)
        self.tempGauge.setMinimumSize(QSize(0, 150))

        self.gaugesRow.addWidget(self.tempGauge)

        self.powerGauge = QCustomRadialGauge(self.gaugesCard)
        self.powerGauge.setObjectName(u"powerGauge")
        sizePolicy.setHeightForWidth(self.powerGauge.sizePolicy().hasHeightForWidth())
        self.powerGauge.setSizePolicy(sizePolicy)
        self.powerGauge.setMinimumSize(QSize(0, 150))

        self.gaugesRow.addWidget(self.powerGauge)


        self.gaugesLayout.addLayout(self.gaugesRow)

        self.statusRow = QHBoxLayout()
        self.statusRow.setObjectName(u"statusRow")
        self.tempStatus = QWidget(self.gaugesCard)
        self.tempStatus.setObjectName(u"tempStatus")
        self.tempStatusLay = QHBoxLayout(self.tempStatus)
        self.tempStatusLay.setSpacing(6)
        self.tempStatusLay.setObjectName(u"tempStatusLay")
        self.tempStatusLay.setContentsMargins(0, 0, 0, 0)

        self.statusRow.addWidget(self.tempStatus)

        self.powerStatus = QWidget(self.gaugesCard)
        self.powerStatus.setObjectName(u"powerStatus")
        self.powerStatusLay = QHBoxLayout(self.powerStatus)
        self.powerStatusLay.setSpacing(6)
        self.powerStatusLay.setObjectName(u"powerStatusLay")
        self.powerStatusLay.setContentsMargins(0, 0, 0, 0)

        self.statusRow.addWidget(self.powerStatus)


        self.gaugesLayout.addLayout(self.statusRow)


        self.gaugesRoot.addWidget(self.gaugesCard)


        self.retranslateUi(GaugesCard)

        QMetaObject.connectSlotsByName(GaugesCard)
    # setupUi

    def retranslateUi(self, GaugesCard):
        self.gaugesCard.setProperty(u"role", QCoreApplication.translate("GaugesCard", u"card", None))
        self.tempTitle.setText(QCoreApplication.translate("GaugesCard", u"Temperature", None))
        self.tempTitle.setProperty(u"role", QCoreApplication.translate("GaugesCard", u"gaugeTitle", None))
        self.powerTitle.setText(QCoreApplication.translate("GaugesCard", u"Power", None))
        self.powerTitle.setProperty(u"role", QCoreApplication.translate("GaugesCard", u"gaugeTitle", None))
        self.gaugesMenu.setText("")
        self.gaugesMenu.setProperty(u"role", QCoreApplication.translate("GaugesCard", u"menuBtn", None))
        pass
    # retranslateUi

