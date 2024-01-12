from typing import List
from ...core.dataStructs import ProgramTypes, ProgramSettings, ItemSettings, ScriptSettings

from ..qtUiFiles import ui_createWidget
from ..tutorialOverlay import AbstractTutorialClass

from ..util import abstractQt

from PySide6 import QtWidgets, QtCore, QtGui

from dataclass_wizard import asdict
import typing
import copy


class CreateWidget(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    # we are actually emitting a dict, but PySide6 has an error with dict Signals, so change to object
    addProgram = QtCore.Signal(object)
    doesProgramNameExist = QtCore.Signal(str)
    nameExists = QtCore.Signal(bool)

    TUTORIAL_RESOURCE_PREFIX = "None"

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent, f)

        # Load UI file
        self._ui = ui_createWidget.Ui_CreateWidget()
        self._ui.setupUi(self)
        self._creator_type: ProgramTypes = None

        self._ui.createWizard.addItem.connect(self.addItem)

    def setCurrentType(self, type_: str, creator_config: ProgramSettings):
        self._creator_type = ProgramTypes(type_)
        if self._creator_type == ProgramTypes.SCRIPT:
            self._ui.stackedWidget.setCurrentWidget(self._ui.createWizard)
            self._ui.createWizard.setCurrentType(
                self._creator_type,
                creator_config,
                self.doesProgramNameExist,
                self.nameExists,
            )
        else:
            self._ui.stackedWidget.setCurrentWidget(self._ui.algoTopoView)
            if creator_config is not None:
                self._ui.algoTopoView.setConfig(copy.deepcopy(creator_config))

    def getTutorialClasses(self) -> List:
        return [self]

    @QtCore.Slot()
    def addItem(self, config: ItemSettings):
        """
        The create wizard has finished editing and has sent back the finished item config
        If it's a script, then we wrap it in a program settings and emit that
        If it's an algo, we add it to the topoview page and switch to that"""
        if self._creator_type == ProgramTypes.SCRIPT:
            
