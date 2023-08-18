from .uiConstants import GUI_REFRESH_INTERVAL
from .qtUiFiles import ui_algoStatusWidget
from .algoData import AlgoWidgetData
from .tutorialOverlay import AbstractTutorialClass

from .util import abstractQt

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


class AlgoStatusWidget(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    def __init__(
        self,
        data: AlgoWidgetData,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__("test", parent, f)

        self.data: AlgoWidgetData = data
        self.ui = ui_algoStatusWidget.Ui_AlgoStatusWidget()
        self.ui.setupUi(self)
        self.ui.name_label.setText(self.data.name)
        self.ui.save_button.released.connect(self.saveConfig)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.refresh)
        self._timer.start(GUI_REFRESH_INTERVAL)

    @QtCore.Slot()
    def refresh(self):
        """Refresh the widgets displayed valued based on what's in the stored data object"""
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(COLOR_MAP[self.data.mode]))
        self.ui.status_label.setPalette(pal)
        self.ui.status_label.setText(self.data.mode.value)
        self.ui.data_count_value.setText(str(self.data.data_count))
        self.ui.runtime_value.setText(helpers.getStrElapsedTime(self.data.runtime))
        self.ui.remove_button.setEnabled(self.data.mode != Modes.STARTED)
        self.ui.export_button.setEnabled(self.data.mode != Modes.STANDBY)
        self.ui.start_button.setText(
            "Stop" if self.data.mode == Modes.STARTED else "Start"
        )
        self.ui.remove_button.setText(
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

    def getTutorialClasses(self) -> typing.List:
        return [self]
