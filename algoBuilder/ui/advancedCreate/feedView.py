from ..actionUIConstant import ActionEnum, DataSetEnum, ActionFuncEnum

import typing

from PySide2 import QtCore, QtWidgets, QtGui


class FeedTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent: typing.Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent=parent)
        self.columns: typing.List[typing.Dict[ActionEnum, typing.Any]] = []
        self.columnNames: typing.Set[str] = set()
        self.numDataSourceColumns = 0

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return ActionEnum.DISPLAY_ROWS.value

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.columns)

    def getActionColumns(self):
        return self.columns[self.numDataSourceColumns :]

    def data(
        self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole
    ) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            enumKey = ActionEnum(index.row())
            if enumKey in self.columns[index.column()]:
                rawValue = self.columns[index.column()][enumKey]
                if enumKey == ActionEnum.INPUT:
                    if isinstance(rawValue, list):
                        # Get the source vale from the list of dicts then join them with a comma separation
                        return ", ".join(
                            [
                                inputColDict[DataSetEnum.SOURCE]
                                for inputColDict in rawValue
                            ]
                        )
                    else:
                        # if it's not a dict or a list of dicts it should be a string from the data source
                        return rawValue
                elif enumKey == ActionEnum.ACTION_FUNC:
                    if ActionFuncEnum.NAME in rawValue:
                        return rawValue[ActionFuncEnum.NAME]
                else:
                    return rawValue
            return ""

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: int = QtCore.Qt.DisplayRole,
    ) -> typing.Any:
        if orientation == QtCore.Qt.Vertical:
            if role == QtCore.Qt.DisplayRole:
                return ActionEnum(section).display
        else:
            if role == QtCore.Qt.DisplayRole:
                if section < self.numDataSourceColumns:
                    return "Data Source"
                else:
                    return f"Action {section- self.numDataSourceColumns + 1}"
        return super().headerData(section, orientation, role=role)

    @QtCore.Slot()
    def insert(self, columnDict: typing.Dict[ActionEnum, typing.Any], index: int):
        if (
            columnDict is not None
            and ActionEnum.NAME in columnDict
            and columnDict[ActionEnum.NAME] not in self.columnNames
        ):
            self.beginInsertColumns(QtCore.QModelIndex(), index, index)
            self.columns.insert(index, columnDict)
            self.columnNames.add(columnDict[ActionEnum.NAME])
            self.endInsertColumns()

    def remove(self, index: QtCore.QModelIndex):
        if (
            index is not None
            and index.column() < len(self.columns)
            and index.column() > self.numDataSourceColumns - 1
        ):
            self.beginRemoveColumns(
                QtCore.QModelIndex(), index.column(), index.column()
            )
            del self.columns[index.column()]
            self.endRemoveColumns()

    def appendDataSource(self, columnDict: typing.Dict[ActionEnum, typing.Any]):
        self.insert(columnDict, self.numDataSourceColumns)
        self.numDataSourceColumns += 1

    def clearDataSources(self):
        for i in range(0, self.numDataSourceColumns):
            self.remove(self.index(0, i))
        self.numDataSourceColumns = 0


class FeedViewDelegate(QtWidgets.QStyledItemDelegate):
    """
    Subclassing paint to draw a line seperating data source columns and action columns
    """

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        if index.column() == index.model().numDataSourceColumns:
            painter.drawLine(option.rect.topLeft(), option.rect.bottomLeft())
        return super().paint(painter, option, index)


class FeedView(QtWidgets.QTableView):
    """
    Watch for right click events on table and send the name of the column right clicked to the action creator
    """

    rightClickName = QtCore.Signal(str)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if (event.button() == QtCore.Qt.RightButton) or (
            event.button() == QtCore.Qt.LeftButton
            and QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier
        ):
            index = self.indexAt(event.pos())
            if index is not None and index.isValid():
                nameIndex = index.siblingAtRow(ActionEnum.NAME.value)
                if nameIndex is not None and nameIndex.isValid():
                    name = nameIndex.data()
                    if name is not None and name != "":
                        self.rightClickName.emit(name)

        return super().mousePressEvent(event)
