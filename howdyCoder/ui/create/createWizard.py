from ...core.dataStructs import (
    ActionSettings,
    AlgoSettings,
    DataSourceSettings,
    ItemSettings,
    ScriptSettings,
)
from .createBasePage import CreateBasePage, HelperData, ItemValidity

# various pages
from .createNamePage import CreateNamePage
from .createAddPage import CreateActionAddPage, CreateDataSourceAddPage
from .createTypePage import CreateDataSourceTypePage, CreateActionTypePage
from .createDataSourceSettingsPage import CreateDataSourceSettingsPage
from .createParametersPage import (
    CreateDataSourceParametersPage,
    CreateActionParametersPage,
    CreateScriptParametersPage,
)
from .createConfirmPage import (
    CreateDataSourceConfirmPage,
    CreateActionConfirmPage,
    CreateFinalConfirmPage,
)
from .createActionSettingsPage import CreateActionSettingsPage
from .createScriptSettingsPage import CreateScriptSettingsPage

from ..uiConstants import PageKeys, CreateWizardItemType
from ..qtUiFiles import ui_createWizard
from ..tutorialOverlay import AbstractTutorialClass

from ..util import animations, abstractQt, nonNativeQMessageBox

from ...core.commonGlobals import DATA_SOURCES, ACTION_LIST, ProgramTypes

from PySide6 import QtWidgets, QtCore, QtGui

from dataclass_wizard import asdict
import typing
import copy


SCRIPT_CREATION_WIDGET_PAGES: typing.List[CreateBasePage] = [
    CreateNamePage,
    CreateScriptSettingsPage,
    CreateScriptParametersPage,
    CreateFinalConfirmPage,
]

ACTION_CREATION_WIDGET_PAGES: typing.List[CreateBasePage] = [
    CreateActionTypePage,
    CreateActionSettingsPage,
    CreateActionParametersPage,
    CreateActionConfirmPage,
]


DATA_SOURCE_CREATION_WIDGET_PAGES: typing.List[CreateBasePage] = [
    CreateDataSourceTypePage,
    CreateDataSourceSettingsPage,
    CreateDataSourceParametersPage,
    CreateDataSourceConfirmPage,
]

CREATE_WIZARD_ITEM_TYPE_TO_PAGES: typing.Dict[
    CreateWizardItemType, typing.List[CreateBasePage]
] = {
    CreateWizardItemType.ACTION: ACTION_CREATION_WIDGET_PAGES,
    CreateWizardItemType.SCRIPT: SCRIPT_CREATION_WIDGET_PAGES,
    CreateWizardItemType.DATA_SOURCE: DATA_SOURCE_CREATION_WIDGET_PAGES,
}

CREATE_WIZARD_ITEM_TYPE_TO_SETTING_STRUCT: typing.Dict[CreateWizardItemType, object] = {
    CreateWizardItemType.ACTION: ActionSettings,
    CreateWizardItemType.SCRIPT: ActionSettings,
    CreateWizardItemType.DATA_SOURCE: DataSourceSettings,
}


