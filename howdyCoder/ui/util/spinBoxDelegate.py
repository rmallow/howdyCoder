import typing

from PySide6 import QtWidgets, QtCore


class SpinBoxDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(
        self,
        min_: int,
        max_: int,
        disallowed_values: typing.List = None,
        disallowed_default_value: int = 1,
        parent: QtCore.QObject | None = None,
    ) -> None:
        self._min = min_
        self._max = max_
        self.disallowed_values = (
            set(disallowed_values) if disallowed_values is not None else set()
        )
        self.disallowed_default_value = disallowed_default_value
        super().__init__(parent)

    def createEditor(
        self,
        parent: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
    ) -> QtWidgets.QWidget:
        spin = QtWidgets.QSpinBox(parent)
        spin.setFrame(False)
        spin.setMinimum(self._min)
        spin.setMaximum(self._max)
        spin.editingFinished.connect(self.spinValueChanged)
        return spin

    def setEditorData(
        self,
        editor: QtWidgets.QSpinBox,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
    ) -> None:
        val = index.model().data(index, QtCore.Qt.ItemDataRole.EditRole)
        editor.setValue(val if val is not None else self.disallowed_default_value)
        return editor

    def setModelData(
        self,
        editor: QtWidgets.QSpinBox,
        model: QtCore.QAbstractItemModel,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
    ) -> None:
        editor.interpretText()
        val = (
            editor.value()
            if editor.value() not in self.disallowed_values
            else self.disallowed_default_value
        )
        model.setData(index, editor.value(), QtCore.Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(
        self,
        editor: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
    ) -> None:
        editor.setGeometry(option.rect)

    @QtCore.Slot()
    def spinValueChanged(self):
        if self.sender() and hasattr(self.sender(), "setValue"):
            self.sender().setValue(self.disallowed_default_value)
