from typing import Optional, Union
from PySide6 import QtWidgets, QtCore
import PySide6.QtCore
import PySide6.QtWidgets


class SpinBoxDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(
        self, min_: int, max_: int, parent: QtCore.QObject | None = None
    ) -> None:
        self._min = min_
        self._max = max_
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
        return spin

    def setEditorData(
        self,
        editor: QtWidgets.QSpinBox,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
    ) -> None:
        val = index.model().data(index, QtCore.Qt.ItemDataRole.EditRole)
        editor.setValue(val if val is not None else 1)
        return editor

    def setModelData(
        self,
        editor: QtWidgets.QSpinBox,
        model: QtCore.QAbstractItemModel,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
    ) -> None:
        editor.interpretText()
        model.setData(index, editor.value(), QtCore.Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(
        self,
        editor: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
    ) -> None:
        editor.setGeometry(option.rect)
