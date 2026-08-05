"""Motion widgets: NumberCounter, TypewriterText, GradientText,
RainbowButton, SparklesText.

Animation is the point of all five, so most of these drive the state directly
rather than waiting on timers — a test that sleeps for an animation is slow and
flaky, and the interesting behaviour is in the state machine anyway.
"""
from qtpy.QtCore import QEvent, QPointF, Qt
from qtpy.QtGui import QMouseEvent


class TestNumberCounter:
    def _counter(self, value=0, **kwargs):
        from Custom_Widgets.QCustomNumberCounter import QCustomNumberCounter
        w = QCustomNumberCounter(value=value, **kwargs)
        w.resize(200, 60)
        return w

    def test_reset_jumps_without_animating(self, qapp):
        counter = self._counter()
        counter.reset(1250)
        assert counter.value == 1250.0
        assert counter.displayedValue() == 1250.0
        assert counter.isAnimating() is False

    def test_set_value_without_animation(self, qapp):
        counter = self._counter()
        done = []
        counter.finished.connect(lambda: done.append(True))
        counter.setValue(500, animate=False)
        assert counter.displayedValue() == 500.0 and done == [True]

    def test_zero_duration_jumps(self, qapp):
        counter = self._counter()
        counter.duration = 0
        counter.setValue(99)
        assert counter.displayedValue() == 99.0

    def test_thousands_separator(self, qapp):
        counter = self._counter()
        counter.reset(1234567)
        assert counter.formattedText() == "1,234,567"

    def test_separator_can_be_disabled(self, qapp):
        counter = self._counter()
        counter.separator = ""
        counter.reset(1234567)
        assert counter.formattedText() == "1234567"

    def test_decimals_and_affixes(self, qapp):
        counter = self._counter()
        counter.decimals = 2
        counter.prefix = "$"
        counter.suffix = " USD"
        counter.reset(1234.5)
        assert counter.formattedText() == "$1,234.50 USD"

    def test_negative_keeps_the_sign_outside_the_prefix(self, qapp):
        counter = self._counter()
        counter.prefix = "$"
        counter.reset(-42)
        assert counter.formattedText() == "-$42"

    def test_width_measured_against_the_target_not_the_frame(self, qapp):
        """Sizing to the animating value would resize on every frame."""
        counter = self._counter()
        counter.reset(0)
        counter.setValue(1000000, animate=False)
        wide = counter.sizeHint().width()
        counter._display = 1.0                    # mid-animation
        assert counter.sizeHint().width() == wide

    def test_value_changed_emits(self, qapp):
        counter = self._counter()
        seen = []
        counter.valueChanged.connect(seen.append)
        counter.reset(5)
        assert seen and seen[-1] == 5.0


class TestTypewriterText:
    def _typer(self, phrases=("Build faster", "Ship sooner")):
        from Custom_Widgets.QCustomTypewriterText import QCustomTypewriterText
        w = QCustomTypewriterText(phrases=list(phrases), autoStart=False)
        w.resize(320, 40)
        return w

    def test_phrases_and_visible_text(self, qapp):
        typer = self._typer()
        assert typer.currentPhrase() == "Build faster"
        assert typer.visibleText() == ""
        typer.skip()
        assert typer.visibleText() == "Build faster"

    def test_stepping_types_one_character(self, qapp):
        typer = self._typer()
        typer._step()
        assert typer.visibleText() == "B"
        typer._step()
        assert typer.visibleText() == "Bu"

    def test_finished_signal_on_completion(self, qapp):
        typer = self._typer(phrases=["Hi"])
        seen = []
        typer.phraseFinished.connect(seen.append)
        typer._step(); typer._step()
        assert seen == ["Hi"]

    def test_erasing_then_advancing_cycles(self, qapp):
        typer = self._typer(phrases=["ab", "cd"])
        cycled = []
        typer.cycled.connect(cycled.append)
        typer.skip()
        typer._erasing = True
        typer._shown = 1
        typer._step()                     # 0 -> advance
        assert cycled == [1] and typer.currentPhrase() == "cd"

    def test_sized_against_the_longest_phrase(self, qapp):
        """Sizing to the visible text would resize on every character."""
        typer = self._typer(phrases=["a", "a very much longer phrase"])
        wide = typer.sizeHint().width()
        typer._shown = 1
        assert typer.sizeHint().width() == wide

    def test_start_and_stop(self, qapp):
        typer = self._typer()
        assert typer.start() is True and typer.isRunning() is True
        typer.stop()
        assert typer.isRunning() is False

    def test_start_with_no_phrases(self, qapp):
        typer = self._typer(phrases=[])
        assert typer.start() is False

    def test_csv_roundtrip(self, qapp):
        typer = self._typer()
        typer.phrasesCsv = "One,Two,Three"
        assert typer.phrases() == ["One", "Two", "Three"]
        assert typer.phrasesCsv == "One,Two,Three"


