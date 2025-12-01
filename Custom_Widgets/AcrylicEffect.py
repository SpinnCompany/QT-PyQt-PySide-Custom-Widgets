# coding:utf-8
import warnings
import os
import sys
import platform
from math import floor
from io import BytesIO
from typing import Union

import numpy as np
from colorthief import ColorThief
from PIL import Image
from qtpy.QtCore import Qt, QThread, Signal, QRect, QIODevice, QBuffer
from qtpy.QtGui import QBrush, QColor, QImage, QPainter, QPixmap, QPainterPath, QLinearGradient
from qtpy.QtWidgets import QLabel, QApplication, QWidget

# Handle scipy import with compatibility
try:
    from scipy.ndimage import gaussian_filter
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    # Fallback using PIL
    warnings.warn("scipy not found, using PIL fallback for Gaussian blur")

from Custom_Widgets.Log import *

class PlatformDetector:
    """Detect platform and display server for compatibility handling"""
    
    @staticmethod
    def detect_platform():
        """Detect the current platform and display server"""
        system = platform.system().lower()
        display_server = "unknown"
        
        # Detect display server on Linux
        if system == "linux":
            # Check for Wayland
            wayland_display = os.environ.get('WAYLAND_DISPLAY')
            xdg_session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
            desktop_session = os.environ.get('DESKTOP_SESSION', '').lower()
            
            if wayland_display or xdg_session_type == 'wayland':
                display_server = "wayland"
            else:
                # Check common X11 environment variables
                x11_display = os.environ.get('DISPLAY')
                if x11_display and ':0' in x11_display:
                    display_server = "x11"
                else:
                    # Default to X11 if no specific indicator
                    display_server = "x11"
        
        elif system == "darwin":  # macOS
            display_server = "quartz"
        
        elif system == "windows":
            display_server = "windows"
        
        return {
            "system": system,
            "display_server": display_server,
            "is_linux": system == "linux",
            "is_macos": system == "darwin",
            "is_windows": system == "windows",
            "is_wayland": display_server == "wayland",
            "is_x11": display_server == "x11"
        }


