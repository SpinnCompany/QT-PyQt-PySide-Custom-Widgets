#source: https://github.com/Opticos/GWSL-Source/blob/master/blur.py , https://www.cnblogs.com/zhiyiYo/p/14659981.html , https://github.com/ifwe/digsby/blob/master/digsby/src/gui/vista.py
import platform
import ctypes

if platform.system() == 'Darwin':
    import objc
    from AppKit import *
    from qtpy.QtWidgets import QWidget


    def MacBlur(widget: QWidget, mask, Material=NSVisualEffectMaterialPopover, TitleBar=True):
        """
        Applies a macOS blur effect to the given widget using NSVisualEffectView.

        Args:
            widget: The PySide6/PyQt widget to which the blur effect is applied.
            mask: The widget whose window handle is used to apply the blur effect.
            Material: The type of blur material (default: NSVisualEffectMaterialPopover).
            TitleBar: Whether to adjust the title bar to appear transparent (default: True).
        """
        if not widget.isWindow():
            print("Blur effect can only be applied to top-level windows.")
            return
        
        if widget.hasBlur:
            return

        widget.hasBlur = True
        # Ensure the frame matches the widget's size
        frame = NSMakeRect(0, 0, mask.width(), mask.height())

        # Get the window handle using the mask's winId
        view = objc.objc_object(c_void_p=mask.winId().__int__())

        # Create the visual effect view (blur effect)
        visualEffectView = NSVisualEffectView.new()
        visualEffectView.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)  # Make it resizable
        visualEffectView.setFrame_(frame)  # Set the size to match the widget
        visualEffectView.setState_(NSVisualEffectStateActive)  # Activate the effect
        visualEffectView.setMaterial_(Material)  # Set the desired material
        visualEffectView.setBlendingMode_(NSVisualEffectBlendingModeBehindWindow)  # Ensure it blends correctly

        # Access the macOS window and its content view
        window = view.window()
        content = window.contentView()

        # Add the blur view behind the widget
        content.addSubview_(visualEffectView)

        # Optionally adjust the title bar appearance
        # if TitleBar:
        #     window.setTitlebarAppearsTransparent_(True)
        #     window.setStyleMask_(window.styleMask() | NSFullSizeContentViewWindowMask)

        # Store the visualEffectView as an attribute of the widget for later removal
        mask._visualEffectView = visualEffectView

        # Connect to the widget's hide event to remove the blur effect
        def removeBlur():
            if hasattr(mask, '_visualEffectView'):
                mask._visualEffectView.removeFromSuperview()
                delattr(mask, '_visualEffectView')
            
            widget.hasBlur = False

        mask.destroyed.connect(removeBlur)
        mask.hideEvent = lambda event: removeBlur()


if platform.system() == 'Windows':
    from ctypes.wintypes import  DWORD, BOOL, HRGN, HWND
    user32 = ctypes.windll.user32
    dwm = ctypes.windll.dwmapi


    class ACCENTPOLICY(ctypes.Structure):
        _fields_ = [
            ("AccentState", ctypes.c_uint),
            ("AccentFlags", ctypes.c_uint),
            ("GradientColor", ctypes.c_uint),
            ("AnimationId", ctypes.c_uint)
        ]


    class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
        _fields_ = [
            ("Attribute", ctypes.c_int),
            ("Data", ctypes.POINTER(ctypes.c_int)),
            ("SizeOfData", ctypes.c_size_t)
        ]


    class DWM_BLURBEHIND(ctypes.Structure):
        _fields_ = [
            ('dwFlags', DWORD), 
            ('fEnable', BOOL),  
            ('hRgnBlur', HRGN), 
            ('fTransitionOnMaximized', BOOL) 
        ]


    class MARGINS(ctypes.Structure):
        _fields_ = [("cxLeftWidth", ctypes.c_int),
                    ("cxRightWidth", ctypes.c_int),
                    ("cyTopHeight", ctypes.c_int),
                    ("cyBottomHeight", ctypes.c_int)
                    ]


    SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
    SetWindowCompositionAttribute.argtypes = (HWND, WINDOWCOMPOSITIONATTRIBDATA)
    SetWindowCompositionAttribute.restype = ctypes.c_int


def ExtendFrameIntoClientArea(HWND):
    margins = MARGINS(-1, -1, -1, -1)
    dwm.DwmExtendFrameIntoClientArea(HWND, ctypes.byref(margins))


def Win7Blur(HWND,Acrylic):
    if Acrylic == False:
        DWM_BB_ENABLE = 0x01
        bb = DWM_BLURBEHIND()
        bb.dwFlags = DWM_BB_ENABLE
        bb.fEnable = 1
        bb.hRgnBlur = 1
        dwm.DwmEnableBlurBehindWindow(HWND, ctypes.byref(bb))
    else:
        ExtendFrameIntoClientArea(HWND)


def HEXtoRGBAint(HEX:str):
    alpha = HEX[7:]
    blue = HEX[5:7]
    green = HEX[3:5]
    red = HEX[1:3]

    gradientColor = alpha + blue + green + red
    return int(gradientColor, base=16)


def blur(hwnd, hexColor=False, Acrylic=False, Dark=False):
    accent = ACCENTPOLICY()
    accent.AccentState = 3 #Default window Blur #ACCENT_ENABLE_BLURBEHIND

    gradientColor = 0
    
    if hexColor != False:
        gradientColor = HEXtoRGBAint(hexColor)
        accent.AccentFlags = 2 #Window Blur With Accent Color #ACCENT_ENABLE_TRANSPARENTGRADIENT
    
    if Acrylic:
        accent.AccentState = 4 #UWP but LAG #ACCENT_ENABLE_ACRYLICBLURBEHIND
        if hexColor == False: #UWP without color is translucent
            accent.AccentFlags = 2
            gradientColor = HEXtoRGBAint('#12121240') #placeholder color
    
    accent.GradientColor = gradientColor
    
    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = 19 #WCA_ACCENT_POLICY
    data.SizeOfData = ctypes.sizeof(accent)
    data.Data = ctypes.cast(ctypes.pointer(accent), ctypes.POINTER(ctypes.c_int))
    
    SetWindowCompositionAttribute(int(hwnd), data)
    
    if Dark: 
        data.Attribute = 26 #WCA_USEDARKMODECOLORS
        SetWindowCompositionAttribute(int(hwnd), data)


def BlurLinux(WID): #may not work in all distros (working in Deepin)
    import os

    c = "xprop -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION 0 -id " + str(WID)
    os.system(c)


def GlobalBlur(HWND,hexColor=False,Acrylic=False,Dark=False,widget=None, mask=None):
    release = platform.release()
    system = platform.system()

    if system == 'Windows':
        if release == 'Vista': 
            Win7Blur(HWND,Acrylic)
        else:
            release = int(float(release))
            if release == 10 or release == 8 or release == 11: #idk what windows 8.1 spits, if is '8.1' int(float(release)) will work...
                blur(HWND,hexColor,Acrylic,Dark)
            else:
                Win7Blur(HWND,Acrylic)
    
    if system == 'Linux':
        BlurLinux(HWND)

    if system == 'Darwin':
        MacBlur(widget, mask)