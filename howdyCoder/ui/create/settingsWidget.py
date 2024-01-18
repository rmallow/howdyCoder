from ..qtUiFiles import (
    ui_settingsWidgetFrequency,
    ui_settingsWidgetFlatten,
    ui_settingsWidgetContainer,
)

from ..util import abstractQt

from ...core.dataStructs import ItemSettings

from abc import ABC, abstractmethod
from dataclasses import dataclass

from PySide6 import QtWidgets, QtCore


class SettingsWidgetBase(
    ABC,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, ABC),
):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)

    @abstractmethod
    def load(self, item_settings: ItemSettings):
        pass

    @abstractmethod
    def save(self, item_settings: ItemSettings):
        pass


class SettingsWidgetFrequency(SettingsWidgetBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._ui = ui_settingsWidgetFrequency.Ui_SettingsWidgetFrequency()
        self._ui.setupUi(self)

        self._ui.single_shot_check.stateChanged.connect(self.singleShotStateChanged)

    def load(self, item_settings: ItemSettings):
        self._ui.time_edit.setTime(QtCore.QTime(0, 0, 0).addSecs(item_settings.period))
        self._ui.single_shot_check.setChecked(item_settings.single_shot)

    def save(self, item_settings: ItemSettings):
        item_settings.period = max(
            1, QtCore.QTime(0, 0, 0).secsTo(self._ui.time_edit.time())
        )
        item_settings.single_shot = self._ui.single_shot_check.isChecked()

    @QtCore.Slot()
    def singleShotStateChanged(self, _):
        self._ui.time_edit.setEnabled(not self._ui.single_shot_check.isChecked())


class SettingsWidgetFlatten(SettingsWidgetBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._ui = ui_settingsWidgetFlatten.Ui_SettingsWidgetFlatten()
        self._ui.setupUi(self)

    def load(self, item_settings: ItemSettings):
        self._ui.flattened_check.setChecked(item_settings.flatten)

    def save(self, item_settings: ItemSettings):
        item_settings.flatten = self._ui.flattened_check.isChecked()


@dataclass
class SettingsWidgetInfo:
    settings_widget_constructor: SettingsWidgetBase
    label: str = ""
    description: str = ""


class SettingsWidgetContainer(QtWidgets.QWidget):
    def __init__(
        self,
        settings_widget_info: SettingsWidgetInfo,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)
        self._ui = ui_settingsWidgetContainer.Ui_SettingsWidgetContainer()
        self._ui.setupUi(self)

        self._ui.setting_label.setText(settings_widget_info.label)
        self._ui.setting_description.setText(settings_widget_info.description)
        layout = QtWidgets.QVBoxLayout(self._ui.settings_widget)
        self.widget = settings_widget_info.settings_widget_constructor(
            self._ui.settings_widget
        )
        layout.addWidget(self.widget)
        self._ui.settings_widget.setLayout(layout)