class GaussianBlurUtils:
    """Utility class for Gaussian blur operations with platform compatibility"""
    
    @staticmethod
    def gaussianBlur(image, blurRadius=18, brightFactor=1, blurPicSize=None):
        """
        Apply Gaussian blur to an image with platform compatibility
        
        Parameters:
        -----------
        image: str, PIL.Image, QPixmap, or QImage
            Input image
        blurRadius: float
            Radius for Gaussian blur
        brightFactor: float
            Brightness factor (0.0 to 1.0)
        blurPicSize: tuple or None
            Target size for performance optimization
        
        Returns:
        --------
        QPixmap: Blurred image as QPixmap
        """
        try:
            # Convert input to PIL Image if needed
            if isinstance(image, str) and not image.startswith(':'):
                pil_image = Image.open(image)
            elif isinstance(image, (QPixmap, QImage)):
                pil_image = GaussianBlurUtils.fromQtImage(image)
            elif isinstance(image, Image.Image):
                pil_image = image
            else:
                raise ValueError(f"Unsupported image type: {type(image)}")
            
            # Handle blur radius
            if blurRadius <= 0:
                # Return original image if no blur needed
                return GaussianBlurUtils.toQPixmap(pil_image)
            
            # Resize for performance if requested
            if blurPicSize:
                w, h = pil_image.size
                ratio = min(blurPicSize[0] / w, blurPicSize[1] / h)
                if ratio < 1.0:  # Only downscale if needed
                    w_, h_ = int(w * ratio), int(h * ratio)
                    pil_image = pil_image.resize((w_, h_), Image.Resampling.LANCZOS)
            
            # Apply blur using available method
            if HAS_SCIPY:
                # Use scipy for high-quality blur
                image_array = np.array(pil_image)
                
                # Handle different image modes
                if len(image_array.shape) == 2:  # Grayscale
                    image_array = np.stack([image_array] * 3, axis=-1)
                elif image_array.shape[2] == 4:  # RGBA
                    # Separate alpha channel
                    alpha = image_array[:, :, 3]
                    rgb = image_array[:, :, :3]
                    
                    # Blur RGB channels
                    for i in range(3):
                        rgb[:, :, i] = gaussian_filter(rgb[:, :, i], blurRadius) * brightFactor
                    
                    # Recombine with original alpha
                    image_array = np.dstack((rgb, alpha))
                else:  # RGB
                    for i in range(3):
                        image_array[:, :, i] = gaussian_filter(
                            image_array[:, :, i], blurRadius) * brightFactor
                
                return GaussianBlurUtils.ndarrayToQPixmap(image_array)
                
            else:
                # Fallback using PIL's Gaussian blur
                warnings.warn("Using PIL fallback for Gaussian blur (install scipy for better quality)")
                
                # Convert to RGBA if needed
                if pil_image.mode != 'RGBA':
                    pil_image = pil_image.convert('RGBA')
                
                # Apply PIL's Gaussian blur
                # Note: PIL's blur is simpler but works without scipy
                blurred = pil_image.filter(ImageFilter.GaussianBlur(radius=blurRadius/2))
                
                # Adjust brightness
                if brightFactor != 1.0:
                    from PIL import ImageEnhance
                    enhancer = ImageEnhance.Brightness(blurred)
                    blurred = enhancer.enhance(brightFactor)
                
                return GaussianBlurUtils.toQPixmap(blurred)
                
        except Exception as e:
            logError(f"Gaussian blur failed: {e}")
            # Return original image as fallback
            if isinstance(image, (QPixmap, QImage)):
                return image if isinstance(image, QPixmap) else QPixmap.fromImage(image)
            else:
                # Create a solid color fallback
                fallback = QPixmap(100, 100)
                fallback.fill(QColor(200, 200, 200, 200))
                return fallback
    
    @staticmethod
    def fromQtImage(qt_image):
        """Convert QImage or QPixmap to PIL Image"""
        buffer = QBuffer()
        buffer.open(QIODevice.OpenModeFlag.ReadWrite)
        
        # Save to buffer with appropriate format
        if isinstance(qt_image, QImage):
            if qt_image.hasAlphaChannel():
                qt_image.save(buffer, "PNG")
            else:
                qt_image.save(buffer, "JPEG")
        elif isinstance(qt_image, QPixmap):
            if qt_image.hasAlpha():
                qt_image.save(buffer, "PNG")
            else:
                qt_image.save(buffer, "JPEG")
        
        buffer_data = buffer.data()
        buffer.close()
        
        # Convert to PIL Image
        return Image.open(BytesIO(buffer_data))
    
    @staticmethod
    def toQPixmap(pil_image):
        """Convert PIL Image to QPixmap"""
        # Convert PIL Image to bytes
        buffer = BytesIO()
        
        if pil_image.mode == 'RGBA':
            pil_image.save(buffer, format='PNG')
            format = QImage.Format.Format_RGBA8888
        else:
            pil_image.convert('RGB').save(buffer, format='JPEG')
            format = QImage.Format.Format_RGB888
        
        buffer.seek(0)
        
        # Create QImage from buffer
        qimage = QImage()
        qimage.loadFromData(buffer.getvalue())
        
        return QPixmap.fromImage(qimage)
    
    @staticmethod
    def ndarrayToQPixmap(array):
        """Convert numpy array to QPixmap"""
        h, w, c = array.shape
        
        if c == 3:  # RGB
            format = QImage.Format.Format_RGB888
        elif c == 4:  # RGBA
            format = QImage.Format.Format_RGBA8888
        else:
            # Convert grayscale to RGB
            array = np.stack([array[:, :, 0]] * 3, axis=-1)
            format = QImage.Format.Format_RGB888
            c = 3
        
        # Ensure correct data type
        if array.dtype != np.uint8:
            array = np.clip(array, 0, 255).astype(np.uint8)
        
        return QPixmap.fromImage(QImage(array.data, w, h, c * w, format))


