from __future__ import annotations
from ..core.dataStructs import AlgoSettings, Modes, ProgramSettings
from .uiConstants import GUI_REFRESH_INTERVAL
from .qtUiFiles import ui_algoStatusWidget
from .programData import ProgramWidgetData
from .tutorialOverlay import AbstractTutorialClass

from .util import abstractQt, qtResourceManager

from ..commonUtil import helpers
from ..core.commonGlobals import DataSourcesTypeEnum, ENUM_DISPLAY, ProgramTypes

from PySide6 import QtWidgets, QtCore, QtGui

import logging
import typing
import yaml
from dataclass_wizard import asdict

LOG_LEVEL_ROLE = QtCore.Qt.ItemDataRole.UserRole


class LoggingListWidgetItem(QtWidgets.QListWidgetItem):
    def __lt__(self, other: LoggingListWidgetItem) -> bool:
        return self.data(LOG_LEVEL_ROLE) < other.data(LOG_LEVEL_ROLE)


LOGGING_LEVEL_TO_ICON = {
    logging.DEBUG: "debug.png",
    logging.INFO: "info.png",
    logging.WARNING: "warning.png",
    logging.ERROR: "error.png",
    logging.CRITICAL: "critical.png",
}


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

        self.updateLogging()

    @QtCore.Slot()
    def saveConfig(self):
        if file_path := QtWidgets.QFileDialog.getSaveFileName(filter="Config (*.yml)")[
            0
        ]:
            with open(file_path, "w") as yaml_file:
                yaml.dump(
                    asdict(self.data.config),
                    yaml_file,
                    default_flow_style=False,
                )

    def getTutorialClasses(self) -> typing.List:
        return [self]

    def updateLogging(self):
        """Updates from proram dict the mpLogging for this program, and adds new widget items if needed"""
        if self.ui.logging_list_widget.count() != len(self.data.logging_count):
            self.ui.logging_list_widget.clear()
            for k, v in self.data.logging_count.items():
                item = LoggingListWidgetItem(
                    qtResourceManager.getResourceByName(
                        "logging", LOGGING_LEVEL_TO_ICON[k]
                    ),
                    str(v),
                )
                item.setData(LOG_LEVEL_ROLE, k)
                item.setData(
                    QtCore.Qt.ItemDataRole.ToolTipRole,
                    logging.getLevelName(k).capitalize(),
                )
                self.ui.logging_list_widget.addItem(item)
        else:
            for x in range(self.ui.logging_list_widget.count()):
                item = self.ui.logging_list_widget.item(x)
                item.setText(str(self.data.logging_count[item.data(LOG_LEVEL_ROLE)]))
