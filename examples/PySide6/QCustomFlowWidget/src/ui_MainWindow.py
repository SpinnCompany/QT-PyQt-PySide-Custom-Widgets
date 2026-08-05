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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHBoxLayout, QLabel, QMainWindow, QPushButton,
    QScrollArea, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QSplitter, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomFlowWidget import QCustomFlowWidget
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1300, 900)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(10)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(10, 10, 10, 10)
        self.mainSplitter = QSplitter(self.centralwidget)
        self.mainSplitter.setObjectName(u"mainSplitter")
        self.mainSplitter.setOrientation(Qt.Vertical)
        self.controlTabs = QTabWidget(self.mainSplitter)
        self.controlTabs.setObjectName(u"controlTabs")
        self.managementTab = QWidget()
        self.managementTab.setObjectName(u"managementTab")
        self.managementLayout = QVBoxLayout(self.managementTab)
        self.managementLayout.setSpacing(10)
        self.managementLayout.setObjectName(u"managementLayout")
        self.typeGroup = QGroupBox(self.managementTab)
        self.typeGroup.setObjectName(u"typeGroup")
        self.typeLayout = QHBoxLayout(self.typeGroup)
        self.typeLayout.setObjectName(u"typeLayout")
        self.typeCaption = QLabel(self.typeGroup)
        self.typeCaption.setObjectName(u"typeCaption")

        self.typeLayout.addWidget(self.typeCaption)

        self.widgetType = QComboBox(self.typeGroup)
        self.widgetType.addItem("")
        self.widgetType.addItem("")
        self.widgetType.addItem("")
        self.widgetType.addItem("")
        self.widgetType.addItem("")
        self.widgetType.addItem("")
        self.widgetType.addItem("")
        self.widgetType.addItem("")
        self.widgetType.setObjectName(u"widgetType")

        self.typeLayout.addWidget(self.widgetType)


        self.managementLayout.addWidget(self.typeGroup)

        self.addGroup = QGroupBox(self.managementTab)
        self.addGroup.setObjectName(u"addGroup")
        self.addLayout = QVBoxLayout(self.addGroup)
        self.addLayout.setObjectName(u"addLayout")
        self.addBtn = QPushButton(self.addGroup)
        self.addBtn.setObjectName(u"addBtn")

        self.addLayout.addWidget(self.addBtn)

        self.batchLayout = QHBoxLayout()
        self.batchLayout.setObjectName(u"batchLayout")
        self.batchCaption = QLabel(self.addGroup)
        self.batchCaption.setObjectName(u"batchCaption")

        self.batchLayout.addWidget(self.batchCaption)

        self.add5Btn = QPushButton(self.addGroup)
        self.add5Btn.setObjectName(u"add5Btn")

        self.batchLayout.addWidget(self.add5Btn)

        self.add10Btn = QPushButton(self.addGroup)
        self.add10Btn.setObjectName(u"add10Btn")

        self.batchLayout.addWidget(self.add10Btn)

        self.add20Btn = QPushButton(self.addGroup)
        self.add20Btn.setObjectName(u"add20Btn")

        self.batchLayout.addWidget(self.add20Btn)

        self.add50Btn = QPushButton(self.addGroup)
        self.add50Btn.setObjectName(u"add50Btn")

        self.batchLayout.addWidget(self.add50Btn)


        self.addLayout.addLayout(self.batchLayout)


        self.managementLayout.addWidget(self.addGroup)

        self.removeGroup = QGroupBox(self.managementTab)
        self.removeGroup.setObjectName(u"removeGroup")
        self.removeLayout = QVBoxLayout(self.removeGroup)
        self.removeLayout.setObjectName(u"removeLayout")
        self.removeLastBtn = QPushButton(self.removeGroup)
        self.removeLastBtn.setObjectName(u"removeLastBtn")

        self.removeLayout.addWidget(self.removeLastBtn)

        self.removeRandomBtn = QPushButton(self.removeGroup)
        self.removeRandomBtn.setObjectName(u"removeRandomBtn")

        self.removeLayout.addWidget(self.removeRandomBtn)

        self.clearAllBtn = QPushButton(self.removeGroup)
        self.clearAllBtn.setObjectName(u"clearAllBtn")

        self.removeLayout.addWidget(self.clearAllBtn)


        self.managementLayout.addWidget(self.removeGroup)

        self.orderGroup = QGroupBox(self.managementTab)
        self.orderGroup.setObjectName(u"orderGroup")
        self.orderLayout = QVBoxLayout(self.orderGroup)
        self.orderLayout.setObjectName(u"orderLayout")
        self.useJsonOrderCheck = QCheckBox(self.orderGroup)
        self.useJsonOrderCheck.setObjectName(u"useJsonOrderCheck")

        self.orderLayout.addWidget(self.useJsonOrderCheck)


        self.managementLayout.addWidget(self.orderGroup)

        self.counterGroup = QGroupBox(self.managementTab)
        self.counterGroup.setObjectName(u"counterGroup")
        self.counterLayout = QVBoxLayout(self.counterGroup)
        self.counterLayout.setObjectName(u"counterLayout")
        self.counterLabel = QLabel(self.counterGroup)
        self.counterLabel.setObjectName(u"counterLabel")
        self.counterLabel.setAlignment(Qt.AlignCenter)

        self.counterLayout.addWidget(self.counterLabel)


        self.managementLayout.addWidget(self.counterGroup)

        self.managementSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.managementLayout.addItem(self.managementSpacer)

        self.controlTabs.addTab(self.managementTab, "")
        self.animationTab = QWidget()
        self.animationTab.setObjectName(u"animationTab")
        self.animationLayout = QVBoxLayout(self.animationTab)
        self.animationLayout.setSpacing(15)
        self.animationLayout.setObjectName(u"animationLayout")
        self.enableGroup = QGroupBox(self.animationTab)
        self.enableGroup.setObjectName(u"enableGroup")
        self.enableLayout = QVBoxLayout(self.enableGroup)
        self.enableLayout.setObjectName(u"enableLayout")
        self.animateCb = QCheckBox(self.enableGroup)
        self.animateCb.setObjectName(u"animateCb")
        self.animateCb.setChecked(True)

        self.enableLayout.addWidget(self.animateCb)


        self.animationLayout.addWidget(self.enableGroup)

        self.durationGroup = QGroupBox(self.animationTab)
        self.durationGroup.setObjectName(u"durationGroup")
        self.durationLayout = QHBoxLayout(self.durationGroup)
        self.durationLayout.setObjectName(u"durationLayout")
        self.durationCaption = QLabel(self.durationGroup)
        self.durationCaption.setObjectName(u"durationCaption")

        self.durationLayout.addWidget(self.durationCaption)

        self.durationSlider = QSlider(self.durationGroup)
        self.durationSlider.setObjectName(u"durationSlider")
        self.durationSlider.setOrientation(Qt.Horizontal)
        self.durationSlider.setMinimum(0)
        self.durationSlider.setMaximum(1000)
        self.durationSlider.setValue(300)

        self.durationLayout.addWidget(self.durationSlider)

        self.durationLabel = QLabel(self.durationGroup)
        self.durationLabel.setObjectName(u"durationLabel")

        self.durationLayout.addWidget(self.durationLabel)


        self.animationLayout.addWidget(self.durationGroup)

        self.easingGroup = QGroupBox(self.animationTab)
        self.easingGroup.setObjectName(u"easingGroup")
        self.easingLayout = QVBoxLayout(self.easingGroup)
        self.easingLayout.setObjectName(u"easingLayout")
        self.easingCombo = QComboBox(self.easingGroup)
        self.easingCombo.setObjectName(u"easingCombo")

        self.easingLayout.addWidget(self.easingCombo)


        self.animationLayout.addWidget(self.easingGroup)

        self.statusGroup = QGroupBox(self.animationTab)
        self.statusGroup.setObjectName(u"statusGroup")
        self.statusLayout = QVBoxLayout(self.statusGroup)
        self.statusLayout.setObjectName(u"statusLayout")
        self.animStatus = QLabel(self.statusGroup)
        self.animStatus.setObjectName(u"animStatus")
        self.animStatus.setAlignment(Qt.AlignCenter)

        self.statusLayout.addWidget(self.animStatus)


        self.animationLayout.addWidget(self.statusGroup)

        self.animationSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.animationLayout.addItem(self.animationSpacer)

        self.controlTabs.addTab(self.animationTab, "")
        self.layoutTab = QWidget()
        self.layoutTab.setObjectName(u"layoutTab")
        self.layoutTabLayout = QVBoxLayout(self.layoutTab)
        self.layoutTabLayout.setSpacing(15)
        self.layoutTabLayout.setObjectName(u"layoutTabLayout")
        self.marginGroup = QGroupBox(self.layoutTab)
        self.marginGroup.setObjectName(u"marginGroup")
        self.marginLayout = QHBoxLayout(self.marginGroup)
        self.marginLayout.setObjectName(u"marginLayout")
        self.marginCaption = QLabel(self.marginGroup)
        self.marginCaption.setObjectName(u"marginCaption")

        self.marginLayout.addWidget(self.marginCaption)

        self.marginSlider = QSlider(self.marginGroup)
        self.marginSlider.setObjectName(u"marginSlider")
        self.marginSlider.setOrientation(Qt.Horizontal)
        self.marginSlider.setMinimum(0)
        self.marginSlider.setMaximum(50)
        self.marginSlider.setValue(15)

        self.marginLayout.addWidget(self.marginSlider)

        self.marginLabel = QLabel(self.marginGroup)
        self.marginLabel.setObjectName(u"marginLabel")

        self.marginLayout.addWidget(self.marginLabel)


        self.layoutTabLayout.addWidget(self.marginGroup)

        self.spacingGroup = QGroupBox(self.layoutTab)
        self.spacingGroup.setObjectName(u"spacingGroup")
        self.spacingLayout = QHBoxLayout(self.spacingGroup)
        self.spacingLayout.setObjectName(u"spacingLayout")
        self.spacingCaption = QLabel(self.spacingGroup)
        self.spacingCaption.setObjectName(u"spacingCaption")

        self.spacingLayout.addWidget(self.spacingCaption)

        self.spacingSlider = QSlider(self.spacingGroup)
        self.spacingSlider.setObjectName(u"spacingSlider")
        self.spacingSlider.setOrientation(Qt.Horizontal)
        self.spacingSlider.setMinimum(0)
        self.spacingSlider.setMaximum(50)
        self.spacingSlider.setValue(15)

        self.spacingLayout.addWidget(self.spacingSlider)

        self.spacingLabel = QLabel(self.spacingGroup)
        self.spacingLabel.setObjectName(u"spacingLabel")

        self.spacingLayout.addWidget(self.spacingLabel)


        self.layoutTabLayout.addWidget(self.spacingGroup)

        self.hvGroup = QGroupBox(self.layoutTab)
        self.hvGroup.setObjectName(u"hvGroup")
        self.hvLayout = QVBoxLayout(self.hvGroup)
        self.hvLayout.setObjectName(u"hvLayout")
        self.hRow = QHBoxLayout()
        self.hRow.setObjectName(u"hRow")
        self.hCaption = QLabel(self.hvGroup)
        self.hCaption.setObjectName(u"hCaption")

        self.hRow.addWidget(self.hCaption)

        self.hSpin = QSpinBox(self.hvGroup)
        self.hSpin.setObjectName(u"hSpin")
        self.hSpin.setMinimum(0)
        self.hSpin.setMaximum(50)
        self.hSpin.setValue(15)

        self.hRow.addWidget(self.hSpin)


        self.hvLayout.addLayout(self.hRow)

        self.vRow = QHBoxLayout()
        self.vRow.setObjectName(u"vRow")
        self.vCaption = QLabel(self.hvGroup)
        self.vCaption.setObjectName(u"vCaption")

        self.vRow.addWidget(self.vCaption)

        self.vSpin = QSpinBox(self.hvGroup)
        self.vSpin.setObjectName(u"vSpin")
        self.vSpin.setMinimum(0)
        self.vSpin.setMaximum(50)
        self.vSpin.setValue(15)

        self.vRow.addWidget(self.vSpin)


        self.hvLayout.addLayout(self.vRow)


        self.layoutTabLayout.addWidget(self.hvGroup)

        self.applySpacingBtn = QPushButton(self.layoutTab)
        self.applySpacingBtn.setObjectName(u"applySpacingBtn")

        self.layoutTabLayout.addWidget(self.applySpacingBtn)

        self.layoutSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutTabLayout.addItem(self.layoutSpacer)

        self.controlTabs.addTab(self.layoutTab, "")
        self.testsTab = QWidget()
        self.testsTab.setObjectName(u"testsTab")
        self.testsLayout = QVBoxLayout(self.testsTab)
        self.testsLayout.setSpacing(10)
        self.testsLayout.setObjectName(u"testsLayout")
        self.perfBtn = QPushButton(self.testsTab)
        self.perfBtn.setObjectName(u"perfBtn")

        self.testsLayout.addWidget(self.perfBtn)

        self.extremeBtn = QPushButton(self.testsTab)
        self.extremeBtn.setObjectName(u"extremeBtn")

        self.testsLayout.addWidget(self.extremeBtn)

        self.reorderGroup = QGroupBox(self.testsTab)
        self.reorderGroup.setObjectName(u"reorderGroup")
        self.reorderLayout = QVBoxLayout(self.reorderGroup)
        self.reorderLayout.setObjectName(u"reorderLayout")
        self.shuffleBtn = QPushButton(self.reorderGroup)
        self.shuffleBtn.setObjectName(u"shuffleBtn")

        self.reorderLayout.addWidget(self.shuffleBtn)

        self.reverseBtn = QPushButton(self.reorderGroup)
        self.reverseBtn.setObjectName(u"reverseBtn")

        self.reorderLayout.addWidget(self.reverseBtn)

        self.sortBtn = QPushButton(self.reorderGroup)
        self.sortBtn.setObjectName(u"sortBtn")

        self.reorderLayout.addWidget(self.sortBtn)


        self.testsLayout.addWidget(self.reorderGroup)

        self.stressGroup = QGroupBox(self.testsTab)
        self.stressGroup.setObjectName(u"stressGroup")
        self.stressLayout = QVBoxLayout(self.stressGroup)
        self.stressLayout.setObjectName(u"stressLayout")
        self.resizeStressBtn = QPushButton(self.stressGroup)
        self.resizeStressBtn.setObjectName(u"resizeStressBtn")

        self.stressLayout.addWidget(self.resizeStressBtn)

        self.rapidAddBtn = QPushButton(self.stressGroup)
        self.rapidAddBtn.setObjectName(u"rapidAddBtn")

        self.stressLayout.addWidget(self.rapidAddBtn)


        self.testsLayout.addWidget(self.stressGroup)

        self.testsSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.testsLayout.addItem(self.testsSpacer)

        self.controlTabs.addTab(self.testsTab, "")
        self.infoTab = QWidget()
        self.infoTab.setObjectName(u"infoTab")
        self.infoLayout = QVBoxLayout(self.infoTab)
        self.infoLayout.setObjectName(u"infoLayout")
        self.infoLabel = QLabel(self.infoTab)
        self.infoLabel.setObjectName(u"infoLabel")
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.infoLabel.setTextFormat(Qt.RichText)

        self.infoLayout.addWidget(self.infoLabel)

        self.infoSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.infoLayout.addItem(self.infoSpacer)

        self.controlTabs.addTab(self.infoTab, "")
        self.mainSplitter.addWidget(self.controlTabs)
        self.flowScroll = QScrollArea(self.mainSplitter)
        self.flowScroll.setObjectName(u"flowScroll")
        self.flowScroll.setWidgetResizable(True)
        self.flowScroll.setMinimumSize(QSize(0, 400))
        self.flowWidget = QCustomFlowWidget()
        self.flowWidget.setObjectName(u"flowWidget")
        self.flowWidget.setGeometry(QRect(0, 0, 1270, 420))
        self.flowWidget.setProperty(u"spacing", 15)
        self.flowWidget.setProperty(u"horizontalSpacing", 15)
        self.flowWidget.setProperty(u"verticalSpacing", 15)
        self.flowWidget.setProperty(u"margin", 15)
        self.flowWidget.setProperty(u"animationEnabled", True)
        self.flowWidget.setProperty(u"animationDuration", 300)
        self.flowScroll.setWidget(self.flowWidget)
        self.mainSplitter.addWidget(self.flowScroll)

        self.rootLayout.addWidget(self.mainSplitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.controlTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomFlowWidget \u2014 Complete Test Suite", None))
        self.typeGroup.setTitle(QCoreApplication.translate("MainWindow", u"Widget Type", None))
        self.typeCaption.setText(QCoreApplication.translate("MainWindow", u"Type:", None))
        self.widgetType.setItemText(0, QCoreApplication.translate("MainWindow", u"Color Box", None))
        self.widgetType.setItemText(1, QCoreApplication.translate("MainWindow", u"Number Box", None))
        self.widgetType.setItemText(2, QCoreApplication.translate("MainWindow", u"Letter Box", None))
        self.widgetType.setItemText(3, QCoreApplication.translate("MainWindow", u"Icon Box", None))
        self.widgetType.setItemText(4, QCoreApplication.translate("MainWindow", u"Button", None))
        self.widgetType.setItemText(5, QCoreApplication.translate("MainWindow", u"Custom Size", None))
        self.widgetType.setItemText(6, QCoreApplication.translate("MainWindow", u"Random Color", None))
        self.widgetType.setItemText(7, QCoreApplication.translate("MainWindow", u"Gradient Box", None))

        self.addGroup.setTitle(QCoreApplication.translate("MainWindow", u"Add Widgets", None))
        self.addBtn.setText(QCoreApplication.translate("MainWindow", u"Add Widget", None))
        self.batchCaption.setText(QCoreApplication.translate("MainWindow", u"Batch:", None))
        self.add5Btn.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.add10Btn.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.add20Btn.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.add50Btn.setText(QCoreApplication.translate("MainWindow", u"50", None))
        self.add50Btn.setProperty(u"role", QCoreApplication.translate("MainWindow", u"warning", None))
        self.removeGroup.setTitle(QCoreApplication.translate("MainWindow", u"Remove Widgets", None))
        self.removeLastBtn.setText(QCoreApplication.translate("MainWindow", u"Remove Last", None))
        self.removeLastBtn.setProperty(u"role", QCoreApplication.translate("MainWindow", u"danger", None))
        self.removeRandomBtn.setText(QCoreApplication.translate("MainWindow", u"Remove Random", None))
        self.removeRandomBtn.setProperty(u"role", QCoreApplication.translate("MainWindow", u"warning", None))
        self.clearAllBtn.setText(QCoreApplication.translate("MainWindow", u"Clear All", None))
        self.clearAllBtn.setProperty(u"role", QCoreApplication.translate("MainWindow", u"danger", None))
        self.orderGroup.setTitle(QCoreApplication.translate("MainWindow", u"Data-driven Order", None))
        self.useJsonOrderCheck.setText(QCoreApplication.translate("MainWindow", u"Order seed tiles from style.json (QCustomFlowLayoutOrder)", None))
        self.counterGroup.setTitle(QCoreApplication.translate("MainWindow", u"Statistics", None))
        self.counterLabel.setText(QCoreApplication.translate("MainWindow", u"Widgets: 0", None))
        self.counterLabel.setProperty(u"state", QCoreApplication.translate("MainWindow", u"empty", None))
        self.controlTabs.setTabText(self.controlTabs.indexOf(self.managementTab), QCoreApplication.translate("MainWindow", u"Widget Management", None))
        self.enableGroup.setTitle(QCoreApplication.translate("MainWindow", u"Animation State", None))
        self.animateCb.setText(QCoreApplication.translate("MainWindow", u"Enable Animations", None))
        self.durationGroup.setTitle(QCoreApplication.translate("MainWindow", u"Duration", None))
        self.durationCaption.setText(QCoreApplication.translate("MainWindow", u"Time:", None))
        self.durationLabel.setText(QCoreApplication.translate("MainWindow", u"300ms", None))
        self.easingGroup.setTitle(QCoreApplication.translate("MainWindow", u"Easing Curve", None))
        self.statusGroup.setTitle(QCoreApplication.translate("MainWindow", u"Status", None))
        self.animStatus.setText(QCoreApplication.translate("MainWindow", u"Idle", None))
        self.animStatus.setProperty(u"state", QCoreApplication.translate("MainWindow", u"idle", None))
        self.controlTabs.setTabText(self.controlTabs.indexOf(self.animationTab), QCoreApplication.translate("MainWindow", u"Animation Settings", None))
        self.marginGroup.setTitle(QCoreApplication.translate("MainWindow", u"Margin", None))
        self.marginCaption.setText(QCoreApplication.translate("MainWindow", u"Value:", None))
        self.marginLabel.setText(QCoreApplication.translate("MainWindow", u"15px", None))
        self.spacingGroup.setTitle(QCoreApplication.translate("MainWindow", u"Spacing", None))
        self.spacingCaption.setText(QCoreApplication.translate("MainWindow", u"Value:", None))
        self.spacingLabel.setText(QCoreApplication.translate("MainWindow", u"15px", None))
        self.hvGroup.setTitle(QCoreApplication.translate("MainWindow", u"Separate Spacing", None))
        self.hCaption.setText(QCoreApplication.translate("MainWindow", u"Horizontal:", None))
        self.vCaption.setText(QCoreApplication.translate("MainWindow", u"Vertical:", None))
        self.applySpacingBtn.setText(QCoreApplication.translate("MainWindow", u"Apply Separate Spacing", None))
        self.controlTabs.setTabText(self.controlTabs.indexOf(self.layoutTab), QCoreApplication.translate("MainWindow", u"Layout Properties", None))
        self.perfBtn.setText(QCoreApplication.translate("MainWindow", u"Performance Test (100 widgets)", None))
        self.perfBtn.setProperty(u"role", QCoreApplication.translate("MainWindow", u"warning", None))
        self.extremeBtn.setText(QCoreApplication.translate("MainWindow", u"Extreme Test (500 widgets)", None))
        self.extremeBtn.setProperty(u"role", QCoreApplication.translate("MainWindow", u"danger", None))
        self.reorderGroup.setTitle(QCoreApplication.translate("MainWindow", u"Reorder Tests", None))
        self.shuffleBtn.setText(QCoreApplication.translate("MainWindow", u"Shuffle Widgets", None))
        self.reverseBtn.setText(QCoreApplication.translate("MainWindow", u"Reverse Order", None))
        self.sortBtn.setText(QCoreApplication.translate("MainWindow", u"Sort by Size", None))
        self.stressGroup.setTitle(QCoreApplication.translate("MainWindow", u"Stress Tests", None))
        self.resizeStressBtn.setText(QCoreApplication.translate("MainWindow", u"Resize Stress Test", None))
        self.rapidAddBtn.setText(QCoreApplication.translate("MainWindow", u"Rapid Add/Remove", None))
        self.rapidAddBtn.setProperty(u"role", QCoreApplication.translate("MainWindow", u"warning", None))
        self.controlTabs.setTabText(self.controlTabs.indexOf(self.testsTab), QCoreApplication.translate("MainWindow", u"Test Scenarios", None))
        self.infoLabel.setText(QCoreApplication.translate("MainWindow", u"<h2>QCustomFlowWidget \u2014 Information</h2>\n"
"<b>Features:</b><br>\n"
"\u2022 Smooth animated repositioning of widgets<br>\n"
"\u2022 Fully customizable in Qt Designer<br>\n"
"\u2022 Supports widgets of different sizes<br>\n"
"\u2022 Automatic wrapping to next line<br>\n"
"\u2022 Configurable margins and spacing<br>\n"
"\u2022 Various easing curves for animations<br>\n"
"\u2022 Data-driven ordering via orderJsonPath (QCustomFlowLayoutOrder)<br>\n"
"\u2022 Performance optimized for many widgets<br>\n"
"<br>\n"
"<b>Usage Tips:</b><br>\n"
"\u2022 Resize the window to see widgets reposition smoothly<br>\n"
"\u2022 Try different easing curves for different animation feels<br>\n"
"\u2022 Use batch operations to test performance<br>\n"
"\u2022 Separate horizontal/vertical spacing for fine control<br>\n"
"<br>\n"
"<b>Test Scenarios:</b><br>\n"
"\u2022 Add many widgets to test layout performance<br>\n"
"\u2022 Shuffle widgets to see reordering animation<br>\n"
"\u2022 Stress test to check stability<br>\n"
"\u2022 T"
                        "ry different widget sizes for complex layouts<br>\n"
"<br>\n"
"<b>Properties:</b><br>\n"
"\u2022 animationEnabled \u2014 Toggle animations on/off<br>\n"
"\u2022 animationDuration \u2014 Set animation speed (ms)<br>\n"
"\u2022 animationEasingCurve \u2014 Choose easing curve<br>\n"
"\u2022 margin \u2014 Space around layout edges<br>\n"
"\u2022 spacing \u2014 Space between widgets<br>\n"
"\u2022 horizontalSpacing \u2014 Horizontal space between widgets<br>\n"
"\u2022 verticalSpacing \u2014 Vertical space between widgets<br>\n"
"\u2022 orderJsonPath \u2014 JSON file naming the widget order", None))
        self.controlTabs.setTabText(self.controlTabs.indexOf(self.infoTab), QCoreApplication.translate("MainWindow", u"Information", None))
        self.flowWidget.setProperty(u"animationEasingCurve", QCoreApplication.translate("MainWindow", u"OutCubic", None))
    # retranslateUi

