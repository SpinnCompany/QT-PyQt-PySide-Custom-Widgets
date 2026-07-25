# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_ThoughtsComponent.ui'
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

from Custom_Widgets.QCustomCodeEditor import QCustomCodeEditor
from Custom_Widgets.QCustomComponent import QCustomComponent
class Ui_ThoughtsComponent(object):
    def setupUi(self, ThoughtsComponent):
        if not ThoughtsComponent.objectName():
            ThoughtsComponent.setObjectName(u"ThoughtsComponent")
        ThoughtsComponent.resize(640, 220)
        self.thoughtsOuter = QVBoxLayout(ThoughtsComponent)
        self.thoughtsOuter.setSpacing(0)
        self.thoughtsOuter.setObjectName(u"thoughtsOuter")
        self.thoughtsOuter.setContentsMargins(0, 0, 0, 0)
        self.thoughtsFrame = QFrame(ThoughtsComponent)
        self.thoughtsFrame.setObjectName(u"thoughtsFrame")
        self.thoughtsFrame.setFrameShape(QFrame.StyledPanel)
        self.thoughtsLayout = QVBoxLayout(self.thoughtsFrame)
        self.thoughtsLayout.setSpacing(8)
        self.thoughtsLayout.setObjectName(u"thoughtsLayout")
        self.thoughtsLayout.setContentsMargins(14, 12, 14, 12)
        self.thoughtsHeader = QHBoxLayout()
        self.thoughtsHeader.setObjectName(u"thoughtsHeader")
        self.thoughtsDot = QLabel(self.thoughtsFrame)
        self.thoughtsDot.setObjectName(u"thoughtsDot")
        self.thoughtsDot.setMinimumSize(QSize(18, 18))
        self.thoughtsDot.setMaximumSize(QSize(18, 18))

        self.thoughtsHeader.addWidget(self.thoughtsDot)

        self.thoughtsTitle = QLabel(self.thoughtsFrame)
        self.thoughtsTitle.setObjectName(u"thoughtsTitle")

        self.thoughtsHeader.addWidget(self.thoughtsTitle)

        self.thoughtsSpacer = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.thoughtsHeader.addItem(self.thoughtsSpacer)


        self.thoughtsLayout.addLayout(self.thoughtsHeader)

        self.codeEditor = QCustomCodeEditor(self.thoughtsFrame)
        self.codeEditor.setObjectName(u"codeEditor")

        self.thoughtsLayout.addWidget(self.codeEditor)


        self.thoughtsOuter.addWidget(self.thoughtsFrame)


        self.retranslateUi(ThoughtsComponent)

        QMetaObject.connectSlotsByName(ThoughtsComponent)
    # setupUi

    def retranslateUi(self, ThoughtsComponent):
        self.thoughtsDot.setText("")
        self.thoughtsTitle.setText(QCoreApplication.translate("ThoughtsComponent", u"Thoughts for 15s", None))
        pass
    # retranslateUi

