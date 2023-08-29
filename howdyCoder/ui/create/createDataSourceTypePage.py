from ...core.dataStructs import AlgoSettings
from .createTypeBasePage import CreateTypeBasePage
from ..uiConstants import PageKeys
from ...core.commonGlobals import (
    DataSourcesTypeEnum,
)
from ...core.commonGlobals import DATA_SOURCES

import typing

from PySide6 import QtWidgets


class CreateDataSourceTypePage(CreateTypeBasePage):
    TYPE_DESCRIPTION = {
        DataSourcesTypeEnum.FUNC.display: """
    Use a given function call as the source of the data. \n
    On the next page you can choose what function to use.
    """,
        DataSourcesTypeEnum.THREADED.display: """
    A more advanced version of Func data source. \n
    Only necessary if the funciton would normally be used in a multithreaded environment.
    """,
        DataSourcesTypeEnum.INPUT.display: """
    Take user input data as the source of the data. \n
    When this option is used, after the program is created, a window can be opened that has the selected input option for inputting user data. \n
    Useful for if you need to tell the program dynamically your own data.
    """,
    }
    PAGE_KEY = PageKeys.DATA_SOURCE_TYPE
    EXIT = PageKeys.ADD_DATA_SOURCE
    EXIT_LABEL = "Exit Data Source Creator"

    TUTORIAL_RESOURCE_PREFIX = "CreateTypeDataSource"

    GROUP = DATA_SOURCES

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config,
            "Data Source Type",
            self.TYPE_DESCRIPTION,
            self.TUTORIAL_RESOURCE_PREFIX,
            parent=parent,
        )