class CreateWizard(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    # we are actually emitting a dict, but PySide6 has an error with dict Signals, so change to object
    addItem = QtCore.Signal(object)

    TUTORIAL_RESOURCE_PREFIX = "CreateWidget"

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
        self._ui = ui_createWizard.Ui_CreateWizard()
        self._ui.setupUi(self)

        self._createWidgetBoxLayout = QtWidgets.QVBoxLayout(self._ui.createWidgetBox)
        self._createWidgetBoxLayout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self._ui.createWidgetBox.setLayout(self._createWidgetBoxLayout)

        self._create_widgets_list: typing.List[CreateBasePage] = []

        self._current_exit_page: PageKeys = PageKeys.NO_PAGE
        self._creator_type: CreateWizardItemType = None
        self.helper_data = HelperData()

        self._ui.nextButton.released.connect(self.nextPressed)
        self._ui.backButton.released.connect(self.backPressed)
        self._ui.exitButton.released.connect(self.exitPressed)

        self._current_index: int = 0
        self.current_config = None

        self._animation_group = QtCore.QParallelAnimationGroup(self)
        self._graphics_effects = []

    def getCurrentPageList(self):
        return CREATE_WIZARD_ITEM_TYPE_TO_PAGES.get(self._creator_type, [])

    def loadCreationWidgets(
        self,
        parent_signal_name_check: QtCore.Signal,
        parent_signal_name_answer: QtCore.Signal,
    ) -> None:
        """
        Based on the mapping provided use the factory functions to create and load into the list
        """
        assert len(set(v.PAGE_KEY for v in self.getCurrentPageList())) == len(
            self.getCurrentPageList()
        ), "Duplicate Creation Widget Page Keys"
        self._create_widgets_list = []
        for widget_class in self.getCurrentPageList():
            p = widget_class(self.current_config, self)
            p.helper_data = self.helper_data
            p.creator_type = self._creator_type
            if isinstance(p, CreateNamePage):
                p.doesProgramNameExist.connect(parent_signal_name_check)
                parent_signal_name_answer.connect(p.doesNameExistSlot)
            self._create_widgets_list.append(p)
        self._current_index: int = 0

        for w in self._create_widgets_list:
            w.hide()

    def loadProgressSteps(self) -> None:
        """
        Use the keys provided to create the progress steps widget
        """
        steps = [page.PAGE_KEY.value for page in self.getCurrentPageList()]
        self._ui.progressSteps.setSteps(steps)

    def loadCurrentPage(self) -> None:
        """
        Clear out any widgets and set the layout to the current page
        """
        for _ in range(0, self._createWidgetBoxLayout.count()):
            layout_item = self._createWidgetBoxLayout.takeAt(0)
            layout_item.widget().hide()
            layout_item.widget().deleteLater()
        self._createWidgetBoxLayout.addWidget(
            self._create_widgets_list[self._current_index]
        )
        self._create_widgets_list[self._current_index].show()
        self._create_widgets_list[self._current_index].loadPage()
        self._ui.backButton.setEnabled(
            self._current_index != 0
            and self._create_widgets_list[self._current_index].back_enabled
        )
        self._ui.backButton.setEnabled(
            self._create_widgets_list[self._current_index].next_enabled
        )

    def changePage(self, newIndex: int):
        """Change the page to the given page with an animation, save the current page and check its validity"""
        if newIndex >= 0 and newIndex < len(self._create_widgets_list):
            if (
                self._create_widgets_list[self._current_index].GROUP
                != self._create_widgets_list[newIndex].GROUP
            ):
                self.helper_data.clear()
            # disable both the buttons, at the end of the animation they'll be reenabled
            self._ui.nextButton.setEnabled(False)
            self._ui.backButton.setEnabled(False)
            self._ui.exitButton.setEnabled(False)
            currentPage = self._create_widgets_list[self._current_index]

            if valid_page := all(
                v != ItemValidity.INVALID for v in currentPage.validate().values()
            ):
                currentPage.save()
            # Get keys from the page before the page we are loading and put it in the page we are loading
            if newIndex > 0:
                self._create_widgets_list[newIndex].loadPage()
            animations.fadeStart(
                self._ui.createWidgetBox,
                self._create_widgets_list[self._current_index],
                self._create_widgets_list[newIndex],
                self._createWidgetBoxLayout,
                finishedSlot=lambda: self.animationFinished(newIndex),
            )
            self._ui.progressSteps.setCompletedStep(
                self._current_index,
                valid_page,
            )
            self._ui.progressSteps.goTo(newIndex)
            self._current_index = newIndex
            self.setButtonText()

    def nextPressed(self):
        """Go forward a page, if it's the last page then check for any error and save config"""
        if self._current_index == len(self._create_widgets_list) - 1:
            # The main window will change from the create widget to control
            self.addItem.emit(self.current_config)
            self.reset()
        else:
            if self._animation_group.state() == self._animation_group.State.Stopped:
                for x in range(self._animation_group.animationCount()):
                    a = self._animation_group.takeAnimation(x)
                    if a:
                        a.deleteLater()
                validated_widgets = self._create_widgets_list[
                    self._current_index
                ].validate()
                warnings = []
                for widget_or_warning_str, status in validated_widgets.items():
                    if status == ItemValidity.INVALID:
                        self.createColorBlinkAnimation(widget_or_warning_str)
                    elif status == ItemValidity.WARNING:
                        warnings.append(widget_or_warning_str)
                if self._animation_group.animationCount() > 0:
                    self._animation_group.finished.connect(self.pageAnimationFinished)
                    self._animation_group.setLoopCount(3)
                    self._animation_group.start()
                else:
                    message_box = None
                    if warnings:
                        message_box = nonNativeQMessageBox.NonNativeQMessageBox(self)
                        message_box.setText("Are you sure you want to continue?")
                        info_text = (
                            "Some warnings have been encountered. Althought not required, it's probably a good idea to fix the warnings:\n"
                            + "\n".join(warnings)
                        )
                        message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        message_box.setInformativeText(info_text)
                        message_box.setStandardButtons(
                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                        )
                        message_box.setDefaultButton(QtWidgets.QMessageBox.No)
                        message_box.setWindowModality(
                            QtCore.Qt.WindowModality.ApplicationModal
                        )
                    if not warnings or message_box.exec() == QtWidgets.QMessageBox.Yes:
                        self.changePage(self._current_index + 1)

    def createColorBlinkAnimation(self, widget):
        """Create color blink animation for a widget and add it to the group"""
        effect = QtWidgets.QGraphicsColorizeEffect(self)
        effect.setColor(QtGui.QColor(255, 0, 0))
        effect.setStrength(0.1)
        self._graphics_effects.append(effect)
        widget.setGraphicsEffect(effect)
        animation = QtCore.QPropertyAnimation(effect, QtCore.QByteArray(b"strength"))
        animation.setStartValue(0.5)
        animation.setEndValue(0)
        animation.setDuration(1200)
        self._animation_group.addAnimation(animation)

    def pageAnimationFinished(self):
        for effect in self._graphics_effects:
            effect: QtWidgets.QGraphicsColorizeEffect
            effect.setEnabled(False)
            effect.deleteLater()
        self._graphics_effects = []

    def setButtonText(self):
        self._ui.nextButton.setText(
            "Finish"
            if self._current_index == len(self._create_widgets_list) - 1
            else "Next"
        )
        self._ui.backButton.setText(
            "Start Over"
            if self._current_index == len(self._create_widgets_list) - 1
            else "Back"
        )

    def backPressed(self):
        """Go back a page"""
        if self._current_index == len(self._create_widgets_list) - 1:
            # The back button/start over button was hit on the last page
            # rest all the pages
            message_box = QtWidgets.QMessageBox(self)
            message_box.setText("Are you sure you want to start over?")
            message_box.setInformativeText("The algo you've made will be deleted.")
            message_box.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            message_box.setDefaultButton(QtWidgets.QMessageBox.No)
            message_box.setWindowModality(
                QtCore.Qt.WindowModality.ApplicationModal
            )  # redundancy for macOS
            if message_box.exec_() == QtWidgets.QMessageBox.No:
                return
            self.reset()
        else:
            self.changePage(self._current_index - 1)
        self._ui.nextButton.setText("Next")
        self._ui.backButton.setText("Back")

    def animationFinished(self, newIndex: int):
        """
        after widget animation is done, enable button and update widget
        """
        self._ui.backButton.setEnabled(self._create_widgets_list[newIndex].back_enabled)
        self._ui.nextButton.setEnabled(self._create_widgets_list[newIndex].next_enabled)
        self._ui.exitButton.setEnabled(True)
        if self._create_widgets_list[newIndex].EXIT_LABEL:
            self._ui.exitButton.setText(self._create_widgets_list[newIndex].EXIT_LABEL)
        if self._create_widgets_list[newIndex].EXIT:
            self._current_exit_page = self._create_widgets_list[newIndex].EXIT
        self._create_widgets_list[newIndex].update()
        self._create_widgets_list[newIndex].drawingFix()
        self._ui.scrollArea.viewport().update()

    @QtCore.Slot()
    def resetPages(self, reset_to_index: int) -> None:
        """
        From the current index to the given index, reset those pages by calling CreateBasePage::reset
        Using min, max in range here as reset_to_index could be before or after current index
        """
        for x in range(
            min(self._current_index, reset_to_index),
            min(
                max(self._current_index, reset_to_index) + 1,
                len(self._create_widgets_list),
            ),
        ):
            self._create_widgets_list[x].reset()

    def reset(self):
        self.resetPages(0)
        self.changePage(0)
        self.helper_data.clear()
        self._ui.progressSteps.resetDisplay()
        if self.current_config is not None:
            self.current_config.clear()

    def exitPressed(self, exit_page=None):
        if exit_page is None:
            exit_page = self._current_exit_page
        if exit_page is PageKeys.NO_PAGE:
            self.reset()
            self.addItem.emit({})
        else:
            index = None
            for i, v in enumerate(self.getCurrentPageList()):
                if v.PAGE_KEY is exit_page:
                    index = i
            if index is not None:
                self.resetPages(index)
                self.changePage(index)

    def getTutorialClasses(self) -> typing.List:
        return [self] + self._create_widgets_list[
            self._current_index
        ].getTutorialClasses()

    def setCurrentType(
        self,
        type_: CreateWizardItemType,
        creator_config: ItemSettings,
        parent_signal_name_check: QtCore.Signal,
        parent_signal_name_answer: QtCore.Signal,
    ):
        for page in self._create_widgets_list:
            page.deleteLater()
        self._creator_type = type_
        # must reset before we assign values
        self.reset()
        if creator_config is None:
            self.current_config = CREATE_WIZARD_ITEM_TYPE_TO_SETTING_STRUCT[
                self._creator_type
            ]()
        else:
            self.current_config = copy.deepcopy(creator_config.settings)

        self.loadCreationWidgets(parent_signal_name_check, parent_signal_name_answer)
        self.loadProgressSteps()
        self.loadCurrentPage()

        # don't want clicking through till animation is over so we disable button on press
        for page in self._create_widgets_list:
            page.nextPage.connect(self.nextPressed)
            page.enableBack.connect(self._ui.backButton.setEnabled)
            page.manualExit.connect(self.exitPressed)

        self._ui.nextButton.setEnabled(True)
        self._ui.exitButton.setEnabled(True)
