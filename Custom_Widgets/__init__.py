## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
import os
import sys
import __main__


from qtpy.QtCore import QCoreApplication, Qt, QSettings, QPoint, QSize, Signal, QEvent
from qtpy.QtGui import QCursor, QPaintEvent,QColor, QMouseEvent, QPainter, QIcon
from qtpy.QtWidgets import QPushButton, QLabel, QTabWidget, QCheckBox, QMainWindow, QWidget, QVBoxLayout, QStyle, QStyleOption, QGraphicsDropShadowEffect, QToolBox

import re

from Custom_Widgets.JSonStyles import loadJsonStyle
from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.Utils import is_in_designer, SharedData

from Custom_Widgets.Log import *
from Custom_Widgets.QCustomComponentLoader import QCustomComponentLoader
from Custom_Widgets.QCustomHamburgerMenu import QCustomHamburgerMenu
from Custom_Widgets.FileMonitor import QSsFileMonitor

script_dir = os.path.dirname(os.path.abspath(sys.argv[0])).replace("\\", "/")

class QMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.clickPosition = None  
        self.normalGeometry = self.geometry()
        self.iconsWorker = None
        self.allIconsWorker = None
        
        self.orginazationName = ""
        self.applicationName = ""
        self.orginazationDomain = ""

        self._border_width = 5 #for resizing
        self.borderWidth = self._border_width
        self._is_resizing = False
        self._margin_applied = False
        self._shadow_applied = False

        self.themeEngine =  QCustomTheme()
        self.themeEngine.onThemeChanged.connect(self.applyThemeIcons)
        self._init_theme_name = self.themeEngine.theme

        self.themeEngine.sassCompilationProgress = self.sassCompilationProgress

        self.shared_data = SharedData()
        self.qss_watcher = None

        self._win_restored = False
        self._loaded_side_drawers = set()
        self._loaded_side_drawer_files = set()
        self._custom_side_drawers = ""

        self.customSideDrawers = ""

        self._qss_file_monitor = QSsFileMonitor.instance()
        self.qss_watcher = None
        self.liveCompileQss = False
        self._qss_file_monitor.start_qss_file_listener(self.themeEngine)

    def saveGeometryToSettings(self):
        """Save the current window geometry (position and size) to settings."""
        self.settings = QSettings()
        self.settings.setValue("window/size", self.size())
        self.settings.setValue("window/position", self.pos())
        self.settings.setValue("window/state", self.isMaximized())


    def loadGeometryFromSettings(self):
        """Load and apply the saved window geometry (position and size) from settings."""
        # Get saved size and position
        if self._win_restored:
            return
        try:
            self._win_restored = True

            self.settings = QSettings()
            size = self.settings.value("window/size")  # Default size if not saved
            position = self.settings.value("window/position")  # Default position if not saved
            state = self.settings.value("window/state")  

            # Apply saved geometry
            # self.resize(size)
            # self.move(position)

            # if state:
            #     self.showMaximized()

        except:
            self._win_restored = False

    def sassCompilationProgress(self, n):
        pass

    @property
    def themes(self):
        self.themeEngine =  QCustomTheme()
        return self.themeEngine.themes

    def applyThemeIcons(self):
        if hasattr(self, "ui"):
            try:
                # Check the module name where ui is loaded from
                self.ui_module_name = self.ui.__module__.split('.')[-1]

                # Replace "ui_" with empty string only at the start
                if self.ui_module_name.startswith("ui_"):
                    self.ui_module_name = self.ui_module_name[len("ui_"):]

            except Exception as e:
                self.ui_module_name = ""
                logException(e)

            try:
                self.themeEngine.applyIcons(self.ui, ui_file_name=self.ui_module_name)

            except Exception as e:
                logException(e, "Error loading theme icons for : "+ str(self.ui))
                
            self.restyleAllButtonGroups()

        # Also update side drawers if any
        self.reloadCustomSideDrawersThemeIcons()

    # Update restore button icon on maximizing or minimizing window
    def updateRestoreButtonIcon(self):
        normal_color = self.themeEngine.iconsColor
        icons_folder = normal_color.replace("#", "")

        prefix_to_remove = re.compile(r'^Qss/icons/[^/]+/')
        self.maximizedIcon = re.sub(prefix_to_remove, 'Qss/icons/'+icons_folder+'/', self.maximizedIcon)
        self.normalIcon = re.sub(prefix_to_remove, 'Qss/icons/'+icons_folder+'/', self.normalIcon)

        # If window is maxmized
        if self.isMaximized():
            # Change Iconload
            if len(str(self.maximizedIcon)) > 0:
                # self.restoreBtn.setIcon(QtGui.QIcon(str(self.maximizedIcon)))
                self.restoreBtn.setNewIcon(str(self.maximizedIcon))
        else:
            # Change Icon
            if len(str(self.normalIcon)) > 0:
                # self.restoreBtn.setIcon(QtGui.QIcon(str(self.normalIcon)))
                self.restoreBtn.setNewIcon(str(self.normalIcon))

    def restore_or_maximize_window(self):
        self.toggleWindowSize("")

    # Function to Move window on mouse drag event on the tittle bar
    def moveWindow(self, e):
        # Detect if the window is  normal size
        if not self.isMaximized(): #Not maximized
            # Move window only when window is normal size
            #if left mouse button is clicked (Only accept left mouse button clicks)
            if e.buttons() == Qt.LeftButton:
                #Move window
                if self.clickPosition is not None:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

            self.normalGeometry = self.geometry()
        # else:
        #     self.showNormal()

        self.saveGeometryToSettings()

    def toggleWindowSize(self, e):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

        self.updateRestoreButtonIcon()
        self.updateProperties()

    def updateProperties(self):
        if self.isMaximized():
            self.setProperty("window-state", "maximized")
        else:
            self.setProperty("window-state", "normal")

        self.style().unpolish(self) 
        self.style().polish(self) 

    ## Check Button Groups
    def checkButtonGroup(self, button = None):
        if self.sender() is not None:
            btn = self.sender()
        else:
            btn = button
                
        group = btn.group
        groupBtns = getattr(self, "group_btns_"+str(group))
        active = getattr(self, "group_active_"+str(group))
        notActive = getattr(self, "group_not_active_"+str(group))

        for x in groupBtns:
            if x == btn and self.sender() is not None:
                x.setStyleSheet(self.themeEngine.styleVariablesFromTheme(active))
                x.active = True

            elif  x.active and self.sender() is None:
                x.setStyleSheet(self.themeEngine.styleVariablesFromTheme(active))
                x.active = True

            else:
                x.setStyleSheet(self.themeEngine.styleVariablesFromTheme(notActive))
                x.active = False

    def restyleAllButtonGroups(self):
        """
        Loop through all button groups and reapply active/inactive styles based on the theme.
        """
        # Iterate over each group number, assuming groups are counted as integers from 1
        grp_count = 1
        while hasattr(self, f"group_btns_{grp_count}"):
            group_buttons = getattr(self, f"group_btns_{grp_count}")
            active_style = getattr(self, f"group_active_{grp_count}", "")
            not_active_style = getattr(self, f"group_not_active_{grp_count}", "")

            # Apply styles for each button based on its active state
            for btn in group_buttons:
                if btn.active:
                    btn.setStyleSheet(self.themeEngine.styleVariablesFromTheme(active_style))
                else:
                    btn.setStyleSheet(self.themeEngine.styleVariablesFromTheme(not_active_style))
            
            grp_count += 1  # Move to the next group
    
    def loadCustomSideDrawers(self):
        """Load QCustomHamburgerMenu from customSideDrawers list."""
        _custom_side_drawers = [f.strip() for f in self.customSideDrawers.split(",") if f.strip()]
        
        if is_in_designer(self):
            return
        
        for drawer_file in _custom_side_drawers:
            if drawer_file in self._loaded_side_drawer_files:
                continue
                
            try:
                # Create component loader
                component_loader = QCustomComponentLoader(self)
                component_loader.previewComponent = True
                component_loader.loadComponent(filePath=drawer_file)

                component_loader.setMaximumSize(QSize(0, 0))
                # remove margins
                component_loader.layout().setContentsMargins(0, 0, 0, 0)
                # Add the loader widget to layout
                self.centralWidget().layout().addWidget(component_loader)

                # Store reference
                if component_loader.ui:
                    component_loader.form = component_loader.ui
                    component_loader.shownForm = component_loader.ui
                    component_loader.component = component_loader.ui
                
                # Search for QCustomHamburgerMenu in the component loader
                hamburger_menu = self._findHamburgerMenu(component_loader)
                if hamburger_menu:
                    self._reparentHamburgerMenu(hamburger_menu)
                    self._loaded_side_drawers.add(component_loader)
                else:
                    logWarning(f"No QCustomHamburgerMenu found in loaded side drawers, file: {drawer_file}, container: {component_loader.objectName()}")
                
                self._loaded_side_drawer_files.add(drawer_file)
                
                component_loader.hide()

            except Exception as e:
                logError(f"Failed to load side drawer {drawer_file}: {str(e)}")
                    
    def reloadCustomSideDrawersThemeIcons(self):
        """Reload theme icons for all loaded side drawers."""
        for drawer in self._loaded_side_drawers:
            try:
                # drawer.themeEngine = self.themeEngine
                drawer.applyThemeIcons()
            except Exception as e:
                logError(f"Failed to reload theme icons for side drawer {drawer.objectName()}: {str(e)}")
                
    def _findHamburgerMenu(self, root_widget):
        """
        Recursively search for QCustomHamburgerMenu widget.
        Returns the first top-level hamburger menu found.
        """
        # Check if root widget itself is a hamburger menu
        if isinstance(root_widget, QCustomHamburgerMenu):
            return root_widget
        
        # Search through all child widgets recursively
        def search_children(widget):
            for child in widget.children():
                if isinstance(child, QCustomHamburgerMenu):
                    return child
                # Recursively search deeper
                result = search_children(child)
                if result:
                    return result
            return None
        
        return search_children(root_widget)

    def getHamburgerMenu(self, name: str) -> QCustomHamburgerMenu:
        try:
            # Validate input
            if not name or not isinstance(name, str):
                raise ValueError("Hamburger menu name must be a non-empty string")
            
            # Search in central widget first
            hamburger = self.centralWidget().findChild(QCustomHamburgerMenu, name)
            
            # If not found, search recursively through all widgets
            if not hamburger:
                hamburger = self.findChild(QCustomHamburgerMenu, name)
            
            if not hamburger:
                logWarning(f"Hamburger menu '{name}' not found")
                return None
                
            return hamburger
            
        except ValueError as e:
            logError(f"Invalid hamburger menu name: {e}")
            raise
        except Exception as e:
            logError(f"Unexpected error while finding hamburger menu '{name}': {str(e)}")
            return None
    
    def getHamburgerWidget(self, menu_name: str, widget_name: str) -> QWidget:
        hamburger = self.getHamburgerMenu(menu_name)
        if hamburger:
            return hamburger.getWidget(widget_name)
        return None

    
    def _reparentHamburgerMenu(self, hamburger_menu):
        """
        Reparent hamburger menu to central widget and remove from any layout.
        """
        hamburger_menu.hide()
        # Store current geometry and properties
        old_geometry = hamburger_menu.geometry()
        old_parent = hamburger_menu.parent()
        # Remove from any existing layout
        # if old_parent and old_parent.layout():
        #     old_parent.layout().removeWidget(hamburger_menu)
        
        # # Reparent to central widget
        hamburger_menu.setParent(self.centralWidget())
        
        # Restore geometry and ensure it's visible
        hamburger_menu.setGeometry(old_geometry)
        hamburger_menu.raise_()
        hamburger_menu.show()
    

    def showEvent(self, e: QEvent):
        super().showEvent(e)
        self.updateProperties()
        self.applyThemeIcons()
        try:
            self.borderWidth = self._border_width - self.shadowBlurRadius * 2.2
        except:
            pass

        self.applyBorderRadius()
        self.restyleAllButtonGroups()
        
        self.loadCustomSideDrawers()


    def resizeEvent(self, e: QEvent):
        self.saveGeometryToSettings()
        super().resizeEvent(e)
        # self.applyBorderRadius()
        self.update()

    def moveEvent(self, e: QEvent):
        self.applyBorderRadius()
        super().moveEvent(e)
        self.saveGeometryToSettings()
    
    def paintEvent(self, e: QPaintEvent):
        super().paintEvent(e)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        # self.applyBorderRadius()

        centralWidget = self.centralWidget()
        centralWidget.setGeometry(
            (self.width() - centralWidget.width()) // 2,
            (self.height() - centralWidget.height()) // 2,
            centralWidget.width(),
            centralWidget.height()
        )

        if self._init_theme_name != self.themeEngine.theme:
            self._init_theme_name = self.themeEngine.theme
            self.applyThemeIcons()
            self.loadGeometryFromSettings() #assumed its being shown for the first time

        
    # Override the changeEvent method
    def changeEvent(self, event):
        # Check if the event is a window state change
        if event.type() == QEvent.WindowStateChange:
            self.applyBorderRadius()
            self.saveGeometryToSettings()

        # Call the base class implementation
        super().changeEvent(event)

    def applyBorderRadius(self):
        if self.isFrameless():
            try:
                if self.centralWidget():
                    centralWidget = self.centralWidget()
                    layout = centralWidget.layout()
                    name = centralWidget.objectName()

                    # self.layout().setAlignment(centralWidget, Qt.AlignCenter)
                    
                    if self.isMaximized():
                        self.layout().setContentsMargins(0, 0, 0, 0)
                        layout.setContentsMargins(0, 0, 0, 0)

                        centralWidget.setMaximumSize(self.width(), self.height())

                        self._margin_applied = False

                        self.centralWidget().setGraphicsEffect(None)

                    else:
                        centralWidget.setMaximumSize(self.width() - self.shadowBlurRadius * 2.2, self.height() - self.shadowBlurRadius * 2.2)
                        if not self._margin_applied:
                            top = self.height() - self.shadowBlurRadius * 2.2
                            left = self.width() - centralWidget.width() // 2

                            self.layout().setContentsMargins(40, 40, 40, 40)
                            layout.setContentsMargins(self.borderRadius * .7, self.borderRadius * .7, self.borderRadius * .7, self.borderRadius * .7)

                            self._margin_applied = True

                        if not self._shadow_applied:
                            self.applyDropShadow()
                            self._shadow_applied = True

            except Exception as e:
                print(e)

        self.update()

    def applyDropShadow(self):
        self.centralWidget().setGraphicsEffect(None)
        self.shadow = QGraphicsDropShadowEffect(self)
        if self.shadowBlurRadius > 0:
            self.shadow.setColor(QColor(self.shadowColor))
            self.shadow.setBlurRadius(self.shadowBlurRadius)
            self.shadow.setXOffset(self.shadowXOffset)
            self.shadow.setYOffset(self.shadowYOffset)

            ## # Appy shadow to central widget
            self.centralWidget().setGraphicsEffect(self.shadow)

        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
        # We will use this value to move the window
        # Hide floating widgets
        cursor = QCursor()
        xPos = cursor.pos().x()
        yPos = cursor.pos().y()
        # if hasattr(self, "floatingWidgets"):
        #     for x in self.floatingWidgets:
        #         if hasattr(x, "autoHide") and x.autoHide:
        #             x.collapseMenu()

        if not self.isFrameless():
            return
        
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPosition().toPoint()
            self._resize_direction = self._detect_resize_direction(event.position().toPoint())
            if self._resize_direction:
                self._is_resizing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.isFrameless():
            return

        if self.isMaximized():
            self.borderWidth = self._border_width
        else:
            self.borderWidth = self._border_width + self.shadowBlurRadius
        
        self._update_cursor(event.position().toPoint())

        if self._is_resizing:
            self._resize_window(event)
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._is_resizing = False
            self._resize_direction = None
            self.unsetCursor()

    def _detect_resize_direction(self, pos: QPoint):
        rect = self.rect()
        if pos.x() < self.borderWidth:
            if pos.y() < self.borderWidth:
                return "top_left"
            elif pos.y() > rect.height() - self.borderWidth:
                return "bottom_left"
            else:
                return "left"
        elif pos.x() > rect.width() - self.borderWidth:
            if pos.y() < self.borderWidth:
                return "top_right"
            elif pos.y() > rect.height() - self.borderWidth:
                return "bottom_right"
            else:
                return "right"
        elif pos.y() < self.borderWidth:
            return "top"
        elif pos.y() > rect.height() - self.borderWidth:
            return "bottom"
        else:
            return None

    def _update_cursor(self, pos: QPoint):
        direction = self._detect_resize_direction(pos)
        if direction in ["left", "right"]:
            self.setCursor(Qt.SizeHorCursor)
        elif direction in ["top", "bottom"]:
            self.setCursor(Qt.SizeVerCursor)
        elif direction in ["top_left", "bottom_right"]:
            self.setCursor(Qt.SizeFDiagCursor)
        elif direction in ["top_right", "bottom_left"]:
            self.setCursor(Qt.SizeBDiagCursor)
        else:
            self.unsetCursor()

    def _resize_window(self, event: QMouseEvent):
        # self._update_cursor(event.position().toPoint())
        if self._resize_direction:
            rect = self.geometry()
            delta = event.globalPosition().toPoint() - self._drag_position
            if self._resize_direction == "left":
                rect.setLeft(rect.left() + delta.x())
            elif self._resize_direction == "right":
                rect.setRight(rect.right() + delta.x())
            elif self._resize_direction == "top":
                rect.setTop(rect.top() + delta.y())
            elif self._resize_direction == "bottom":
                rect.setBottom(rect.bottom() + delta.y())
            elif self._resize_direction == "top_left":
                rect.setTopLeft(rect.topLeft() + delta)
            elif self._resize_direction == "top_right":
                rect.setTopRight(rect.topRight() + delta)
            elif self._resize_direction == "bottom_left":
                rect.setBottomLeft(rect.bottomLeft() + delta)
            elif self._resize_direction == "bottom_right":
                rect.setBottomRight(rect.bottomRight() + delta)

            self.setGeometry(rect)
            self._drag_position = event.globalPosition().toPoint()
        
    def isFrameless(window: QMainWindow) -> bool:
        return bool(window.windowFlags() & Qt.FramelessWindowHint)

def mouseReleaseEvent(self, QMouseEvent):
    cursor = QCursor()
    # self.ui.frame.setGeometry(QRect(cursor.pos().x(), cursor.pos().y(), 151, 111))


