# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_AnalyticsComponent.ui'
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
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomCharts.QCustomLineChart import QCustomLineChart
from Custom_Widgets.QCustomCharts.QCustomPieChart import QCustomPieChart
from Custom_Widgets.QCustomComponent import QCustomComponent
class Ui_AnalyticsComponent(object):
    def setupUi(self, AnalyticsComponent):
        if not AnalyticsComponent.objectName():
            AnalyticsComponent.setObjectName(u"AnalyticsComponent")
        AnalyticsComponent.resize(940, 680)
        self.analyticsRoot = QVBoxLayout(AnalyticsComponent)
        self.analyticsRoot.setSpacing(14)
        self.analyticsRoot.setObjectName(u"analyticsRoot")
        self.analyticsRoot.setContentsMargins(24, 24, 24, 24)
        self.analyticsHeader = QVBoxLayout()
        self.analyticsHeader.setSpacing(2)
        self.analyticsHeader.setObjectName(u"analyticsHeader")
        self.analyticsKicker = QLabel(AnalyticsComponent)
        self.analyticsKicker.setObjectName(u"analyticsKicker")

        self.analyticsHeader.addWidget(self.analyticsKicker)

        self.analyticsTitle = QLabel(AnalyticsComponent)
        self.analyticsTitle.setObjectName(u"analyticsTitle")

        self.analyticsHeader.addWidget(self.analyticsTitle)

        self.analyticsSub = QLabel(AnalyticsComponent)
        self.analyticsSub.setObjectName(u"analyticsSub")

        self.analyticsHeader.addWidget(self.analyticsSub)


        self.analyticsRoot.addLayout(self.analyticsHeader)

        self.chartsRow = QHBoxLayout()
        self.chartsRow.setSpacing(14)
        self.chartsRow.setObjectName(u"chartsRow")
        self.kpPanel = QFrame(AnalyticsComponent)
        self.kpPanel.setObjectName(u"kpPanel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.kpPanel.sizePolicy().hasHeightForWidth())
        self.kpPanel.setSizePolicy(sizePolicy)
        self.kpPanelLayout = QVBoxLayout(self.kpPanel)
        self.kpPanelLayout.setSpacing(10)
        self.kpPanelLayout.setObjectName(u"kpPanelLayout")
        self.kpPanelLayout.setContentsMargins(18, 16, 18, 16)
        self.kpChartLabel = QLabel(self.kpPanel)
        self.kpChartLabel.setObjectName(u"kpChartLabel")

        self.kpPanelLayout.addWidget(self.kpChartLabel)

        self.kpChart = QCustomLineChart(self.kpPanel)
        self.kpChart.setObjectName(u"kpChart")
        self.kpChart.setMinimumSize(QSize(0, 240))

        self.kpPanelLayout.addWidget(self.kpChart)


        self.chartsRow.addWidget(self.kpPanel)

        self.regionPanel = QFrame(AnalyticsComponent)
        self.regionPanel.setObjectName(u"regionPanel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.regionPanel.sizePolicy().hasHeightForWidth())
        self.regionPanel.setSizePolicy(sizePolicy1)
        self.regionPanelLayout = QVBoxLayout(self.regionPanel)
        self.regionPanelLayout.setSpacing(10)
        self.regionPanelLayout.setObjectName(u"regionPanelLayout")
        self.regionPanelLayout.setContentsMargins(18, 16, 18, 16)
        self.regionChartLabel = QLabel(self.regionPanel)
        self.regionChartLabel.setObjectName(u"regionChartLabel")

        self.regionPanelLayout.addWidget(self.regionChartLabel)

        self.regionPie = QCustomPieChart(self.regionPanel)
        self.regionPie.setObjectName(u"regionPie")
        self.regionPie.setMinimumSize(QSize(0, 240))

        self.regionPanelLayout.addWidget(self.regionPie)


        self.chartsRow.addWidget(self.regionPanel)


        self.analyticsRoot.addLayout(self.chartsRow)


        self.retranslateUi(AnalyticsComponent)

        QMetaObject.connectSlotsByName(AnalyticsComponent)
    # setupUi

    def retranslateUi(self, AnalyticsComponent):
        self.analyticsKicker.setProperty(u"role", QCoreApplication.translate("AnalyticsComponent", u"kicker", None))
        self.analyticsKicker.setText(QCoreApplication.translate("AnalyticsComponent", u"SIGNALS", None))
        self.analyticsTitle.setProperty(u"role", QCoreApplication.translate("AnalyticsComponent", u"h1", None))
        self.analyticsTitle.setText(QCoreApplication.translate("AnalyticsComponent", u"Analytics", None))
        self.analyticsSub.setProperty(u"role", QCoreApplication.translate("AnalyticsComponent", u"muted", None))
        self.analyticsSub.setText(QCoreApplication.translate("AnalyticsComponent", u"Kp trend and station distribution.", None))
        self.kpPanel.setProperty(u"role", QCoreApplication.translate("AnalyticsComponent", u"panel", None))
        self.kpChartLabel.setProperty(u"role", QCoreApplication.translate("AnalyticsComponent", u"kicker", None))
        self.kpChartLabel.setText(QCoreApplication.translate("AnalyticsComponent", u"KP TREND", None))
        self.regionPanel.setProperty(u"role", QCoreApplication.translate("AnalyticsComponent", u"panel", None))
        self.regionChartLabel.setProperty(u"role", QCoreApplication.translate("AnalyticsComponent", u"kicker", None))
        self.regionChartLabel.setText(QCoreApplication.translate("AnalyticsComponent", u"BY REGION", None))
        pass
    # retranslateUi

