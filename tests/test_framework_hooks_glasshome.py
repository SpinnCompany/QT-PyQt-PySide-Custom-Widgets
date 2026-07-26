"""Framework hooks moved out of GlassHome's app code (2026-07-26):
QCustomWallpaper, QCustomClockLabel, QCustomQLabel image mode, set_state,
PlayerBar numeric time, gauge stepping, PageDots bindTo, MiniBarChart
selectOnClick, and the theme toggle's custom-theme pair."""

import re

from qtpy.QtCore import QPoint, Qt
from qtpy.QtGui import QColor, QImage, QPainter, QPixmap


def test_wallpaper_fallback_gradient_and_cover_fit(qapp):
    from Custom_Widgets.QCustomWallpaper import QCustomWallpaper
    w = QCustomWallpaper()
    w.fallbackTop = QColor("#ff0000")
    w.fallbackMid = QColor("#00ff00")
    w.fallbackBottom = QColor("#0000ff")
    w.resize(200, 150)
    img = w.grab().toImage()
    # the gradient runs diagonally from the top-left — probe along its axis
    assert img.pixelColor(2, 2).red() > 150            # start ~red
    assert img.pixelColor(60, 145).blue() > 150        # end ~blue

    # cover-fit: a 2:1 pixmap into a 1:1 widget must FILL (no letterbox bands)
    pm = QPixmap(200, 100)
    pm.fill(QColor("#ffaa00"))
    w._on_loaded(pm)
    w.resize(150, 150)
    img = w.grab().toImage()
    assert img.pixelColor(75, 5) == QColor("#ffaa00")
    assert img.pixelColor(75, 145) == QColor("#ffaa00")


def test_clock_label_ticks_and_formats(qapp):
    from Custom_Widgets.QCustomClockLabel import QCustomClockLabel
    clock = QCustomClockLabel()
    assert re.match(r"^\d{1,2}:\d{2} (AM|PM)$", clock.text())
    clock.format = "HH:mm"
    assert re.match(r"^\d{2}:\d{2}$", clock.text())
    assert clock.running is True
    clock.running = False
    assert clock.running is False


def test_qlabel_image_mode_rounds_and_fits(qapp):
    from Custom_Widgets.QCustomQLabel import QCustomQLabel
    lbl = QCustomQLabel()
    lbl.resize(100, 100)
    lbl.imageCornerRadius = 20
    pm = QPixmap(200, 400)
    pm.fill(QColor("#3355e8"))
    lbl._onImageLoaded(pm)
    out = lbl.pixmap()
    assert out is not None and not out.isNull()
    img = out.toImage()
    # corners clipped by the rounded path, centre filled
    assert img.pixelColor(1, 1).alpha() == 0
    assert img.pixelColor(img.width() // 2, img.height() // 2).alpha() == 255


def test_set_state_repolishes_children(qapp):
    from qtpy.QtWidgets import QLabel, QWidget
    from Custom_Widgets import set_state
    host = QWidget()
    child = QLabel(host)
    set_state(host, "active", True)
    assert host.property("active") == "true"
    set_state(host, "active", False)
    assert host.property("active") == "false"


def test_player_numeric_time(qapp):
    from Custom_Widgets.QCustomPlayerBar import QCustomPlayerBar
    bar = QCustomPlayerBar()
    bar.durationSeconds = 147
    assert bar.totalText == "2:27"
    bar.elapsedSeconds = 34
    assert bar.elapsedText == "0:34"
    assert abs(bar.position - 34 / 147.0) < 1e-6


def test_gauge_step_api_clamps(qapp):
    from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
    g = QCustomRadialGauge(value=64, minimum=40, maximum=90)
    g.animated = False
    g.stepUp()
    assert g.value == 65
    g.singleStep = 30
    g.stepUp()
    assert g.value == 90          # clamped at maximum
    g.stepDown()
    assert g.value == 60


def test_pagedots_bind_to_segmented(qapp):
    from Custom_Widgets.QCustomPageDots import QCustomPageDots
    from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
    seg = QCustomSegmentedControl()
    seg.setSegments(["A", "B", "C"])
    dots = QCustomPageDots()
    dots.bindTo(seg)
    assert dots.count == 3
    seg.setCurrentIndex(2)
    assert dots.activeIndex == 2
    dots.pageChanged.emit(1)
    assert seg.currentIndex() == 1


def test_minibar_select_on_click(qapp):
    from qtpy.QtCore import QEvent, QPointF
    from qtpy.QtGui import QMouseEvent, QRegion
    from qtpy.QtWidgets import QWidget
    from Custom_Widgets.QCustomMiniBarChart import QCustomMiniBarChart
    chart = QCustomMiniBarChart(values=[90, 120, 169, 60], labels=list("abcd"))
    chart.highlightIndexProp = 2
    chart.calloutText = "169 kWh"
    chart.hoverSuffix = " kWh"
    chart.selectOnClick = True
    chart.resize(360, 220)
    img = QImage(360, 220, QImage.Format_ARGB32)
    p = QPainter(img)
    chart.render(p, QPoint(0, 0), QRegion(), QWidget.RenderFlag.DrawChildren)
    p.end()
    x = sum(chart._col_spans[3]) / 2.0
    ev = QMouseEvent(QEvent.MouseButtonPress, QPointF(x, 100), Qt.LeftButton,
                     Qt.LeftButton, Qt.NoModifier)
    chart.mousePressEvent(ev)
    assert chart.highlightIndexProp == 3
    assert chart.calloutText == "60 kWh"


def test_theme_toggle_custom_pair_roundtrip(qapp):
    from Custom_Widgets.QCustomThemeDarkLightToggle import QCustomThemeDarkLightToggle
    t = QCustomThemeDarkLightToggle()
    t.darkTheme = "Glass Dusk"
    t.lightTheme = "Glass Day"
    assert t.darkTheme == "Glass Dusk"
    assert t.lightTheme == "Glass Day"
