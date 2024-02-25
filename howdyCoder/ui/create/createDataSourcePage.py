from ...core.dataStructs import ItemSettings, DataSourceSettings
from .createBasePage import PagePassThrough, ItemValidity
from ..uiConstants import PageKeys
from ..qtUiFiles import ui_createDataSourcePage

from ..util.qtUtil import CompleterDelegate
from .. import editableTable
from ..selectorWidget import SelectorWidget
from ..funcSelector import FuncSelector
from ..treeSelect import UrlTreeSelect
from ..pathSelector import PathSelector

from ..util.helperData import addHelperData

from ...commonUtil import helpers, astUtil
from ...core.commonGlobals import (
    ENUM_DISPLAY,
    DATA_SOURCES,
    PathType,
    DataSourcesTypeEnum,
    InputType,
)
import typing

from PySide6 import QtWidgets, QtCore


class CreateDataSourcePage(PagePassThrough):
    PAGE_KEY = PageKeys.DATA_SOURCE

    TUTORIAL_RESOURCE_PREFIX_FUNC = "CreateSettingsDataSource"
    TUTORIAL_RESOURCE_PREFIX_INPUT = "CreateSettingsInput"

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config, self.TUTORIAL_RESOURCE_PREFIX_FUNC, parent=parent
        )

        self._ui = ui_createDataSourcePage.Ui_CreateDataSourcePage()
        self._ui.setupUi(self)

        self.stacked_widget = self._ui.stacked_widget

        for x in range(self._ui.stacked_widget.count()):
            self._ui.stacked_widget.widget(x).parent_page = self

    def getWidgetForStack(self):
        curr_settings: DataSourceSettings = self.getConfig()
        return_widget = None
        if curr_settings.type_:
            enum_type = helpers.findEnumByAttribute(
                DataSourcesTypeEnum, ENUM_DISPLAY, curr_settings.type_
            )
            if (
                enum_type == DataSourcesTypeEnum.INPUT
                or enum_type == DataSourcesTypeEnum.FUNC
                or enum_type == DataSourcesTypeEnum.THREADED
            ):
                return_widget = self._ui.create_standard_data_source
            elif enum_type == DataSourcesTypeEnum.FILE:
                return_widget = self._ui.create_file_data_source
        return return_widget
