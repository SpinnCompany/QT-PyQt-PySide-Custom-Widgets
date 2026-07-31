########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomCardStack - an interactive stack of payment cards.
##
## Holds several QCustomPaymentCard children laid out as a peeking stack (the
## front card full-size at the bottom, the ones behind shifted up + inset so
## their top edges show). Click / tap (or call next()/previous()) to cycle the
## stack with an animated reshuffle - the front card peels to the back. Perfect
## for a "My cards" panel. Emits currentChanged(index).
##
## Give cards in code with setCards([{...}]) / addCard(...), or in Qt Designer
## with the cardsJson property (a JSON list of card dicts).
########################################################################
import json

from qtpy.QtCore import (Qt, Property, Signal, QRect, QPropertyAnimation,
                         QParallelAnimationGroup, QEasingCurve)
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QWidget, QSizePolicy

from Custom_Widgets.QCustomPaymentCard import QCustomPaymentCard


class QCustomCardStack(QWidget):

    WIDGET_ICON = "components/icons/credit-card.png"
    WIDGET_TOOLTIP = "An interactive stack of payment cards - click to cycle"
    WIDGET_MODULE = "Custom_Widgets.QCustomCardStack"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomCardStack' name='customCardStack'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>230</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomCardStack",
        "props": {"cardsJson": {"type": "string", "default": ""},
                  "cardHeight": {"type": "int", "default": 170},
                  "cardPeek": {"type": "int", "default": 22},
                  "xInset": {"type": "int", "default": 14},
                  "maxVisible": {"type": "int", "default": 3},
                  "currentIndex": {"type": "int", "default": 0},
                  "animationDuration": {"type": "int", "default": 300}},
        "signals": ["currentChanged(int)"],
        "tokens_used": ["accent"],
    }

    currentChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomCardStack")
        self._cards = []
        self._index = 0
        self._card_h = 170
        self._card_peek = 22
        self._x_inset = 14
        self._max_visible = 3
        self._duration = 300
        self._anim = None
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumHeight(180)
        self._seed_defaults()

    def _seed_defaults(self):
        """Demo cards so the stack previews in Designer / render_widget
        (replaced the moment setCards() is called)."""
        self.setCards([
            {"brand": "VISA", "amount": "$4,540.20", "number": "2104",
             "top": "#0f5a50", "bottom": "#0a2f2a", "fullNumber": "4539 8843 0117 2104"},
            {"brand": "Mastercard", "amount": "$12,980.00", "number": "8821",
             "top": "#6d4bd0", "bottom": "#3a2472", "fullNumber": "5218 4471 9930 8821"},
            {"brand": "VISA", "amount": "$640.75", "number": "3390",
             "top": "#f0873f", "bottom": "#c9531f", "fullNumber": "4024 0071 3355 3390"},
        ])

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def addCard(self, brand="VISA", amount="$0.00", number="0000",
                top="#0f4a43", bottom="#0a2b27", variant="gradient",
                textColor="#ffffff", fullNumber="", revealable=True):
        card = QCustomPaymentCard(self, brand=brand, amount=amount, number=number)
        card.setVariant(variant)
        if variant == "flat":
            card.flatColor = QColor(top)
        else:
            card.setColors(top, bottom)
        card.textColor = QColor(textColor)
        if fullNumber:
            card.fullNumber = fullNumber
        card.revealable = bool(revealable)
        card.show()
        self._cards.append(card)
        self._relayout(animate=False)
        return card

    def setCards(self, cards):
        for c in self._cards:
            c.setParent(None)
            c.deleteLater()
        self._cards = []
        self._index = 0
        for spec in (cards or []):
            self.addCard(**spec)
        self._relayout(animate=False)

    def clear(self):
        self.setCards([])

    def setCardColors(self, top, bottom=None):
        """Re-apply one gradient to every card (e.g. on a theme flip) without
        rebuilding the stack, so the current index is preserved."""
        for c in self._cards:
            c.setColors(top, bottom)

    def setCardColorsList(self, grads):
        """Give each card its OWN gradient. `grads` is a list of (top, bottom)
        pairs, applied per card (cycled if shorter than the card count)."""
        if not grads:
            return
        for i, c in enumerate(self._cards):
            top, bottom = grads[i % len(grads)]
            c.setColors(top, bottom)

    def count(self):
        return len(self._cards)

    def currentIndexValue(self):
        return self._index

    def setCurrentIndex(self, index, animate=True):
        if not self._cards:
            return
        self._index = int(index) % len(self._cards)
        self._relayout(animate=animate)
        self.currentChanged.emit(self._index)

    def next(self):
        if self._cards:
            self.setCurrentIndex(self._index + 1)

    def previous(self):
        if self._cards:
            self.setCurrentIndex(self._index - 1)

    def currentCard(self):
        return self._cards[self._index] if self._cards else None

    # ------------------------------------------------------------------ #
    ## Layout / animation
    # ------------------------------------------------------------------ #
    def _slot_rect(self, depth):
        """Geometry for the card at stack `depth` (0 = front, at the bottom)."""
        d = min(depth, self._max_visible)
        w, h = self.width(), self.height()
        inset = d * self._x_inset
        peek = d * self._card_peek
        x = inset
        cw = max(40, w - 2 * inset)
        y = max(0, (h - self._card_h) - peek)
        return QRect(x, y, cw, self._card_h)

    def _relayout(self, animate=True):
        n = len(self._cards)
        if n == 0:
            return
        # stack order: depth 0 = the current (front) card, increasing behind it
        order = [(self._index + d) % n for d in range(n)]
        targets = {}
        for depth, ci in enumerate(order):
            targets[self._cards[ci]] = self._slot_rect(depth)

        # z-order: raise from back to front so the front card ends on top
        for depth in range(n - 1, -1, -1):
            self._cards[order[depth]].raise_()

        if self._anim is not None:
            self._anim.stop()
        if not animate or not self.isVisible():
            for card, rect in targets.items():
                card.setGeometry(rect)
            return

        group = QParallelAnimationGroup(self)
        for card, rect in targets.items():
            a = QPropertyAnimation(card, b"geometry", self)
            a.setDuration(self._duration)
            a.setStartValue(card.geometry())
            a.setEndValue(rect)
            a.setEasingCurve(QEasingCurve.OutCubic)
            group.addAnimation(a)
        self._anim = group
        group.start()

    def resizeEvent(self, e):
        self._relayout(animate=False)
        super().resizeEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and len(self._cards) > 1:
            self.next()
        super().mousePressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def cardsJson(self):
        return ""

    @cardsJson.setter
    def cardsJson(self, text):
        text = str(text or "").strip()
        if not text:
            return
        try:
            data = json.loads(text)
            if isinstance(data, list):
                self.setCards(data)
        except Exception:
            pass

    @Property(int)
    def cardHeight(self):
        return self._card_h

    @cardHeight.setter
    def cardHeight(self, v):
        self._card_h = max(60, int(v))
        self.setMinimumHeight(self._card_h + 10)
        self._relayout(animate=False)

    @Property(int)
    def cardPeek(self):
        return self._card_peek

    @cardPeek.setter
    def cardPeek(self, v):
        self._card_peek = max(0, int(v))
        self._relayout(animate=False)

    @Property(int)
    def xInset(self):
        return self._x_inset

    @xInset.setter
    def xInset(self, v):
        self._x_inset = max(0, int(v))
        self._relayout(animate=False)

    @Property(int)
    def maxVisible(self):
        return self._max_visible

    @maxVisible.setter
    def maxVisible(self, v):
        self._max_visible = max(1, int(v))
        self._relayout(animate=False)

    @Property(int)
    def currentIndex(self):
        return self._index

    @currentIndex.setter
    def currentIndex(self, v):
        self.setCurrentIndex(v, animate=False)

    @Property(int)
    def animationDuration(self):
        return self._duration

    @animationDuration.setter
    def animationDuration(self, v):
        self._duration = max(0, int(v))
