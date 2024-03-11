from ..core.dataStructs import ProgramStatusData, Modes
from ..core.commonGlobals import (
    UI_GROUP,
    MAINFRAME,
)
from ..commonUtil import mpLogging, helpers

from ..core.message import message

from PySide6 import QtGui, QtCore

_SPECIAL_FORMATTING = {"runtime": helpers.getStrElapsedTime}

ROW_TO_KEY_MAP_ROLE = QtCore.Qt.UserRole + 1
NEXT_ROW_ROLE = ROW_TO_KEY_MAP_ROLE + 1


class statusModel(QtGui.QStandardItemModel):
    def receiveData(self, msg: message):
        root = self.invisibleRootItem()
        codeItem = None
        code = msg.key.sourceCode
        findList = self.findItems(code)
        if len(findList) == 0:
            # code has not been added to table yet, add it now
            codeItem = QtGui.QStandardItem(code)
            codeItem.setData({}, role=ROW_TO_KEY_MAP_ROLE)
            codeItem.setData(0, role=NEXT_ROW_ROLE)
            root.appendRow(codeItem)
        elif len(findList) == 1:
            codeItem = findList[0]
        else:
            mpLogging.error(
                "Multiple items with same code found",
                description=f"Code: {code}",
                group=UI_GROUP,
            )

        # Set the status color based on the presence of certain fields in details
        statusColor = QtCore.Qt.red
        if code == MAINFRAME or ProgramStatusData(**msg.details).mode == Modes.RUNNING:
            statusColor = QtCore.Qt.green
        codeItem.setBackground(QtGui.QBrush(statusColor))

        row_to_key_map = codeItem.data(ROW_TO_KEY_MAP_ROLE)
        next_row = codeItem.data(NEXT_ROW_ROLE)
        # Iterate through details and add the items
        for key, value in msg.details.items():
            if key in _SPECIAL_FORMATTING:
                value = _SPECIAL_FORMATTING[key](value)
            elif "time" in str(key).lower() and isinstance(value, float):
                value = helpers.getStrTime(value)
            detailItem = QtGui.QStandardItem(f"{key}: {value}")
            codeItem.setChild(row_to_key_map.get(key, next_row), detailItem)
            if key not in row_to_key_map:
                row_to_key_map[key] = next_row
                next_row += 1
        codeItem.setData(row_to_key_map, ROW_TO_KEY_MAP_ROLE)
        codeItem.setData(next_row, NEXT_ROW_ROLE)
