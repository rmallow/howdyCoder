from .createBasePage import CreateBasePage

from ..uiConstants import PageKeys
from ..qtUiFiles import ui_createDataSourceAdd

from ...core.configConstants import DATA_SOURCES, TYPE, ACTION_LIST

import typing

from PySide6 import QtWidgets, QtCore

ACTION_TOP_TEXT = "Actions act on data either from data sources and/or events. There are two types of actions, events which take input data and apply a function to output data, and triggers which take input data and determine if a criteria is met to trigger an output function. "


class CreateAddPageBase(CreateBasePage):
    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        group: str,
        skip_page: PageKeys,
        top_text="",
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, "test", parent=parent)

        self._ui = ui_createDataSourceAdd.Ui_CreateDataSourceAdd()
        self._ui.setupUi(self)
        if top_text:
            self._ui.topText.setText(top_text)
        self._dataSourcesModel = QtCore.QStringListModel()
        self._ui.dataSourcesView.setModel(self._dataSourcesModel)
        self.next_enabled = False
        self._group = group
        self._skip_page: PageKeys = skip_page
        self._ui.addButton.released.connect(self.nextPage)
        self._ui.skipButton.released.connect(
            lambda: self.manualExit.emit(self._skip_page)
        )
        self._ui.removeButton.released.connect(self.removeSelected)

    def save(self) -> None:
        curr = self.getConfigSection()
        if self._group not in curr:
            curr[self._group] = {}

    def getKeysForNextPage(self) -> typing.Any:
        return [self.config_keys[0], self._group]

    def validate(self) -> bool:
        return True

    def reset(self) -> None:
        self._ui.skipButton.setEnabled(False)
        self._dataSourcesModel.setStringList([])
        self.getTempConfig().clear()
        return super().reset()

    def setGroupModel(self):
        rows = []
        for k, v in self.getConfigSection().get(self._group, {}).items():
            if TYPE in v:
                rows.append(f"{k} : {v[TYPE]}")
        self._ui.skipButton.setEnabled(len(rows) > 0)
        self._dataSourcesModel.setStringList(rows)

    def loadPage(self, keys):
        super().loadPage(keys)
        self.getTempConfig().clear()
        self.setGroupModel()

    def removeSelected(self):
        selection = self._ui.dataSourcesView.selectionModel().selectedIndexes()
        if len(selection) == 1:
            index = selection[0]
            strings = self._dataSourcesModel.stringList()
            if index.row() >= 0 and index.row() < len(strings):
                if strings[index.row()] in self.getConfigSection().get(self._group, {}):
                    del self.getConfigSection()[self._group][strings[index.row()]]
                    self.setGroupModel()

    def getTutorialClasses(self) -> typing.List:
        return [self]


class CreateDataSourceAddPage(CreateAddPageBase):
    PAGE_KEY = PageKeys.ADD_DATA_SOURCE
    EXIT = PageKeys.NO_PAGE
    EXIT_LABEL = "Exit Creator"

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config, DATA_SOURCES, PageKeys.ADD_ACTION, parent=parent
        )


class CreateActionAddPage(CreateAddPageBase):
    PAGE_KEY = PageKeys.ADD_ACTION
    EXIT = PageKeys.ADD_DATA_SOURCE
    EXIT_LABEL = "Exit Action Creator"

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config,
            ACTION_LIST,
            PageKeys.FINAL_CONFIRM,
            top_text=ACTION_TOP_TEXT,
            parent=parent,
        )
        self.back_enabled = False
