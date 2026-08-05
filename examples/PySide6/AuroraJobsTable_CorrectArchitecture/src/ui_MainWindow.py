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
    QPushButton, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomComponentContainer import QCustomComponentContainer
from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget
from Custom_Widgets.QCustomSidebar import QCustomSidebar
from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1440, 900)
        MainWindow.setMinimumSize(QSize(1120, 680))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QHBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.railBar = QCustomSidebar(self.centralwidget)
        self.railBar.setObjectName(u"railBar")
        self.railBar.setProperty(u"collapsedWidth", 72)
        self.railBar.setProperty(u"expandedWidth", 240)
        self.railBar.setProperty(u"defaultWidth", 72)
        self.railLayout = QVBoxLayout(self.railBar)
        self.railLayout.setSpacing(10)
        self.railLayout.setObjectName(u"railLayout")
        self.railLayout.setContentsMargins(14, 18, 14, 18)
        self.railLogo = QLabel(self.railBar)
        self.railLogo.setObjectName(u"railLogo")
        self.railLogo.setMinimumSize(QSize(0, 40))
        self.railLogo.setMaximumSize(QSize(16777215, 40))
        self.railLogo.setAlignment(Qt.AlignCenter)

        self.railLayout.addWidget(self.railLogo)

        self.sidebarToggle = QPushButton(self.railBar)
        self.sidebarToggle.setObjectName(u"sidebarToggle")
        self.sidebarToggle.setMinimumSize(QSize(0, 40))
        self.sidebarToggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.sidebarToggle.setIconSize(QSize(20, 20))

        self.railLayout.addWidget(self.sidebarToggle)

        self.navWork = QCustomSidebarButton(self.railBar)
        self.navWork.setObjectName(u"navWork")
        self.navWork.setMinimumSize(QSize(0, 44))
        self.navWork.setCheckable(True)
        self.navWork.setAutoExclusive(True)
        self.navWork.setChecked(True)
        self.navWork.setIconSize(QSize(20, 20))

        self.railLayout.addWidget(self.navWork)

        self.navCalendar = QCustomSidebarButton(self.railBar)
        self.navCalendar.setObjectName(u"navCalendar")
        self.navCalendar.setMinimumSize(QSize(0, 44))
        self.navCalendar.setCheckable(True)
        self.navCalendar.setAutoExclusive(True)
        self.navCalendar.setIconSize(QSize(20, 20))

        self.railLayout.addWidget(self.navCalendar)

        self.navClock = QCustomSidebarButton(self.railBar)
        self.navClock.setObjectName(u"navClock")
        self.navClock.setMinimumSize(QSize(0, 44))
        self.navClock.setCheckable(True)
        self.navClock.setAutoExclusive(True)
        self.navClock.setIconSize(QSize(20, 20))

        self.railLayout.addWidget(self.navClock)

        self.navUsers = QCustomSidebarButton(self.railBar)
        self.navUsers.setObjectName(u"navUsers")
        self.navUsers.setMinimumSize(QSize(0, 44))
        self.navUsers.setCheckable(True)
        self.navUsers.setAutoExclusive(True)
        self.navUsers.setIconSize(QSize(20, 20))

        self.railLayout.addWidget(self.navUsers)

        self.navInvoice = QCustomSidebarButton(self.railBar)
        self.navInvoice.setObjectName(u"navInvoice")
        self.navInvoice.setMinimumSize(QSize(0, 44))
        self.navInvoice.setCheckable(True)
        self.navInvoice.setAutoExclusive(True)
        self.navInvoice.setIconSize(QSize(20, 20))

        self.railLayout.addWidget(self.navInvoice)

        self.navNote = QCustomSidebarButton(self.railBar)
        self.navNote.setObjectName(u"navNote")
        self.navNote.setMinimumSize(QSize(0, 44))
        self.navNote.setCheckable(True)
        self.navNote.setAutoExclusive(True)
        self.navNote.setIconSize(QSize(20, 20))

        self.railLayout.addWidget(self.navNote)

        self.navBox = QCustomSidebarButton(self.railBar)
        self.navBox.setObjectName(u"navBox")
        self.navBox.setMinimumSize(QSize(0, 44))
        self.navBox.setCheckable(True)
        self.navBox.setAutoExclusive(True)
        self.navBox.setIconSize(QSize(20, 20))

        self.railLayout.addWidget(self.navBox)

        self.navChart = QCustomSidebarButton(self.railBar)
        self.navChart.setObjectName(u"navChart")
        self.navChart.setMinimumSize(QSize(0, 44))
        self.navChart.setCheckable(True)
        self.navChart.setAutoExclusive(True)
        self.navChart.setIconSize(QSize(20, 20))

        self.railLayout.addWidget(self.navChart)

        self.railSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.railLayout.addItem(self.railSpacer)

        self.navSettings = QCustomSidebarButton(self.railBar)
        self.navSettings.setObjectName(u"navSettings")
        self.navSettings.setMinimumSize(QSize(0, 44))
        self.navSettings.setCheckable(True)
        self.navSettings.setAutoExclusive(True)
        self.navSettings.setIconSize(QSize(20, 20))

        self.railLayout.addWidget(self.navSettings)


        self.rootLayout.addWidget(self.railBar)

        self.mainColumn = QWidget(self.centralwidget)
        self.mainColumn.setObjectName(u"mainColumn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainColumn.sizePolicy().hasHeightForWidth())
        self.mainColumn.setSizePolicy(sizePolicy)
        self.mainColumnLayout = QVBoxLayout(self.mainColumn)
        self.mainColumnLayout.setSpacing(0)
        self.mainColumnLayout.setObjectName(u"mainColumnLayout")
        self.mainColumnLayout.setContentsMargins(0, 0, 0, 0)
        self.topbar = QFrame(self.mainColumn)
        self.topbar.setObjectName(u"topbar")
        self.topbar.setMinimumSize(QSize(0, 64))
        self.topbar.setMaximumSize(QSize(16777215, 64))
        self.topbar.setFrameShape(QFrame.StyledPanel)
        self.topbarLayout = QHBoxLayout(self.topbar)
        self.topbarLayout.setSpacing(14)
        self.topbarLayout.setObjectName(u"topbarLayout")
        self.topbarLayout.setContentsMargins(28, 0, 24, 0)
        self.crumb = QLabel(self.topbar)
        self.crumb.setObjectName(u"crumb")
        self.crumb.setTextFormat(Qt.RichText)

        self.topbarLayout.addWidget(self.crumb)

        self.topbarSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topbarLayout.addItem(self.topbarSpacer)

        self.searchIcon = QToolButton(self.topbar)
        self.searchIcon.setObjectName(u"searchIcon")
        self.searchIcon.setMinimumSize(QSize(34, 34))
        self.searchIcon.setMaximumSize(QSize(34, 34))
        self.searchIcon.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.searchIcon.setAutoRaise(True)
        self.searchIcon.setIconSize(QSize(18, 18))

        self.topbarLayout.addWidget(self.searchIcon)

        self.helpIcon = QToolButton(self.topbar)
        self.helpIcon.setObjectName(u"helpIcon")
        self.helpIcon.setMinimumSize(QSize(34, 34))
        self.helpIcon.setMaximumSize(QSize(34, 34))
        self.helpIcon.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.helpIcon.setAutoRaise(True)
        self.helpIcon.setIconSize(QSize(18, 18))

        self.topbarLayout.addWidget(self.helpIcon)

        self.bellIcon = QToolButton(self.topbar)
        self.bellIcon.setObjectName(u"bellIcon")
        self.bellIcon.setMinimumSize(QSize(34, 34))
        self.bellIcon.setMaximumSize(QSize(34, 34))
        self.bellIcon.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.bellIcon.setAutoRaise(True)
        self.bellIcon.setIconSize(QSize(18, 18))

        self.topbarLayout.addWidget(self.bellIcon)

        self.avatar = QPushButton(self.topbar)
        self.avatar.setObjectName(u"avatar")
        self.avatar.setMinimumSize(QSize(36, 36))
        self.avatar.setMaximumSize(QSize(36, 36))

        self.topbarLayout.addWidget(self.avatar)

        self.avatarCaret = QToolButton(self.topbar)
        self.avatarCaret.setObjectName(u"avatarCaret")
        self.avatarCaret.setMinimumSize(QSize(16, 34))
        self.avatarCaret.setMaximumSize(QSize(16, 34))
        self.avatarCaret.setAutoRaise(True)
        self.avatarCaret.setIconSize(QSize(13, 13))

        self.topbarLayout.addWidget(self.avatarCaret)


        self.mainColumnLayout.addWidget(self.topbar)

        self.pageStack = QCustomQStackedWidget(self.mainColumn)
        self.pageStack.setObjectName(u"pageStack")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.pageStack.sizePolicy().hasHeightForWidth())
        self.pageStack.setSizePolicy(sizePolicy1)
        self.pageStack.setProperty(u"slideTransition", True)
        self.pageStack.setProperty(u"transitionTime", 320)
        self.jobsContainer = QCustomComponentContainer()
        self.jobsContainer.setObjectName(u"jobsContainer")
        self.jobsContainer.setProperty(u"previewComponent", False)
        self.pageStack.addWidget(self.jobsContainer)

        self.mainColumnLayout.addWidget(self.pageStack)


        self.rootLayout.addWidget(self.mainColumn)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Aurora \u2014 Work \u00b7 Jobs (Correct Architecture)", None))
        self.railLogo.setText(QCoreApplication.translate("MainWindow", u"We.", None))
