from ..core.message import message

import time
import typing

from PySide2 import QtCore

_loggingColumns = ["Time", "Severity", "Key", "Group", "Title"]
_notAvail = "----"


class loggingModel(QtCore.QAbstractTableModel):
    addKey = QtCore.Signal(str)
    addGroup = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logMessages = []
        self.keys = set()
        self.groups = set()

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.logMessages)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(_loggingColumns)

    def data(self, index: QtCore.QModelIndex, role: int) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            return self.logMessages[index.row()][index.column()]
        else:
            return None

    def headerData(
        self, section: int, orientation: QtCore.Qt.Orientation, role: int
    ) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return _loggingColumns[section]
            else:
                return str(section)
        return None

    def receiveData(self, message: message):
        """
        Recieve the logging message from the main model and parse it into a data structure for the Qt Table Model
        Turn logging message into list and add to main list
        """
        self.beginInsertRows(
            QtCore.QModelIndex(), len(self.logMessages), len(self.logMessages)
        )

        messageList = []

        # Time
        messageList.append(
            time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(message.details["created"])
            )
        )

        # Severity
        messageList.append(message.details["levelname"])

        # Key
        key = message.details.get("mpKey", _notAvail)
        if key not in self.keys:
            self.keys.add(key)
            self.addKey.emit(key)
        messageList.append(key)

        # Group
        group = message.details.get("group", _notAvail)
        if group not in self.groups:
            self.groups.add(group)
            self.addGroup.emit(group)
        messageList.append(group)

        # Title
        messageList.append(message.details["msg"])

        # Description
        description = (
            "Location: "
            + message.details["filename"]
            + " : "
            + str(message.details["lineno"])
            + "\n\n"
        )
        description += message.details["msg"]
        if "description" in message.details:
            description += ":\n" + message.details["description"]
        messageList.append(description)

        self.logMessages.append(messageList)
        self.endInsertRows()
