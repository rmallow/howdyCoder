import typing

from PySide6 import QtCore
import pandas as pd


class pandasModel(QtCore.QAbstractTableModel):
    modelUpdated = QtCore.Signal(pd.DataFrame)

    def __init__(self, *args, period=None, **kwargs):
        super().__init__()
        self.df: pd.DataFrame = pd.DataFrame()
        self.period = period

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.df.index)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.df.columns)

    def data(self, index: QtCore.QModelIndex, role: int) -> typing.Any:
        """
        Override QAbstractTableModel data for displaying pandas dataframe data
        """
        if role == QtCore.Qt.DisplayRole:
            return str(self.df.iloc[index.row(), index.column()])
        else:
            return None

    def headerData(
        self, section: int, orientation: QtCore.Qt.Orientation, role: int
    ) -> typing.Any:
        """
        Override QAbstractTableModel header data for displaying column/row header based off pandas dataframe
        """
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.df.columns[section]
            else:
                try:
                    return self.df.index[section].strftime("%m/%d/%Y, %H:%M:%S")
                except AttributeError:
                    return str(self.df.index[section])
        return None

    def appendDataFrame(self, dataframe):
        """
        Add new rows to the dataframe and remove if needed for period
        """
        if (
            self.period is not None
            and len(self.df.index) + len(dataframe.index) > self.period
        ):
            # Remove rows so that the combined dataframes won't be more than the period
            self.beginResetModel()
            self.df = self.df.append(dataframe).tail(self.period)
            self.df = self.df.reset_index(drop=True)
            self.endResetModel()
        else:
            self.insertRows(self.rowCount(), dataframe)

        self.modelUpdated.emit(dataframe)

    def removeRows(self, rowStart, count, beginRemove=True):
        """
        Function to remove rows from the dataframe and from the table model
        """
        if beginRemove:
            self.beginRemoveRows(QtCore.QModelIndex(), rowStart, rowStart + count - 1)
        self.df = self.df.drop(self.df.index[rowStart : rowStart + count - 1])
        if beginRemove:
            self.endRemoveRows()

    def insertRows(self, rowStart, dataframe, beginChanges=True):
        """
        Add new rows to the dataframe, if df is empty, resetModel to get column changes
        otherwise just beginInsertRows as it is far more efficient
        """
        resetModel = False
        if beginChanges:
            if len(self.df.index) == 0 or len(self.df.columns) == 0:
                self.beginResetModel()
                resetModel = True
            else:
                self.beginInsertRows(
                    QtCore.QModelIndex(),
                    rowStart,
                    self.rowCount() + len(dataframe.index) - 1,
                )

        self.df = self.df.append(dataframe)
        self.df = self.df.reset_index(drop=True)

        if resetModel:
            self.endResetModel()
        elif beginChanges:
            self.endInsertRows()
