from qtpy.QtCore import QEasingCurve, Qt
########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

# snake_case easing names (used by the chart widgets) -> QEasingCurve.Type.
# The CamelCase names handled by returnAnimationEasingCurve below are the
# QEasingCurve member names themselves, resolved via getattr.
_SNAKE_EASING = {
    "linear": QEasingCurve.Linear, "in_quad": QEasingCurve.InQuad,
    "out_quad": QEasingCurve.OutQuad, "in_out_quad": QEasingCurve.InOutQuad,
    "out_in_quad": QEasingCurve.OutInQuad, "in_cubic": QEasingCurve.InCubic,
    "out_cubic": QEasingCurve.OutCubic, "in_out_cubic": QEasingCurve.InOutCubic,
    "out_in_cubic": QEasingCurve.OutInCubic, "in_quart": QEasingCurve.InQuart,
    "out_quart": QEasingCurve.OutQuart, "in_out_quart": QEasingCurve.InOutQuart,
    "out_in_quart": QEasingCurve.OutInQuart, "in_quint": QEasingCurve.InQuint,
    "out_quint": QEasingCurve.OutQuint, "in_out_quint": QEasingCurve.InOutQuint,
    "out_in_quint": QEasingCurve.OutInQuint, "in_sine": QEasingCurve.InSine,
    "out_sine": QEasingCurve.OutSine, "in_out_sine": QEasingCurve.InOutSine,
    "out_in_sine": QEasingCurve.OutInSine, "in_expo": QEasingCurve.InExpo,
    "out_expo": QEasingCurve.OutExpo, "in_out_expo": QEasingCurve.InOutExpo,
    "out_in_expo": QEasingCurve.OutInExpo, "in_circ": QEasingCurve.InCirc,
    "out_circ": QEasingCurve.OutCirc, "in_out_circ": QEasingCurve.InOutCirc,
    "out_in_circ": QEasingCurve.OutInCirc, "in_elastic": QEasingCurve.InElastic,
    "out_elastic": QEasingCurve.OutElastic, "in_out_elastic": QEasingCurve.InOutElastic,
    "out_in_elastic": QEasingCurve.OutInElastic, "in_back": QEasingCurve.InBack,
    "out_back": QEasingCurve.OutBack, "in_out_back": QEasingCurve.InOutBack,
    "out_in_back": QEasingCurve.OutInBack, "in_bounce": QEasingCurve.InBounce,
    "out_bounce": QEasingCurve.OutBounce, "in_out_bounce": QEasingCurve.InOutBounce,
    "out_in_bounce": QEasingCurve.OutInBounce,
}


def easingCurveFromAny(value):
    """Normalize any easing input to a QEasingCurve.Type: accepts a
    QEasingCurve.Type, an int (its value), a CamelCase member name
    ("OutQuad"), or a snake_case name ("out_quad")."""
    if isinstance(value, QEasingCurve.Type):
        return value
    if isinstance(value, bool):
        return QEasingCurve.OutQuad
    if isinstance(value, int):
        try:
            return QEasingCurve.Type(value)
        except Exception:
            return QEasingCurve.OutQuad
    if isinstance(value, str):
        name = value.strip()
        if name in _SNAKE_EASING:
            return _SNAKE_EASING[name]
        member = getattr(QEasingCurve, name, None)
        if isinstance(member, QEasingCurve.Type):
            return member
    return QEasingCurve.OutQuad


def easingCurveToInt(value):
    """Easing input (name/int/QEasingCurve.Type) -> int, for @Property(int)."""
    return easingCurveFromAny(value).value


