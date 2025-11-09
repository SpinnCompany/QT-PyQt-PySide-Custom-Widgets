# coding:utf-8
from qtpy.QtCore import QEasingCurve, QPropertyAnimation, Qt, QEvent, Signal
from qtpy.QtGui import QColor, QResizeEvent, QPalette, QPaintEvent, QPainter, QMouseEvent
from qtpy.QtWidgets import (QDialog, QGraphicsDropShadowEffect, QStyleOption, QStyle, QApplication,
                             QGraphicsOpacityEffect, QWidget, QGraphicsBlurEffect)

from Custom_Widgets.components.python.ui_dialog import Ui_Form
from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.QCustomComponentLoader import QCustomComponentLoader

from Custom_Widgets.BlurWindow import GlobalBlur
        
class QCustomQDialog(QDialog, Ui_Form):
    accepted = Signal()
    rejected = Signal()
    
    title = None
    description = None
    # Add some padding if needed
    padding = 0
    margin = 60 #for drop shadow effect
    borderRadius = 0
    windowMovable = False
    animationDuration = 500
    
    maskWidget = None
    hasBlur = False

    def __init__(
        self,
        parent=None,
        showForm=None,
        title=None,
        description=None,
        padding=0,
        yesButtonIcon=None,
        cancelButtonIcon=None,
        yesButtonText="Yes",
        cancelButtonText="Cancel",
        animationDuration=300,
        showYesButton=True,
        showCancelButton=True,
        setModal=False,
        frameless=False,
        windowMovable=False,
        addWidget=None,
        blurBackground=True
    ):
        """Initialize the custom dialog with configurable options."""
        QDialog.__init__(self, parent)  # Initialize QDialog parent class
        Ui_Form.__init__(self)  # Initialize Ui_Form parent class

        self.window().installEventFilter(self)

        self.setupUi(self)

        # Mask widget setup
        # self.maskWidget = MaskWidget(parent)
        # self.maskWidget.hide()
        # self.maskWidget.setParent(self.parent())
        # self.maskWidget.lower()

        # Set title
        if title:
            self.titleLabel.setText(str(title))
        else:
            self.titleLabel.hide()

        # Set description
        if description:
            self.descriptionLabel.setText(str(description))
        else:
            self.descriptionLabel.hide()

        # Set padding
        self.padding = padding

        # Set button icons and text
        if yesButtonIcon:
            self.yesButton.setIcon(yesButtonIcon)
        self.yesButton.setText(yesButtonText)

        if cancelButtonIcon:
            self.cancelButton.setIcon(cancelButtonIcon)
        self.cancelButton.setText(cancelButtonText)

        # Set animation duration
        self.animationDuration = animationDuration

        # Show or hide buttons
        if not showYesButton:
            self.hideYesButton()

        if not showCancelButton:
            self.hideCancelButton()

        # Set modal behavior
        self.setModal(setModal)

        # Frameless and movable settings
        if frameless:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            if windowMovable:
                self.setMovable(True)
                self.titleBar.mousePressEvent = self.mousePressEvent
                self.titleBar.mouseMoveEvent = self.mouseMoveEvent
                self.titleBar.mouseReleaseEvent = self.mouseReleaseEvent
            else:
                self.setMovable(False)


        self.shownForm = None       
        if showForm:
            self.form = QCustomComponentLoader()
            self.form.loadComponent(formClass = showForm)
            self.verticalLayout_2.addWidget(self.form) 
            try:
                #older versions
                self.form.form =  self.form.ui 
                self.shownForm =  self.form.ui  
            except:
                self.shownForm = None
        
        if addWidget:
            self.addWidget(addWidget)

        self.yesButton.clicked.connect(self.__onYesButtonClicked)
        self.cancelButton.clicked.connect(self.__onCancelButtonClicked)
        self.yesButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        self.cancelButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        
        self.yesButton.setFocus()
        self.setShadowEffect()

        self.blurBackground = blurBackground
    
    def addWidget(self, widget, alignment = None):
        if alignment:
            self.verticalLayout_2.addWidget(widget, alignment=alignment) 
        else:
            self.verticalLayout_2.addWidget(widget) 
    
    def setShadowEffect(self, blurRadius=60, offset=(0, 10), color=QColor(0,0,0,100)):
        shadowEffect = QGraphicsDropShadowEffect(self.widget)
        shadowEffect.setBlurRadius(blurRadius)
        shadowEffect.setOffset(*offset)
        shadowEffect.setColor(color)
        # self.widget.setGraphicsEffect(None)
        self.widget.setGraphicsEffect(shadowEffect)
            
    def setMovable(self, movable: bool):
        self.windowMovable = movable

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if hasattr(self, 'offset'):
            if self.windowFlags() & Qt.FramelessWindowHint and self.windowMovable:
                self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if hasattr(self, 'offset'):
            del self.offset

    def __onCancelButtonClicked(self):
        self.reject()
        # self.rejected.emit()

    def __onYesButtonClicked(self):
        self.accept()
        # self.accepted.emit()

    def hideYesButton(self):
        self.yesButton.hide()

    def hideCancelButton(self):
        self.cancelButton.hide()
    
    def paintEvent(self, e: QPaintEvent):
        painter = QPainter(self)
        if not painter.isActive():
            return

        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 6, 6)

        # self.adjustSizeToContent()
        # painter.end()
        super().paintEvent(e)

        self.adjustSizeToContent()
        
    def showEvent(self, e):
        self.checkAppTheme()
        c = 0 if self.isDark() else 255
        if self.maskWidget is None:
            self.maskWidget = MaskWidget(parent=self.parent())
            self.maskWidget.lower()
        
        if not self.blurBackground:
            self.maskWidget.setStyleSheet(f'background:rgba({c}, {c}, {c}, .8)')
        else:
            self.maskWidget.setStyleSheet(f'background:rgba({c}, {c}, {c}, .1)')

        if self.maskWidget:
            self.maskWidget.show()

        """ Fade in """
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(0)
        opacityAni.setEndValue(1)
        opacityAni.setDuration(self.animationDuration)
        opacityAni.setEasingCurve(QEasingCurve.InSine)
        opacityAni.finished.connect(opacityEffect.deleteLater)
        opacityAni.start()
        
        super().showEvent(e)

            
    def hideEvent(self, e):
        super().hideEvent(e)
        try:
            self.maskWidget.hide()
            self.maskWidget.deleteLater()
        except:
            pass

    def done(self, code):
        """ fade out """
        self.setGraphicsEffect(None)
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(.9)
        opacityAni.setEndValue(0)
        opacityAni.setDuration(self.animationDuration)
        opacityAni.setEasingCurve(QEasingCurve.OutSine)
        opacityAni.finished.connect(lambda: QDialog.done(self, code))
        opacityAni.start()
        
        if self.maskWidget is not None:
            self.maskWidget.hide()
            self.maskWidget.deleteLater()
            self.maskWidget = None

    def resizeEvent(self, e):
        self.adjustSizeToContent()

    def adjustSizeToContent(self):
        # # Calculate the size hint based on the content
        # self.verticalLayout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        # content_size = self.layout().sizeHint()
        # self.setMinimumSize(content_size.width() + self.padding, content_size.height() + self.padding)
        # self.adjustSize()

        # Size maximized to support BG Blur
        self.adjustToParentSize()

        self.checkAppTheme()
        self.updateBlurEffect()

    def adjustToParentSize(self):
        """Adjust the dialog to the size and position of the parent."""
        if self.parent():
            self.resize(self.parent().size())
            
            # Calculate the top-left position to center the dialog on the parent
            parent_geometry = self.parent().geometry()
            parent_center_x = parent_geometry.x() + parent_geometry.width() // 2
            parent_center_y = parent_geometry.y() + parent_geometry.height() // 2

            dialog_x = parent_center_x - self.width() // 2
            dialog_y = parent_center_y - self.height() // 2

            self.move(dialog_x, dialog_y)  # Move the dialog to the calculated position

    def checkAppTheme(self):
        # icons
        if self.shownForm:
            if self.form.defaultTheme != QCustomTheme().theme:
                # theme changed
                self.form.applyThemeIcons()

    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() in {QEvent.Resize, QEvent.Move}:
                self.adjustToParentSize()

        return super().eventFilter(obj, e)
    
    def isDark(self):
        palette = self.palette()
        background_color = palette.color(QPalette.Window)
        # Calculate the luminance of the background color
        luminance = 0.2126 * background_color.red() + 0.7152 * background_color.green() + 0.0722 * background_color.blue()

        # Determine if the background color is dark or light
        if luminance < 128:
            # Dark background
            return True
        else:
            # Light background
            return False
    
    def updateBlurEffect(self):
        """Update the GlobalBlur effect to match the MaskWidget size."""
        if self.blurBackground and self.maskWidget is not None:
            self.bgBlur = GlobalBlur(HWND=self.winId(), widget=self, mask=self.maskWidget, Dark=self.isDark())
        
class MaskWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Make the widget fill the entire main window
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(self.parent().geometry() if parent else QApplication.primaryScreen().geometry())
        
                
        self.hide()
        
        if parent:
            parent.installEventFilter(self)
            parent.resizeEvent = self.resizeEvent
            parent.moveEvent = self.moveEvent
            
    def resizeEvent(self, event):
        try:
            if self.parent():
                parent_width = self.parent().width()
                parent_height = self.parent().height()
                self.setGeometry(0, 0, parent_width, parent_height)
        except:
            pass

    def moveEvent(self, event):
        try:
            if self.parent():
                parent_width = self.parent().width()
                parent_height = self.parent().height()
                self.setGeometry(0, 0, parent_width, parent_height)
        except:
            pass

    def eventFilter(self, obj, event):
        if obj == self.parent():
            if event.type() == QEvent.Resize:
                parent_width = self.parent().width()
                parent_height = self.parent().height()
                self.setGeometry(0, 0, parent_width, parent_height)
        return super().eventFilter(obj, event)
    
    def paintEvent(self, e: QPaintEvent):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        if not painter.isActive():
            return
        painter.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
        painter.end()
        super().paintEvent(e)
        
    def deleteLater(self):
        try:
            if self.parent():
                self.parent().destroyed.disconnect(self.onParentDestroyed)
            super().deleteLater()
        except:
            pass

    def onParentDestroyed(self):
        self.deleteLater()

    def showEvent(self, event):
        if self.parent():
            self.parent().destroyed.connect(self.onParentDestroyed)
        super().showEvent(event)

