########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomChatBubble - a single chat message bubble.
##
## The core building block of a messenger thread: a rounded, tail-cornered
## bubble that wraps its text with a REAL font (a QLabel, not painted glyphs),
## sized to its content up to a max width, and self-aligned to the left
## (incoming) or right (outgoing) inside a full-width thread row. An optional
## meta line above (sender + time) and an optional foot line below (delivery /
## credits-cost) round out the anatomy seen in real chat UIs. Every colour is a
## qproperty so incoming/outgoing bubbles flip with the theme; the `side`
## drives the default palette, the tail corner and the alignment. Set the body
## through `text`, or embed any widget (a voice message, an image) with
## setBodyWidget() to reuse the same bubble chrome.
########################################################################
from qtpy.QtCore import Qt, Property, QRectF
from qtpy.QtGui import QColor, QPainter, QBrush, QPainterPath, QFontMetrics
from qtpy.QtWidgets import (QFrame, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
                            QSizePolicy)


class _BubbleBody(QFrame):
    """The rounded, tail-cornered surface. Hosts either a wrapping text label
    or an arbitrary embedded widget, and paints its own background so the
    corner radii (and the single squared 'tail' corner) stay crisp."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("chatBubbleBody")
        self._bg = QColor("#eef0f4")
        self._radius = 20
        self._tail = "bottom-left"          # which corner is squared
        self._tail_radius = 6
        self._pad_h = 16
        self._pad_v = 11
        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(self._pad_h, self._pad_v, self._pad_h, self._pad_v)
        self._lay.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def setBg(self, c):
        self._bg = QColor(c)
        self.update()

    def setRadius(self, r):
        self._radius = max(0, int(r))
        self.update()

    def setTail(self, corner):
        self._tail = str(corner)
        self.update()

    def setPadding(self, h, v):
        self._pad_h, self._pad_v = int(h), int(v)
        self._lay.setContentsMargins(self._pad_h, self._pad_v, self._pad_h, self._pad_v)

    def _bubble_path(self):
        r = float(self._radius)
        tr = float(self._tail_radius)
        w, h = float(self.width()), float(self.height())
        r = min(r, w / 2.0, h / 2.0)
        # per-corner radius: tl, tr, br, bl
        rad = {"top-left": r, "top-right": r, "bottom-right": r, "bottom-left": r}
        if self._tail in rad:
            rad[self._tail] = tr
        tl, tR, br, bl = rad["top-left"], rad["top-right"], rad["bottom-right"], rad["bottom-left"]
        path = QPainterPath()
        path.moveTo(tl, 0)
        path.lineTo(w - tR, 0)
        path.arcTo(w - 2 * tR, 0, 2 * tR, 2 * tR, 90, -90)
        path.lineTo(w, h - br)
        path.arcTo(w - 2 * br, h - 2 * br, 2 * br, 2 * br, 0, -90)
        path.lineTo(bl, h)
        path.arcTo(0, h - 2 * bl, 2 * bl, 2 * bl, 270, -90)
        path.lineTo(0, tl)
        path.arcTo(0, 0, 2 * tl, 2 * tl, 180, -90)
        path.closeSubpath()
        return path

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._bg))
        p.drawPath(self._bubble_path())
        p.end()
        super().paintEvent(e)


class QCustomChatBubble(QFrame):

    WIDGET_ICON = "components/icons/chat_bubble.png"
    WIDGET_TOOLTIP = "A chat message bubble (incoming / outgoing)"
    WIDGET_MODULE = "Custom_Widgets.QCustomChatBubble"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomChatBubble' name='customChatBubble'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>420</width><height>72</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomChatBubble",
        "props": {
            "text": {"type": "string", "default": "Hey Ricky! I'm feeling amazing, how about you?"},
            "side": {"type": "enum", "values": ["incoming", "outgoing"], "default": "incoming"},
            "sender": {"type": "string", "default": ""},
            "time": {"type": "string", "default": ""},
            "foot": {"type": "string", "default": ""},
            "bubbleColor": {"type": "color", "default": "#eef0f4"},
            "textColor": {"type": "color", "default": "#1f2430"},
            "metaColor": {"type": "color", "default": "#8a93a6"},
            "radius": {"type": "int", "default": 20},
            "maxBubbleWidth": {"type": "int", "default": 420},
        },
        "signals": [],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, text="", side="incoming"):
        super().__init__(parent)
        self.setObjectName("QCustomChatBubble")
        self._side = "outgoing" if side == "outgoing" else "incoming"
        self._meta_color = QColor("#8a93a6")
        self._max_w = 420
        self._custom_body = False
        self._meta_extra = None      # e.g. QCustomMessageStatus ticks
        self._reaction_bar = None    # e.g. QCustomReactionBar

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(4)

        # meta line (sender + time [+ status ticks])
        self._meta = QLabel("")
        self._meta.setObjectName("chatBubbleMeta")
        self._meta.setVisible(False)
        self._metaRow = QHBoxLayout()
        self._metaRow.setContentsMargins(2, 0, 2, 0)
        self._metaRow.setSpacing(5)

        # body
        self._body = _BubbleBody(self)
        self._label = QLabel(text)
        self._label.setObjectName("chatBubbleText")
        self._label.setWordWrap(True)
        self._label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._body._lay.addWidget(self._label)
        self._bodyRow = QHBoxLayout()
        self._bodyRow.setContentsMargins(0, 0, 0, 0)
        self._bodyRow.setSpacing(0)

        # reactions row (below the bubble body)
        self._reactionRow = QHBoxLayout()
        self._reactionRow.setContentsMargins(2, 0, 2, 0)
        self._reactionRow.setSpacing(0)

        # foot line (delivery / cost)
        self._foot = QLabel("")
        self._foot.setObjectName("chatBubbleFoot")
        self._foot.setVisible(False)
        self._footRow = QHBoxLayout()
        self._footRow.setContentsMargins(2, 0, 2, 0)
        self._footRow.setSpacing(0)

        root.addLayout(self._metaRow)
        root.addLayout(self._bodyRow)
        root.addLayout(self._reactionRow)
        root.addLayout(self._footRow)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._apply_side_defaults()
        self._relayout()
        self._restyle()

    # ------------------------------------------------------------------ #
    ## Content API
    # ------------------------------------------------------------------ #
    def setText(self, text):
        self._label.setText(str(text))
        self._label.setVisible(bool(str(text)))
        self._size_body()
        self.updateGeometry()

    def _size_body(self):
        """Size the bubble to its text's natural width (capped at maxBubbleWidth)
        so a short message stays on one line and a long one wraps at a sensible
        width instead of collapsing to the widest-word minimum."""
        if self._custom_body or not self._label.text():
            return
        fm = QFontMetrics(self._label.font())
        pad = 2 * self._body._pad_h
        tw = fm.horizontalAdvance(self._label.text()) + pad + 2
        target = min(self._max_w, max(0, tw))
        self._body.setMinimumWidth(target)
        self._body.setMaximumWidth(self._max_w)

    def setBodyWidget(self, widget):
        """Replace the text label with an arbitrary widget (voice message,
        image, ...) while keeping the bubble chrome."""
        self._custom_body = True
        self._label.setVisible(False)
        self._body._lay.addWidget(widget)

    def setMetaWidget(self, widget):
        """Add a small widget after the meta line (e.g. QCustomMessageStatus
        delivery ticks next to an outgoing message's time)."""
        self._meta_extra = widget
        self._relayout()

    def setReactionBar(self, widget):
        """Attach a reactions row (e.g. QCustomReactionBar) below the bubble,
        aligned to the message side."""
        self._reaction_bar = widget
        self._relayout()

    def setSender(self, text):
        self._sender = str(text)
        self._refresh_meta()

    def setTime(self, text):
        self._time = str(text)
        self._refresh_meta()

    def setFoot(self, text):
        self._foot.setText(str(text))
        self._foot.setVisible(bool(str(text)))

    _sender = ""
    _time = ""

    def _refresh_meta(self):
        parts = []
        if self._side == "outgoing":
            if self._time:
                parts.append(self._time)
            if self._sender:
                parts.append(self._sender)
        else:
            if self._sender:
                parts.append(self._sender)
            if self._time:
                parts.append(self._time)
        txt = "  ".join(parts)
        self._meta.setText(txt)
        self._meta.setVisible(bool(txt))

    # ------------------------------------------------------------------ #
    ## Layout / alignment by side
    # ------------------------------------------------------------------ #
    def _clear_row(self, row):
        while row.count():
            item = row.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(self)

    def _relayout(self):
        out = (self._side == "outgoing")
        # meta row: [time] + optional status ticks, aligned to the side
        self._clear_row(self._metaRow)
        if out:
            self._metaRow.addStretch(1)
            self._metaRow.addWidget(self._meta, 0)
            if self._meta_extra is not None:
                self._metaRow.addWidget(self._meta_extra, 0)
        else:
            self._metaRow.addWidget(self._meta, 0)
            if self._meta_extra is not None:
                self._metaRow.addWidget(self._meta_extra, 0)
            self._metaRow.addStretch(1)
        # body + reactions + foot rows
        for row, w in ((self._bodyRow, self._body),
                       (self._reactionRow, self._reaction_bar),
                       (self._footRow, self._foot)):
            self._clear_row(row)
            if w is None:
                continue
            if out:
                row.addStretch(1)
                row.addWidget(w, 0)
            else:
                row.addWidget(w, 0)
                row.addStretch(1)

    def _apply_side_defaults(self):
        # `side` is a Qt property the app QSS targets (QCustomChatBubble[side=…]);
        # colours (bubble + text) come from the app QSS (bubble bg via
        # qproperty-bubbleColor, text via #chatBubbleText color). We only set the
        # painted tail + meta alignment here (geometry, not style).
        if self._side == "outgoing":
            self._body.setTail("bottom-right")
            self._meta.setAlignment(Qt.AlignRight)
            self._foot.setAlignment(Qt.AlignRight)
        else:
            self._body.setTail("bottom-left")
            self._meta.setAlignment(Qt.AlignLeft)
            self._foot.setAlignment(Qt.AlignLeft)
        for w in (self, self._label, self._meta, self._foot, self._body):
            w.style().unpolish(w)
            w.style().polish(w)

    def _restyle(self):
        self._body.setMaximumWidth(self._max_w)
        fm = QFontMetrics(self._meta.font())
        self._meta.setMinimumHeight(fm.height())

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def text(self):
        return self._label.text()

    @text.setter
    def text(self, v):
        self.setText(v)

    @Property(str)
    def side(self):
        return self._side

    @side.setter
    def side(self, v):
        self._side = "outgoing" if str(v) == "outgoing" else "incoming"
        self._apply_side_defaults()
        self._relayout()
        self._refresh_meta()

    @Property(str)
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, v):
        self.setSender(v)

    @Property(str)
    def time(self):
        return self._time

    @time.setter
    def time(self, v):
        self.setTime(v)

    @Property(str)
    def foot(self):
        return self._foot.text()

    @foot.setter
    def foot(self, v):
        self.setFoot(v)

    @Property(QColor)
    def bubbleColor(self):
        return self._body._bg

    @bubbleColor.setter
    def bubbleColor(self, c):
        self._body.setBg(QColor(c))

    @Property(QColor)
    def textColor(self):
        return QColor("#1f2430")

    @textColor.setter
    def textColor(self, c):
        # Text colour is driven by the app QSS (#chatBubbleText, per `side`);
        # keep the setter as a no-op repolish so nothing sets a per-widget sheet.
        self._label.style().unpolish(self._label)
        self._label.style().polish(self._label)

    @Property(QColor)
    def metaColor(self):
        return self._meta_color

    @metaColor.setter
    def metaColor(self, c):
        self._meta_color = QColor(c)
        self._restyle()

    @Property(int)
    def radius(self):
        return self._body._radius

    @radius.setter
    def radius(self, v):
        self._body.setRadius(v)

    @Property(int)
    def maxBubbleWidth(self):
        return self._max_w

    @maxBubbleWidth.setter
    def maxBubbleWidth(self, v):
        self._max_w = max(80, int(v))
        self._restyle()
        self._size_body()
