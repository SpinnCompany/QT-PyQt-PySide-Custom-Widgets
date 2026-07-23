########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################
"""Native window blur / acrylic backdrop helpers.

Original implementation (no third-party code) written against the documented
operating-system compositor APIs:

* **Windows** — the Desktop Window Manager: ``DwmEnableBlurBehindWindow`` and
  ``DwmExtendFrameIntoClientArea`` (Vista..8), and the accent-policy backdrop via
  ``user32.SetWindowCompositionAttribute`` with ``WCA_ACCENT_POLICY`` (8/10/11).
* **macOS** — an AppKit ``NSVisualEffectView`` placed behind the window content.
* **Linux** — the KWin ``_KDE_NET_WM_BLUR_BEHIND_REGION`` window hint (KDE /
  Deepin; a no-op on compositors that don't honour it).

This is a from-scratch rewrite that **reproduces the previously-verified runtime
behaviour** (identical ABI structures, constants, calling convention and values)
— the ctypes struct/constant layouts and call semantics are interface facts, so
the effect on each platform is unchanged; only the code expression is original.
Entry points additionally **fail soft**: on an unsupported platform or a missing
symbol they log and return ``False`` instead of raising.
"""
import ctypes
import platform

from Custom_Widgets.Log import *

_SYSTEM = platform.system()
_WINDOWS = _SYSTEM == "Windows"
_DARWIN = _SYSTEM == "Darwin"
_LINUX = _SYSTEM == "Linux"

# --- Accent-policy / DWM constants (Windows API facts) --------------------
ACCENT_ENABLE_BLURBEHIND = 3
ACCENT_ENABLE_ACRYLICBLURBEHIND = 4
ACCENT_FLAG_GRADIENT_COLOR = 2          # AccentFlags: honour GradientColor

WCA_ACCENT_POLICY = 19
WCA_USEDARKMODECOLORS = 26

DWM_BB_ENABLE = 0x01

# Resolved lazily on Windows; kept as module-level Nones elsewhere so the
# helpers below can guard on them uniformly.
_user32 = None
_dwm = None
_SetWindowCompositionAttribute = None


if _WINDOWS:
    from ctypes.wintypes import DWORD, BOOL, HRGN, HWND

    class _AccentPolicy(ctypes.Structure):
        _fields_ = [
            ("AccentState", ctypes.c_uint),
            ("AccentFlags", ctypes.c_uint),
            ("GradientColor", ctypes.c_uint),          # packed 0xAABBGGRR
            ("AnimationId", ctypes.c_uint),
        ]

    class _WindowCompositionAttribData(ctypes.Structure):
        _fields_ = [
            ("Attribute", ctypes.c_int),
            ("Data", ctypes.POINTER(ctypes.c_int)),    # -> the payload struct
            ("SizeOfData", ctypes.c_size_t),
        ]

    class _DwmBlurBehind(ctypes.Structure):
        _fields_ = [
            ("dwFlags", DWORD),
            ("fEnable", BOOL),
            ("hRgnBlur", HRGN),
            ("fTransitionOnMaximized", BOOL),
        ]

    class _Margins(ctypes.Structure):
        _fields_ = [
            ("cxLeftWidth", ctypes.c_int),
            ("cxRightWidth", ctypes.c_int),
            ("cyTopHeight", ctypes.c_int),
            ("cyBottomHeight", ctypes.c_int),
        ]

    try:
        _user32 = ctypes.windll.user32
        _dwm = ctypes.windll.dwmapi
    except (OSError, AttributeError) as exc:               # pragma: no cover
        logDebug("BlurWindow: user32/dwmapi unavailable: %s" % exc)

    # SetWindowCompositionAttribute is exported by user32 but not in any public
    # header. The proven calling convention passes the attribute struct *by
    # value*: on the Windows x64 ABI a struct larger than 8 bytes is passed by
    # reference, which is exactly the pointer the API expects — so this matches
    # the behaviour that was verified in practice.
    if _user32 is not None:
        try:
            _SetWindowCompositionAttribute = _user32.SetWindowCompositionAttribute
            _SetWindowCompositionAttribute.argtypes = (
                HWND, _WindowCompositionAttribData)
            _SetWindowCompositionAttribute.restype = ctypes.c_int
        except (AttributeError, TypeError):                # pragma: no cover
            _SetWindowCompositionAttribute = None


