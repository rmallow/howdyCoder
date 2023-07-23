from ..commonUtil.sparseDictList import SparseDictList

import typing

from PySide6 import QtCore


class SparseDictListModel(QtCore.QAbstractTableModel):
    modelUpdated = QtCore.Signal(SparseDictList)

    def __init__(self, *args, period=None, **kwargs):
        super().__init__()
        self.dictList: SparseDictList = SparseDictList()
        self.period = period
        self.show_index = False

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return self.dictList.getLengthOfLongestList()

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.dictList)

    def data(self, index: QtCore.QModelIndex, role: int) -> typing.Any:
        """
        Override QAbstractTableModel data for displaying dictList data
        """
        if role == QtCore.Qt.DisplayRole:
            key = self.dictList.getNthKey(index.column())
            if index.row() < len(self.dictList[key]):
                return self.dictList[key][index.row()].to_string(self.show_index)
            else:
                return "---"
        else:
            return None

    def headerData(
        self, section: int, orientation: QtCore.Qt.Orientation, role: int
    ) -> typing.Any:
        """
        Override QAbstractTableModel header data for displaying column/row header based off dictList
        """
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.dictList.getNthKey(section)
            else:
                if self.dictList.index is not None:
                    try:
                        return self.dataList.index[section].strftime(
                            "%m/%d/%Y, %H:%M:%S"
                        )
                    except AttributeError:
                        return self.dataList.index[section]
                else:
                    return section
        return None

    def appendData(self, data: SparseDictList) -> None:
        """
        Add new rows to the dataframe and remove if needed for period
        """
        if self.period is not None and (
            self.rowCount() + data.getLengthOfLongestList() >= self.period
            or any(k not in self.dictList for k in data.keys())
        ):
            self.beginResetModel()
            self.dictList.appendDictList(data)
            self.dictList = self.dictList.sliceDictListEnd(self.period)
            self.dictList.longest_list = self.period
            self.endResetModel()
        else:
            self.insertRows(self.rowCount(), data)

        self.modelUpdated.emit(data)

    @QtCore.Slot()
    def changeState(self, state: int):
        if self.show_index != (state == QtCore.Qt.CheckState.Checked):
            self.beginResetModel()
            self.show_index = state == QtCore.Qt.CheckState.Checked
            self.endResetModel()

    def removeRows(self, rowStart, count, beginRemove=True):
        """
        Function to remove rows from the dataframe and from the table model
        """
        if beginRemove:
            self.beginRemoveRows(QtCore.QModelIndex(), rowStart, rowStart + count - 1)
        firstHalf = self.dictList.sliceDictList(0, rowStart)
        secondHalf = self.dictList.sliceDictListEnd(rowStart + count)
        self.dictList = firstHalf.appendDictList(secondHalf)
        if beginRemove:
            self.endRemoveRows()

    def insertRows(self, rowStart: int, data: SparseDictList, beginChanges=True):
        """
        Add new rows to the dictList, if dictList is empty, resetModel to get column changes
        otherwise just beginInsertRows as it is far more efficient
        """
        resetModel = False
        if beginChanges:
            if self.rowCount() == 0 or self.columnCount() == 0:
                self.beginResetModel()
                resetModel = True
            else:
                self.beginInsertRows(
                    QtCore.QModelIndex(),
                    rowStart,
                    self.rowCount() + data.getLengthOfLongestList() - 1,
                )

        self.dictList.appendDictList(data)

        if resetModel:
            self.endResetModel()
        elif beginChanges:
            self.endInsertRows()
