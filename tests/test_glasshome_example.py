"""GlassHome example — offscreen probe that a compiled component's glass frame
really samples the app's wallpaper (backdropSource wiring end-to-end)."""

import os
import sys

import pytest
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QImage, QPainter, QPixmap
from qtpy.QtWidgets import QLabel, QWidget

_GLASSHOME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "examples", "PySide6", "GlassHome")


@pytest.fixture()
def glasshome_path():
    if not os.path.isdir(os.path.join(_GLASSHOME, "src")):
        pytest.skip("GlassHome example not built")
    sys.path.insert(0, _GLASSHOME)
    yield
    sys.path.remove(_GLASSHOME)


def test_statcard_glass_samples_wallpaper(qapp, glasshome_path):
    from src.ui_StatCard import Ui_StatCard

    host = QWidget()
    host.resize(400, 300)

    img = QImage(400, 300, QImage.Format_ARGB32)
    p = QPainter(img)
    p.fillRect(0, 0, 200, 300, QColor(220, 30, 30))
    p.fillRect(200, 0, 200, 300, QColor(30, 30, 220))
    p.end()
    wallpaper = QLabel(host)
    wallpaper.setObjectName("wallpaper")
    wallpaper.setPixmap(QPixmap.fromImage(img))
    wallpaper.setGeometry(0, 0, 400, 300)

    card_host = QWidget(host)
    ui = Ui_StatCard()
    ui.setupUi(card_host)
    card_host.setGeometry(100, 50, 200, 150)  # straddles the red/blue boundary

    host.show()
    qapp.processEvents()

    glass = ui.statGlass
    assert glass.backdropSource == "wallpaper"
    glass.refreshBackdrop()
    qapp.processEvents()
    assert glass._backdrop_pix is not None and not glass._backdrop_pix.isNull()

    # the sampled backdrop must contain BOTH wallpaper hues (really sampled,
    # not the placeholder gradient)
    bd = glass._backdrop_pix.toImage()
    reds = blues = 0
    for x in range(0, bd.width(), 4):
        for y in range(0, bd.height(), 4):
            c = bd.pixelColor(x, y)
            if c.red() > 120 and c.blue() < 120:
                reds += 1
            if c.blue() > 120 and c.red() < 120:
                blues += 1
    assert reds > 0 and blues > 0
