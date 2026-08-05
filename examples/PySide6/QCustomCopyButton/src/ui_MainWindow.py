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

from Custom_Widgets.QCustomCopyButton import QCustomCopyButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 320)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(24, 24, 24, 24)
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.copyOutline = QCustomCopyButton(self.centralwidget)
        self.copyOutline.setObjectName(u"copyOutline")

        self.verticalLayout.addWidget(self.copyOutline)

        self.copyGhost = QCustomCopyButton(self.centralwidget)
        self.copyGhost.setObjectName(u"copyGhost")

        self.verticalLayout.addWidget(self.copyGhost)

        self.copySolid = QCustomCopyButton(self.centralwidget)
        self.copySolid.setObjectName(u"copySolid")

        self.verticalLayout.addWidget(self.copySolid)

        self.copyIconOnly = QCustomCopyButton(self.centralwidget)
        self.copyIconOnly.setObjectName(u"copyIconOnly")
        self.copyIconOnly.setProperty(u"iconOnly", True)

        self.verticalLayout.addWidget(self.copyIconOnly)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.verticalLayout.addWidget(self.statusLabel)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setObjectName(u"controlsRow")
        self.delayLabel = QLabel(self.centralwidget)
        self.delayLabel.setObjectName(u"delayLabel")

        self.controlsRow.addWidget(self.delayLabel)

        self.delaySpin = QSpinBox(self.centralwidget)
        self.delaySpin.setObjectName(u"delaySpin")
        self.delaySpin.setMinimum(0)
        self.delaySpin.setMaximum(6000)
        self.delaySpin.setSingleStep(200)
        self.delaySpin.setValue(1600)

        self.controlsRow.addWidget(self.delaySpin)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")

        self.controlsRow.addWidget(self.themeButton)

        self.controlsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsRow.addItem(self.controlsSpacer)


        self.verticalLayout.addLayout(self.controlsRow)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomCopyButton", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Copy to clipboard \u2014 all three variants", None))
        self.copyOutline.setProperty(u"payload", QCoreApplication.translate("MainWindow", u"sk-live-outline-abc123", None))
        self.copyOutline.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Copy outline key", None))
        self.copyOutline.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.copyGhost.setProperty(u"payload", QCoreApplication.translate("MainWindow", u"sk-live-ghost-abc123", None))
        self.copyGhost.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Copy ghost key", None))
        self.copyGhost.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"ghost", None))
        self.copySolid.setProperty(u"payload", QCoreApplication.translate("MainWindow", u"sk-live-solid-abc123", None))
        self.copySolid.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Copy solid key", None))
        self.copySolid.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"solid", None))
        self.copyIconOnly.setProperty(u"payload", QCoreApplication.translate("MainWindow", u"short", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Press a button, then paste somewhere", None))
        self.delayLabel.setText(QCoreApplication.translate("MainWindow", u"Reset ms", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
    # retranslateUi

