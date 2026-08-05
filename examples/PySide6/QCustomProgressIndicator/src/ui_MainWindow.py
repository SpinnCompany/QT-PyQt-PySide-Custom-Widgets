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
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

from Custom_Widgets.QCustomProgressIndicator import QCustomProgressIndicator
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)

        self.downloadIndicator = QCustomProgressIndicator(self.centralwidget)
        self.downloadIndicator.setObjectName(u"downloadIndicator")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadIndicator.sizePolicy().hasHeightForWidth())
        self.downloadIndicator.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.downloadIndicator, 0, Qt.AlignHCenter)

        self.downloadCaption = QLabel(self.centralwidget)
        self.downloadCaption.setObjectName(u"downloadCaption")
        self.downloadCaption.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.downloadCaption)

        self.statsFrame = QFrame(self.centralwidget)
        self.statsFrame.setObjectName(u"statsFrame")
        self.statsFrame.setFrameShape(QFrame.StyledPanel)
        self.statsFrame.setFrameShadow(QFrame.Raised)
        self.statsLayout = QHBoxLayout(self.statsFrame)
        self.statsLayout.setObjectName(u"statsLayout")
        self.heightCaption = QLabel(self.statsFrame)
        self.heightCaption.setObjectName(u"heightCaption")

        self.statsLayout.addWidget(self.heightCaption)

        self.heightValue = QLabel(self.statsFrame)
        self.heightValue.setObjectName(u"heightValue")
        font = QFont()
        font.setBold(True)
        font.setItalic(True)
        self.heightValue.setFont(font)

        self.statsLayout.addWidget(self.heightValue)

        self.stepsCaption = QLabel(self.statsFrame)
        self.stepsCaption.setObjectName(u"stepsCaption")

        self.statsLayout.addWidget(self.stepsCaption)

        self.stepsValue = QLabel(self.statsFrame)
        self.stepsValue.setObjectName(u"stepsValue")
        self.stepsValue.setFont(font)

        self.statsLayout.addWidget(self.stepsValue)

        self.themeCaption = QLabel(self.statsFrame)
        self.themeCaption.setObjectName(u"themeCaption")

        self.statsLayout.addWidget(self.themeCaption)

        self.themeValue = QLabel(self.statsFrame)
        self.themeValue.setObjectName(u"themeValue")
        self.themeValue.setFont(font)

        self.statsLayout.addWidget(self.themeValue)


        self.verticalLayout.addWidget(self.statsFrame)

        self.formIndicator10 = QCustomProgressIndicator(self.centralwidget)
        self.formIndicator10.setObjectName(u"formIndicator10")
        sizePolicy.setHeightForWidth(self.formIndicator10.sizePolicy().hasHeightForWidth())
        self.formIndicator10.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.formIndicator10, 0, Qt.AlignHCenter)

        self.stepRow10 = QFrame(self.centralwidget)
        self.stepRow10.setObjectName(u"stepRow10")
        self.stepRow10.setFrameShape(QFrame.StyledPanel)
        self.stepRow10.setFrameShadow(QFrame.Raised)
        self.stepRow10Layout = QHBoxLayout(self.stepRow10)
        self.stepRow10Layout.setObjectName(u"stepRow10Layout")
        self.btnPct20 = QPushButton(self.stepRow10)
        self.btnPct20.setObjectName(u"btnPct20")

        self.stepRow10Layout.addWidget(self.btnPct20)

        self.btnPct40 = QPushButton(self.stepRow10)
        self.btnPct40.setObjectName(u"btnPct40")

        self.stepRow10Layout.addWidget(self.btnPct40)

        self.btnPct60 = QPushButton(self.stepRow10)
        self.btnPct60.setObjectName(u"btnPct60")

        self.stepRow10Layout.addWidget(self.btnPct60)

        self.btnPct80 = QPushButton(self.stepRow10)
        self.btnPct80.setObjectName(u"btnPct80")

        self.stepRow10Layout.addWidget(self.btnPct80)

        self.btnPct100 = QPushButton(self.stepRow10)
        self.btnPct100.setObjectName(u"btnPct100")

        self.stepRow10Layout.addWidget(self.btnPct100)


        self.verticalLayout.addWidget(self.stepRow10)

        self.caption10 = QLabel(self.centralwidget)
        self.caption10.setObjectName(u"caption10")
        self.caption10.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.caption10)

        self.formIndicator5 = QCustomProgressIndicator(self.centralwidget)
        self.formIndicator5.setObjectName(u"formIndicator5")
        sizePolicy.setHeightForWidth(self.formIndicator5.sizePolicy().hasHeightForWidth())
        self.formIndicator5.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.formIndicator5, 0, Qt.AlignHCenter)

        self.stepRow5 = QFrame(self.centralwidget)
        self.stepRow5.setObjectName(u"stepRow5")
        self.stepRow5.setFrameShape(QFrame.StyledPanel)
        self.stepRow5.setFrameShadow(QFrame.Raised)
        self.stepRow5Layout = QHBoxLayout(self.stepRow5)
        self.stepRow5Layout.setObjectName(u"stepRow5Layout")
        self.btnStep1 = QPushButton(self.stepRow5)
        self.btnStep1.setObjectName(u"btnStep1")

        self.stepRow5Layout.addWidget(self.btnStep1)

        self.btnStep2 = QPushButton(self.stepRow5)
        self.btnStep2.setObjectName(u"btnStep2")

        self.stepRow5Layout.addWidget(self.btnStep2)

        self.btnStep3 = QPushButton(self.stepRow5)
        self.btnStep3.setObjectName(u"btnStep3")

        self.stepRow5Layout.addWidget(self.btnStep3)

        self.btnStep4 = QPushButton(self.stepRow5)
        self.btnStep4.setObjectName(u"btnStep4")

        self.stepRow5Layout.addWidget(self.btnStep4)

        self.btnStep5 = QPushButton(self.stepRow5)
        self.btnStep5.setObjectName(u"btnStep5")

        self.stepRow5Layout.addWidget(self.btnStep5)


        self.verticalLayout.addWidget(self.stepRow5)

        self.caption5 = QLabel(self.centralwidget)
        self.caption5.setObjectName(u"caption5")
        self.caption5.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.caption5)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomProgressIndicator Showcase", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Form Progress Indicator", None))
        self.downloadCaption.setText(QCoreApplication.translate("MainWindow", u"Simulating Download Task", None))
        self.heightCaption.setText(QCoreApplication.translate("MainWindow", u"Height", None))
        self.heightValue.setText(QCoreApplication.translate("MainWindow", u"NA", None))
        self.stepsCaption.setText(QCoreApplication.translate("MainWindow", u"Steps", None))
        self.stepsValue.setText(QCoreApplication.translate("MainWindow", u"NA", None))
        self.themeCaption.setText(QCoreApplication.translate("MainWindow", u"Theme", None))
        self.themeValue.setText(QCoreApplication.translate("MainWindow", u"NA", None))
        self.btnPct20.setText(QCoreApplication.translate("MainWindow", u"20%", None))
        self.btnPct40.setText(QCoreApplication.translate("MainWindow", u"40%", None))
        self.btnPct60.setText(QCoreApplication.translate("MainWindow", u"60%", None))
        self.btnPct80.setText(QCoreApplication.translate("MainWindow", u"80%", None))
        self.btnPct100.setText(QCoreApplication.translate("MainWindow", u"100%", None))
        self.caption10.setText(QCoreApplication.translate("MainWindow", u"Simulating Navigation Through A Form With 10 Steps", None))
        self.btnStep1.setText(QCoreApplication.translate("MainWindow", u"Step 1", None))
        self.btnStep2.setText(QCoreApplication.translate("MainWindow", u"Step 2", None))
        self.btnStep3.setText(QCoreApplication.translate("MainWindow", u"Step 3", None))
        self.btnStep4.setText(QCoreApplication.translate("MainWindow", u"Step 4", None))
        self.btnStep5.setText(QCoreApplication.translate("MainWindow", u"Step 5", None))
        self.caption5.setText(QCoreApplication.translate("MainWindow", u"Simulating Navigation Through A Form With 5 Steps", None))
    # retranslateUi

