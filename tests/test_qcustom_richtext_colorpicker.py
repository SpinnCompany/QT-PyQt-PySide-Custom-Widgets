"""QCustomRichTextEditor + QCustomColorPicker."""
from qtpy.QtGui import QFont, QTextCursor, QColor


class TestRichText:
    def test_content_api(self, qapp):
        from Custom_Widgets.QCustomRichTextEditor import QCustomRichTextEditor
        e = QCustomRichTextEditor()
        e.setPlainText("hello world")
        assert e.toPlainText() == "hello world"
        assert "hello world" in e.toHtml()
        seen = []
        e.textChanged.connect(lambda: seen.append(1))
        e.setPlainText("changed")
        assert seen                              # textChanged forwarded

    def test_bold_applies_to_selection(self, qapp):
        from Custom_Widgets.QCustomRichTextEditor import QCustomRichTextEditor
        e = QCustomRichTextEditor()
        e.setPlainText("bold me")
        cur = e.editor().textCursor()
        cur.select(QTextCursor.Document)
        e.editor().setTextCursor(cur)
        e._applyBold(True)
        assert e.editor().textCursor().charFormat().fontWeight() >= QFont.Bold

    def test_toggle_buttons_sync(self, qapp):
        from Custom_Widgets.QCustomRichTextEditor import QCustomRichTextEditor
        e = QCustomRichTextEditor()
        e.setPlainText("x")
        cur = e.editor().textCursor()
        cur.select(QTextCursor.Document)
        e.editor().setTextCursor(cur)
        e._applyItalic(True)
        # moving the cursor over italic text checks the italic button
        e.editor().setTextCursor(cur)
        assert e._italic.isChecked() is True

    def test_heading_sets_size(self, qapp):
        from Custom_Widgets.QCustomRichTextEditor import QCustomRichTextEditor
        e = QCustomRichTextEditor()
        e.setPlainText("title")
        cur = e.editor().textCursor()
        cur.select(QTextCursor.Document)
        e.editor().setTextCursor(cur)
        e._heading(1)
        assert e.editor().textCursor().charFormat().fontPointSize() == 22


class TestColorPicker:
    def test_default_and_set(self, qapp):
        from Custom_Widgets.QCustomColorPicker import QCustomColorPicker
        p = QCustomColorPicker(color="#3b82f6")
        assert p.colorName() == "#3b82f6"
        seen = []
        p.colorChanged.connect(seen.append)
        p.setColor("#ff0000")
        assert p.color() == QColor("#ff0000")
        assert p.colorName() == "#ff0000"
        assert seen and seen[-1] == QColor("#ff0000")

    def test_hex_field_reflects_color(self, qapp):
        from Custom_Widgets.QCustomColorPicker import QCustomColorPicker
        p = QCustomColorPicker(color="#123456")
        assert p._hex.text() == "#123456"
        p.setColor("#abcdef")
        assert p._hex.text() == "#abcdef"

    def test_invalid_hex_reverts(self, qapp):
        from Custom_Widgets.QCustomColorPicker import QCustomColorPicker
        p = QCustomColorPicker(color="#3b82f6")
        p._hex.setText("not-a-color")
        p._onHexEdited()
        assert p.colorName() == "#3b82f6"        # unchanged
        assert p._hex.text() == "#3b82f6"        # reverted

    def test_no_signal_on_same_color(self, qapp):
        from Custom_Widgets.QCustomColorPicker import QCustomColorPicker
        p = QCustomColorPicker(color="#3b82f6")
        seen = []
        p.colorChanged.connect(seen.append)
        p.setColor("#3b82f6")                    # same -> no emit
        assert seen == []

    def test_presets_and_custom_button_exist(self, qapp):
        from Custom_Widgets.QCustomColorPicker import QCustomColorPicker, _PRESETS
        p = QCustomColorPicker()
        presets = p._popup.findChildren(type(p._swatch))
        # 20 presets + the "Custom..." button
        assert len(presets) >= len(_PRESETS)
