from PySide2 import QtGui, QtCore
from abc import ABC, abstractmethod


HIGHLIGHT_ROLE = QtCore.Qt.UserRole + 10  # arbitrary


class HighlightBaseModelMeta(type(ABC), type(QtGui.QStandardItemModel)):
    pass


class HighlightBaseModel(
    QtGui.QStandardItemModel, ABC, metaclass=HighlightBaseModelMeta
):
    """
    QStandardItemModel that colors specified indexes for trees
    """

    def __init__(self, *args, color=QtGui.QColor(QtCore.Qt.red), **kwargs):
        self.oldIndex: QtCore.QModelIndex = None
        self.color = color
        super().__init__(*args, **kwargs)

    @abstractmethod
    def changeIndexColor(self, index: QtCore.QModelIndex, color: QtGui.QColor):
        pass

    @QtCore.Slot()
    def changeTextColor(self, index: QtCore.QModelIndex):
        self.changeIndexColor(self.oldIndex, QtGui.QColor(QtCore.Qt.white))
        self.changeIndexColor(index, self.color)
        self.oldIndex = index

    def clear(self):
        self.oldIndex = None
        super().clear()


class HighlightTreeModel(HighlightBaseModel):
    def changeIndexColor(self, index: QtCore.QModelIndex, color: QtGui.QColor):
        if index is not None:
            while index.isValid():
                self.setData(index, color, QtCore.Qt.ForegroundRole)
                index = index.parent()


class HighlightTableModel(HighlightBaseModel):
    def changeIndexColor(self, index: QtCore.QModelIndex, color: QtGui.QColor):
        if index is not None:
            for x in range(index.model().columnCount()):
                new_index = index.siblingAtColumn(x)
                if new_index.isValid():
                    if new_index.data(HIGHLIGHT_ROLE) is not None:
                        if index.sibling(*new_index.data(HIGHLIGHT_ROLE)).isValid():
                            self.setData(
                                index.sibling(*new_index.data(HIGHLIGHT_ROLE)),
                                color,
                                QtCore.Qt.ForegroundRole,
                            )
                    else:
                        self.setData(new_index, color, QtCore.Qt.ForegroundRole)