class DominantColor:
    """Dominant color extraction with error handling"""
    
    @classmethod
    def getDominantColor(cls, imagePath, defaultColor=(24, 24, 24)):
        """extract dominant color from image with error handling
        
        Parameters
        ----------
        imagePath: str
            image path
        defaultColor: tuple
            default color to return if extraction fails
        
        Returns
        -------
        r, g, b: int
            RGB color values
        """
        try:
            if imagePath.startswith(':'):
                return defaultColor
            
            if not os.path.exists(imagePath):
                logWarning(f"Image file not found: {imagePath}")
                return defaultColor
            
            colorThief = ColorThief(imagePath)
            
            # Scale image to speed up computation
            if max(colorThief.image.size) > 400:
                colorThief.image = colorThief.image.resize((400, 400))
            
            # Get color palette
            palette = colorThief.get_palette(quality=5)  # Lower quality for speed
            
            if not palette:
                return defaultColor
            
            # Adjust palette brightness
            palette = cls.__adjustPaletteValue(palette)
            
            # Filter out very dark or very bright colors
            filtered_palette = []
            for rgb in palette:
                h, s, v = cls.rgb2hsv(rgb)
                # Filter criteria
                if 0.1 < v < 0.95 and s > 0.1:
                    filtered_palette.append(rgb)
            
            # If filtering removed all colors, use original palette
            if not filtered_palette:
                filtered_palette = palette
            
            # Sort by colorfulness
            filtered_palette.sort(key=lambda rgb: cls.colorfulness(*rgb), reverse=True)
            
            return filtered_palette[0] if filtered_palette else defaultColor
            
        except Exception as e:
            logError(f"Dominant color extraction failed for {imagePath}: {e}")
            return defaultColor
    
    @classmethod
    def __adjustPaletteValue(cls, palette):
        """Adjust the brightness of palette for better visual results"""
        newPalette = []
        for rgb in palette:
            h, s, v = cls.rgb2hsv(rgb)
            
            # Adjust value based on brightness
            if v > 0.9:
                factor = 0.8  # Reduce very bright colors
            elif 0.7 < v <= 0.9:
                factor = 0.9  # Slightly reduce bright colors
            elif v < 0.3:
                factor = 1.2  # Boost very dark colors
            else:
                factor = 1.0  # Leave mid-tones as-is
            
            v = min(v * factor, 1.0)  # Ensure value doesn't exceed 1.0
            newPalette.append(cls.hsv2rgb(h, s, v))
        
        return newPalette
    
    @staticmethod
    def rgb2hsv(rgb):
        """Convert RGB to HSV color space"""
        r, g, b = [i / 255.0 for i in rgb]
        
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        delta = max_val - min_val
        
        # Calculate hue
        if delta == 0:
            h = 0
        elif max_val == r:
            h = 60 * (((g - b) / delta) % 6)
        elif max_val == g:
            h = 60 * (((b - r) / delta) + 2)
        else:  # max_val == b
            h = 60 * (((r - g) / delta) + 4)
        
        # Calculate saturation
        s = 0 if max_val == 0 else delta / max_val
        
        # Value is max component
        v = max_val
        
        return h, s, v
    
    @staticmethod
    def hsv2rgb(h, s, v):
        """Convert HSV to RGB color space"""
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:  # 300 <= h < 360
            r, g, b = c, 0, x
        
        r, g, b = (r + m) * 255, (g + m) * 255, (b + m) * 255
        
        return int(r), int(g), int(b)
    
    @staticmethod
    def colorfulness(r: int, g: int, b: int):
        """Calculate colorfulness metric"""
        rg = abs(r - g)
        yb = abs(0.5 * (r + g) - b)
        
        # Compute mean and standard deviation
        rg_mean, rg_std = np.mean(rg), np.std(rg)
        yb_mean, yb_std = np.mean(yb), np.std(yb)
        
        # Combine metrics
        std_root = np.sqrt((rg_std ** 2) + (yb_std ** 2))
        mean_root = np.sqrt((rg_mean ** 2) + (yb_mean ** 2))
        
        return std_root + (0.3 * mean_root)


