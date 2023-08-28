from .createBasePage import CreateBasePage

from ..uiConstants import PageKeys
from ..qtUiFiles import ui_createDataSourceAdd

from ...core.commonGlobals import AlgoSettings, DATA_SOURCES, ACTION_LIST
import typing

from PySide6 import QtWidgets, QtCore

ACTION_TOP_TEXT = "Actions act on data either from data sources and/or events. There are two types of actions, events which take input data and apply a function to output data, and triggers which take input data and determine if a criteria is met to trigger an output function. "


class CreateAddPageBase(CreateBasePage):
    TUTORIAL_RESOURCE_PREFIX = "CreateAdd"

    def __init__(
        self,
        current_config: AlgoSettings,
        skip_page: PageKeys,
        top_text="",
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TUTORIAL_RESOURCE_PREFIX, parent=parent)

        self._ui = ui_createDataSourceAdd.Ui_CreateDataSourceAdd()
        self._ui.setupUi(self)
        if top_text:
            self._ui.topText.setText(top_text)
        self._dataSourcesModel = QtCore.QStringListModel()
        self._ui.dataSourcesView.setModel(self._dataSourcesModel)
        self.next_enabled = False
        self._skip_page: PageKeys = skip_page
        self._ui.addButton.released.connect(self.nextPage)
        self._ui.skipButton.released.connect(
            lambda: self.manualExit.emit(self._skip_page)
        )
        self._ui.removeButton.released.connect(self.removeSelected)

    def save(self) -> None:
        pass

    def validate(self) -> bool:
        return True

    def reset(self) -> None:
        self._ui.skipButton.setEnabled(False)
        self._dataSourcesModel.setStringList([])
        self.getTempConfig().clear()
        return super().reset()

    def setGroupModel(self):
        rows = []
        for k, v in self.getConfigGroup().items():
            rows.append(f"{k} : {v.type_}")
        self._ui.skipButton.setEnabled(len(rows) > 0)
        self._dataSourcesModel.setStringList(rows)

    def loadPage(self):
        super().loadPage()
        self.getTempConfig().clear()
        self.setGroupModel()

    def removeSelected(self):
        selection = self._ui.dataSourcesView.selectionModel().selectedIndexes()
        if len(selection) == 1:
            index = selection[0]
            strings = self._dataSourcesModel.stringList()
            if index.row() >= 0 and index.row() < len(strings):
                if strings[index.row()] in self.getConfigGroup():
                    del self.getConfigGroup()[strings[index.row()]]
                    self.setGroupModel()

    def getTutorialClasses(self) -> typing.List:
        return [self]


class CreateDataSourceAddPage(CreateAddPageBase):
    PAGE_KEY = PageKeys.ADD_DATA_SOURCE
    EXIT = PageKeys.NO_PAGE
    EXIT_LABEL = "Exit Creator"
    GROUP = DATA_SOURCES

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, PageKeys.ADD_ACTION, parent=parent)


class CreateActionAddPage(CreateAddPageBase):
    PAGE_KEY = PageKeys.ADD_ACTION
    EXIT = PageKeys.ADD_DATA_SOURCE
    EXIT_LABEL = "Exit Action Creator"
    GROUP = ACTION_LIST

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config,
            PageKeys.FINAL_CONFIRM,
            top_text=ACTION_TOP_TEXT,
            parent=parent,
        )
        self.back_enabled = False
