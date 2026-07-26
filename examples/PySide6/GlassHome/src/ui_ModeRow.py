# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_ModeRow.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

from Custom_Widgets.QCustomTileButton import QCustomTileButton
class Ui_ModeRow(object):
    def setupUi(self, ModeRow):
        if not ModeRow.objectName():
            ModeRow.setObjectName(u"ModeRow")
        ModeRow.resize(280, 78)
        self.modeRoot = QHBoxLayout(ModeRow)
        self.modeRoot.setSpacing(10)
        self.modeRoot.setObjectName(u"modeRoot")
        self.modeRoot.setContentsMargins(0, 0, 0, 0)
        self.modeHot = QCustomTileButton(ModeRow)
        self.modeHot.setObjectName(u"modeHot")
        self.modeHot.setMinimumSize(QSize(0, 66))
        self.modeHot.setCheckable(True)
        self.modeHot.setProperty(u"cornerRadius", 16)
        self.modeHot.setProperty(u"iconSize", 20)

        self.modeRoot.addWidget(self.modeHot)

        self.modeEco = QCustomTileButton(ModeRow)
        self.modeEco.setObjectName(u"modeEco")
        self.modeEco.setMinimumSize(QSize(0, 66))
        self.modeEco.setCheckable(True)
        self.modeEco.setChecked(True)
        self.modeEco.setProperty(u"cornerRadius", 16)
        self.modeEco.setProperty(u"iconSize", 20)

        self.modeRoot.addWidget(self.modeEco)

        self.modeFan = QCustomTileButton(ModeRow)
        self.modeFan.setObjectName(u"modeFan")
        self.modeFan.setMinimumSize(QSize(0, 66))
        self.modeFan.setCheckable(True)
        self.modeFan.setProperty(u"cornerRadius", 16)
        self.modeFan.setProperty(u"iconSize", 20)

        self.modeRoot.addWidget(self.modeFan)

        self.modeCold = QCustomTileButton(ModeRow)
        self.modeCold.setObjectName(u"modeCold")
        self.modeCold.setMinimumSize(QSize(0, 66))
        self.modeCold.setCheckable(True)
        self.modeCold.setProperty(u"cornerRadius", 16)
        self.modeCold.setProperty(u"iconSize", 20)

        self.modeRoot.addWidget(self.modeCold)


        self.retranslateUi(ModeRow)

        QMetaObject.connectSlotsByName(ModeRow)
    # setupUi

    def retranslateUi(self, ModeRow):
        self.modeHot.setProperty(u"caption", QCoreApplication.translate("ModeRow", u"Hot", None))
        self.modeEco.setProperty(u"caption", QCoreApplication.translate("ModeRow", u"Eco", None))
        self.modeFan.setProperty(u"caption", QCoreApplication.translate("ModeRow", u"Fan", None))
        self.modeCold.setProperty(u"caption", QCoreApplication.translate("ModeRow", u"Cold", None))
        pass
    # retranslateUi

