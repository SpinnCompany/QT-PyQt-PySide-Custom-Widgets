import weakref

from qtpy.QtGui import QPaintEvent, QPainter, QIcon, QPalette, QPixmap
from qtpy.QtCore import Qt, QPoint, QSize, QEvent, QTimer, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QObject, Signal
from qtpy.QtWidgets import QStyleOption, QWidget, QStyle, QGraphicsOpacityEffect, QApplication
from Custom_Widgets.components.python.ui_info import Ui_Form
from Custom_Widgets.QCustomComponentLoader import QCustomComponentLoader

class LoadForm(QWidget):
    def __init__(self, form):
        super().__init__()
        self.form = form
        self.form.setupUi(self)
        
class QCustomModals:
    class BaseModal(QWidget, Ui_Form):
        position = None
        title = None
        description = None
        closeIcon = None
        modalIcon = None
        isClosable = True
        animationDuration = 5000
        fadeOutDuration = 1000
        
        margin = 24
        spacing = 16
        
        closedSignal = Signal()
        
        commonStyle = ("""
                * {
                    background-color: transparent;
                }
                QPushButton#closeButton{
                    background-color: transparent;
                    font-weight: 1000;
                    min-width: 20px;
                    min-height: 20px;
                    max-width: 20px;
                    max-height: 20px;
                }
                QLabel#iconlabel{
                    min-width: 20px;
                    min-height: 20px;
                    max-width: 20px;
                    max-height: 20px;
                }
            """)
        
        def __init__(self, title=None, description=None, closeIcon=None, modalIcon=None, 
             isClosable=True, parent=None, position=None, animationDuration=None, showForm=None,
             addWidget=None, duration=None):
    
            super().__init__()
            self.setupUi(self)
            self._is_closing = False
            self._fadeOutAnimationRunning = False
            self._is_manual_close = False
            
            if parent:
                self.setParent(parent)

            if self.parent() is not None:
                palette = self.parent().palette()
            else:
                app = QApplication.instance()
                if app is None:
                    app = QApplication([])
                palette = app.palette()

            background_color = palette.color(QPalette.Window)
            luminance = 0.2126 * background_color.red() + 0.7152 * background_color.green() + 0.0722 * background_color.blue()
            self.isDark = luminance < 128

            self.closeIcon = self.style().standardIcon(QStyle.SP_TitleBarCloseButton).pixmap(QSize(32, 32))
            self.closeButton.setIcon(self.closeIcon)

            self.infoIcon = self.style().standardIcon(QStyle.SP_MessageBoxInformation).pixmap(QSize(32, 32))
            self.successIcon = self.style().standardIcon(QStyle.SP_DialogApplyButton).pixmap(QSize(32, 32))
            self.warningIcon = self.style().standardIcon(QStyle.SP_MessageBoxWarning).pixmap(QSize(32, 32))
            self.errorIcon = self.style().standardIcon(QStyle.SP_MessageBoxCritical).pixmap(QSize(32, 32))

            self.isClosable = isClosable
            self.position = position

            if title:
                self.titlelabel.setText(title)
            else:
                self.titlelabel.hide()

            if description:
                self.bodyLabel.setText(description)
            else:
                self.body.hide()

            if closeIcon:
                self.closeIcon = QIcon(closeIcon)
                self.closeButton.setIcon(self.closeIcon)

            if not self.isClosable and not title:
                self.header.hide()

            if modalIcon:
                self.modalIcon = QPixmap(modalIcon)
                self.iconlabel.setPixmap(self.modalIcon)

            if showForm: 
                self.form = QCustomComponentLoader()
                self.form.loadComponent(formClass=showForm)
                self.layout().addWidget(self.form) 
                self.form.form = self.form.ui 
                self.shownForm = self.form.ui  
              
            if addWidget:
                self.addWidget(addWidget)

            self.animationDuration = animationDuration if animationDuration else duration
            self._autoCloseTimer = None

            self.closeButton.setFixedSize(20, 20)
            self.closeButton.setIconSize(QSize(self.spacing, self.spacing))
            self.closeButton.setCursor(Qt.PointingHandCursor)
            self.closeButton.clicked.connect(self.manualClose)
            self.closeButton.setVisible(self.isClosable)

            self.opacityEffect = QGraphicsOpacityEffect(self)
            self.opacityEffect.setOpacity(1.0)
            self.setGraphicsEffect(self.opacityEffect)
            self.opacityAni = QPropertyAnimation(self.opacityEffect, b"opacity")
            self.opacityAni.setDuration(self.fadeOutDuration)
            self.opacityAni.setEasingCurve(QEasingCurve.OutCubic)
            self.opacityAni.finished.connect(self._onFadeOutFinished)

                        
        def paintEvent(self, e: QPaintEvent):
            opt = QStyleOption()
            opt.initFrom(self)
            painter = QPainter(self)
            self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

            painter.setRenderHints(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)

            rect = self.rect().adjusted(1, 1, -1, -1)
            painter.drawRoundedRect(rect, 6, 6)

            super().paintEvent(e)
            
            
        def adjustSizeToContent(self):
            self.adjustSize()
            
            if self.position == 'top-right':
                x = self.parent().size().width() - self.width() - self.margin
                self.move(x, self.pos().y())
            
            if self.position == 'top-center':
                x = (self.parent().size().width() - self.width()) / 2
                self.move(x, self.pos().y())

            elif self.position == 'top-left':
                x = self.margin
                self.move(x, self.pos().y())

            elif self.position == 'center-center':
                x = (self.parent().size().width() - self.width()) / 2
                y = (self.parent().size().height() - self.height()) / 2
                self.move(x, y)

            elif self.position == 'center-right':
                x = self.parent().size().width() - self.width() - self.margin
                y = (self.parent().size().height() - self.height()) / 2
                self.move(x, y)

            elif self.position == 'center-left':
                x = self.margin
                y = (self.parent().size().height() - self.height()) / 2
                self.move(x, y)

            elif self.position == 'bottom-right':
                x = self.parent().size().width() - self.width() - self.margin
                y = self.parent().size().height() - self.height() - self.margin
                self.move(x, y)

            elif self.position == 'bottom-left':
                x = self.margin
                y = self.parent().size().height() - self.height() - self.margin
                self.move(x, y)

        def manualClose(self):
            """Handle manual close button click - immediate removal"""
            if self._is_closing:
                return
            
            # Mark as manual close - no fade animation
            self._is_manual_close = True
            self._performClose()

        def closeModal(self):
            """Public method to close modal from external code"""
            if self._is_closing:
                return
            self._is_manual_close = True
            self._performClose()
            
        def fadeOut(self):
            """Auto fade out animation before closing"""
            if self._is_closing or self._fadeOutAnimationRunning:
                return
                
            if self.animationDuration is None or self.animationDuration < 0:
                self._performClose()
                return
                
            self._fadeOutAnimationRunning = True
            
            # Stop any ongoing animations
            if self.opacityAni.state() == QPropertyAnimation.Running:
                self.opacityAni.stop()
            
            # Start fade out animation
            self.opacityAni.setStartValue(1.0)
            self.opacityAni.setEndValue(0.0)
            self.opacityAni.start()

        def _onFadeOutFinished(self):
            """Called after fade out animation completes"""
            self._fadeOutAnimationRunning = False
            self._performClose()

        def _performClose(self):
            """Actually close the modal and clean up"""
            if self._is_closing:
                return
                
            self._is_closing = True
            
            # Stop auto-close timer if it exists
            if self._autoCloseTimer:
                self._autoCloseTimer.stop()
                self._autoCloseTimer.deleteLater()
                self._autoCloseTimer = None
            
            # Notify manager to remove this modal and update positions
            if self.position is not None:
                try:
                    manager = QCustomModalsManager.make(self.position)
                    manager.remove(self)
                except Exception as ex:
                    pass
            
            self.closedSignal.emit()
            
            # Clear graphics effect before deletion
            self.setGraphicsEffect(None)
            
            # Hide immediately
            self.hide()
            
            # Schedule deletion
            self.deleteLater()

        def closeEvent(self, e):
            """Handle close event"""
            if self._is_closing:
                e.accept()
                return
            
            self._performClose()
            e.accept()

        def forceClose(self):
            """Force close immediately without any animation"""
            self._is_manual_close = True
            self._performClose()

        def showEvent(self, e):
            self.adjustSizeToContent()
            
            # Set up auto-close timer only if not manually closed and duration is positive
            if not self._is_manual_close and self.animationDuration and self.animationDuration > 0:
                self._autoCloseTimer = QTimer(self)
                self._autoCloseTimer.setSingleShot(True)
                self._autoCloseTimer.timeout.connect(self.fadeOut)
                self._autoCloseTimer.start(self.animationDuration)

            if self.position is not None:
                manager = QCustomModalsManager.make(self.position)
                manager.add(self)
            
            super().showEvent(e)

        def setIcon(self, icon):
            self.icon = icon
            if isinstance(icon, QIcon):
                pixmap = icon.pixmap(QSize(32, 32))
                self.iconlabel.setPixmap(pixmap)
            elif isinstance(icon, str):
                pixmap = QPixmap(icon).scaled(QSize(32, 32))
                self.iconlabel.setPixmap(pixmap)
            else:
                self.iconlabel.hide()

        def setDescription(self, description):
            self.description = description
            if not self.description:
                self.description.hide()
                return
            self.bodyLabel.setText(description)
        
        def setTitle(self, title):
            self.title = title
            if not self.title:
                self.titlelabel.hide()
                return
            self.titlelabel.setText(title)

        def loadForm(self, form):
            self.showForm = form
            if self.showForm:
                self.form = LoadForm(self.showForm)
                self.verticalLayout_2.addWidget(self.form) 
            
        def addWidget(self, widget):
            self.widget = widget
            if self.widget:
                self.layout().addWidget(self.widget) 


    class InformationModal(BaseModal):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.setWindowTitle("Information")
            if self.modalIcon: self.iconlabel.setPixmap(self.modalIcon) 
            else: self.iconlabel.setPixmap(self.infoIcon)
            
            lightStyle = """
                InformationModal {
                    background-color: #E6F7FF;
                }
                InformationModal * {
                    color: #333333;
                    background-color: transparent;
                }
            """
            
            darkStyle = """
                InformationModal {
                    background-color: #2799be;
                }
                InformationModal * {
                    color: #F5F5F5;
                    background-color: transparent;
                }
            """
            
            if self.isDark:  
                self.setStyleSheet(darkStyle + self.commonStyle)
            else:
                self.setStyleSheet(lightStyle + self.commonStyle)

    class SuccessModal(BaseModal):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.setWindowTitle("Success")
            if self.modalIcon: self.iconlabel.setPixmap(self.modalIcon) 
            else: self.iconlabel.setPixmap(self.successIcon)
            
            lightStyle = """
                SuccessModal {
                    background-color: #C8E6C9;
                }
                SuccessModal * {
                    color: #333333;
                    background-color: transparent;
                }
            """
            darkStyle = """
                SuccessModal {
                    background-color: #29b328;
                }
                SuccessModal * {
                    color: #F5F5F5;
                    background-color: transparent;
                }
            """
            if self.isDark:
                self.setStyleSheet(darkStyle + self.commonStyle)
            else:
                self.setStyleSheet(lightStyle + self.commonStyle)
                

    class WarningModal(BaseModal):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.setWindowTitle("Warning")
            if self.modalIcon: self.iconlabel.setPixmap(self.modalIcon) 
            else: self.iconlabel.setPixmap(self.warningIcon)
            
            lightStyle = """
                WarningModal {
                    background-color: #FFF9E1;
                }
                WarningModal * {
                    color: #333333;
                    background-color: transparent;
                }
            """
            darkStyle = """
                WarningModal {
                    background-color: #bb8128;
                }
                WarningModal * {
                    color: #F5F5F5;
                    background-color: transparent;
                }
            """
            if self.isDark:
                self.setStyleSheet(darkStyle + self.commonStyle)
            else:
                self.setStyleSheet(lightStyle + self.commonStyle)


    class ErrorModal(BaseModal):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.setWindowTitle("Error")
            if self.modalIcon: self.iconlabel.setPixmap(self.modalIcon) 
            else: self.iconlabel.setPixmap(self.errorIcon)
            
            lightStyle = """
                ErrorModal {
                    background-color: #FFEBEE;
                }
                ErrorModal * {
                    color: #333333;
                    background-color: transparent;
                }
            """
            darkStyle = """
                ErrorModal {
                    background-color: #bb221d;
                }
                ErrorModal * {
                    color: #F5F5F5;
                    background-color: transparent;
                }
            """
            if self.isDark:
                self.setStyleSheet(darkStyle + self.commonStyle)
            else:
                self.setStyleSheet(lightStyle + self.commonStyle)



    class CustomModal(BaseModal):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.setWindowTitle("Custom")
            if self.modalIcon: self.iconlabel.setPixmap(QPixmap(self.modalIcon))

            style = ""
            self.setStyleSheet(style)
            

