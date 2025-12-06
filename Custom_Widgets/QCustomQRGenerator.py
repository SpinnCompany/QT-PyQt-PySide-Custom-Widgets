import os
import qrcode
import io
import tempfile
from decimal import Decimal
from qtpy.QtCore import Qt, QSize, QRect, Property, QPoint
from qtpy.QtWidgets import (QWidget, QStyleOption, QStyle, QApplication, QFileDialog, QLabel, QVBoxLayout)
from qtpy.QtGui import QPainter, QColor, QPaintEvent, QPixmap, QIcon, QPalette
# Import your custom utilities
from Custom_Widgets.Log import *
from Custom_Widgets.Utils import is_in_designer
from Custom_Widgets.QCustomTheme import QCustomTheme

# Import advanced QR code features
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, 
    RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import (
    SolidFillColorMask, RadialGradiantColorMask, SquareGradiantColorMask,
    HorizontalGradiantColorMask, VerticalGradiantColorMask
)

class QCustomQRGenerator(QWidget):
    """
    A customizable QR code generator widget for Qt Designer.
    Uses QWidget with QLabel to display QR codes with customization through properties.
    """
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/qr_code_scanner.png")
    WIDGET_TOOLTIP = "A customizable QR code generator widget"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomQRGenerator' name='customQRGenerator'>
            <property name='geometry'>
                <rect>
                    <x>0</x>
                    <y>0</y>
                    <width>300</width>
                    <height>300</height>
                </rect>
            </property>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomQRGenerator"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create QLabel for displaying QR code
        self.qrLabel = QLabel(self)
        self.qrLabel.setAlignment(Qt.AlignCenter)
        self.qrLabel.setScaledContents(False)
        
        # Set up layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.qrLabel)
        
        # Get application palette for default colors
        app_palette = QApplication.palette()
        
        # Private attributes with default values from application palette
        self._data = "https://example.com"
        self._version = None  # Auto-detect version
        self._errorCorrection = "H"
        self._boxSize = 10
        self._border = 4
        
        # Use text color for fill and window color for background
        self._fillColor = app_palette.color(QPalette.Text)
        self._backgroundColor = app_palette.color(QPalette.Window)
        
        # Track if colors are from palette (for theme change detection)
        self._fillColorFromPalette = True
        self._backgroundColorFromPalette = True
        self._gradientStartColorFromPalette = True
        self._gradientEndColorFromPalette = True
        
        # Advanced styling properties - use accent colors from palette
        self._moduleDrawer = "square"
        self._colorMask = "solid"
        
        # Use highlight color for gradient start and a complementary color for gradient end
        self._gradientStartColor = app_palette.color(QPalette.Highlight)
        self._gradientEndColor = self._getComplementaryColor(self._gradientStartColor)
        
        self._sizeRatio = 1.0
        self._embedImage = False
        self._embeddedImageIcon = QIcon()
        
        # Caching
        self._currentQRPixmap = None
        self._cacheEnabled = True
        self._lastSettingsHash = ""

        self.themeEngine = QCustomTheme()
        self.defaultTheme = self.themeEngine.theme
        self.defaultIconsColor = self.themeEngine.iconsColor
        # self.themeEngine.onThemeChanged.connect(self.refreshQRCode)
        self.themeEngine.onThemeChangeComplete.connect(self.refreshQRCode)
        
        # Widget setup
        self.setMinimumSize(100, 100)
        self.refreshQRCode()
        
        # Generate QR code immediately for both designer and runtime
        self.generateQRCode()
    
    def _getComplementaryColor(self, color):
        """Get a complementary color for gradient end."""
        # Simple complementary color calculation
        h, s, v, a = color.getHsvF()
        complementary_h = (h + 0.5) % 1.0  # Opposite hue
        complementary = QColor.fromHsvF(complementary_h, s, v, a)
        return complementary
    
    def _getAccentColorsFromPalette(self):
        """Get a set of attractive accent colors from the application palette."""
        palette = QApplication.palette()
        accents = [
            palette.color(QPalette.Highlight),  # Primary accent
            palette.color(QPalette.Link),       # Link color
            palette.color(QPalette.AlternateBase),  # Alternate base
        ]
        
        # If we need more colors, create some variations
        base_color = palette.color(QPalette.Highlight)
        if len(accents) < 2:
            # Create lighter and darker variations
            lighter = base_color.lighter(150)
            darker = base_color.darker(150)
            accents.extend([lighter, darker])
        
        return accents
    
    def _getSettingsHash(self):
        """Generate a hash of current settings for caching."""
        embedded_icon_name = self._embeddedImageIcon.name() if not self._embeddedImageIcon.isNull() else ""
        settings = f"{self._data}_{self._version}_{self._errorCorrection}_{self._boxSize}_{self._border}_{self._fillColor.name()}_{self._backgroundColor.name()}_{self._moduleDrawer}_{self._colorMask}_{self._sizeRatio}_{self._embedImage}_{embedded_icon_name}"
        return hash(settings)
    
    def _getModuleDrawer(self):
        """Get the module drawer instance based on selection."""
        drawer_map = {
            "square": SquareModuleDrawer(),
            "gapped_square": GappedSquareModuleDrawer(size_ratio=Decimal(str(self._sizeRatio))),
            "circle": CircleModuleDrawer(),
            "rounded": RoundedModuleDrawer(),
            "vertical_bars": VerticalBarsDrawer(),
            "horizontal_bars": HorizontalBarsDrawer()
        }
        
        return drawer_map.get(self._moduleDrawer, SquareModuleDrawer())
    
    def _getColorMask(self):
        """Get the color mask instance based on selection."""
        # Convert QColor to RGB tuples
        back_color = (self._backgroundColor.red(), self._backgroundColor.green(), self._backgroundColor.blue())
        
        # For gradient masks, we need to use the gradient colors
        gradient_start = (self._gradientStartColor.red(), self._gradientStartColor.green(), self._gradientStartColor.blue())
        gradient_end = (self._gradientEndColor.red(), self._gradientEndColor.green(), self._gradientEndColor.blue())
        
        mask_map = {
            "solid": SolidFillColorMask(
                back_color=back_color, 
                front_color=(self._fillColor.red(), self._fillColor.green(), self._fillColor.blue())
            ),
            "radial": RadialGradiantColorMask(
                back_color=back_color, 
                center_color=gradient_start, 
                edge_color=gradient_end
            ),
            "square": SquareGradiantColorMask(
                back_color=back_color, 
                center_color=gradient_start, 
                edge_color=gradient_end
            ),
            "horizontal": HorizontalGradiantColorMask(
                back_color=back_color, 
                left_color=gradient_start, 
                right_color=gradient_end
            ),
            "vertical": VerticalGradiantColorMask(
                back_color=back_color, 
                top_color=gradient_start, 
                bottom_color=gradient_end
            )
        }
        
        return mask_map.get(self._colorMask, SolidFillColorMask(back_color=back_color, front_color=(0, 0, 0)))
    
    def _saveIconToTempFile(self):
        """Save QIcon to a temporary file for QR code generation."""
        if self._embedImage and not self._embeddedImageIcon.isNull():
            try:
                # Get pixmap from icon
                pixmap = self._embeddedImageIcon.pixmap(512, 512)
                
                if not pixmap.isNull():
                    # Create a temporary file
                    tfile = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                    tfile.close()
                    
                    temp_file_path = tfile.name
                    
                    # Save pixmap to this path
                    if pixmap.save(temp_file_path, "PNG"):
                        return temp_file_path
            except Exception as e:
                logError(f"Error saving icon to temp file: {str(e)}")
        return ""

    def generateQRCode(self):
        """Generate the QR code pixmap and set it to the QLabel."""
        try:
            if not self._data.strip():
                self._currentQRPixmap = None 
                self.qrLabel.clear()
                self.qrLabel.setText("No Data")
                return
            
            # Check if we need advanced styling and transparency workaround
            use_advanced_styling = (self._colorMask != "solid" or 
                                  self._moduleDrawer != "square")
            has_transparency = self._backgroundColor.alpha() < 255
            needs_transparency_workaround = use_advanced_styling and has_transparency
            
            # Generate cache hash BEFORE any temporary modifications
            current_hash = self._getSettingsHash()
            
            # If we need transparency workaround, create a modified hash for caching
            if needs_transparency_workaround:
                # Create a modified settings string for cache that includes the workaround
                temp_background = QColor(self._backgroundColor)
                temp_background.setAlpha(255)
                workaround_settings = f"{current_hash}_workaround_{temp_background.name()}"
                current_hash = hash(workaround_settings)
            
            if self._cacheEnabled and self._lastSettingsHash == current_hash and self._currentQRPixmap:
                logInfo("Using cached QR code")
                self.qrLabel.setPixmap(self._currentQRPixmap)
                self.resizeQR()
                return
            
            logInfo(f"Generating new QR code with fill: {self._fillColor.name()}, background: {self._backgroundColor.name()}")
            
            # Create QR code instance
            qr = qrcode.QRCode(
                version=self._version if self._version else None,
                error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{self._errorCorrection}"),
                box_size=self._boxSize,
                border=self._border,
            )
            
            qr.add_data(self._data)
            qr.make(fit=True)

            # Handle transparency workaround for gradient masks
            temp_background_used = None
            original_background = None
            
            if needs_transparency_workaround:
                logWarning("Transparency is not supported with gradient color masks. Using workaround.")
                # Create a temporary background color without transparency for gradient generation
                temp_background_used = QColor(self._backgroundColor)
                temp_background_used.setAlpha(255)
                original_background = self._backgroundColor
                self._backgroundColor = temp_background_used
            
            if use_advanced_styling:
                # Use advanced styling with StyledPilImage
                module_drawer = self._getModuleDrawer()
                color_mask = self._getColorMask()
                
                logInfo(f"Using advanced styling: {self._colorMask} with module drawer: {self._moduleDrawer}")
                
                qr_img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=module_drawer,
                    color_mask=color_mask
                )
                
                # Restore original background color if we temporarily changed it
                if temp_background_used is not None:
                    self._backgroundColor = original_background
                    
                    # Now convert to RGBA and apply transparency manually
                    qr_img = qr_img.convert("RGBA")
                    datas = qr_img.getdata()
                    
                    new_data = []
                    target_back_color = (temp_background_used.red(), temp_background_used.green(), temp_background_used.blue())
                    
                    for item in datas:
                        # Change temporary background color pixels to transparent
                        if item[:3] == target_back_color:
                            new_data.append((*target_back_color, 0))
                        else:
                            new_data.append(item)
                    
                    qr_img.putdata(new_data)
                    
            else:
                # Use basic QR code generation
                logInfo(f"Using basic styling with fill: {self._fillColor.name()}, background: {self._backgroundColor.name()}")
                
                # For basic styling with transparency, we need to handle it differently
                if has_transparency:
                    # Generate with white background first, then make transparent
                    qr_img = qr.make_image(
                        fill_color=self._fillColor.name(),
                        back_color="white"  # Generate with white first
                    )
                    qr_img = qr_img.convert("RGBA")
                    
                    # Make white pixels transparent
                    datas = qr_img.getdata()
                    new_data = []
                    for item in datas:
                        # Change white pixels to transparent
                        if item[0] == 255 and item[1] == 255 and item[2] == 255:
                            new_data.append((255, 255, 255, 0))
                        else:
                            new_data.append(item)
                    qr_img.putdata(new_data)
                else:
                    # No transparency needed, use normal generation
                    qr_img = qr.make_image(
                        fill_color=self._fillColor.name(),
                        back_color=self._backgroundColor.name()
                    )

            # Handle embedded image
            if self._embedImage and not self._embeddedImageIcon.isNull():
                embedded_image_path = self._saveIconToTempFile()
                if embedded_image_path:
                    try:
                        from PIL import Image
                        
                        # Ensure image is in RGBA mode for transparency support
                        if qr_img.mode != 'RGBA':
                            qr_img = qr_img.convert('RGBA')
                        
                        # Open and process the logo
                        logo = Image.open(embedded_image_path)
                        qr_w, qr_h = qr_img.size

                        # Resize logo
                        logo_size = int(qr_w / 4)
                        logo = logo.resize((logo_size, logo_size))
                        
                        # Convert logo to RGBA if not already
                        if logo.mode != 'RGBA':
                            logo = logo.convert('RGBA')
                        
                        pos = ((qr_w - logo_size) // 2, (qr_h - logo_size) // 2)

                        # Paste logo with transparency
                        qr_img.paste(logo, pos, logo)
                            
                        logInfo("Logo successfully embedded in QR code")
                        
                    except Exception as e:
                        logError(f"Failed to add logo: {e}")
                    
                    # Cleanup temp file
                    try:
                        os.remove(embedded_image_path)
                    except:
                        pass

            # Convert PIL Image to QPixmap
            img_bytes = io.BytesIO()
            
            # Save as PNG (handles both RGB and RGBA)
            qr_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            pixmap = QPixmap()
            if pixmap.loadFromData(img_bytes.getvalue(), "PNG"):
                self._currentQRPixmap = pixmap
                self.qrLabel.setPixmap(pixmap)
                self._lastSettingsHash = current_hash  # Update cache hash
                logInfo("QR code generated successfully")
            else:
                self._currentQRPixmap = None
                self.qrLabel.clear()
                self.qrLabel.setText("QR Error")
            
            self.resizeQR()

        except Exception as e:
            logError(f"Error generating QR code: {str(e)}")
            self._currentQRPixmap = None
            self.qrLabel.clear()
            self.qrLabel.setText("QR Error")

    def resizeQR(self):
        """
        Scale pixmap to fit while maintaining aspect ratio
        """
        if self._currentQRPixmap and not self._currentQRPixmap.isNull():
            scaled_pixmap = self._currentQRPixmap.scaled(
                self.qrLabel.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.qrLabel.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        """
        Handle resize to maintain aspect ratio.
        """
        super().resizeEvent(event)
        self.resizeQR()

    def refreshQRCode(self):
        """Refresh QR code when theme changes, only if colors are from palette."""
        logInfo("Theme changed detected in QCustomQRGenerator")
        
        # Get current palette
        current_palette = QApplication.palette()
        
        # Update colors only if they were originally from palette
        if self._fillColorFromPalette:
            self._fillColor = current_palette.color(QPalette.Text)
            logInfo(f"Updated fill color from palette: {self._fillColor.name()}")
        
        if self._backgroundColorFromPalette:
            self._backgroundColor = current_palette.color(QPalette.Window)
            logInfo(f"Updated background color from palette: {self._backgroundColor.name()}")
        
        if self._gradientStartColorFromPalette:
            self._gradientStartColor = current_palette.color(QPalette.Highlight)
            logInfo(f"Updated gradient start color from palette: {self._gradientStartColor.name()}")
        
        if self._gradientEndColorFromPalette:
            # Recalculate complementary color based on new gradient start
            self._gradientEndColor = self._getComplementaryColor(self._gradientStartColor)
            logInfo(f"Updated gradient end color from palette: {self._gradientEndColor.name()}")
        
        # Regenerate QR code with new colors
        self.generateQRCode()

    def saveQRCode(self, file_path=None):
        """Save the generated QR code to file."""
        try:
            if not self._currentQRPixmap or self._currentQRPixmap.isNull():
                logWarning("No QR code to save")
                return False
            
            if not file_path:
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save QR Code",
                    f"qrcode_{os.path.basename(self._data[:20]) if self._data else 'qrcode'}.png",
                    "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)"
                )
            
            if file_path:
                # For better quality, regenerate the QR code at high resolution for saving
                original_box_size = self._boxSize
                original_border = self._border
                
                # Temporarily increase resolution for saving
                self._boxSize = 20
                self._border = 8
                self.generateQRCode()
                
                # Save high quality version
                success = self._currentQRPixmap.save(file_path)
                
                # Restore original settings
                self._boxSize = original_box_size
                self._border = original_border
                self.generateQRCode()
                
                if success:
                    logInfo(f"High quality QR code saved to: {file_path}")
                    return True
                else:
                    logError(f"Failed to save QR code to: {file_path}")
                    return False
                
        except Exception as e:
            logError(f"Error saving QR code: {str(e)}")
            return False
        
        return False

    def getQRCodePixmap(self):
        """Get the current QR code as QPixmap."""
        return self._currentQRPixmap
    
    def copyToClipboard(self):
        """Copy the QR code to clipboard."""
        try:
            if self._currentQRPixmap and not self._currentQRPixmap.isNull():
                QApplication.clipboard().setPixmap(self._currentQRPixmap)
                logInfo("QR code copied to clipboard")
                return True
            else:
                logWarning("No QR code to copy")
                return False
        except Exception as e:
            logError(f"Error copying to clipboard: {str(e)}")
            return False
    
    def clearCache(self):
        """Clear the QR code cache."""
        self._currentQRPixmap = None
        self._lastSettingsHash = ""
        self.generateQRCode()
    
    def setEmbeddedImageFromFileDialog(self):
        """Open a file dialog to set the embedded image."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Choose Embedded Image", 
            "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        if file_path:
            self.embeddedImageIcon = QIcon(file_path)
            return True
        return False

    # Property getters and setters
    @Property(str)
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = str(value)
        self.generateQRCode()
    
    @Property(int)
    def version(self):
        return self._version if self._version else 0
    
    @version.setter
    def version(self, value):
        self._version = max(1, min(40, value)) if value else None
        self.generateQRCode()
    
    @Property(str)
    def errorCorrection(self):
        return self._errorCorrection
    
    @errorCorrection.setter
    def errorCorrection(self, value):
        if value in ["L", "M", "Q", "H"]:
            self._errorCorrection = value
            self.generateQRCode()
    
    @Property(int)
    def boxSize(self):
        return self._boxSize
    
    @boxSize.setter
    def boxSize(self, value):
        self._boxSize = max(1, value)
        self.generateQRCode()
    
    @Property(int)
    def border(self):
        return self._border
    
    @border.setter
    def border(self, value):
        self._border = max(0, value)
        self.generateQRCode()
    
    @Property(QColor)
    def fillColor(self):
        return self._fillColor
    
    @fillColor.setter
    def fillColor(self, value):
        self._fillColor = value
        # If user sets a custom color, mark it as not from palette
        self._fillColorFromPalette = False
        self.generateQRCode()
    
    @Property(QColor)
    def backgroundColor(self):
        return self._backgroundColor
    
    @backgroundColor.setter
    def backgroundColor(self, value):
        self._backgroundColor = value
        # If user sets a custom color, mark it as not from palette
        self._backgroundColorFromPalette = False
        self.generateQRCode()
    
    @Property(bool)
    def cacheEnabled(self):
        return self._cacheEnabled
    
    @cacheEnabled.setter
    def cacheEnabled(self, value):
        self._cacheEnabled = bool(value)
        if not value:
            self.clearCache()
    
    # Advanced properties
    @Property(str)
    def moduleDrawer(self):
        return self._moduleDrawer
    
    @moduleDrawer.setter
    def moduleDrawer(self, value):
        if value in ["square", "gapped_square", "circle", "rounded", "vertical_bars", "horizontal_bars"]:
            self._moduleDrawer = value
            self.generateQRCode()
    
    @Property(str)
    def colorMask(self):
        return self._colorMask
    
    @colorMask.setter
    def colorMask(self, value):
        if value in ["solid", "radial", "square", "horizontal", "vertical"]:
            self._colorMask = value
            self.generateQRCode()
    
    @Property(QColor)
    def gradientStartColor(self):
        return self._gradientStartColor
    
    @gradientStartColor.setter
    def gradientStartColor(self, value):
        self._gradientStartColor = value
        # If user sets a custom color, mark it as not from palette
        self._gradientStartColorFromPalette = False
        self.generateQRCode()
    
    @Property(QColor)
    def gradientEndColor(self):
        return self._gradientEndColor
    
    @gradientEndColor.setter
    def gradientEndColor(self, value):
        self._gradientEndColor = value
        # If user sets a custom color, mark it as not from palette
        self._gradientEndColorFromPalette = False
        self.generateQRCode()
    
    @Property(float)
    def sizeRatio(self):
        return self._sizeRatio
    
    @sizeRatio.setter
    def sizeRatio(self, value):
        self._sizeRatio = max(0.1, min(1.0, value))
        self.generateQRCode()
    
    @Property(bool)
    def embedImage(self):
        return self._embedImage
    
    @embedImage.setter
    def embedImage(self, value):
        self._embedImage = bool(value)
        self.generateQRCode()
    
    @Property(QIcon)
    def embeddedImageIcon(self):
        return self._embeddedImageIcon
    
    @embeddedImageIcon.setter
    def embeddedImageIcon(self, value):
        if isinstance(value, QIcon):
            self._embeddedImageIcon = value
        elif isinstance(value, str):
            self._embeddedImageIcon = QIcon(value)
        else:
            self._embeddedImageIcon = QIcon()
        self.generateQRCode()