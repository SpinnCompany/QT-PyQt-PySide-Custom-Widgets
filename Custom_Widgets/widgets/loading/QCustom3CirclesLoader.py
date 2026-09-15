# ///////////////////////////////////////////////////////////////
#
# Copyright 2021 by Parham Oyan and Oleg Frolov
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////
# Edits and improvements made by Khamisi Kibet
# QT GUI BY SPINN TV(YOUTUBE)

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

class RoundedRect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class QCustom3CirclesLoader(QFrame):
    # Qt Designer contract. WIDGET_MODULE is the FLAT public path --
    # Custom_Widgets.QCustom3CirclesLoader is what .ui files carry in <header>, not the
    # subpackage this file now lives in.
    __catalog__ = {
        "name": "QCustom3CirclesLoader",
        "props": {
            "color": {},
            "penWidth": {},
            "animationDuration": {},
        },
        # Accurate as of the token conversion: the colour default now resolves
        # through activeDesignTokens().role("accent"). Declared only because it
        # is now true — most self-painted widgets still own their colours and
        # correctly declare nothing here.
        "tokens_used": ["accent"],
    }
    WIDGET_MODULE = "Custom_Widgets.QCustom3CirclesLoader"
    WIDGET_TOOLTIP = "A three-circle bouncing loading animation"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustom3CirclesLoader' name='qCustom3CirclesLoader'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>64</width><height>64</height></rect></property>
        </widget>
    </ui>
    """

    # Rich editors for the Designer "Custom Properties" dock (see
    # DesignerTools.CustomPropertiesDock).
    DESIGNER_CUSTOM_PROPS = [
        {"name": "color", "kind": "color", "group": "Colors"},
        {"name": "penWidth", "kind": "int", "group": "General"},
        {"name": "animationDuration", "kind": "int", "group": "Animation"},
    ]

    @Property(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = QColor(value)
        self.update()

    @Property(int)
    def penWidth(self):
        return self._penWidth

    @penWidth.setter
    def penWidth(self, value):
        self._penWidth = int(value)
        self.update()

    @Property(int)
    def animationDuration(self):
        return self._animationDuration

    @animationDuration.setter
    def animationDuration(self, value):
        self._animationDuration = int(value)

    @staticmethod
    def _defaultColor():
        """The accent role when the app is token-themed, else the old #333333.

        This widget paints itself, so the token QSS that styles most of the
        library cannot reach it — the same gap QCustomChartThemeManager exists
        to close for charts. The default used to be a hard "#333333", which is
        invisible on a dark background: the loader looked broken to every user
        on a dark theme. (Its sibling QCustomArcLoader had the mirror image of
        this bug, defaulting to white.)

        activeDesignTokens() returns None when nothing has applied tokens, and
        its docstring is explicit that None must mean "fall back" rather than
        "assume a default". So an untokenised app keeps exactly the behaviour
        it had.
        """
        try:
            from Custom_Widgets.theming.tokens import activeDesignTokens
            tokens = activeDesignTokens()
            if tokens is not None:
                return QColor(tokens.role("accent"))
        except Exception:
            pass
        return QColor("#333333")

    def __init__(
            self,
            parent=None,
            color=None,
            penWidth=20,
            animationDuration=400
            ):
        QFrame.__init__(self, parent=parent)

        self.setFrameShape(QFrame.NoFrame)
        self.setFixedSize(140, 140)

        # None means "follow the theme"; an explicit colour still wins.
        self.color = self._defaultColor() if color is None else color
        self.penWidth = penWidth
        self.animationDuration = animationDuration

        self.initRects()
        
        self.startAnimations()
    
    def initRects(self):
        x = self.penWidth/2
        self.rectsList = [
            RoundedRect(x, x, 40, 40),
            RoundedRect(x+80, x, 40, 40),
            RoundedRect(x, x+80, 40, 40)
        ]
    
    def getVariantAnimation(self):
        animation = QVariantAnimation(self)
        animation.setDuration(self.animationDuration)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        return animation

    # ANIMATION INITALIZER METHODS ==============================================================
    
    def initMoveDownAnimation(self):
        self.moveDownGP = QSequentialAnimationGroup(self)

        animation = self.getVariantAnimation()
        animation.setStartValue(40)
        animation.setEndValue(120)
        animation.valueChanged.connect(self.moveDownUpdateH)
        self.moveDownGP.addAnimation(animation)

        animation = self.getVariantAnimation()
        animation.setStartValue(10)
        animation.setEndValue(90)
        animation.valueChanged.connect(self.moveDownUpdateY)
        self.moveDownGP.addAnimation(animation)
    
    def initMoveRightAnimation(self):
        self.moveRightGP = QSequentialAnimationGroup(self)

        animation = self.getVariantAnimation()
        animation.setStartValue(40)
        animation.setEndValue(120)
        animation.valueChanged.connect(self.moveRightUpdateW)
        self.moveRightGP.addAnimation(animation)

        animation = self.getVariantAnimation()
        animation.setStartValue(10)
        animation.setEndValue(90)
        animation.valueChanged.connect(self.moveRightUpdateX)
        self.moveRightGP.addAnimation(animation)

    def initMoveUpAnimation(self):
        self.moveUpGP = QSequentialAnimationGroup(self)

        animation = QVariantAnimation(self)
        animation.setDuration(self.animationDuration)
        animation.setStartValue(90)
        animation.setEndValue(10)
        animation.valueChanged.connect(self.moveUpUpdateY)
        self.moveUpGP.addAnimation(animation)

        animation = self.getVariantAnimation()
        animation.setStartValue(120)
        animation.setEndValue(40)
        animation.valueChanged.connect(self.moveUpUpdateH)
        self.moveUpGP.addAnimation(animation)

    def initMoveLeftAnimation(self):
        self.moveLeftGP = QSequentialAnimationGroup(self)

        animation = self.getVariantAnimation()
        animation.setStartValue(90)
        animation.setEndValue(10)
        animation.valueChanged.connect(self.moveLeftUpdateX)
        self.moveLeftGP.addAnimation(animation)

        animation = self.getVariantAnimation()
        animation.setStartValue(120)
        animation.setEndValue(40)
        animation.valueChanged.connect(self.moveLeftUpdateH)
        self.moveLeftGP.addAnimation(animation)

    # UPDATE METHODS ==============================================================

    def moveDownUpdateH(self, newValue):
        self.rectsList[1].h = newValue
        self.update()
    
    def moveDownUpdateY(self, newValue):
        self.rectsList[1].y = newValue
        self.rectsList[1].h = 130-newValue
        self.update()
    
    def moveRightUpdateW(self, newValue):
        self.rectsList[0].w = newValue
        self.update()

    def moveRightUpdateX(self, newValue):
        self.rectsList[0].x = newValue
        self.rectsList[0].w = 130-newValue
        self.update()

    def moveUpUpdateY(self, newValue):
        self.rectsList[2].y = newValue
        self.rectsList[2].h = 130-newValue
        self.update()

    def moveUpUpdateH(self, newValue):
        self.rectsList[2].h = newValue
        self.update()

    def moveLeftUpdateX(self, newValue):
        self.rectsList[1].x = newValue
        self.rectsList[1].w = 130-newValue
        self.update()

    def moveLeftUpdateH(self, newValue):
        self.rectsList[1].w = newValue
        self.update()

    # START ANIMATIONS METHOD ===========================================================

    def startAnimations(self):
        self.initMoveDownAnimation()
        self.initMoveRightAnimation()
        self.initMoveUpAnimation()
        self.initMoveLeftAnimation()
        gp = QSequentialAnimationGroup(self)
        gp.addAnimation(self.moveDownGP)
        gp.addAnimation(self.moveRightGP)
        gp.addAnimation(self.moveUpGP)
        gp.addAnimation(self.moveLeftGP)
        self.moveLeftGP.finished.connect(self.finished)
        gp.setLoopCount(10)
        gp.start()
    
    def finished(self):
        self.rectsList = [self.rectsList[2], self.rectsList[0], self.rectsList[1]]

    # OVERRIDE PAINT EVENT ==============================================================

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen()
        pen.setColor(self.color)
        pen.setWidth(self.penWidth)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        x = self.penWidth/2
        for rect in self.rectsList:
            painter.drawRoundedRect(rect.x, rect.y, rect.w, rect.h, 20, 20)
        painter.end()