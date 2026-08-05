"""Theme broadcasts must never reach a dead chart.

Chart theme managers used to connect bound methods straight to the
QCustomTheme singleton; a chart whose Python wrapper was collected while its
C++ half was still dying could then be resurrected by a broadcast — a
GC-timing segfault (CI hit it on 3.10 and 3.13). The managers now register in
a module-level WeakSet the singleton fans out to, so dead ones simply drop
out. These tests pin both halves: dropped charts leave the listener set, and
the historical crash recipe (drop refs, collect, restyle the app twice) runs
clean.
"""
import gc
import importlib

# the qtcharts package re-exports the CLASS under this name; the module (with
# the dispatcher globals) must be imported explicitly
tm_module = importlib.import_module(
    "Custom_Widgets.widgets.charts.qtcharts.QCustomChartThemeManager")
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens  # noqa: E402


def _makeChart():
    from Custom_Widgets.widgets.charts.qtcharts.QCustomLineChart import (
        QCustomLineChart)
    chart = QCustomLineChart()
    chart.categoriesCsv = "Jan,Feb,Mar"
    chart.seriesCsv = "Revenue=12,19,15"
    return chart


class TestListenerLifetime:
    def test_collected_manager_leaves_the_listener_set(self, qapp):
        # Track OUR manager through a weakref and assert about it alone —
        # counting the whole listener set is hostage to whatever half-dead
        # charts previous tests left in the deferred-delete queue.
        import weakref

        chart = _makeChart()
        mgr_ref = weakref.ref(chart._theme_manager)
        assert mgr_ref() in tm_module._liveListeners()

        chart.deleteLater()
        del chart
        # deleteLater queues a DeferredDelete that plain processEvents at this
        # nesting level does not consume — flush explicitly, settling in a
        # bounded loop because how many flush × collect rounds the teardown
        # needs depends on what else is in the queue.
        from qtpy.QtCore import QCoreApplication, QEvent
        for _ in range(10):
            gc.collect()
            QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
            qapp.processEvents()
            manager = mgr_ref()
            if manager is None or manager not in tm_module._liveListeners():
                break

        manager = mgr_ref()
        assert manager is None or manager not in tm_module._liveListeners()

    def test_broadcast_after_drop_is_harmless(self, qapp):
        chart = _makeChart()
        del chart
        gc.collect()
        # fan the broadcast out directly: with the old wiring this is the
        # call path that resurrected a dying wrapper
        tm_module._broadcastThemeChanged()
        tm_module._broadcastThemeChangeComplete()

    def test_dropped_chart_then_token_switch(self, qapp):
        """The exact historical crash recipe, as a test."""
        _makeChart()                       # dropped immediately
        gc.collect()
        applyDesignTokens(qapp, theme="light")
        _makeChart()                       # a second carcass mid-restyle
        gc.collect()
        applyDesignTokens(qapp, theme="dark")
        applyDesignTokens(qapp, theme="light")
        qapp.setStyleSheet("")

    def test_live_chart_still_follows_broadcasts(self, qapp):
        """The weak dispatch must not break the feature it protects."""
        chart = _makeChart()
        applyDesignTokens(qapp, theme="light")
        chart._theme_manager.applyTheme(chart._chart)
        light = chart._chart.backgroundBrush().color().name()
        applyDesignTokens(qapp, theme="dark")
        chart._theme_manager.applyTheme(chart._chart)
        dark = chart._chart.backgroundBrush().color().name()
        assert light != dark
        chart.deleteLater()
        qapp.setStyleSheet("")
