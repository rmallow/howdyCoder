from .createTypeBasePage import CreateTypeBasePage
from ..uiConstants import PageKeys
from ...core.configConstants import (
    DataSourcesTypeEnum,
)
import typing

from PySide6 import QtWidgets


TYPE_DESCRIPTION = {
    DataSourcesTypeEnum.FUNC.display: """
    Use a given function call as the source of the data. \n
    On the next page you can choose what function to use.
    """,
    DataSourcesTypeEnum.THREADED.display: """
    A more advanced version of Func data source. \n
    Only necessary if the funciton would normally be used in a multithreaded environment.
    """,
}


class CreateDataSourceTypePage(CreateTypeBasePage):
    PAGE_KEY = PageKeys.DATA_SOURCE_TYPE
    EXIT = PageKeys.ADD_DATA_SOURCE
    EXIT_LABEL = "Exit Data Source Creator"

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config, "Data Source Type", TYPE_DESCRIPTION, parent=parent
        )
