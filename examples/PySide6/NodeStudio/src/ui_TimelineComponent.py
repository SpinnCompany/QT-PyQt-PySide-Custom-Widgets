# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_TimelineComponent.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomMediaTimeline import QCustomMediaTimeline
class Ui_TimelineComponent(object):
    def setupUi(self, TimelineComponent):
        if not TimelineComponent.objectName():
            TimelineComponent.setObjectName(u"TimelineComponent")
        TimelineComponent.resize(380, 190)
        self.timelineOuter = QVBoxLayout(TimelineComponent)
        self.timelineOuter.setSpacing(0)
        self.timelineOuter.setObjectName(u"timelineOuter")
        self.timelineOuter.setContentsMargins(0, 0, 0, 0)
        self.timelineFrame = QFrame(TimelineComponent)
        self.timelineFrame.setObjectName(u"timelineFrame")
        self.timelineFrame.setFrameShape(QFrame.StyledPanel)
        self.timelineLayout = QVBoxLayout(self.timelineFrame)
        self.timelineLayout.setSpacing(0)
        self.timelineLayout.setObjectName(u"timelineLayout")
        self.timelineLayout.setContentsMargins(10, 10, 10, 10)
        self.mediaTimeline = QCustomMediaTimeline(self.timelineFrame)
        self.mediaTimeline.setObjectName(u"mediaTimeline")

        self.timelineLayout.addWidget(self.mediaTimeline)


        self.timelineOuter.addWidget(self.timelineFrame)


        self.retranslateUi(TimelineComponent)

        QMetaObject.connectSlotsByName(TimelineComponent)
    # setupUi

    def retranslateUi(self, TimelineComponent):
        pass
    # retranslateUi

