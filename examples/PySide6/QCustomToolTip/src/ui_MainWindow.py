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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 300)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(14)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(20, 20, 20, 20)
        self.tipBtn1 = QPushButton(self.centralwidget)
        self.tipBtn1.setObjectName(u"tipBtn1")

        self.rootLayout.addWidget(self.tipBtn1)

        self.tipRow = QWidget(self.centralwidget)
        self.tipRow.setObjectName(u"tipRow")
        self.tipRowLayout = QHBoxLayout(self.tipRow)
        self.tipRowLayout.setObjectName(u"tipRowLayout")
        self.tipRowLayout.setContentsMargins(0, 0, 0, 0)
        self.tipBtn2 = QPushButton(self.tipRow)
        self.tipBtn2.setObjectName(u"tipBtn2")

        self.tipRowLayout.addWidget(self.tipBtn2)

        self.tipBtn3 = QPushButton(self.tipRow)
        self.tipBtn3.setObjectName(u"tipBtn3")

        self.tipRowLayout.addWidget(self.tipBtn3)


        self.rootLayout.addWidget(self.tipRow)

        self.tipBtn4 = QPushButton(self.centralwidget)
        self.tipBtn4.setObjectName(u"tipBtn4")

        self.rootLayout.addWidget(self.tipBtn4)

        self.bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rootLayout.addItem(self.bottomSpacer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QCustomQToolTip Tail Position Test", None))
        self.tipBtn1.setText(QCoreApplication.translate("MainWindow", u"HOVER: Auto-positioned Tool-Tip", None))
#if QT_CONFIG(tooltip)
        self.tipBtn1.setToolTip(QCoreApplication.translate("MainWindow", u"Testing Auto-positioned Tool-Tip.  Try resizing the window then hover again!", None))
#endif // QT_CONFIG(tooltip)
        self.tipBtn2.setText(QCoreApplication.translate("MainWindow", u"HOVER: Auto-positioned Tool-Tip", None))
#if QT_CONFIG(tooltip)
        self.tipBtn2.setToolTip(QCoreApplication.translate("MainWindow", u"Testing Auto-positioned Tool-Tip.  Try resizing the window then hover again!", None))
#endif // QT_CONFIG(tooltip)
        self.tipBtn3.setText(QCoreApplication.translate("MainWindow", u"HOVER: Auto-positioned Tool-Tip", None))
#if QT_CONFIG(tooltip)
        self.tipBtn3.setToolTip(QCoreApplication.translate("MainWindow", u"Testing Auto-positioned Tool-Tip.  Try resizing the window then hover again!", None))
#endif // QT_CONFIG(tooltip)
        self.tipBtn4.setText(QCoreApplication.translate("MainWindow", u"HOVER: Auto-positioned Tool-Tip", None))
#if QT_CONFIG(tooltip)
        self.tipBtn4.setToolTip(QCoreApplication.translate("MainWindow", u"Testing Auto-positioned Tool-Tip.  Try resizing the window then hover again!", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