class QCustomModalsManager(QObject):
    _instance = None
    managers = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(QCustomModalsManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return

        super().__init__()
        self.spacing = 16
        self.margin = 24
        self.QCustomModalss = weakref.WeakKeyDictionary()
        self.aniGroups = weakref.WeakKeyDictionary()
        self.slideAnis = []
        self.dropAnis = []
        self.__initialized = True

    def add(self, QCustomModals: QCustomModals):
        p = QCustomModals.parent()
        if not p:
            return

        if p not in self.QCustomModalss:
            p.installEventFilter(self)
            self.QCustomModalss[p] = []
            self.aniGroups[p] = QParallelAnimationGroup(self)

        if QCustomModals in self.QCustomModalss[p]:
            return

        if self.QCustomModalss[p]:
            dropAni = QPropertyAnimation(QCustomModals, b'pos')
            dropAni.setDuration(200)
            dropAni.setEasingCurve(QEasingCurve.OutCubic)

            self.aniGroups[p].addAnimation(dropAni)
            self.dropAnis.append(dropAni)
            QCustomModals.setProperty('dropAni', dropAni)

        self.QCustomModalss[p].append(QCustomModals)
        slideAni = self.createSlideAni(QCustomModals)
        self.slideAnis.append(slideAni)

        QCustomModals.setProperty('slideAni', slideAni)
        QCustomModals.closedSignal.connect(lambda: self.remove(QCustomModals))

        slideAni.start()

    def remove(self, QCustomModals: QCustomModals):
        p = QCustomModals.parent()
        if p is None or p not in self.QCustomModalss:
            return

        if QCustomModals not in self.QCustomModalss[p]:
            return

        # Store the list of remaining modals before removal
        remaining_modals = [m for m in self.QCustomModalss[p] if m != QCustomModals]

        # Remove from list
        if QCustomModals in self.QCustomModalss[p]:
            self.QCustomModalss[p].remove(QCustomModals)

        # Clean up animations
        dropAni = QCustomModals.property('dropAni')
        if dropAni and p in self.aniGroups:
            self.aniGroups[p].removeAnimation(dropAni)
            if dropAni in self.dropAnis:
                self.dropAnis.remove(dropAni)

        slideAni = QCustomModals.property('slideAni')
        if slideAni and slideAni in self.slideAnis:
            self.slideAnis.remove(slideAni)

        # Clear properties
        QCustomModals.setProperty('dropAni', None)
        QCustomModals.setProperty('slideAni', None)

        # Immediately update positions of remaining modals
        if remaining_modals:
            # Calculate and set new positions for all remaining modals
            for modal in remaining_modals:
                new_pos = self.modalPosition(modal)
                modal.move(new_pos)
            
            # Start animation group if it exists and has animations
            if p in self.aniGroups and self.aniGroups[p].animationCount() > 0:
                self.aniGroups[p].start()
        else:
            # No modals left, clean up
            if p in self.QCustomModalss:
                del self.QCustomModalss[p]
            if p in self.aniGroups:
                self.aniGroups[p].deleteLater()
                del self.aniGroups[p]

    def createSlideAni(self, QCustomModals: QCustomModals):
        slideAni = QPropertyAnimation(QCustomModals, b'pos')
        slideAni.setEasingCurve(QEasingCurve.OutCubic)
        slideAni.setDuration(300)

        start_pos = self.slideStartPos(QCustomModals)
        end_pos = self.modalPosition(QCustomModals)
        
        QCustomModals.move(start_pos)
        
        slideAni.setStartValue(start_pos)
        slideAni.setEndValue(end_pos)

        return slideAni

    def updateDropAni(self, parent):
        if parent not in self.QCustomModalss:
            return
            
        for bar in self.QCustomModalss[parent]:
            ani = bar.property('dropAni')
            if not ani:
                continue

            current_pos = bar.pos()
            new_pos = self.modalPosition(bar)
            
            if current_pos != new_pos:
                ani.setStartValue(current_pos)
                ani.setEndValue(new_pos)

    def modalPosition(self, QCustomModals: QCustomModals, parentSize=None) -> QPoint:
        position = QCustomModals.position
        parent = QCustomModals.parent()
        
        if parent is None:
            return QCustomModals.pos()
            
        parentSize = parentSize or parent.size()
        
        if position == 'top-right':
            x = parentSize.width() - QCustomModals.width() - self.margin
            y = self.margin
        elif position == 'top-center':
            x = (parentSize.width() - QCustomModals.width()) / 2
            y = self.margin
        elif position == 'top-left':
            x = self.margin
            y = self.margin
        elif position == 'center-center':
            x = (parentSize.width() - QCustomModals.width()) / 2
            y = (parentSize.height() - QCustomModals.height()) / 2
        elif position == 'center-right':
            x = parentSize.width() - QCustomModals.width() - self.margin
            y = (parentSize.height() - QCustomModals.height()) / 2
        elif position == 'center-left':
            x = self.margin
            y = (parentSize.height() - QCustomModals.height()) / 2
        elif position == 'bottom-right':
            x = parentSize.width() - QCustomModals.width() - self.margin
            y = parentSize.height() - QCustomModals.height() - self.margin
        elif position == 'bottom-left':
            x = self.margin
            y = parentSize.height() - QCustomModals.height() - self.margin
        elif position == 'bottom-center':
            x = (parentSize.width() - QCustomModals.width()) / 2
            y = parentSize.height() - QCustomModals.height() - self.margin
        else:
            x = parentSize.width() - QCustomModals.width() - self.margin
            y = self.margin

        # Adjust y position for stacked modals
        if parent in self.QCustomModalss and QCustomModals in self.QCustomModalss[parent]:
            index = self.QCustomModalss[parent].index(QCustomModals)
            if position in ['top-right', 'top-left', 'top-center']:
                offset_y = y
                for i in range(index):
                    if i < len(self.QCustomModalss[parent]):
                        modal = self.QCustomModalss[parent][i]
                        if modal and modal is not QCustomModals:
                            offset_y += modal.height() + self.spacing
                y = offset_y
            elif position in ['bottom-right', 'bottom-left', 'bottom-center']:
                offset_y = y
                for i in range(index):
                    if i < len(self.QCustomModalss[parent]):
                        modal = self.QCustomModalss[parent][i]
                        if modal and modal is not QCustomModals:
                            offset_y -= modal.height() + self.spacing
                y = offset_y

        return QPoint(int(x), int(y))

    def slideStartPos(self, QCustomModals: QCustomModals) -> QPoint:
        target_pos = self.modalPosition(QCustomModals)
        
        if QCustomModals.position.startswith('top'):
            # Slide down from above final position
            return QPoint(target_pos.x(), target_pos.y() - QCustomModals.height())
        elif QCustomModals.position.startswith('bottom'):
            # Slide up from below final position
            return QPoint(target_pos.x(), target_pos.y() + QCustomModals.height())
        elif QCustomModals.position.startswith('center'):
            # For center positions, slide from appropriate direction
            if QCustomModals.position.endswith('left'):
                return QPoint(target_pos.x() - QCustomModals.width(), target_pos.y())
            elif QCustomModals.position.endswith('right'):
                return QPoint(target_pos.x() + QCustomModals.width(), target_pos.y())
            else:
                # Center-center slides from above
                return QPoint(target_pos.x(), target_pos.y() - QCustomModals.height())
        else:
            # Default slide from top
            return QPoint(target_pos.x(), target_pos.y() - QCustomModals.height())

    def eventFilter(self, obj, e: QEvent):
        if obj not in self.QCustomModalss:
            return False

        if e.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            size = e.size() if e.type() == QEvent.Resize else None
            modals = list(self.QCustomModalss[obj])
            for modal in modals:
                if modal and not modal._is_closing:
                    new_pos = self.modalPosition(modal, size)
                    modal.move(new_pos)

        return super().eventFilter(obj, e)

    @classmethod
    def register(cls, name):
        def wrapper(Manager):
            if name not in cls.managers:
                cls.managers[name] = Manager
            return Manager
        return wrapper

    @classmethod
    def make(cls, position: str):
        if position not in cls.managers:
            raise ValueError(f'`{position}` is an invalid animation type.')
        return cls.managers[position]()

@QCustomModalsManager.register("center-center")
class CenterCenterQCustomModalsManager(QCustomModalsManager):
    def modalPosition(self, QCustomModals: QCustomModals, parentSize=None):
        p = QCustomModals.parent()
        if p is None:
            return QCustomModals.pos()
        parentSize = parentSize or p.size()
        x = (parentSize.width() - QCustomModals.width()) // 2
        y = (parentSize.height() - QCustomModals.height()) // 2
        return QPoint(x, y)

    def slideStartPos(self, QCustomModals: QCustomModals):
        target_pos = self.modalPosition(QCustomModals)
        return QPoint(target_pos.x(), target_pos.y() - QCustomModals.height())

@QCustomModalsManager.register("top-center")
class TopQCustomModalsManager(QCustomModalsManager):
    def modalPosition(self, QCustomModals: QCustomModals, parentSize=None):
        p = QCustomModals.parent()
        if p is None or p not in self.QCustomModalss:
            return QCustomModals.pos()
        parentSize = parentSize or p.size()
        x = (parentSize.width() - QCustomModals.width()) // 2
        y = self.margin
        if QCustomModals in self.QCustomModalss[p]:
            index = self.QCustomModalss[p].index(QCustomModals)
            for bar in self.QCustomModalss[p][0:index]:
                if bar is not None and bar is not QCustomModals:
                    y += (bar.height() + self.spacing)
        return QPoint(x, y)

    def slideStartPos(self, QCustomModals: QCustomModals):
        target_pos = self.modalPosition(QCustomModals)
        return QPoint(target_pos.x(), target_pos.y() - QCustomModals.height())

@QCustomModalsManager.register("top-right")
class TopRightQCustomModalsManager(QCustomModalsManager):
    def modalPosition(self, QCustomModals: QCustomModals, parentSize=None):
        p = QCustomModals.parent()
        if p is None or p not in self.QCustomModalss:
            return QCustomModals.pos()
        parentSize = parentSize or p.size()
        x = parentSize.width() - QCustomModals.width() - self.margin
        y = self.margin
        if QCustomModals in self.QCustomModalss[p]:
            index = self.QCustomModalss[p].index(QCustomModals)
            for bar in self.QCustomModalss[p][0:index]:
                if bar is not None and bar is not QCustomModals:
                    y += (bar.height() + self.spacing)
        return QPoint(x, y)

    def slideStartPos(self, QCustomModals: QCustomModals):
        target_pos = self.modalPosition(QCustomModals)
        return QPoint(target_pos.x() + QCustomModals.width(), target_pos.y())

@QCustomModalsManager.register("bottom-right")
class BottomRightQCustomModalsManager(QCustomModalsManager):
    def modalPosition(self, QCustomModals: QCustomModals, parentSize=None) -> QPoint:
        p = QCustomModals.parent()
        if p is None or p not in self.QCustomModalss:
            return QCustomModals.pos()
        parentSize = parentSize or p.size()
        x = parentSize.width() - QCustomModals.width() - self.margin
        y = parentSize.height() - QCustomModals.height() - self.margin
        if QCustomModals in self.QCustomModalss[p]:
            index = self.QCustomModalss[p].index(QCustomModals)
            for bar in self.QCustomModalss[p][0:index]:
                if bar is not None and bar is not QCustomModals:
                    y -= (bar.height() + self.spacing)
        return QPoint(x, y)

    def slideStartPos(self, QCustomModals: QCustomModals):
        target_pos = self.modalPosition(QCustomModals)
        return QPoint(target_pos.x() + QCustomModals.width(), target_pos.y())

@QCustomModalsManager.register("top-left")
class TopLeftQCustomModalsManager(QCustomModalsManager):
    def modalPosition(self, QCustomModals: QCustomModals, parentSize=None) -> QPoint:
        p = QCustomModals.parent()
        if p is None or p not in self.QCustomModalss:
            return QCustomModals.pos()
        parentSize = parentSize or p.size()
        y = self.margin
        if QCustomModals in self.QCustomModalss[p]:
            index = self.QCustomModalss[p].index(QCustomModals)
            for bar in self.QCustomModalss[p][0:index]:
                if bar is not None and bar is not QCustomModals:
                    y += (bar.height() + self.spacing)
        return QPoint(self.margin, y)

    def slideStartPos(self, QCustomModals: QCustomModals):
        target_pos = self.modalPosition(QCustomModals)
        return QPoint(target_pos.x() - QCustomModals.width(), target_pos.y())

@QCustomModalsManager.register("bottom-left")
class BottomLeftQCustomModalsManager(QCustomModalsManager):
    def modalPosition(self, QCustomModals: QCustomModals, parentSize: QSize = None) -> QPoint:
        p = QCustomModals.parent()
        if p is None or p not in self.QCustomModalss:
            return QCustomModals.pos()
        parentSize = parentSize or p.size()
        y = parentSize.height() - QCustomModals.height() - self.margin
        if QCustomModals in self.QCustomModalss[p]:
            index = self.QCustomModalss[p].index(QCustomModals)
            for bar in self.QCustomModalss[p][0:index]:
                if bar is not None and bar is not QCustomModals:
                    y -= (bar.height() + self.spacing)
        return QPoint(self.margin, y)

    def slideStartPos(self, QCustomModals: QCustomModals):
        target_pos = self.modalPosition(QCustomModals)
        return QPoint(target_pos.x() - QCustomModals.width(), target_pos.y())

@QCustomModalsManager.register("bottom-center")
class BottomQCustomModalsManager(QCustomModalsManager):
    def modalPosition(self, QCustomModals: QCustomModals, parentSize: QSize = None) -> QPoint:
        p = QCustomModals.parent()
        if p is None or p not in self.QCustomModalss:
            return QCustomModals.pos()
        parentSize = parentSize or p.size()
        x = (parentSize.width() - QCustomModals.width()) // 2
        y = parentSize.height() - QCustomModals.height() - self.margin
        if QCustomModals in self.QCustomModalss[p]:
            index = self.QCustomModalss[p].index(QCustomModals)
            for bar in self.QCustomModalss[p][0:index]:
                if bar is not None and bar is not QCustomModals:
                    y -= (bar.height() + self.spacing)
        return QPoint(x, y)

    def slideStartPos(self, QCustomModals: QCustomModals):
        target_pos = self.modalPosition(QCustomModals)
        return QPoint(target_pos.x(), target_pos.y() + QCustomModals.height())

@QCustomModalsManager.register("center-left")
class CenterLeftQCustomModalsManager(QCustomModalsManager):
    def modalPosition(self, QCustomModals, parentSize=None):
        p = QCustomModals.parent()
        if p is None:
            return QCustomModals.pos()
        parentSize = parentSize or p.size()
        x = self.margin
        y = (parentSize.height() - QCustomModals.height()) // 2
        return QPoint(x, y)

    def slideStartPos(self, QCustomModals):
        target_pos = self.modalPosition(QCustomModals)
        return QPoint(target_pos.x() - QCustomModals.width(), target_pos.y())

@QCustomModalsManager.register("center-right")
class CenterRightQCustomModalsManager(QCustomModalsManager):
    def modalPosition(self, QCustomModals, parentSize=None):
        p = QCustomModals.parent()
        if p is None:
            return QCustomModals.pos()
        parentSize = parentSize or p.size()
        x = parentSize.width() - QCustomModals.width() - self.margin
        y = (parentSize.height() - QCustomModals.height()) // 2
        return QPoint(x, y)

    def slideStartPos(self, QCustomModals):
        target_pos = self.modalPosition(QCustomModals)
        return QPoint(target_pos.x() + QCustomModals.width(), target_pos.y())