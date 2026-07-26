"""QCustomPlayerBar compactMode (2026-07-26): the opt-in stacked card layout
positions cover/seek/transport in three rows, drops favorite+shuffle, and the
default wide-bar layout stays byte-identical in behaviour."""

from qtpy.QtCore import QPoint
from qtpy.QtGui import QColor, QImage, QPainter


def _bar(**props):
    from Custom_Widgets.QCustomPlayerBar import QCustomPlayerBar
    bar = QCustomPlayerBar()
    for k, v in props.items():
        setattr(bar, k, v)
    return bar


def _paint(bar, w, h):
    bar.resize(w, h)
    img = QImage(w, h, QImage.Format_ARGB32)
    img.fill(QColor("#101418"))
    p = QPainter(img)
    bar.render(p, QPoint(0, 0))
    p.end()
    return img


def test_compact_layout_rows(qapp):
    bar = _bar(compactMode=True)
    bar.resize(280, 150)
    L = bar._layout_compact()
    # row order: cover on top, seek in the middle, transport at the bottom
    assert L["cover"].bottom() < L["track"].top()
    assert L["track"].bottom() < L["play"].top()
    # transport is horizontally centred-ish
    assert abs(L["play"].center().x() - 140) < 20
    # favorite/shuffle are parked off-canvas
    assert L["right"]["favorite"].x() < 0
    assert L["right"]["shuffle"].x() < 0


def test_compact_hit_zones_drop_favorite(qapp):
    bar = _bar(compactMode=True)
    _paint(bar, 280, 150)
    assert "favorite" not in bar._hit
    assert "shuffle" not in bar._hit
    for name in ("prev", "play", "next", "repeat", "volume"):
        assert name in bar._hit


def test_wide_default_unchanged(qapp):
    bar = _bar()
    assert bar.compactMode is False
    _paint(bar, 900, 88)
    for name in ("favorite", "shuffle", "repeat", "volume", "prev", "play", "next"):
        assert name in bar._hit


def test_compact_roundtrip_and_sizehint(qapp):
    bar = _bar()
    assert bar.sizeHint().width() == 900
    bar.compactMode = True
    assert bar.compactMode is True
    assert bar.sizeHint().height() == 150
