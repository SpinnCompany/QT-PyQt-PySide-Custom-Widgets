# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_StatCard.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
class Ui_StatCard(object):
    def setupUi(self, StatCard):
        if not StatCard.objectName():
            StatCard.setObjectName(u"StatCard")
        StatCard.resize(260, 110)
        self.statRoot = QVBoxLayout(StatCard)
        self.statRoot.setSpacing(0)
        self.statRoot.setObjectName(u"statRoot")
        self.statRoot.setContentsMargins(0, 0, 0, 0)
        self.statGlass = QCustomGlassFrame(StatCard)
        self.statGlass.setObjectName(u"statGlass")
        self.statGlass.setProperty(u"cornerRadius", 22)
        self.statLayout = QVBoxLayout(self.statGlass)
        self.statLayout.setSpacing(6)
        self.statLayout.setObjectName(u"statLayout")
        self.statLayout.setContentsMargins(18, 16, 18, 16)
        self.statLabel = QLabel(self.statGlass)
        self.statLabel.setObjectName(u"statLabel")

        self.statLayout.addWidget(self.statLabel)

        self.statValue = QLabel(self.statGlass)
        self.statValue.setObjectName(u"statValue")

        self.statLayout.addWidget(self.statValue)


        self.statRoot.addWidget(self.statGlass)


        self.retranslateUi(StatCard)

        QMetaObject.connectSlotsByName(StatCard)
    # setupUi

    def retranslateUi(self, StatCard):
        self.statGlass.setProperty(u"backdropSource", QCoreApplication.translate("StatCard", u"wallpaper", None))
        self.statLabel.setText(QCoreApplication.translate("StatCard", u"Current Consumption", None))
        self.statLabel.setProperty(u"role", QCoreApplication.translate("StatCard", u"mutedSm", None))
        self.statValue.setText(QCoreApplication.translate("StatCard", u"1,5 kWh", None))
        self.statValue.setProperty(u"role", QCoreApplication.translate("StatCard", u"statValue", None))
        pass
    # retranslateUi

