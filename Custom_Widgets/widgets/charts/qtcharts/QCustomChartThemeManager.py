# file name: QCustomChartThemeManager.py
from typing import List, Optional, Dict, Any
from qtpy.QtCore import Qt, Signal, QObject, QTimer
from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QColor, QPalette, QBrush, QLinearGradient, QPen
from qtpy.QtCharts import QChart

from .QCustomChartConstants import QCustomChartConstants
from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.Log import logInfo, logWarning, logError

from .QCustomChartConstants import QCustomChartConstants

class QCustomChartThemeManager(QObject, QCustomChartConstants):
    """
    Centralized theme manager for chart components.
    Handles theme switching, palette management, and theme-aware styling.
    Integrates with QCustomTheme from Custom_Widgets module.
    """
    # Signals
    themeChanged = Signal(str)  # New theme name
    themeApplied = Signal(str)  # Theme name after application
    paletteChanged = Signal(QPalette)  # When palette changes
    refreshRequested = Signal()  # Request to refresh theme
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Theme properties
        self._currentTheme = self.THEME_APP_THEME  # Use imported constant
        self._customPalette = None
        self._themeCache = {}
        
        # Theme mapping to QChart themes
        self._chartThemeMapping = {
            self.THEME_LIGHT: QChart.ChartThemeLight,
            self.THEME_DARK: QChart.ChartThemeDark,
            self.THEME_BLUE_NCS: QChart.ChartThemeBlueNcs,
            self.THEME_BLUE_ICY: QChart.ChartThemeBlueIcy,
            self.THEME_HIGH_CONTRAST: QChart.ChartThemeHighContrast,
            self.THEME_QT_LIGHT: QChart.ChartThemeQt,
            self.THEME_QT_DARK: QChart.ChartThemeDark,
            self.THEME_QT_BROWN_SAND: QChart.ChartThemeBrownSand
        }
        
        # Initialize theme system
        self._appTheme = QCustomTheme()
        self._appTheme.onThemeChanged.connect(self._onAppThemeChanged)
        self._appTheme.onThemeChangeComplete.connect(self._onAppThemeChangeComplete)
        
        # Initialize with default settings
        # self._setupDefaultThemes()
    
    def _setupDefaultThemes(self):
        """Setup default theme configurations"""
        # Default colors for each theme
        self._themeCache = {
            self.THEME_APP_THEME: {
                "background": QColor(0, 0, 0, 0),
                "plot_area": QColor(255, 255, 255),
                "text": QColor(0, 0, 0),
                "grid": QColor(200, 200, 200, 100),
                "highlight": QColor(0, 120, 215),
                "crosshair": QColor(0, 0, 0, 180)
            },
            self.THEME_LIGHT: {
                "background": QColor(255, 255, 255),
                "text": QColor(0, 0, 0),
                "grid": QColor(200, 200, 200),
                "highlight": QColor(0, 120, 215)
            },
            self.THEME_DARK: {
                "background": QColor(30, 30, 30),
                "text": QColor(255, 255, 255),
                "grid": QColor(80, 80, 80),
                "highlight": QColor(0, 180, 255)
            }
        }
    
    def _onAppThemeChanged(self):
        """Handle app theme changes"""
        logInfo("App theme changed, refreshing chart theme")
        if self._currentTheme == self.THEME_APP_THEME:
            self.refreshRequested.emit()
    
    def _onAppThemeChangeComplete(self):
        """Handle app theme change completion"""
        logInfo("App theme change complete, applying to chart")
        if self._currentTheme == self.THEME_APP_THEME:
            self.refreshRequested.emit()
    
    def setTheme(self, theme_name: str):
        """Set the current theme"""
        if theme_name != self._currentTheme:
            self._currentTheme = theme_name
            self.themeChanged.emit(theme_name)
            # Don't call applyTheme() here - let the caller do it
            # This prevents circular calls when toolbar triggers theme change
    
    def getTheme(self) -> str:
        """Get the current theme name"""
        return self._currentTheme
    
    def getAvailableThemes(self) -> List[str]:
        """Get list of available theme names"""
        return list(self._chartThemeMapping.keys()) + [self.THEME_APP_THEME]
    
    def applyTheme(self, chart: Optional[QChart] = None):
        """Apply the current theme to a chart"""
        try:
            theme_name = self._currentTheme
            
            if chart:
                if theme_name == self.THEME_APP_THEME:
                    self._applyAppTheme(chart)
                elif theme_name in self._chartThemeMapping:
                    chart_theme = self._chartThemeMapping[theme_name]
                    chart.setTheme(chart_theme)
                else:
                    # Fallback to Light theme
                    chart.setTheme(QChart.ChartThemeLight)
            
            self.themeApplied.emit(theme_name)
            
        except Exception as e:
            logError(f"Error applying theme {self._currentTheme}: {e}")
            # Fallback to default
            if chart:
                chart.setTheme(QChart.ChartThemeLight)
    
    def _applyAppTheme(self, chart: QChart):
        """Apply App Theme based on QCustomTheme theme variables"""
        if not chart:
            return
        
        # Clear any existing theme
        chart.setTheme(QChart.ChartThemeLight)  # Start with a clean slate
        
        # Use theme variables directly from QCustomTheme
        if self._appTheme.isThemeDark:
            chart.setTheme(QChart.ChartThemeDark)
        else:
            chart.setTheme(QChart.ChartThemeLight)

        # Get theme variable values directly
        try:
            # Background colors - use COLOR_BACKGROUND_1
            bg_color_1 = QColor(self._appTheme.COLOR_BACKGROUND_1)
            bg_color_3 = QColor(self._appTheme.COLOR_BACKGROUND_3)
            text_color_1 = QColor(self._appTheme.COLOR_TEXT_1)
            accent_color_1 = QColor(self._appTheme.COLOR_ACCENT_1)
            
        except Exception as e:
            logError(f"Error accessing theme variables: {e}")
            # Fallback to palette if theme variables not available
            palette = self._appTheme.getPalette()
            bg_color_1 = palette.color(QPalette.Window)
            bg_color_3 = palette.color(QPalette.Base)
            text_color_1 = palette.color(QPalette.Text)
            accent_color_1 = palette.color(QPalette.Highlight)
        
        # Set background to COLOR_BACKGROUND_1
        chart.setBackgroundBrush(QBrush(bg_color_1))
        
        # Set plot area background to COLOR_BACKGROUND_3 (slightly different shade)
        chart.setPlotAreaBackgroundBrush(QBrush(bg_color_3))
        chart.setPlotAreaBackgroundVisible(True)
        
        # Set title color to COLOR_TEXT_1
        title_font = chart.titleFont()
        title_font.setBold(True)
        chart.setTitleFont(title_font)
        
        # Apply theme variables to axes
        for axis in chart.axes():
            axis.setTitleBrush(QBrush(text_color_1))
            axis.setLabelsBrush(QBrush(text_color_1))
            axis.setLinePenColor(text_color_1)
            
            # Set grid color with transparency using COLOR_TEXT_1
            grid_color = QColor(text_color_1)
            grid_color.setAlpha(100)
            axis.setGridLineColor(grid_color)
        
        # Apply to legend
        legend = chart.legend()
        if legend:
            legend.setLabelColor(text_color_1)
            legend.setBackgroundVisible(True)
            legend.setBrush(QBrush(bg_color_1))
            legend.setPen(QPen(bg_color_3))
        
        logInfo(f"Applied App Theme (Dark: {self._appTheme.isThemeDark}) to chart using theme variables")
    
    def applyCustomPalette(self, chart: QChart, palette: QPalette):
        """Apply a custom palette to the chart (for App Theme)"""
        if self._currentTheme != self.THEME_APP_THEME:
            return
        
        self._customPalette = palette
        
        chart.setBackgroundBrush(QBrush(palette.color(QPalette.Window)))
        chart.setPlotAreaBackgroundBrush(QBrush(palette.color(QPalette.Base)))
        
        text_color = palette.color(QPalette.Text)
        
        for axis in chart.axes():
            axis.setLinePenColor(text_color)
            axis.setLabelsColor(text_color)
            axis.setTitleBrush(QBrush(text_color))
            
            grid_color = text_color
            grid_color.setAlpha(80)
            axis.setGridLineColor(grid_color)
            
            if hasattr(axis, 'setMinorGridLineColor'):
                minor_grid_color = text_color
                minor_grid_color.setAlpha(40)
                axis.setMinorGridLineColor(minor_grid_color)
        
        legend = chart.legend()
        if legend:
            legend.setLabelColor(text_color)
        
        logInfo("Applied custom palette to chart")
    
    def getCrosshairColor(self, theme_name: Optional[str] = None) -> QColor:
        """Get appropriate crosshair color for a theme"""
        if theme_name is None:
            theme_name = self._currentTheme
        
        if theme_name == self.THEME_APP_THEME:
            # Use COLOR_TEXT_1 directly from theme
            try:
                text_color = QColor(self._appTheme.COLOR_TEXT_1)
                crosshair_color = QColor(text_color)
                crosshair_color.setAlpha(200)
                return crosshair_color
            except Exception:
                # Fallback
                return QColor(0, 0, 0, 200)
        
        if theme_name in [self.THEME_DARK, self.THEME_QT_DARK]:
            # Dark themes - use light crosshair
            return QColor(255, 255, 255, 200)
        else:
            # Light themes - use dark crosshair
            return QColor(0, 0, 0, 200)
    
    def getTextColor(self, theme_name: Optional[str] = None) -> QColor:
        """Get text color for a theme"""
        if theme_name is None:
            theme_name = self._currentTheme
        
        if theme_name == self.THEME_APP_THEME:
            # Use COLOR_TEXT_1 directly from theme
            try:
                return QColor(self._appTheme.COLOR_TEXT_1)
            except Exception:
                return QColor(0, 0, 0)
        
        if theme_name in [self.THEME_DARK, self.THEME_QT_DARK]:
            return QColor(255, 255, 255)
        else:
            return QColor(0, 0, 0)
    
    def getBackgroundColor(self, theme_name: Optional[str] = None) -> QColor:
        """Get background color for a theme"""
        if theme_name is None:
            theme_name = self._currentTheme
        
        if theme_name == self.THEME_APP_THEME:
            # Use COLOR_BACKGROUND_1 directly from theme
            try:
                return QColor(self._appTheme.COLOR_BACKGROUND_1)
            except Exception:
                return QColor(255, 255, 255)
        
        if theme_name in [self.THEME_DARK, self.THEME_QT_DARK]:
            return QColor(30, 30, 30)
        else:
            return QColor(255, 255, 255)
    
    def getGridColor(self, theme_name: Optional[str] = None) -> QColor:
        """Get grid color for a theme"""
        if theme_name is None:
            theme_name = self._currentTheme
        
        if theme_name == self.THEME_APP_THEME:
            # Use COLOR_TEXT_1 with transparency
            try:
                text_color = QColor(self._appTheme.COLOR_TEXT_1)
                grid_color = QColor(text_color)
                grid_color.setAlpha(100)
                return grid_color
            except Exception:
                return QColor(200, 200, 200, 150)
        
        if theme_name in [self.THEME_DARK, self.THEME_QT_DARK]:
            return QColor(80, 80, 80, 150)
        else:
            return QColor(200, 200, 200, 150)
    
    def getHighlightColor(self, theme_name: Optional[str] = None) -> QColor:
        """Get highlight/selection color for a theme"""
        if theme_name is None:
            theme_name = self._currentTheme
        
        if theme_name == self.THEME_APP_THEME:
            # Use COLOR_ACCENT_1 directly from theme
            try:
                return QColor(self._appTheme.COLOR_ACCENT_1)
            except Exception:
                return QColor(0, 120, 215)
        
        if theme_name in [self.THEME_DARK, self.THEME_QT_DARK]:
            return QColor(0, 180, 255)
        else:
            return QColor(0, 120, 215)
    
    def isDarkTheme(self, theme_name: Optional[str] = None) -> bool:
        """Check if a theme is dark"""
        if theme_name is None:
            theme_name = self._currentTheme
        
        if theme_name == self.THEME_APP_THEME:
            # Use _isThemeDark from QCustomTheme
            try:
                return self._appTheme._isThemeDark
            except Exception:
                # Fallback: check brightness of COLOR_BACKGROUND_1
                try:
                    bg_color = QColor(self._appTheme.COLOR_BACKGROUND_1)
                    return bg_color.lightness() < 128
                except Exception:
                    return False
        
        return theme_name in [self.THEME_DARK, self.THEME_QT_DARK]
    
    def refresh(self):
        """Refresh the current theme"""
        logInfo(f"Refreshing chart theme: {self._currentTheme}")
        self.refreshRequested.emit()
    
    def setThemeColor(self, theme_name: str, color_type: str, color: QColor):
        """Set a custom color for a specific theme and color type"""
        if theme_name not in self._themeCache:
            self._themeCache[theme_name] = {}
        
        self._themeCache[theme_name][color_type] = color
        logInfo(f"Set custom color {color_type} = {color.name()} for theme {theme_name}")
    
    def getThemeColor(self, theme_name: str, color_type: str) -> Optional[QColor]:
        """Get a color for a specific theme and color type"""
        if theme_name in self._themeCache and color_type in self._themeCache[theme_name]:
            return self._themeCache[theme_name][color_type]
        return None
    
    def createGradient(self, start_color: QColor, end_color: QColor, 
                      direction: Qt.Orientation = Qt.Vertical):
        """Create a gradient for chart backgrounds"""
        gradient = QLinearGradient()
        
        if direction == Qt.Vertical:
            gradient.setStart(0, 0)
            gradient.setFinalStop(0, 1)
        else:
            gradient.setStart(0, 0)
            gradient.setFinalStop(1, 0)
        
        gradient.setColorAt(0, start_color)
        gradient.setColorAt(1, end_color)
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        
        return gradient
    
    def getChartThemeEnum(self, theme_name: Optional[str] = None) -> QChart.ChartTheme:
        """Get QChart.ChartTheme enum for a theme name"""
        if theme_name is None:
            theme_name = self._currentTheme
        
        if theme_name in self._chartThemeMapping:
            return self._chartThemeMapping[theme_name]
        
        # Default to Light theme
        return QChart.ChartThemeLight
    
    def createCustomTheme(self, name: str, colors: Dict[str, QColor], 
                         chart_theme: Optional[QChart.ChartTheme] = None):
        """Create a custom theme with specific colors"""
        self._themeCache[name] = colors
        if chart_theme:
            self._chartThemeMapping[name] = chart_theme
        logInfo(f"Created custom theme: {name}")
    
    def removeCustomTheme(self, name: str):
        """Remove a custom theme"""
        if name in self._themeCache:
            del self._themeCache[name]
        if name in self._chartThemeMapping:
            del self._chartThemeMapping[name]
        logInfo(f"Removed custom theme: {name}")
    
    def getThemeInfo(self, theme_name: str) -> Dict[str, Any]:
        """Get detailed information about a theme"""
        info = {
            "name": theme_name,
            "is_dark": self.isDarkTheme(theme_name),
            "is_custom": theme_name not in self.getAvailableThemes(),
            "has_chart_theme": theme_name in self._chartThemeMapping,
            "colors": {}
        }
        
        # Get all color types
        color_types = ["text", "background", "grid", "highlight", "crosshair"]
        for color_type in color_types:
            color = self.getThemeColor(theme_name, color_type)
            if color:
                info["colors"][color_type] = color
        
        return info
    
    def syncWithAppTheme(self):
        """Sync with application theme (for App Theme mode)"""
        if self._currentTheme == self.THEME_APP_THEME:
            logInfo("Syncing chart theme with app theme")
            self.refresh()
    
    def getAppTheme(self):
        """Get the QCustomTheme instance"""
        return self._appTheme
    
    def isAppThemeAvailable(self) -> bool:
        """Check if QCustomTheme is available"""
        return self._appTheme is not None and hasattr(self._appTheme, 'isThemeDark')
    
    def logThemeInfo(self):
        """Log information about current theme"""
        theme_info = self.getThemeInfo(self._currentTheme)
        logInfo(f"Current Theme: {self._currentTheme}")
        logInfo(f"Is Dark: {theme_info['is_dark']}")
        logInfo(f"App Theme Available: {self.isAppThemeAvailable()}")
        if self.isAppThemeAvailable():
            logInfo(f"App Theme Dark: {self._appTheme.isThemeDark}")