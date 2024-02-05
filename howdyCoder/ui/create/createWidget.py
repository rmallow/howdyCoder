from ..uiConstants import SceneMode
from .createWizard import CreateWizardItemType

from ...core.dataStructs import (
    ProgramTypes,
    ProgramSettings,
    ItemSettings,
    ScriptSettings,
    ActionSettings,
    AlgoSettings,
)

from ...core.commonGlobals import ActionTypeEnum, ENUM_DISPLAY


from ..qtUiFiles import ui_createWidget
from ..tutorialOverlay import AbstractTutorialClass
from ..mainWindowPageBase import MainWindowPageBase

from ..util import abstractQt

from PySide6 import QtWidgets, QtCore, QtGui

import typing
import copy


class CreateWidget(
    AbstractTutorialClass,
    MainWindowPageBase,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    addProgram = QtCore.Signal(ProgramSettings)

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
        self.current_settings: ProgramSettings = None
        self._editing_item: ItemSettings = None

        self._ui.createWizard.addItem.connect(self.addItem)
        self._ui.algoTopoView.openWizard.connect(self.openWizard)
        self._ui.algoTopoView.addItem.connect(self.addItemToSettings)
        self._ui.algoTopoView.removeItem.connect(self.removeItem)
        self._ui.algoTopoView.editItem.connect(self.editItem)
        self._ui.algoTopoView.finished.connect(self.finished)

    def setCurrentProgramType(
        self, type_: str, creator_settings: ProgramSettings | None
    ):
        self.current_settings = creator_settings
        self._creator_type = ProgramTypes(type_)
        if self._creator_type == ProgramTypes.SCRIPT:
            if self.current_settings is None:
                self.current_settings = ProgramSettings(
                    type_,
                    ScriptSettings.DEFAULT_NAME,
                    ScriptSettings(
                        action=ActionSettings(
                            ScriptSettings.DEFAULT_NAME,
                            ActionTypeEnum.SCRIPT.value,
                        )
                    ),
                )
            self.openWizard(self.current_settings.settings.action)
        else:
            if self.current_settings is None:
                self.current_settings = ProgramSettings(
                    type_=type_,
                    name=AlgoSettings.DEFAULT_NAME,
                    settings=AlgoSettings(),
                )
            self._ui.algoTopoView.setConfigFirstTime(self.current_settings)
            self.showTopoView()

    def getTutorialClasses(self) -> typing.List:
        return [self]

    @QtCore.Slot()
    def addItem(self, item_settings: ItemSettings):
        """
        The create wizard has finished editing and has sent back the finished item config
        If it's a script, then we wrap it in a program settings and emit that
        If it's an algo, we add it to the topoview page and switch to that
        """
        copied_settings = copy.deepcopy(item_settings)
        if self._creator_type == ProgramTypes.SCRIPT:
            if item_settings is not None:
                self.addProgram.emit(
                    ProgramSettings(
                        self._creator_type.value,
                        copied_settings.name,
                        ScriptSettings(copied_settings, copied_settings.name),
                    )
                )
            else:
                self.addProgram.emit(None)
        else:
            if item_settings is not None:
                if self._editing_item:
                    self.current_settings.settings.removeItem(self._editing_item)
                self.addItemToSettings(copied_settings)
            self.showTopoView()
        self._editing_item = None

    @QtCore.Slot()
    def finished(self, program_name):
        self.current_settings.name = program_name
        self.current_settings.settings.name = self.current_settings.name
        self.addProgram.emit(self.current_settings)

    @QtCore.Slot()
    def addItemToSettings(self, item_settings: ItemSettings):
        self.current_settings.settings.addItem(item_settings)
        self._ui.algoTopoView.setConfig(self.current_settings)

    @QtCore.Slot()
    def removeItem(self, item_settings: ItemSettings):
        self.current_settings.settings.removeItem(item_settings)
        self._ui.algoTopoView.setConfig(self.current_settings)

    @QtCore.Slot()
    def editItem(self, item_settings: ItemSettings):
        self._editing_item = item_settings
        self.openWizard(item_settings)

    def showTopoView(self):
        self._ui.algoTopoView.scene.setMode(SceneMode.TOPO_VIEW)
        self._ui.stackedWidget.setCurrentWidget(self._ui.algoTopoView)

    @QtCore.Slot()
    def openWizard(self, item_settings: ItemSettings):
        create_wizard_type = CreateWizardItemType.SCRIPT
        if self._creator_type != ProgramTypes.SCRIPT:
            create_wizard_type = (
                CreateWizardItemType.DATA_SOURCE
                if item_settings.isDataSource()
                else CreateWizardItemType.ACTION
            )

        self._ui.createWizard.setCurrentWizardType(
            create_wizard_type,
            item_settings,
            self.current_settings,
            self._ui.algoTopoView.scene,
        )
        self._ui.stackedWidget.setCurrentWidget(self._ui.createWizard)

    def loadMainPage(self):
        pass

    def leaveMainPage(self):
        pass
