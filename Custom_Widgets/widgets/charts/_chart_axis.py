########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## Shared cartesian axis maths for the painted charts.
##
## Extracted when Scatter became the second consumer - QCustomCandlestickChart
## had a minimal version inline. Kept deliberately small: ticks, nice-number
## rounding and label thinning are the three things every cartesian painted
## chart re-derives, and three divergent implementations of "nice ticks" is how
## charts end up disagreeing about where 0 is.
##
## Pure maths, no Qt: everything here is testable without a QApplication.
########################################################################
import math


def niceNumber(value, roundIt=True):
    """Round to a 1/2/5/10-style step. The classic Heckbert nice-number.

    Tick steps that are not 1, 2 or 5 times a power of ten read as arbitrary -
    a gridline every 3.7 units tells the eye nothing.
    """
    if value <= 0:
        return 0.0
    exponent = math.floor(math.log10(value))
    fraction = value / (10 ** exponent)
    if roundIt:
        nice = 1.0 if fraction < 1.5 else 2.0 if fraction < 3 else 5.0 if fraction < 7 else 10.0
    else:
        nice = 1.0 if fraction <= 1 else 2.0 if fraction <= 2 else 5.0 if fraction <= 5 else 10.0
    return nice * (10 ** exponent)


def niceTicks(low, high, count=5):
    """(start, stop, step) covering [low, high] on round numbers.

    Returns a range at least as wide as the data, so no point is ever painted
    outside the plot. A degenerate range (all values equal) is widened rather
    than returned as zero-width, which would divide by zero downstream.
    """
    if not (low == low) or not (high == high):        # NaN guard
        low, high = 0.0, 1.0
    if high < low:
        low, high = high, low
    if high - low < 1e-12:
        # A flat series still needs a drawable band around it.
        pad = abs(high) * 0.1 or 1.0
        low, high = low - pad, high + pad
    count = max(1, int(count))
    span = niceNumber(high - low, roundIt=False)
    step = niceNumber(span / count, roundIt=True) or 1.0
    start = math.floor(low / step) * step
    stop = math.ceil(high / step) * step
    return start, stop, step


def tickValues(low, high, count=5):
    """The tick positions themselves, inclusive of both ends."""
    start, stop, step = niceTicks(low, high, count)
    ticks, value = [], start
    # Accumulate rather than multiply so float drift cannot skip the last tick.
    guard = 0
    while value <= stop + step * 1e-6 and guard < 1000:
        ticks.append(round(value, 10))
        value += step
        guard += 1
    return ticks


def formatTick(value, step):
    """Render a tick with only as many decimals as the step needs.

    Derived from the step's actual decimal places, not from
    ceil(-log10(step)). That shortcut is right only when the step is a power
    of ten: a step of 0.25 needs two decimals but the log gives one, so the
    tick rendered as "0.2" and quietly lost a digit.
    """
    if step >= 1:
        return "%g" % round(value, 10)
    for decimals in range(0, 11):
        if abs(round(step, decimals) - step) < 1e-12:
            return "%.*f" % (decimals, value)
    return "%.10g" % value


def thinLabels(labels, available, widthOf, gap=10):
    """Indices of the labels that fit without overlapping.

    Charts that skip this either overlap their labels into mush or silently
    drop the last one. Always keeps the first label.
    """
    if not labels:
        return []
    slot = available / float(len(labels))
    widest = max((widthOf(text) for text in labels), default=1)
    stride = 1 if slot >= widest + gap else int(math.ceil((widest + gap) / max(slot, 1e-6)))
    return list(range(0, len(labels), max(1, stride)))


########################################################################
## Polar mapping — shared by the radial charts.
##
## Extracted from QCustomRadarChart when the radial charts became the second
## and third consumers. Same reasoning as the tick maths: three copies of
## "where does slot i sit on a circle" is three chances to disagree about
## which way the chart winds.
########################################################################
def polarAngle(index, count, startAngle=90.0, clockwise=True):
    """Radians for slot `index` of `count`, from `startAngle` degrees.

    Clockwise by default: chart convention runs the other way from the
    mathematical one, and getting it wrong mirrors the whole chart.
    """
    count = max(1, int(count))
    step = 2 * math.pi / count
    offset = index * step
    return math.radians(startAngle) + (-offset if clockwise else offset)


def polarPoint(centreX, centreY, radius, angle):
    """Cartesian point at `radius`/`angle`, in screen coordinates.

    Screen y grows downward, so the sine is subtracted — forgetting that
    flips the chart vertically and is easy to miss on a symmetric dataset.
    """
    return (centreX + radius * math.cos(angle),
            centreY - radius * math.sin(angle))
