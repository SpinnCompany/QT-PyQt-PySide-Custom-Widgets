# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_LeftRail.ui'
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
    QSpacerItem, QVBoxLayout, QWidget)
class Ui_LeftRail(object):
    def setupUi(self, LeftRail):
        if not LeftRail.objectName():
            LeftRail.setObjectName(u"LeftRail")
        LeftRail.resize(64, 560)
        self.railLayout = QVBoxLayout(LeftRail)
        self.railLayout.setSpacing(14)
        self.railLayout.setObjectName(u"railLayout")
        self.railLayout.setContentsMargins(0, 6, 0, 6)
        self.railBtn0 = QPushButton(LeftRail)
        self.railBtn0.setObjectName(u"railBtn0")
        self.railBtn0.setMinimumSize(QSize(46, 46))
        self.railBtn0.setMaximumSize(QSize(46, 46))
        self.railBtn0.setCheckable(True)
        self.railBtn0.setChecked(True)

        self.railLayout.addWidget(self.railBtn0, 0, Qt.AlignHCenter)

        self.railBtn1 = QPushButton(LeftRail)
        self.railBtn1.setObjectName(u"railBtn1")
        self.railBtn1.setMinimumSize(QSize(46, 46))
        self.railBtn1.setMaximumSize(QSize(46, 46))
        self.railBtn1.setCheckable(True)

        self.railLayout.addWidget(self.railBtn1, 0, Qt.AlignHCenter)

        self.railBtn2 = QPushButton(LeftRail)
        self.railBtn2.setObjectName(u"railBtn2")
        self.railBtn2.setMinimumSize(QSize(46, 46))
        self.railBtn2.setMaximumSize(QSize(46, 46))
        self.railBtn2.setCheckable(True)

        self.railLayout.addWidget(self.railBtn2, 0, Qt.AlignHCenter)

        self.railBtn3 = QPushButton(LeftRail)
        self.railBtn3.setObjectName(u"railBtn3")
        self.railBtn3.setMinimumSize(QSize(46, 46))
        self.railBtn3.setMaximumSize(QSize(46, 46))
        self.railBtn3.setCheckable(True)

        self.railLayout.addWidget(self.railBtn3, 0, Qt.AlignHCenter)

        self.railSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.railLayout.addItem(self.railSpacer)

        self.addBtn = QPushButton(LeftRail)
        self.addBtn.setObjectName(u"addBtn")
        self.addBtn.setMinimumSize(QSize(50, 50))
        self.addBtn.setMaximumSize(QSize(50, 50))

        self.railLayout.addWidget(self.addBtn, 0, Qt.AlignHCenter)


        self.retranslateUi(LeftRail)

        QMetaObject.connectSlotsByName(LeftRail)
    # setupUi

    def retranslateUi(self, LeftRail):
        self.railBtn0.setText("")
        self.railBtn0.setProperty(u"role", QCoreApplication.translate("LeftRail", u"railBtn", None))
        self.railBtn1.setText("")
        self.railBtn1.setProperty(u"role", QCoreApplication.translate("LeftRail", u"railBtn", None))
        self.railBtn2.setText("")
        self.railBtn2.setProperty(u"role", QCoreApplication.translate("LeftRail", u"railBtn", None))
        self.railBtn3.setText("")
        self.railBtn3.setProperty(u"role", QCoreApplication.translate("LeftRail", u"railBtn", None))
        self.addBtn.setText("")
        self.addBtn.setProperty(u"role", QCoreApplication.translate("LeftRail", u"fab", None))
        pass
    # retranslateUi

