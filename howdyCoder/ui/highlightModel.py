from .util import abstractQt

from PySide6 import QtGui, QtCore, QtWidgets
from abc import abstractmethod


HIGHLIGHT_ROLE = QtCore.Qt.UserRole + 10  # arbitrary


class HighlightBaseModel(
    QtGui.QStandardItemModel,
    metaclass=abstractQt.getAbstractQtResolver(QtGui.QStandardItemModel),
):
    """
    QStandardItemModel that colors specified indexes for trees
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oldIndex: QtCore.QModelIndex = None

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    @abstractmethod
    def changeIndexState(self, index: QtCore.QModelIndex, state: bool):
        pass

    @QtCore.Slot()
    def changeTextColor(self, index: QtCore.QModelIndex):
        self.changeIndexState(self.oldIndex, True)
        self.changeIndexState(index, False)
        self.oldIndex = index

    def clear(self):
        self.oldIndex = None
        super().clear()

    def setState(self, index, state):
        self.itemFromIndex(index).setEnabled(state)


class HighlightTreeModel(HighlightBaseModel):
    def changeIndexState(self, index: QtCore.QModelIndex, state: bool):
        if index is not None:
            while index.isValid():
                self.setState(index, state)
                index = index.parent()


class HighlightTableModel(HighlightBaseModel):
    def changeIndexState(self, index: QtCore.QModelIndex, state: bool):
        if index is not None:
            for x in range(index.model().columnCount()):
                new_index = index.siblingAtColumn(x)
                if new_index.isValid():
                    if new_index.data(HIGHLIGHT_ROLE) is not None:
                        if index.sibling(*new_index.data(HIGHLIGHT_ROLE)).isValid():
                            self.setState(
                                index.sibling(*new_index.data(HIGHLIGHT_ROLE)), state
                            )
                    else:
                        self.setState(new_index, state)
