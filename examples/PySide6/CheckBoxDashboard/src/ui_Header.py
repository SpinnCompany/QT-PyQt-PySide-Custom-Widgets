# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_Header.ui'
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
    QSizePolicy, QSpacerItem, QWidget)
class Ui_Header(object):
    def setupUi(self, Header):
        if not Header.objectName():
            Header.setObjectName(u"Header")
        Header.resize(1000, 56)
        self.headerLayout = QHBoxLayout(Header)
        self.headerLayout.setSpacing(12)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(2, 0, 2, 0)
        self.pageTitle = QLabel(Header)
        self.pageTitle.setObjectName(u"pageTitle")

        self.headerLayout.addWidget(self.pageTitle)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.filterBtn0 = QPushButton(Header)
        self.filterBtn0.setObjectName(u"filterBtn0")
        self.filterBtn0.setMinimumSize(QSize(0, 44))
        self.filterBtn0.setLayoutDirection(Qt.RightToLeft)

        self.headerLayout.addWidget(self.filterBtn0)

        self.filterBtn1 = QPushButton(Header)
        self.filterBtn1.setObjectName(u"filterBtn1")
        self.filterBtn1.setMinimumSize(QSize(0, 44))
        self.filterBtn1.setLayoutDirection(Qt.RightToLeft)

        self.headerLayout.addWidget(self.filterBtn1)

        self.filterBtn2 = QPushButton(Header)
        self.filterBtn2.setObjectName(u"filterBtn2")
        self.filterBtn2.setMinimumSize(QSize(0, 44))
        self.filterBtn2.setLayoutDirection(Qt.RightToLeft)

        self.headerLayout.addWidget(self.filterBtn2)

        self.settingsBtn = QPushButton(Header)
        self.settingsBtn.setObjectName(u"settingsBtn")
        self.settingsBtn.setMinimumSize(QSize(44, 44))
        self.settingsBtn.setMaximumSize(QSize(44, 44))

        self.headerLayout.addWidget(self.settingsBtn)


        self.retranslateUi(Header)

        QMetaObject.connectSlotsByName(Header)
    # setupUi

    def retranslateUi(self, Header):
        self.pageTitle.setText(QCoreApplication.translate("Header", u"CHECK BOX", None))
        self.pageTitle.setProperty(u"role", QCoreApplication.translate("Header", u"pageTitle", None))
        self.filterBtn0.setText(QCoreApplication.translate("Header", u"Date: Now", None))
        self.filterBtn0.setProperty(u"role", QCoreApplication.translate("Header", u"filterPill", None))
        self.filterBtn1.setText(QCoreApplication.translate("Header", u"Product: All", None))
        self.filterBtn1.setProperty(u"role", QCoreApplication.translate("Header", u"filterPill", None))
        self.filterBtn2.setText(QCoreApplication.translate("Header", u"Profile: Bogdan", None))
        self.filterBtn2.setProperty(u"role", QCoreApplication.translate("Header", u"filterPill", None))
        self.settingsBtn.setText("")
        self.settingsBtn.setProperty(u"role", QCoreApplication.translate("Header", u"iconPill", None))
        pass
    # retranslateUi

