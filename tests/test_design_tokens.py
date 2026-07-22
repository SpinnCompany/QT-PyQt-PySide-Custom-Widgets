"""Tests for the design-token system and variant/size widget styling.

Covers primitive/{ref} resolution, per-theme semantic roles, generated QSS,
idempotent application, the button's variant/sizeVariant properties, and the
regression guard that `sizeVariant` (not `size`) is used so QWidget.size()
still works.
"""
from qtpy.QtWidgets import QApplication


class TestTokenResolution:
    def test_ref_chain_resolves_to_primitive(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens
        t = DesignTokens(theme="light")
        assert t.role("primary") == "#2563eb"        # {color.blue.600}
        assert t.role("on-primary") == "#ffffff"

    def test_theme_changes_roles(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens
        light = DesignTokens(theme="light")
        dark = DesignTokens(theme="dark")
        assert light.role("surface") != dark.role("surface")
        assert dark.role("surface") == "#0f172a"     # {color.slate.900}

    def test_primitive_path_and_px(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens
        t = DesignTokens()
        assert t.role("space.2") == 8
        assert t.px("radius.md") == "8px"

    def test_overrides_deep_merge(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens
        t = DesignTokens(theme="light",
                         semantic={"light": {"primary": "{color.red.600}"}})
        assert t.role("primary") == "#dc2626"
        assert t.role("on-primary") == "#ffffff"      # untouched role intact


class TestQssGeneration:
    def test_qss_has_variant_and_size_selectors(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens, button_qss
        qss = button_qss(DesignTokens(theme="light"))
        assert 'QCustomQPushButton[variant="primary"]' in qss
        assert 'QCustomQPushButton[variant="destructive"]' in qss
        assert 'QCustomQPushButton[sizeVariant="sm"]' in qss
        assert "#2563eb" in qss                        # resolved primary colour
        assert ":focus" in qss                         # a11y focus ring

    def test_apply_is_idempotent(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        w = QApplication.instance()
        applyDesignTokens(w, theme="light")
        once = w.styleSheet()
        applyDesignTokens(w, theme="light")
        twice = w.styleSheet()
        assert once == twice                           # no accumulation
        assert once.count("custom-widgets design tokens >>>") == 1
        w.setStyleSheet("")                            # clean up shared app state


class TestDataTableTokens:
    def test_datatable_qss_selectors(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens, datatable_qss
        qss = datatable_qss(DesignTokens(theme="light"))
        assert "QCustomDataTable QTableView" in qss
        assert "QCustomDataTable QHeaderView::section" in qss
        assert "selection-background-color: #2563eb" in qss   # accent
        assert '#dataTablePrev' in qss

    def test_header_paints_surface_muted(self, qapp):
        from qtpy.QtGui import QColor
        from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        t = QCustomDataTable()
        t.setColumns([DataTableColumn("a"), DataTableColumn("b")])
        t.setData([{"a": "x", "b": 1}])
        t.pageSize = 0
        t.resize(300, 200)
        t.show()
        t.ensurePolished()
        hdr = t.view().horizontalHeader()
        c = QColor(hdr.grab().toImage().pixel(hdr.width() // 2, hdr.height() // 2))
        assert c.name().lower() == "#f1f5f9"          # light surface-muted
        applyDesignTokens(qapp, theme="dark")
        t.ensurePolished()
        c2 = QColor(hdr.grab().toImage().pixel(hdr.width() // 2, hdr.height() // 2))
        assert c2.name().lower() == "#1e293b"         # dark surface-muted
        qapp.setStyleSheet("")


class TestButtonVariant:
    def test_defaults_set_dynamic_properties(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        b = QCustomQPushButton()
        assert b.variant == "primary"
        assert b.sizeVariant == "md"
        assert b.property("variant") == "primary"
        assert b.property("sizeVariant") == "md"

    def test_setting_updates_dynamic_property(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        b = QCustomQPushButton()
        b.variant = "ghost"
        b.sizeVariant = "lg"
        assert b.property("variant") == "ghost"        # QSS selector will match
        assert b.property("sizeVariant") == "lg"

    def test_variant_actually_paints(self, qapp):
        # End-to-end: a declared Qt property must be matched by the QSS
        # attribute selector and actually paint the token colour.
        from qtpy.QtGui import QColor
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        b = QCustomQPushButton("")          # empty text -> solid fill to sample
        b.variant = "primary"
        b.resize(120, 40)
        b.ensurePolished()
        center = QColor(b.grab().toImage().pixel(60, 20)).name().lower()
        assert center == "#2563eb"          # primary token painted
        b.variant = "destructive"           # setter repolishes -> repaint
        b.ensurePolished()
        center = QColor(b.grab().toImage().pixel(60, 20)).name().lower()
        assert center == "#dc2626"
        qapp.setStyleSheet("")

    def test_size_method_not_shadowed(self, qapp):
        # Regression: naming the property `size` would shadow QWidget.size().
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        from Custom_Widgets.QCustomDataTable import QCustomDataTable
        b = QCustomQPushButton()
        assert b.size().isValid() or b.size() is not None  # callable, returns QSize
        t = QCustomDataTable()
        assert t.size() is not None                    # was broken with `size` prop
        assert t.sizeVariant == "md"
