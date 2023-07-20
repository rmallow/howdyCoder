from .qtUiFiles import ui_newBlockWidget

import typing

from PySide2 import QtWidgets, QtCore


class NewBlockWidget(QtWidgets.QWidget):
    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)
        # accessed by main window
        self.ui = ui_newBlockWidget.Ui_NewBlockWidget()
        self.ui.setupUi(self)
