# file name: QCustomChartExporter.py
import os
from typing import Optional, List, Tuple, Dict, Any
from qtpy.QtCore import Qt, Signal, QObject, QRect, QSize, QMarginsF
from qtpy.QtWidgets import QWidget, QFileDialog, QMessageBox, QApplication
from qtpy.QtGui import QPainter, QPixmap, QImage, QPageLayout, QPageSize
from qtpy.QtPrintSupport import QPrinter
from qtpy.QtCharts import QChartView

from .QCustomChartConstants import QCustomChartConstants


class QCustomChartExporter(QObject, QCustomChartConstants):
    """
    Chart export system supporting multiple formats and customization options.
    Handles image, PDF, and data export with various settings.
    """
    
    # Signals
    exportStarted = Signal(str)  # format being exported
    exportComplete = Signal(str, bool)  # filename, success
    exportProgress = Signal(int)  # progress percentage
    exportError = Signal(str)  # error message
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Export settings
        self._defaultDirectory = ""
        self._defaultFilename = "chart_export"
        self._imageQuality = 90  # for JPEG
        self._imageResolution = 300  # DPI
        self._pageSize = QPageSize.A4
        self._pageOrientation = Qt.PortraitOrientation
        self._margins = (10, 10, 10, 10)  # left, top, right, bottom in mm
        
        # Export mode
        self._exportMode = "current_view"  # "current_view", "full_chart", or "custom"
        self._exportScaleFactor = 1.0  # For custom scaling
        
        # Supported formats
        self._supportedImageFormats = [self.FORMAT_PNG, self.FORMAT_JPEG]
        self._supportedVectorFormats = [self.FORMAT_PDF, self.FORMAT_SVG]
        self._supportedDataFormats = [self.FORMAT_CSV, self.FORMAT_JSON]
        
        # Current export
        self._isExporting = False
        self._currentFormat = ""
    
    def setDefaultDirectory(self, directory: str):
        """Set default export directory"""
        if os.path.isdir(directory):
            self._defaultDirectory = directory
    
    def getDefaultDirectory(self) -> str:
        """Get default export directory"""
        return self._defaultDirectory
    
    def setDefaultFilename(self, filename: str):
        """Set default export filename (without extension)"""
        self._defaultFilename = filename
    
    def getDefaultFilename(self) -> str:
        """Get default export filename"""
        return self._defaultFilename
    
    def setImageQuality(self, quality: int):
        """Set JPEG image quality (0-100)"""
        self._imageQuality = max(0, min(100, quality))
    
    def getImageQuality(self) -> int:
        """Get JPEG image quality"""
        return self._imageQuality
    
    def setImageResolution(self, dpi: int):
        """Set image resolution in DPI"""
        self._imageResolution = max(72, dpi)
    
    def getImageResolution(self) -> int:
        """Get image resolution in DPI"""
        return self._imageResolution
    
    def setPageSize(self, page_size: QPageSize):
        """Set page size for PDF export"""
        self._pageSize = page_size
    
    def getPageSize(self) -> QPageSize:
        """Get page size for PDF export"""
        return self._pageSize
    
    def setPageOrientation(self, orientation: Qt.Orientation):
        """Set page orientation for PDF export"""
        self._pageOrientation = orientation
    
    def getPageOrientation(self) -> Qt.Orientation:
        """Get page orientation for PDF export"""
        return self._pageOrientation
    
    def setMargins(self, left: int, top: int, right: int, bottom: int):
        """Set page margins in millimeters"""
        self._margins = (left, top, right, bottom)
    
    def getMargins(self) -> Tuple[int, int, int, int]:
        """Get page margins"""
        return self._margins
    
    def setExportMode(self, mode: str):
        """Set export mode: 'current_view', 'full_chart', or 'custom'"""
        valid_modes = ["current_view", "full_chart", "custom"]
        if mode in valid_modes:
            self._exportMode = mode
    
    def getExportMode(self) -> str:
        """Get export mode"""
        return self._exportMode
    
    def setExportScaleFactor(self, factor: float):
        """Set custom scale factor for export"""
        self._exportScaleFactor = max(0.1, min(5.0, factor))
    
    def getExportScaleFactor(self) -> float:
        """Get export scale factor"""
        return self._exportScaleFactor
    
    def getSupportedFormats(self) -> Dict[str, List[str]]:
        """Get all supported export formats by category"""
        return {
            "image": self._supportedImageFormats,
            "vector": self._supportedVectorFormats,
            "data": self._supportedDataFormats
        }
    
    def exportChart(self, chart_view: QChartView, 
                   format: str = None,
                   filename: Optional[str] = None,
                   parent_widget: Optional[QWidget] = None) -> bool:
        """
        Export a chart to a file.
        
        Args:
            chart_view: The chart view to export
            format: Export format (PNG, JPEG, PDF, SVG, CSV, JSON)
            filename: Optional filename (prompt if None)
            parent_widget: Optional parent widget for dialogs
            
        Returns:
            bool: True if export succeeded, False otherwise
        """
        if self._isExporting:
            self.exportError.emit("Another export is in progress")
            return False
        
        if format is None:
            format = self.FORMAT_PNG
        
        self._isExporting = True
        self._currentFormat = format
        
        try:
            # Get filename if not provided
            if not filename:
                filename = self._getExportFilename(format, parent_widget)
                if not filename:  # User cancelled
                    self._isExporting = False
                    return False
            
            # Emit start signal
            self.exportStarted.emit(format)
            self.exportProgress.emit(10)
            
            # Perform export based on format
            success = False
            
            if format in self._supportedImageFormats:
                success = self._exportImage(chart_view, filename, format)
            elif format in self._supportedVectorFormats:
                success = self._exportVector(chart_view, filename, format)
            elif format in self._supportedDataFormats:
                success = self._exportData(chart_view, filename, format)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.exportProgress.emit(100)
            self.exportComplete.emit(filename, success)
            
            return success
            
        except Exception as e:
            error_msg = f"Export error: {str(e)}"
            self.exportError.emit(error_msg)
            self.exportComplete.emit(filename if 'filename' in locals() else "", False)
            return False
        finally:
            self._isExporting = False
    
    def _getExportFilename(self, format: str, parent: Optional[QWidget]) -> Optional[str]:
        """Get export filename from user via dialog"""
        # Determine file filter based on format
        if format == self.FORMAT_PNG:
            file_filter = "PNG Files (*.png);;All Files (*)"
            default_ext = ".png"
        elif format == self.FORMAT_JPEG:
            file_filter = "JPEG Files (*.jpg *.jpeg);;All Files (*)"
            default_ext = ".jpg"
        elif format == self.FORMAT_PDF:
            file_filter = "PDF Files (*.pdf);;All Files (*)"
            default_ext = ".pdf"
        elif format == self.FORMAT_SVG:
            file_filter = "SVG Files (*.svg);;All Files (*)"
            default_ext = ".svg"
        elif format == self.FORMAT_CSV:
            file_filter = "CSV Files (*.csv);;All Files (*)"
            default_ext = ".csv"
        elif format == self.FORMAT_JSON:
            file_filter = "JSON Files (*.json);;All Files (*)"
            default_ext = ".json"
        else:
            file_filter = "All Files (*)"
            default_ext = ""
        
        # Build default filename
        default_name = f"{self._defaultFilename}{default_ext}"
        if self._defaultDirectory:
            default_path = os.path.join(self._defaultDirectory, default_name)
        else:
            default_path = default_name
        
        # Show file dialog
        filename, selected_filter = QFileDialog.getSaveFileName(
            parent,
            f"Export Chart as {format}",
            default_path,
            file_filter
        )
        
        if not filename:
            return None
        
        # Ensure correct extension
        if not filename.lower().endswith(default_ext.lower()):
            filename += default_ext
        
        return filename
    
    def _exportImage(self, chart_view: QChartView, filename: str, format: str) -> bool:
        """Export chart as image (PNG or JPEG)"""
        self.exportProgress.emit(30)
        
        # Calculate size based on resolution and export mode
        if self._exportMode == "current_view":
            # Export current view (as seen on screen)
            pixmap = self._captureCurrentView(chart_view)
        elif self._exportMode == "full_chart":
            # Export full chart (reset zoom for export)
            pixmap = self._captureFullChart(chart_view)
        else:  # custom
            # Export with custom scaling
            pixmap = self._captureWithCustomScale(chart_view)
        
        self.exportProgress.emit(70)
        
        # Save with appropriate settings
        if format == self.FORMAT_PNG:
            success = pixmap.save(filename, "PNG")
        elif format == self.FORMAT_JPEG:
            success = pixmap.save(filename, "JPEG", self._imageQuality)
        else:
            success = False
        
        self.exportProgress.emit(90)
        return success
    
    def _captureCurrentView(self, chart_view: QChartView) -> QPixmap:
        """Capture the current view (what's visible on screen)"""
        # Simply grab what's currently visible
        return chart_view.grab()
    
    def _captureFullChart(self, chart_view: QChartView) -> QPixmap:
        """Capture the full chart (reset zoom temporarily)"""
        # Store current zoom state
        chart = chart_view.chart()
        
        # Calculate size based on resolution
        dpi_scale = self._imageResolution / 72.0
        size = chart_view.size() * dpi_scale
        
        # Create pixmap
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        
        # Create painter
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Scale to DPI
        painter.scale(dpi_scale, dpi_scale)
        
        # Temporarily zoom reset to show full chart
        original_zoom = chart.zoomFactor()
        chart.zoomReset()
        
        # Render the chart
        chart_view.render(painter)
        
        # Restore original zoom
        chart.zoomIn(original_zoom)
        
        painter.end()
        
        return pixmap
    
    def _captureWithCustomScale(self, chart_view: QChartView) -> QPixmap:
        """Capture chart with custom scale factor"""
        # Calculate size based on resolution and scale factor
        dpi_scale = self._imageResolution / 72.0
        scale = self._exportScaleFactor
        size = chart_view.size() * dpi_scale * scale
        
        # Create pixmap
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        
        # Create painter
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Scale to DPI and custom scale
        painter.scale(dpi_scale * scale, dpi_scale * scale)
        
        # Render chart
        chart_view.render(painter)
        painter.end()
        
        return pixmap
    
    def _exportVector(self, chart_view: QChartView, filename: str, format: str) -> bool:
        """Export chart as vector (PDF or SVG)"""
        self.exportProgress.emit(30)
        
        if format == self.FORMAT_PDF:
            success = self._exportToPDF(chart_view, filename)
        elif format == self.FORMAT_SVG:
            success = self._exportToSVG(chart_view, filename)
        else:
            success = False
        
        self.exportProgress.emit(90)
        return success
    
    def _exportToPDF(self, chart_view: QChartView, filename: str) -> bool:
        """Export chart to PDF"""
        try:
            # Create printer for PDF
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(filename)
            
            # Set page layout
            printer.setPageSize(self._pageSize)
            printer.setOrientation(self._pageOrientation)
            
            # Set margins
            printer.setPageMargins(
                QMarginsF(self._margins[0], self._margins[1], 
                         self._margins[2], self._margins[3]),
                QPrinter.Millimeter
            )
            
            # Create painter
            painter = QPainter(printer)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Get page and chart rectangles
            page_rect = printer.pageRect(QPrinter.DevicePixel)
            chart_rect = chart_view.rect()
            
            # Calculate scale to fit page with margins
            available_width = page_rect.width()
            available_height = page_rect.height()
            
            x_scale = available_width / chart_rect.width()
            y_scale = available_height / chart_rect.height()
            scale = min(x_scale, y_scale) * 0.95  # Leave 5% margin
            
            # Apply transformation to center on page
            painter.translate(page_rect.center())
            painter.scale(scale, scale)
            painter.translate(-chart_rect.center())
            
            # Render chart
            chart_view.render(painter)
            painter.end()
            
            return True
            
        except Exception as e:
            print(f"PDF export error: {e}")
            return False
    
    def _exportToSVG(self, chart_view: QChartView, filename: str) -> bool:
        """Export chart to SVG (simplified - uses image export for now)"""
        # Note: Proper SVG export would require more complex implementation
        # For now, fall back to high-res PNG
        return self._exportImage(chart_view, filename, self.FORMAT_PNG)
    
    def _exportData(self, chart_view: QChartView, filename: str, format: str) -> bool:
        """Export chart data (CSV or JSON)"""
        self.exportProgress.emit(30)
        
        try:
            # Get chart data from parent if available
            chart_data = None
            parent = self.parent()
            if parent:
                # Try to get data from parent's data manager
                if hasattr(parent, '_data_manager'):
                    chart_data = parent._data_manager.getAllData()
                elif hasattr(parent, 'getSeriesNames'):
                    # Try to get data via method
                    chart_data = {}
                    series_names = parent.getSeriesNames()
                    for name in series_names:
                        chart_data[name] = parent.getSeriesData(name)
            
            if not chart_data:
                # Fallback: extract data from chart series
                chart_data = self._extractDataFromChart(chart_view.chart())
            
            self.exportProgress.emit(60)
            
            # Export based on format
            if format == self.FORMAT_CSV:
                success = self._exportToCSV(chart_data, filename)
            elif format == self.FORMAT_JSON:
                success = self._exportToJSON(chart_data, filename)
            else:
                success = False
            
            self.exportProgress.emit(90)
            return success
            
        except Exception as e:
            print(f"Data export error: {e}")
            return False
    
    def _extractDataFromChart(self, chart) -> Dict[str, List[Tuple[float, float]]]:
        """Extract data from chart series"""
        data = {}
        
        for series in chart.series():
            series_name = series.name()
            if series_name and not series_name.startswith("__"):  # Skip internal series
                points = []
                for i in range(series.count()):
                    point = series.at(i)
                    points.append((point.x(), point.y()))
                data[series_name] = points
        
        return data
    
    def _exportToCSV(self, data: Dict[str, List[Tuple[float, float]]], filename: str) -> bool:
        """Export data to CSV format"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Write header
                f.write("Series,X,Y\n")
                
                # Write data
                for series_name, points in data.items():
                    for x, y in points:
                        f.write(f'"{series_name}",{x},{y}\n')
            
            return True
        except Exception as e:
            print(f"CSV export error: {e}")
            return False
    
    def _exportToJSON(self, data: Dict[str, List[Tuple[float, float]]], filename: str) -> bool:
        """Export data to JSON format"""
        try:
            import json
            
            # Convert to JSON-serializable format
            json_data = {}
            for series_name, points in data.items():
                json_data[series_name] = [
                    {"x": x, "y": y} for x, y in points
                ]
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"JSON export error: {e}")
            return False
    
    def exportToClipboard(self, chart_view: QChartView, mode: str = "current_view"):
        """Export chart to clipboard as image"""
        try:
            if mode == "current_view":
                pixmap = chart_view.grab()
            elif mode == "full_chart":
                pixmap = self._captureFullChart(chart_view)
            else:
                pixmap = self._captureWithCustomScale(chart_view)
                
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(pixmap)
            return True
        except Exception as e:
            print(f"Clipboard export error: {e}")
            return False
    
    def printChart(self, chart_view: QChartView, printer: QPrinter = None):
        """Print the chart"""
        try:
            if not printer:
                printer = QPrinter(QPrinter.HighResolution)
            
            painter = QPainter(printer)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Get page and chart rectangles
            page_rect = printer.pageRect(QPrinter.DevicePixel)
            chart_rect = chart_view.rect()
            
            # Calculate scale to fit page
            x_scale = page_rect.width() / chart_rect.width()
            y_scale = page_rect.height() / chart_rect.height()
            scale = min(x_scale, y_scale) * 0.9
            
            # Apply transformation
            painter.translate(page_rect.center())
            painter.scale(scale, scale)
            painter.translate(-chart_rect.center())
            
            # Render chart
            chart_view.render(painter)
            painter.end()
            
            return True
        except Exception as e:
            print(f"Print error: {e}")
            return False
    
    def isExporting(self) -> bool:
        """Check if an export is in progress"""
        return self._isExporting
    
    def cancelExport(self):
        """Cancel current export"""
        # Note: This would need proper threading to cancel
        self._isExporting = False
    
    def getExportModes(self) -> List[str]:
        """Get available export modes"""
        return ["current_view", "full_chart", "custom"]
    
    def getExportSettings(self) -> Dict[str, Any]:
        """Get current export settings"""
        return {
            "default_directory": self._defaultDirectory,
            "default_filename": self._defaultFilename,
            "image_quality": self._imageQuality,
            "image_resolution": self._imageResolution,
            "page_size": str(self._pageSize.id()),
            "page_orientation": "portrait" if self._pageOrientation == Qt.PortraitOrientation else "landscape",
            "margins": self._margins,
            "export_mode": self._exportMode,
            "export_scale_factor": self._exportScaleFactor,
            "is_exporting": self._isExporting
        }