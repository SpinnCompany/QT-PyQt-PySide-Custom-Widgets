########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomChatThread - a data-driven message thread.
##
## The scrolling column of chat bubbles. A manager calls setMessages([...]) with
## DATA and the thread renders the right widget per row (QCustomChatBubble,
## QCustomVoiceMessage inside a bubble, QCustomChatDivider, QCustomTyping
## Indicator) and colours them from ITS OWN qproperties — so the whole look is
## set in Designer / QSS and Python never builds or paints a bubble.
##
## Each message is a dict:
##   {"kind": "date",  "text": "YESTERDAY"}
##   {"kind": "text",  "side": "in"/"out", "text", "time", "sender", "foot"}
##   {"kind": "voice", "side": "in"/"out", "duration", "time", "sender", "wave"}
##   {"kind": "typing","sender"}
########################################################################
from qtpy.QtCore import Qt, Property, QTimer, Signal
from qtpy.QtGui import QColor
from qtpy.QtWidgets import (QFrame, QWidget, QVBoxLayout, QHBoxLayout,
                            QScrollArea, QSizePolicy)

from Custom_Widgets.QCustomChatBubble import QCustomChatBubble
from Custom_Widgets.QCustomVoiceMessage import QCustomVoiceMessage
from Custom_Widgets.QCustomChatDivider import QCustomChatDivider
from Custom_Widgets.QCustomTypingIndicator import QCustomTypingIndicator
from Custom_Widgets.QCustomMessageStatus import QCustomMessageStatus
from Custom_Widgets.QCustomReactionBar import QCustomReactionBar


