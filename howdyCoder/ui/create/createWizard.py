from ...core.dataStructs import (
    ActionSettings,
    DataSourceSettings,
    ItemSettings,
    ProgramSettings,
)
from .createBasePage import CreateBasePage, HelperData, ItemValidity

# various pages
from .createNamePage import CreateNamePage
from .createTypePage import CreateDataSourceTypePage, CreateActionTypePage
from .createDataSourcePage import CreateDataSourcePage
from .createParametersPage import (
    CreateParametersPage,
)
from .createConfirmPage import (
    CreateConfirmPage,
)

from .createSettingsPage import (
    CreateSettingsActionPage,
    CreateSettingsDataSourcePage,
    CreateSettingsScriptPage,
)

from .createActionPage import CreateActionPage
from .createScriptPage import CreateScriptPage

from .algoTopoView import AlgoTopoScene

from ..uiConstants import PageKeys, CreateWizardItemType
from ..qtUiFiles import ui_createWizard
from ..tutorialOverlay import AbstractTutorialClass

from ..util import animations, abstractQt, nonNativeQMessageBox

from PySide6 import QtWidgets, QtCore, QtGui

import typing
import copy


SCRIPT_CREATION_WIDGET_PAGES: typing.List[CreateBasePage] = [
    CreateNamePage,
    CreateScriptPage,
    CreateParametersPage,
    CreateSettingsScriptPage,
    CreateConfirmPage,
]

ACTION_CREATION_WIDGET_PAGES: typing.List[CreateBasePage] = [
    CreateActionTypePage,
    CreateActionPage,
    CreateParametersPage,
    CreateSettingsActionPage,
    CreateConfirmPage,
]