class BlurCoverThread(QThread):
    """Thread for blurring album covers in background"""
    
    blurFinished = Signal(QPixmap)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.imagePath = ""
        self.blurRadius = 7
        self.maxSize = None
    
    def run(self):
        if not self.imagePath or not os.path.exists(self.imagePath):
            self.blurFinished.emit(QPixmap())  # Empty pixmap on error
            return
        
        try:
            pixmap = GaussianBlurUtils.gaussianBlur(
                self.imagePath, self.blurRadius, 0.85, self.maxSize)
            self.blurFinished.emit(pixmap)
        except Exception as e:
            logError(f"Blur thread failed for {self.imagePath}: {e}")
            # Fallback to original image
            try:
                pixmap = QPixmap(self.imagePath)
                self.blurFinished.emit(pixmap)
            except:
                self.blurFinished.emit(QPixmap())
    
    def blur(self, imagePath: str, blurRadius=6, maxSize: tuple = (450, 450)):
        """Start blur operation"""
        self.imagePath = imagePath
        self.blurRadius = blurRadius
        self.maxSize = maxSize
        self.start()


class AcrylicTextureLabel(QLabel):
    """Acrylic texture label with noise generation"""
    
    def __init__(self, tintColor: QColor, luminosityColor: QColor, 
                 noiseOpacity=0.03, parent=None):
        """
        Parameters
        ----------
        tintColor: QColor
            RGB tint color
        luminosityColor: QColor
            luminosity layer color
        noiseOpacity: float
            noise layer opacity
        parent:
            parent window
        """
        super().__init__(parent=parent)
        self.tintColor = QColor(tintColor)
        self.luminosityColor = QColor(luminosityColor)
        self.noiseOpacity = noiseOpacity
        
        # Create noise image
        self.noiseImage = self.createNoiseImage(128)  # Larger size for better quality
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def createNoiseImage(self, size=128):
        """Create a noise texture image programmatically"""
        noiseImage = QImage(size, size, QImage.Format.Format_ARGB32)
        
        # Generate perlin-like noise for better visual quality
        for x in range(size):
            for y in range(size):
                # Create more natural noise pattern
                nx = x / size
                ny = y / size
                
                # Simplex/Perlin-like noise approximation
                value = (np.sin(nx * 10) * np.cos(ny * 10) * 0.5 + 0.5) * 55
                value += np.random.randint(0, 55)
                
                # Clamp and set pixel
                gray_value = int(np.clip(value, 0, 255))
                alpha = 200 + np.random.randint(0, 55)  # Slight alpha variation
                
                noiseImage.setPixel(x, y, 
                    QColor(gray_value, gray_value, gray_value, alpha).rgba())
        
        return noiseImage
    
    def setTintColor(self, color: QColor):
        self.tintColor = color
        self.update()
    
    def paintEvent(self, e):
        """Paint acrylic texture with noise"""
        acrylicTexture = QImage(128, 128, QImage.Format.Format_ARGB32_Premultiplied)
        
        # Paint luminosity layer
        acrylicTexture.fill(self.luminosityColor)
        
        # Paint tint color
        painter = QPainter(acrylicTexture)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.fillRect(acrylicTexture.rect(), self.tintColor)
        
        # Paint noise with opacity
        painter.setOpacity(self.noiseOpacity)
        painter.drawImage(acrylicTexture.rect(), self.noiseImage)
        painter.end()
        
        # Paint final texture
        painter = QPainter(self)
        acrylicBrush = QBrush(acrylicTexture)
        painter.fillRect(self.rect(), acrylicBrush)