class TestGradientText:
    def _text(self, text="Build something great"):
        from Custom_Widgets.QCustomGradientText import QCustomGradientText
        w = QCustomGradientText(text=text)
        w.resize(320, 52)
        return w

    def test_default_stops(self, qapp):
        assert len(self._text().stops()) == 2

    def test_single_stop_rejected(self, qapp):
        """One stop is a fill, not a gradient — same rule as the picker."""
        widget = self._text()
        assert widget.setStops([(0.0, "#ff0000")]) is False
        assert len(widget.stops()) == 2

    def test_invalid_stops_dropped(self, qapp):
        widget = self._text()
        assert widget.setStops([(0.0, "#ff0000"), (0.5, "nope"),
                                (1.0, "#0000ff")]) is True
        assert len(widget.stops()) == 2

    def test_stops_csv_roundtrip(self, qapp):
        widget = self._text()
        widget.stopsCsv = "0:#ff0000,1:#0000ff"
        assert widget.stopsCsv == "0:#ff0000,1:#0000ff"

    def test_renders_differently_per_gradient(self, qapp):
        a = self._text()
        b = self._text()
        b.stopsCsv = "0:#16a34a,1:#f59e0b"
        assert a.grab().toImage() != b.grab().toImage()

    def test_angle_changes_render(self, qapp):
        flat = self._text()
        angled = self._text()
        angled.angle = 90
        assert flat.grab().toImage() != angled.grab().toImage()

    def test_animation_toggles(self, qapp):
        widget = self._text()
        widget.animated = True
        assert widget.isAnimating() is True
        widget.animated = False
        assert widget.isAnimating() is False

    def test_empty_text_paints_nothing_without_raising(self, qapp):
        self._text(text="").grab()


class TestRainbowButton:
    def _button(self, text="Get started"):
        from Custom_Widgets.QCustomRainbowButton import QCustomRainbowButton
        w = QCustomRainbowButton(text=text)
        w.resize(w.sizeHint())
        return w

    def test_default_colors(self, qapp):
        assert len(self._button().colors()) >= 2

    def test_single_colour_rejected(self, qapp):
        button = self._button()
        assert button.setColors(["#ff0000"]) is False

    def test_colors_csv_roundtrip(self, qapp):
        button = self._button()
        button.colorsCsv = "#ff0000,#00ff00,#0000ff"
        assert button.colorsCsv == "#ff0000,#00ff00,#0000ff"

    def test_animation_stops_when_hidden(self, qapp):
        """Repainting a button nobody can see is pure battery drain."""
        button = self._button()
        button.show()
        assert button.isAnimating() is True
        button.hide()
        assert button.isAnimating() is False

    def test_animated_false_never_starts(self, qapp):
        button = self._button()
        button.animated = False
        button.show()
        assert button.isAnimating() is False
        button.hide()

    def test_rotation_changes_render(self, qapp):
        a = self._button()
        a._angle = 0
        b = self._button()
        b._angle = 120
        assert a.grab().toImage() != b.grab().toImage()

    def test_filled_and_glow_render_differently(self, qapp):
        plain = self._button()
        filled = self._button()
        filled.filled = True
        glow = self._button()
        glow.glow = True
        assert plain.grab().toImage() != filled.grab().toImage()
        assert plain.grab().toImage() != glow.grab().toImage()

    def test_clicked(self, qapp):
        button = self._button()
        seen = []
        button.clicked.connect(lambda: seen.append(True))
        button.mouseReleaseEvent(QMouseEvent(
            QEvent.MouseButtonRelease, QPointF(button.rect().center()),
            Qt.LeftButton, Qt.LeftButton, Qt.NoModifier))
        assert seen == [True]


