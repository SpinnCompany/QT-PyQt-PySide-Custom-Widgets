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
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomSparklesText import QCustomSparklesText
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 300)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(16)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(24, 24, 24, 24)
        self.sparklesMain = QCustomSparklesText(self.centralwidget)
        self.sparklesMain.setObjectName(u"sparklesMain")
        self.sparklesMain.setMinimumSize(QSize(0, 90))

        self.rootLayout.addWidget(self.sparklesMain)

        self.sparklesSecond = QCustomSparklesText(self.centralwidget)
        self.sparklesSecond.setObjectName(u"sparklesSecond")
        self.sparklesSecond.setMinimumSize(QSize(0, 90))
        self.sparklesSecond.setProperty(u"seed", 42)

        self.rootLayout.addWidget(self.sparklesSecond)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(8)
        self.controlsRow.setObjectName(u"controlsRow")
        self.countLabel = QLabel(self.centralwidget)
        self.countLabel.setObjectName(u"countLabel")

        self.controlsRow.addWidget(self.countLabel)

        self.countSpin = QSpinBox(self.centralwidget)
        self.countSpin.setObjectName(u"countSpin")
        self.countSpin.setMinimum(0)
        self.countSpin.setMaximum(60)
        self.countSpin.setValue(14)

        self.controlsRow.addWidget(self.countSpin)

        self.seedLabel = QLabel(self.centralwidget)
        self.seedLabel.setObjectName(u"seedLabel")

        self.controlsRow.addWidget(self.seedLabel)

        self.seedSpin = QSpinBox(self.centralwidget)
        self.seedSpin.setObjectName(u"seedSpin")
        self.seedSpin.setMinimum(0)
        self.seedSpin.setMaximum(999)
        self.seedSpin.setValue(7)

        self.controlsRow.addWidget(self.seedSpin)

        self.animateBtn = QPushButton(self.centralwidget)
        self.animateBtn.setObjectName(u"animateBtn")

        self.controlsRow.addWidget(self.animateBtn)

        self.themeBtn = QPushButton(self.centralwidget)
        self.themeBtn.setObjectName(u"themeBtn")

        self.controlsRow.addWidget(self.themeBtn)

        self.controlsSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.rootLayout.addLayout(self.controlsRow)

        self.bottomSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rootLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomSparklesText Showcase", None))
        self.sparklesMain.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Powered by AI", None))
        self.sparklesSecond.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Magic inside", None))
        self.countLabel.setText(QCoreApplication.translate("MainWindow", u"Sparkles", None))
        self.seedLabel.setText(QCoreApplication.translate("MainWindow", u"Seed", None))
        self.animateBtn.setText(QCoreApplication.translate("MainWindow", u"Animate", None))
        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
    # retranslateUi

