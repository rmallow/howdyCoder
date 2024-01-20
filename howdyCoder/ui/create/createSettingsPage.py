from .createBasePage import CreateBasePage
from . import settingsWidget

from ..qtUiFiles import ui_createSettingsBasePage
from ..uiConstants import PageKeys

from ...core.dataStructs import ItemSettings
from ...core.commonGlobals import ENUM_DISPLAY, ActionTypeEnum, DataSourcesTypeEnum

import typing

from PySide6 import QtWidgets, QtCore

FREQUENCY_LABEL = "Frequency"
DATA_SOURCE_FREQUENCY_DESCRIPTION = """Set how often you'd like to run the data source in the period section or set single shot if you want it to run only once."""
SCIRPT_FREQUENCY_DESCRIPTION = """Set how often you'd like to run the script in the period section or set single shot if you want it to run only once."""

FLATTEN_LABEL = "Flatten"
FLATTEN_DESCRIPTION = "Set if the output should be flattened. If any of the output is lists, flattening will cause each data point to be counted as individual data. If the ouput is a dict and contains multiple lists, flattening will only happen if all lists are the same length."


class CreateSettingsBasePage(CreateBasePage):
    PAGE_KEY = PageKeys.SETTINGS
    TUTORIAL_RESOURCE_PREFIX = "None"

    def __init__(
        self,
        current_config: ItemSettings,
        setting_widget_info_list: typing.List[settingsWidget.SettingsWidgetInfo] = None,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TUTORIAL_RESOURCE_PREFIX, parent=parent)

        self._ui = ui_createSettingsBasePage.Ui_CreateSettingsBasePage()
        self._ui.setupUi(self)

        self._setting_widgets: typing.Dict[str, settingsWidget.SettingsWidgetBase] = {}
        layout = QtWidgets.QVBoxLayout(self._ui.settings_list)
        if setting_widget_info_list is not None:
            for info in setting_widget_info_list:
                self._setting_widgets[
                    info.label
                ] = settingsWidget.SettingsWidgetContainer(info, self._ui.settings_list)
                layout.addWidget(self._setting_widgets[info.label])

    def save(self) -> None:
        for container in self._setting_widgets.values():
            container.widget.save(self.getConfig())

    def loadPage(self) -> None:
        self.showAll()
        self.hideAnyWidgets()
        for container in self._setting_widgets.values():
            container.widget.load(self.getConfig())

    def hideAnyWidgets(self):
        pass

    def showAll(self):
        for container in self._setting_widgets.values():
            container.show()

    def getTutorialClasses(self) -> typing.List:
        return [self]


class CreateSettingsActionPage(CreateSettingsBasePage):
    SETTINGS_WIDGET_INFO_LIST = [
        settingsWidget.SettingsWidgetInfo(
            settingsWidget.SettingsWidgetFlatten, FLATTEN_LABEL, FLATTEN_DESCRIPTION
        )
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, setting_widget_info_list=self.SETTINGS_WIDGET_INFO_LIST, **kwargs
        )

    def hideAnyWidgets(self):
        if self.getConfig().type_ == ActionTypeEnum.TRIGGER.value:
            self._setting_widgets[FLATTEN_LABEL].hide()


class CreateSettingsDataSourcePage(CreateSettingsBasePage):
    SETTINGS_WIDGET_INFO_LIST = [
        settingsWidget.SettingsWidgetInfo(
            settingsWidget.SettingsWidgetFrequency,
            FREQUENCY_LABEL,
            DATA_SOURCE_FREQUENCY_DESCRIPTION,
        ),
        settingsWidget.SettingsWidgetInfo(
            settingsWidget.SettingsWidgetFlatten, FLATTEN_LABEL, FLATTEN_DESCRIPTION
        ),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, setting_widget_info_list=self.SETTINGS_WIDGET_INFO_LIST, **kwargs
        )

    def hideAnyWidgets(self):
        if self.getConfig().type_ == getattr(
            DataSourcesTypeEnum.INPUT, ENUM_DISPLAY, ""
        ):
            self._setting_widgets[FLATTEN_LABEL].hide()
            self._setting_widgets[FREQUENCY_LABEL].hide()


class CreateSettingsScriptPage(CreateSettingsBasePage):
    SETTINGS_WIDGET_INFO_LIST = [
        settingsWidget.SettingsWidgetInfo(
            settingsWidget.SettingsWidgetFrequency,
            FREQUENCY_LABEL,
            SCIRPT_FREQUENCY_DESCRIPTION,
        ),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, setting_widget_info_list=self.SETTINGS_WIDGET_INFO_LIST, **kwargs
        )
