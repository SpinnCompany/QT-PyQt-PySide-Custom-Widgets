"""QCustomCodeEditor JavaScript syntax support (added for the NodeStudio
'Thoughts' panel) + the parent=None ctor fix for .ui promotion."""


class TestCodeEditorJs:
    def test_parent_ctor(self, qapp):
        from Custom_Widgets.QCustomCodeEditor import QCustomCodeEditor
        from qtpy.QtWidgets import QWidget
        host = QWidget()
        ed = QCustomCodeEditor(host)     # uic calls Widget(parent)
        assert ed.parent() is host

    def test_javascript_lang(self, qapp):
        from Custom_Widgets.QCustomCodeEditor import QCustomCodeEditor
        ed = QCustomCodeEditor()
        ed.setTheme("one-dark")
        ed.setLang("javascript")
        assert ed.lang_lbl.text() == "JavaScript"
        assert ed.highlighter.lang == "javascript"
        assert len(ed.highlighter.rules) > 0
        # 'import'/'export' are JS keywords in the new syntax file
        assert "import" in ed.highlighter.keywords
        assert "export" in ed.highlighter.keywords

    def test_js_aliases(self, qapp):
        from Custom_Widgets.QCustomCodeEditor import QCustomSyntaxHighlighter
        al = QCustomSyntaxHighlighter.AVAILABLE_LANGS
        for a in ("js", "jsx", "ts", "tsx", "typescript"):
            assert al[a] == "javascript"

    def test_renders_highlighted(self, qapp):
        from Custom_Widgets.QCustomCodeEditor import QCustomCodeEditor
        ed = QCustomCodeEditor()
        ed.setTheme("one-dark")
        ed.setLang("javascript")
        ed.editor.setPlainText('import { X } from "y";\nexport default function A() {}')
        ed.resize(360, 160)
        img = ed.grab().toImage()
        assert img.width() > 0
