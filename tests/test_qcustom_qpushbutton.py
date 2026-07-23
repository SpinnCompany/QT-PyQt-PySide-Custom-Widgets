"""QCustomQPushButton - variant/sizeVariant properties, click, Designer attrs."""

import xml.etree.ElementTree as ET


class TestVariantProps:
    def test_defaults(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        b = QCustomQPushButton()
        assert b.variant == "primary"
        assert b.sizeVariant == "md"

    def test_variant_set_get_and_repolish(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        b = QCustomQPushButton()
        for v in ("secondary", "outline", "ghost", "destructive"):
            b.variant = v
            assert b.variant == v
            # the Qt property mirrors the python attribute (QSS selectors read it)
            assert b.property("variant") == v

    def test_size_variant_set_get(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        b = QCustomQPushButton()
        for s in ("sm", "md", "lg"):
            b.sizeVariant = s
            assert b.sizeVariant == s
            assert b.property("sizeVariant") == s

    def test_size_variant_does_not_shadow_qwidget_size(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        b = QCustomQPushButton()
        b.resize(120, 34)
        # .size() is still the QWidget geometry, not the variant string
        assert b.size().width() == 120


class TestBehaviour:
    def test_clicked_signal(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        b = QCustomQPushButton()
        seen = []
        b.clicked.connect(lambda: seen.append(1))
        b.click()
        assert seen == [1]

    def test_tokenized_and_paints(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        b = QCustomQPushButton()
        b.setText("Go")
        b.variant = "primary"
        b.ensurePolished()
        b.resize(120, 34)
        img = b.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 4)
                  for x in range(0, img.width(), 4)}
        assert len(colors) > 1                    # actually painted
        qapp.setStyleSheet("")


class TestDesignerRegistration:
    def test_widget_attrs_present(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        assert QCustomQPushButton.WIDGET_MODULE == "Custom_Widgets.QCustomQPushButton"
        assert QCustomQPushButton.WIDGET_TOOLTIP
        assert QCustomQPushButton.WIDGET_ICON

    def test_dom_xml_is_wellformed(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        root = ET.fromstring(QCustomQPushButton.WIDGET_DOM_XML)
        widget = root.find("widget")
        assert widget is not None
        assert widget.get("class") == "QCustomQPushButton"
