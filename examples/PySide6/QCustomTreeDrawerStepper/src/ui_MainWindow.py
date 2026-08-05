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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTreeWidgetItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomStepper import QCustomStepper
from Custom_Widgets.QCustomTreeWidget import QCustomTreeWidget
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 520)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(12)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(20, 20, 20, 20)
        self.stepper = QCustomStepper(self.centralwidget)
        self.stepper.setObjectName(u"stepper")

        self.rootLayout.addWidget(self.stepper)

        self.navRow = QHBoxLayout()
        self.navRow.setObjectName(u"navRow")
        self.backBtn = QCustomQPushButton(self.centralwidget)
        self.backBtn.setObjectName(u"backBtn")

        self.navRow.addWidget(self.backBtn)

        self.navSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.navRow.addItem(self.navSpacer)

        self.nextBtn = QCustomQPushButton(self.centralwidget)
        self.nextBtn.setObjectName(u"nextBtn")

        self.navRow.addWidget(self.nextBtn)


        self.rootLayout.addLayout(self.navRow)

        self.tree = QCustomTreeWidget(self.centralwidget)
        self.qtreewidgetitem = QTreeWidgetItem()
        self.qtreewidgetitem.setText(0, u"1")
        self.tree.setHeaderItem(self.qtreewidgetitem)
        self.tree.setObjectName(u"tree")
        self.tree.header().setVisible(False)

        self.rootLayout.addWidget(self.tree)

        self.openDrawerBtn = QCustomQPushButton(self.centralwidget)
        self.openDrawerBtn.setObjectName(u"openDrawerBtn")

        self.rootLayout.addWidget(self.openDrawerBtn)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Tree / Drawer / Stepper", None))
        self.backBtn.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.backBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.nextBtn.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.nextBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
        self.openDrawerBtn.setText(QCoreApplication.translate("MainWindow", u"Open drawer", None))
        self.openDrawerBtn.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"secondary", None))
    # retranslateUi

