# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_TimelineCard.ui'
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

from Custom_Widgets.QCustomGanttChart import QCustomGanttChart
class Ui_TimelineCard(object):
    def setupUi(self, TimelineCard):
        if not TimelineCard.objectName():
            TimelineCard.setObjectName(u"TimelineCard")
        TimelineCard.resize(520, 560)
        self.tlRoot = QVBoxLayout(TimelineCard)
        self.tlRoot.setSpacing(0)
        self.tlRoot.setObjectName(u"tlRoot")
        self.tlRoot.setContentsMargins(0, 0, 0, 0)
        self.timelineCard = QFrame(TimelineCard)
        self.timelineCard.setObjectName(u"timelineCard")
        self.timelineCard.setFrameShape(QFrame.StyledPanel)
        self.tlLayout = QVBoxLayout(self.timelineCard)
        self.tlLayout.setSpacing(10)
        self.tlLayout.setObjectName(u"tlLayout")
        self.tlLayout.setContentsMargins(20, 18, 20, 18)
        self.tlHeader = QHBoxLayout()
        self.tlHeader.setObjectName(u"tlHeader")
        self.tlTitle = QLabel(self.timelineCard)
        self.tlTitle.setObjectName(u"tlTitle")

        self.tlHeader.addWidget(self.tlTitle)

        self.tlHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.tlHeader.addItem(self.tlHeaderSpacer)

        self.timelineMenu = QPushButton(self.timelineCard)
        self.timelineMenu.setObjectName(u"timelineMenu")
        self.timelineMenu.setMinimumSize(QSize(30, 26))
        self.timelineMenu.setMaximumSize(QSize(30, 26))

        self.tlHeader.addWidget(self.timelineMenu)


        self.tlLayout.addLayout(self.tlHeader)

        self.timeline = QCustomGanttChart(self.timelineCard)
        self.timeline.setObjectName(u"timeline")
        self.timeline.setMinimumSize(QSize(0, 300))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.timeline.sizePolicy().hasHeightForWidth())
        self.timeline.setSizePolicy(sizePolicy)

        self.tlLayout.addWidget(self.timeline)

        self.tlFooter = QHBoxLayout()
        self.tlFooter.setSpacing(18)
        self.tlFooter.setObjectName(u"tlFooter")
        self.timelineLegend = QWidget(self.timelineCard)
        self.timelineLegend.setObjectName(u"timelineLegend")
        self.tlLegendLayout = QHBoxLayout(self.timelineLegend)
        self.tlLegendLayout.setSpacing(18)
        self.tlLegendLayout.setObjectName(u"tlLegendLayout")
        self.tlLegendLayout.setContentsMargins(0, 0, 0, 0)

        self.tlFooter.addWidget(self.timelineLegend)

        self.tlFooterSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.tlFooter.addItem(self.tlFooterSpacer)

        self.timelineTotal = QLabel(self.timelineCard)
        self.timelineTotal.setObjectName(u"timelineTotal")

        self.tlFooter.addWidget(self.timelineTotal)


        self.tlLayout.addLayout(self.tlFooter)


        self.tlRoot.addWidget(self.timelineCard)


        self.retranslateUi(TimelineCard)

        QMetaObject.connectSlotsByName(TimelineCard)
    # setupUi

    def retranslateUi(self, TimelineCard):
        self.timelineCard.setProperty(u"role", QCoreApplication.translate("TimelineCard", u"card", None))
        self.tlTitle.setText(QCoreApplication.translate("TimelineCard", u"PROJECTS TIMELINE", None))
        self.tlTitle.setProperty(u"role", QCoreApplication.translate("TimelineCard", u"cardTitle", None))
        self.timelineMenu.setText("")
        self.timelineMenu.setProperty(u"role", QCoreApplication.translate("TimelineCard", u"menuBtn", None))
        self.timelineTotal.setText(QCoreApplication.translate("TimelineCard", u"Total: 284", None))
        self.timelineTotal.setProperty(u"role", QCoreApplication.translate("TimelineCard", u"total", None))
        pass
    # retranslateUi