class QCustomChatThread(QFrame):

    # (message index, reaction-bar widget) — a manager opens an emoji picker.
    reactionAddRequested = Signal(int, object)
    # (message index, emoji) — an existing reaction chip was clicked.
    reactionClicked = Signal(int, str)

    WIDGET_ICON = "components/icons/chat_thread.png"
    WIDGET_TOOLTIP = "A data-driven chat message thread"
    WIDGET_MODULE = "Custom_Widgets.QCustomChatThread"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomChatThread' name='customChatThread'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>560</width><height>560</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomChatThread",
        "props": {"incomingBubbleColor": {"type": "color", "default": "#eef1f5"},
                  "incomingTextColor": {"type": "color", "default": "#1f2430"},
                  "outgoingBubbleColor": {"type": "color", "default": "#1b74e4"},
                  "outgoingTextColor": {"type": "color", "default": "#ffffff"},
                  "metaColor": {"type": "color", "default": "#99a0b0"},
                  "dateBgColor": {"type": "color", "default": "#eef1f5"},
                  "dateTextColor": {"type": "color", "default": "#8a93a6"},
                  "accentColor": {"type": "color", "default": "#1b74e4"},
                  "waveUnplayedColor": {"type": "color", "default": "#c7d0dc"},
                  "maxBubbleWidth": {"type": "int", "default": 460},
                  "spacing": {"type": "int", "default": 10},
                  "showReactionAdd": {"type": "bool", "default": True}},
        "signals": ["reactionAddRequested", "reactionClicked"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomChatThread")
        self._in_bubble = QColor("#eef1f5")
        self._in_text = QColor("#1f2430")
        self._out_bubble = QColor("#1b74e4")
        self._out_text = QColor("#ffffff")
        self._meta = QColor("#99a0b0")
        self._date_bg = QColor("#eef1f5")
        self._date_text = QColor("#8a93a6")
        self._accent = QColor("#1b74e4")
        self._wave_unplayed = QColor("#c7d0dc")
        self._max_w = 460
        self._spacing = 10
        self._show_reaction_add = True
        self._messages = []
        self._sender_name = ""

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        self._scroll = QScrollArea(self)
        self._scroll.setObjectName("chatThreadScroll")
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._contents = QWidget()
        self._contents.setObjectName("chatThreadContents")
        self._vbox = QVBoxLayout(self._contents)
        self._vbox.setContentsMargins(30, 20, 30, 16)
        self._vbox.setSpacing(self._spacing)
        self._vbox.addStretch(1)
        self._scroll.setWidget(self._contents)
        outer.addWidget(self._scroll)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setSenderName(self, name):
        """Default sender label for incoming rows that omit their own."""
        self._sender_name = str(name)

    def setMessages(self, messages):
        self._messages = list(messages or [])
        self._rebuild()

    def _rebuild(self):
        # clear all but the trailing stretch
        for i in range(self._vbox.count() - 2, -1, -1):
            it = self._vbox.itemAt(i)
            w = it.widget()
            if w is not None:
                self._vbox.removeWidget(w)
                w.setParent(None)
                w.deleteLater()
        idx = 0
        for mi, m in enumerate(self._messages):
            w = self._make(m, mi)
            if w is not None:
                self._vbox.insertWidget(idx, w)
                idx += 1
        QTimer.singleShot(0, self._scroll_to_bottom)

    def addReaction(self, index, emoji):
        """Add one of `emoji` to message `index` (increment if it already
        exists), then refresh. Lets a manager apply an emoji-picker choice."""
        if not (0 <= index < len(self._messages)):
            return
        m = self._messages[index]
        reactions = [(str(e), int(c)) for (e, c) in
                     (self._normalize_reactions(m.get("reactions")))]
        for j, (e, c) in enumerate(reactions):
            if e == emoji:
                reactions[j] = (e, c + 1)
                break
        else:
            reactions.append((str(emoji), 1))
        m["reactions"] = reactions
        self._rebuild()

    @staticmethod
    def _normalize_reactions(reactions):
        out = []
        for r in (reactions or []):
            if isinstance(r, (tuple, list)) and len(r) >= 2:
                out.append((r[0], r[1]))
            elif isinstance(r, dict):
                out.append((r.get("emoji", ""), r.get("count", 1)))
        return out

    def _make(self, m, mi=-1):
        kind = m.get("kind", "text")
        if kind == "date":
            d = QCustomChatDivider(text=m.get("text", ""), variant="pill")
            d.pillColor = self._date_bg
            d.textColor = self._date_text
            return d
        if kind == "typing":
            wrap = QWidget()
            h = QHBoxLayout(wrap)
            h.setContentsMargins(0, 0, 0, 0)
            ti = QCustomTypingIndicator()
            ti.dotColor = self._meta
            ti.bubbleColor = self._in_bubble
            h.addWidget(ti, 0)
            h.addStretch(1)
            return wrap
        out = (m.get("side") == "out")
        sender = m.get("sender") or ("You" if out else self._sender_name)
        if kind == "voice":
            b = QCustomChatBubble(side=("outgoing" if out else "incoming"))
            b.bubbleColor = self._out_bubble if out else self._in_bubble
            b.metaColor = self._meta
            b.setSender(sender)
            b.setTime(m.get("time", ""))
            b.maxBubbleWidth = 320
            v = QCustomVoiceMessage()
            if m.get("wave"):
                v.valuesCsv = m["wave"]
            v.duration = m.get("duration", "00:00")
            base = "#ffffff" if out else self._accent.name()
            v.playedColor = QColor(base)
            v.buttonColor = QColor(base)
            v.buttonIconColor = QColor(self._out_bubble if out else QColor("#ffffff"))
            v.unplayedColor = QColor(255, 255, 255, 110) if out else QColor(self._wave_unplayed)
            v.durationColor = QColor(self._out_text if out else self._meta)
            b.setBodyWidget(v)
            self._attach_extras(b, m, out, mi)
            return b
        # text (default)
        b = QCustomChatBubble(text=m.get("text", ""),
                              side=("outgoing" if out else "incoming"))
        b.bubbleColor = self._out_bubble if out else self._in_bubble
        b.textColor = self._out_text if out else self._in_text
        b.metaColor = self._meta
        b.setSender(sender)
        b.setTime(m.get("time", ""))
        if m.get("foot"):
            b.setFoot(m["foot"])
        b.maxBubbleWidth = self._max_w
        self._attach_extras(b, m, out, mi)
        return b

    def _attach_extras(self, bubble, m, out, mi=-1):
        # Delivery ticks next to an outgoing message's time (sent/delivered/read)
        status = m.get("status")
        if out and status:
            st = QCustomMessageStatus()
            st.tickColor = self._meta
            st.readColor = self._accent
            st.setStatus(status)
            bubble.setMetaWidget(st)
        # Reaction bar below EVERY message bubble: chips render only when the
        # message has reactions, but the "+" add affordance is always present so
        # any message can be reacted to from scratch. Suppressed only when the
        # thread opts out via `showReactionAdd`.
        reactions = m.get("reactions")
        if reactions or self._show_reaction_add:
            rb = QCustomReactionBar()
            rb.showAdd = self._show_reaction_add
            if reactions:
                rb.setReactions(reactions)
            # forward interactions up with the owning message index
            rb.addRequested.connect(lambda i=mi, w=rb: self.reactionAddRequested.emit(i, w))
            rb.reactionClicked.connect(lambda emoji, i=mi: self.reactionClicked.emit(i, emoji))
            bubble.setReactionBar(rb)

    def _scroll_to_bottom(self):
        bar = self._scroll.verticalScrollBar()
        bar.setValue(bar.maximum())

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(QColor)
    def incomingBubbleColor(self):
        return self._in_bubble

    @incomingBubbleColor.setter
    def incomingBubbleColor(self, c):
        self._in_bubble = QColor(c)
        self._rebuild()

    @Property(QColor)
    def incomingTextColor(self):
        return self._in_text

    @incomingTextColor.setter
    def incomingTextColor(self, c):
        self._in_text = QColor(c)
        self._rebuild()

    @Property(QColor)
    def outgoingBubbleColor(self):
        return self._out_bubble

    @outgoingBubbleColor.setter
    def outgoingBubbleColor(self, c):
        self._out_bubble = QColor(c)
        self._rebuild()

    @Property(QColor)
    def outgoingTextColor(self):
        return self._out_text

    @outgoingTextColor.setter
    def outgoingTextColor(self, c):
        self._out_text = QColor(c)
        self._rebuild()

    @Property(QColor)
    def metaColor(self):
        return self._meta

    @metaColor.setter
    def metaColor(self, c):
        self._meta = QColor(c)
        self._rebuild()

    @Property(QColor)
    def dateBgColor(self):
        return self._date_bg

    @dateBgColor.setter
    def dateBgColor(self, c):
        self._date_bg = QColor(c)
        self._rebuild()

    @Property(QColor)
    def dateTextColor(self):
        return self._date_text

    @dateTextColor.setter
    def dateTextColor(self, c):
        self._date_text = QColor(c)
        self._rebuild()

    @Property(QColor)
    def accentColor(self):
        return self._accent

    @accentColor.setter
    def accentColor(self, c):
        self._accent = QColor(c)
        self._rebuild()

    @Property(QColor)
    def waveUnplayedColor(self):
        return self._wave_unplayed

    @waveUnplayedColor.setter
    def waveUnplayedColor(self, c):
        self._wave_unplayed = QColor(c)
        self._rebuild()

    @Property(int)
    def maxBubbleWidth(self):
        return self._max_w

    @maxBubbleWidth.setter
    def maxBubbleWidth(self, v):
        self._max_w = max(120, int(v))
        self._rebuild()

    @Property(int)
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, v):
        self._spacing = max(0, int(v))
        self._vbox.setSpacing(self._spacing)

    @Property(bool)
    def showReactionAdd(self):
        return self._show_reaction_add

    @showReactionAdd.setter
    def showReactionAdd(self, v):
        self._show_reaction_add = bool(v)
        self._rebuild()
