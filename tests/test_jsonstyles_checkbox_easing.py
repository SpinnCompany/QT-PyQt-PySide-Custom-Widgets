"""Regression: a style.json QCustomCheckBox block with animationEasingCurve
crashed with AttributeError — JSonStyles called self.returnAnimationEasingCurve
(self being the user's MainWindow) instead of the imported free function.
This is what killed the old examples/PySide6/QCustomCheckBox demo.
"""
import json

from qtpy.QtCore import QEasingCurve
from qtpy.QtWidgets import QMainWindow


def test_checkbox_easing_curve_from_style_json(qapp, tmp_path):
    from Custom_Widgets.JSonStyles import configure_custom_check_box
    from Custom_Widgets.QCustomCheckBox import QCustomCheckBox

    style = {
        "QCustomCheckBox": [
            {
                # Deliberately NOT the widget default (OutBounce), so the
                # assertion proves the json value was applied.
                "name": "demoCheck",
                "animationEasingCurve": "InOutQuad",
                "animationDuration": 250,
            }
        ]
    }
    style_file = tmp_path / "style.json"
    style_file.write_text(json.dumps(style))

    window = QMainWindow()

    class Ui:
        pass

    window.ui = Ui()
    window.ui.demoCheck = QCustomCheckBox(window)
    window.ui.demoCheck.setObjectName("demoCheck")

    data = json.loads(style_file.read_text())
    # Crashed before the fix: AttributeError on MainWindow.returnAnimationEasingCurve
    configure_custom_check_box(window, data)

    from Custom_Widgets.QPropertyAnimation import easingCurveToInt

    # The property getter reports the int code of the applied curve.
    assert window.ui.demoCheck.animationEasingCurve == easingCurveToInt(
        QEasingCurve.InOutQuad)
    assert window.ui.demoCheck.animationDuration == 250
