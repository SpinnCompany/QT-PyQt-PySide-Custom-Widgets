# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_TopBar.ui'
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
class Ui_TopBar(object):
    def setupUi(self, TopBar):
        if not TopBar.objectName():
            TopBar.setObjectName(u"TopBar")
        TopBar.resize(1200, 96)
        self.topRoot = QVBoxLayout(TopBar)
        self.topRoot.setSpacing(0)
        self.topRoot.setObjectName(u"topRoot")
        self.topRoot.setContentsMargins(0, 0, 0, 0)
        self.topBarFrame = QFrame(TopBar)
        self.topBarFrame.setObjectName(u"topBarFrame")
        self.topBarFrame.setFrameShape(QFrame.StyledPanel)
        self.topBarLayout = QHBoxLayout(self.topBarFrame)
        self.topBarLayout.setSpacing(14)
        self.topBarLayout.setObjectName(u"topBarLayout")
        self.topBarLayout.setContentsMargins(26, 0, 30, 0)
        self.avatar = QLabel(self.topBarFrame)
        self.avatar.setObjectName(u"avatar")
        self.avatar.setMinimumSize(QSize(52, 52))
        self.avatar.setMaximumSize(QSize(52, 52))
        self.avatar.setAlignment(Qt.AlignCenter)

        self.topBarLayout.addWidget(self.avatar)

        self.titleCol = QVBoxLayout()
        self.titleCol.setSpacing(0)
        self.titleCol.setObjectName(u"titleCol")
        self.headerTitle = QLabel(self.topBarFrame)
        self.headerTitle.setObjectName(u"headerTitle")

        self.titleCol.addWidget(self.headerTitle)

        self.subRow = QHBoxLayout()
        self.subRow.setSpacing(6)
        self.subRow.setObjectName(u"subRow")
        self.headerSub = QLabel(self.topBarFrame)
        self.headerSub.setObjectName(u"headerSub")

        self.subRow.addWidget(self.headerSub)

        self.memberChevron = QLabel(self.topBarFrame)
        self.memberChevron.setObjectName(u"memberChevron")
        self.memberChevron.setMinimumSize(QSize(14, 14))
        self.memberChevron.setMaximumSize(QSize(14, 14))

        self.subRow.addWidget(self.memberChevron)

        self.subSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.subRow.addItem(self.subSpacer)


        self.titleCol.addLayout(self.subRow)


        self.topBarLayout.addLayout(self.titleCol)

        self.topSpacer = QSpacerItem(60, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBarLayout.addItem(self.topSpacer)

        self.navRow = QHBoxLayout()
        self.navRow.setSpacing(10)
        self.navRow.setObjectName(u"navRow")
        self.navBtn0 = QPushButton(self.topBarFrame)
        self.navBtn0.setObjectName(u"navBtn0")
        self.navBtn0.setMinimumSize(QSize(40, 40))
        self.navBtn0.setMaximumSize(QSize(40, 40))

        self.navRow.addWidget(self.navBtn0)

        self.navBtn1 = QPushButton(self.topBarFrame)
        self.navBtn1.setObjectName(u"navBtn1")
        self.navBtn1.setMinimumSize(QSize(40, 40))
        self.navBtn1.setMaximumSize(QSize(40, 40))

        self.navRow.addWidget(self.navBtn1)

        self.navBtn2 = QPushButton(self.topBarFrame)
        self.navBtn2.setObjectName(u"navBtn2")
        self.navBtn2.setMinimumSize(QSize(40, 40))
        self.navBtn2.setMaximumSize(QSize(40, 40))

        self.navRow.addWidget(self.navBtn2)

        self.navBtn3 = QPushButton(self.topBarFrame)
        self.navBtn3.setObjectName(u"navBtn3")
        self.navBtn3.setMinimumSize(QSize(40, 40))
        self.navBtn3.setMaximumSize(QSize(40, 40))

        self.navRow.addWidget(self.navBtn3)

        self.navBtn4 = QPushButton(self.topBarFrame)
        self.navBtn4.setObjectName(u"navBtn4")
        self.navBtn4.setMinimumSize(QSize(40, 40))
        self.navBtn4.setMaximumSize(QSize(40, 40))

        self.navRow.addWidget(self.navBtn4)

        self.navBtn5 = QPushButton(self.topBarFrame)
        self.navBtn5.setObjectName(u"navBtn5")
        self.navBtn5.setMinimumSize(QSize(40, 40))
        self.navBtn5.setMaximumSize(QSize(40, 40))

        self.navRow.addWidget(self.navBtn5)

        self.navBtn6 = QPushButton(self.topBarFrame)
        self.navBtn6.setObjectName(u"navBtn6")
        self.navBtn6.setMinimumSize(QSize(40, 40))
        self.navBtn6.setMaximumSize(QSize(40, 40))

        self.navRow.addWidget(self.navBtn6)

        self.navBtn7 = QPushButton(self.topBarFrame)
        self.navBtn7.setObjectName(u"navBtn7")
        self.navBtn7.setMinimumSize(QSize(40, 40))
        self.navBtn7.setMaximumSize(QSize(40, 40))

        self.navRow.addWidget(self.navBtn7)


        self.topBarLayout.addLayout(self.navRow)


        self.topRoot.addWidget(self.topBarFrame)


        self.retranslateUi(TopBar)

        QMetaObject.connectSlotsByName(TopBar)
    # setupUi

    def retranslateUi(self, TopBar):
        self.avatar.setText("")
        self.headerTitle.setText(QCoreApplication.translate("TopBar", u"My Home", None))
        self.headerTitle.setProperty(u"role", QCoreApplication.translate("TopBar", u"headerTitle", None))
        self.headerSub.setText(QCoreApplication.translate("TopBar", u"3 MEMBERS", None))
        self.headerSub.setProperty(u"role", QCoreApplication.translate("TopBar", u"headerSub", None))
        self.memberChevron.setText("")
        self.navBtn0.setText("")
        self.navBtn0.setProperty(u"role", QCoreApplication.translate("TopBar", u"navIcon", None))
        self.navBtn1.setText("")
        self.navBtn1.setProperty(u"role", QCoreApplication.translate("TopBar", u"navIcon", None))
        self.navBtn2.setText("")
        self.navBtn2.setProperty(u"role", QCoreApplication.translate("TopBar", u"navIcon", None))
        self.navBtn3.setText("")
        self.navBtn3.setProperty(u"role", QCoreApplication.translate("TopBar", u"navIcon", None))
        self.navBtn4.setText("")
        self.navBtn4.setProperty(u"role", QCoreApplication.translate("TopBar", u"navIcon", None))
        self.navBtn5.setText("")
        self.navBtn5.setProperty(u"role", QCoreApplication.translate("TopBar", u"navIcon", None))
        self.navBtn6.setText("")
        self.navBtn6.setProperty(u"role", QCoreApplication.translate("TopBar", u"navIcon", None))
        self.navBtn7.setText("")
        self.navBtn7.setProperty(u"role", QCoreApplication.translate("TopBar", u"navIcon", None))
        pass
    # retranslateUi

