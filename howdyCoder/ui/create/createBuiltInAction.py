from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt
from .createBasePage import ItemValidity, CreateBasePage
from ..uiConstants import SceneMode

from ..qtUiFiles import ui_createBuiltInAction

from ...core.dataStructs import ActionSettings

import typing
from PySide6 import QtWidgets, QtCore, QtGui


class CreateBuiltInAction(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    def __init__(self, *args, **kwargs):
        super().__init__("None", *args, **kwargs)
        self._ui = ui_createBuiltInAction.Ui_CreateBuiltInAction()
        self._ui.setupUi(self)
        self.parent_page: CreateBasePage = None

    def loadPage(self) -> None:
        curr_settings: ActionSettings = self.parent_page.getConfig()
        self._ui.graphicsView.setScene(self.parent_page.scene)
        self.parent_page.scene.setMode(SceneMode.ACTION, curr_settings.name)
        self.parent_page.scene

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        {}

    def reset(self) -> None:
        pass

    def save(self) -> None:
        pass

    def getTutorialClasses(self) -> typing.List:
        return [self]