#if QT_CONFIG(tooltip)
        self.sidebarToggle.setToolTip(QCoreApplication.translate("MainWindow", u"Expand / collapse menu", None))
#endif // QT_CONFIG(tooltip)
        self.navWork.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Work", None))
        self.navCalendar.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Schedule", None))
        self.navClock.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Timesheets", None))
        self.navUsers.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Team", None))
        self.navInvoice.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Invoices", None))
        self.navNote.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Notes", None))
        self.navBox.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Inventory", None))
        self.navChart.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Reports", None))
        self.navSettings.setProperty(u"labelText", QCoreApplication.translate("MainWindow", u"Settings", None))
        self.crumb.setText(QCoreApplication.translate("MainWindow", u"Work  \u203a  <b>Jobs</b>", None))
        self.crumb.setProperty(u"role", QCoreApplication.translate("MainWindow", u"crumb", None))
        self.avatar.setText(QCoreApplication.translate("MainWindow", u"JG", None))
#if QT_CONFIG(tooltip)
        self.avatar.setToolTip(QCoreApplication.translate("MainWindow", u"Toggle Aurora Light / Dark", None))
#endif // QT_CONFIG(tooltip)
        self.jobsContainer.setProperty(u"filePath", QCoreApplication.translate("MainWindow", u"ui/JobsComponent.ui", None))
    # retranslateUi

