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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(520, 420)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.outerLayout = QVBoxLayout(self.centralwidget)
        self.outerLayout.setObjectName(u"outerLayout")
        self.topRow = QHBoxLayout()
        self.topRow.setObjectName(u"topRow")
        self.themeLabel = QLabel(self.centralwidget)
        self.themeLabel.setObjectName(u"themeLabel")

        self.topRow.addWidget(self.themeLabel)

        self.toggleButton = QCustomQPushButton(self.centralwidget)
        self.toggleButton.setObjectName(u"toggleButton")

        self.topRow.addWidget(self.toggleButton)

        self.topSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topRow.addItem(self.topSpacer)


        self.outerLayout.addLayout(self.topRow)

        self.variantGrid = QGridLayout()
        self.variantGrid.setObjectName(u"variantGrid")
        self.cornerLabel = QLabel(self.centralwidget)
        self.cornerLabel.setObjectName(u"cornerLabel")

        self.variantGrid.addWidget(self.cornerLabel, 0, 0, 1, 1)

        self.colLabelSm = QLabel(self.centralwidget)
        self.colLabelSm.setObjectName(u"colLabelSm")

        self.variantGrid.addWidget(self.colLabelSm, 0, 1, 1, 1)

        self.colLabelMd = QLabel(self.centralwidget)
        self.colLabelMd.setObjectName(u"colLabelMd")

        self.variantGrid.addWidget(self.colLabelMd, 0, 2, 1, 1)

        self.colLabelLg = QLabel(self.centralwidget)
        self.colLabelLg.setObjectName(u"colLabelLg")

        self.variantGrid.addWidget(self.colLabelLg, 0, 3, 1, 1)

        self.rowLabelPrimary = QLabel(self.centralwidget)
        self.rowLabelPrimary.setObjectName(u"rowLabelPrimary")

        self.variantGrid.addWidget(self.rowLabelPrimary, 1, 0, 1, 1)

        self.btnPrimarySm = QCustomQPushButton(self.centralwidget)
        self.btnPrimarySm.setObjectName(u"btnPrimarySm")

        self.variantGrid.addWidget(self.btnPrimarySm, 1, 1, 1, 1)

        self.btnPrimaryMd = QCustomQPushButton(self.centralwidget)
        self.btnPrimaryMd.setObjectName(u"btnPrimaryMd")

        self.variantGrid.addWidget(self.btnPrimaryMd, 1, 2, 1, 1)

        self.btnPrimaryLg = QCustomQPushButton(self.centralwidget)
        self.btnPrimaryLg.setObjectName(u"btnPrimaryLg")

        self.variantGrid.addWidget(self.btnPrimaryLg, 1, 3, 1, 1)

        self.rowLabelSecondary = QLabel(self.centralwidget)
        self.rowLabelSecondary.setObjectName(u"rowLabelSecondary")

        self.variantGrid.addWidget(self.rowLabelSecondary, 2, 0, 1, 1)

        self.btnSecondarySm = QCustomQPushButton(self.centralwidget)
        self.btnSecondarySm.setObjectName(u"btnSecondarySm")

        self.variantGrid.addWidget(self.btnSecondarySm, 2, 1, 1, 1)

        self.btnSecondaryMd = QCustomQPushButton(self.centralwidget)
        self.btnSecondaryMd.setObjectName(u"btnSecondaryMd")

        self.variantGrid.addWidget(self.btnSecondaryMd, 2, 2, 1, 1)

        self.btnSecondaryLg = QCustomQPushButton(self.centralwidget)
        self.btnSecondaryLg.setObjectName(u"btnSecondaryLg")

        self.variantGrid.addWidget(self.btnSecondaryLg, 2, 3, 1, 1)

        self.rowLabelOutline = QLabel(self.centralwidget)
        self.rowLabelOutline.setObjectName(u"rowLabelOutline")

        self.variantGrid.addWidget(self.rowLabelOutline, 3, 0, 1, 1)

        self.btnOutlineSm = QCustomQPushButton(self.centralwidget)
        self.btnOutlineSm.setObjectName(u"btnOutlineSm")

        self.variantGrid.addWidget(self.btnOutlineSm, 3, 1, 1, 1)

        self.btnOutlineMd = QCustomQPushButton(self.centralwidget)
        self.btnOutlineMd.setObjectName(u"btnOutlineMd")

        self.variantGrid.addWidget(self.btnOutlineMd, 3, 2, 1, 1)

        self.btnOutlineLg = QCustomQPushButton(self.centralwidget)
        self.btnOutlineLg.setObjectName(u"btnOutlineLg")

        self.variantGrid.addWidget(self.btnOutlineLg, 3, 3, 1, 1)

        self.rowLabelGhost = QLabel(self.centralwidget)
        self.rowLabelGhost.setObjectName(u"rowLabelGhost")

        self.variantGrid.addWidget(self.rowLabelGhost, 4, 0, 1, 1)

        self.btnGhostSm = QCustomQPushButton(self.centralwidget)
        self.btnGhostSm.setObjectName(u"btnGhostSm")

        self.variantGrid.addWidget(self.btnGhostSm, 4, 1, 1, 1)

        self.btnGhostMd = QCustomQPushButton(self.centralwidget)
        self.btnGhostMd.setObjectName(u"btnGhostMd")

        self.variantGrid.addWidget(self.btnGhostMd, 4, 2, 1, 1)

        self.btnGhostLg = QCustomQPushButton(self.centralwidget)
        self.btnGhostLg.setObjectName(u"btnGhostLg")

        self.variantGrid.addWidget(self.btnGhostLg, 4, 3, 1, 1)

        self.rowLabelDestructive = QLabel(self.centralwidget)
        self.rowLabelDestructive.setObjectName(u"rowLabelDestructive")

        self.variantGrid.addWidget(self.rowLabelDestructive, 5, 0, 1, 1)

        self.btnDestructiveSm = QCustomQPushButton(self.centralwidget)
        self.btnDestructiveSm.setObjectName(u"btnDestructiveSm")

        self.variantGrid.addWidget(self.btnDestructiveSm, 5, 1, 1, 1)

        self.btnDestructiveMd = QCustomQPushButton(self.centralwidget)
        self.btnDestructiveMd.setObjectName(u"btnDestructiveMd")

        self.variantGrid.addWidget(self.btnDestructiveMd, 5, 2, 1, 1)

        self.btnDestructiveLg = QCustomQPushButton(self.centralwidget)
        self.btnDestructiveLg.setObjectName(u"btnDestructiveLg")

        self.variantGrid.addWidget(self.btnDestructiveLg, 5, 3, 1, 1)


        self.outerLayout.addLayout(self.variantGrid)

        self.bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.outerLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Design Tokens - variant / size", None))
        self.themeLabel.setText(QCoreApplication.translate("MainWindow", u"Theme:", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Switch to dark", None))
        self.toggleButton.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.cornerLabel.setText("")
        self.colLabelSm.setText(QCoreApplication.translate("MainWindow", u"<b>sm</b>", None))
        self.colLabelMd.setText(QCoreApplication.translate("MainWindow", u"<b>md</b>", None))
        self.colLabelLg.setText(QCoreApplication.translate("MainWindow", u"<b>lg</b>", None))
        self.rowLabelPrimary.setText(QCoreApplication.translate("MainWindow", u"<b>primary</b>", None))
        self.btnPrimarySm.setText(QCoreApplication.translate("MainWindow", u"Primary", None))
        self.btnPrimarySm.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
        self.btnPrimarySm.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"sm", None))
        self.btnPrimaryMd.setText(QCoreApplication.translate("MainWindow", u"Primary", None))
        self.btnPrimaryMd.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
        self.btnPrimaryMd.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.btnPrimaryLg.setText(QCoreApplication.translate("MainWindow", u"Primary", None))
        self.btnPrimaryLg.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"primary", None))
        self.btnPrimaryLg.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.rowLabelSecondary.setText(QCoreApplication.translate("MainWindow", u"<b>secondary</b>", None))
        self.btnSecondarySm.setText(QCoreApplication.translate("MainWindow", u"Secondary", None))
        self.btnSecondarySm.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"secondary", None))
        self.btnSecondarySm.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"sm", None))
        self.btnSecondaryMd.setText(QCoreApplication.translate("MainWindow", u"Secondary", None))
        self.btnSecondaryMd.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"secondary", None))
        self.btnSecondaryMd.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.btnSecondaryLg.setText(QCoreApplication.translate("MainWindow", u"Secondary", None))
        self.btnSecondaryLg.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"secondary", None))
        self.btnSecondaryLg.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.rowLabelOutline.setText(QCoreApplication.translate("MainWindow", u"<b>outline</b>", None))
        self.btnOutlineSm.setText(QCoreApplication.translate("MainWindow", u"Outline", None))
        self.btnOutlineSm.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.btnOutlineSm.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"sm", None))
        self.btnOutlineMd.setText(QCoreApplication.translate("MainWindow", u"Outline", None))
        self.btnOutlineMd.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.btnOutlineMd.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.btnOutlineLg.setText(QCoreApplication.translate("MainWindow", u"Outline", None))
        self.btnOutlineLg.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"outline", None))
        self.btnOutlineLg.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.rowLabelGhost.setText(QCoreApplication.translate("MainWindow", u"<b>ghost</b>", None))
        self.btnGhostSm.setText(QCoreApplication.translate("MainWindow", u"Ghost", None))
        self.btnGhostSm.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"ghost", None))
        self.btnGhostSm.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"sm", None))
        self.btnGhostMd.setText(QCoreApplication.translate("MainWindow", u"Ghost", None))
        self.btnGhostMd.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"ghost", None))
        self.btnGhostMd.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.btnGhostLg.setText(QCoreApplication.translate("MainWindow", u"Ghost", None))
        self.btnGhostLg.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"ghost", None))
        self.btnGhostLg.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
        self.rowLabelDestructive.setText(QCoreApplication.translate("MainWindow", u"<b>destructive</b>", None))
        self.btnDestructiveSm.setText(QCoreApplication.translate("MainWindow", u"Destructive", None))
        self.btnDestructiveSm.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"destructive", None))
        self.btnDestructiveSm.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"sm", None))
        self.btnDestructiveMd.setText(QCoreApplication.translate("MainWindow", u"Destructive", None))
        self.btnDestructiveMd.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"destructive", None))
        self.btnDestructiveMd.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"md", None))
        self.btnDestructiveLg.setText(QCoreApplication.translate("MainWindow", u"Destructive", None))
        self.btnDestructiveLg.setProperty(u"variant", QCoreApplication.translate("MainWindow", u"destructive", None))
        self.btnDestructiveLg.setProperty(u"sizeVariant", QCoreApplication.translate("MainWindow", u"lg", None))
    # retranslateUi

