# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_MainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomCard import QCustomCard
from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
from Custom_Widgets.QCustomStatCard import QCustomStatCard
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 420)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(14)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(14, 14, 14, 14)
        self.statsRow = QHBoxLayout()
        self.statsRow.setSpacing(12)
        self.statsRow.setObjectName(u"statsRow")
        self.statRevenue = QCustomStatCard(self.centralwidget)
        self.statRevenue.setObjectName(u"statRevenue")

        self.statsRow.addWidget(self.statRevenue)

        self.statChurn = QCustomStatCard(self.centralwidget)
        self.statChurn.setObjectName(u"statChurn")

        self.statsRow.addWidget(self.statChurn)

        self.statSignups = QCustomStatCard(self.centralwidget)
        self.statSignups.setObjectName(u"statSignups")

        self.statsRow.addWidget(self.statSignups)


        self.rootLayout.addLayout(self.statsRow)

        self.goalsCard = QCustomCard(self.centralwidget)
        self.goalsCard.setObjectName(u"goalsCard")

        self.rootLayout.addWidget(self.goalsCard)

        self.ringsHolder = QWidget(self.centralwidget)
        self.ringsHolder.setObjectName(u"ringsHolder")
        self.ringsLayout = QHBoxLayout(self.ringsHolder)
        self.ringsLayout.setSpacing(20)
        self.ringsLayout.setObjectName(u"ringsLayout")
        self.salesColumn = QVBoxLayout()
        self.salesColumn.setObjectName(u"salesColumn")
        self.ringSales = QCustomProgressRing(self.ringsHolder)
        self.ringSales.setObjectName(u"ringSales")
        self.ringSales.setMinimumSize(QSize(96, 96))

        self.salesColumn.addWidget(self.ringSales, 0, Qt.AlignHCenter)

        self.salesLabel = QLabel(self.ringsHolder)
        self.salesLabel.setObjectName(u"salesLabel")

        self.salesColumn.addWidget(self.salesLabel, 0, Qt.AlignHCenter)


        self.ringsLayout.addLayout(self.salesColumn)

        self.supportColumn = QVBoxLayout()
        self.supportColumn.setObjectName(u"supportColumn")
        self.ringSupport = QCustomProgressRing(self.ringsHolder)
        self.ringSupport.setObjectName(u"ringSupport")
        self.ringSupport.setMinimumSize(QSize(96, 96))

        self.supportColumn.addWidget(self.ringSupport, 0, Qt.AlignHCenter)

        self.supportLabel = QLabel(self.ringsHolder)
        self.supportLabel.setObjectName(u"supportLabel")

        self.supportColumn.addWidget(self.supportLabel, 0, Qt.AlignHCenter)


        self.ringsLayout.addLayout(self.supportColumn)

        self.marketingColumn = QVBoxLayout()
        self.marketingColumn.setObjectName(u"marketingColumn")
        self.ringMarketing = QCustomProgressRing(self.ringsHolder)
        self.ringMarketing.setObjectName(u"ringMarketing")
        self.ringMarketing.setMinimumSize(QSize(96, 96))

        self.marketingColumn.addWidget(self.ringMarketing, 0, Qt.AlignHCenter)

        self.marketingLabel = QLabel(self.ringsHolder)
        self.marketingLabel.setObjectName(u"marketingLabel")

        self.marketingColumn.addWidget(self.marketingLabel, 0, Qt.AlignHCenter)


        self.ringsLayout.addLayout(self.marketingColumn)


        self.rootLayout.addWidget(self.ringsHolder)

        self.bottomSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rootLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Stat cards / Progress rings / Card", None))
        self.statRevenue.setProperty(u"label", QCoreApplication.translate("MainWindow", u"Revenue", None))
        self.statRevenue.setProperty(u"value", QCoreApplication.translate("MainWindow", u"$48.2k", None))
        self.statRevenue.setProperty(u"caption", QCoreApplication.translate("MainWindow", u"vs last mo", None))
        self.statChurn.setProperty(u"label", QCoreApplication.translate("MainWindow", u"Churn", None))
        self.statChurn.setProperty(u"value", QCoreApplication.translate("MainWindow", u"2.1%", None))
        self.statChurn.setProperty(u"caption", QCoreApplication.translate("MainWindow", u"vs last mo", None))
        self.statSignups.setProperty(u"label", QCoreApplication.translate("MainWindow", u"Sign-ups", None))
        self.statSignups.setProperty(u"value", QCoreApplication.translate("MainWindow", u"1,204", None))
        self.statSignups.setProperty(u"caption", QCoreApplication.translate("MainWindow", u"this week", None))
        self.goalsCard.setProperty(u"title", QCoreApplication.translate("MainWindow", u"Quarterly goals", None))
        self.goalsCard.setProperty(u"subtitle", QCoreApplication.translate("MainWindow", u"Progress toward Q3 targets", None))
        self.salesLabel.setText(QCoreApplication.translate("MainWindow", u"Sales", None))
        self.supportLabel.setText(QCoreApplication.translate("MainWindow", u"Support", None))
        self.marketingLabel.setText(QCoreApplication.translate("MainWindow", u"Marketing", None))
    # retranslateUi

