from .createBasePage import CreateBasePage

from ..qtUiFiles import ui_createDataSourceConfirmPage
from ..uiConstants import PageKeys
from ..util import createWidgetFuncs
from ...core.dataStructs import ItemSettings


import typing


from PySide6 import QtWidgets, QtCore, QtGui


class CreateConfirmPage(CreateBasePage):
    PAGE_KEY = PageKeys.CONFRIM
    TUTORIAL_RESOURCE_PREFIX = "CreateConfirm"

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, self.TUTORIAL_RESOURCE_PREFIX, parent=parent)

        self._ui = ui_createDataSourceConfirmPage.Ui_CreateDataSourceConfirmPage()
        self._ui.setupUi(self)

    def getConfigForView(self):
        pass

    def loadPage(self) -> None:
        """
        We want the confirm page to only show the section we've been working on.
        """
        super().loadPage()
        config = self.getConfig()
        self._ui.title_label.setText(f"{config.name} : {config.type_}")
        w = QtWidgets.QWidget(self._ui.scrollArea)
        layout = createWidgetFuncs.createLayout(w)
        w.setFont(QtGui.QFont(w.font().family(), 26))
        layout.addWidget(createWidgetFuncs.createWidget(config, w))
        w.setLayout(layout)
        self._ui.scrollArea.setWidget(w)

    def save(self) -> None:
        # saving of the temp config to the full config is done via the confirm button
        pass

    def getTutorialClasses(self) -> typing.List:
        return [self]
