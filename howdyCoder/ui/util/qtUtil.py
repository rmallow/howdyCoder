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
