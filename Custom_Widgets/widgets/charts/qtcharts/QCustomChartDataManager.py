# file name: QCustomChartDataManager.py
import random
import math
from typing import List, Tuple, Dict, Any, Optional, Union
from qtpy.QtCore import QObject, Signal
from qtpy.QtGui import QColor

from .QCustomChartConstants import QCustomChartConstants


class QCustomChartDataManager(QObject, QCustomChartConstants):
    """
    Data management system for chart series.
    Handles data storage, validation, and series configuration.
    """
    
    # Signals
    dataChanged = Signal(str)  # series name that changed
    seriesAdded = Signal(str)  # series name added
    seriesRemoved = Signal(str)  # series name removed
    seriesVisibilityChanged = Signal(str, bool)  # series name, visible
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Data storage
        self._seriesData = {}  # {series_name: [(x1, y1), (x2, y2), ...]}
        self._seriesColors = {}  # {series_name: QColor}
        self._seriesVisible = {}  # {series_name: bool}
        
        # Style storage
        self._seriesLineStyles = {}  # {series_name: str} e.g., "solid", "dash"
        self._seriesLineWidths = {}  # {series_name: float}
        self._seriesMarkerStyles = {}  # {series_name: str} e.g., "circle", "none"
        self._seriesMarkerSizes = {}  # {series_name: float}
        
        # Default values
        self._defaultColor = QColor("#00bcff")
        self._defaultLineStyle = self.LINE_SOLID
        self._defaultLineWidth = 2.0
        self._defaultMarkerStyle = self.MARKER_NONE
        self._defaultMarkerSize = 8.0
        self._defaultVisible = True
    
    # ============ DATA MANAGEMENT METHODS ============
    
    def addSeries(self, name: str, data: List[Tuple[float, float]], 
                 color: Optional[QColor] = None,
                 visible: Optional[bool] = None,
                 line_style: Optional[str] = None,
                 line_width: Optional[float] = None,
                 marker_style: Optional[str] = None,
                 marker_size: Optional[float] = None) -> bool:
        """
        Add a new series to the data manager.
        
        Args:
            name: Unique series name
            data: List of (x, y) tuples
            color: Optional series color
            visible: Optional visibility
            line_style: Optional line style
            line_width: Optional line width
            marker_style: Optional marker style
            marker_size: Optional marker size
            
        Returns:
            bool: True if added successfully, False if series already exists
        """
        if name in self._seriesData:
            return False  # Series already exists
        
        # Validate data
        if not self._validateData(data):
            raise ValueError("Invalid data format")
        
        # Store data
        self._seriesData[name] = data.copy()
        
        # Store properties with defaults
        self._seriesColors[name] = color if color else self._getNextColor(len(self._seriesData))
        self._seriesVisible[name] = visible if visible is not None else self._defaultVisible
        self._seriesLineStyles[name] = line_style if line_style else self._defaultLineStyle
        self._seriesLineWidths[name] = line_width if line_width else self._defaultLineWidth
        self._seriesMarkerStyles[name] = marker_style if marker_style else self._defaultMarkerStyle
        self._seriesMarkerSizes[name] = marker_size if marker_size else self._defaultMarkerSize
        
        # Emit signal
        self.seriesAdded.emit(name)
        
        return True
    
    def removeSeries(self, name: str) -> bool:
        """
        Remove a series from the data manager.
        
        Args:
            name: Series name to remove
            
        Returns:
            bool: True if removed successfully, False if series doesn't exist
        """
        if name not in self._seriesData:
            return False
        
        # Remove all references to the series
        for dictionary in [self._seriesData, self._seriesColors, self._seriesVisible,
                          self._seriesLineStyles, self._seriesLineWidths,
                          self._seriesMarkerStyles, self._seriesMarkerSizes]:
            dictionary.pop(name, None)
        
        # Emit signal
        self.seriesRemoved.emit(name)
        
        return True
    
    def updateSeriesData(self, name: str, data: List[Tuple[float, float]]) -> bool:
        """
        Update data for an existing series.
        
        Args:
            name: Series name
            data: New data points
            
        Returns:
            bool: True if updated successfully, False if series doesn't exist
        """
        if name not in self._seriesData:
            return False
        
        # Validate data
        if not self._validateData(data):
            raise ValueError("Invalid data format")
        
        # Update data
        self._seriesData[name] = data.copy()
        
        # Emit signal
        self.dataChanged.emit(name)
        
        return True
    
    def appendToSeries(self, name: str, points: List[Tuple[float, float]]) -> bool:
        """
        Append points to an existing series.
        
        Args:
            name: Series name
            points: Points to append
            
        Returns:
            bool: True if appended successfully, False if series doesn't exist
        """
        if name not in self._seriesData:
            return False
        
        # Validate data
        if not self._validateData(points):
            raise ValueError("Invalid data format")
        
        # Append points
        self._seriesData[name].extend(points.copy())
        
        # Emit signal
        self.dataChanged.emit(name)
        
        return True
    
    def clearSeriesData(self, name: str) -> bool:
        """
        Clear all data points from a series.
        
        Args:
            name: Series name
            
        Returns:
            bool: True if cleared successfully, False if series doesn't exist
        """
        if name not in self._seriesData:
            return False
        
        self._seriesData[name].clear()
        self.dataChanged.emit(name)
        
        return True
    
    def clearAllData(self):
        """Clear all series and data from the manager."""
        series_names = list(self._seriesData.keys())
        
        self._seriesData.clear()
        self._seriesColors.clear()
        self._seriesVisible.clear()
        self._seriesLineStyles.clear()
        self._seriesLineWidths.clear()
        self._seriesMarkerStyles.clear()
        self._seriesMarkerSizes.clear()
        
        # Emit removed signals
        for name in series_names:
            self.seriesRemoved.emit(name)
    
    # ============ DATA RETRIEVAL METHODS ============
    
    def getSeriesNames(self) -> List[str]:
        """Get list of all series names."""
        return list(self._seriesData.keys())
    
    def getSeriesData(self, name: str) -> Optional[List[Tuple[float, float]]]:
        """Get data for a specific series."""
        return self._seriesData.get(name, None)
    
    def getVisibleSeriesData(self) -> Dict[str, List[Tuple[float, float]]]:
        """Get data for all visible series."""
        return {name: data for name, data in self._seriesData.items() 
                if self._seriesVisible.get(name, True)}
    
    def getAllData(self) -> Dict[str, List[Tuple[float, float]]]:
        """Get all data (including hidden series)."""
        return self._seriesData.copy()
    
    def getSeriesCount(self) -> int:
        """Get number of series."""
        return len(self._seriesData)
    
    def getTotalPointCount(self) -> int:
        """Get total number of data points across all series."""
        return sum(len(data) for data in self._seriesData.values())
    
    def getPointCount(self, name: str) -> int:
        """Get number of data points for a specific series."""
        data = self._seriesData.get(name)
        return len(data) if data else 0
    
    def getDataBounds(self) -> Dict[str, Tuple[float, float, float, float]]:
        """
        Get bounds for each series.
        
        Returns:
            Dict with series name as key and (x_min, x_max, y_min, y_max) as value
        """
        bounds = {}
        for name, data in self._seriesData.items():
            if data:
                x_vals = [p[0] for p in data]
                y_vals = [p[1] for p in data]
                bounds[name] = (min(x_vals), max(x_vals), min(y_vals), max(y_vals))
        
        return bounds
    
    def getAllDataBounds(self) -> Tuple[float, float, float, float]:
        """
        Get overall bounds of all data.
        
        Returns:
            (x_min, x_max, y_min, y_max) for all data
        """
        all_x = []
        all_y = []
        
        for data in self._seriesData.values():
            for x, y in data:
                all_x.append(x)
                all_y.append(y)
        
        if not all_x or not all_y:
            return (0, 1, 0, 1)
        
        return (min(all_x), max(all_x), min(all_y), max(all_y))
    
    # ============ SERIES PROPERTY METHODS ============
    
    def setSeriesColor(self, name: str, color: QColor) -> bool:
        """Set color for a series."""
        if name not in self._seriesData:
            return False
        
        self._seriesColors[name] = color
        self.dataChanged.emit(name)
        return True
    
    def getSeriesColor(self, name: str) -> Optional[QColor]:
        """Get color for a series."""
        return self._seriesColors.get(name)
    
    def setSeriesVisibility(self, name: str, visible: bool) -> bool:
        """Set visibility for a series."""
        if name not in self._seriesData:
            return False
        
        self._seriesVisible[name] = visible
        self.seriesVisibilityChanged.emit(name, visible)
        return True
    
    def getSeriesVisibility(self, name: str) -> bool:
        """Get visibility for a series."""
        return self._seriesVisible.get(name, self._defaultVisible)
    
    def setSeriesLineStyle(self, name: str, style: str) -> bool:
        """Set line style for a series."""
        if name not in self._seriesData:
            return False
        
        self._seriesLineStyles[name] = style
        self.dataChanged.emit(name)
        return True
    
    def getSeriesLineStyle(self, name: str) -> str:
        """Get line style for a series."""
        return self._seriesLineStyles.get(name, self._defaultLineStyle)
    
    def setSeriesLineWidth(self, name: str, width: float) -> bool:
        """Set line width for a series."""
        if name not in self._seriesData:
            return False
        
        self._seriesLineWidths[name] = float(width)
        self.dataChanged.emit(name)
        return True
    
    def getSeriesLineWidth(self, name: str) -> float:
        """Get line width for a series."""
        return self._seriesLineWidths.get(name, self._defaultLineWidth)
    
    def setSeriesMarkerStyle(self, name: str, style: str) -> bool:
        """Set marker style for a series."""
        if name not in self._seriesData:
            return False
        
        self._seriesMarkerStyles[name] = style
        self.dataChanged.emit(name)
        return True
    
    def getSeriesMarkerStyle(self, name: str) -> str:
        """Get marker style for a series."""
        return self._seriesMarkerStyles.get(name, self._defaultMarkerStyle)
    
    def setSeriesMarkerSize(self, name: str, size: float) -> bool:
        """Set marker size for a series."""
        if name not in self._seriesData:
            return False
        
        self._seriesMarkerSizes[name] = float(size)
        self.dataChanged.emit(name)
        return True
    
    def getSeriesMarkerSize(self, name: str) -> float:
        """Get marker size for a series."""
        return self._seriesMarkerSizes.get(name, self._defaultMarkerSize)
    
    # ============ BULK OPERATIONS ============
    
    def setAllSeriesVisibility(self, visible: bool):
        """Set visibility for all series."""
        for name in self._seriesData.keys():
            self._seriesVisible[name] = visible
            self.seriesVisibilityChanged.emit(name, visible)
    
    def setAllSeriesColor(self, color: QColor):
        """Set color for all series."""
        for name in self._seriesData.keys():
            self._seriesColors[name] = color
        # Emit changed for all series
        for name in self._seriesData.keys():
            self.dataChanged.emit(name)
    
    def setAllMarkerSizes(self, size: float):
        """Set marker size for all series."""
        size_float = float(size)
        for name in self._seriesData.keys():
            self._seriesMarkerSizes[name] = size_float
        # Emit changed for all series
        for name in self._seriesData.keys():
            self.dataChanged.emit(name)
    
    # ============ DEFAULT VALUE METHODS ============
    
    def setDefaultColor(self, color: QColor):
        """Set default color for new series."""
        self._defaultColor = color
    
    def getDefaultColor(self) -> QColor:
        """Get default color."""
        return self._defaultColor
    
    def setDefaultLineStyle(self, style: str):
        """Set default line style for new series."""
        self._defaultLineStyle = style
    
    def getDefaultLineStyle(self) -> str:
        """Get default line style."""
        return self._defaultLineStyle
    
    def setDefaultLineWidth(self, width: float):
        """Set default line width for new series."""
        self._defaultLineWidth = float(width)
    
    def getDefaultLineWidth(self) -> float:
        """Get default line width."""
        return self._defaultLineWidth
    
    def setDefaultMarkerStyle(self, style: str):
        """Set default marker style for new series."""
        self._defaultMarkerStyle = style
    
    def getDefaultMarkerStyle(self) -> str:
        """Get default marker style."""
        return self._defaultMarkerStyle
    
    def setDefaultMarkerSize(self, size: float):
        """Set default marker size for new series."""
        self._defaultMarkerSize = float(size)
    
    def getDefaultMarkerSize(self) -> float:
        """Get default marker size."""
        return self._defaultMarkerSize
    
    def setDefaultVisible(self, visible: bool):
        """Set default visibility for new series."""
        self._defaultVisible = visible
    
    def getDefaultVisible(self) -> bool:
        """Get default visibility."""
        return self._defaultVisible
    
    # ============ VALIDATION AND HELPER METHODS ============
    
    def _validateData(self, data: List[Tuple[float, float]]) -> bool:
        """Validate data format."""
        if not isinstance(data, list):
            return False
        
        for point in data:
            if not isinstance(point, (list, tuple)) or len(point) != 2:
                return False
            if not all(isinstance(coord, (int, float)) for coord in point):
                return False
        
        return True
    
    def _getNextColor(self, index: int) -> QColor:
        """Get a color for a series based on index."""
        colors = [
            QColor(255, 100, 100),    # Red
            QColor(100, 200, 100),    # Green
            QColor(100, 150, 255),    # Blue
            QColor(200, 100, 200),    # Purple
            QColor(255, 150, 50),     # Orange
            QColor(50, 200, 200),     # Cyan
            QColor(200, 200, 50),     # Yellow
            QColor(150, 100, 255),    # Violet
        ]
        
        return colors[index % len(colors)]
    
    def seriesExists(self, name: str) -> bool:
        """Check if a series exists."""
        return name in self._seriesData
    
    def getSeriesProperties(self, name: str) -> Optional[Dict[str, Any]]:
        """Get all properties for a series."""
        if name not in self._seriesData:
            return None
        
        return {
            "name": name,
            "data": self._seriesData[name].copy(),
            "color": self._seriesColors.get(name),
            "visible": self._seriesVisible.get(name, True),
            "line_style": self._seriesLineStyles.get(name, self._defaultLineStyle),
            "line_width": self._seriesLineWidths.get(name, self._defaultLineWidth),
            "marker_style": self._seriesMarkerStyles.get(name, self._defaultMarkerStyle),
            "marker_size": self._seriesMarkerSizes.get(name, self._defaultMarkerSize),
            "point_count": len(self._seriesData[name])
        }
    
    def getAllSeriesProperties(self) -> Dict[str, Dict[str, Any]]:
        """Get properties for all series."""
        properties = {}
        for name in self._seriesData.keys():
            properties[name] = self.getSeriesProperties(name)
        return properties
    
    def importData(self, data_dict: Dict[str, Any]) -> List[str]:
        """
        Import data from a dictionary.
        
        Expected format:
        {
            "series_name": {
                "data": [(x1, y1), (x2, y2), ...],
                "color": QColor or (r, g, b, a),
                "visible": bool,
                "line_style": str,
                "line_width": float,
                "marker_style": str,
                "marker_size": float
            },
            ...
        }
        
        Returns:
            List of imported series names
        """
        imported = []
        
        for name, series_data in data_dict.items():
            if "data" not in series_data:
                continue
            
            data = series_data["data"]
            color = series_data.get("color")
            visible = series_data.get("visible")
            line_style = series_data.get("line_style")
            line_width = series_data.get("line_width")
            marker_style = series_data.get("marker_style")
            marker_size = series_data.get("marker_size")
            
            # Convert color if it's a tuple
            if isinstance(color, (list, tuple)) and len(color) in [3, 4]:
                if len(color) == 3:
                    color = QColor(color[0], color[1], color[2])
                else:
                    color = QColor(color[0], color[1], color[2], color[3])
            
            if self.addSeries(name, data, color, visible, line_style, 
                             line_width, marker_style, marker_size):
                imported.append(name)
        
        return imported
    
    def exportData(self) -> Dict[str, Any]:
        """
        Export all data to a dictionary.
        
        Returns:
            Dictionary containing all series data and properties
        """
        export_dict = {}
        
        for name in self._seriesData.keys():
            props = self.getSeriesProperties(name)
            if props:
                # Convert QColor to tuple for serialization
                if isinstance(props["color"], QColor):
                    color = props["color"]
                    props["color"] = (color.red(), color.green(), color.blue(), color.alpha())
                
                export_dict[name] = props
        
        return export_dict
    

    def addDummyData(self, num_series: int = 3, num_points: int = 10):
        """
        Add dummy series for testing/designer preview.
        
        Args:
            num_series: Number of series to add
            num_points: Number of points per series
        """
        
        # Clear existing data
        self.clearAllData()
        
        # Add dummy series
        for i in range(num_series):
            series_name = f"Series {i+1}"
            data = []
            
            # Generate different types of data
            if i == 0:
                # Sine wave
                for j in range(num_points):
                    x = j * 2.0
                    y = 20 * math.sin(x * math.pi / 10)
                    data.append((x, y))
            elif i == 1:
                # Cosine wave
                for j in range(num_points):
                    x = j * 2.0
                    y = 20 * math.cos(x * math.pi / 10)
                    data.append((x, y))
            else:
                # Linear with noise
                base = random.uniform(10, 30)
                for j in range(num_points):
                    x = j * 2.0
                    y = base + j * 2 + random.uniform(-5, 5)
                    data.append((x, y))
            
            # Use default colors from the color list
            color = self._getNextColor(i)
            
            # Add series with different styles
            self.addSeries(
                name=series_name,
                data=data,
                color=color,
                visible=True,
                line_style=self._defaultLineStyle,
                line_width=self._defaultLineWidth,
                marker_style=self.MARKER_CIRCLE if i == 0 else self.MARKER_RECTANGLE,
                marker_size=self._defaultMarkerSize
            )