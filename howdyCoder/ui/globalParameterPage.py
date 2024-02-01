from .qtUiFiles import ui_globalParameterPage

from PySide6 import QtWidgets, QtCore, QtGui


class GlobalParameterPage(QtWidgets.QWidget):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)

        self._ui = ui_globalParameterPage.Ui_GlobalParameterPage()
        self._ui.setupUi(self)
