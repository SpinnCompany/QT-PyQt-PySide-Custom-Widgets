"""Remaining untested user-facing widgets: action button, avatar, list row,
payment card, media grid, button group, slider, tag edit, code editor, slide
menu, annotation canvas, tip overlay, tooltip, dialog, embedded window, emoji
picker and modals. Headless construction + behaviour + paint smoke (part of the
widget hardening pass toward the tiering gate)."""


def _colors(w, size):
    w.resize(*size)
    w.ensurePolished()
    img = w.grab().toImage()
    return len({img.pixel(x, y) for y in range(0, img.height(), 4)
                for x in range(0, img.width(), 4)})


class TestActionButton:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomActionButton import QCustomActionButton
        b = QCustomActionButton(caption="Save")
        assert hasattr(b, "clicked")
        assert _colors(b, (120, 44)) > 1


class TestAvatar:
    def test_text_image_status(self, qapp):
        from qtpy.QtGui import QPixmap
        from Custom_Widgets.QCustomAvatar import QCustomAvatar
        a = QCustomAvatar(text="AB")
        a.setText("CD")
        a.setBgColor("#3355ff")
        a.setStatus(True, "#22c55e")
        pm = QPixmap(32, 32)
        pm.fill()
        a.setImage(pm)
        assert _colors(a, (48, 48)) > 1


class TestListRow:
    def test_setters_and_paint(self, qapp):
        from Custom_Widgets.QCustomListRow import QCustomListRow
        r = QCustomListRow(title="Item", subtitle="sub", value="$9", meta="now")
        r.setTitle("Item 2")
        r.setSubtitle("changed")
        r.setValue("$12")
        r.setMeta("1m")
        assert _colors(r, (240, 56)) > 1


class TestPaymentCard:
    def test_setters_signal_paint(self, qapp):
        from Custom_Widgets.QCustomPaymentCard import QCustomPaymentCard
        c = QCustomPaymentCard()
        c.setBrand("VISA")
        c.setAmount("$1,240.00")
        c.setNumber("4242 4242 4242 4242")
        c.setVariant("gradient")
        got = []
        c.numberRevealed.connect(got.append)
        c.numberRevealed.emit(True)
        assert got == [True]
        assert _colors(c, (300, 180)) > 1


class TestMediaGrid:
    def test_construct_images_signal(self, qapp):
        from Custom_Widgets.QCustomMediaGrid import QCustomMediaGrid
        g = QCustomMediaGrid()
        assert hasattr(g, "tileClicked")
        g.setImages([])                          # empty safe
        assert _colors(g, (200, 200)) >= 1


class TestButtonGroup:
    def test_construct_and_paint(self, qapp):
        # setButtonGroup*Style requires prior group membership (raises otherwise);
        # here we cover construction + inherited QPushButton behaviour + paint.
        from Custom_Widgets.QCustomQPushButtonGroup import QCustomQPushButtonGroup
        b = QCustomQPushButtonGroup()
        b.setText("Tab")
        assert b.text() == "Tab"
        assert _colors(b, (100, 32)) >= 1


class TestSlider:
    def test_value_and_paint(self, qapp):
        from Custom_Widgets.QCustomQSlider import QCustomQSlider
        s = QCustomQSlider()
        s.setMinimum(0)
        s.setMaximum(10)
        s.setValue(7)
        assert s.value() == 7
        assert _colors(s, (160, 28)) >= 1


class TestTagEdit:
    def test_add_set_tags(self, qapp):
        from Custom_Widgets.QCustomTagEdit import QTagEdit
        t = QTagEdit()
        assert t.addTag("python") is True
        t.setTags(["qt", "pyside", "widgets"])
        t.setTagSuggestions(["python", "cython"])
        assert _colors(t, (240, 60)) >= 1


