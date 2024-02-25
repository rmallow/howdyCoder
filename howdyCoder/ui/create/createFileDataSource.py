from ...core.dataStructs import ItemSettings, DataSourceSettings
from .createBasePage import ItemValidity, CreateBasePage
from ..qtUiFiles import ui_createFileDataSource

from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt, helperData
from .. import editableTable
from ..selectorWidget import SelectorWidget
from ..pathSelector import PathSelector


from ...commonUtil import helpers, astUtil, fileLoaders
from ...core.commonGlobals import (
    ENUM_DISPLAY,
    DATA_SOURCES,
    PathType,
    DataSourcesTypeEnum,
    InputType,
)
import typing
import pathlib
import pandas as pd


from PySide6 import QtWidgets, QtCore, QtGui

CSV_EXT = ".csv"


class CreateFileDataSource(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):

    TUTORIAL_RESOURCE_PREFIX_FUNC = "CreateSettingsDataSource"

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX_FUNC, parent=parent)
        self._ui = ui_createFileDataSource.Ui_CreateFileDataSource()
        self._ui.setupUi(self)
        self.parent_page: CreateBasePage = None

        self._file_selector = PathSelector(PathType.FILE, self)
        self._file_selector_widget = SelectorWidget(
            None, self._file_selector, self._ui.selector_widget_box
        )
        self._ui.selector_widget_box.setLayout(
            QtWidgets.QVBoxLayout(self._ui.selector_widget_box)
        )
        self._table_model = QtGui.QStandardItemModel(self._ui.file_view)
        self._ui.file_view.setModel(self._table_model)
        self._ui.file_view.verticalHeader().setSectionsClickable(False)
        self._ui.selector_widget_box.layout().addWidget(self._file_selector_widget)
        self._file_selector.itemSelected.connect(self.fileSelected)

    def loadPage(self) -> None:
        pass

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {}

    def reset(self) -> None:
        pass

    def save(self) -> None:
        pass

    def getTutorialClasses(self) -> typing.List:
        return []

    def fileSelected(self, path_data: helperData.PathWithHelperData) -> None:
        path = pathlib.Path(path_data.path)
        if not any(path.suffix == file_type for file_type in self.LOADERS):
            self._ui.file_status_label.setText(
                f"Loading file of type: {path.suffix} not currently supported"
            )
            return
        else:
            data = self.LOADERS[path.suffix](path.absolute())
            self.OUTPUT_SETUP[path.suffix](self, data)

    def setExcelHeaders(self):
        self._table_model.setVerticalHeaderLabels(
            [str(x) for x in range(1, self._table_model.rowCount() + 1)]
        )
        curr, horiz_labels = [-1], []
        for _ in range(self._table_model.columnCount()):
            curr[0] += 1
            for x in range(len(curr)):
                if curr[x] == 26:
                    curr[x] = 0
                    if x == len(curr) - 1:
                        curr.append(-1)
                    curr[x + 1] += 1
                else:
                    break
            horiz_labels.append("".join([chr(ord("A") + c) for c in curr[::-1]]))
        self._table_model.setHorizontalHeaderLabels(horiz_labels)

    def setupCsv(self, data: typing.List[typing.List[str]]):
        self._table_model.clear()
        for row in data:
            self._table_model.appendRow(
                [QtGui.QStandardItem(item_str) for item_str in row]
            )
        self.setExcelHeaders()

    LOADERS = {CSV_EXT: fileLoaders.loadCSV}
    OUTPUT_SETUP = {CSV_EXT: setupCsv}