class AcrylicBrush:
    """Acrylic brush with multi-platform compatibility"""
    
    def __init__(self, device: QWidget, blurRadius: int, 
                 tintColor=QColor(242, 242, 242, 150),
                 luminosityColor=QColor(255, 255, 255, 10), 
                 noiseOpacity=0.03):
        self.device = device
        self.blurRadius = blurRadius
        self.tintColor = QColor(tintColor)
        self.luminosityColor = QColor(luminosityColor)
        self.noiseOpacity = noiseOpacity
        
        # Platform detection
        self.platform_info = PlatformDetector.detect_platform()
        
        # Create noise image
        self.noiseImage = self.createNoiseImage(64)
        
        # Image storage
        self.originalImage = QPixmap()
        self.image = QPixmap()
        self.clipPath = QPainterPath()
        
        # Fallback mode tracking
        self.using_fallback = False
        
        logInfo(f"AcrylicBrush initialized on {self.platform_info['system']} "
               f"with {self.platform_info['display_server']} display server")
    
    def createNoiseImage(self, size=64):
        """Create a noise texture image programmatically"""
        noiseImage = QImage(size, size, QImage.Format.Format_ARGB32)
        
        # Fill with random noise
        for x in range(size):
            for y in range(size):
                # Create subtle noise with slight color variation
                base = np.random.randint(200, 230)
                r = np.clip(base + np.random.randint(-20, 20), 0, 255)
                g = np.clip(base + np.random.randint(-20, 20), 0, 255)
                b = np.clip(base + np.random.randint(-20, 20), 0, 255)
                a = 200 + np.random.randint(0, 55)
                
                noiseImage.setPixel(x, y, QColor(r, g, b, a).rgba())
        
        return noiseImage
    
    def setBlurRadius(self, radius: int):
        if radius == self.blurRadius:
            return
        
        self.blurRadius = max(1, radius)
        if not self.originalImage.isNull():
            self.setImage(self.originalImage)
    
    def setTintColor(self, color: QColor):
        self.tintColor = QColor(color)
        self.device.update()
    
    def setLuminosityColor(self, color: QColor):
        self.luminosityColor = QColor(color)
        self.device.update()
    
    def isAvailable(self):
        """Check if acrylic effect is available on current platform"""
        # Acrylic is always "available" - we'll use fallbacks if needed
        return True
    
    def grabFromScreen(self, rect: QRect):
        """Grab image from screen with platform-specific methods"""
        try:
            # Platform-specific screen grabbing
            if self.platform_info['is_wayland']:
                self.grabFromScreenWayland(rect)
            elif self.platform_info['is_x11']:
                self.grabFromScreenX11(rect)
            elif self.platform_info['is_windows']:
                self.grabFromScreenWindows(rect)
            elif self.platform_info['is_macos']:
                self.grabFromScreenMacOS(rect)
            else:
                # Unknown platform, try generic method
                self.grabFromScreenGeneric(rect)
                
        except Exception as e:
            logError(f"Screen grab failed on {self.platform_info['display_server']}: {e}")
            self.createFallbackBackground(rect.size())
    
    def grabFromScreenWayland(self, rect: QRect):
        """Wayland-compatible screen grabbing with fallbacks"""
        try:
            # Method 1: Try widget-based grab (most likely to work)
            parent_window = self.device.window()
            if parent_window and parent_window.isVisible():
                # Grab the window itself
                pixmap = parent_window.grab()
                if not pixmap.isNull():
                    # Convert global coordinates to widget-relative
                    global_pos = self.device.mapToGlobal(rect.topLeft())
                    window_pos = parent_window.mapFromGlobal(global_pos)
                    
                    # Create a rect in window coordinates
                    window_rect = QRect(window_pos, rect.size())
                    
                    # Ensure rect is within window bounds
                    if parent_window.rect().contains(window_rect):
                        cropped = pixmap.copy(window_rect)
                        if not cropped.isNull():
                            self.setImage(cropped)
                            self.using_fallback = False
                            return
            
            # Method 2: Use QScreen.grabWindow with 0 (root window)
            screen = QApplication.primaryScreen()
            if screen:
                # Get screen geometry
                screen_geometry = screen.geometry()
                
                # Convert widget coordinates to global screen coordinates
                global_top_left = self.device.mapToGlobal(rect.topLeft())
                global_rect = QRect(global_top_left, rect.size())
                
                # Ensure the rect is within screen bounds
                if screen_geometry.contains(global_rect):
                    # Try to grab from screen
                    pixmap = screen.grabWindow(0, 
                        global_rect.x(), 
                        global_rect.y(), 
                        rect.width(), 
                        rect.height())
                    
                    if not pixmap.isNull():
                        self.setImage(pixmap)
                        self.using_fallback = False
                        return
            
            # Method 3: Create acrylic fallback
            self.createFallbackBackground(rect.size())
            self.using_fallback = True
            logInfo("Using acrylic fallback on Wayland")
            
        except Exception as e:
            logError(f"Wayland screen grab failed: {e}")
            self.createFallbackBackground(rect.size())
            self.using_fallback = True
    
    def grabFromScreenX11(self, rect: QRect):
        """X11 screen grabbing method"""
        try:
            screen = QApplication.primaryScreen()
            if not screen:
                raise Exception("No screen available")
            
            # Convert to global coordinates
            global_top_left = self.device.mapToGlobal(rect.topLeft())
            
            # Grab from screen
            pixmap = screen.grabWindow(
                0,  # Root window
                global_top_left.x(),
                global_top_left.y(),
                rect.width(),
                rect.height()
            )
            
            if not pixmap.isNull():
                self.setImage(pixmap)
                self.using_fallback = False
            else:
                raise Exception("Grab returned null pixmap")
                
        except Exception as e:
            logError(f"X11 screen grab failed: {e}")
            self.createFallbackBackground(rect.size())
            self.using_fallback = True
    
    def grabFromScreenWindows(self, rect: QRect):
        """Windows screen grabbing method"""
        try:
            # Windows typically works with the standard method
            screen = QApplication.primaryScreen()
            global_top_left = self.device.mapToGlobal(rect.topLeft())
            
            pixmap = screen.grabWindow(
                0,
                global_top_left.x(),
                global_top_left.y(),
                rect.width(),
                rect.height()
            )
            
            if not pixmap.isNull():
                self.setImage(pixmap)
                self.using_fallback = False
            else:
                # Try alternative method for Windows
                self.grabFromScreenGeneric(rect)
                
        except Exception as e:
            logError(f"Windows screen grab failed: {e}")
            self.createFallbackBackground(rect.size())
            self.using_fallback = True
    
    def grabFromScreenMacOS(self, rect: QRect):
        """macOS screen grabbing method"""
        try:
            # macOS typically uses Quartz
            screen = QApplication.primaryScreen()
            global_top_left = self.device.mapToGlobal(rect.topLeft())
            
            pixmap = screen.grabWindow(
                0,
                int(global_top_left.x()),
                int(global_top_left.y()),
                rect.width(),
                rect.height()
            )
            
            if not pixmap.isNull():
                self.setImage(pixmap)
                self.using_fallback = False
            else:
                # Create acrylic fallback for macOS
                self.createFallbackBackground(rect.size())
                self.using_fallback = True
                
        except Exception as e:
            logError(f"macOS screen grab failed: {e}")
            self.createFallbackBackground(rect.size())
            self.using_fallback = True
    
    def grabFromScreenGeneric(self, rect: QRect):
        """Generic screen grabbing method as last resort"""
        try:
            # Try to grab the widget's parent window
            parent = self.device.window()
            if parent:
                pixmap = parent.grab(rect)
                if not pixmap.isNull():
                    self.setImage(pixmap)
                    self.using_fallback = False
                    return
            
            # Create fallback
            self.createFallbackBackground(rect.size())
            self.using_fallback = True
            
        except Exception as e:
            logError(f"Generic screen grab failed: {e}")
            self.createFallbackBackground(rect.size())
            self.using_fallback = True
    
    def createFallbackBackground(self, size):
        """Create a fallback acrylic-like background when screen grab fails"""
        try:
            pixmap = QPixmap(size)
            pixmap.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Create a subtle gradient
            gradient = QLinearGradient(0, 0, size.width(), size.height())
            gradient.setColorAt(0, QColor(245, 245, 245, 180))
            gradient.setColorAt(0.5, QColor(240, 240, 240, 160))
            gradient.setColorAt(1, QColor(235, 235, 235, 180))
            
            painter.fillRect(QRect(0, 0, size.width(), size.height()), gradient)
            
            # Add noise texture
            painter.setOpacity(self.noiseOpacity)
            noise_rect = QRect(0, 0, size.width(), size.height())
            painter.drawImage(noise_rect, self.noiseImage)
            
            painter.end()
            
            self.setImage(pixmap)
            self.using_fallback = True
            
        except Exception as e:
            logError(f"Fallback background creation failed: {e}")
            # Ultimate fallback - solid color
            fallback = QPixmap(size)
            fallback.fill(QColor(240, 240, 240, 200))
            self.setImage(fallback)
            self.using_fallback = True
    
    def setImage(self, image: Union[str, QImage, QPixmap]):
        """Set blurred image with error handling"""
        try:
            # Convert to QPixmap
            if isinstance(image, str):
                if os.path.exists(image):
                    pixmap = QPixmap(image)
                else:
                    raise FileNotFoundError(f"Image file not found: {image}")
            elif isinstance(image, QImage):
                pixmap = QPixmap.fromImage(image)
            elif isinstance(image, QPixmap):
                pixmap = image
            else:
                raise TypeError(f"Unsupported image type: {type(image)}")
            
            self.originalImage = pixmap
            
            # Apply blur if we have a valid image and blur radius > 0
            if not pixmap.isNull() and self.blurRadius > 0:
                self.image = GaussianBlurUtils.gaussianBlur(pixmap, self.blurRadius)
            else:
                self.image = pixmap
            
            self.device.update()
            
        except Exception as e:
            logError(f"Image processing failed: {e}")
            # Create a simple fallback
            fallback = QPixmap(100, 100)
            fallback.fill(QColor(200, 200, 200, 200))
            self.image = fallback
            self.device.update()
    
    def setClipPath(self, path: QPainterPath):
        self.clipPath = path
        self.device.update()
    
    def textureImage(self):
        """Create acrylic texture image"""
        texture = QImage(64, 64, QImage.Format.Format_ARGB32_Premultiplied)
        texture.fill(self.luminosityColor)
        
        # Paint tint color
        painter = QPainter(texture)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.fillRect(texture.rect(), self.tintColor)
        
        # Paint noise
        painter.setOpacity(self.noiseOpacity)
        painter.drawImage(texture.rect(), self.noiseImage)
        painter.end()
        
        return texture
    
    def paint(self):
        """Paint the acrylic effect"""
        device = self.device
        
        painter = QPainter(device)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if not self.clipPath.isEmpty():
            painter.setClipPath(self.clipPath)
        
        # Paint blurred background image
        if not self.image.isNull():
            # Scale image to fit while maintaining aspect ratio
            scaled_image = self.image.scaled(
                device.size(), 
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            
            # Center the image
            x = (device.width() - scaled_image.width()) // 2
            y = (device.height() - scaled_image.height()) // 2
            
            painter.drawPixmap(x, y, scaled_image)
        
        # Paint acrylic texture overlay
        painter.fillRect(device.rect(), QBrush(self.textureImage()))
        
        painter.end()


class AcrylicEffect:
    """Main acrylic effect class for cross-platform compatibility"""
    
    def __init__(self, widget: QWidget, blurRadius: int = 15, 
                 tintColor: QColor = QColor(242, 242, 242, 150),
                 luminosityColor: QColor = QColor(255, 255, 255, 10),
                 noiseOpacity: float = 0.03):
        """
        Apply acrylic effect to any widget with cross-platform compatibility
        
        Parameters:
        -----------
        widget: QWidget
            The widget to apply the acrylic effect to
        blurRadius: int
            Radius for the blur effect (0 for no blur)
        tintColor: QColor  
            Tint color for the acrylic effect
        luminosityColor: QColor
            Luminosity layer color
        noiseOpacity: float
            Opacity for the noise texture
        """
        self.widget = widget
        self.platform_info = PlatformDetector.detect_platform()
        
        self.acrylicBrush = AcrylicBrush(
            device=widget,
            blurRadius=blurRadius,
            tintColor=tintColor,
            luminosityColor=luminosityColor,
            noiseOpacity=noiseOpacity
        )
        
        # Set widget attributes for transparency
        self.widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.widget.setAutoFillBackground(False)
        
        logInfo(f"AcrylicEffect applied to {widget.objectName() or widget.__class__.__name__} "
               f"on {self.platform_info['system']}")
        
    def setBlurRadius(self, radius: int):
        """Set the blur radius"""
        self.acrylicBrush.setBlurRadius(radius)
        
    def setTintColor(self, color: QColor):
        """Set the tint color"""
        self.acrylicBrush.setTintColor(color)
        
    def setLuminosityColor(self, color: QColor):
        """Set the luminosity color"""
        self.acrylicBrush.setLuminosityColor(color)
        
    def setImage(self, image: Union[str, QImage, QPixmap]):
        """Set the background image to blur"""
        self.acrylicBrush.setImage(image)
        
    def grabFromScreen(self, rect: QRect = None):
        """Grab background from screen with platform compatibility"""
        if rect is None:
            rect = self.widget.rect()
        self.acrylicBrush.grabFromScreen(rect)
        
    def setClipPath(self, path: QPainterPath):
        """Set clip path for custom shapes"""
        self.acrylicBrush.setClipPath(path)
        
    def paintEvent(self, event):
        """Call this in the widget's paintEvent"""
        self.acrylicBrush.paint()
        
    def applyToWidget(self):
        """Apply the acrylic effect to the widget"""
        # Store original paint event
        originalPaintEvent = self.widget.paintEvent
        
        def newPaintEvent(event):
            # Paint acrylic effect first
            self.paintEvent(event)
            # Then call original paint event if it exists
            if originalPaintEvent:
                originalPaintEvent(event)
            
        self.widget.paintEvent = newPaintEvent
        
        # Also handle resize events to update acrylic effect
        originalResizeEvent = self.widget.resizeEvent
        
        def newResizeEvent(event):
            # Update acrylic on resize
            if originalResizeEvent:
                originalResizeEvent(event)
            # Regrab screen if using fallback
            if hasattr(self.acrylicBrush, 'using_fallback') and self.acrylicBrush.using_fallback:
                self.grabFromScreen()
            
        self.widget.resizeEvent = newResizeEvent
        
    def isUsingFallback(self):
        """Check if acrylic is using fallback mode"""
        return getattr(self.acrylicBrush, 'using_fallback', False)
    
    def getPlatformInfo(self):
        """Get current platform information"""
        return self.platform_info
    
    @staticmethod
    def getDominantColor(imagePath: str, defaultColor=(24, 24, 24)):
        """Get dominant color from an image"""
        return DominantColor.getDominantColor(imagePath, defaultColor)
    
    @staticmethod
    def createGaussianBlur(image, blurRadius=18, brightFactor=1, blurPicSize=None):
        """Static method to create Gaussian blur"""
        return GaussianBlurUtils.gaussianBlur(image, blurRadius, brightFactor, blurPicSize)


# Convenience function for easy application
def applyAcrylicEffect(widget: QWidget, blurRadius: int = 15, 
                      tintColor: QColor = None,
                      luminosityColor: QColor = None,
                      noiseOpacity: float = 0.03) -> AcrylicEffect:
    """
    Convenience function to apply acrylic effect to a widget
    
    Parameters:
    -----------
    widget: QWidget
        Widget to apply effect to
    blurRadius: int
        Blur radius (0 for no blur)
    tintColor: QColor
        Tint color (default: light gray with transparency)
    luminosityColor: QColor
        Luminosity color (default: white with slight transparency)
    noiseOpacity: float
        Noise texture opacity
    
    Returns:
    --------
    AcrylicEffect: The created acrylic effect instance
    """
    if tintColor is None:
        tintColor = QColor(242, 242, 242, 150)
    if luminosityColor is None:
        luminosityColor = QColor(255, 255, 255, 10)
    
    effect = AcrylicEffect(
        widget=widget,
        blurRadius=blurRadius,
        tintColor=tintColor,
        luminosityColor=luminosityColor,
        noiseOpacity=noiseOpacity
    )
    
    effect.applyToWidget()
    return effect