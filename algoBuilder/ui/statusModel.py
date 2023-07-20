from ..core.commonGlobals import UI_GROUP, SEND_TIME, RECEIVE_TIME, BACK_TIME, RUNTIME
from ..commonUtil import mpLogging, helpers

from ..core.message import message

from PySide2 import QtGui, QtCore

SEND_ROW = 0
RECEIVE_ROW = 1
BACK_ROW = 2

_SPECIAL_HANDLING = {
    SEND_TIME: SEND_ROW,
    RECEIVE_TIME: RECEIVE_ROW,
    BACK_TIME: BACK_ROW,
}
_SPECIAL_FORMATTING = {RUNTIME: helpers.getStrElapsedTime}

ROW_TO_KEY_MAP_ROLE = QtCore.Qt.UserRole + 1
NEXT_ROW_ROLE = ROW_TO_KEY_MAP_ROLE + 1


class statusModel(QtGui.QStandardItemModel):
    def receiveData(self, msg: message):
        root = self.invisibleRootItem()
        codeItem = None
        findList = self.findItems(msg.key.sourceCode)
        if len(findList) == 0:
            # code has not been added to table yet, add it now
            codeItem = QtGui.QStandardItem(msg.key.sourceCode)
            codeItem.setData(_SPECIAL_HANDLING.copy(), role=ROW_TO_KEY_MAP_ROLE)
            codeItem.setData(max(_SPECIAL_HANDLING.values()) + 1, role=NEXT_ROW_ROLE)
            root.appendRow(codeItem)
        elif len(findList) == 1:
            codeItem = findList[0]
        else:
            mpLogging.error(
                "Multiple items with same code found",
                description=f"Code: {msg.key.sourceCode}",
                group=UI_GROUP,
            )

        # Set the status color based on the presence of certain fields in details
        statusColor = QtCore.Qt.red
        if RECEIVE_TIME in msg.details:
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
