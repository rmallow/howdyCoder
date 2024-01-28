import typing

from PySide6 import QtWidgets, QtCore, QtGui


def setWordWrapOnButton(button: QtWidgets.QPushButton):
    text = button.text()
    button.setText("")
    label = QtWidgets.QLabel(text, button)
    label.setWordWrap(True)
    layout = QtWidgets.QHBoxLayout(button)
    layout.addWidget(label, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
    button.setLayout(layout)


class CompleterDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent: QtCore.QObject | None = ...) -> None:
        self._completer_strings: typing.List[str] = []
        super().__init__(parent)

    def setCompleterStrings(self, string_list):
        self._completer_strings = string_list

    def createEditor(
        self,
        parent: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
    ) -> QtWidgets.QWidget:
        editor = super().createEditor(parent, option, index)
        setCompleter(editor, self._completer_strings)
        return editor


def setCompleter(editor: QtWidgets.QWidget, completer_strings: typing.List[str]):
    try:
        editor.setCompleter(QtWidgets.QCompleter())
    except:
        return None
    completer = QtWidgets.QCompleter(completer_strings, editor)
    editor.setCompleter(completer)
    return completer


class StayOnTopInFocus:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        QtGui.QGuiApplication.instance().applicationStateChanged.connect(
            self.changeAlwaysOnTop
        )

    def changeAlwaysOnTop(self, state: QtCore.Qt.ApplicationState):
        self.setWindowFlag(
            QtCore.Qt.WindowType.WindowStaysOnTopHint,
            state == QtCore.Qt.ApplicationState.ApplicationActive,
        )
        self.show()


class ExpandingLabelWidget(QtWidgets.QWidget):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout(self)
        self.label = ElidedLabel(text)
        self.label.setMaximumWidth(200)
        self.setSizePolicy(
            self.sizePolicy().horizontalPolicy(), QtWidgets.QSizePolicy.Policy.Maximum
        )

        self.button = QtWidgets.QPushButton("+")
        self.button.released.connect(self.label.toggleExpansion)
        layout.addWidget(self.button)
        layout.addWidget(self.label)


class ElidedLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._elide_mode = QtCore.Qt.TextElideMode.ElideRight
        self._button_disabled = False
        self._collapsed = True

    def setElideMode(self, mode: QtCore.Qt.TextElideMode):
        self._elide_mode = mode
        self.update()

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        if self._elide_mode == QtCore.Qt.TextElideMode.ElideNone:
            return super().paintEvent(e)
        painter = QtGui.QPainter(self)
        fm = self.fontMetrics()
        rect = self.contentsRect()
        painter.drawText(
            rect,
            self.alignment(),
            fm.elidedText(self.text(), self._elide_mode, rect.width()),
        )

    def animationFinished(self):
        if self._collapsed:
            self.setWordWrap(False)
            self.setElideMode(QtCore.Qt.TextElideMode.ElideRight)
        self._button_disabled = False

    @QtCore.Slot()
    def toggleExpansion(self):
        if not self._button_disabled:
            self._button_disabled = True
            min_height = max_height = text_flag = 0
            if self._elide_mode == QtCore.Qt.TextElideMode.ElideNone:
                self._collapsed = True
                text_flag = QtCore.Qt.TextFlag.TextSingleLine
            else:
                self._collapsed = False
                self.setWordWrap(True)
                self.setElideMode(QtCore.Qt.TextElideMode.ElideNone)
                text_flag = QtCore.Qt.TextFlag.TextWordWrap

            fm = self.fontMetrics()
            rect = self.rect()
            rect.setHeight(10000)
            min_height = max_height = fm.boundingRect(
                rect, text_flag, self.text()
            ).height()
            self.min_anim = QtCore.QPropertyAnimation(self, b"minimumHeight")
            self.min_anim.setDuration(1000)
            self.min_anim.setStartValue(self.minimumHeight())
            self.min_anim.setEndValue(min_height)

            self.max_anim = QtCore.QPropertyAnimation(self, b"maximumHeight")
            self.max_anim.setDuration(1000)
            self.max_anim.setStartValue(self.maximumHeight())
            self.max_anim.setEndValue(max_height)
            self.group = QtCore.QParallelAnimationGroup()
            self.group.addAnimation(self.min_anim)
            self.group.addAnimation(self.max_anim)
            self.group.start()
            self.group.finished.connect(self.animationFinished)
