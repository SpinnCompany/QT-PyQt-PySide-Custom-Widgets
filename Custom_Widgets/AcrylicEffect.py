# coding:utf-8
import warnings
import os
from math import floor
from io import BytesIO
from typing import Union

import numpy as np
from colorthief import ColorThief
from PIL import Image
from qtpy.QtCore import Qt, QThread, Signal, QRect, QIODevice, QBuffer
from qtpy.QtGui import QBrush, QColor, QImage, QPainter, QPixmap, QPainterPath
from qtpy.QtWidgets import QLabel, QApplication, QWidget
from scipy.ndimage.filters import gaussian_filter

from Custom_Widgets.Log import *

class GaussianBlurUtils:
    """Utility class for Gaussian blur operations"""
    
    @staticmethod
    def gaussianBlur(image, blurRadius=18, brightFactor=1, blurPicSize=None):
        if isinstance(image, str) and not image.startswith(':'):
            image = Image.open(image)
        else:
            image = GaussianBlurUtils.fromQpixmap(QPixmap(image))

        if blurPicSize:
            # adjust image size to reduce computation
            w, h = image.size
            ratio = min(blurPicSize[0] / w, blurPicSize[1] / h)
            w_, h_ = w * ratio, h * ratio

            if w_ < w:
                image = image.resize((int(w_), int(h_)), Image.ANTIALIAS)

        image = np.array(image)

        # handle gray image
        if len(image.shape) == 2:
            image = np.stack([image, image, image], axis=-1)

        # blur each channel
        for i in range(3):
            image[:, :, i] = gaussian_filter(
                image[:, :, i], blurRadius) * brightFactor

        # convert ndarray to QPixmap
        h, w, c = image.shape
        if c == 3:
            format = QImage.Format_RGB888
        else:
            format = QImage.Format_RGBA8888

        return QPixmap.fromImage(QImage(image.data, w, h, c*w, format))

    @staticmethod
    def fromQpixmap(im: Union[QImage, QPixmap]):
        """
        :param im: QImage or PIL ImageQt object
        """
        buffer = QBuffer()
        buffer.open(QIODevice.OpenModeFlag.ReadWrite)

        # preserve alpha channel with png
        # otherwise ppm is more friendly with Image.open
        if im.hasAlphaChannel():
            im.save(buffer, "png")
        else:
            im.save(buffer, "ppm")

        b = BytesIO()
        b.write(buffer.data())
        buffer.close()
        b.seek(0)

        return Image.open(b)


class DominantColor:
    """Dominant color class"""

    @classmethod
    def getDominantColor(cls, imagePath, defaultColor=(24, 24, 24)):
        """extract dominant color from image

        Parameters
        ----------
        imagePath: str
            image path
        defaultColor: tuple
            default color to return if extraction fails

        Returns
        -------
        r, g, b: int
            gray value of each color channel
        """
        try:
            if imagePath.startswith(':'):
                return defaultColor

            colorThief = ColorThief(imagePath)

            # scale image to speed up the computation speed
            if max(colorThief.image.size) > 400:
                colorThief.image = colorThief.image.resize((400, 400))

            palette = colorThief.get_palette(quality=9)

            # adjust the brightness of palette
            palette = cls.__adjustPaletteValue(palette)
            for rgb in palette[:]:
                h, s, v = cls.rgb2hsv(rgb)
                if h < 0.02:
                    palette.remove(rgb)
                    if len(palette) <= 2:
                        break

            palette = palette[:5]
            palette.sort(key=lambda rgb: cls.colorfulness(*rgb), reverse=True)

            return palette[0]
        except Exception:
            return defaultColor

    @classmethod
    def __adjustPaletteValue(cls, palette):
        """adjust the brightness of palette"""
        newPalette = []
        for rgb in palette:
            h, s, v = cls.rgb2hsv(rgb)
            if v > 0.9:
                factor = 0.8
            elif 0.8 < v <= 0.9:
                factor = 0.9
            elif 0.7 < v <= 0.8:
                factor = 0.95
            else:
                factor = 1
            v *= factor
            newPalette.append(cls.hsv2rgb(h, s, v))

        return newPalette

    @staticmethod
    def rgb2hsv(rgb):
        """convert rgb to hsv"""
        r, g, b = [i / 255 for i in rgb]
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        s = 0 if mx == 0 else df / mx
        v = mx
        return (h, s, v)

    @staticmethod
    def hsv2rgb(h, s, v):
        """convert hsv to rgb"""
        h60 = h / 60.0
        h60f = floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return (r, g, b)

    @staticmethod
    def colorfulness(r: int, g: int, b: int):
        rg = np.absolute(r - g)
        yb = np.absolute(0.5 * (r + g) - b)

        # Compute the mean and standard deviation of both `rg` and `yb`.
        rg_mean, rg_std = (np.mean(rg), np.std(rg))
        yb_mean, yb_std = (np.mean(yb), np.std(yb))

        # Combine the mean and standard deviations.
        std_root = np.sqrt((rg_std ** 2) + (yb_std ** 2))
        mean_root = np.sqrt((rg_mean ** 2) + (yb_mean ** 2))

        return std_root + (0.3 * mean_root)


