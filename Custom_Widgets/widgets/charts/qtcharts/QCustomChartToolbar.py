# file name: QCustomChartToolbar.py
from typing import List, Optional, Callable
from qtpy.QtCore import Qt, Signal, QSize
from qtpy.QtWidgets import (
    QWidget, QHBoxLayout, QToolButton, QComboBox, QLabel,
    QSpinBox, QFrame, QPushButton, QMenu, QAction, QStyle
)
from qtpy.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor

from .QCustomChartConstants import QCustomChartConstants


class QCustomChartToolbar(QWidget, QCustomChartConstants):
    """
    Reusable toolbar component for chart controls.
    Provides common chart manipulation tools with customizable buttons.
    """
    
    # Signals
    themeChanged = Signal(str)  # theme name
    legendPositionChanged = Signal(str)  # legend position
    zoomInRequested = Signal()
    zoomOutRequested = Signal()
    resetViewRequested = Signal()
    exportRequested = Signal()
    toggleGrid = Signal(bool)  # grid on/off
    toggleLegend = Signal(bool)  # legend on/off
    toggleCrosshair = Signal(bool)  # crosshair on/off
    toggleTooltips = Signal(bool)  # tooltips on/off
    markerSizeChanged = Signal(float)  # marker size
    animationToggled = Signal(bool)  # animation on/off
    antialiasingToggled = Signal(bool)  # antialiasing on/off
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Toolbar state
        self._showToolbar = True
        self._compactMode = False
        self._customizable = True
        self._availableThemes = []
        self._currentTheme = ""
        self._currentLegendPosition = self.LEGEND_BOTTOM
        
        # Button states
        self._gridVisible = True
        self._legendVisible = True
        self._crosshairVisible = True
        self._tooltipsEnabled = True
        self._animationEnabled = True
        self._antialiasingEnabled = True
        self._markerSize = 8.0
        
        # Widgets
        self._theme_combo = None
        self._legend_position_combo = None
        self._marker_size_spin = None
        self._grid_btn = None
        self._legend_btn = None
        self._crosshair_btn = None
        self._tooltip_btn = None
        self._zoom_in_btn = None
        self._zoom_out_btn = None
        self._reset_view_btn = None
        self._export_btn = None
        self._animation_btn = None
        self._antialiasing_btn = None
        
        # Layout
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(5, 2, 5, 2)
        self._layout.setSpacing(3)
        
        # Create toolbar
        self._createToolbar()
        
        # Set object name for styling
        self.setObjectName("chartToolbar")
    
    def _createToolbar(self):
        """Create the toolbar with all controls"""
        # Clear existing widgets
        while self._layout.count():
            child = self._layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Zoom controls
        self._zoom_in_btn = self._createToolButton("Zoom In", "zoom-in", 
                                                   self._onZoomInClicked)
        self._zoom_out_btn = self._createToolButton("Zoom Out", "zoom-out",
                                                    self._onZoomOutClicked)
        self._reset_view_btn = self._createToolButton("Reset", "reset",
                                                      self._onResetViewClicked)
        
        self._layout.addWidget(self._zoom_in_btn)
        self._layout.addWidget(self._zoom_out_btn)
        self._layout.addWidget(self._reset_view_btn)
        
        # Separator
        self._layout.addWidget(self._createSeparator())
        
        # View toggles
        self._grid_btn = self._createToggleButton("Grid", "grid", 
                                                  self._gridVisible, 
                                                  self._onGridToggled)
        self._legend_btn = self._createToggleButton("Legend", "legend",
                                                    self._legendVisible,
                                                    self._onLegendToggled)
        self._crosshair_btn = self._createToggleButton("Crosshair", "crosshair",
                                                       self._crosshairVisible,
                                                       self._onCrosshairToggled)
        self._tooltip_btn = self._createToggleButton("Tooltips", "tooltip",
                                                     self._tooltipsEnabled,
                                                     self._onTooltipsToggled)
        
        self._layout.addWidget(self._grid_btn)
        self._layout.addWidget(self._legend_btn)
        self._layout.addWidget(self._crosshair_btn)
        self._layout.addWidget(self._tooltip_btn)
        
        # Animation and antialiasing (optional)
        if not self._compactMode:
            self._animation_btn = self._createToggleButton("Anim", "animation",
                                                          self._animationEnabled,
                                                          self._onAnimationToggled)
            self._antialiasing_btn = self._createToggleButton("AA", "antialiasing",
                                                            self._antialiasingEnabled,
                                                            self._onAntialiasingToggled)
            self._layout.addWidget(self._animation_btn)
            self._layout.addWidget(self._antialiasing_btn)
        
        # Separator
        self._layout.addWidget(self._createSeparator())
        
        # Legend position
        legend_label = QLabel("Legend:")
        legend_label.setMaximumWidth(40)
        self._layout.addWidget(legend_label)
        
        self._legend_position_combo = QComboBox()
        self._legend_position_combo.addItems([
            self.LEGEND_TOP,
            self.LEGEND_BOTTOM,
            self.LEGEND_LEFT,
            self.LEGEND_RIGHT,
            self.LEGEND_FLOATING
        ])
        self._legend_position_combo.setCurrentText(self._currentLegendPosition)
        self._legend_position_combo.currentTextChanged.connect(self._onLegendPositionChanged)
        self._legend_position_combo.setMaximumWidth(100)
        self._legend_position_combo.setToolTip("Legend position")
        
        self._layout.addWidget(self._legend_position_combo)
        
        # Separator
        self._layout.addWidget(self._createSeparator())
        
        # Marker size
        if not self._compactMode:
            marker_label = QLabel("Marker:")
            marker_label.setMaximumWidth(40)
            self._layout.addWidget(marker_label)
            
            self._marker_size_spin = QSpinBox()
            self._marker_size_spin.setRange(1, 20)
            self._marker_size_spin.setValue(int(self._markerSize))
            self._marker_size_spin.valueChanged.connect(self._onMarkerSizeChanged)
            self._marker_size_spin.setMaximumWidth(60)
            self._marker_size_spin.setToolTip("Marker size")
            
            self._layout.addWidget(self._marker_size_spin)
        
        # Stretch
        self._layout.addStretch()
        
        # Theme selector
        theme_label = QLabel("Theme:")
        theme_label.setMaximumWidth(40)
        self._layout.addWidget(theme_label)
        
        self._theme_combo = QComboBox()
        self._updateThemeCombo()
        if self._currentTheme and self._currentTheme in self._availableThemes:
            self._theme_combo.setCurrentText(self._currentTheme)
        self._theme_combo.currentTextChanged.connect(self._onThemeChanged)
        self._theme_combo.setMaximumWidth(150)
        self._theme_combo.setToolTip("Chart theme")
        
        self._layout.addWidget(self._theme_combo)
        
        # Stretch
        self._layout.addStretch()
        
        # Export button
        self._export_btn = self._createToolButton("Export", "export",
                                                  self._onExportClicked)
        self._layout.addWidget(self._export_btn)
        
        # Set toolbar height
        self.setMaximumHeight(30)
    
    def _createToolButton(self, text: str, icon_name: str, 
                         callback: Callable) -> QToolButton:
        """Create a tool button with text and optional icon"""
        button = QToolButton()
        button.setText(text)
        button.setToolTip(text)
        button.clicked.connect(callback)
        
        # Try to set icon if available
        icon = self._getIcon(icon_name)
        if icon:
            button.setIcon(icon)
            button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        return button
    
    def _createToggleButton(self, text: str, icon_name: str, 
                           initial_state: bool, 
                           callback: Callable) -> QToolButton:
        """Create a toggle button"""
        button = QToolButton()
        button.setText(text)
        button.setCheckable(True)
        button.setChecked(initial_state)
        button.setToolTip(text)
        button.toggled.connect(callback)
        
        # Try to set icon if available
        icon = self._getIcon(icon_name)
        if icon:
            button.setIcon(icon)
            button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        return button
    
    def _createSeparator(self) -> QFrame:
        """Create a vertical separator"""
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setMaximumWidth(2)
        return separator
    
    def _getIcon(self, icon_name: str) -> Optional[QIcon]:
        """Get icon by name (placeholder - implement actual icon loading)"""
        # This is a placeholder - you should implement proper icon loading
        # based on your application's icon system
        return None
    
    def _onZoomInClicked(self):
        """Handle zoom in button click"""
        self.zoomInRequested.emit()
    
    def _onZoomOutClicked(self):
        """Handle zoom out button click"""
        self.zoomOutRequested.emit()
    
    def _onResetViewClicked(self):
        """Handle reset view button click"""
        self.resetViewRequested.emit()
    
    def _onExportClicked(self):
        """Handle export button click"""
        self.exportRequested.emit()
    
    def _onGridToggled(self, checked: bool):
        """Handle grid toggle"""
        self._gridVisible = checked
        self.toggleGrid.emit(checked)
    
    def _onLegendToggled(self, checked: bool):
        """Handle legend toggle"""
        self._legendVisible = checked
        self.toggleLegend.emit(checked)
    
    def _onCrosshairToggled(self, checked: bool):
        """Handle crosshair toggle"""
        self._crosshairVisible = checked
        self.toggleCrosshair.emit(checked)
    
    def _onTooltipsToggled(self, checked: bool):
        """Handle tooltips toggle"""
        self._tooltipsEnabled = checked
        self.toggleTooltips.emit(checked)
    
    def _onAnimationToggled(self, checked: bool):
        """Handle animation toggle"""
        self._animationEnabled = checked
        self.animationToggled.emit(checked)
    
    def _onAntialiasingToggled(self, checked: bool):
        """Handle antialiasing toggle"""
        self._antialiasingEnabled = checked
        self.antialiasingToggled.emit(checked)
    
    def _onMarkerSizeChanged(self, value: int):
        """Handle marker size change"""
        self._markerSize = float(value)
        self.markerSizeChanged.emit(self._markerSize)
    
    def _onThemeChanged(self, theme: str):
        """Handle theme selection change"""
        self._currentTheme = theme
        self.themeChanged.emit(theme)
    
    def _onLegendPositionChanged(self, position: str):
        """Handle legend position selection change"""
        self._currentLegendPosition = position
        self.legendPositionChanged.emit(position)
    
    def _updateThemeCombo(self):
        """Update theme combo box with available themes"""
        if self._theme_combo:
            self._theme_combo.clear()
            self._theme_combo.addItems(self._availableThemes)
    
    # Public API Methods
    
    def setAvailableThemes(self, themes: List[str]):
        """Set available themes for the theme selector"""
        self._availableThemes = themes
        self._updateThemeCombo()
    
    def getAvailableThemes(self) -> List[str]:
        """Get available themes"""
        return self._availableThemes
    
    def setCurrentTheme(self, theme: str):
        """Set current theme"""
        self._currentTheme = theme
        if self._theme_combo and theme in self._availableThemes:
            self._theme_combo.setCurrentText(theme)
    
    def getCurrentTheme(self) -> str:
        """Get current theme"""
        return self._currentTheme
    
    def setLegendPosition(self, position: str):
        """Set legend position"""
        self._currentLegendPosition = position
        if self._legend_position_combo:
            self._legend_position_combo.setCurrentText(position)
    
    def getLegendPosition(self) -> str:
        """Get legend position"""
        return self._currentLegendPosition
    
    def setGridVisible(self, visible: bool):
        """Set grid visibility"""
        self._gridVisible = visible
        if self._grid_btn:
            self._grid_btn.setChecked(visible)
    
    def isGridVisible(self) -> bool:
        """Check if grid is visible"""
        return self._gridVisible
    
    def setLegendVisible(self, visible: bool):
        """Set legend visibility"""
        self._legendVisible = visible
        if self._legend_btn:
            self._legend_btn.setChecked(visible)
    
    def isLegendVisible(self) -> bool:
        """Check if legend is visible"""
        return self._legendVisible
    
    def setCrosshairVisible(self, visible: bool):
        """Set crosshair visibility"""
        self._crosshairVisible = visible
        if self._crosshair_btn:
            self._crosshair_btn.setChecked(visible)
    
    def isCrosshairVisible(self) -> bool:
        """Check if crosshair is visible"""
        return self._crosshairVisible
    
    def setTooltipsEnabled(self, enabled: bool):
        """Set tooltips enabled"""
        self._tooltipsEnabled = enabled
        if self._tooltip_btn:
            self._tooltip_btn.setChecked(enabled)
    
    def areTooltipsEnabled(self) -> bool:
        """Check if tooltips are enabled"""
        return self._tooltipsEnabled
    
    def setAnimationEnabled(self, enabled: bool):
        """Set animation enabled"""
        self._animationEnabled = enabled
        if self._animation_btn:
            self._animation_btn.setChecked(enabled)
    
    def isAnimationEnabled(self) -> bool:
        """Check if animation is enabled"""
        return self._animationEnabled
    
    def setAntialiasingEnabled(self, enabled: bool):
        """Set antialiasing enabled"""
        self._antialiasingEnabled = enabled
        if self._antialiasing_btn:
            self._antialiasing_btn.setChecked(enabled)
    
    def isAntialiasingEnabled(self) -> bool:
        """Check if antialiasing is enabled"""
        return self._antialiasingEnabled
    
    def setMarkerSize(self, size: float):
        """Set marker size"""
        self._markerSize = size
        if self._marker_size_spin:
            self._marker_size_spin.setValue(int(size))
    
    def getMarkerSize(self) -> float:
        """Get marker size"""
        return self._markerSize
    
    def setCompactMode(self, compact: bool):
        """Set compact mode (hides some controls)"""
        self._compactMode = compact
        self._createToolbar()  # Recreate toolbar with new mode
    
    def isCompactMode(self) -> bool:
        """Check if compact mode is enabled"""
        return self._compactMode
    
    def setCustomizable(self, customizable: bool):
        """Set whether toolbar is customizable"""
        self._customizable = customizable
        # Enable/disable widget editing based on customizable flag
        for widget in self.findChildren((QComboBox, QSpinBox, QToolButton)):
            widget.setEnabled(customizable)
    
    def isCustomizable(self) -> bool:
        """Check if toolbar is customizable"""
        return self._customizable
    
    def addCustomButton(self, text: str, icon_name: str, 
                       callback: Callable, 
                       checkable: bool = False,
                       position: int = -1) -> QToolButton:
        """Add a custom button to the toolbar"""
        if checkable:
            button = self._createToggleButton(text, icon_name, False, callback)
        else:
            button = self._createToolButton(text, icon_name, callback)
        
        if position < 0 or position >= self._layout.count():
            self._layout.insertWidget(self._layout.count() - 2, button)
        else:
            self._layout.insertWidget(position, button)
        
        return button
    
    def removeButton(self, button: QToolButton):
        """Remove a button from the toolbar"""
        self._layout.removeWidget(button)
        button.deleteLater()
    
    def addSeparator(self, position: int = -1):
        """Add a separator to the toolbar"""
        separator = self._createSeparator()
        if position < 0 or position >= self._layout.count():
            self._layout.insertWidget(self._layout.count() - 2, separator)
        else:
            self._layout.insertWidget(position, separator)
    
    def getButton(self, button_type: str) -> Optional[QToolButton]:
        """Get a button by type"""
        button_map = {
            "zoom_in": self._zoom_in_btn,
            "zoom_out": self._zoom_out_btn,
            "reset": self._reset_view_btn,
            "grid": self._grid_btn,
            "legend": self._legend_btn,
            "crosshair": self._crosshair_btn,
            "tooltip": self._tooltip_btn,
            "export": self._export_btn,
            "animation": self._animation_btn,
            "antialiasing": self._antialiasing_btn
        }
        
        return button_map.get(button_type)
    
    def updateButtonTooltip(self, button_type: str, tooltip: str):
        """Update button tooltip"""
        button = self.getButton(button_type)
        if button:
            button.setToolTip(tooltip)
    
    def setButtonVisible(self, button_type: str, visible: bool):
        """Set button visibility"""
        button = self.getButton(button_type)
        if button:
            button.setVisible(visible)
    
    def refresh(self):
        """Refresh toolbar state"""
        self._createToolbar()
    
    def getAvailableLegendPositions(self) -> List[str]:
        """Get available legend positions"""
        return [
            self.LEGEND_TOP,
            self.LEGEND_BOTTOM,
            self.LEGEND_LEFT,
            self.LEGEND_RIGHT,
            self.LEGEND_FLOATING
        ]