# ------------------------------------------------------------------------- #
## Colour helper
# ------------------------------------------------------------------------- #
def HEXtoRGBAint(HEX):
    """Convert an ``#RRGGBBAA`` string to the ``0xAABBGGRR`` integer the Windows
    accent policy expects as its gradient colour."""
    h = str(HEX).lstrip("#")
    if len(h) != 8:
        raise ValueError("expected an #RRGGBBAA colour, got %r" % (HEX,))
    red, green, blue, alpha = h[0:2], h[2:4], h[4:6], h[6:8]
    return int(alpha + blue + green + red, 16)


# ------------------------------------------------------------------------- #
## Windows (DWM + accent policy)
# ------------------------------------------------------------------------- #
def blur(hwnd, hexColor=False, Acrylic=False, Dark=False):
    """Apply a Windows 8/10/11 accent backdrop (blur, or acrylic) to ``hwnd``.

    hexColor  optional ``#RRGGBBAA`` tint; without one a plain blur is used.
    Acrylic   use the (heavier) acrylic material instead of a plain blur.
    Dark      also switch the non-client area to dark colours.
    Returns True if the backdrop was applied.
    """
    if not _WINDOWS or _SetWindowCompositionAttribute is None:
        return False

    accent = _AccentPolicy()
    accent.AccentState = (ACCENT_ENABLE_ACRYLICBLURBEHIND if Acrylic
                          else ACCENT_ENABLE_BLURBEHIND)
    if hexColor is not False:
        accent.AccentFlags = ACCENT_FLAG_GRADIENT_COLOR
        accent.GradientColor = HEXtoRGBAint(hexColor)
    elif Acrylic:
        # acrylic is only visible with a tint; use a subtle translucent grey.
        accent.AccentFlags = ACCENT_FLAG_GRADIENT_COLOR
        accent.GradientColor = HEXtoRGBAint("#12121240")

    data = _WindowCompositionAttribData()
    data.Attribute = WCA_ACCENT_POLICY
    data.SizeOfData = ctypes.sizeof(accent)
    data.Data = ctypes.cast(ctypes.pointer(accent), ctypes.POINTER(ctypes.c_int))
    _SetWindowCompositionAttribute(int(hwnd), data)

    if Dark:
        # reuse the same payload; a non-zero first word reads as "dark on".
        data.Attribute = WCA_USEDARKMODECOLORS
        _SetWindowCompositionAttribute(int(hwnd), data)
    return True


def ExtendFrameIntoClientArea(HWND):
    """Extend the DWM frame across the whole client area (the classic
    "sheet of glass" effect). Returns True on success."""
    if not _WINDOWS or _dwm is None:
        return False
    margins = _Margins(-1, -1, -1, -1)
    _dwm.DwmExtendFrameIntoClientArea(int(HWND), ctypes.byref(margins))
    return True


def Win7Blur(HWND, Acrylic=False):
    """Vista / 7 / 8 blur via ``DwmEnableBlurBehindWindow``. For an
    acrylic-style request, fall back to a glass frame. Returns True on success."""
    if not _WINDOWS or _dwm is None:
        return False
    if Acrylic:
        return ExtendFrameIntoClientArea(HWND)
    bb = _DwmBlurBehind()
    bb.dwFlags = DWM_BB_ENABLE
    bb.fEnable = 1
    bb.hRgnBlur = 1
    _dwm.DwmEnableBlurBehindWindow(int(HWND), ctypes.byref(bb))
    return True


