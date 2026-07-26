"""QCustomMiniBarChart reference hooks (2026-07-26): the opt-in callout bubble
and y-scale labels paint, and defaults leave the classic axis-less look
untouched."""

from qtpy.QtCore import QPoint, Qt
from qtpy.QtGui import QColor, QImage


def _grab(chart, w=360, h=220):
    from qtpy.QtGui import QPainter, QRegion
    from qtpy.QtWidgets import QWidget
    chart.resize(w, h)
    img = QImage(w, h, QImage.Format_ARGB32)
    img.fill(QColor("#202634"))
    p = QPainter(img)
    # skip DrawWindowBackground — in the app the chart sits on glass; the
    # palette fill would read as a false "white" everywhere
    chart.render(p, QPoint(0, 0), QRegion(), QWidget.RenderFlag.DrawChildren)
    p.end()
    return img


def _make(**props):
    from Custom_Widgets.QCustomMiniBarChart import QCustomMiniBarChart
    chart = QCustomMiniBarChart(values=[90, 120, 169, 60, 130, 105],
                                labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
    for k, v in props.items():
        setattr(chart, k, v)
    return chart


def _has_color(img, rgb, region, tol=30):
    x0, y0, x1, y1 = region
    for x in range(int(x0), int(x1), 2):
        for y in range(int(y0), int(y1), 2):
            c = img.pixelColor(x, y)
            if (abs(c.red() - rgb[0]) < tol and abs(c.green() - rgb[1]) < tol
                    and abs(c.blue() - rgb[2]) < tol):
                return True
    return False


def test_callout_bubble_paints_above_highlight(qapp):
    chart = _make(highlightIndexProp=2, calloutText="169 kWh",
                  calloutBg=QColor("#ffffff"), calloutTextColor=QColor("#151928"))
    img = _grab(chart)
    # a white bubble must appear in the top band over the Mar column
    # (probe an inner region — render() leaves a background artefact at x=0)
    assert _has_color(img, (255, 255, 255), (90, 2, 240, 40))


def test_callout_off_by_default(qapp):
    chart = _make(highlightIndexProp=2)
    img = _grab(chart)
    assert not _has_color(img, (255, 255, 255), (90, 2, 240, 26))


def test_y_labels_reserve_gutter_and_paint(qapp):
    chart = _make(yLabelsCsv="0,50,90,130,170",
                  yLabelColor=QColor("#ff00ff"))  # loud probe colour
    img = _grab(chart)
    # magenta scale text must appear in the left gutter
    assert _has_color(img, (255, 0, 255), (0, 0, 60, 220), tol=90)


def test_y_labels_scale_max_extends_range(qapp):
    chart = _make(yLabelsCsv="0,50,90,130,170")
    assert chart.yLabelsCsv == "0,50,90,130,170"
    # roundtrip + defaults untouched
    plain = _make()
    assert plain.yLabelsCsv == ""
    assert plain.calloutText == ""


def _mouse_move(widget, x, y):
    from qtpy.QtCore import QEvent, QPointF, Qt
    from qtpy.QtGui import QMouseEvent
    ev = QMouseEvent(QEvent.MouseMove, QPointF(x, y), Qt.NoButton,
                     Qt.NoButton, Qt.NoModifier)
    widget.mouseMoveEvent(ev)


def test_hover_highlights_and_bubbles(qapp):
    chart = _make(hoverSuffix=" kWh")
    hovered = []
    chart.barHovered.connect(hovered.append)
    _grab(chart)                       # paint once to build the column spans
    assert chart._col_spans
    x = sum(chart._col_spans[1]) / 2.0 # centre of the Feb column
    _mouse_move(chart, x, 100)
    assert chart._hover_index == 1
    assert hovered == [1]
    img = _grab(chart)
    # a bubble appears above the hovered bar even with no static callout
    assert _has_color(img, (255, 255, 255), (30, 2, 330, 120))
    chart.leaveEvent(None)
    assert chart._hover_index == -1
    assert hovered == [1, -1]


def test_click_emits_bar_index(qapp):
    from qtpy.QtCore import QEvent, QPointF, Qt
    from qtpy.QtGui import QMouseEvent
    chart = _make()
    clicked = []
    chart.barClicked.connect(clicked.append)
    _grab(chart)
    x = sum(chart._col_spans[3]) / 2.0
    ev = QMouseEvent(QEvent.MouseButtonPress, QPointF(x, 100), Qt.LeftButton,
                     Qt.LeftButton, Qt.NoModifier)
    chart.mousePressEvent(ev)
    assert clicked == [3]


def test_hover_disabled_is_inert(qapp):
    chart = _make(hoverEnabled=False)
    _grab(chart)
    _mouse_move(chart, 100, 100)
    assert chart._hover_index == -1
