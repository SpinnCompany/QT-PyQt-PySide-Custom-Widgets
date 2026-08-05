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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomAccordion import QCustomAccordion
from Custom_Widgets.QCustomAlert import QCustomAlert
from Custom_Widgets.QCustomBadge import QCustomBadge
from Custom_Widgets.QCustomCard import QCustomCard
from Custom_Widgets.QCustomCheckBox import QCustomCheckBox
from Custom_Widgets.QCustomForm import QCustomForm
from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider
from Custom_Widgets.QCustomRating import QCustomRating
from Custom_Widgets.QCustomStatCard import QCustomStatCard
from Custom_Widgets.QCustomSwitch import QCustomSwitch
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(12)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(20, 20, 20, 20)
        self.headerTitle = QLabel(self.centralwidget)
        self.headerTitle.setObjectName(u"headerTitle")

        self.rootLayout.addWidget(self.headerTitle)

        self.themeBar = QHBoxLayout()
        self.themeBar.setSpacing(10)
        self.themeBar.setObjectName(u"themeBar")
        self.themeLabel = QLabel(self.centralwidget)
        self.themeLabel.setObjectName(u"themeLabel")

        self.themeBar.addWidget(self.themeLabel)

        self.themeGroupHost = QWidget(self.centralwidget)
        self.themeGroupHost.setObjectName(u"themeGroupHost")
        self.themeGroupHostLayout = QHBoxLayout(self.themeGroupHost)
        self.themeGroupHostLayout.setObjectName(u"themeGroupHostLayout")
        self.themeGroupHostLayout.setContentsMargins(0, 0, 0, 0)

        self.themeBar.addWidget(self.themeGroupHost)

        self.themeSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.themeBar.addItem(self.themeSpacer)


        self.rootLayout.addLayout(self.themeBar)

        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.setObjectName(u"tabs")
        self.inputsTab = QWidget()
        self.inputsTab.setObjectName(u"inputsTab")
        self.inputsTabLayout = QVBoxLayout(self.inputsTab)
        self.inputsTabLayout.setObjectName(u"inputsTabLayout")
        self.inputsTabLayout.setContentsMargins(0, 0, 0, 0)
        self.inputsScroll = QScrollArea(self.inputsTab)
        self.inputsScroll.setObjectName(u"inputsScroll")
        self.inputsScroll.setWidgetResizable(True)
        self.inputsScroll.setFrameShape(QFrame.NoFrame)
        self.inputsContent = QWidget()
        self.inputsContent.setObjectName(u"inputsContent")
        self.inputsContent.setGeometry(QRect(0, 0, 1100, 640))
        self.inputsLayout = QVBoxLayout(self.inputsContent)
        self.inputsLayout.setSpacing(16)
        self.inputsLayout.setObjectName(u"inputsLayout")
        self.inputsLayout.setContentsMargins(12, 12, 12, 12)
        self.formsSectionLabel = QLabel(self.inputsContent)
        self.formsSectionLabel.setObjectName(u"formsSectionLabel")

        self.inputsLayout.addWidget(self.formsSectionLabel)

        self.formCard = QFrame(self.inputsContent)
        self.formCard.setObjectName(u"formCard")
        self.formCard.setFrameShape(QFrame.StyledPanel)
        self.formCardLayout = QVBoxLayout(self.formCard)
        self.formCardLayout.setObjectName(u"formCardLayout")
        self.showcaseForm = QCustomForm(self.formCard)
        self.showcaseForm.setObjectName(u"showcaseForm")

        self.formCardLayout.addWidget(self.showcaseForm)


        self.inputsLayout.addWidget(self.formCard)

        self.groupSectionLabel = QLabel(self.inputsContent)
        self.groupSectionLabel.setObjectName(u"groupSectionLabel")

        self.inputsLayout.addWidget(self.groupSectionLabel)

        self.prefGroupHost = QWidget(self.inputsContent)
        self.prefGroupHost.setObjectName(u"prefGroupHost")
        self.prefGroupHostLayout = QHBoxLayout(self.prefGroupHost)
        self.prefGroupHostLayout.setObjectName(u"prefGroupHostLayout")
        self.prefGroupHostLayout.setContentsMargins(0, 0, 0, 0)

        self.inputsLayout.addWidget(self.prefGroupHost)

        self.agreeCheck = QCustomCheckBox(self.inputsContent)
        self.agreeCheck.setObjectName(u"agreeCheck")
        self.agreeCheck.setChecked(True)

        self.inputsLayout.addWidget(self.agreeCheck)

        self.rangeSectionLabel = QLabel(self.inputsContent)
        self.rangeSectionLabel.setObjectName(u"rangeSectionLabel")

        self.inputsLayout.addWidget(self.rangeSectionLabel)

        self.rangeSlider = QCustomRangeSlider(self.inputsContent)
        self.rangeSlider.setObjectName(u"rangeSlider")
        self.rangeSlider.setMinimumSize(QSize(0, 32))
        self.rangeSlider.setProperty(u"minimum", 0)
        self.rangeSlider.setProperty(u"maximum", 100)
        self.rangeSlider.setProperty(u"lowerValue", 20)
        self.rangeSlider.setProperty(u"upperValue", 80)

        self.inputsLayout.addWidget(self.rangeSlider)

        self.switchSectionLabel = QLabel(self.inputsContent)
        self.switchSectionLabel.setObjectName(u"switchSectionLabel")

        self.inputsLayout.addWidget(self.switchSectionLabel)

        self.notifySwitch = QCustomSwitch(self.inputsContent)
        self.notifySwitch.setObjectName(u"notifySwitch")
        self.notifySwitch.setProperty(u"checked", True)

        self.inputsLayout.addWidget(self.notifySwitch, 0, Qt.AlignLeft)

        self.inputsSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.inputsLayout.addItem(self.inputsSpacer)

        self.inputsScroll.setWidget(self.inputsContent)

        self.inputsTabLayout.addWidget(self.inputsScroll)

        self.tabs.addTab(self.inputsTab, "")
        self.dataTab = QWidget()
        self.dataTab.setObjectName(u"dataTab")
        self.dataTabLayout = QVBoxLayout(self.dataTab)
        self.dataTabLayout.setObjectName(u"dataTabLayout")
        self.dataTabLayout.setContentsMargins(0, 0, 0, 0)
        self.dataScroll = QScrollArea(self.dataTab)
        self.dataScroll.setObjectName(u"dataScroll")
        self.dataScroll.setWidgetResizable(True)
        self.dataScroll.setFrameShape(QFrame.NoFrame)
        self.dataContent = QWidget()
        self.dataContent.setObjectName(u"dataContent")
        self.dataContent.setGeometry(QRect(0, 0, 1100, 640))
        self.dataLayout = QVBoxLayout(self.dataContent)
        self.dataLayout.setSpacing(16)
        self.dataLayout.setObjectName(u"dataLayout")
        self.dataLayout.setContentsMargins(12, 12, 12, 12)
        self.kpiSectionLabel = QLabel(self.dataContent)
        self.kpiSectionLabel.setObjectName(u"kpiSectionLabel")

        self.dataLayout.addWidget(self.kpiSectionLabel)

        self.kpiRow = QHBoxLayout()
        self.kpiRow.setSpacing(12)
        self.kpiRow.setObjectName(u"kpiRow")
        self.statRevenue = QCustomStatCard(self.dataContent)
        self.statRevenue.setObjectName(u"statRevenue")

        self.kpiRow.addWidget(self.statRevenue)

        self.statUsers = QCustomStatCard(self.dataContent)
        self.statUsers.setObjectName(u"statUsers")

        self.kpiRow.addWidget(self.statUsers)

        self.statRetention = QCustomStatCard(self.dataContent)
        self.statRetention.setObjectName(u"statRetention")

        self.kpiRow.addWidget(self.statRetention)


        self.dataLayout.addLayout(self.kpiRow)

        self.progressSectionLabel = QLabel(self.dataContent)
        self.progressSectionLabel.setObjectName(u"progressSectionLabel")

        self.dataLayout.addWidget(self.progressSectionLabel)

        self.progressRow = QHBoxLayout()
        self.progressRow.setSpacing(20)
        self.progressRow.setObjectName(u"progressRow")
        self.cpuColumn = QVBoxLayout()
        self.cpuColumn.setObjectName(u"cpuColumn")
        self.ringCpu = QCustomProgressRing(self.dataContent)
        self.ringCpu.setObjectName(u"ringCpu")
        self.ringCpu.setMinimumSize(QSize(96, 96))

        self.cpuColumn.addWidget(self.ringCpu, 0, Qt.AlignHCenter)

        self.cpuLabel = QLabel(self.dataContent)
        self.cpuLabel.setObjectName(u"cpuLabel")

        self.cpuColumn.addWidget(self.cpuLabel, 0, Qt.AlignHCenter)


        self.progressRow.addLayout(self.cpuColumn)

        self.memoryColumn = QVBoxLayout()
        self.memoryColumn.setObjectName(u"memoryColumn")
        self.ringMemory = QCustomProgressRing(self.dataContent)
        self.ringMemory.setObjectName(u"ringMemory")
        self.ringMemory.setMinimumSize(QSize(96, 96))

        self.memoryColumn.addWidget(self.ringMemory, 0, Qt.AlignHCenter)

        self.memoryLabel = QLabel(self.dataContent)
        self.memoryLabel.setObjectName(u"memoryLabel")

        self.memoryColumn.addWidget(self.memoryLabel, 0, Qt.AlignHCenter)


        self.progressRow.addLayout(self.memoryColumn)

        self.diskColumn = QVBoxLayout()
        self.diskColumn.setObjectName(u"diskColumn")
        self.ringDisk = QCustomProgressRing(self.dataContent)
        self.ringDisk.setObjectName(u"ringDisk")
        self.ringDisk.setMinimumSize(QSize(96, 96))

        self.diskColumn.addWidget(self.ringDisk, 0, Qt.AlignHCenter)

        self.diskLabel = QLabel(self.dataContent)
        self.diskLabel.setObjectName(u"diskLabel")

        self.diskColumn.addWidget(self.diskLabel, 0, Qt.AlignHCenter)


        self.progressRow.addLayout(self.diskColumn)

        self.progressSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.progressRow.addItem(self.progressSpacer)


        self.dataLayout.addLayout(self.progressRow)

        self.ratingSectionLabel = QLabel(self.dataContent)
        self.ratingSectionLabel.setObjectName(u"ratingSectionLabel")

        self.dataLayout.addWidget(self.ratingSectionLabel)

        self.userRating = QCustomRating(self.dataContent)
        self.userRating.setObjectName(u"userRating")
        self.userRating.setProperty(u"maximum", 5)
        self.userRating.setProperty(u"value", 4)

        self.dataLayout.addWidget(self.userRating, 0, Qt.AlignLeft)

        self.badgeSectionLabel = QLabel(self.dataContent)
        self.badgeSectionLabel.setObjectName(u"badgeSectionLabel")

        self.dataLayout.addWidget(self.badgeSectionLabel)

        self.badgeRow = QHBoxLayout()
        self.badgeRow.setSpacing(8)
        self.badgeRow.setObjectName(u"badgeRow")
        self.badgeActive = QCustomBadge(self.dataContent)
        self.badgeActive.setObjectName(u"badgeActive")

        self.badgeRow.addWidget(self.badgeActive)

        self.badgeApproved = QCustomBadge(self.dataContent)
        self.badgeApproved.setObjectName(u"badgeApproved")

        self.badgeRow.addWidget(self.badgeApproved)

        self.badgePending = QCustomBadge(self.dataContent)
        self.badgePending.setObjectName(u"badgePending")

        self.badgeRow.addWidget(self.badgePending)

        self.badgeFailed = QCustomBadge(self.dataContent)
        self.badgeFailed.setObjectName(u"badgeFailed")

        self.badgeRow.addWidget(self.badgeFailed)

        self.badgeSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.badgeRow.addItem(self.badgeSpacer)


        self.dataLayout.addLayout(self.badgeRow)

        self.dataSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.dataLayout.addItem(self.dataSpacer)

        self.dataScroll.setWidget(self.dataContent)

        self.dataTabLayout.addWidget(self.dataScroll)

        self.tabs.addTab(self.dataTab, "")
        self.feedbackTab = QWidget()
        self.feedbackTab.setObjectName(u"feedbackTab")
        self.feedbackTabLayout = QVBoxLayout(self.feedbackTab)
        self.feedbackTabLayout.setObjectName(u"feedbackTabLayout")
        self.feedbackTabLayout.setContentsMargins(0, 0, 0, 0)
        self.feedbackScroll = QScrollArea(self.feedbackTab)
        self.feedbackScroll.setObjectName(u"feedbackScroll")
        self.feedbackScroll.setWidgetResizable(True)
        self.feedbackScroll.setFrameShape(QFrame.NoFrame)
        self.feedbackContent = QWidget()
        self.feedbackContent.setObjectName(u"feedbackContent")
        self.feedbackContent.setGeometry(QRect(0, 0, 1100, 640))
        self.feedbackLayout = QVBoxLayout(self.feedbackContent)
        self.feedbackLayout.setSpacing(16)
        self.feedbackLayout.setObjectName(u"feedbackLayout")
        self.feedbackLayout.setContentsMargins(12, 12, 12, 12)
        self.alertsSectionLabel = QLabel(self.feedbackContent)
        self.alertsSectionLabel.setObjectName(u"alertsSectionLabel")

        self.feedbackLayout.addWidget(self.alertsSectionLabel)

        self.alertInfo = QCustomAlert(self.feedbackContent)
        self.alertInfo.setObjectName(u"alertInfo")

        self.feedbackLayout.addWidget(self.alertInfo)

        self.alertSuccess = QCustomAlert(self.feedbackContent)
        self.alertSuccess.setObjectName(u"alertSuccess")

        self.feedbackLayout.addWidget(self.alertSuccess)

        self.alertWarning = QCustomAlert(self.feedbackContent)
        self.alertWarning.setObjectName(u"alertWarning")

        self.feedbackLayout.addWidget(self.alertWarning)

        self.alertError = QCustomAlert(self.feedbackContent)
        self.alertError.setObjectName(u"alertError")

        self.feedbackLayout.addWidget(self.alertError)

        self.toastSectionLabel = QLabel(self.feedbackContent)
        self.toastSectionLabel.setObjectName(u"toastSectionLabel")

        self.feedbackLayout.addWidget(self.toastSectionLabel)

        self.toastRow = QHBoxLayout()
        self.toastRow.setSpacing(10)
        self.toastRow.setObjectName(u"toastRow")
        self.toastInfoBtn = QCustomQPushButton(self.feedbackContent)
        self.toastInfoBtn.setObjectName(u"toastInfoBtn")

        self.toastRow.addWidget(self.toastInfoBtn)

        self.toastSuccessBtn = QCustomQPushButton(self.feedbackContent)
        self.toastSuccessBtn.setObjectName(u"toastSuccessBtn")

        self.toastRow.addWidget(self.toastSuccessBtn)

        self.toastWarningBtn = QCustomQPushButton(self.feedbackContent)
        self.toastWarningBtn.setObjectName(u"toastWarningBtn")

        self.toastRow.addWidget(self.toastWarningBtn)

        self.toastErrorBtn = QCustomQPushButton(self.feedbackContent)
        self.toastErrorBtn.setObjectName(u"toastErrorBtn")

        self.toastRow.addWidget(self.toastErrorBtn)

        self.toastSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toastRow.addItem(self.toastSpacer)


        self.feedbackLayout.addLayout(self.toastRow)

        self.feedbackSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.feedbackLayout.addItem(self.feedbackSpacer)

        self.feedbackScroll.setWidget(self.feedbackContent)

        self.feedbackTabLayout.addWidget(self.feedbackScroll)

        self.tabs.addTab(self.feedbackTab, "")
        self.advancedTab = QWidget()
        self.advancedTab.setObjectName(u"advancedTab")
        self.advancedTabLayout = QVBoxLayout(self.advancedTab)
        self.advancedTabLayout.setObjectName(u"advancedTabLayout")
        self.advancedTabLayout.setContentsMargins(0, 0, 0, 0)
        self.advancedScroll = QScrollArea(self.advancedTab)
        self.advancedScroll.setObjectName(u"advancedScroll")
        self.advancedScroll.setWidgetResizable(True)
        self.advancedScroll.setFrameShape(QFrame.NoFrame)
        self.advancedContent = QWidget()
        self.advancedContent.setObjectName(u"advancedContent")
        self.advancedContent.setGeometry(QRect(0, 0, 1100, 640))
        self.advancedLayout = QVBoxLayout(self.advancedContent)
        self.advancedLayout.setSpacing(16)
        self.advancedLayout.setObjectName(u"advancedLayout")
        self.advancedLayout.setContentsMargins(12, 12, 12, 12)
        self.cardSectionLabel = QLabel(self.advancedContent)
        self.cardSectionLabel.setObjectName(u"cardSectionLabel")

        self.advancedLayout.addWidget(self.cardSectionLabel)

        self.featureCard = QCustomCard(self.advancedContent)
        self.featureCard.setObjectName(u"featureCard")

        self.advancedLayout.addWidget(self.featureCard)

        self.cardContentHolder = QWidget(self.advancedContent)
        self.cardContentHolder.setObjectName(u"cardContentHolder")
        self.cardContentLayout = QVBoxLayout(self.cardContentHolder)
        self.cardContentLayout.setObjectName(u"cardContentLayout")
        self.cardContentLayout.setContentsMargins(0, 0, 0, 0)
        self.cardDescLabel = QLabel(self.cardContentHolder)
        self.cardDescLabel.setObjectName(u"cardDescLabel")
        self.cardDescLabel.setWordWrap(True)

        self.cardContentLayout.addWidget(self.cardDescLabel)


        self.advancedLayout.addWidget(self.cardContentHolder)

        self.accordionSectionLabel = QLabel(self.advancedContent)
        self.accordionSectionLabel.setObjectName(u"accordionSectionLabel")

        self.advancedLayout.addWidget(self.accordionSectionLabel)

        self.accordion = QCustomAccordion(self.advancedContent)
        self.accordion.setObjectName(u"accordion")

        self.advancedLayout.addWidget(self.accordion)

        self.advancedSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.advancedLayout.addItem(self.advancedSpacer)

        self.advancedScroll.setWidget(self.advancedContent)

        self.advancedTabLayout.addWidget(self.advancedScroll)

        self.tabs.addTab(self.advancedTab, "")

        self.rootLayout.addWidget(self.tabs)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Custom Widgets Showcase \u2014 Complete Library", None))
        self.headerTitle.setText(QCoreApplication.translate("MainWindow", u"Custom Widgets \u2014 Complete Release Showcase", None))
        self.themeLabel.setText(QCoreApplication.translate("MainWindow", u"Theme:", None))
        self.formsSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Forms & Validation", None))
        self.groupSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Selection Buttons", None))
        self.agreeCheck.setText(QCoreApplication.translate("MainWindow", u"I agree to the terms", None))
        self.rangeSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Range Selector", None))
        self.switchSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Toggles", None))
        self.tabs.setTabText(self.tabs.indexOf(self.inputsTab), QCoreApplication.translate("MainWindow", u"Inputs && Forms", None))
        self.kpiSectionLabel.setText(QCoreApplication.translate("MainWindow", u"KPI Statistics", None))
        self.statRevenue.setProperty(u"label", QCoreApplication.translate("MainWindow", u"Revenue", None))
        self.statRevenue.setProperty(u"value", QCoreApplication.translate("MainWindow", u"$12.5K", None))
        self.statUsers.setProperty(u"label", QCoreApplication.translate("MainWindow", u"Users", None))
        self.statUsers.setProperty(u"value", QCoreApplication.translate("MainWindow", u"1,234", None))
        self.statRetention.setProperty(u"label", QCoreApplication.translate("MainWindow", u"Retention", None))
        self.statRetention.setProperty(u"value", QCoreApplication.translate("MainWindow", u"92%", None))
        self.progressSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Progress Indicators", None))
        self.cpuLabel.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.memoryLabel.setText(QCoreApplication.translate("MainWindow", u"Memory", None))
        self.diskLabel.setText(QCoreApplication.translate("MainWindow", u"Disk", None))
        self.ratingSectionLabel.setText(QCoreApplication.translate("MainWindow", u"User Rating", None))
        self.badgeSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Status Indicators", None))
        self.badgeActive.setText(QCoreApplication.translate("MainWindow", u"Active", None))
        self.badgeActive.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
        self.badgeApproved.setText(QCoreApplication.translate("MainWindow", u"Approved", None))
        self.badgeApproved.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"success", None))
        self.badgePending.setText(QCoreApplication.translate("MainWindow", u"Pending", None))
        self.badgePending.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"warning", None))
        self.badgeFailed.setText(QCoreApplication.translate("MainWindow", u"Failed", None))
        self.badgeFailed.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"destructive", None))
        self.tabs.setTabText(self.tabs.indexOf(self.dataTab), QCoreApplication.translate("MainWindow", u"Data && Visualization", None))
        self.alertsSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Alert Messages", None))
        self.alertInfo.setProperty(u"title", QCoreApplication.translate("MainWindow", u"Information", None))
        self.alertInfo.setProperty(u"text", QCoreApplication.translate("MainWindow", u"This is an informational alert.", None))
        self.alertInfo.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"info", None))
        self.alertSuccess.setProperty(u"title", QCoreApplication.translate("MainWindow", u"Success", None))
        self.alertSuccess.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Operation completed successfully.", None))
        self.alertSuccess.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"success", None))
        self.alertWarning.setProperty(u"title", QCoreApplication.translate("MainWindow", u"Warning", None))
        self.alertWarning.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Please review this warning carefully.", None))
        self.alertWarning.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"warning", None))
        self.alertError.setProperty(u"title", QCoreApplication.translate("MainWindow", u"Error", None))
        self.alertError.setProperty(u"text", QCoreApplication.translate("MainWindow", u"An error has occurred.", None))
        self.alertError.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"destructive", None))
        self.toastSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Notifications (Toast)", None))
        self.toastInfoBtn.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.toastInfoBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.toastInfoBtn.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.toastSuccessBtn.setText(QCoreApplication.translate("MainWindow", u"Success", None))
        self.toastSuccessBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.toastSuccessBtn.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.toastWarningBtn.setText(QCoreApplication.translate("MainWindow", u"Warning", None))
        self.toastWarningBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.toastWarningBtn.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.toastErrorBtn.setText(QCoreApplication.translate("MainWindow", u"Error", None))
        self.toastErrorBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.toastErrorBtn.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.tabs.setTabText(self.tabs.indexOf(self.feedbackTab), QCoreApplication.translate("MainWindow", u"Feedback && Status", None))
        self.cardSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Card Containers", None))
        self.featureCard.setProperty(u"title", QCoreApplication.translate("MainWindow", u"Feature Card", None))
        self.featureCard.setProperty(u"subtitle", QCoreApplication.translate("MainWindow", u"Reusable content container", None))
        self.cardDescLabel.setText(QCoreApplication.translate("MainWindow", u"This demonstrates the QCustomCard container with nested content.", None))
        self.accordionSectionLabel.setText(QCoreApplication.translate("MainWindow", u"Collapsible Content", None))
        self.tabs.setTabText(self.tabs.indexOf(self.advancedTab), QCoreApplication.translate("MainWindow", u"Advanced Components", None))
    # retranslateUi

