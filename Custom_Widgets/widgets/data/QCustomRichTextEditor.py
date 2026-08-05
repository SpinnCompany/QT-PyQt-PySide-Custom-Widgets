########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomRichTextEditor - a WYSIWYG rich-text editor.
##
## A formatting toolbar (bold / italic / underline / headings / lists /
## alignment / text colour / clear) over a QTextEdit. Tokenized. Exposes
## toHtml / setHtml / toPlainText / setPlainText and a `textChanged` signal.
########################################################################
from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import (QFont, QTextCharFormat, QTextListFormat, QTextCursor,
                        QColor)
from qtpy.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                            QToolButton, QColorDialog)


class QCustomRichTextEditor(QWidget):
    textChanged = Signal()

    WIDGET_ICON = "components/icons/richtext.png"
    WIDGET_TOOLTIP = "A WYSIWYG rich-text editor"
    WIDGET_MODULE = "Custom_Widgets.QCustomRichTextEditor"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRichTextEditor' name='customRichTextEditor'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>420</width><height>300</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRichTextEditor",
        "props": {},
        "signals": ["textChanged"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "accent", "on-primary"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomRichTextEditor")
        col = QVBoxLayout(self)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(0)

        self._toolbar = QWidget(self)
        self._toolbar.setObjectName("rteToolbar")
        bar = QHBoxLayout(self._toolbar)
        bar.setContentsMargins(6, 6, 6, 6)
        bar.setSpacing(2)

        self._edit = QTextEdit(self)
        self._edit.setObjectName("rteEditor")
        self._edit.textChanged.connect(self.textChanged)
        self._edit.currentCharFormatChanged.connect(self._syncButtons)

        self._btns = {}
        self._bold = self._toggle(bar, "B", self._applyBold, bold=True)
        self._italic = self._toggle(bar, "I", self._applyItalic, italic=True)
        self._underline = self._toggle(bar, "U", self._applyUnderline, underline=True)
        self._sep(bar)
        self._push(bar, "H1", lambda: self._heading(1))
        self._push(bar, "H2", lambda: self._heading(2))
        self._push(bar, "¶", lambda: self._heading(0))
        self._sep(bar)
        self._push(bar, "•", lambda: self._list(QTextListFormat.ListDisc))
        self._push(bar, "1.", lambda: self._list(QTextListFormat.ListDecimal))
        self._sep(bar)
        self._push(bar, "⯇", lambda: self._edit.setAlignment(Qt.AlignLeft))
        self._push(bar, "≡", lambda: self._edit.setAlignment(Qt.AlignCenter))
        self._push(bar, "⯈", lambda: self._edit.setAlignment(Qt.AlignRight))
        self._sep(bar)
        self._push(bar, "A", self._textColor)
        self._push(bar, "⌫", self._clearFormat)
        bar.addStretch(1)

        col.addWidget(self._toolbar)
        col.addWidget(self._edit, 1)

    # ------------------------------------------------------------------ #
    ## Toolbar builders
    # ------------------------------------------------------------------ #
    def _toggle(self, bar, text, slot, **font):
        b = QToolButton(self._toolbar)
        b.setObjectName("rteButton")
        b.setText(text)
        b.setCheckable(True)
        b.setCursor(Qt.PointingHandCursor)
        f = b.font()
        f.setBold(font.get("bold", False))
        f.setItalic(font.get("italic", False))
        f.setUnderline(font.get("underline", False))
        b.setFont(f)
        b.clicked.connect(lambda checked: slot(checked))
        bar.addWidget(b)
        return b

    def _push(self, bar, text, slot):
        b = QToolButton(self._toolbar)
        b.setObjectName("rteButton")
        b.setText(text)
        b.setCursor(Qt.PointingHandCursor)
        b.clicked.connect(lambda: slot())
        bar.addWidget(b)
        return b

    def _sep(self, bar):
        s = QWidget(self._toolbar)
        s.setObjectName("rteSep")
        s.setFixedWidth(1)
        bar.addWidget(s)

    # ------------------------------------------------------------------ #
    ## Formatting
    # ------------------------------------------------------------------ #
    def _merge(self, fmt):
        self._edit.mergeCurrentCharFormat(fmt)

    def _applyBold(self, on):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if on else QFont.Normal)
        self._merge(fmt)

    def _applyItalic(self, on):
        fmt = QTextCharFormat()
        fmt.setFontItalic(on)
        self._merge(fmt)

    def _applyUnderline(self, on):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(on)
        self._merge(fmt)

    def _heading(self, level):
        sizes = {0: 12, 1: 22, 2: 17}
        cursor = self._edit.textCursor()
        cursor.select(QTextCursor.BlockUnderCursor)
        fmt = QTextCharFormat()
        fmt.setFontPointSize(sizes.get(level, 12))
        fmt.setFontWeight(QFont.Bold if level > 0 else QFont.Normal)
        cursor.mergeCharFormat(fmt)
        self._edit.mergeCurrentCharFormat(fmt)

    def _list(self, style):
        cursor = self._edit.textCursor()
        cursor.createList(QTextListFormat(style) if not isinstance(style, QTextListFormat)
                          else style)

    def _textColor(self):
        col = QColorDialog.getColor(self._edit.textColor(), self, "Text colour")
        if col.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(col)
            self._merge(fmt)

    def _clearFormat(self):
        cursor = self._edit.textCursor()
        cursor.setCharFormat(QTextCharFormat())
        self._edit.setCurrentCharFormat(QTextCharFormat())

    def _syncButtons(self, fmt):
        self._bold.setChecked(fmt.fontWeight() >= QFont.Bold)
        self._italic.setChecked(fmt.fontItalic())
        self._underline.setChecked(fmt.fontUnderline())

    # ------------------------------------------------------------------ #
    ## Content API
    # ------------------------------------------------------------------ #
    def editor(self):
        return self._edit

    def toHtml(self):
        return self._edit.toHtml()

    def setHtml(self, html):
        self._edit.setHtml(html)

    def toPlainText(self):
        return self._edit.toPlainText()

    def setPlainText(self, text):
        self._edit.setPlainText(text)