def returnAnimationEasingCurve(easingCurveName):
    # Accept ints and snake_case in addition to the CamelCase names below.
    if isinstance(easingCurveName, QEasingCurve.Type):
        return easingCurveName
    if isinstance(easingCurveName, int) and not isinstance(easingCurveName, bool):
        return easingCurveFromAny(easingCurveName)
    if isinstance(easingCurveName, str) and easingCurveName.strip() in _SNAKE_EASING:
        return _SNAKE_EASING[easingCurveName.strip()]

    if easingCurveName:
        if str(easingCurveName) == "OutQuad":
            return QEasingCurve.OutQuad
        elif str(easingCurveName) == "Linear":
            return QEasingCurve.Linear
        elif str(easingCurveName) == "InQuad":
            return QEasingCurve.InQuad
        elif str(easingCurveName) == "InOutQuad":
            return QEasingCurve.InOutQuad
        elif str(easingCurveName) == "OutInQuad":
            return QEasingCurve.OutInQuad
        elif str(easingCurveName) == "InCubic":
            return QEasingCurve.InCubic
        elif str(easingCurveName) == "OutCubic":
            return QEasingCurve.OutCubic
        elif str(easingCurveName) == "InOutCubic":
            return QEasingCurve.InOutCubic
        elif str(easingCurveName) == "OutInCubic":
            return QEasingCurve.OutInCubic
        elif str(easingCurveName) == "InQuart":
            return QEasingCurve.InQuart
        elif str(easingCurveName) == "OutQuart":
            return QEasingCurve.OutQuart
        elif str(easingCurveName) == "InOutQuart":
            return QEasingCurve.InOutQuart
        elif str(easingCurveName) == "OutInQuart":
            return QEasingCurve.OutInQuart
        elif str(easingCurveName) == "InQuint":
            return QEasingCurve.InQuint
        elif str(easingCurveName) == "OutQuint":
            return QEasingCurve.OutQuint
        elif str(easingCurveName) == "InOutQuint":
            return QEasingCurve.InOutQuint
        elif str(easingCurveName) == "InSine":
            return QEasingCurve.InSine
        elif str(easingCurveName) == "OutSine":
            return QEasingCurve.OutSine
        elif str(easingCurveName) == "InOutSine":
            return QEasingCurve.InOutSine
        elif str(easingCurveName) == "OutInSine":
            return QEasingCurve.OutInSine
        elif str(easingCurveName) == "InExpo":
            return QEasingCurve.InExpo
        elif str(easingCurveName) == "OutExpo":
            return QEasingCurve.OutExpo
        elif str(easingCurveName) == "InOutExpo":
            return QEasingCurve.InOutExpo
        elif str(easingCurveName) == "OutInExpo":
            return QEasingCurve.OutInExpo
        elif str(easingCurveName) == "InCirc":
            return QEasingCurve.InCirc
        elif str(easingCurveName) == "OutCirc":
            return QEasingCurve.OutCirc
        elif str(easingCurveName) == "InOutCirc":
            return QEasingCurve.InOutCirc
        elif str(easingCurveName) == "OutInCirc":
            return QEasingCurve.OutInCirc
        elif str(easingCurveName) == "InElastic":
            return QEasingCurve.InElastic
        elif str(easingCurveName) == "OutElastic":
            return QEasingCurve.OutElastic
        elif str(easingCurveName) == "InOutElastic":
            return QEasingCurve.InOutElastic
        elif str(easingCurveName) == "OutInElastic":
            return QEasingCurve.OutInElastic
        elif str(easingCurveName) == "InBack":
            return QEasingCurve.InBack
        elif str(easingCurveName) == "OutBack":
            return QEasingCurve.OutBack
        elif str(easingCurveName) == "InOutBack":
            return QEasingCurve.InOutBack
        elif str(easingCurveName) == "OutInBack":
            return QEasingCurve.OutInBack
        elif str(easingCurveName) == "InBounce":
            return QEasingCurve.InBounce
        elif str(easingCurveName) == "OutBounce":
            return QEasingCurve.OutBounce
        elif str(easingCurveName) == "InOutBounce":
            return QEasingCurve.InOutBounce
        elif str(easingCurveName) == "OutInBounce":
            return QEasingCurve.OutInBounce
        else:
            raise Exception("Unknown value'" +easingCurveName+ "' for setEasingCurve()")
########################################################################
##
########################################################################

########################################################################
##
########################################################################
def returnQtDirection(direction):
    if isinstance(direction, Qt.Orientation):
        return direction
    
    if direction:
        if str(direction) == "horizontal":
            return Qt.Horizontal
        elif str(direction) == "vertical":
            return Qt.Vertical
        else:
            raise Exception("Unknown direction name given ("+direction+"), please use Vertical or Horizontal direction")

    else:
        raise Exception("Empty direction name given, please use Vertical or Horizontal direction")