DATA_SOURCE_CREATION_WIDGET_PAGES: typing.List[CreateBasePage] = [
    CreateDataSourceTypePage,
    CreateDataSourcePage,
    CreateParametersPage,
    CreateSettingsDataSourcePage,
    CreateConfirmPage,
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
    addItem = QtCore.Signal(ItemSettings)

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

        self._current_create_widgets_list: typing.List[CreateBasePage] = []
        self._all_create_widget_lists: typing.Dict[
            str, typing.List[CreateBasePage]
        ] = {}

        self._current_exit_page: PageKeys = PageKeys.NO_PAGE
        self._creator_type: CreateWizardItemType = None
        self.helper_data = HelperData()

        self._ui.nextButton.released.connect(self.nextPressed)
        self._ui.backButton.released.connect(self.backPressed)
        self._ui.exitButton.released.connect(self.exitPressed)

        self._current_index: int = 0
        self.current_config: ItemSettings = ItemSettings()
        self._editing_name: str = ""

        self._animation_group = QtCore.QParallelAnimationGroup(self)
        self._graphics_effects = []

        self._skip_pages: typing.Set[PageKeys] = set()

        self.createAllPages()

    def createAllPages(self):
        for type_, widget_class_list in CREATE_WIZARD_ITEM_TYPE_TO_PAGES.items():
            self._all_create_widget_lists[type_] = []
            for widget_class in widget_class_list:
                page: CreateBasePage = widget_class(self.current_config, parent=self)
                page.nextPage.connect(self.nextPressed)
                page.enableBack.connect(self._ui.backButton.setEnabled)
                page.manualExit.connect(self.exitPressed)
                page.setSkipPages.connect(self.setSkipPages)
                page.hide()
                self._all_create_widget_lists[type_].append(page)

    def getCurrentPageList(self):
        return self._all_create_widget_lists.get(self._creator_type, [])

    def loadCreationWidgets(
        self,
        program_settings: ProgramSettings,
        scene: AlgoTopoScene,
    ) -> None:
        """
        Based on the mapping provided use the factory functions to create and load into the list
        """
        assert len(set(v.PAGE_KEY for v in self.getCurrentPageList())) == len(
            self.getCurrentPageList()
        ), "Duplicate Creation Widget Page Keys"
        for page in self.getCurrentPageList():
            page.current_config = self.current_config
            page.helper_data = self.helper_data
            page.creator_type = self._creator_type
            page.editing_name = self._editing_name
            page.program_settings = program_settings
            page.scene = scene
            if page.graphicsEffect():
                page.graphicsEffect().setEnabled(False)
                page.graphicsEffect().deleteLater()
            page.reset()
            page.hide()
        self._current_create_widgets_list = self.getCurrentPageList()

        self._current_index: int = 0
        self.setButtonText()

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
        if self._createWidgetBoxLayout.count():
            self._createWidgetBoxLayout.replaceWidget(
                self._createWidgetBoxLayout.itemAt(0).widget(),
                self._current_create_widgets_list[self._current_index],
            )
        else:
            self._createWidgetBoxLayout.addWidget(
                self._current_create_widgets_list[self._current_index]
            )
        self._current_create_widgets_list[self._current_index].show()
        self._current_create_widgets_list[self._current_index].loadPage()
        self._ui.backButton.setEnabled(
            self._current_index != 0
            and self._current_create_widgets_list[self._current_index].back_enabled
        )
        self._ui.backButton.setEnabled(
            self._current_create_widgets_list[self._current_index].next_enabled
        )

    def changePage(self, new_index: int):
        """Change the page to the given page with an animation, save the current page and check its validity"""
        if new_index >= 0 and new_index < len(self._current_create_widgets_list):
            # disable both the buttons, at the end of the animation they'll be reenabled
            self._ui.nextButton.setEnabled(False)
            self._ui.backButton.setEnabled(False)
            self._ui.exitButton.setEnabled(False)
            currentPage = self._current_create_widgets_list[self._current_index]

            if valid_page := all(
                v != ItemValidity.INVALID for v in currentPage.validate().values()
            ):
                currentPage.save()
            if abs(new_index - self._current_index) == 1:
                """
                Determine what direction we are going (forward or back)
                Then if the new page is one we're supposed to skip, then skip it
                """
                change = new_index - self._current_index
                while self._current_create_widgets_list[
                    new_index
                ].PAGE_KEY in self._skip_pages and (
                    new_index != 0
                    or new_index != len(self._current_create_widgets_list) - 1
                ):
                    self._ui.progressSteps.setCompletedStep(
                        new_index,
                        True,
                    )
                    new_index += change

            # Get keys from the page before the page we are loading and put it in the page we are loading
            if new_index > 0:
                self._current_create_widgets_list[new_index].loadPage()
            animations.fadeStart(
                self._ui.createWidgetBox,
                self._current_create_widgets_list[self._current_index],
                self._current_create_widgets_list[new_index],
                self._createWidgetBoxLayout,
                finishedSlot=lambda: self.animationFinished(new_index),
            )
            self._ui.progressSteps.setCompletedStep(
                self._current_index,
                valid_page,
            )
            self._ui.progressSteps.goTo(new_index)
            self._current_index = new_index
            self.setButtonText()

    def nextPressed(self):
        """Go forward a page, if it's the last page then check for any error and save config"""
        if self._current_index == len(self._current_create_widgets_list) - 1:
            # The main window will change from the create widget to control
            self.addItem.emit(self.current_config)
        else:
            if self._animation_group.state() == self._animation_group.State.Stopped:
                for x in range(self._animation_group.animationCount()):
                    a = self._animation_group.takeAnimation(x)
                    if a:
                        a.deleteLater()
                validated_widgets = self._current_create_widgets_list[
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
                    self._animation_group.setLoopCount(2)
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
            if self._current_index == len(self._current_create_widgets_list) - 1
            else "Next"
        )

    def backPressed(self):
        """Go back a page"""
        self.changePage(self._current_index - 1)
        self._ui.nextButton.setText("Next")

    def animationFinished(self, new_index: int):
        """
        after widget animation is done, enable button and update widget
        """
        self._ui.backButton.setEnabled(
            self._current_create_widgets_list[new_index].back_enabled
        )
        self._ui.nextButton.setEnabled(
            self._current_create_widgets_list[new_index].next_enabled
        )
        self._ui.exitButton.setEnabled(True)
        self._current_create_widgets_list[new_index].update()
        self._current_create_widgets_list[new_index].drawingFix()
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
                len(self._current_create_widgets_list),
            ),
        ):
            self._current_create_widgets_list[x].reset()

    def reset(self):
        self.resetPages(0)
        self.helper_data.clear()
        self._ui.progressSteps.resetDisplay()
        self._skip_pages = set()
        if self.current_config is not None:
            self.current_config.clear()
        for page in self._current_create_widgets_list:
            page.hide()

    def exitPressed(self, exit_page=None):
        self.addItem.emit(None)
        self.reset()

    def getTutorialClasses(self) -> typing.List:
        return [self] + self._current_create_widgets_list[
            self._current_index
        ].getTutorialClasses()

    @QtCore.Slot()
    def setSkipPages(self, skip_pages: typing.List[PageKeys]) -> None:
        self._skip_pages = set(skip_pages)

    def setCurrentWizardType(
        self,
        type_: CreateWizardItemType,
        item_settings: ItemSettings,
        program_settings: ProgramSettings,
        scene: AlgoTopoScene,
    ):
        self._current_index = 0
        self._creator_type = type_
        if item_settings is not None and item_settings.name:
            self._editing_name = item_settings.name
        else:
            self._editing_name = ""
        # must reset before we assign values
        self.reset()
        if item_settings is None:
            self.current_config = CREATE_WIZARD_ITEM_TYPE_TO_SETTING_STRUCT[
                self._creator_type
            ]()
        else:
            self.current_config = copy.deepcopy(item_settings)

        self.loadCreationWidgets(program_settings, scene)
        self.loadProgressSteps()

        # don't want clicking through till animation is over so we disable button on press

        self.loadCurrentPage()

        self._ui.nextButton.setEnabled(True)
        self._ui.exitButton.setEnabled(True)
