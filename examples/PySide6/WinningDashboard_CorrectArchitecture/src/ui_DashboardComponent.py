# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_DashboardComponent.ui'
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

from Custom_Widgets.QCustomCharts.QCustomAreaChart import QCustomAreaChart
from Custom_Widgets.QCustomCharts.QCustomBarChart import QCustomBarChart
from Custom_Widgets.QCustomComponent import QCustomComponent
from Custom_Widgets.QCustomDonut import QCustomDonut
class Ui_DashboardComponent(object):
    def setupUi(self, DashboardComponent):
        if not DashboardComponent.objectName():
            DashboardComponent.setObjectName(u"DashboardComponent")
        DashboardComponent.resize(1000, 760)
        self.dashOuter = QVBoxLayout(DashboardComponent)
        self.dashOuter.setSpacing(0)
        self.dashOuter.setObjectName(u"dashOuter")
        self.dashOuter.setContentsMargins(0, 0, 0, 0)
        self.dashScroll = QScrollArea(DashboardComponent)
        self.dashScroll.setObjectName(u"dashScroll")
        self.dashScroll.setWidgetResizable(True)
        self.dashScroll.setFrameShape(QFrame.NoFrame)
        self.dashScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.dashScrollContents = QWidget()
        self.dashScrollContents.setObjectName(u"dashScrollContents")
        self.dashScrollContents.setGeometry(QRect(0, 0, 1000, 860))
        self.dashBody = QVBoxLayout(self.dashScrollContents)
        self.dashBody.setSpacing(18)
        self.dashBody.setObjectName(u"dashBody")
        self.dashBody.setContentsMargins(26, 22, 26, 22)
        self.headerRow = QHBoxLayout()
        self.headerRow.setSpacing(12)
        self.headerRow.setObjectName(u"headerRow")
        self.headerText = QVBoxLayout()
        self.headerText.setSpacing(3)
        self.headerText.setObjectName(u"headerText")
        self.pageTitle = QLabel(self.dashScrollContents)
        self.pageTitle.setObjectName(u"pageTitle")

        self.headerText.addWidget(self.pageTitle)

        self.pageSub = QLabel(self.dashScrollContents)
        self.pageSub.setObjectName(u"pageSub")

        self.headerText.addWidget(self.pageSub)


        self.headerRow.addLayout(self.headerText)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerRow.addItem(self.headerSpacer)

        self.searchChip = QFrame(self.dashScrollContents)
        self.searchChip.setObjectName(u"searchChip")
        self.searchChip.setMinimumSize(QSize(40, 40))
        self.searchChip.setMaximumSize(QSize(40, 40))
        self.searchChip.setFrameShape(QFrame.StyledPanel)
        self.searchChipLayout = QHBoxLayout(self.searchChip)
        self.searchChipLayout.setObjectName(u"searchChipLayout")
        self.searchChipLayout.setContentsMargins(0, 0, 0, 0)
        self.searchIcon = QLabel(self.searchChip)
        self.searchIcon.setObjectName(u"searchIcon")
        self.searchIcon.setAlignment(Qt.AlignCenter)

        self.searchChipLayout.addWidget(self.searchIcon)


        self.headerRow.addWidget(self.searchChip)

        self.bellChip = QFrame(self.dashScrollContents)
        self.bellChip.setObjectName(u"bellChip")
        self.bellChip.setMinimumSize(QSize(40, 40))
        self.bellChip.setMaximumSize(QSize(40, 40))
        self.bellChip.setFrameShape(QFrame.StyledPanel)
        self.bellChipLayout = QHBoxLayout(self.bellChip)
        self.bellChipLayout.setObjectName(u"bellChipLayout")
        self.bellChipLayout.setContentsMargins(0, 0, 0, 0)
        self.bellIcon = QLabel(self.bellChip)
        self.bellIcon.setObjectName(u"bellIcon")
        self.bellIcon.setAlignment(Qt.AlignCenter)

        self.bellChipLayout.addWidget(self.bellIcon)


        self.headerRow.addWidget(self.bellChip)

        self.headerAvatar = QLabel(self.dashScrollContents)
        self.headerAvatar.setObjectName(u"headerAvatar")
        self.headerAvatar.setMinimumSize(QSize(40, 40))
        self.headerAvatar.setMaximumSize(QSize(40, 40))
        self.headerAvatar.setAlignment(Qt.AlignCenter)

        self.headerRow.addWidget(self.headerAvatar)


        self.dashBody.addLayout(self.headerRow)

        self.kpiRow = QFrame(self.dashScrollContents)
        self.kpiRow.setObjectName(u"kpiRow")
        self.kpiRow.setMinimumSize(QSize(0, 128))
        self.kpiRowLayout = QHBoxLayout(self.kpiRow)
        self.kpiRowLayout.setSpacing(16)
        self.kpiRowLayout.setObjectName(u"kpiRowLayout")
        self.kpiRowLayout.setContentsMargins(0, 0, 0, 0)

        self.dashBody.addWidget(self.kpiRow)

        self.midRow = QHBoxLayout()
        self.midRow.setSpacing(16)
        self.midRow.setObjectName(u"midRow")
        self.salesPanel = QFrame(self.dashScrollContents)
        self.salesPanel.setObjectName(u"salesPanel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.salesPanel.sizePolicy().hasHeightForWidth())
        self.salesPanel.setSizePolicy(sizePolicy)
        self.salesPanel.setFrameShape(QFrame.StyledPanel)
        self.salesPanelLayout = QVBoxLayout(self.salesPanel)
        self.salesPanelLayout.setSpacing(12)
        self.salesPanelLayout.setObjectName(u"salesPanelLayout")
        self.salesPanelLayout.setContentsMargins(20, 18, 20, 18)
        self.salesHead = QHBoxLayout()
        self.salesHead.setObjectName(u"salesHead")
        self.salesTitle = QLabel(self.salesPanel)
        self.salesTitle.setObjectName(u"salesTitle")

        self.salesHead.addWidget(self.salesTitle)

        self.salesHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.salesHead.addItem(self.salesHeadSpacer)

        self.salesLegend = QWidget(self.salesPanel)
        self.salesLegend.setObjectName(u"salesLegend")
        self.salesLegendLayout = QHBoxLayout(self.salesLegend)
        self.salesLegendLayout.setSpacing(14)
        self.salesLegendLayout.setObjectName(u"salesLegendLayout")
        self.salesLegendLayout.setContentsMargins(0, 0, 0, 0)

        self.salesHead.addWidget(self.salesLegend)


        self.salesPanelLayout.addLayout(self.salesHead)

        self.salesChart = QCustomBarChart(self.salesPanel)
        self.salesChart.setObjectName(u"salesChart")
        self.salesChart.setMinimumSize(QSize(0, 300))

        self.salesPanelLayout.addWidget(self.salesChart)


        self.midRow.addWidget(self.salesPanel)

        self.distPanel = QFrame(self.dashScrollContents)
        self.distPanel.setObjectName(u"distPanel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.distPanel.sizePolicy().hasHeightForWidth())
        self.distPanel.setSizePolicy(sizePolicy1)
        self.distPanel.setFrameShape(QFrame.StyledPanel)
        self.distPanelLayout = QVBoxLayout(self.distPanel)
        self.distPanelLayout.setSpacing(10)
        self.distPanelLayout.setObjectName(u"distPanelLayout")
        self.distPanelLayout.setContentsMargins(20, 18, 20, 18)
        self.distTitle = QLabel(self.distPanel)
        self.distTitle.setObjectName(u"distTitle")

        self.distPanelLayout.addWidget(self.distTitle)

        self.distChart = QCustomDonut(self.distPanel)
        self.distChart.setObjectName(u"distChart")
        self.distChart.setMinimumSize(QSize(0, 200))

        self.distPanelLayout.addWidget(self.distChart)

        self.distLegend = QWidget(self.distPanel)
        self.distLegend.setObjectName(u"distLegend")
        self.distLegendLayout = QVBoxLayout(self.distLegend)
        self.distLegendLayout.setSpacing(8)
        self.distLegendLayout.setObjectName(u"distLegendLayout")
        self.distLegendLayout.setContentsMargins(2, 4, 2, 0)

        self.distPanelLayout.addWidget(self.distLegend)


        self.midRow.addWidget(self.distPanel)


        self.dashBody.addLayout(self.midRow)

        self.bottomRow = QHBoxLayout()
        self.bottomRow.setSpacing(16)
        self.bottomRow.setObjectName(u"bottomRow")
        self.ordersPanel = QFrame(self.dashScrollContents)
        self.ordersPanel.setObjectName(u"ordersPanel")
        sizePolicy1.setHeightForWidth(self.ordersPanel.sizePolicy().hasHeightForWidth())
        self.ordersPanel.setSizePolicy(sizePolicy1)
        self.ordersPanel.setFrameShape(QFrame.StyledPanel)
        self.ordersPanelLayout = QVBoxLayout(self.ordersPanel)
        self.ordersPanelLayout.setSpacing(10)
        self.ordersPanelLayout.setObjectName(u"ordersPanelLayout")
        self.ordersPanelLayout.setContentsMargins(20, 18, 20, 18)
        self.ordersTitle = QLabel(self.ordersPanel)
        self.ordersTitle.setObjectName(u"ordersTitle")

        self.ordersPanelLayout.addWidget(self.ordersTitle)

        self.ordersHead = QHBoxLayout()
        self.ordersHead.setObjectName(u"ordersHead")
        self.colProduct = QLabel(self.ordersPanel)
        self.colProduct.setObjectName(u"colProduct")

        self.ordersHead.addWidget(self.colProduct)

        self.colDate = QLabel(self.ordersPanel)
        self.colDate.setObjectName(u"colDate")

        self.ordersHead.addWidget(self.colDate)

        self.colPrice = QLabel(self.ordersPanel)
        self.colPrice.setObjectName(u"colPrice")

        self.ordersHead.addWidget(self.colPrice)

        self.colStatus = QLabel(self.ordersPanel)
        self.colStatus.setObjectName(u"colStatus")
        self.colStatus.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.ordersHead.addWidget(self.colStatus)


        self.ordersPanelLayout.addLayout(self.ordersHead)

        self.ordersBody = QWidget(self.ordersPanel)
        self.ordersBody.setObjectName(u"ordersBody")
        self.ordersBodyLayout = QVBoxLayout(self.ordersBody)
        self.ordersBodyLayout.setSpacing(0)
        self.ordersBodyLayout.setObjectName(u"ordersBodyLayout")
        self.ordersBodyLayout.setContentsMargins(0, 0, 0, 0)

        self.ordersPanelLayout.addWidget(self.ordersBody)

        self.ordersSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.ordersPanelLayout.addItem(self.ordersSpacer)


        self.bottomRow.addWidget(self.ordersPanel)

        self.customersPanel = QFrame(self.dashScrollContents)
        self.customersPanel.setObjectName(u"customersPanel")
        sizePolicy1.setHeightForWidth(self.customersPanel.sizePolicy().hasHeightForWidth())
        self.customersPanel.setSizePolicy(sizePolicy1)
        self.customersPanel.setFrameShape(QFrame.StyledPanel)
        self.customersPanelLayout = QVBoxLayout(self.customersPanel)
        self.customersPanelLayout.setSpacing(10)
        self.customersPanelLayout.setObjectName(u"customersPanelLayout")
        self.customersPanelLayout.setContentsMargins(20, 18, 20, 18)
        self.custHead = QHBoxLayout()
        self.custHead.setObjectName(u"custHead")
        self.custTitle = QLabel(self.customersPanel)
        self.custTitle.setObjectName(u"custTitle")

        self.custHead.addWidget(self.custTitle)

        self.custHeadSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.custHead.addItem(self.custHeadSpacer)

        self.custLegend = QWidget(self.customersPanel)
        self.custLegend.setObjectName(u"custLegend")
        self.custLegendLayout = QHBoxLayout(self.custLegend)
        self.custLegendLayout.setSpacing(14)
        self.custLegendLayout.setObjectName(u"custLegendLayout")
        self.custLegendLayout.setContentsMargins(0, 0, 0, 0)

        self.custHead.addWidget(self.custLegend)


        self.customersPanelLayout.addLayout(self.custHead)

        self.customersChart = QCustomAreaChart(self.customersPanel)
        self.customersChart.setObjectName(u"customersChart")
        self.customersChart.setMinimumSize(QSize(0, 210))

        self.customersPanelLayout.addWidget(self.customersChart)

        self.monthRow = QWidget(self.customersPanel)
        self.monthRow.setObjectName(u"monthRow")
        self.monthRowLayout = QHBoxLayout(self.monthRow)
        self.monthRowLayout.setSpacing(0)
        self.monthRowLayout.setObjectName(u"monthRowLayout")
        self.monthRowLayout.setContentsMargins(6, 0, 6, 0)

        self.customersPanelLayout.addWidget(self.monthRow)


        self.bottomRow.addWidget(self.customersPanel)


        self.dashBody.addLayout(self.bottomRow)

        self.dashBottomSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.dashBody.addItem(self.dashBottomSpacer)

        self.dashScroll.setWidget(self.dashScrollContents)

        self.dashOuter.addWidget(self.dashScroll)


        self.retranslateUi(DashboardComponent)

        QMetaObject.connectSlotsByName(DashboardComponent)
    # setupUi

    def retranslateUi(self, DashboardComponent):
        self.pageTitle.setText(QCoreApplication.translate("DashboardComponent", u"Welcome back", None))
        self.pageTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"h1", None))
        self.pageSub.setText(QCoreApplication.translate("DashboardComponent", u"Check your last activity today", None))
        self.pageSub.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"sub", None))
        self.searchChip.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"iconChip", None))
        self.bellChip.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"iconChip", None))
        self.headerAvatar.setText(QCoreApplication.translate("DashboardComponent", u"AK", None))
        self.salesPanel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panel", None))
        self.salesTitle.setText(QCoreApplication.translate("DashboardComponent", u"Total sales", None))
        self.salesTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelTitle", None))
        self.distPanel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panel", None))
        self.distTitle.setText(QCoreApplication.translate("DashboardComponent", u"Sales distribution", None))
        self.distTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelTitle", None))
        self.ordersPanel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panel", None))
        self.ordersTitle.setText(QCoreApplication.translate("DashboardComponent", u"Recent orders", None))
        self.ordersTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelTitle", None))
        self.colProduct.setText(QCoreApplication.translate("DashboardComponent", u"Product name", None))
        self.colProduct.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"colHead", None))
        self.colDate.setText(QCoreApplication.translate("DashboardComponent", u"Date", None))
        self.colDate.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"colHead", None))
        self.colPrice.setText(QCoreApplication.translate("DashboardComponent", u"Price", None))
        self.colPrice.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"colHead", None))
        self.colStatus.setText(QCoreApplication.translate("DashboardComponent", u"Status", None))
        self.colStatus.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"colHead", None))
        self.customersPanel.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panel", None))
        self.custTitle.setText(QCoreApplication.translate("DashboardComponent", u"Customers", None))
        self.custTitle.setProperty(u"role", QCoreApplication.translate("DashboardComponent", u"panelTitle", None))
        pass
    # retranslateUi

