"""QCustomStatCard + QCustomProgressRing + QCustomCard."""


class TestStatCard:
    def test_content_and_trend(self, qapp):
        from Custom_Widgets.QCustomStatCard import QCustomStatCard
        c = QCustomStatCard(label="Revenue", value="$12.4k",
                            delta="12.5%", trend="up", caption="vs last mo")
        assert c.label == "Revenue" and c.value == "$12.4k"
        assert c.trend == "up"
        assert "12.5%" in c._delta.text() and c._delta.text().startswith("▲")
        assert c._caption.text() == "vs last mo"

    def test_trend_change_recolors_glyph(self, qapp):
        from Custom_Widgets.QCustomStatCard import QCustomStatCard
        c = QCustomStatCard(value="10", delta="3", trend="up")
        assert c._delta.text().startswith("▲")
        c.setTrend("down")
        assert c._delta.text().startswith("▼") and "3" in c._delta.text()
        c.setTrend("flat")
        assert c._delta.text() == "3"                 # no arrow for flat

    def test_empty_delta_hidden(self, qapp):
        from Custom_Widgets.QCustomStatCard import QCustomStatCard
        c = QCustomStatCard(value="5")
        assert c._delta.isHidden()

    def test_trend_property_drives_qss_and_paints(self, qapp):
        from Custom_Widgets.QCustomStatCard import QCustomStatCard
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        c = QCustomStatCard(label="Users", value="1,204", delta="8%", trend="up")
        c.ensurePolished()
        c.resize(200, 110)
        img = c.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 6)
                  for x in range(0, img.width(), 6)}
        assert len(colors) > 2
        qapp.setStyleSheet("")


class TestProgressRing:
    def test_value_clamp_and_signal(self, qapp):
        from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
        r = QCustomProgressRing(minimum=0, maximum=100, value=0)
        seen = []
        r.valueChanged.connect(seen.append)
        r.setValue(60)
        assert r.value() == 60 and seen == [60]
        r.setValue(200)                               # clamp high
        assert r.value() == 100 and seen == [60, 100]
        r.setValue(-5)                                # clamp low
        assert r.value() == 0

    def test_fraction(self, qapp):
        from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
        r = QCustomProgressRing(minimum=0, maximum=50, value=25)
        assert abs(r._fraction() - 0.5) < 1e-9

    def test_colors_via_qproperty_and_paints(self, qapp):
        from Custom_Widgets.QCustomProgressRing import QCustomProgressRing
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        r = QCustomProgressRing(value=75)
        r.ensurePolished()
        assert r.ringColor.name().lower() == "#2563eb"      # accent
        assert r.trackColor.name().lower() == "#f1f5f9"     # surface-muted
        r.resize(96, 96)
        img = r.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 4)
                  for x in range(0, img.width(), 4)}
        assert len(colors) > 2
        qapp.setStyleSheet("")


class TestCard:
    def test_header_visibility(self, qapp):
        from Custom_Widgets.QCustomCard import QCustomCard
        c = QCustomCard()
        assert c._title.isHidden() and c._subtitle.isHidden()
        c.setTitle("Account"); c.setSubtitle("Billing details")
        assert not c._title.isHidden() and not c._subtitle.isHidden()
        assert c.title == "Account" and c.subtitle == "Billing details"

    def test_add_widget_goes_to_body(self, qapp):
        from Custom_Widgets.QCustomCard import QCustomCard
        from qtpy.QtWidgets import QLabel
        c = QCustomCard(title="Card")
        inner = QLabel("hello")
        c.addWidget(inner)
        assert inner.parent() is c.body()
        assert c.contentLayout().indexOf(inner) >= 0