class TestSparklesText:
    def _sparkles(self, text="Powered by AI", count=14):
        from Custom_Widgets.QCustomSparklesText import QCustomSparklesText
        w = QCustomSparklesText(text=text, sparkleCount=count)
        w.resize(300, 60)
        return w

    def test_particle_count(self, qapp):
        assert len(self._sparkles().sparkles()) == 14

    def test_zero_particles_is_safe(self, qapp):
        widget = self._sparkles(count=0)
        assert widget.sparkles() == []
        widget.grab()

    def test_particles_are_deterministic(self, qapp):
        """A random field cannot be screenshotted reproducibly or tested."""
        a = self._sparkles()
        b = self._sparkles()
        a._phase = b._phase = 0.37
        assert [(round(x, 6), round(y, 6)) for x, y, _s, _o, _c in a.sparkles()] == \
               [(round(x, 6), round(y, 6)) for x, y, _s, _o, _c in b.sparkles()]

    def test_seed_changes_the_field(self, qapp):
        a = self._sparkles()
        b = self._sparkles()
        b.seed = 99
        assert a.sparkles()[0][0] != b.sparkles()[0][0]

    def test_particles_stay_inside_the_widget(self, qapp):
        widget = self._sparkles()
        for phase in (0.0, 0.25, 0.5, 0.75):
            widget._phase = phase
            for x, y, _s, _o, _c in widget.sparkles():
                assert 0 <= x <= widget.width()
                assert -5 <= y <= widget.height() + 5

    def test_opacity_never_negative(self, qapp):
        """A negative alpha would invert the sparkle instead of fading it."""
        widget = self._sparkles()
        for phase in (0.0, 0.1, 0.3, 0.6, 0.9):
            widget._phase = phase
            assert all(o >= 0.0 for _x, _y, _s, o, _c in widget.sparkles())

    def test_phase_changes_render(self, qapp):
        a = self._sparkles()
        a._phase = 0.1
        b = self._sparkles()
        b._phase = 0.6
        assert a.grab().toImage() != b.grab().toImage()

    def test_animation_stops_when_hidden(self, qapp):
        widget = self._sparkles()
        widget.show()
        assert widget.isAnimating() is True
        widget.hide()
        assert widget.isAnimating() is False

    def test_colors_csv(self, qapp):
        widget = self._sparkles()
        widget.colorsCsv = "#ff0000,#00ff00"
        assert widget.colorsCsv == "#ff0000,#00ff00"
        assert widget.setColors([]) is False


class TestMotionTokens:
    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        from Custom_Widgets.QCustomNumberCounter import QCustomNumberCounter
        from Custom_Widgets.QCustomTypewriterText import QCustomTypewriterText
        applyDesignTokens(qapp, theme="light")
        counter = QCustomNumberCounter()
        typer = QCustomTypewriterText(autoStart=False)
        counter.ensurePolished()
        typer.ensurePolished()
        assert counter.textColor.name().lower() == "#0f172a"
        assert typer.caretColor.name().lower() == "#2563eb"
        qapp.setStyleSheet("")