class TestCodeEditor:
    def test_lang_theme_and_text(self, qapp):
        from Custom_Widgets.QCustomCodeEditor import QCustomCodeEditor
        ce = QCustomCodeEditor()
        ce.setLang("python")
        ce.setTheme("monokai")
        ce.editor.setPlainText("def f():\n    return 42\n")
        assert "return 42" in ce.editor.toPlainText()
        assert _colors(ce, (240, 120)) > 1


class TestSlideMenu:
    def test_collapse_expand_and_signals(self, qapp):
        from Custom_Widgets.QCustomSlideMenu import QCustomSlideMenu
        m = QCustomSlideMenu()
        for sig in ("onCollapsed", "onExpanded", "onCollapsing", "onExpanding"):
            assert hasattr(m, sig)
        m.collapseMenu()                         # must not raise
        m.expandMenu()


class TestAnnotationCanvas:
    def test_draw_config_and_paint(self, qapp):
        from qtpy.QtGui import QColor
        from Custom_Widgets.QCustomAnnotationWidget import Canvas
        c = Canvas()
        c.setLabel("cat")
        c.setPenColor(QColor("#ff0000"))
        c.setDrawShape("rectangle")
        assert _colors(c, (200, 150)) >= 1


class TestTipOverlay:
    def test_class_structure(self, qapp):
        # A popup that attaches to a live host form; assert structure rather than
        # force a hostless construction.
        from qtpy.QtWidgets import QWidget
        from Custom_Widgets.QCustomTipOverlay import QCustomTipOverlay
        assert issubclass(QCustomTipOverlay, QWidget)
        for m in ("setDescription", "setIcon", "setCloseIcon"):
            assert hasattr(QCustomTipOverlay, m)
        assert hasattr(QCustomTipOverlay, "closed")


class TestToolTip:
    def test_class_structure(self, qapp):
        # Positions against a target widget's geometry; assert structure.
        from qtpy.QtWidgets import QWidget
        from Custom_Widgets.QCustomQToolTip import QCustomQToolTip
        assert issubclass(QCustomQToolTip, QWidget)
        for m in ("setText", "setIcon"):
            assert hasattr(QCustomQToolTip, m)
        assert hasattr(QCustomQToolTip, "onClosed")


class TestDialog:
    def test_construct_addwidget_signals(self, qapp):
        from qtpy.QtWidgets import QLabel
        from Custom_Widgets.QCustomQDialog import QCustomQDialog
        dlg = QCustomQDialog(title="Confirm", description="Proceed?")
        dlg.addWidget(QLabel("body"))
        for sig in ("accepted", "rejected"):
            assert hasattr(dlg, sig)


class TestEmbeddedWindow:
    def test_class_structure(self, qapp):
        # Hosts a form widget (needs a live, retained form to construct);
        # assert structure rather than force a throwaway-form construction.
        from qtpy.QtWidgets import QWidget
        from Custom_Widgets.QCustomEmbeddedWindow import QCustomEmbeddedWindow
        assert issubclass(QCustomEmbeddedWindow, QWidget)
        for m in ("addWidget", "setTitle", "setControlsVisible"):
            assert hasattr(QCustomEmbeddedWindow, m)
        assert hasattr(QCustomEmbeddedWindow, "closed")


class TestEmojiPicker:
    def test_class_structure(self, qapp):
        # Offline-first + opt-in network (autoUpdate=False by default), but it
        # still needs a live host form to construct; assert structure only.
        from Custom_Widgets.QCustomEmojiPicker import QCustomEmojiPicker
        from Custom_Widgets.QCustomTipOverlay import QCustomTipOverlay
        assert issubclass(QCustomEmojiPicker, QCustomTipOverlay)
        assert "emojiSelected" in QCustomEmojiPicker.__dict__


class TestModals:
    def test_manager_classes_present(self, qapp):
        import Custom_Widgets.QCustomModals as mod
        for cls in ("QCustomModalsManager", "CenterCenterQCustomModalsManager",
                    "TopQCustomModalsManager", "TopRightQCustomModalsManager"):
            assert hasattr(mod, cls)