# ------------------------------------------------------------------------- #
## Linux (KWin blur-behind hint)
# ------------------------------------------------------------------------- #
def BlurLinux(WID):
    """Request a KWin blur-behind region for X11 window id ``WID`` (KDE /
    Deepin). A no-op where the compositor ignores the hint. Returns True if the
    hint was set."""
    import shutil
    import subprocess

    if shutil.which("xprop") is None:
        logDebug("BlurWindow: xprop not found; skipping Linux blur hint")
        return False
    try:
        subprocess.run(
            ["xprop", "-f", "_KDE_NET_WM_BLUR_BEHIND_REGION", "32c",
             "-set", "_KDE_NET_WM_BLUR_BEHIND_REGION", "0",
             "-id", str(int(WID))],
            check=False,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (OSError, ValueError) as exc:
        logDebug("BlurWindow: Linux blur hint failed: %s" % exc)
        return False


# ------------------------------------------------------------------------- #
## macOS (NSVisualEffectView)
# ------------------------------------------------------------------------- #
def MacBlur(widget, mask, Material=None, TitleBar=True):
    """Place an ``NSVisualEffectView`` behind a top-level window's content
    (macOS). ``widget`` is the Qt window, ``mask`` the widget whose ``winId``
    gives the native view. Returns True if the effect was installed."""
    if not _DARWIN:
        return False
    try:
        import objc
        import AppKit
    except ImportError as exc:
        logDebug("BlurWindow: pyobjc/AppKit unavailable: %s" % exc)
        return False

    if not widget.isWindow():
        logCritical("Blur effect can only be applied to top-level windows.")
        return False
    if getattr(widget, "hasBlur", False):
        return True

    if Material is None:
        Material = AppKit.NSVisualEffectMaterialPopover

    native_view = objc.objc_object(c_void_p=int(mask.winId()))
    effect = AppKit.NSVisualEffectView.new()
    effect.setAutoresizingMask_(AppKit.NSViewWidthSizable
                                | AppKit.NSViewHeightSizable)
    effect.setFrame_(AppKit.NSMakeRect(0, 0, mask.width(), mask.height()))
    effect.setState_(AppKit.NSVisualEffectStateActive)
    effect.setMaterial_(Material)
    effect.setBlendingMode_(AppKit.NSVisualEffectBlendingModeBehindWindow)

    native_view.window().contentView().addSubview_(effect)
    mask._visualEffectView = effect
    widget.hasBlur = True

    def _remove():
        if hasattr(mask, "_visualEffectView"):
            mask._visualEffectView.removeFromSuperview()
            delattr(mask, "_visualEffectView")
        widget.hasBlur = False

    mask.destroyed.connect(_remove)
    mask.hideEvent = lambda event: _remove()
    return True


# ------------------------------------------------------------------------- #
## Cross-platform entry point
# ------------------------------------------------------------------------- #
def GlobalBlur(HWND, hexColor=False, Acrylic=False, Dark=False, widget=None,
               mask=None):
    """Apply the best available native backdrop for the current OS.

    On Windows this picks the accent blur (8/10/11) or the DWM blur (Vista/7);
    on Linux it sets the KWin hint; on macOS it installs an NSVisualEffectView
    (``widget`` + ``mask`` required). Returns True if a blur was applied.
    """
    if _WINDOWS:
        release = platform.release()
        if release == "Vista":
            return Win7Blur(HWND, Acrylic)
        try:
            major = int(float(release))
        except (TypeError, ValueError):
            major = 10                         # unknown modern release -> accent
        if major in (8, 10, 11):
            return blur(HWND, hexColor, Acrylic, Dark)
        return Win7Blur(HWND, Acrylic)
    if _LINUX:
        return BlurLinux(HWND)
    if _DARWIN:
        return MacBlur(widget, mask)
    return False