class BlurCoverThread(QThread):
    """Blur album cover thread"""

    blurFinished = Signal(QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.imagePath = ""
        self.blurRadius = 7
        self.maxSize = None

    def run(self):
        if not self.imagePath:
            return

        try:
            pixmap = GaussianBlurUtils.gaussianBlur(
                self.imagePath, self.blurRadius, 0.85, self.maxSize)
            self.blurFinished.emit(pixmap)
        except Exception:
            # Fallback to original image if blur fails
            pixmap = QPixmap(self.imagePath)
            self.blurFinished.emit(pixmap)

    def blur(self, imagePath: str, blurRadius=6, maxSize: tuple = (450, 450)):
        self.imagePath = imagePath
        self.blurRadius = blurRadius
        self.maxSize = maxSize or self.maxSize
        self.start()


class AcrylicTextureLabel(QLabel):
    """Acrylic texture label"""

    def __init__(self, tintColor: QColor, luminosityColor: QColor, noiseOpacity=0.03, parent=None):
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
        
        # Create noise image if it doesn't exist
        self.noiseImage = self.createNoiseImage()
        
        self.setAttribute(Qt.WA_TranslucentBackground)

    def createNoiseImage(self):
        """Create a noise texture image programmatically"""
        size = 64
        noiseImage = QImage(size, size, QImage.Format_ARGB32)
        
        # Fill with random noise
        for x in range(size):
            for y in range(size):
                # Create subtle noise (values between 200-255 for alpha)
                noise_value = np.random.randint(200, 256)
                noiseImage.setPixel(x, y, QColor(noise_value, noise_value, noise_value, noise_value).rgba())
        
        return noiseImage

    def setTintColor(self, color: QColor):
        self.tintColor = color
        self.update()

    def paintEvent(self, e):
        acrylicTexture = QImage(64, 64, QImage.Format_ARGB32_Premultiplied)

        # paint luminosity layer
        acrylicTexture.fill(self.luminosityColor)

        # paint tint color
        painter = QPainter(acrylicTexture)
        painter.fillRect(acrylicTexture.rect(), self.tintColor)

        # paint noise
        painter.setOpacity(self.noiseOpacity)
        painter.drawImage(acrylicTexture.rect(), self.noiseImage)

        acrylicBrush = QBrush(acrylicTexture)
        painter = QPainter(self)
        painter.fillRect(self.rect(), acrylicBrush)


class AcrylicBrush:
    """Acrylic brush"""

    def __init__(self, device: QWidget, blurRadius: int, tintColor=QColor(242, 242, 242, 150),
                 luminosityColor=QColor(255, 255, 255, 10), noiseOpacity=0.03):
        self.device = device
        self.blurRadius = blurRadius
        self.tintColor = QColor(tintColor)
        self.luminosityColor = QColor(luminosityColor)
        self.noiseOpacity = noiseOpacity
        
        # Create noise image programmatically instead of loading from file
        self.noiseImage = self.createNoiseImage()
        
        self.originalImage = QPixmap()
        self.image = QPixmap()
        self.clipPath = QPainterPath()

    def createNoiseImage(self):
        """Create a noise texture image programmatically"""
        size = 64
        noiseImage = QImage(size, size, QImage.Format_ARGB32)
        
        # Fill with random noise
        for x in range(size):
            for y in range(size):
                # Create subtle noise (values between 200-255 for alpha)
                noise_value = np.random.randint(200, 256)
                noiseImage.setPixel(x, y, QColor(noise_value, noise_value, noise_value, noise_value).rgba())
        
        return noiseImage

    def setBlurRadius(self, radius: int):
        if radius == self.blurRadius:
            return

        self.blurRadius = radius
        self.setImage(self.originalImage)

    def setTintColor(self, color: QColor):
        self.tintColor = QColor(color)
        self.device.update()

    def setLuminosityColor(self, color: QColor):
        self.luminosityColor = QColor(color)
        self.device.update()

    def isAvailable(self):
        return True

    def getScreenForWidget(self, widget):
        """Get the correct screen for a widget, handling multi-monitor setups"""
        try:
            # Get the widget's global position
            global_pos = widget.mapToGlobal(widget.rect().topLeft())
            
            # Find which screen contains this point
            app = QApplication.instance()
            for screen in app.screens():
                screen_geometry = screen.geometry()
                if screen_geometry.contains(global_pos):
                    return screen
            
            # Fallback to primary screen
            return app.primaryScreen()
        except Exception:
            return QApplication.primaryScreen()

    def grabFromScreen(self, rect: QRect):
        """grab image from screen with proper multi-monitor support

        Parameters
        ----------
        rect: QRect
            grabbed region in widget coordinates
        """
        try:
            # Get the correct screen for the widget
            screen = self.getScreenForWidget(self.device)
            if not screen:
                screen = QApplication.primaryScreen()

            # Convert widget coordinates to global screen coordinates
            global_top_left = self.device.mapToGlobal(rect.topLeft())
            global_bottom_right = self.device.mapToGlobal(rect.bottomRight())
            
            # Calculate global rectangle
            global_rect = QRect(global_top_left, global_bottom_right)
            
            # Get screen geometry in global coordinates
            screen_geometry = screen.geometry()
            
            # Adjust coordinates relative to the screen
            screen_x = global_rect.x() - screen_geometry.x()
            screen_y = global_rect.y() - screen_geometry.y()
            
            # Ensure we don't grab outside screen bounds
            screen_x = max(0, min(screen_x, screen_geometry.width() - rect.width()))
            screen_y = max(0, min(screen_y, screen_geometry.height() - rect.height()))
            
            # Grab from the correct screen with correct coordinates
            grabbed_pixmap = screen.grabWindow(
                0,  # Root window
                screen_x, 
                screen_y, 
                rect.width(), 
                rect.height()
            )
            
            self.setImage(grabbed_pixmap)
            
        except Exception as e:
            logError(f"Screen grab failed: {e}")
            # Fallback to a solid color if screen grab fails
            fallback_pixmap = QPixmap(rect.size())
            fallback_pixmap.fill(QColor(240, 240, 240))
            self.setImage(fallback_pixmap)

    def setImage(self, image: Union[str, QImage, QPixmap]):
        """set blurred image"""
        try:
            if isinstance(image, str):
                image = QPixmap(image)
            elif isinstance(image, QImage):
                image = QPixmap.fromImage(image)

            self.originalImage = image
            if not image.isNull():
                self.image = GaussianBlurUtils.gaussianBlur(image, self.blurRadius)
            else:
                # Create a fallback image if original is null
                fallback_pixmap = QPixmap(100, 100)
                fallback_pixmap.fill(QColor(200, 200, 200))
                self.image = GaussianBlurUtils.gaussianBlur(fallback_pixmap, self.blurRadius)

            self.device.update()
        except Exception as e:
            logError(f"Image processing failed: {e}")
            # Use original image as fallback if blur fails
            self.image = self.originalImage
            self.device.update()

    def setClipPath(self, path: QPainterPath):
        self.clipPath = path
        self.device.update()

    def textureImage(self):
        texture = QImage(64, 64, QImage.Format_ARGB32_Premultiplied)
        texture.fill(self.luminosityColor)

        # paint tint color
        painter = QPainter(texture)
        painter.fillRect(texture.rect(), self.tintColor)

        # paint noise
        painter.setOpacity(self.noiseOpacity)
        painter.drawImage(texture.rect(), self.noiseImage)

        return texture

    def paint(self):
        device = self.device

        painter = QPainter(device)
        painter.setRenderHints(QPainter.Antialiasing)

        if not self.clipPath.isEmpty():
            painter.setClipPath(self.clipPath)

        # paint image
        if not self.image.isNull():
            image = self.image.scaled(device.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, image)

        # paint acrylic texture
        painter.fillRect(device.rect(), QBrush(self.textureImage()))


class AcrylicEffect:
    """Main acrylic effect class that can be applied to any widget"""
    
    def __init__(self, widget: QWidget, blurRadius: int = 15, 
                 tintColor: QColor = QColor(242, 242, 242, 150),
                 luminosityColor: QColor = QColor(255, 255, 255, 10),
                 noiseOpacity: float = 0.03):
        """
        Apply acrylic effect to any widget
        
        Parameters:
        -----------
        widget: QWidget
            The widget to apply the acrylic effect to
        blurRadius: int
            Radius for the blur effect
        tintColor: QColor  
            Tint color for the acrylic effect
        luminosityColor: QColor
            Luminosity layer color
        noiseOpacity: float
            Opacity for the noise texture
        """
        self.widget = widget
        self.acrylicBrush = AcrylicBrush(
            device=widget,
            blurRadius=blurRadius,
            tintColor=tintColor,
            luminosityColor=luminosityColor,
            noiseOpacity=noiseOpacity
        )
        
        # Set widget attributes for transparency
        self.widget.setAttribute(Qt.WA_TranslucentBackground)
        self.widget.setAutoFillBackground(False)
        
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
        """Grab background from screen with multi-monitor support"""
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
            self.paintEvent(event)
            if originalPaintEvent:
                originalPaintEvent(event)
            
        self.widget.paintEvent = newPaintEvent
        
    @staticmethod
    def getDominantColor(imagePath: str, defaultColor=(24, 24, 24)):
        """Get dominant color from an image"""
        return DominantColor.getDominantColor(imagePath, defaultColor)