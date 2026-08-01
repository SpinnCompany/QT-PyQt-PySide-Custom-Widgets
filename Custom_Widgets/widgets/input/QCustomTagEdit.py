from qtpy import QtGui, QtCore, QtWidgets
import typing

from Custom_Widgets.QCustomFlowLayout import QCustomFlowLayout


class QTagEdit(QtWidgets.QScrollArea):
    """A tag based edit"""

    def __init__(self, parent: QtWidgets = None, tag_suggestions: typing.List[str] = []):
        super().__init__(parent)

        # setup the ui stuff
        self.setWidgetResizable(True)

        self._main_widget = QtWidgets.QWidget()
        self._layout = QCustomFlowLayout(self._main_widget)

        self._tag_input = QtWidgets.QLineEdit()
        # self._tag_input.setPlaceholderText('Type in a new tag and hit enter...')
        self._tag_input.setFixedWidth(10)
        self._tag_input.setStyleSheet('border: 0px')
        self._tag_input.setContentsMargins(0, 5, 0, 0)
        self._tag_input.keyReleaseEvent = self.__tag_input_key_release_event

        self._layout.addWidget(self._tag_input)

        # No baked-in background. This used to snapshot the platform palette's
        # window colour into a stylesheet at construction, pinning the widget
        # to the OS theme: under a dark desktop it painted a dark slab whatever
        # the app's own theme said, and being a stylesheet it beat anything the
        # token QSS tried to set. Colours come from the properties below now.
        self._tagColor = QtGui.QColor("#e2e8f0")        # secondary
        self._tagTextColor = QtGui.QColor("#0f172a")    # on-secondary

        self.setWidget(self._main_widget)

        # setup all other things
        self.__font_calculator = QtGui.QFontMetrics(QtWidgets.QApplication.font())
        self.__tags = {}
        self.__tag_suggestions = tag_suggestions
        self._tag_suggestions = False
        self._check_for_doubles = True

    def focusInEvent(self, a0: QtGui.QFocusEvent) -> None:
        """Sets the focus always to `self._tag_input`"""
        self._tag_input.setFocus()

    def addTag(self, text: str) -> bool:
        """
        Adds a new tag

        Args:
            text: The text of the new tag

        Returns:
            If the tag was added successfully
        """
        # if `self._check_for_doubles` is True, it checks if the tag already exists
        if self._check_for_doubles and text.lower() in (tag.lower() for tag in self.__tags.keys()):
            self.onDoubledTag(text)
            return False
        else:
            # a new tag
            tag = self.__QTagFrame(self, text)
            # tag.setStyleSheet('border: 0px; margin: 0px; padding: 0px')

            self.__tags[text] = tag
            for tag_name in self.__tag_suggestions:
                # if the tag is in `self.__tag_suggestions` it will be removed from there
                if tag_name.lower() == text:
                    self.__tag_suggestions.remove(tag_name)
                    self.enableTagSuggestions(self._tag_suggestions)
                    break
            # insert the tag before the line edit
            self._layout.addWidget(tag, -1)
            return True

    def clear(self, input=True) -> None:
        """
        Clears all tags

        Args:
            input: If True, the current text in the line edit will be cleared as well
        """
        for i in range(self._layout.count()):
            widget = self._layout.itemAt(i).widget()
            if type(widget) == QtWidgets.QLineEdit and input:
                widget.clear()
            elif type(widget) == self.__QTagFrame:
                self.removeTag(widget.text())

    def enableCheckForDoubles(self, check_for_doubles) -> None:
        """
        Enables if a new tag, when its going to be added, should be checked if it already exists

        Args:
            check_for_doubles: True if double checking should be active, False if not
        """
        self._check_for_doubles = check_for_doubles

    def enableTagSuggestions(self, tag_suggestions: bool) -> None:
        """
        Enables whenever a new tag is typed in that suggestions from `self.__tag_suggestions(...)` should be showing or not.
        They can be added on the class initialization or via `setTagSuggestions`

        Args:
            tag_suggestions: If tag suggestions should be active or not
        """
        self._tag_suggestions = tag_suggestions
        if tag_suggestions:
            # sets the completer for the line edit
            completer = QtWidgets.QCompleter(self.__tag_suggestions)
            completer.setCompletionMode(completer.InlineCompletion)
            completer.setCaseSensitivity(QtCore.Qt.CaseSensitive)
            self._tag_input.setCompleter(completer)
        else:
            self._tag_input.setCompleter(None)

    def onDoubledTag(self, text: str) -> None:
        """
        This method gets called if `self._check_for_doubles` is True (can be set via `enableCheckForDoubles(...)`)
        and a new tag which already exists are going to be added.
        This method is actually there to display an error message

        Args:
            text: The text of the new tag
        """
        button = QtWidgets.QMessageBox()

        # if `self.tag_input.keyReleaseEvent`is not overridden, it would trigger itself when the enter key is pressed
        # to close the popup and open it again. idk why
        def reset(a0: QtGui.QKeyEvent):
            if a0.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                button.destroy()
                self._tag_input.keyReleaseEvent = self.__tag_input_key_release_event

        self._tag_input.keyReleaseEvent = reset

        # shows the warning
        button.warning(self, 'Tag already exists', f'The tag {text} already exists')

    def removeTag(self, tag: str) -> None:
        """
        Removes a tag

        Args:
            The tag to remove
        """
        if tag in self.__tags:
            self._layout.removeWidget(self.__tags[tag])
            del self.__tags[tag]

    def setTags(self, tags: typing.List[str]) -> None:
        """
        Replaces all current tags with tag from the `tags` argument

        Args:
            tags: The new tags to be set
        """
        self.clear()
        for tag in tags:
            self.addTag(tag)

    def setTagSuggestions(self, suggestions: typing.List[str]) -> None:
        """
        Sets the tag suggestions. They will be used if `self._tag_suggestions` is True (can be set via `enableTagSuggestions(...)`)
        and will be shown if a new tag is typed in

        Args:
            suggestions: The new tag suggestions
        """
        self.__tag_suggestions = suggestions
        self.enableTagSuggestions(self._tag_suggestions)

    def tags(self) -> typing.Union[typing.List[str]]:
        """
        Returns all tag names

        Returns:
            All tag names
        """
        return list(self.__tags.keys())

    def __tag_input_key_release_event(self, a0: QtGui.QKeyEvent) -> None:
        """
        The `keyReleaseEvent(...)` of the line edit. Whenever return / enter is pressed, the current text in the line edit
        will be added as new tag. It also expands the width of the line edit if the text in it is over an specific limit
        """
        if a0.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            # adds the tag
            if self.addTag(self._tag_input.text()):
                self._tag_input.clear()
                self._tag_input.setFixedWidth(10)
            return
        elif a0.key() in (QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete):
            # calculates the current line edit text width
            width = self.__font_calculator.width(self._tag_input.text())
            if width + 10 < self._tag_input.width():
                self._tag_input.setFixedWidth(width + 10)
        else:
            # calculates the current line edit text width
            width = self.__font_calculator.width(self._tag_input.text())
            # this resizes the tag input if the text in it will be longer than it's width.
            # not the best way, but it does what it does
            if width + 20 > self._tag_input.width():
                self._tag_input.setFixedWidth(width + 20)

    class __QTagFrame(QtWidgets.QFrame):
        """The tag class for the QTagEdit tags"""

        def __init__(self, parent, text: str):
            super().__init__()

            # setup the ui stuff
            self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
            self.setLayout(QtWidgets.QHBoxLayout())
            self.setContentsMargins(3, 0, 3, 0)

            # the tag name label
            self._name = QtWidgets.QLabel()
            self._name.setText(text)
            self._name.setStyleSheet('background: transparent')

            # the tag delete button
            self._delete_button = QtWidgets.QPushButton()
            self._delete_button.setStyleSheet('QPushButton {'
                                              '     background: transparent;'
                                              '     border: 0px;'
                                              '}')
            self._delete_button.clicked.connect(self.onDeleteButtonClick)
            self._delete_button.setCursor(QtCore.Qt.PointingHandCursor)

            self.layout().addWidget(self._name)
            self.layout().addWidget(self._delete_button)

            # setup all other things
            self.__parent = parent
            self._text = text

        def onDeleteButtonClick(self) -> None:
            """This will get triggered if the delete button on a tag is pressed"""
            self.__parent.removeTag(self.text())
            self.__parent._tag_input.setFocus()

        def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
            """Styles the tag from the parent's themed colours."""
            fill = self.__parent.tagColor
            text = self.__parent.tagTextColor

            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QBrush(fill, QtCore.Qt.SolidPattern))

            # draws the tag 'filling'
            painter.drawRoundedRect(0, 0, self.width() - 5, self.height(), self.height() / 2, self.height() / 2)

            # The delete affordance is DRAWN. It used to be the '✕' glyph,
            # which the design lint bans: it does not tint, does not scale and
            # is a different picture on every platform.
            centre = QtCore.QPointF(self.width() - 25, self.height() / 2)
            arm = 3.5
            pen = QtGui.QPen(text, 1.6)
            pen.setCapStyle(QtCore.Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(QtCore.QPointF(centre.x() - arm, centre.y() - arm),
                             QtCore.QPointF(centre.x() + arm, centre.y() + arm))
            painter.drawLine(QtCore.QPointF(centre.x() - arm, centre.y() + arm),
                             QtCore.QPointF(centre.x() + arm, centre.y() - arm))

        def text(self) -> str:
            """
            Returns the current tag text

            Returns:
                The tag text

            """
            return self._text
    # ---------------------------------------------------------------- #
    ## Designer properties
    #
    # Driven by the token QSS so the tags flip with the app theme instead
    # of following whatever the desktop palette happens to be.
    # ---------------------------------------------------------------- #
    @QtCore.Property(QtGui.QColor)
    def tagColor(self):
        return self._tagColor

    @tagColor.setter
    def tagColor(self, value):
        self._tagColor = QtGui.QColor(value)
        self.update()

    @QtCore.Property(QtGui.QColor)
    def tagTextColor(self):
        return self._tagTextColor

    @tagTextColor.setter
    def tagTextColor(self, value):
        self._tagTextColor = QtGui.QColor(value)
        for tag in self.__dict__.get('_QTagEdit__tags', {}).values():
            tag._name.setStyleSheet(
                'background: transparent; color: %s' % self._tagTextColor.name())
        self.update()
