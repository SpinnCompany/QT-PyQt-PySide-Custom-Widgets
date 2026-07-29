# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_HeroCard.ui'
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

from Custom_Widgets.QCustomCoverFlow import QCustomCoverFlow
class Ui_HeroCard(object):
    def setupUi(self, heroRoot):
        if not heroRoot.objectName():
            heroRoot.setObjectName(u"heroRoot")
        heroRoot.resize(900, 330)
        self.heroLayout = QVBoxLayout(heroRoot)
        self.heroLayout.setSpacing(0)
        self.heroLayout.setObjectName(u"heroLayout")
        self.heroLayout.setContentsMargins(0, 0, 0, 0)
        self.coverFlow = QCustomCoverFlow(heroRoot)
        self.coverFlow.setObjectName(u"coverFlow")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coverFlow.sizePolicy().hasHeightForWidth())
        self.coverFlow.setSizePolicy(sizePolicy)

        self.heroLayout.addWidget(self.coverFlow)


        self.retranslateUi(heroRoot)

        QMetaObject.connectSlotsByName(heroRoot)
    # setupUi

    def retranslateUi(self, heroRoot):
        pass
    # retranslateUi

