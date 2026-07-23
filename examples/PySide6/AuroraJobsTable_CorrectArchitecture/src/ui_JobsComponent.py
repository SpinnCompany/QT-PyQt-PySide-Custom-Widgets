# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_JobsComponent.ui'
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
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomDataTable import QCustomDataTable
from Custom_Widgets.QCustomTableToolbar import QCustomTableToolbar
class Ui_JobsComponent(object):
    def setupUi(self, JobsComponent):
        if not JobsComponent.objectName():
            JobsComponent.setObjectName(u"JobsComponent")
        JobsComponent.resize(1180, 760)
        self.jobsOuter = QVBoxLayout(JobsComponent)
        self.jobsOuter.setSpacing(0)
        self.jobsOuter.setObjectName(u"jobsOuter")
        self.jobsOuter.setContentsMargins(0, 0, 0, 0)
        self.jobsScroll = QScrollArea(JobsComponent)
        self.jobsScroll.setObjectName(u"jobsScroll")
        self.jobsScroll.setWidgetResizable(True)
        self.jobsScroll.setFrameShape(QFrame.NoFrame)
        self.jobsScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.jobsScrollContents = QWidget()
        self.jobsScrollContents.setObjectName(u"jobsScrollContents")
        self.jobsScrollContents.setGeometry(QRect(0, 0, 1180, 760))
        self.jobsBody = QVBoxLayout(self.jobsScrollContents)
        self.jobsBody.setSpacing(18)
        self.jobsBody.setObjectName(u"jobsBody")
        self.jobsBody.setContentsMargins(28, 22, 28, 24)
        self.titleRow = QHBoxLayout()
        self.titleRow.setSpacing(12)
        self.titleRow.setObjectName(u"titleRow")
        self.pageTitle = QLabel(self.jobsScrollContents)
        self.pageTitle.setObjectName(u"pageTitle")

        self.titleRow.addWidget(self.pageTitle)

        self.titleSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.titleRow.addItem(self.titleSpacer)

        self.addJobBtn = QPushButton(self.jobsScrollContents)
        self.addJobBtn.setObjectName(u"addJobBtn")
        self.addJobBtn.setMinimumSize(QSize(0, 42))
        self.addJobBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addJobBtn.setIconSize(QSize(16, 16))

        self.titleRow.addWidget(self.addJobBtn)


        self.jobsBody.addLayout(self.titleRow)

        self.card = QFrame(self.jobsScrollContents)
        self.card.setObjectName(u"card")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.card.sizePolicy().hasHeightForWidth())
        self.card.setSizePolicy(sizePolicy)
        self.card.setFrameShape(QFrame.StyledPanel)
        self.cardLayout = QVBoxLayout(self.card)
        self.cardLayout.setSpacing(16)
        self.cardLayout.setObjectName(u"cardLayout")
        self.cardLayout.setContentsMargins(20, 20, 20, 16)
        self.tableToolbar = QCustomTableToolbar(self.card)
        self.tableToolbar.setObjectName(u"tableToolbar")

        self.cardLayout.addWidget(self.tableToolbar)

        self.jobsTable = QCustomDataTable(self.card)
        self.jobsTable.setObjectName(u"jobsTable")
        sizePolicy.setHeightForWidth(self.jobsTable.sizePolicy().hasHeightForWidth())
        self.jobsTable.setSizePolicy(sizePolicy)

        self.cardLayout.addWidget(self.jobsTable)


        self.jobsBody.addWidget(self.card)

        self.jobsScroll.setWidget(self.jobsScrollContents)

        self.jobsOuter.addWidget(self.jobsScroll)


        self.retranslateUi(JobsComponent)

        QMetaObject.connectSlotsByName(JobsComponent)
    # setupUi

    def retranslateUi(self, JobsComponent):
        self.pageTitle.setText(QCoreApplication.translate("JobsComponent", u"Jobs", None))
        self.pageTitle.setProperty(u"role", QCoreApplication.translate("JobsComponent", u"h1", None))
        self.addJobBtn.setText(QCoreApplication.translate("JobsComponent", u"  Add job", None))
        self.card.setProperty(u"role", QCoreApplication.translate("JobsComponent", u"card", None))
        pass
    # retranslateUi

