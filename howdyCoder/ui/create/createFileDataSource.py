from ...core.dataStructs import ItemSettings, DataSourceSettings
from .createBasePage import ItemValidity, CreateBasePage
from ..qtUiFiles import ui_createFileDataSource
from .fileDataSourceSettings import FileDataSourceSettings
from .customHeaderModels import CustomHeaderStandardModel, CustomHeaderLOLModel

from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt, helperData
from ..selectorWidget import SelectorWidget
from ..pathSelector import PathSelector
from ..util import expander


from ...commonUtil import helpers, fileLoaders
from ...core.commonGlobals import (
    PathType,
)
import typing
import pathlib


from PySide6 import QtWidgets, QtCore, QtGui

CSV_EXT = ".csv"
EXCEL_EXT_LIST = [".xlsx", ".xlsm", ".xls", ".xlsb", ".ods"]


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
        self._ui.selector_widget_box.layout().addWidget(self._file_selector_widget)
        self._file_selector.itemSelected.connect(self.fileSelected)

        self._hz_expander = expander.HorizontalExpander(
            self._ui.file_view_box,
            "Settings",
            animation_end_value=self._ui.file_view.sizeHint().width() // 3,
        )
        layout = QtWidgets.QVBoxLayout()
        self._settings_widget = FileDataSourceSettings(self._hz_expander)
        self._settings_widget.headerSettingsChanged.connect(self.headerSettingsChanged)
        self._settings_widget.sheetSettingsChanged.connect(self.sheetSettingsChanged)
        layout.addWidget(self._settings_widget)
        self._hz_expander.setContentLayout(layout)
        self._ui.file_view_box.layout().addWidget(self._hz_expander, 1)
        """We just want to open then close it so it's in the default closed position, hacky"""
        self._hz_expander.toggleButton.click()
        self._hz_expander.toggleButton.click()

        self._standard_model = CustomHeaderStandardModel()
        self._standard_model.dataChanged.connect(self.setExampleHeaders)

        self._lol_model = CustomHeaderLOLModel()
        self._lol_model.dataChanged.connect(self.setExampleHeaders)

        self._abs_path: pathlib.Path = None
        self._current_file_type: str = ""
        self._added_custom_headers = False
        self._custom_header_is_first_row = False
        self._secondary_key: str = ""
        self._file_data = None
        self._override_headers = []

    def loadPage(self) -> None:
        curr: DataSourceSettings = self.parent_page.getConfig()
        if curr.key:
            self._settings_widget.setCustomHeader(curr.custom_headers)
            self._settings_widget.setDataInRows(curr.data_in_rows)
            self._secondary_key = curr.secondary_key
            self._override_headers = curr.output
            self._file_selector_widget.updateText(curr.key)
            self.loadFile(curr.key)

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {self._file_selector_widget: ItemValidity.getEnum(str(self._abs_path))}

    def reset(self) -> None:
        self._standard_model.clear()
        self._lol_model.clear()
        self._settings_widget.reset()
        self._file_selector_widget.reset()

    def save(self) -> None:
        curr: DataSourceSettings = self.parent_page.getConfig()
        curr.key = str(self._abs_path)
        curr.custom_headers = self._settings_widget.getCustomHeaderSet()
        curr.data_in_rows = self._settings_widget.getDataInRows()
        curr.output = self.getHeaders()
        curr.secondary_key = self._secondary_key

    def getTutorialClasses(self) -> typing.List:
        return []

    def fileSelected(self, path_data: helperData.PathWithHelperData) -> None:
        self._settings_widget.reset()
        self.loadFile(path_data.path)

    def loadFile(self, path_str: str) -> None:
        self._abs_path = pathlib.Path(path_str).resolve()
        if not self._abs_path.is_file():
            self._ui.file_status_label.setText(
                f"File at path: {str(self._abs_path)} could not be found."
            )
        else:
            if not any(self._abs_path.suffix == file_type for file_type in LOADERS):
                self._ui.file_status_label.setText(
                    f"Loading file of type: {self._abs_path.suffix} not currently supported"
                )
            else:
                self._current_file_type = self._abs_path.suffix
                try:
                    open_format = "r" + (
                        "b" if self._current_file_type in EXCEL_EXT_LIST else ""
                    )
                    with self._abs_path.open(open_format) as file:
                        self._file_data = LOADERS[self._abs_path.suffix](file)
                        OUTPUT_SETUP[self._abs_path.suffix](self, self._file_data)
                except IOError as e:
                    self._ui.file_status_label.setText(
                        f"Could not open the file at path: {str(self._abs_path)} because {e.strerror}"
                    )

    def headerSettingsChanged(self):
        if self._ui.file_view.model():
            self._ui.file_view.model().removeCustomHeader()
            self.setExcelSettings()

    def sheetSettingsChanged(self):
        self._lol_model.clear()
        self._secondary_key = self._settings_widget.getSheetSelected()
        self.setExcelDataToModel()

    def setExcelSettings(self):
        if (
            self._settings_widget.getCustomHeaderSet()
            and self._ui.file_view.model() is not None
        ):
            self._ui.file_view.model().addCustomHeader(
                self._settings_widget.getDataInRows(), self._override_headers
            )
            self._override_headers = []

        self._ui.file_view.horizontalHeader().setProperty(
            "highlightHeader", not self._settings_widget.getDataInRows()
        )
        self._ui.file_view.verticalHeader().setProperty(
            "highlightHeader", self._settings_widget.getDataInRows()
        )
        for w in [
            self._ui.file_view.horizontalHeader(),
            self._ui.file_view.verticalHeader(),
        ]:
            w.style().unpolish(w)
            w.style().polish(w)
        self.setExampleHeaders()

    def setExcelHeaders(self):
        if self._ui.file_view.model():
            self._ui.file_view.model().setVerticalHeaderLabels(
                [str(x) for x in range(1, self._ui.file_view.model().rowCount() + 1)]
            )
            curr, horiz_labels = [-1], []
            for _ in range(self._ui.file_view.model().columnCount()):
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
            self._ui.file_view.model().setHorizontalHeaderLabels(horiz_labels)

    def setExcelDataToModel(self):
        if self._secondary_key in self._file_data:
            self._lol_model.setTable(self._file_data[self._secondary_key])
        self.setExcelHeaders()
        self.setExcelSettings()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """Setting how far out the settings box should expand to"""
        ret_val = super().resizeEvent(event)
        self._hz_expander.setContentLayoutAnimationEndValue(
            self._ui.file_view_box.size().width() // 3
        )
        return ret_val

    def getHeaders(self) -> typing.List[str]:
        headers = []
        if self._ui.file_view.model() is not None:
            # using index to get data here so it works for both abstract and standard
            if self._settings_widget.getDataInRows():
                headers = [
                    self._ui.file_view.model()
                    .index(x, 0)
                    .data(QtCore.Qt.ItemDataRole.DisplayRole)
                    for x in range(self._ui.file_view.model().rowCount())
                ]
            else:
                headers = [
                    self._ui.file_view.model()
                    .index(0, x)
                    .data(QtCore.Qt.ItemDataRole.DisplayRole)
                    for x in range(self._ui.file_view.model().columnCount())
                ]
        return headers

    def setExampleHeaders(self):
        headers = self.getHeaders()[:5]
        self._settings_widget.setExampleHeaderText(
            helpers.listToFormattedString("Example Headers: ", headers)
            if headers
            else ""
        )

    def setupCsv(self, data: typing.List[typing.List[str]]):
        self._standard_model.clear()
        self._secondary_key = ""
        self._ui.file_view.setModel(self._standard_model)
        for row in data:
            self._ui.file_view.model().appendRow(
                [QtGui.QStandardItem(item_str) for item_str in row]
            )
        self.setExcelHeaders()
        self.setExcelSettings()

    def setupExcel(self, data: typing.Dict[str, typing.List[typing.List[typing.Any]]]):
        self._settings_widget.showSheetSettings(True)
        self._settings_widget.setSheetsAvailable(data.keys())
        if self._secondary_key not in data:
            self._secondary_key = next(iter(data.keys()))
        self._settings_widget.setSheetSelected(self._secondary_key)
        self._lol_model.clear()
        self._ui.file_view.setModel(self._lol_model)
        self.setExcelDataToModel()


OUTPUT_SETUP = {k: CreateFileDataSource.setupExcel for k in EXCEL_EXT_LIST} | {
    CSV_EXT: CreateFileDataSource.setupCsv
}
LOADERS = {CSV_EXT: fileLoaders.loadCSV} | {
    k: fileLoaders.loadExcel for k in EXCEL_EXT_LIST
}
