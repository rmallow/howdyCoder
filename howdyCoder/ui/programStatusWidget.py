from ..core.dataStructs import AlgoSettings, Modes, ProgramSettings
from .uiConstants import GUI_REFRESH_INTERVAL
from .qtUiFiles import ui_algoStatusWidget
from .programData import ProgramWidgetData
from .tutorialOverlay import AbstractTutorialClass

from .util import abstractQt

from ..commonUtil import helpers
from ..core.commonGlobals import DataSourcesTypeEnum, ENUM_DISPLAY, ProgramTypes

from PySide6 import QtWidgets, QtCore, QtGui

import typing
import yaml
from dataclass_wizard import asdict, fromdict

COLOR_MAP = {
    Modes.STANDBY: QtCore.Qt.GlobalColor.gray,
    Modes.STARTED: QtCore.Qt.GlobalColor.green,
    Modes.STOPPED: QtCore.Qt.GlobalColor.red,
}


class ProgramStatusWidget(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    TUTORIAL_RESOURCE_PREFIX = "AlgoStatusWidget"

    def __init__(
        self,
        data: ProgramWidgetData,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent, f)

        self.data: ProgramWidgetData = data
        self.ui = ui_algoStatusWidget.Ui_AlgoStatusWidget()
        self.ui.setupUi(self)
        self.ui.name_label.setText(self.data.name)
        self.ui.save_button.released.connect(self.saveConfig)
        self._input_found = False
        if data.config.type_ == ProgramTypes.ALGO.value:
            for v in data.config.settings.data_sources.values():
                if v.type_ == getattr(DataSourcesTypeEnum.INPUT, ENUM_DISPLAY):
                    self._input_found = True
        elif data.config.type_ == ProgramTypes.SCRIPT:
            self.ui.input_button.hide()
            self.ui.export_button.hide()
            self.ui.feedLengthBox.hide()
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
        self.ui.input_button.setEnabled(
            self._input_found and self.data.mode != Modes.STANDBY
        )
        self.ui.start_button.setText(
            "Stop" if self.data.mode == Modes.STARTED else "Start"
        )
        self.ui.remove_button.setText(
            "Shutdown" if self.data.mode == Modes.STOPPED else "Remove"
        )

    @QtCore.Slot()
    def saveConfig(self):
        if file_path := QtWidgets.QFileDialog.getSaveFileName(filter="Config (*.yml)")[
            0
        ]:
            with open(file_path, "w") as yaml_file:
                yaml.dump(
                    {self.data.config.name: asdict(self.data.config)},
                    yaml_file,
                    default_flow_style=False,
                )

    def getTutorialClasses(self) -> typing.List:
        return [self]
