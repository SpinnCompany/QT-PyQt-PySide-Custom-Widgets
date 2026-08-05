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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomSocialButton import QCustomSocialButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(620, 520)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(16)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(24, 24, 24, 24)
        self.brandGrid = QGridLayout()
        self.brandGrid.setSpacing(10)
        self.brandGrid.setObjectName(u"brandGrid")
        self.btnGithub = QCustomSocialButton(self.centralwidget)
        self.btnGithub.setObjectName(u"btnGithub")

        self.brandGrid.addWidget(self.btnGithub, 0, 0, 1, 1)

        self.btnGoogle = QCustomSocialButton(self.centralwidget)
        self.btnGoogle.setObjectName(u"btnGoogle")

        self.brandGrid.addWidget(self.btnGoogle, 0, 1, 1, 1)

        self.btnX = QCustomSocialButton(self.centralwidget)
        self.btnX.setObjectName(u"btnX")

        self.brandGrid.addWidget(self.btnX, 0, 2, 1, 1)

        self.btnFacebook = QCustomSocialButton(self.centralwidget)
        self.btnFacebook.setObjectName(u"btnFacebook")

        self.brandGrid.addWidget(self.btnFacebook, 1, 0, 1, 1)

        self.btnLinkedin = QCustomSocialButton(self.centralwidget)
        self.btnLinkedin.setObjectName(u"btnLinkedin")

        self.brandGrid.addWidget(self.btnLinkedin, 1, 1, 1, 1)

        self.btnDiscord = QCustomSocialButton(self.centralwidget)
        self.btnDiscord.setObjectName(u"btnDiscord")

        self.brandGrid.addWidget(self.btnDiscord, 1, 2, 1, 1)

        self.btnSlack = QCustomSocialButton(self.centralwidget)
        self.btnSlack.setObjectName(u"btnSlack")

        self.brandGrid.addWidget(self.btnSlack, 2, 0, 1, 1)

        self.btnApple = QCustomSocialButton(self.centralwidget)
        self.btnApple.setObjectName(u"btnApple")

        self.brandGrid.addWidget(self.btnApple, 2, 1, 1, 1)

        self.btnWhatsapp = QCustomSocialButton(self.centralwidget)
        self.btnWhatsapp.setObjectName(u"btnWhatsapp")

        self.brandGrid.addWidget(self.btnWhatsapp, 2, 2, 1, 1)


        self.rootLayout.addLayout(self.brandGrid)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")

        self.rootLayout.addWidget(self.statusLabel)

        self.controlsRow = QHBoxLayout()
        self.controlsRow.setSpacing(8)
        self.controlsRow.setObjectName(u"controlsRow")
        self.variantLabel = QLabel(self.centralwidget)
        self.variantLabel.setObjectName(u"variantLabel")

        self.controlsRow.addWidget(self.variantLabel)

        self.variantCombo = QComboBox(self.centralwidget)
        self.variantCombo.addItem("")
        self.variantCombo.addItem("")
        self.variantCombo.addItem("")
        self.variantCombo.setObjectName(u"variantCombo")

        self.controlsRow.addWidget(self.variantCombo)

        self.shapeLabel = QLabel(self.centralwidget)
        self.shapeLabel.setObjectName(u"shapeLabel")

        self.controlsRow.addWidget(self.shapeLabel)

        self.shapeCombo = QComboBox(self.centralwidget)
        self.shapeCombo.addItem("")
        self.shapeCombo.addItem("")
        self.shapeCombo.addItem("")
        self.shapeCombo.setObjectName(u"shapeCombo")

        self.controlsRow.addWidget(self.shapeCombo)

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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomSocialButton Showcase", None))
        self.btnGithub.setProperty(u"brand", QCoreApplication.translate("MainWindow", u"github", None))
        self.btnGithub.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Continue with GitHub", None))
        self.btnGoogle.setProperty(u"brand", QCoreApplication.translate("MainWindow", u"google", None))
        self.btnGoogle.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Continue with Google", None))
        self.btnX.setProperty(u"brand", QCoreApplication.translate("MainWindow", u"x", None))
        self.btnX.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Share on X", None))
        self.btnFacebook.setProperty(u"brand", QCoreApplication.translate("MainWindow", u"facebook", None))
        self.btnFacebook.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Continue with Facebook", None))
        self.btnLinkedin.setProperty(u"brand", QCoreApplication.translate("MainWindow", u"linkedin", None))
        self.btnLinkedin.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Share on LinkedIn", None))
        self.btnDiscord.setProperty(u"brand", QCoreApplication.translate("MainWindow", u"discord", None))
        self.btnDiscord.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Join on Discord", None))
        self.btnSlack.setProperty(u"brand", QCoreApplication.translate("MainWindow", u"slack", None))
        self.btnSlack.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Add to Slack", None))
        self.btnApple.setProperty(u"brand", QCoreApplication.translate("MainWindow", u"apple", None))
        self.btnApple.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Continue with Apple", None))
        self.btnWhatsapp.setProperty(u"brand", QCoreApplication.translate("MainWindow", u"whatsapp", None))
        self.btnWhatsapp.setProperty(u"text", QCoreApplication.translate("MainWindow", u"Share on WhatsApp", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Click a brand", None))
        self.variantLabel.setText(QCoreApplication.translate("MainWindow", u"Variant", None))
        self.variantCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"solid", None))
        self.variantCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"outline", None))
        self.variantCombo.setItemText(2, QCoreApplication.translate("MainWindow", u"soft", None))

        self.shapeLabel.setText(QCoreApplication.translate("MainWindow", u"Shape", None))
        self.shapeCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"rounded", None))
        self.shapeCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"pill", None))
        self.shapeCombo.setItemText(2, QCoreApplication.translate("MainWindow", u"square", None))

        self.themeBtn.setText(QCoreApplication.translate("MainWindow", u"Light / dark", None))
    # retranslateUi

