from .uiConstants import GUI_REFRESH_INTERVAL
from .qtUiFiles import ui_algoStatusWidget
from .algoData import AlgoWidgetData

from ..commonUtil import helpers
from ..core.commonGlobals import Modes

from PySide6 import QtWidgets, QtCore, QtGui

import typing
import yaml

COLOR_MAP = {
    Modes.STANDBY: QtCore.Qt.GlobalColor.gray,
    Modes.STARTED: QtCore.Qt.GlobalColor.green,
    Modes.STOPPED: QtCore.Qt.GlobalColor.red,
}


class AlgoStatusWidget(QtWidgets.QWidget):
    def __init__(
        self,
        data: AlgoWidgetData,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)

        self.data: AlgoWidgetData = data
        self._ui = ui_algoStatusWidget.Ui_AlgoStatusWidget()
        self._ui.setupUi(self)
        self._ui.name_label.setText(self.data.name)
        self._ui.save_button.released.connect(self.saveConfig)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.refresh)
        self._timer.start(GUI_REFRESH_INTERVAL)

    @QtCore.Slot()
    def refresh(self):
        """Refresh the widgets displayed valued based on what's in the stored data object"""
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(COLOR_MAP[self.data.mode]))
        self._ui.status_label.setPalette(pal)
        self._ui.status_label.setText(self.data.mode.value)
        self._ui.data_count_value.setText(str(self.data.data_count))
        self._ui.runtime_value.setText(helpers.getStrElapsedTime(self.data.runtime))
        self._ui.remove_button.setEnabled(self.data.mode != Modes.STARTED)
        self._ui.export_button.setEnabled(self.data.mode != Modes.STANDBY)
        self._ui.start_button.setText(
            "Stop" if self.data.mode == Modes.STARTED else "Start"
        )
        self._ui.remove_button.setText(
            "Shutdown" if self.data.mode == Modes.STOPPED else "Remove"
        )

    @QtCore.Slot()
    def saveConfig(self):
        file_path = QtWidgets.QFileDialog.getSaveFileName(filter="Config (*.yml)")
        with open(file_path[0], "w") as yaml_file:
            yaml.dump(
                {self.data.name: self.data.config},
                yaml_file,
                default_flow_style=False,
            )
