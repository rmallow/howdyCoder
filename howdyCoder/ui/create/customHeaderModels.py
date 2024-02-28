import typing

import pandas as pd
from PySide6 import QtGui, QtWidgets, QtCore


class CustomHeaderStandardModel(QtGui.QStandardItemModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._custom_header_added = False
        self._custom_header_is_first_row = False

    def addCustomHeader(
        self, data_in_rows: bool, override_headers: typing.List[str] = None
    ) -> None:
        if not self._custom_header_added:
            self._custom_header_added = True
            orientation = (
                QtCore.Qt.Orientation.Vertical
                if data_in_rows
                else QtCore.Qt.Orientation.Horizontal
            )
            count = self.rowCount() if data_in_rows else self.columnCount()
            header_str_items = []
            if override_headers is not None and len(override_headers) == count:
                header_str_items = [
                    QtGui.QStandardItem(header) for header in override_headers
                ]
            else:
                header_str_items = [
                    QtGui.QStandardItem(str(self.headerData(x, orientation)))
                    for x in range(count)
                ]
            if data_in_rows:
                self.insertColumn(0, header_str_items)
            else:
                self.insertRow(0, header_str_items)
                self._custom_header_is_first_row = True
            self.setHeaderData(
                0,
                (
                    QtCore.Qt.Orientation.Horizontal
                    if data_in_rows
                    else QtCore.Qt.Orientation.Vertical
                ),
                "Custom",
                role=QtCore.Qt.ItemDataRole.DisplayRole,
            )

    def removeCustomHeader(self) -> None:
        if self._custom_header_added:
            if self._custom_header_is_first_row:
                self.removeRow(0)
            else:
                self.removeColumn(0)
            self._custom_header_added = False

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        flags = (
            super().flags(index)
            & ~QtCore.Qt.ItemFlag.ItemIsEditable
            & ~QtCore.Qt.ItemFlag.ItemIsEnabled
        )
        if self._custom_header_added:
            if (index.row() == 0 and self._custom_header_is_first_row) or (
                index.column() == 0 and not self._custom_header_is_first_row
            ):
                flags |= (
                    QtCore.Qt.ItemFlag.ItemIsEditable | QtCore.Qt.ItemFlag.ItemIsEnabled
                )
        return flags


class CustomHeaderPandaModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._table: pd.DataFrame = None
        self._headers_by_orientation: typing.Dict[
            QtCore.Qt.Orientation, typing.List[str]
        ] = {}
        self._custom_header_strs: typing.List[str] = []

        self._custom_header_added = False
        self._custom_header_is_first_row = False

    def clear(self):
        self.beginResetModel()
        self._table = None
        self._headers_by_orientation = {}
        self._custom_header_strs = []
        self._custom_header_added = False
        self._custom_header_is_first_row = False
        self.endResetModel()

    def setHorizontalHeaderLabels(self, header_strs: typing.List):
        self._headers_by_orientation[QtCore.Qt.Orientation.Horizontal] = header_strs

    def setVerticalHeaderLabels(self, header_strs: typing.List):
        self._headers_by_orientation[QtCore.Qt.Orientation.Vertical] = header_strs

    def addCustomHeader(
        self, data_in_rows: bool, override_headers: typing.List[str] = None
    ) -> None:
        if not self._custom_header_added:
            self._custom_header_added = True
            orientation = (
                QtCore.Qt.Orientation.Vertical
                if data_in_rows
                else QtCore.Qt.Orientation.Horizontal
            )
            if override_headers is not None and len(override_headers) == len(
                self._headers_by_orientation[orientation]
            ):
                self._custom_header_strs = override_headers[:]
            else:
                self._custom_header_strs = self._headers_by_orientation[orientation][:]
            self._custom_header_is_first_row = not data_in_rows

    def removeCustomHeader(self) -> None:
        if self._custom_header_added:
            if self._custom_header_is_first_row:
                self.removeRow(0)
            else:
                self.removeColumn(0)
            self._custom_header_added = False

    def setDataFrame(self, new_data_frame: pd.DataFrame):
        self.beginResetModel()
        self._table = new_data_frame
        self.endResetModel()

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        if self._table is None:
            return 0
        return self._table.index.size + (
            1 if (self._custom_header_added and self._custom_header_is_first_row) else 0
        )

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        if self._table is None:
            return 0
        return self._table.columns.size + (
            1
            if (self._custom_header_added and not self._custom_header_is_first_row)
            else 0
        )

    def setData(
        self, index, value: typing.Any, role: int = QtCore.Qt.ItemDataRole.DisplayRole
    ) -> bool:
        if index.isValid() and role == QtCore.Qt.ItemDataRole.EditRole:
            i = index.column() if self._custom_header_is_first_row else index.row()
            self._custom_header_strs[i] = value
            self.dataChanged.emit(index, index, [role])
        return super().setData(index, value, role)

    def data(
        self,
        index: QtCore.QModelIndex,
        role: QtCore.Qt.ItemDataRole = QtCore.Qt.ItemDataRole.DisplayRole,
    ):
        if index.isValid():
            if (
                role == QtCore.Qt.ItemDataRole.DisplayRole
                or role == QtCore.Qt.ItemDataRole.EditRole
            ):
                row, col = index.row(), index.column()
                if self._custom_header_added:
                    if self._custom_header_is_first_row:
                        if row == 0:
                            return self._custom_header_strs[col]
                        else:
                            row -= 1
                    else:
                        if col == 0:
                            return self._custom_header_strs[row]
                        else:
                            col -= 1
                return str(self._table.iloc[row, col])
        return None

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: QtCore.Qt.ItemDataRole,
    ):
        if (
            self._table is not None
            and role == QtCore.Qt.DisplayRole
            and orientation in self._headers_by_orientation
        ):
            if self._custom_header_added:
                if (
                    self._custom_header_is_first_row
                    and orientation == QtCore.Qt.Orientation.Vertical
                ) or (
                    not self._custom_header_is_first_row
                    and orientation == QtCore.Qt.Orientation.Horizontal
                ):
                    if section == 0:
                        return "Custom"
                    else:
                        section -= 1
            # fallback to return normal headers (with modified section if need be)
            return self._headers_by_orientation[orientation][
                min(section, len(self._headers_by_orientation[orientation]) - 1)
            ]
        return None

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        flags = (
            super().flags(index)
            & ~QtCore.Qt.ItemFlag.ItemIsEditable
            & ~QtCore.Qt.ItemFlag.ItemIsEnabled
        )
        if self._custom_header_added:
            if (index.row() == 0 and self._custom_header_is_first_row) or (
                index.column() == 0 and not self._custom_header_is_first_row
            ):
                flags |= (
                    QtCore.Qt.ItemFlag.ItemIsEditable | QtCore.Qt.ItemFlag.ItemIsEnabled
                )
        return flags
